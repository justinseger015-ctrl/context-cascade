"""
loopctl core - The single authority for Ralph loop decisions.

This module:
1. Finds artifacts produced by the iteration
2. Runs frozen eval harness to produce eval_report.json (authoritative)
3. Calls UnifiedBridge to decide block/allow
4. If block: updates runtime_config.json
5. Returns JSON decision for Ralph stop-hook

INVARIANTS:
- Harness is the ONLY source of truth for metrics
- Bridge is the ONLY writer of runtime_config.json
- Events are append-only
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Add parent paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integration.unified_bridge import (
    UnifiedBridge,
    BridgeInput,
    UnifiedEvent,
    DecisionIntent,
    Plane,
    Timescale,
)


class FrozenHarness:
    """
    Wrapper for the frozen eval harness.

    The harness is the ONLY source of truth for metrics.
    It does NOT self-improve (Goodhart prevention).
    """

    def __init__(self, loop_dir: Path, harness_version: str = "1.0.0"):
        self.loop_dir = Path(loop_dir)
        self.harness_version = harness_version
        self._harness_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        """Compute hash of harness for integrity verification."""
        # In production, this would hash the actual harness code
        return f"frozen_eval_harness_v{self.harness_version}"

    @property
    def current_hash(self) -> str:
        return self._harness_hash

    def verify_integrity(self, expected_hash: Optional[str]) -> bool:
        """Verify harness hasn't been modified."""
        if expected_hash is None:
            return True
        return self._harness_hash == expected_hash

    def grade(self, artifact_path: Path) -> Dict[str, float]:
        """
        Grade an artifact and return metrics.

        This is a simplified implementation. In production, this would:
        1. Run benchmark suites from eval-harness SKILL
        2. Run regression tests
        3. Check human gates

        Returns metrics dict (NOT model-reported).
        """
        if not artifact_path.exists():
            return {
                "task_accuracy": 0.0,
                "token_efficiency": 0.0,
                "edge_robustness": 0.0,
                "epistemic_consistency": 0.0,
                "overall": 0.0,
            }

        # Read artifact content
        content = artifact_path.read_text(errors="ignore")

        # Simple heuristic grading (would be replaced by actual harness)
        metrics = {
            "task_accuracy": self._grade_accuracy(content),
            "token_efficiency": self._grade_efficiency(content),
            "edge_robustness": self._grade_robustness(content),
            "epistemic_consistency": self._grade_epistemic(content),
        }

        # Overall is weighted average
        weights = {
            "task_accuracy": 0.4,
            "token_efficiency": 0.2,
            "edge_robustness": 0.2,
            "epistemic_consistency": 0.2,
        }
        metrics["overall"] = sum(
            metrics[k] * weights[k] for k in weights
        )

        return metrics

    def _grade_accuracy(self, content: str) -> float:
        """Grade task accuracy (simplified)."""
        # Check for completion indicators
        if not content:
            return 0.0
        if len(content) < 100:
            return 0.3
        if "[assert" in content.lower() or "[witnessed" in content.lower():
            return 0.8
        return 0.6

    def _grade_efficiency(self, content: str) -> float:
        """Grade token efficiency (simplified)."""
        # Shorter responses with same quality = more efficient
        word_count = len(content.split())
        if word_count < 50:
            return 0.9
        elif word_count < 200:
            return 0.8
        elif word_count < 500:
            return 0.7
        else:
            return 0.5

    def _grade_robustness(self, content: str) -> float:
        """Grade edge case handling (simplified)."""
        # Check for error handling indicators
        indicators = ["error", "exception", "edge case", "boundary", "validation"]
        count = sum(1 for i in indicators if i in content.lower())
        return min(0.9, 0.5 + count * 0.1)

    def _grade_epistemic(self, content: str) -> float:
        """Grade epistemic consistency (simplified)."""
        # Check for VERIX markers
        verix_markers = ["[assert", "[conf:", "[ground:", "[state:", "[witnessed", "[inferred"]
        count = sum(1 for m in verix_markers if m in content.lower())
        return min(0.95, 0.4 + count * 0.1)


