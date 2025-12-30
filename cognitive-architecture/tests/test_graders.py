"""
Tests for eval/graders/deterministic.py and eval/graders/llm_judge.py

Tests:
- FormatGrader, TokenGrader, LatencyGrader, RegexGrader
- VERIXGrader, VERILINGUAGrader
- CompositeGrader
- RubricGrader and council evaluation
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.graders.deterministic import (
    Grader,
    FormatGrader,
    TokenGrader,
    LatencyGrader,
    RegexGrader,
    VERIXGrader,
    VERILINGUAGrader,
    CompositeGrader,
    create_cognitive_grader,
    create_meta_prompt_grader,
)
from eval.graders.llm_judge import (
    RubricGrader,
    RubricCriterion,
    JudgingResult,
    JudgeModel,
    create_rubric,
    create_council_grader,
)


class TestFormatGrader:
    """Tests for FormatGrader."""

    def test_empty_requirements_passes(self):
        """No requirements should return 1.0."""
        grader = FormatGrader()
        score = grader.grade("Any response", None, {})
        assert score == 1.0

    def test_required_sections_found(self):
        """Should detect required sections."""
        grader = FormatGrader(required_sections=["## Summary", "## Details"])
        response = "## Summary\nContent\n\n## Details\nMore content"
        score = grader.grade(response, None, {})
        assert score == 1.0

    def test_required_sections_missing(self):
        """Should penalize missing sections."""
        grader = FormatGrader(required_sections=["## Summary", "## Details"])
        response = "## Summary\nContent only"
        score = grader.grade(response, None, {})
        assert score == 0.5

    def test_required_markers_found(self):
        """Should detect required markers."""
        grader = FormatGrader(required_markers=["[assert", "[ground:"])
        response = "[assert|neutral] Claim [ground: evidence]"
        score = grader.grade(response, None, {})
        assert score == 1.0

    def test_case_sensitivity(self):
        """Should respect case sensitivity setting."""
        grader_sensitive = FormatGrader(
            required_sections=["## Summary"],
            case_sensitive=True,
        )
        grader_insensitive = FormatGrader(
            required_sections=["## Summary"],
            case_sensitive=False,
        )

        response = "## summary\nContent"  # lowercase

        score_sensitive = grader_sensitive.grade(response, None, {})
        score_insensitive = grader_insensitive.grade(response, None, {})

        assert score_sensitive < score_insensitive

    def test_grade_with_details(self):
        """grade_with_details should return breakdown."""
        grader = FormatGrader(
            required_sections=["## A", "## B"],
            required_markers=["[x]"],
        )
        response = "## A\n[x]"
        score, details = grader.grade_with_details(response, None, {})

        assert "missing_sections" in details
        assert "missing_markers" in details


class TestTokenGrader:
    """Tests for TokenGrader."""

    def test_at_baseline(self):
        """At baseline should return 1.0."""
        grader = TokenGrader(baseline_tokens=500)
        score = grader.grade("", None, {"token_count": 500})
        assert score == 1.0

    def test_below_baseline(self):
        """Below baseline should return 1.0."""
        grader = TokenGrader(baseline_tokens=500)
        score = grader.grade("", None, {"token_count": 200})
        assert score == 1.0

    def test_above_baseline_penalized(self):
        """Above baseline should be penalized."""
        grader = TokenGrader(baseline_tokens=500)
        score = grader.grade("", None, {"token_count": 1000})
        assert score < 1.0

    def test_too_short_penalized(self):
        """Below minimum should be penalized."""
        grader = TokenGrader(baseline_tokens=500, min_tokens=50)
        score = grader.grade("Short", None, {"token_count": 10})
        assert score < 1.0

    def test_estimates_tokens_when_missing(self):
        """Should estimate tokens when not in metadata."""
        grader = TokenGrader(baseline_tokens=500)
        response = "This is a test response with some words."
        score = grader.grade(response, None, {})
        assert 0.0 <= score <= 1.0


class TestLatencyGrader:
    """Tests for LatencyGrader."""

    def test_at_target(self):
        """At target should return 1.0."""
        grader = LatencyGrader(target_ms=1000, max_ms=5000)
        score = grader.grade("", None, {"latency_ms": 1000})
        assert score == 1.0

    def test_below_target(self):
        """Below target should return 1.0."""
        grader = LatencyGrader(target_ms=1000, max_ms=5000)
        score = grader.grade("", None, {"latency_ms": 500})
        assert score == 1.0

    def test_at_max(self):
        """At max should return 0.0."""
        grader = LatencyGrader(target_ms=1000, max_ms=5000)
        score = grader.grade("", None, {"latency_ms": 5000})
        assert score == 0.0

    def test_between_target_and_max(self):
        """Between target and max should interpolate."""
        grader = LatencyGrader(target_ms=1000, max_ms=5000)
        score = grader.grade("", None, {"latency_ms": 3000})
        assert 0.0 < score < 1.0

    def test_no_latency_assumes_good(self):
        """No latency data should assume good."""
        grader = LatencyGrader()
        score = grader.grade("", None, {})
        assert score == 1.0


class TestRegexGrader:
    """Tests for RegexGrader."""

    def test_all_patterns_match(self):
        """All patterns matching should return 1.0."""
        grader = RegexGrader([r"\d+", r"[A-Z]"], all_required=True)
        score = grader.grade("Test 123", None, {})
        assert score == 1.0

    def test_partial_match(self):
        """Partial match should return fraction."""
        grader = RegexGrader([r"\d+", r"missing_pattern"], all_required=True)
        score = grader.grade("Test 123", None, {})
        assert score == 0.5

    def test_any_match_mode(self):
        """all_required=False should score by count."""
        grader = RegexGrader([r"\d+", r"test"], all_required=False)
        score = grader.grade("test 123", None, {})
        assert score == 1.0

    def test_case_insensitive(self):
        """Should be case insensitive by default."""
        grader = RegexGrader([r"test"])
        score = grader.grade("TEST", None, {})
        assert score == 1.0


class TestVERIXGrader:
    """Tests for VERIXGrader."""

    def test_l1_markers_detected(self):
        """Should detect L1 VERIX markers."""
        grader = VERIXGrader(compression_level=1)
        response = "[assert|neutral] The sky is blue [ground: observation] [conf:0.9]"
        score = grader.grade(response, None, {})
        assert score > 0.5

    def test_no_markers_low_score(self):
        """No markers should return low score."""
        grader = VERIXGrader(compression_level=1)
        response = "This is a plain response without any markers."
        score = grader.grade(response, None, {})
        assert score < 0.5


class TestVERILINGUAGrader:
    """Tests for VERILINGUAGrader."""

    def test_evidential_markers_detected(self):
        """Should detect evidential frame markers."""
        grader = VERILINGUAGrader(active_frames=["evidential"])
        response = "[witnessed] I saw this happen. [inferred] Therefore..."
        score = grader.grade(response, None, {})
        assert score > 0.3

    def test_multiple_frames(self):
        """Should check multiple frames."""
        grader = VERILINGUAGrader(active_frames=["evidential", "aspectual"])
        response = "[witnessed] Event [complete] Task done"
        score = grader.grade(response, None, {})
        # Score is average of frame scores (0.25 each with 1/4 markers per frame)
        assert score >= 0.2  # Adjusted threshold


class TestCompositeGrader:
    """Tests for CompositeGrader."""

    def test_combines_graders(self):
        """Should combine grader scores."""
        graders = [
            (TokenGrader(baseline_tokens=500), 0.5),
            (LatencyGrader(target_ms=1000), 0.5),
        ]
        composite = CompositeGrader(graders)
        score = composite.grade("", None, {"token_count": 500, "latency_ms": 1000})
        assert score == 1.0

    def test_weighted_combination(self):
        """Should weight scores correctly."""
        graders = [
            (TokenGrader(baseline_tokens=100), 0.75),  # Will score 1.0
            (TokenGrader(baseline_tokens=1), 0.25),   # Will score < 1.0
        ]
        composite = CompositeGrader(graders, normalize_weights=True)
        score = composite.grade("test", None, {"token_count": 100})
        # Should be closer to 1.0 due to higher weight on first grader
        assert score > 0.5

    def test_grade_with_details(self):
        """grade_with_details should include components."""
        graders = [
            (FormatGrader(required_sections=["## A"]), 1.0),
        ]
        composite = CompositeGrader(graders)
        score, details = composite.grade_with_details("## A", None, {})

        assert "components" in details
        assert "format" in details["components"]


class TestRubricCriterion:
    """Tests for RubricCriterion."""

    def test_create_with_defaults(self):
        """Should create with default levels."""
        criterion = RubricCriterion(
            name="Test",
            description="A test criterion",
        )
        assert len(criterion.levels) == 5  # 0-4

    def test_to_prompt_text(self):
        """to_prompt_text should format for LLM."""
        criterion = RubricCriterion(
            name="Clarity",
            description="How clear is the response",
            weight=1.5,
        )
        text = criterion.to_prompt_text()
        assert "Clarity" in text
        assert "1.5" in text


class TestRubricGrader:
    """Tests for RubricGrader."""

    def test_grade_returns_result(self):
        """grade should return JudgingResult."""
        grader = RubricGrader()
        task = {"id": "test", "task": "Test task"}
        result = grader.grade("Test response", task)

        assert isinstance(result, JudgingResult)
        assert 0.0 <= result.score <= 1.0
        assert result.judge_model == "claude"

    def test_council_grading(self):
        """Council grading should aggregate results."""
        grader = RubricGrader(use_council=True)
        task = {"id": "test", "task": "Test task"}
        result = grader.grade("Test response", task)

        assert result.judge_model == "council"


class TestCreateRubric:
    """Tests for create_rubric() function."""

    def test_creates_criteria_list(self):
        """Should create list of criteria from config."""
        configs = [
            {"name": "A", "description": "First"},
            {"name": "B", "description": "Second", "weight": 2.0},
        ]
        criteria = create_rubric(configs)

        assert len(criteria) == 2
        assert criteria[0].name == "A"
        assert criteria[1].weight == 2.0


class TestFactoryFunctions:
    """Tests for grader factory functions."""

    def test_create_cognitive_grader(self):
        """Should create cognitive grader."""
        grader = create_cognitive_grader()
        assert isinstance(grader, CompositeGrader)

    def test_create_meta_prompt_grader(self):
        """Should create meta-prompt grader."""
        grader = create_meta_prompt_grader()
        assert isinstance(grader, CompositeGrader)

    def test_create_council_grader(self):
        """Should create council grader."""
        grader = create_council_grader("default")
        assert isinstance(grader, RubricGrader)
        assert grader.use_council is True
