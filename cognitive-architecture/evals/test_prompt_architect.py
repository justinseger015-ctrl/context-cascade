"""
DeepEval Tests for Prompt Architect Skill

Task corpus: PA-001 to PA-050
- Easy (PA-001 to PA-010): Intent extraction
- Medium (PA-011 to PA-030): Prompt optimization
- Hard (PA-031 to PA-050): Anti-pattern detection + epistemic calibration

Run with: pytest evals/test_prompt_architect.py -v
"""

import json
import pytest
from pathlib import Path

from evals.conftest import (
    load_corpus,
    check_confidence_ceiling,
    check_verix_format,
    check_l2_purity,
    CONFIDENCE_CEILINGS,
)


class TestPromptArchitectCorpus:
    """Test that the corpus is valid and complete."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpus = load_corpus("prompt-architect")

    def test_corpus_has_50_tasks(self):
        """Verify corpus contains exactly 50 tasks."""
        assert len(self.corpus["tasks"]) == 50

    def test_corpus_has_correct_skill_name(self):
        """Verify corpus is for prompt-architect."""
        assert self.corpus["skill"] == "prompt-architect"

    def test_corpus_has_version(self):
        """Verify corpus has version specified."""
        assert "version" in self.corpus
        assert self.corpus["version"] == "3.1.1"

    def test_all_tasks_have_required_fields(self):
        """Verify all tasks have required fields."""
        required_fields = ["id", "difficulty", "category", "input", "success_criteria"]
        for task in self.corpus["tasks"]:
            for field in required_fields:
                assert field in task, f"Task {task.get('id', 'unknown')} missing {field}"

    def test_task_ids_are_sequential(self):
        """Verify task IDs follow PA-XXX pattern."""
        for i, task in enumerate(self.corpus["tasks"], 1):
            expected_id = f"PA-{i:03d}"
            assert task["id"] == expected_id, f"Expected {expected_id}, got {task['id']}"

    def test_difficulty_distribution(self):
        """Verify correct distribution of difficulties."""
        difficulties = [t["difficulty"] for t in self.corpus["tasks"]]
        assert difficulties.count("easy") == 10
        assert difficulties.count("medium") == 20
        assert difficulties.count("hard") == 20


class TestIntentExtraction:
    """Tests for easy tasks (PA-001 to PA-010): Intent extraction."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpus = load_corpus("prompt-architect")
        self.easy_tasks = [t for t in self.corpus["tasks"] if t["difficulty"] == "easy"]

    def test_easy_tasks_have_expected_intent(self):
        """Verify easy tasks specify expected intent."""
        for task in self.easy_tasks:
            assert "expected_intent" in task, f"Task {task['id']} missing expected_intent"

    def test_easy_tasks_have_expected_constraints(self):
        """Verify easy tasks specify expected constraints."""
        for task in self.easy_tasks:
            assert "expected_constraints" in task, f"Task {task['id']} missing expected_constraints"

    @pytest.mark.parametrize("task_id", [f"PA-{i:03d}" for i in range(1, 11)])
    def test_intent_categories_are_valid(self, task_id):
        """Verify intent categories are from allowed set."""
        valid_intents = {
            "code_generation",
            "explanation",
            "debugging",
            "feature_addition",
            "code_review",
            "analysis",
            "refactoring",
            "test_creation",
            "optimization",
            "documentation",
        }
        task = next(t for t in self.easy_tasks if t["id"] == task_id)
        assert task["expected_intent"] in valid_intents


