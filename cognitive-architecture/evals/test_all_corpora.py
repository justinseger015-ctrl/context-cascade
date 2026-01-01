"""
DeepEval Tests for All Three Foundry Skills

Validates corpus structure and completeness for:
- prompt-architect (50 tasks)
- agent-creator (50 tasks)
- skill-forge (50 tasks)

Total: 150 tasks for VVV recursive improvement loop

Run with: pytest evals/test_all_corpora.py -v
"""

import pytest
from evals.conftest import load_corpus


class TestAllCorpora:
    """Test all three corpora are valid and complete."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpora = {
            "prompt-architect": load_corpus("prompt-architect"),
            "agent-creator": load_corpus("agent-creator"),
            "skill-forge": load_corpus("skill-forge"),
        }

    def test_total_task_count(self):
        """Verify total of 150 tasks across all corpora."""
        total = sum(len(c["tasks"]) for c in self.corpora.values())
        assert total == 150

    @pytest.mark.parametrize("skill_name", ["prompt-architect", "agent-creator", "skill-forge"])
    def test_corpus_has_50_tasks(self, skill_name):
        """Each corpus should have exactly 50 tasks."""
        assert len(self.corpora[skill_name]["tasks"]) == 50

    @pytest.mark.parametrize("skill_name", ["prompt-architect", "agent-creator", "skill-forge"])
    def test_corpus_has_eval_dimensions(self, skill_name):
        """Each corpus should specify eval dimensions."""
        assert "eval_dimensions" in self.corpora[skill_name]
        assert len(self.corpora[skill_name]["eval_dimensions"]) >= 3

    @pytest.mark.parametrize("skill_name", ["prompt-architect", "agent-creator", "skill-forge"])
    def test_corpus_version_present(self, skill_name):
        """Each corpus should have version."""
        assert "version" in self.corpora[skill_name]

    @pytest.mark.parametrize("skill_name,prefix", [
        ("prompt-architect", "PA"),
        ("agent-creator", "AC"),
        ("skill-forge", "SF"),
    ])
    def test_task_id_prefixes(self, skill_name, prefix):
        """Task IDs should have correct prefix."""
        for task in self.corpora[skill_name]["tasks"]:
            assert task["id"].startswith(prefix)


class TestDifficultyDistribution:
    """Test difficulty distribution across corpora."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpora = {
            "prompt-architect": load_corpus("prompt-architect"),
            "agent-creator": load_corpus("agent-creator"),
            "skill-forge": load_corpus("skill-forge"),
        }

    @pytest.mark.parametrize("skill_name", ["prompt-architect", "agent-creator", "skill-forge"])
    def test_has_easy_tasks(self, skill_name):
        """Each corpus should have easy tasks."""
        easy = [t for t in self.corpora[skill_name]["tasks"] if t["difficulty"] == "easy"]
        assert len(easy) >= 10

    @pytest.mark.parametrize("skill_name", ["prompt-architect", "agent-creator", "skill-forge"])
    def test_has_medium_tasks(self, skill_name):
        """Each corpus should have medium tasks."""
        medium = [t for t in self.corpora[skill_name]["tasks"] if t["difficulty"] == "medium"]
        assert len(medium) >= 15

    @pytest.mark.parametrize("skill_name", ["prompt-architect", "agent-creator", "skill-forge"])
    def test_has_hard_tasks(self, skill_name):
        """Each corpus should have hard tasks."""
        hard = [t for t in self.corpora[skill_name]["tasks"] if t["difficulty"] == "hard"]
        assert len(hard) >= 15


class TestCategoryDistribution:
    """Test category coverage across corpora."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpora = {
            "prompt-architect": load_corpus("prompt-architect"),
            "agent-creator": load_corpus("agent-creator"),
            "skill-forge": load_corpus("skill-forge"),
        }

    def test_prompt_architect_categories(self):
        """Prompt architect should have intent, optimization, anti-pattern categories."""
        categories = {t["category"] for t in self.corpora["prompt-architect"]["tasks"]}
        assert "intent_extraction" in categories
        assert "prompt_optimization" in categories
        assert "anti_pattern_detection" in categories

    def test_agent_creator_categories(self):
        """Agent creator should have definition, validation, compliance categories."""
        categories = {t["category"] for t in self.corpora["agent-creator"]["tasks"]}
        assert "agent_definition" in categories
        assert "registry_validation" in categories
        assert "vcl_7slot_compliance" in categories

    def test_skill_forge_categories(self):
        """Skill forge should have structure, adversarial, cov categories."""
        categories = {t["category"] for t in self.corpora["skill-forge"]["tasks"]}
        assert "skill_structure" in categories
        assert "adversarial_testing" in categories
        assert "cov_validation" in categories


class TestSuccessCriteria:
    """Test all tasks have success criteria."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.corpora = {
            "prompt-architect": load_corpus("prompt-architect"),
            "agent-creator": load_corpus("agent-creator"),
            "skill-forge": load_corpus("skill-forge"),
        }

    @pytest.mark.parametrize("skill_name", ["prompt-architect", "agent-creator", "skill-forge"])
    def test_all_tasks_have_success_criteria(self, skill_name):
        """Every task must have success criteria defined."""
        for task in self.corpora[skill_name]["tasks"]:
            assert "success_criteria" in task, f"Task {task['id']} missing success_criteria"
            assert len(task["success_criteria"]) > 10, f"Task {task['id']} has too short success_criteria"
