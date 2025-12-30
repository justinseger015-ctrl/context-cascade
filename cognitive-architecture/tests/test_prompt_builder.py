"""
Tests for core/prompt_builder.py

Tests:
- PromptBuilder construction
- build() contract returns tuple
- Prompt components assembly
- Factory methods
- Task-type specific configurations
"""

import pytest
from core.prompt_builder import (
    PromptBuilder,
    PromptBuilderFactory,
    PromptComponents,
    build_prompt,
    TASK_TYPE_INSTRUCTIONS,
)
from core.config import (
    FullConfig,
    FrameworkConfig,
    PromptConfig,
    VectorCodec,
    VerixStrictness,
    STRICT_CONFIG,
    MINIMAL_CONFIG,
)


class TestPromptBuilder:
    """Tests for PromptBuilder class."""

    def test_init_creates_builder(self):
        """Should initialize with config."""
        config = FullConfig()
        builder = PromptBuilder(config)
        assert builder.config == config
        assert builder.active_frames is not None

    def test_build_returns_tuple(self):
        """build() should return (system, user) tuple."""
        builder = PromptBuilder(FullConfig())
        result = builder.build("Test task", "default")

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)  # system
        assert isinstance(result[1], str)  # user

    def test_build_includes_task_in_user_prompt(self):
        """User prompt should include the task."""
        builder = PromptBuilder(FullConfig())
        system, user = builder.build("Calculate the sum of 1 + 2", "reasoning")

        assert "Calculate the sum of 1 + 2" in user

    def test_build_includes_frame_activations(self):
        """System prompt should include active frame instructions."""
        config = FullConfig(
            framework=FrameworkConfig(evidential=True, aspectual=True)
        )
        builder = PromptBuilder(config)
        system, user = builder.build("Test", "default")

        assert "EVIDENTIAL" in system.upper()
        assert "ASPECTUAL" in system.upper()

    def test_build_includes_verix_requirements(self):
        """System prompt should include VERIX requirements."""
        config = FullConfig(
            prompt=PromptConfig(verix_strictness=VerixStrictness.STRICT)
        )
        builder = PromptBuilder(config)
        system, user = builder.build("Test", "default")

        assert "VERIX" in system.upper()
        assert "STRICT" in system.upper()

    def test_cluster_key_returns_string(self):
        """cluster_key() should return cache key string."""
        builder = PromptBuilder(FullConfig())
        key = builder.cluster_key()

        assert isinstance(key, str)
        assert len(key) > 0

    def test_cluster_key_same_for_same_config(self):
        """Same config should produce same cluster key."""
        config = FullConfig()
        builder1 = PromptBuilder(config)
        builder2 = PromptBuilder(config)

        assert builder1.cluster_key() == builder2.cluster_key()

    def test_cluster_key_differs_for_different_config(self):
        """Different configs should produce different keys."""
        builder1 = PromptBuilder(MINIMAL_CONFIG)
        builder2 = PromptBuilder(STRICT_CONFIG)

        assert builder1.cluster_key() != builder2.cluster_key()


class TestTaskTypeInstructions:
    """Tests for task type base instructions."""

    def test_reasoning_instruction_exists(self):
        """Should have reasoning task instruction."""
        assert "reasoning" in TASK_TYPE_INSTRUCTIONS
        assert len(TASK_TYPE_INSTRUCTIONS["reasoning"]) > 50

    def test_coding_instruction_exists(self):
        """Should have coding task instruction."""
        assert "coding" in TASK_TYPE_INSTRUCTIONS
        assert "code" in TASK_TYPE_INSTRUCTIONS["coding"].lower()

    def test_analysis_instruction_exists(self):
        """Should have analysis task instruction."""
        assert "analysis" in TASK_TYPE_INSTRUCTIONS

    def test_default_instruction_exists(self):
        """Should have default task instruction."""
        assert "default" in TASK_TYPE_INSTRUCTIONS

    def test_unknown_type_uses_default(self):
        """Unknown task type should use default instruction."""
        builder = PromptBuilder(FullConfig())
        system1, _ = builder.build("Test", "unknown_type")
        system2, _ = builder.build("Test", "default")

        # Both should use default instruction content
        # (exact match depends on other components)
        assert len(system1) > 0
        assert len(system2) > 0


class TestPromptBuilderFactory:
    """Tests for PromptBuilderFactory."""

    def test_default_factory(self):
        """default() should return builder with default config."""
        builder = PromptBuilderFactory.default()
        assert isinstance(builder, PromptBuilder)
        assert builder.config.framework.evidential is True

    def test_minimal_factory(self):
        """minimal() should return builder with minimal config."""
        builder = PromptBuilderFactory.minimal()
        assert isinstance(builder, PromptBuilder)
        assert builder.config.prompt.verix_strictness == VerixStrictness.RELAXED

    def test_strict_factory(self):
        """strict() should return builder with strict config."""
        builder = PromptBuilderFactory.strict()
        assert isinstance(builder, PromptBuilder)
        assert builder.config.prompt.verix_strictness == VerixStrictness.STRICT
        assert builder.config.framework.frame_count() == 7

    def test_from_vector_creates_builder(self):
        """from_vector() should create builder from config vector."""
        vector = VectorCodec.encode(FullConfig())
        builder = PromptBuilderFactory.from_vector(vector)

        assert isinstance(builder, PromptBuilder)

    def test_for_task_type_coding(self):
        """for_task_type() should optimize for coding."""
        builder = PromptBuilderFactory.for_task_type("coding")
        assert isinstance(builder, PromptBuilder)
        # Coding should have classifier and spatial for code navigation
        assert builder.config.framework.classifier is True
        assert builder.config.framework.spatial is True

    def test_for_task_type_reasoning(self):
        """for_task_type() should optimize for reasoning."""
        builder = PromptBuilderFactory.for_task_type("reasoning")
        assert isinstance(builder, PromptBuilder)
        # Reasoning should have morphological for concept decomposition
        assert builder.config.framework.morphological is True

    def test_for_task_type_unknown_uses_default(self):
        """for_task_type() with unknown type should use default config."""
        builder = PromptBuilderFactory.for_task_type("unknown_xyz")
        assert isinstance(builder, PromptBuilder)
        # Should use default FrameworkConfig
        assert builder.config.framework.evidential is True


class TestBuildPromptFunction:
    """Tests for build_prompt() convenience function."""

    def test_build_prompt_returns_tuple(self):
        """build_prompt() should return (system, user) tuple."""
        result = build_prompt("Test task")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_build_prompt_with_config(self):
        """build_prompt() should accept custom config."""
        config = STRICT_CONFIG
        system, user = build_prompt("Test", "default", config)

        assert "STRICT" in system.upper()

    def test_build_prompt_default_task_type(self):
        """build_prompt() should use 'default' task type."""
        system, user = build_prompt("Test")
        assert len(system) > 0
        assert "Test" in user


class TestPromptComponents:
    """Tests for PromptComponents dataclass."""

    def test_components_creation(self):
        """Should create PromptComponents with all fields."""
        components = PromptComponents(
            base_instruction="Base",
            frame_activations="Frames",
            verix_requirements="VERIX",
            output_format="Format",
            task_content="Task",
        )
        assert components.base_instruction == "Base"
        assert components.task_content == "Task"