class TestPromptOptimization:
    """Tests for medium tasks (PA-011 to PA-030): Prompt optimization."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpus = load_corpus("prompt-architect")
        self.medium_tasks = [t for t in self.corpus["tasks"] if t["difficulty"] == "medium"]

    def test_medium_tasks_have_original_context(self):
        """Verify medium tasks specify original context."""
        for task in self.medium_tasks:
            assert "original_context" in task, f"Task {task['id']} missing original_context"

    def test_medium_tasks_have_expected_optimization(self):
        """Verify medium tasks specify expected optimization."""
        for task in self.medium_tasks:
            assert "expected_optimization" in task, f"Task {task['id']} missing expected_optimization"

    def test_vague_inputs_are_transformed(self):
        """Verify vague inputs have specific optimization targets."""
        vague_patterns = ["make it", "fix the", "help me", "write", "add"]
        for task in self.medium_tasks:
            input_text = task["input"].lower()
            if any(p in input_text for p in vague_patterns):
                # Should have detailed expected_optimization
                assert len(task["expected_optimization"]) > 50


class TestAntiPatternDetection:
    """Tests for hard tasks (PA-031 to PA-040): Anti-pattern detection."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpus = load_corpus("prompt-architect")
        self.hard_tasks = [
            t for t in self.corpus["tasks"]
            if t["difficulty"] == "hard" and t["category"] == "anti_pattern_detection"
        ]

    def test_anti_pattern_tasks_have_patterns(self):
        """Verify anti-pattern tasks specify anti_patterns list."""
        for task in self.hard_tasks:
            assert "anti_patterns" in task, f"Task {task['id']} missing anti_patterns"

    def test_anti_pattern_tasks_have_expected_response(self):
        """Verify anti-pattern tasks specify expected response."""
        for task in self.hard_tasks:
            assert "expected_response" in task, f"Task {task['id']} missing expected_response"


class TestEpistemicCalibration:
    """Tests for hard tasks (PA-046 to PA-050): Epistemic calibration."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpus = load_corpus("prompt-architect")
        self.epistemic_tasks = [
            t for t in self.corpus["tasks"]
            if t["difficulty"] == "hard" and t["category"] == "epistemic_calibration"
        ]

    def test_epistemic_tasks_have_test_type(self):
        """Verify epistemic tasks specify test_type."""
        for task in self.epistemic_tasks:
            assert "test_type" in task, f"Task {task['id']} missing test_type"

    def test_epistemic_tasks_have_expected_behavior(self):
        """Verify epistemic tasks specify expected behavior."""
        for task in self.epistemic_tasks:
            assert "expected_behavior" in task, f"Task {task['id']} missing expected_behavior"


class TestConfidenceCeilings:
    """Test confidence ceiling enforcement."""

    def test_definition_ceiling(self):
        """Definition claims cannot exceed 0.95."""
        assert check_confidence_ceiling("definition", 0.95) is True
        assert check_confidence_ceiling("definition", 0.96) is False

    def test_report_ceiling(self):
        """Report claims cannot exceed 0.70."""
        assert check_confidence_ceiling("report", 0.70) is True
        assert check_confidence_ceiling("report", 0.71) is False

    def test_inference_ceiling(self):
        """Inference claims cannot exceed 0.70."""
        assert check_confidence_ceiling("inference", 0.70) is True
        assert check_confidence_ceiling("inference", 0.71) is False


class TestVERIXFormat:
    """Test VERIX notation format checking."""

    def test_valid_verix_statement(self):
        """Valid VERIX statement passes check."""
        valid = "[assert|neutral] Test claim [ground:test] [conf:0.85] [state:confirmed]"
        assert check_verix_format(valid) is True

    def test_missing_ground_fails(self):
        """Statement missing ground marker fails."""
        invalid = "[assert|neutral] Test claim [conf:0.85] [state:confirmed]"
        assert check_verix_format(invalid) is False

    def test_missing_conf_fails(self):
        """Statement missing conf marker fails."""
        invalid = "[assert|neutral] Test claim [ground:test] [state:confirmed]"
        assert check_verix_format(invalid) is False


class TestL2Purity:
    """Test L2 output purity checking."""

    def test_pure_english_passes(self):
        """Pure English output passes L2 check."""
        pure = "This is a simple English response without any markers."
        assert check_l2_purity(pure) is True

    def test_verix_markers_fail(self):
        """Output with VERIX markers fails L2 check."""
        impure = "This response has [ground:test] markers."
        assert check_l2_purity(impure) is False

    def test_vcl_slot_markers_fail(self):
        """Output with VCL slot markers fails L2 check."""
        impure = "This response has [[EVD:-DI]] markers."
        assert check_l2_purity(impure) is False
