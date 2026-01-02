#!/usr/bin/env python3
"""
L1: Prompt Architect Self-Improvement Loop with Telemetry Capture

This script implements the L1 loop from RMIS:
- PA reviews its own SKILL.md and proposes improvements
- Runs 50-task eval after each improvement
- Captures telemetry to TelemetryStore + LanguageEvolution
- Stops when delta < 2% for 3 consecutive iterations

Usage:
    python l1_self_improvement_loop.py [--max-iterations 10] [--threshold 0.02]
"""

import os
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple

# Add paths
SCRIPT_DIR = Path(__file__).parent
COGNITIVE_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(COGNITIVE_DIR))

from optimization.telemetry_schema import ExecutionTelemetry, TelemetryStore
from optimization.language_evolution import LanguageEvolutionOptimizer, create_language_evolver
from optimization.dspy_level1 import TelemetryAggregator, TelemetryPoint

# Import unified harness
from scripts.rmis_telemetry_harness import RMISTelemetry, create_rmis_harness

# Paths
SKILLS_DIR = COGNITIVE_DIR.parent / "skills" / "foundry"
PA_SKILL_PATH = SKILLS_DIR / "prompt-architect" / "SKILL.md"
EVALS_DIR = COGNITIVE_DIR / "evals"
STORAGE_DIR = COGNITIVE_DIR / "storage" / "l1_loop"


@dataclass
class LoopIteration:
    """Record of a single L1 iteration."""
    iteration: int
    timestamp: str
    pass_count: int
    fail_count: int
    pass_rate: float
    delta: float
    failures: List[str]
    improvement_applied: str
    committed: bool
    telemetry_count: int


@dataclass
class L1LoopState:
    """State of the L1 loop."""
    started_at: str = ""
    iterations: List[LoopIteration] = field(default_factory=list)
    baseline_pass_rate: float = 0.0
    current_pass_rate: float = 0.0
    total_telemetry_records: int = 0
    total_verix_patterns: int = 0
    converged: bool = False
    convergence_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "started_at": self.started_at,
            "iterations": [asdict(i) for i in self.iterations],
            "baseline_pass_rate": self.baseline_pass_rate,
            "current_pass_rate": self.current_pass_rate,
            "total_telemetry_records": self.total_telemetry_records,
            "total_verix_patterns": self.total_verix_patterns,
            "converged": self.converged,
            "convergence_reason": self.convergence_reason,
        }


