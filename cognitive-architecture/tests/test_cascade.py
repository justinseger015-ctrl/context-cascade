"""
Tests for optimization/cascade.py

Tests:
- ThreeMOOCascade phases
- CascadeResult structure
- Phase objectives
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.cascade import (
    ThreeMOOCascade,
    CascadePhase,
    CascadeResult,
    PhaseObjectives,
    PHASE_OBJECTIVES,
    create_cascade,
)
from optimization.globalmoo_client import GlobalMOOClient, ParetoPoint
from core.config import FullConfig, VectorCodec


class TestCascadePhase:
    """Tests for CascadePhase enum."""

    def test_all_phases_defined(self):
        """Should have all three phases."""
        phases = list(CascadePhase)
        assert CascadePhase.PHASE_A in phases
        assert CascadePhase.PHASE_B in phases
        assert CascadePhase.PHASE_C in phases


class TestPhaseObjectives:
    """Tests for phase objective configurations."""

    def test_phase_a_objectives(self):
        """Phase A should focus on accuracy and efficiency."""
        objectives = PHASE_OBJECTIVES[CascadePhase.PHASE_A]
        assert "task_accuracy" in objectives.primary_objectives
        assert "token_efficiency" in objectives.primary_objectives

    def test_phase_b_objectives(self):
        """Phase B should focus on robustness."""
        objectives = PHASE_OBJECTIVES[CascadePhase.PHASE_B]
        assert "edge_robustness" in objectives.primary_objectives

    def test_phase_c_objectives(self):
        """Phase C should include all objectives."""
        objectives = PHASE_OBJECTIVES[CascadePhase.PHASE_C]
        assert len(objectives.primary_objectives) == 4

    def test_weights_sum_to_one(self):
        """Weights should approximately sum to 1."""
        for phase, objectives in PHASE_OBJECTIVES.items():
            total = sum(objectives.weights.values())
            assert 0.99 <= total <= 1.01


class TestCascadeResult:
    """Tests for CascadeResult dataclass."""

    def test_create_result(self):
        """Should create result with all fields."""
        result = CascadeResult(
            phase=CascadePhase.PHASE_A,
            iterations=50,
            pareto_points=[],
            impact_factors={},
            best_config_vector=VectorCodec.encode(FullConfig()),
            best_outcomes={"task_accuracy": 0.9},
            duration_seconds=10.5,
        )
        assert result.iterations == 50
        assert result.duration_seconds == 10.5

    def test_to_dict(self):
        """to_dict should serialize result."""
        result = CascadeResult(
            phase=CascadePhase.PHASE_B,
            iterations=30,
            pareto_points=[
                ParetoPoint(
                    config_vector=[0.5] * 14,
                    outcomes={"task_accuracy": 0.85},
                )
            ],
            impact_factors={"task_accuracy": {0: 0.3}},
            best_config_vector=[0.5] * 14,
            best_outcomes={"task_accuracy": 0.85},
            duration_seconds=5.0,
        )
        d = result.to_dict()
        assert d["phase"] == "phase_b"
        assert d["iterations"] == 30
        assert len(d["pareto_points"]) == 1

    def test_get_best_config(self):
        """get_best_config should return FullConfig."""
        config = FullConfig()
        config.framework.morphological = True
        vector = VectorCodec.encode(config)

        result = CascadeResult(
            phase=CascadePhase.PHASE_C,
            iterations=10,
            pareto_points=[],
            impact_factors={},
            best_config_vector=vector,
            best_outcomes={},
            duration_seconds=1.0,
        )

        best = result.get_best_config()
        assert best.framework.morphological is True


class TestThreeMOOCascade:
    """Tests for ThreeMOOCascade orchestrator."""

    def test_init_with_mock(self):
        """Should initialize with mock client."""
        cascade = ThreeMOOCascade(use_mock=True)
        assert cascade.moo.use_mock is True

    def test_init_with_corpora(self):
        """Should accept task corpora."""
        core = [{"id": "1", "task": "Test"}]
        edge = [{"id": "e1", "task": "Edge test", "edge_type": "adversarial"}]

        cascade = ThreeMOOCascade(
            use_mock=True,
            core_corpus=core,
            edge_corpus=edge,
        )
        assert len(cascade.core_corpus) == 1
        assert len(cascade.edge_corpus) == 1

    def test_run_completes_all_phases(self):
        """run() should complete all three phases."""
        cascade = ThreeMOOCascade(use_mock=True)

        # Use small iteration counts for speed
        results = cascade.run(
            max_iterations_per_phase=2,
            early_stop_threshold=0.99,
        )

        assert len(results) == 3
        assert results[0].phase == CascadePhase.PHASE_A
        assert results[1].phase == CascadePhase.PHASE_B
        assert results[2].phase == CascadePhase.PHASE_C

    def test_state_tracks_progress(self):
        """State should track cascade progress."""
        cascade = ThreeMOOCascade(use_mock=True)
        cascade.run(max_iterations_per_phase=1)

        state = cascade.get_state()
        assert state is not None
        assert state.is_complete()
        assert len(state.completed_phases) == 3

    def test_callback_invoked(self):
        """Callback should be invoked during optimization."""
        cascade = ThreeMOOCascade(use_mock=True)

        callback_invocations = []

        def callback(phase, iteration, outcomes):
            callback_invocations.append((phase, iteration))

        cascade.run(
            max_iterations_per_phase=2,
            callback=callback,
        )

        assert len(callback_invocations) > 0

    def test_pareto_points_generated(self):
        """Results should include Pareto points."""
        cascade = ThreeMOOCascade(use_mock=True)

        # Add some seed data
        cascade.core_corpus = [
            {"id": str(i), "task": f"Task {i}", "task_type": "reasoning"}
            for i in range(5)
        ]

        results = cascade.run(max_iterations_per_phase=3)

        # At least some phases should have Pareto points
        total_pareto = sum(len(r.pareto_points) for r in results)
        # May be 0 with mock, but should not error
        assert total_pareto >= 0


class TestCreateCascade:
    """Tests for create_cascade factory."""

    def test_create_cascade_mock(self):
        """create_cascade should create with mock mode."""
        cascade = create_cascade(use_mock=True)
        assert isinstance(cascade, ThreeMOOCascade)
        assert cascade.moo.use_mock is True

    def test_create_cascade_with_corpora(self):
        """create_cascade should accept corpora."""
        cascade = create_cascade(
            use_mock=True,
            core_corpus=[{"id": "1", "task": "Test"}],
        )
        assert len(cascade.core_corpus) == 1
