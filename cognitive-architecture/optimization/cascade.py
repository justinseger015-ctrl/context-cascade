"""
Three-MOO Cascade orchestration (Phase-based MOO).

THIS MODULE: Runs multi-objective optimization in 3 phases (A, B, C).
DIFFERENT FROM: cascade_optimizer.py which optimizes across cascade LEVELS
(commands, agents, skills, playbooks).

Phases:
- Phase A: Framework structure optimization (frame selection, VERIX strictness)
- Phase B: Edge case discovery (adversarial testing, failure modes)
- Phase C: Production frontier refinement (final Pareto points)

Each phase runs a full GlobalMOO optimization loop with different objectives.

Key Classes:
- ThreeMOOCascade: Main orchestrator
- CascadePhase: Enum of phases (PHASE_A, PHASE_B, PHASE_C)
- CascadeResult: Result of full cascade run
"""

import os
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Callable
from pathlib import Path
from enum import Enum
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec
from core.runtime import evaluate, create_runtime
from optimization.globalmoo_client import (
    GlobalMOOClient,
    OptimizationOutcome,
    ParetoPoint,
    create_cognitive_project,
)
from optimization.dspy_level2 import DSPyLevel2Optimizer


class CascadePhase(Enum):
    """Phases of the Three-MOO Cascade."""
    PHASE_A = "phase_a"  # Framework structure
    PHASE_B = "phase_b"  # Edge discovery
    PHASE_C = "phase_c"  # Production frontier


@dataclass
class PhaseObjectives:
    """Objectives for each cascade phase."""
    phase: CascadePhase
    primary_objectives: List[str]
    weights: Dict[str, float]
    description: str


# Phase-specific objective configurations
PHASE_OBJECTIVES = {
    CascadePhase.PHASE_A: PhaseObjectives(
        phase=CascadePhase.PHASE_A,
        primary_objectives=["task_accuracy", "token_efficiency"],
        weights={
            "task_accuracy": 0.6,
            "token_efficiency": 0.4,
        },
        description="Optimize frame selection and VERIX settings for baseline performance",
    ),
    CascadePhase.PHASE_B: PhaseObjectives(
        phase=CascadePhase.PHASE_B,
        primary_objectives=["task_accuracy", "edge_robustness"],
        weights={
            "task_accuracy": 0.4,
            "edge_robustness": 0.6,
        },
        description="Find failure modes and expand configuration space",
    ),
    CascadePhase.PHASE_C: PhaseObjectives(
        phase=CascadePhase.PHASE_C,
        primary_objectives=[
            "task_accuracy",
            "token_efficiency",
            "edge_robustness",
            "epistemic_consistency",
        ],
        weights={
            "task_accuracy": 0.35,
            "token_efficiency": 0.2,
            "edge_robustness": 0.2,
            "epistemic_consistency": 0.25,
        },
        description="Refine final Pareto frontier for production modes",
    ),
}


@dataclass
class CascadeResult:
    """Result of a single cascade phase."""

    phase: CascadePhase
    iterations: int
    pareto_points: List[ParetoPoint]
    impact_factors: Dict[str, Dict[int, float]]
    best_config_vector: List[float]
    best_outcomes: Dict[str, float]
    duration_seconds: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase.value,
            "iterations": self.iterations,
            "pareto_points": [
                {"config": p.config_vector, "outcomes": p.outcomes}
                for p in self.pareto_points
            ],
            "impact_factors": self.impact_factors,
            "best_config_vector": self.best_config_vector,
            "best_outcomes": self.best_outcomes,
            "duration_seconds": self.duration_seconds,
            "metadata": self.metadata,
        }

    def get_best_config(self) -> FullConfig:
        """Get best config as FullConfig."""
        return VectorCodec.decode(self.best_config_vector)


@dataclass
class CascadeState:
    """State of the cascade execution."""

    current_phase: CascadePhase
    completed_phases: List[CascadePhase] = field(default_factory=list)
    phase_results: Dict[CascadePhase, CascadeResult] = field(default_factory=dict)
    total_iterations: int = 0
    started_at: float = field(default_factory=time.time)

    def is_complete(self) -> bool:
        """Check if all phases complete."""
        return len(self.completed_phases) == 3


