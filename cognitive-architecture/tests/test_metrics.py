"""
Tests for eval/metrics.py

Tests:
- EvaluationResult dataclass
- MetricCalculator all 4 metrics
- Anti-gaming utilities (length_normalize, format_compliance_penalty)
- aggregate_metrics function
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.metrics import (
    EvaluationResult,
    MetricCalculator,
    MetricType,
    length_normalize,
    format_compliance_penalty,
    aggregate_metrics,
)
from core.config import FullConfig


class TestEvaluationResult:
    """Tests for EvaluationResult dataclass."""

    def test_create_valid_result(self):
        """Should create result with valid metrics."""
        result = EvaluationResult(
            task_id="test-001",
            task_accuracy=0.8,
            token_efficiency=0.9,
            edge_robustness=0.7,
            epistemic_consistency=0.85,
        )
        assert result.task_id == "test-001"
        assert result.task_accuracy == 0.8

    def test_invalid_metric_raises(self):
        """Should raise for out-of-range metrics."""
        with pytest.raises(ValueError):
            EvaluationResult(
                task_id="test",
                task_accuracy=1.5,  # Invalid: > 1.0
                token_efficiency=0.9,
                edge_robustness=0.7,
                epistemic_consistency=0.85,
            )

    def test_composite_score_calculation(self):
        """composite_score should be weighted average."""
        result = EvaluationResult(
            task_id="test",
            task_accuracy=1.0,
            token_efficiency=1.0,
            edge_robustness=1.0,
            epistemic_consistency=1.0,
        )
        assert result.composite_score == 1.0

        result2 = EvaluationResult(
            task_id="test",
            task_accuracy=0.0,
            token_efficiency=0.0,
            edge_robustness=0.0,
            epistemic_consistency=0.0,
        )
        assert result2.composite_score == 0.0

    def test_to_dict(self):
        """to_dict() should include all fields."""
        result = EvaluationResult(
            task_id="test",
            task_accuracy=0.8,
            token_efficiency=0.9,
            edge_robustness=0.7,
            epistemic_consistency=0.85,
        )
        d = result.to_dict()
        assert d["task_id"] == "test"
        assert d["task_accuracy"] == 0.8
        assert "composite_score" in d

    def test_from_dict(self):
        """from_dict() should reconstruct result."""
        original = EvaluationResult(
            task_id="test",
            task_accuracy=0.8,
            token_efficiency=0.9,
            edge_robustness=0.7,
            epistemic_consistency=0.85,
        )
        d = original.to_dict()
        reconstructed = EvaluationResult.from_dict(d)
        assert reconstructed.task_id == original.task_id
        assert reconstructed.task_accuracy == original.task_accuracy


class TestMetricCalculator:
    """Tests for MetricCalculator."""

    def test_init_with_config(self):
        """Should initialize with config."""
        config = FullConfig()
        calc = MetricCalculator(config)
        assert calc.config == config

    def test_init_defaults(self):
        """Should use defaults when no config provided."""
        calc = MetricCalculator()
        assert calc.token_baseline == 500
        assert calc.length_target == 1000

    def test_calculate_returns_result(self):
        """calculate() should return EvaluationResult."""
        calc = MetricCalculator()
        task = {"id": "test-001", "task_type": "reasoning"}
        response = "This is a test response with some content."
        expected = "test"

        result = calc.calculate(task, response, expected, token_count=100)

        assert isinstance(result, EvaluationResult)
        assert result.task_id == "test-001"
        assert 0.0 <= result.task_accuracy <= 1.0

    def test_task_accuracy_string_match(self):
        """task_accuracy should detect string matches."""
        calc = MetricCalculator()

        # Exact match in response
        accuracy = calc.task_accuracy(
            "The answer is 42.",
            "42",
            "reasoning",
        )
        assert accuracy == 1.0

    def test_task_accuracy_partial_match(self):
        """task_accuracy should handle partial matches."""
        calc = MetricCalculator()

        # Partial match
        accuracy = calc.task_accuracy(
            "We found one item.",
            "one two three",
            "reasoning",
        )
        assert 0.0 < accuracy < 1.0

    def test_task_accuracy_list_expected(self):
        """task_accuracy should handle list of expected items."""
        calc = MetricCalculator()

        response = "Found apple and banana."
        expected = ["apple", "banana", "orange"]

        accuracy = calc.task_accuracy(response, expected, "reasoning")
        assert accuracy == 2/3  # 2 out of 3 found

    def test_token_efficiency_at_baseline(self):
        """token_efficiency should return 1.0 at baseline."""
        calc = MetricCalculator(token_baseline=500)
        efficiency = calc.token_efficiency(500, 500)
        assert efficiency == 1.0

    def test_token_efficiency_below_baseline(self):
        """token_efficiency should return 1.0 below baseline."""
        calc = MetricCalculator(token_baseline=500)
        efficiency = calc.token_efficiency(200, 500)
        assert efficiency == 1.0

    def test_token_efficiency_above_baseline(self):
        """token_efficiency should decrease above baseline."""
        calc = MetricCalculator(token_baseline=500)
        efficiency = calc.token_efficiency(1000, 500)
        assert 0.0 < efficiency < 1.0

    def test_token_efficiency_zero_returns_zero(self):
        """token_efficiency should return 0.0 for zero tokens."""
        calc = MetricCalculator()
        efficiency = calc.token_efficiency(0, 500)
        assert efficiency == 0.0

    def test_edge_robustness_no_edge_type(self):
        """edge_robustness should return 1.0 for no edge type."""
        calc = MetricCalculator()
        robustness = calc.edge_robustness("Any response", None)
        assert robustness == 1.0

    def test_edge_robustness_with_markers(self):
        """edge_robustness should be higher with uncertainty markers."""
        calc = MetricCalculator()

        # Response with hedging
        robustness1 = calc.edge_robustness(
            "This might be correct, but I'm uncertain about the context.",
            "ambiguous",
        )

        # Response without hedging
        robustness2 = calc.edge_robustness(
            "The answer is definitely X.",
            "ambiguous",
        )

        assert robustness1 > robustness2

    def test_epistemic_consistency_empty_claims(self):
        """epistemic_consistency should return 0.5 for no claims."""
        calc = MetricCalculator()
        consistency = calc.epistemic_consistency([])
        assert consistency == 0.5


class TestLengthNormalize:
    """Tests for length_normalize()."""

    def test_empty_response_penalized(self):
        """Empty response should get heavy penalty."""
        penalty = length_normalize(1.0, 0, 1000)
        assert penalty == 0.1

    def test_target_length_no_penalty(self):
        """Response at target length should get no penalty."""
        penalty = length_normalize(1.0, 1000, 1000)
        assert penalty >= 0.8

    def test_extreme_length_penalized(self):
        """Extremely long/short response should be penalized."""
        # Very long
        penalty_long = length_normalize(1.0, 10000, 1000)
        assert penalty_long < 0.5

        # Very short
        penalty_short = length_normalize(1.0, 50, 1000)
        assert penalty_short < 0.5


class TestFormatCompliancePenalty:
    """Tests for format_compliance_penalty()."""

    def test_normal_response_no_penalty(self):
        """Normal response should have minimal penalty."""
        response = "This is a normal response with varied content."
        penalty = format_compliance_penalty(response, "default")
        assert penalty >= 0.9

    def test_repetitive_response_penalized(self):
        """Repetitive response should be penalized."""
        response = "word word word word word word word word word word word"
        penalty = format_compliance_penalty(response, "default")
        assert penalty < 1.0

    def test_excessive_bullets_penalized(self):
        """Excessive bullet points should be penalized."""
        response = "\n".join([f"- Item {i}" for i in range(25)])
        penalty = format_compliance_penalty(response, "default")
        assert penalty < 1.0


class TestAggregateMetrics:
    """Tests for aggregate_metrics()."""

    def test_empty_list_returns_zeros(self):
        """aggregate_metrics([]) should return zeros."""
        aggregated = aggregate_metrics([])
        assert aggregated["task_accuracy"] == 0.0
        assert aggregated["count"] == 0

    def test_single_result(self):
        """aggregate_metrics with single result should return that result."""
        result = EvaluationResult(
            task_id="test",
            task_accuracy=0.8,
            token_efficiency=0.9,
            edge_robustness=0.7,
            epistemic_consistency=0.85,
        )
        aggregated = aggregate_metrics([result])
        assert aggregated["task_accuracy"] == 0.8
        assert aggregated["count"] == 1

    def test_multiple_results_averaged(self):
        """aggregate_metrics should average multiple results."""
        results = [
            EvaluationResult(
                task_id="test1",
                task_accuracy=1.0,
                token_efficiency=1.0,
                edge_robustness=1.0,
                epistemic_consistency=1.0,
            ),
            EvaluationResult(
                task_id="test2",
                task_accuracy=0.0,
                token_efficiency=0.0,
                edge_robustness=0.0,
                epistemic_consistency=0.0,
            ),
        ]
        aggregated = aggregate_metrics(results)
        assert aggregated["task_accuracy"] == 0.5
        assert aggregated["count"] == 2