class L1SelfImprovementLoop:
    """
    L1: PA -> PA self-improvement loop.

    The loop:
    1. Run baseline eval (or load from L0)
    2. Analyze failures
    3. Have PA propose improvement to its own SKILL.md
    4. Apply improvement
    5. Re-run eval
    6. If improved: commit. Else: revert.
    7. Capture telemetry
    8. Repeat until delta < threshold for N iterations
    """

    def __init__(
        self,
        max_iterations: int = 10,
        threshold: float = 0.02,
        convergence_count: int = 3,
    ):
        self.max_iterations = max_iterations
        self.threshold = threshold
        self.convergence_count = convergence_count

        # Storage
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        self.state_file = STORAGE_DIR / "l1_state.json"
        self.history_file = STORAGE_DIR / "l1_history.jsonl"

        # Unified RMIS Telemetry Harness (captures for L1-L5)
        self.harness = create_rmis_harness()

        # State
        self.state = L1LoopState(started_at=datetime.now().isoformat())
        self.recent_deltas: List[float] = []

    def run(self) -> L1LoopState:
        """Run the L1 self-improvement loop."""
        print("=" * 70)
        print("L1: PROMPT ARCHITECT SELF-IMPROVEMENT LOOP")
        print("=" * 70)
        print(f"Max iterations: {self.max_iterations}")
        print(f"Convergence threshold: {self.threshold}")
        print(f"Convergence count: {self.convergence_count}")
        print()

        # Start telemetry tracking
        self.harness.start_loop("L1", "prompt-architect")

        # 1. Get baseline
        print("[1] Running baseline evaluation...")
        baseline_result = self._run_eval()
        self.state.baseline_pass_rate = baseline_result["pass_rate"]
        self.state.current_pass_rate = baseline_result["pass_rate"]
        print(f"    Baseline: {baseline_result['passed']}/{baseline_result['total']} "
              f"({baseline_result['pass_rate']:.1%})")
        print(f"    Failures: {baseline_result['failures']}")

        # Store baseline telemetry
        self._capture_telemetry(baseline_result, iteration=0)

        # 2. Improvement loop
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n{'='*70}")
            print(f"ITERATION {iteration}")
            print("=" * 70)

            # 2a. Analyze failures and propose improvement
            print(f"\n[{iteration}.1] Analyzing failures and proposing improvement...")
            improvement = self._propose_improvement(baseline_result["failures"])

            if not improvement:
                print("    No improvement proposed. Stopping.")
                self.state.converged = True
                self.state.convergence_reason = "No improvement proposed"
                break

            print(f"    Proposed: {improvement[:100]}...")

            # 2b. Apply improvement
            print(f"\n[{iteration}.2] Applying improvement to SKILL.md...")
            backup = self._backup_skill()
            applied = self._apply_improvement(improvement)

            if not applied:
                print("    Failed to apply improvement. Skipping iteration.")
                self._restore_skill(backup)
                continue

            # 2c. Re-run eval
            print(f"\n[{iteration}.3] Running evaluation...")
            new_result = self._run_eval()
            new_pass_rate = new_result["pass_rate"]
            delta = new_pass_rate - self.state.current_pass_rate

            print(f"    Result: {new_result['passed']}/{new_result['total']} "
                  f"({new_pass_rate:.1%})")
            print(f"    Delta: {delta:+.1%}")

            # 2d. Decide: commit or revert
            if delta > 0:
                print(f"\n[{iteration}.4] Improvement accepted! Committing...")
                self._commit_improvement(iteration, improvement)
                self.state.current_pass_rate = new_pass_rate
                committed = True
            else:
                print(f"\n[{iteration}.4] No improvement. Reverting...")
                self._restore_skill(backup)
                committed = False

            # 2e. Capture telemetry
            self._capture_telemetry(new_result, iteration=iteration)

            # 2f. Record iteration
            iter_record = LoopIteration(
                iteration=iteration,
                timestamp=datetime.now().isoformat(),
                pass_count=new_result["passed"],
                fail_count=new_result["failed"],
                pass_rate=new_pass_rate,
                delta=delta,
                failures=new_result["failures"],
                improvement_applied=improvement[:200] if committed else "",
                committed=committed,
                telemetry_count=new_result["total"],
            )
            self.state.iterations.append(iter_record)
            self._save_state()

            # 2g. Check convergence
            self.recent_deltas.append(abs(delta))
            if len(self.recent_deltas) >= self.convergence_count:
                recent = self.recent_deltas[-self.convergence_count:]
                if all(d < self.threshold for d in recent):
                    print(f"\n[CONVERGED] Delta < {self.threshold} for "
                          f"{self.convergence_count} iterations")
                    self.state.converged = True
                    self.state.convergence_reason = (
                        f"Delta < {self.threshold} for {self.convergence_count} iterations"
                    )
                    break

            # Update baseline for next iteration
            if committed:
                baseline_result = new_result

        # 3. Complete loop via harness (runs language evolution)
        print(f"\n{'='*70}")
        print("COMPLETING L1 LOOP")
        print("=" * 70)
        loop_summary = self.harness.on_loop_complete(
            loop="L1",
            skill="prompt-architect",
            baseline_pass_rate=self.state.baseline_pass_rate,
            final_pass_rate=self.state.current_pass_rate,
            iterations=len(self.state.iterations),
        )
        self.state.total_verix_patterns = loop_summary.verix_patterns
        print(f"Patterns discovered: {self.state.total_verix_patterns}")

        # 4. Save final state
        self._save_state()
        self._print_summary()

        return self.state

    def _run_eval(self) -> Dict[str, Any]:
        """Run the 50-task evaluation using CLI evaluator."""
        eval_script = EVALS_DIR / "cli_evaluator.py"

        try:
            result = subprocess.run(
                ["python", str(eval_script), "prompt-architect", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
                cwd=str(EVALS_DIR),
            )

            # Parse JSON output
            output = result.stdout.strip()
            if output:
                # Find JSON in output
                for line in output.split("\n"):
                    if line.startswith("{"):
                        data = json.loads(line)
                        return {
                            "passed": data.get("passed", 0),
                            "failed": data.get("failed", 0),
                            "total": data.get("total", 50),
                            "pass_rate": data.get("pass_rate", 0.0),
                            "failures": data.get("failures", []),
                            "results": data.get("results", []),
                        }

            # Fallback: parse text output
            return self._parse_eval_output(result.stdout)

        except subprocess.TimeoutExpired:
            print("    [ERROR] Evaluation timed out")
            return {"passed": 0, "failed": 50, "total": 50, "pass_rate": 0.0, "failures": []}
        except Exception as e:
            print(f"    [ERROR] Evaluation failed: {e}")
            return {"passed": 0, "failed": 50, "total": 50, "pass_rate": 0.0, "failures": []}

    def _parse_eval_output(self, output: str) -> Dict[str, Any]:
        """Parse text output from evaluator."""
        passed = 0
        failed = 0
        failures = []

        for line in output.split("\n"):
            if "PASS" in line:
                passed += 1
            elif "FAIL" in line:
                failed += 1
                # Extract task ID
                if "Evaluating" in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.startswith("PA-") or part.startswith("AC-"):
                            failures.append(part.rstrip("..."))
                            break

        total = passed + failed
        return {
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": passed / total if total > 0 else 0.0,
            "failures": failures,
            "results": [],
        }

    def _propose_improvement(self, failures: List[str]) -> Optional[str]:
        """Use Claude CLI to propose an improvement based on failures."""
        if not failures:
            return None

        # Read current skill
        skill_content = PA_SKILL_PATH.read_text(encoding="utf-8")

        # Read failure details from corpus
        corpus_file = EVALS_DIR / "corpus" / "prompt-architect.json"
        failure_details = []

        if corpus_file.exists():
            corpus = json.loads(corpus_file.read_text())
            for task in corpus.get("tasks", []):
                if task.get("id") in failures:
                    failure_details.append({
                        "id": task["id"],
                        "input": task.get("input", ""),
                        "criteria": task.get("success_criteria", []),
                    })

        # Construct prompt for PA to improve itself
        prompt = f"""You are the Prompt Architect skill. Your task is to improve yourself.

CURRENT SKILL.md (excerpt - first 3000 chars):
```
{skill_content[:3000]}
```

FAILING TASKS ({len(failures)} failures):
{json.dumps(failure_details[:5], indent=2)}

Analyze these failures and propose a SPECIFIC improvement to add to SKILL.md.

Requirements:
1. The improvement must be a new rule, pattern, or constraint
2. It must be formatted as a VERIX-annotated block
3. It should address the root cause of at least 2+ failures
4. Keep it focused and actionable

Output ONLY the improvement text to add (no explanation). Format:
[direct|emphatic] RULE_NAME := {{
  rule: "...",
  rationale: "...",
  ...
}} [ground:witnessed:eval-failures] [conf:0.85]
"""

        try:
            result = subprocess.run(
                ["claude", "--print", "--output-format", "text"],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=120,
                shell=True,
            )

            improvement = result.stdout.strip()
            if improvement and len(improvement) > 50:
                return improvement
            return None

        except Exception as e:
            print(f"    [ERROR] Failed to get improvement: {e}")
            return None

    def _backup_skill(self) -> str:
        """Backup current SKILL.md content."""
        return PA_SKILL_PATH.read_text(encoding="utf-8")

    def _restore_skill(self, backup: str) -> None:
        """Restore SKILL.md from backup."""
        PA_SKILL_PATH.write_text(backup, encoding="utf-8")

    def _apply_improvement(self, improvement: str) -> bool:
        """Apply improvement to SKILL.md."""
        try:
            current = PA_SKILL_PATH.read_text(encoding="utf-8")

            # Find insertion point (before closing section)
            insert_marker = "## OPERATIONAL PROCEDURES"
            if insert_marker not in current:
                insert_marker = "---\n\n## "

            if insert_marker in current:
                parts = current.split(insert_marker, 1)
                new_content = (
                    parts[0] +
                    f"\n\n### L1 Improvement (Iteration {len(self.state.iterations) + 1})\n\n" +
                    improvement +
                    f"\n\n{insert_marker}" +
                    parts[1]
                )
            else:
                # Append to end
                new_content = current + f"\n\n### L1 Improvement\n\n{improvement}\n"

            PA_SKILL_PATH.write_text(new_content, encoding="utf-8")
            return True

        except Exception as e:
            print(f"    [ERROR] Failed to apply improvement: {e}")
            return False

    def _commit_improvement(self, iteration: int, improvement: str) -> None:
        """Commit the improvement to git."""
        try:
            subprocess.run(
                ["git", "add", str(PA_SKILL_PATH)],
                cwd=str(COGNITIVE_DIR.parent),
                capture_output=True,
            )

            commit_msg = f"L1 iteration {iteration}: PA self-improvement\n\n{improvement[:200]}"
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=str(COGNITIVE_DIR.parent),
                capture_output=True,
            )

        except Exception as e:
            print(f"    [WARN] Git commit failed: {e}")

    def _capture_telemetry(self, eval_result: Dict[str, Any], iteration: int) -> None:
        """Capture telemetry from evaluation results via unified harness."""
        results = eval_result.get("results", [])

        for result in results:
            # Use unified harness - captures to all backends
            self.harness.on_eval_complete(
                loop="L1",
                skill="prompt-architect",
                task_id=result.get("task_id", f"PA-{iteration:03d}"),
                iteration=iteration,
                passed=result.get("passed", False),
                output=result.get("output", ""),
                reasoning=result.get("reasoning", ""),
                metrics={
                    "output_quality": result.get("output_quality", 0.8),
                    "verix_compliance": result.get("verix_compliance", 0.85),
                },
            )
            self.state.total_telemetry_records += 1

    def _save_state(self) -> None:
        """Save loop state to disk."""
        with open(self.state_file, "w") as f:
            json.dump(self.state.to_dict(), f, indent=2)

        # Append to history
        with open(self.history_file, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "state": self.state.to_dict(),
            }) + "\n")

    def _print_summary(self) -> None:
        """Print final summary."""
        print(f"\n{'='*70}")
        print("L1 LOOP SUMMARY")
        print("=" * 70)
        print(f"Iterations: {len(self.state.iterations)}")
        print(f"Baseline pass rate: {self.state.baseline_pass_rate:.1%}")
        print(f"Final pass rate: {self.state.current_pass_rate:.1%}")
        print(f"Improvement: {self.state.current_pass_rate - self.state.baseline_pass_rate:+.1%}")
        print(f"Converged: {self.state.converged}")
        print(f"Reason: {self.state.convergence_reason}")
        print(f"Telemetry records: {self.state.total_telemetry_records}")
        print(f"VERIX patterns: {self.state.total_verix_patterns}")
        print(f"\nState saved to: {self.state_file}")


def main():
    parser = argparse.ArgumentParser(description="L1 Self-Improvement Loop")
    parser.add_argument("--max-iterations", type=int, default=10,
                        help="Maximum number of iterations")
    parser.add_argument("--threshold", type=float, default=0.02,
                        help="Convergence threshold (delta)")
    parser.add_argument("--convergence-count", type=int, default=3,
                        help="Number of iterations below threshold to converge")

    args = parser.parse_args()

    loop = L1SelfImprovementLoop(
        max_iterations=args.max_iterations,
        threshold=args.threshold,
        convergence_count=args.convergence_count,
    )

    state = loop.run()

    # Exit code based on improvement
    improvement = state.current_pass_rate - state.baseline_pass_rate
    if improvement > 0:
        print(f"\n[SUCCESS] Improved by {improvement:.1%}")
        sys.exit(0)
    else:
        print(f"\n[NO IMPROVEMENT] Delta: {improvement:.1%}")
        sys.exit(1)


if __name__ == "__main__":
    main()
