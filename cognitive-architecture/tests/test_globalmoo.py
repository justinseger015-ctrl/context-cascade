"""
Tests for optimization/globalmoo_client.py

Tests:
- GlobalMOOClient mock mode
- OptimizationOutcome structure
- Pareto frontier operations
- Impact factors
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.globalmoo_client import (
    GlobalMOOClient,
    OptimizationOutcome,
    ParetoPoint,
    Objective,
    ObjectiveDirection,
    create_client,
    create_cognitive_project,
)
from core.config import FullConfig, VectorCodec


class TestOptimizationOutcome:
    """Tests for OptimizationOutcome dataclass."""

    def test_create_outcome(self):
        """Should create outcome with all fields."""
        outcome = OptimizationOutcome(
            config_vector=[0.5] * 14,
            outcomes={"task_accuracy": 0.8, "token_efficiency": 0.9},
        )
        assert len(outcome.config_vector) == 14
        assert outcome.outcomes["task_accuracy"] == 0.8

    def test_to_dict(self):
        """to_dict should include all fields."""
        outcome = OptimizationOutcome(
            config_vector=[1.0, 0.0],
            outcomes={"metric": 0.5},
            metadata={"test": True},
        )
        d = outcome.to_dict()
        assert d["config_vector"] == [1.0, 0.0]
        assert d["outcomes"]["metric"] == 0.5
        assert d["metadata"]["test"] is True

    def test_from_dict(self):
        """from_dict should reconstruct outcome."""
        original = OptimizationOutcome(
            config_vector=[0.5, 0.5],
            outcomes={"accuracy": 0.9},
        )
        d = original.to_dict()
        reconstructed = OptimizationOutcome.from_dict(d)
        assert reconstructed.config_vector == original.config_vector
        assert reconstructed.outcomes == original.outcomes


class TestParetoPoint:
    """Tests for ParetoPoint dataclass."""

    def test_create_point(self):
        """Should create Pareto point."""
        point = ParetoPoint(
            config_vector=VectorCodec.encode(FullConfig()),
            outcomes={"task_accuracy": 0.9, "token_efficiency": 0.8},
            dominance_rank=0,
        )
        assert point.dominance_rank == 0
        assert len(point.config_vector) == 14

    def test_to_config(self):
        """to_config should convert to FullConfig."""
        config = FullConfig()
        config.framework.morphological = True
        vector = VectorCodec.encode(config)

        point = ParetoPoint(
            config_vector=vector,
            outcomes={},
        )
        reconstructed = point.to_config()
        assert reconstructed.framework.morphological is True


class TestGlobalMOOClient:
    """Tests for GlobalMOOClient in mock mode."""

    def test_mock_is_available(self):
        """Mock client should always be available."""
        client = GlobalMOOClient(use_mock=True)
        assert client.is_available is True

    def test_mock_test_connection(self):
        """Mock connection test should pass."""
        client = GlobalMOOClient(use_mock=True)
        assert client.test_connection() is True

    def test_create_model(self):
        """create_model should return model ID."""
        client = GlobalMOOClient(use_mock=True)
        model_id = client.create_model(
            name="test-model",
            description="Test description",
        )
        assert model_id is not None
        assert len(model_id) > 0

    def test_create_project(self):
        """create_project should return project ID."""
        client = GlobalMOOClient(use_mock=True)
        model_id = client.create_model("test")
        project_id = client.create_project(
            model_id=model_id,
            name="test-project",
        )
        assert project_id is not None
        assert client.project_id == project_id

    def test_load_cases(self):
        """load_cases should accept outcomes."""
        client = GlobalMOOClient(use_mock=True)
        model_id = client.create_model("test")
        project_id = client.create_project(model_id, "test-project")

        cases = [
            OptimizationOutcome(
                config_vector=[0.5] * 14,
                outcomes={"task_accuracy": 0.8},
            ),
        ]
        count = client.load_cases(project_id, cases)
        assert count == 1

    def test_suggest_inverse(self):
        """suggest_inverse should return config vectors."""
        client = GlobalMOOClient(use_mock=True)
        model_id = client.create_model("test")
        project_id = client.create_project(model_id, "test-project")

        # Load some cases first
        cases = [
            OptimizationOutcome(
                config_vector=VectorCodec.encode(FullConfig()),
                outcomes={"task_accuracy": 0.8, "token_efficiency": 0.7},
            ),
        ]
        client.load_cases(project_id, cases)

        # Get suggestions
        suggestions = client.suggest_inverse(
            project_id,
            target_outcomes={"task_accuracy": 0.95},
            num_suggestions=3,
        )
        assert len(suggestions) == 3
        assert all(len(s) == 14 for s in suggestions)

    def test_report_outcome(self):
        """report_outcome should accept outcome."""
        client = GlobalMOOClient(use_mock=True)
        model_id = client.create_model("test")
        project_id = client.create_project(model_id, "test-project")

        outcome = OptimizationOutcome(
            config_vector=[0.5] * 14,
            outcomes={"task_accuracy": 0.9},
        )
        # Should not raise
        client.report_outcome(project_id, outcome)

    def test_get_pareto_frontier(self):
        """get_pareto_frontier should return Pareto points."""
        client = GlobalMOOClient(use_mock=True)
        model_id = client.create_model("test")
        project_id = client.create_project(model_id, "test-project")

        # Load diverse cases
        cases = [
            OptimizationOutcome(
                config_vector=[float(i % 2)] * 14,
                outcomes={"task_accuracy": 0.5 + i * 0.1, "token_efficiency": 0.9 - i * 0.1},
            )
            for i in range(5)
        ]
        client.load_cases(project_id, cases)

        pareto = client.get_pareto_frontier(project_id)
        assert isinstance(pareto, list)
        assert all(isinstance(p, ParetoPoint) for p in pareto)

    def test_get_impact_factors(self):
        """get_impact_factors should return impact dict."""
        client = GlobalMOOClient(use_mock=True)
        model_id = client.create_model("test")
        project_id = client.create_project(model_id, "test-project")

        impact = client.get_impact_factors(project_id)
        assert isinstance(impact, dict)
        assert "task_accuracy" in impact


class TestObjective:
    """Tests for Objective dataclass."""

    def test_create_objective(self):
        """Should create objective."""
        obj = Objective(
            name="accuracy",
            direction=ObjectiveDirection.MAXIMIZE,
            threshold=0.9,
        )
        assert obj.name == "accuracy"
        assert obj.direction == ObjectiveDirection.MAXIMIZE

    def test_to_dict(self):
        """to_dict should serialize objective."""
        obj = Objective(
            name="efficiency",
            direction=ObjectiveDirection.MAXIMIZE,
        )
        d = obj.to_dict()
        assert d["name"] == "efficiency"
        assert d["direction"] == "maximize"


class TestFactoryFunctions:
    """Tests for factory functions."""

    def test_create_client(self):
        """create_client should return client."""
        client = create_client(use_mock=True)
        assert isinstance(client, GlobalMOOClient)
        assert client.use_mock is True

    def test_create_cognitive_project(self):
        """create_cognitive_project should set up full project."""
        client = GlobalMOOClient(use_mock=True)
        project = create_cognitive_project(client, "test-cognitive")

        assert project.project_id is not None
        assert project.model_id is not None
        assert len(project.objectives) == 4  # 4 cognitive objectives