class ThreeMOOCascade:
    """
    Orchestrate three-phase MOO optimization.

    The cascade progressively refines configurations:
    1. Phase A: Find good frame/VERIX combinations
    2. Phase B: Stress test with edge cases
    3. Phase C: Final Pareto frontier for production
    """

    def __init__(
        self,
        globalmoo_client: Optional[GlobalMOOClient] = None,
        l2_optimizer: Optional[DSPyLevel2Optimizer] = None,
        core_corpus: Optional[List[Dict[str, Any]]] = None,
        edge_corpus: Optional[List[Dict[str, Any]]] = None,
        use_mock: bool = True,
    ):
        """
        Initialize cascade orchestrator.

        Args:
            globalmoo_client: GlobalMOO API client
            l2_optimizer: DSPy L2 prompt optimizer
            core_corpus: Standard evaluation tasks
            edge_corpus: Adversarial evaluation tasks
            use_mock: Use mock mode for testing
        """
        self.moo = globalmoo_client or GlobalMOOClient(use_mock=use_mock)
        self.l2 = l2_optimizer or DSPyLevel2Optimizer()
        self.core_corpus = core_corpus or []
        self.edge_corpus = edge_corpus or []

        self._state: Optional[CascadeState] = None
        self._storage_dir = Path(__file__).parent.parent / "storage" / "cascade"
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        max_iterations_per_phase: int = 100,
        early_stop_threshold: float = 0.95,
        callback: Optional[Callable[[CascadePhase, int, Dict[str, float]], None]] = None,
    ) -> List[CascadeResult]:
        """
        Run full three-phase cascade.

        Args:
            max_iterations_per_phase: Max iterations per phase
            early_stop_threshold: Stop early if best score exceeds this
            callback: Optional callback for progress updates

        Returns:
            List of phase results
        """
        self._state = CascadeState(current_phase=CascadePhase.PHASE_A)
        results = []

        # Phase A: Framework Structure
        phase_a_result = self._run_phase_a(
            max_iterations_per_phase,
            early_stop_threshold,
            callback,
        )
        results.append(phase_a_result)
        self._state.completed_phases.append(CascadePhase.PHASE_A)
        self._state.phase_results[CascadePhase.PHASE_A] = phase_a_result

        # Phase B: Edge Discovery (seeded from Phase A)
        self._state.current_phase = CascadePhase.PHASE_B
        phase_b_result = self._run_phase_b(
            max_iterations_per_phase,
            early_stop_threshold,
            phase_a_result.pareto_points,
            callback,
        )
        results.append(phase_b_result)
        self._state.completed_phases.append(CascadePhase.PHASE_B)
        self._state.phase_results[CascadePhase.PHASE_B] = phase_b_result

        # Phase C: Production Frontier
        self._state.current_phase = CascadePhase.PHASE_C
        phase_c_result = self._run_phase_c(
            max_iterations_per_phase,
            early_stop_threshold,
            phase_b_result.pareto_points,
            callback,
        )
        results.append(phase_c_result)
        self._state.completed_phases.append(CascadePhase.PHASE_C)
        self._state.phase_results[CascadePhase.PHASE_C] = phase_c_result

        # Save results
        self._save_results(results)

        return results

    def _run_phase_a(
        self,
        max_iterations: int,
        early_stop: float,
        callback: Optional[Callable],
    ) -> CascadeResult:
        """
        Phase A: Framework Structure Optimization.

        Focus: Find which frames and VERIX settings work best for accuracy + efficiency.
        """
        start_time = time.time()
        objectives = PHASE_OBJECTIVES[CascadePhase.PHASE_A]

        # Create project for this phase
        project = create_cognitive_project(
            self.moo,
            name="cascade-phase-a-structure",
        )

        # Generate initial seed configs
        seed_outcomes = self._generate_seed_outcomes(
            corpus=self.core_corpus,
            count=10,
        )
        self.moo.load_cases(project.project_id, seed_outcomes)

        # Optimization loop
        best_vector = seed_outcomes[0].config_vector if seed_outcomes else VectorCodec.encode(FullConfig())
        best_score = 0.0

        for iteration in range(max_iterations):
            # Get suggestions
            target = {"task_accuracy": 0.95, "token_efficiency": 0.8}
            suggestions = self.moo.suggest_inverse(
                project.project_id,
                target,
                num_suggestions=3,
            )

            # Evaluate suggestions
            for suggestion in suggestions:
                outcome = self._evaluate_config(
                    suggestion,
                    self.core_corpus[:20],  # Use subset for speed
                )
                self.moo.report_outcome(project.project_id, outcome)

                # Track best
                weighted_score = self._weighted_score(outcome.outcomes, objectives.weights)
                if weighted_score > best_score:
                    best_score = weighted_score
                    best_vector = suggestion

                if callback:
                    callback(CascadePhase.PHASE_A, iteration, outcome.outcomes)

            # Early stop check
            if best_score >= early_stop:
                break

        # Get final Pareto frontier
        pareto = self.moo.get_pareto_frontier(project.project_id)
        impact = self.moo.get_impact_factors(project.project_id)

        return CascadeResult(
            phase=CascadePhase.PHASE_A,
            iterations=iteration + 1,
            pareto_points=pareto,
            impact_factors=impact,
            best_config_vector=best_vector,
            best_outcomes=self._evaluate_config(best_vector, self.core_corpus[:10]).outcomes,
            duration_seconds=time.time() - start_time,
            metadata={"corpus_size": len(self.core_corpus)},
        )

    def _run_phase_b(
        self,
        max_iterations: int,
        early_stop: float,
        seed_points: List[ParetoPoint],
        callback: Optional[Callable],
    ) -> CascadeResult:
        """
        Phase B: Edge Case Discovery.

        Focus: Stress test with adversarial inputs, find failure modes.
        """
        start_time = time.time()
        objectives = PHASE_OBJECTIVES[CascadePhase.PHASE_B]

        # Create project for this phase
        project = create_cognitive_project(
            self.moo,
            name="cascade-phase-b-edges",
        )

        # Seed with Phase A results
        seed_outcomes = [
            OptimizationOutcome(
                config_vector=p.config_vector,
                outcomes=p.outcomes,
            )
            for p in seed_points
        ]
        if seed_outcomes:
            self.moo.load_cases(project.project_id, seed_outcomes)

        # Best from Phase A
        best_vector = seed_points[0].config_vector if seed_points else VectorCodec.encode(FullConfig())
        best_score = 0.0

        for iteration in range(max_iterations):
            # Target edge robustness
            target = {"task_accuracy": 0.85, "edge_robustness": 0.9}
            suggestions = self.moo.suggest_inverse(
                project.project_id,
                target,
                num_suggestions=3,
            )

            for suggestion in suggestions:
                # Use edge corpus for evaluation
                outcome = self._evaluate_config(
                    suggestion,
                    self.edge_corpus if self.edge_corpus else self.core_corpus[:10],
                )
                self.moo.report_outcome(project.project_id, outcome)

                weighted_score = self._weighted_score(outcome.outcomes, objectives.weights)
                if weighted_score > best_score:
                    best_score = weighted_score
                    best_vector = suggestion

                if callback:
                    callback(CascadePhase.PHASE_B, iteration, outcome.outcomes)

            if best_score >= early_stop:
                break

        pareto = self.moo.get_pareto_frontier(project.project_id)
        impact = self.moo.get_impact_factors(project.project_id)

        return CascadeResult(
            phase=CascadePhase.PHASE_B,
            iterations=iteration + 1,
            pareto_points=pareto,
            impact_factors=impact,
            best_config_vector=best_vector,
            best_outcomes=self._evaluate_config(best_vector, self.edge_corpus[:10] if self.edge_corpus else []).outcomes,
            duration_seconds=time.time() - start_time,
            metadata={"edge_corpus_size": len(self.edge_corpus)},
        )

    def _run_phase_c(
        self,
        max_iterations: int,
        early_stop: float,
        seed_points: List[ParetoPoint],
        callback: Optional[Callable],
    ) -> CascadeResult:
        """
        Phase C: Production Frontier Refinement.

        Focus: All 4 objectives, final Pareto points for named modes.
        """
        start_time = time.time()
        objectives = PHASE_OBJECTIVES[CascadePhase.PHASE_C]

        project = create_cognitive_project(
            self.moo,
            name="cascade-phase-c-production",
        )

        # Seed with Phase B results
        seed_outcomes = [
            OptimizationOutcome(
                config_vector=p.config_vector,
                outcomes=p.outcomes,
            )
            for p in seed_points
        ]
        if seed_outcomes:
            self.moo.load_cases(project.project_id, seed_outcomes)

        best_vector = seed_points[0].config_vector if seed_points else VectorCodec.encode(FullConfig())
        best_score = 0.0

        # Combined corpus for final evaluation
        combined_corpus = self.core_corpus + self.edge_corpus

        for iteration in range(max_iterations):
            # Target all objectives
            target = {
                "task_accuracy": 0.9,
                "token_efficiency": 0.85,
                "edge_robustness": 0.85,
                "epistemic_consistency": 0.9,
            }
            suggestions = self.moo.suggest_inverse(
                project.project_id,
                target,
                num_suggestions=5,
            )

            for suggestion in suggestions:
                outcome = self._evaluate_config(
                    suggestion,
                    combined_corpus[:30] if combined_corpus else [],
                )
                self.moo.report_outcome(project.project_id, outcome)

                weighted_score = self._weighted_score(outcome.outcomes, objectives.weights)
                if weighted_score > best_score:
                    best_score = weighted_score
                    best_vector = suggestion

                if callback:
                    callback(CascadePhase.PHASE_C, iteration, outcome.outcomes)

            if best_score >= early_stop:
                break

        pareto = self.moo.get_pareto_frontier(project.project_id)
        impact = self.moo.get_impact_factors(project.project_id)

        return CascadeResult(
            phase=CascadePhase.PHASE_C,
            iterations=iteration + 1,
            pareto_points=pareto,
            impact_factors=impact,
            best_config_vector=best_vector,
            best_outcomes=self._evaluate_config(best_vector, combined_corpus[:10] if combined_corpus else []).outcomes,
            duration_seconds=time.time() - start_time,
            metadata={"combined_corpus_size": len(combined_corpus)},
        )

    def _generate_seed_outcomes(
        self,
        corpus: List[Dict[str, Any]],
        count: int = 10,
    ) -> List[OptimizationOutcome]:
        """Generate initial seed outcomes with varied configs."""
        outcomes = []

        # Base configs to try
        from core.config import STRICT_CONFIG, MINIMAL_CONFIG, DEFAULT_CONFIG

        seed_configs = [
            FullConfig(),  # Default
            STRICT_CONFIG,
            MINIMAL_CONFIG,
        ]

        # Add variations
        for i in range(count - len(seed_configs)):
            config = FullConfig()
            # Vary frame activations
            config.framework.morphological = i % 2 == 0
            config.framework.compositional = i % 3 == 0
            seed_configs.append(config)

        for config in seed_configs[:count]:
            vector = VectorCodec.encode(config)
            outcome = self._evaluate_config(vector, corpus[:10] if corpus else [])
            outcomes.append(outcome)

        return outcomes

    def _evaluate_config(
        self,
        config_vector: List[float],
        tasks: List[Dict[str, Any]],
    ) -> OptimizationOutcome:
        """Evaluate a configuration against tasks."""
        outcomes = evaluate(config_vector, tasks)

        return OptimizationOutcome(
            config_vector=config_vector,
            outcomes=outcomes,
            metadata={
                "task_count": len(tasks),
                "timestamp": time.time(),
            },
        )

    def _weighted_score(
        self,
        outcomes: Dict[str, float],
        weights: Dict[str, float],
    ) -> float:
        """Calculate weighted score from outcomes."""
        total = 0.0
        for metric, weight in weights.items():
            total += outcomes.get(metric, 0.0) * weight
        return total

    def _save_results(self, results: List[CascadeResult]) -> None:
        """Save cascade results to disk."""
        filepath = self._storage_dir / f"cascade-{int(time.time())}.json"

        with open(filepath, "w") as f:
            json.dump(
                [r.to_dict() for r in results],
                f,
                indent=2,
            )

    def get_state(self) -> Optional[CascadeState]:
        """Get current cascade state."""
        return self._state


# Factory functions

def create_cascade(
    use_mock: bool = True,
    core_corpus: Optional[List[Dict[str, Any]]] = None,
    edge_corpus: Optional[List[Dict[str, Any]]] = None,
) -> ThreeMOOCascade:
    """Create cascade orchestrator with default settings."""
    return ThreeMOOCascade(
        use_mock=use_mock,
        core_corpus=core_corpus,
        edge_corpus=edge_corpus,
    )