def find_artifact(output_path: Optional[str], loop_dir: Path) -> Path:
    """Find the artifact to grade."""
    if output_path:
        return Path(output_path)

    # Look for common output patterns
    candidates = [
        loop_dir / "output" / "latest.txt",
        loop_dir / "output.txt",
        Path(".claude") / "output.txt",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    # Return a non-existent path (harness will handle)
    return loop_dir / "output" / "latest.txt"


def get_git_head() -> Optional[str]:
    """Get current git HEAD hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def ralph_iteration_complete(
    state_path: str,
    loop_dir: str,
    output_path: Optional[str] = None,
    iteration: Optional[int] = None,
) -> Dict[str, Any]:
    """
    SINGLE AUTHORITY for Ralph loop decisions.

    This function:
    1. Finds the artifact produced
    2. Grades with FROZEN harness (authoritative)
    3. Writes authoritative eval_report.json
    4. Asks bridge (NOT model) for decision
    5. If continue: updates runtime_config.json
    6. Appends event to events.jsonl
    7. Returns decision JSON for Ralph stop-hook

    Args:
        state_path: Path to Ralph state file
        loop_dir: Path to .loop/ directory
        output_path: Optional explicit artifact path
        iteration: Optional iteration number (reads from state if not provided)

    Returns:
        Decision JSON: {"decision": "block|allow", "reason": "..."}
    """
    loop_dir = Path(loop_dir)
    bridge = UnifiedBridge(loop_dir)

    # 1. Load current state
    current_config = bridge.load_runtime_config()
    policy = bridge.load_policy()
    history = bridge.load_history()

    # Get iteration from state or param
    if iteration is None:
        iteration = current_config.get("iteration", 0)

    # 2. Find artifact
    artifact_path = find_artifact(output_path, loop_dir)

    # 3. Grade with FROZEN harness (authoritative)
    harness = FrozenHarness(loop_dir)
    expected_hash = policy.get("harness_hash")

    if not harness.verify_integrity(expected_hash):
        return {
            "decision": "allow",
            "reason": "HALT: Harness integrity check failed",
        }

    harness_metrics = harness.grade(artifact_path)

    # 4. Write authoritative eval report
    eval_report = {
        "_comment": "EVIDENCE TRUTH - Written ONLY by Frozen Eval Harness",
        "_schema_version": "1.0.0",
        "iteration": iteration,
        "timestamp": datetime.now().isoformat(),
        "artifact_path": str(artifact_path),
        "artifact_hash": hashlib.sha256(
            artifact_path.read_bytes() if artifact_path.exists() else b""
        ).hexdigest()[:16],
        "metrics": harness_metrics,
        "harness_version": harness.harness_version,
        "harness_hash": harness.current_hash,
    }
    (loop_dir / "eval_report.json").write_text(json.dumps(eval_report, indent=2))

    # 5. Build bridge input
    task_metadata = {}
    task_meta_path = loop_dir / "task_metadata.json"
    if task_meta_path.exists():
        task_metadata = json.loads(task_meta_path.read_text())

    bridge_input = BridgeInput(
        iteration=iteration,
        artifact_path=str(artifact_path),
        eval_report=eval_report,
        history=history,
        policy=policy,
        task_metadata=task_metadata,
        current_config=current_config,
    )

    # 6. Ask bridge (NOT model) for decision
    next_config = bridge.propose_next_config(bridge_input)

    # 7. Build event
    event = UnifiedEvent(
        task_id=f"ralph_{iteration}",
        plane=Plane.EXECUTION.value,
        timescale=Timescale.MICRO.value,
        iteration=iteration,
        git_head=get_git_head(),
        config={
            "mode": next_config.mode,
            "vector14": next_config.vector14,
            "frames": list(k for k, v in next_config.frames.items() if v),
            "verix_strictness": next_config.verix.get("strictness", "MODERATE"),
        },
        metrics=harness_metrics,
        decision=next_config.decision_intent.value,
        reason="; ".join(next_config.reasons),
        grounds=f"[assert|confident] Decision based on harness metrics [ground:eval_report] [conf:0.95] [state:confirmed]",
    )

    # 8. Always append event (audit trail)
    bridge.append_event(event)

    # 9. Update history
    bridge.update_history(iteration, harness_metrics)

    # 10. Make final decision
    if next_config.decision_intent == DecisionIntent.HALT:
        return {
            "decision": "allow",
            "reason": next_config.reasons[0] if next_config.reasons else "HALT",
        }

    if next_config.decision_intent == DecisionIntent.ESCALATE:
        return {
            "decision": "allow",
            "reason": f"ESCALATE: Human review required. Gates: {next_config.human_gates_triggered}",
        }

    # Continue iteration - write updated config
    bridge.write_config(next_config, iteration + 1, harness_metrics.get("overall", 0))

    return {
        "decision": "block",
        "reason": "CONTINUE_ITERATION",
        "iteration": iteration + 1,
        "metrics": harness_metrics,
    }


def get_status(loop_dir: str) -> Dict[str, Any]:
    """Get current loop status."""
    loop_dir = Path(loop_dir)
    bridge = UnifiedBridge(loop_dir)

    config = bridge.load_runtime_config()
    eval_report = bridge.load_eval_report()
    history = bridge.load_history()
    policy = bridge.load_policy()

    return {
        "current_iteration": config.get("iteration", 0),
        "mode": config.get("mode", "unknown"),
        "exploration_mode": config.get("exploration_mode", "unknown"),
        "last_score": eval_report.get("metrics", {}).get("overall", 0),
        "history_length": len(history),
        "max_iterations": policy.get("max_iterations", 50),
        "regression_threshold": policy.get("regression_threshold", 0.03),
    }


def reset_loop(loop_dir: str) -> Dict[str, Any]:
    """Reset loop state to defaults."""
    loop_dir = Path(loop_dir)
    bridge = UnifiedBridge(loop_dir)

    # Write default config
    default_config = bridge._default_config()
    (loop_dir / "runtime_config.json").write_text(json.dumps({
        "_comment": "CONTROL INPUT - Reset by loopctl",
        "_schema_version": "1.0.0",
        **default_config,
        "updated_at": datetime.now().isoformat(),
    }, indent=2))

    # Reset history
    (loop_dir / "history.json").write_text(json.dumps({
        "_comment": "ITERATION HISTORY - Reset by loopctl",
        "iterations": [],
    }, indent=2))

    return {"status": "reset", "message": "Loop state reset to defaults"}
