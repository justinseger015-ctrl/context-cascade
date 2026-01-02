#!/usr/bin/env python3
"""
RMIS Telemetry Harness - Unified telemetry capture for L1-L5 loops.

Captures telemetry from all dogfooding loops and feeds into:
- TelemetryStore (for Two-Stage Optimizer)
- LanguageEvolutionOptimizer (for VCL pattern discovery)
- TelemetryAggregator (for DSPy Level 1 analysis)

Usage:
    from rmis_telemetry_harness import RMISTelemetry

    harness = RMISTelemetry()
    harness.on_eval_complete(loop="L1", skill="prompt-architect", result=...)
    harness.on_loop_complete(loop="L1")
    harness.finalize()  # Run evolution + export
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from enum import Enum

# Add paths
SCRIPT_DIR = Path(__file__).parent
COGNITIVE_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(COGNITIVE_DIR))

from optimization.telemetry_schema import ExecutionTelemetry, TelemetryStore, TelemetryBatch
from optimization.language_evolution import LanguageEvolutionOptimizer, create_language_evolver
from optimization.dspy_level1 import TelemetryAggregator, TelemetryPoint, DSPyLevel1Analyzer
from core.config import FullConfig, VectorCodec


class LoopPhase(Enum):
    """RMIS loop phases."""
    L0_BASELINE = "L0"
    L1_PA_SELF = "L1"      # PA -> PA
    L2_PA_SF = "L2"        # PA -> SF
    L3_SF_SELF = "L3"      # SF -> SF
    L4_ZIGZAG = "L4"       # SF <-> PA
    L5_AM = "L5"           # PA+SF -> AM
    L6_GLOBAL_PROMPT = "L6"
    L7_GLOBAL_STRUCT = "L7"
    L8_HOOKS = "L8"


@dataclass
class EvalResult:
    """Standardized eval result across all loops."""
    task_id: str
    skill: str
    loop: str
    iteration: int
    passed: bool
    output: str = ""
    reasoning: str = ""
    metrics: Dict[str, float] = field(default_factory=dict)
    config_vector: List[float] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class LoopSummary:
    """Summary of a completed loop."""
    loop: str
    skill: str
    iterations: int
    baseline_pass_rate: float
    final_pass_rate: float
    improvement: float
    total_evals: int
    total_failures: int
    telemetry_records: int
    verix_patterns: int
    started_at: str
    completed_at: str


@dataclass
class RMISSession:
    """A complete RMIS session (L0-L8)."""
    session_id: str
    started_at: str
    loops_completed: List[str] = field(default_factory=list)
    loop_summaries: Dict[str, LoopSummary] = field(default_factory=dict)
    total_telemetry: int = 0
    total_verix_patterns: int = 0
    evolution_runs: int = 0


class RMISTelemetry:
    """
    Unified telemetry harness for RMIS loops L1-L5.

    Captures:
    - Per-eval telemetry -> TelemetryStore
    - VERIX patterns -> LanguageEvolution
    - Aggregated outcomes -> DSPy Level 1

    Triggers:
    - Language evolution after each loop
    - DSPy L1 analysis after L5 completes
    - Two-stage optimization after full RMIS run
    """

    STORAGE_DIR = COGNITIVE_DIR / "storage" / "rmis_telemetry"

    def __init__(self, session_id: Optional[str] = None):
        # Create storage
        self.STORAGE_DIR.mkdir(parents=True, exist_ok=True)

        # Session
        self.session_id = session_id or f"rmis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session = RMISSession(
            session_id=self.session_id,
            started_at=datetime.now().isoformat(),
        )

        # Telemetry backends
        self.telemetry_store = TelemetryStore(
            base_path=str(self.STORAGE_DIR / "executions")
        )
        self.aggregator = TelemetryAggregator(
            storage_dir=self.STORAGE_DIR / "aggregated"
        )
        self.language_evolver = create_language_evolver(
            storage_dir=self.STORAGE_DIR / "language_evolution",
            use_mock_moo=True,
        )
        self.l1_analyzer = DSPyLevel1Analyzer(
            telemetry=self.aggregator,
            proposals_dir=self.STORAGE_DIR / "proposals",
        )

        # Per-loop tracking
        self._current_loop: Optional[str] = None
        self._loop_evals: Dict[str, List[EvalResult]] = {}
        self._loop_start_times: Dict[str, str] = {}

        # Files
        self.session_file = self.STORAGE_DIR / f"{self.session_id}_session.json"
        self.events_file = self.STORAGE_DIR / f"{self.session_id}_events.jsonl"

        print(f"[RMIS Telemetry] Session: {self.session_id}")
        print(f"[RMIS Telemetry] Storage: {self.STORAGE_DIR}")

    def start_loop(self, loop: str, skill: str) -> None:
        """Mark the start of a loop."""
        self._current_loop = loop
        self._loop_evals[loop] = []
        self._loop_start_times[loop] = datetime.now().isoformat()

        self._log_event({
            "type": "loop_start",
            "loop": loop,
            "skill": skill,
            "timestamp": self._loop_start_times[loop],
        })

        print(f"[RMIS] Starting {loop} ({skill})")

    def on_eval_complete(
        self,
        loop: str,
        skill: str,
        task_id: str,
        iteration: int,
        passed: bool,
        output: str = "",
        reasoning: str = "",
        metrics: Optional[Dict[str, float]] = None,
        config_vector: Optional[List[float]] = None,
    ) -> None:
        """
        Called after each eval task completes.

        This is the main entry point for telemetry capture.
        """
        metrics = metrics or {}
        config_vector = config_vector or self._default_config_vector()

        # Create eval result
        result = EvalResult(
            task_id=task_id,
            skill=skill,
            loop=loop,
            iteration=iteration,
            passed=passed,
            output=output,
            reasoning=reasoning,
            metrics=metrics,
            config_vector=config_vector,
        )

        # Track in loop
        if loop not in self._loop_evals:
            self._loop_evals[loop] = []
        self._loop_evals[loop].append(result)

        # 1. Store ExecutionTelemetry
        telemetry = ExecutionTelemetry(
            task_id=task_id,
            timestamp=result.timestamp,
            session_id=self.session_id,
            config_vector=config_vector,
            active_frames=self._extract_frames(config_vector),
            verix_strictness=int(config_vector[7]) if len(config_vector) > 7 else 1,
            compression_level=int(config_vector[8]) if len(config_vector) > 8 else 1,
            task_type=f"{loop}_{skill}",
            task_success=passed,
            aggregate_frame_score=metrics.get("output_quality", 0.5),
            verix_compliance_score=metrics.get("verix_compliance", 0.5),
            skill_name=skill,
            agent_type=f"rmis_{loop}",
        )
        self.telemetry_store.store(telemetry)
        self.session.total_telemetry += 1

        # 2. Feed to aggregator
        self.aggregator.record_outcome(
            config_vector=config_vector,
            outcomes={
                "task_accuracy": 1.0 if passed else 0.0,
                "token_efficiency": metrics.get("token_efficiency", 0.8),
                "edge_robustness": metrics.get("edge_robustness", 0.7),
                "epistemic_consistency": metrics.get("verix_compliance", 0.85),
            },
            task_type=f"{loop}_{skill}",
            metadata={
                "task_id": task_id,
                "iteration": iteration,
                "loop": loop,
            },
        )

        # 3. Feed to language evolution (if output has VERIX claims)
        if output and ("[" in output or "conf:" in output.lower()):
            self.language_evolver.analyze_execution(
                output=output,
                context=skill,
                success=passed,
                config_vector=config_vector,
            )

        # Log event
        self._log_event({
            "type": "eval_complete",
            "loop": loop,
            "skill": skill,
            "task_id": task_id,
            "iteration": iteration,
            "passed": passed,
            "timestamp": result.timestamp,
        })

    def on_loop_complete(
        self,
        loop: str,
        skill: str,
        baseline_pass_rate: float,
        final_pass_rate: float,
        iterations: int,
    ) -> LoopSummary:
        """
        Called when a loop completes.

        Triggers language evolution and creates summary.
        """
        evals = self._loop_evals.get(loop, [])
        failures = [e for e in evals if not e.passed]

        # Create summary
        summary = LoopSummary(
            loop=loop,
            skill=skill,
            iterations=iterations,
            baseline_pass_rate=baseline_pass_rate,
            final_pass_rate=final_pass_rate,
            improvement=final_pass_rate - baseline_pass_rate,
            total_evals=len(evals),
            total_failures=len(failures),
            telemetry_records=len(evals),
            verix_patterns=0,  # Updated after evolution
            started_at=self._loop_start_times.get(loop, ""),
            completed_at=datetime.now().isoformat(),
        )

        # Run language evolution
        print(f"[RMIS] Running language evolution for {loop}...")
        evolution_report = self.language_evolver.evolve()
        summary.verix_patterns = len(evolution_report.get("optimal_verix_patterns", []))
        self.session.total_verix_patterns = summary.verix_patterns
        self.session.evolution_runs += 1

        # Store summary
        self.session.loops_completed.append(loop)
        self.session.loop_summaries[loop] = summary
        self._save_session()

        # Log
        self._log_event({
            "type": "loop_complete",
            "loop": loop,
            "summary": asdict(summary),
        })

        print(f"[RMIS] {loop} complete: {baseline_pass_rate:.1%} -> {final_pass_rate:.1%} "
              f"({summary.improvement:+.1%})")
        print(f"[RMIS] Telemetry: {summary.telemetry_records} records, "
              f"{summary.verix_patterns} patterns")

        return summary

    def on_iteration_complete(
        self,
        loop: str,
        iteration: int,
        pass_rate: float,
        delta: float,
        committed: bool,
    ) -> None:
        """Called after each iteration within a loop."""
        self._log_event({
            "type": "iteration_complete",
            "loop": loop,
            "iteration": iteration,
            "pass_rate": pass_rate,
            "delta": delta,
            "committed": committed,
            "timestamp": datetime.now().isoformat(),
        })

    def finalize(self) -> Dict[str, Any]:
        """
        Finalize the RMIS session.

        - Runs DSPy L1 analysis if enough data
        - Saves all telemetry
        - Returns session summary
        """
        print(f"\n{'='*60}")
        print("FINALIZING RMIS TELEMETRY SESSION")
        print("=" * 60)

        # Save aggregator data
        self.aggregator.save("rmis_telemetry.jsonl")

        # Run DSPy L1 analysis if we have enough data
        proposals = []
        if self.session.total_telemetry >= 50:
            print("\n[RMIS] Running DSPy Level 1 analysis...")
            proposals = self.l1_analyzer.analyze(min_samples=50)
            self.l1_analyzer.save_proposals("l1_proposals.json")
            print(f"[RMIS] Generated {len(proposals)} evolution proposals")

        # Final language evolution
        print("\n[RMIS] Final language evolution...")
        final_evolution = self.language_evolver.evolve()

        # Save session
        self._save_session()

        # Summary
        summary = {
            "session_id": self.session_id,
            "loops_completed": self.session.loops_completed,
            "total_telemetry": self.session.total_telemetry,
            "total_verix_patterns": self.session.total_verix_patterns,
            "evolution_runs": self.session.evolution_runs,
            "l1_proposals": len(proposals),
            "loop_summaries": {
                loop: asdict(s) for loop, s in self.session.loop_summaries.items()
            },
            "language_evolution": {
                "optimal_patterns": final_evolution.get("optimal_verix_patterns", []),
                "frame_combinations": final_evolution.get("optimal_frame_combinations", []),
                "context_mappings": len(final_evolution.get("context_frame_mapping", {})),
            },
            "storage_path": str(self.STORAGE_DIR),
        }

        # Save summary
        summary_file = self.STORAGE_DIR / f"{self.session_id}_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        self._print_summary(summary)

        return summary

    def _default_config_vector(self) -> List[float]:
        """Return default 14-dim config vector."""
        return [
            1.0,  # evidential
            1.0,  # aspectual
            0.5,  # morphological
            0.3,  # compositional
            0.1,  # honorific
            0.5,  # classifier
            0.2,  # spatial
            1.0,  # verix_strictness (MODERATE)
            1.0,  # compression_level (L1)
            1.0,  # require_ground
            0.8,  # require_confidence
            0.7,  # temperature
            0.6,  # coherence_weight
            0.7,  # evidence_weight
        ]

    def _extract_frames(self, config_vector: List[float]) -> List[str]:
        """Extract active frames from config vector."""
        frame_names = [
            "evidential", "aspectual", "morphological",
            "compositional", "honorific", "classifier", "spatial"
        ]
        active = []
        for i, name in enumerate(frame_names):
            if i < len(config_vector) and config_vector[i] > 0.5:
                active.append(name)
        return active

    def _log_event(self, event: Dict[str, Any]) -> None:
        """Append event to events log."""
        with open(self.events_file, "a") as f:
            f.write(json.dumps(event) + "\n")

    def _save_session(self) -> None:
        """Save session state."""
        data = {
            "session_id": self.session.session_id,
            "started_at": self.session.started_at,
            "loops_completed": self.session.loops_completed,
            "loop_summaries": {
                loop: asdict(s) for loop, s in self.session.loop_summaries.items()
            },
            "total_telemetry": self.session.total_telemetry,
            "total_verix_patterns": self.session.total_verix_patterns,
            "evolution_runs": self.session.evolution_runs,
        }
        with open(self.session_file, "w") as f:
            json.dump(data, f, indent=2)

    def _print_summary(self, summary: Dict[str, Any]) -> None:
        """Print final summary."""
        print(f"\n{'='*60}")
        print("RMIS TELEMETRY SESSION SUMMARY")
        print("=" * 60)
        print(f"Session ID: {summary['session_id']}")
        print(f"Loops completed: {', '.join(summary['loops_completed'])}")
        print(f"Total telemetry records: {summary['total_telemetry']}")
        print(f"Total VERIX patterns: {summary['total_verix_patterns']}")
        print(f"Evolution runs: {summary['evolution_runs']}")
        print(f"L1 proposals generated: {summary['l1_proposals']}")

        if summary['loop_summaries']:
            print(f"\nLoop Results:")
            for loop, s in summary['loop_summaries'].items():
                print(f"  {loop}: {s['baseline_pass_rate']:.1%} -> {s['final_pass_rate']:.1%} "
                      f"({s['improvement']:+.1%})")

        print(f"\nLanguage Evolution:")
        le = summary['language_evolution']
        print(f"  Optimal patterns: {len(le['optimal_patterns'])}")
        print(f"  Frame combinations: {len(le['frame_combinations'])}")
        print(f"  Context mappings: {le['context_mappings']}")

        print(f"\nData saved to: {summary['storage_path']}")


# Convenience function for integration
def create_rmis_harness(session_id: Optional[str] = None) -> RMISTelemetry:
    """Create RMIS telemetry harness."""
    return RMISTelemetry(session_id=session_id)


if __name__ == "__main__":
    # Demo usage
    print("RMIS Telemetry Harness Demo")
    print("=" * 50)

    harness = create_rmis_harness()

    # Simulate L1 loop
    harness.start_loop("L1", "prompt-architect")

    for i in range(5):
        harness.on_eval_complete(
            loop="L1",
            skill="prompt-architect",
            task_id=f"PA-{i+1:03d}",
            iteration=1,
            passed=(i % 3 != 0),  # 2/3 pass
            output=f"[assert|neutral] Test output {i} [conf:0.9]",
            metrics={"output_quality": 0.8, "verix_compliance": 0.9},
        )

    harness.on_loop_complete(
        loop="L1",
        skill="prompt-architect",
        baseline_pass_rate=0.6,
        final_pass_rate=0.8,
        iterations=3,
    )

    # Finalize
    summary = harness.finalize()
    print(f"\nDemo complete. Session: {summary['session_id']}")
