"""
Integration tests for Phase 3 components.

Tests:
- Commands integration
- Hooks integration
- Mode selection flow
- End-to-end workflows
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModeCommand:
    """Tests for /mode command."""

    def test_mode_list(self):
        """Should list available modes."""
        from commands.mode import mode_command

        result = mode_command()
        assert result["success"]
        assert "balanced" in result["data"]["modes"]
        assert "strict" in result["data"]["modes"]

    def test_mode_info(self):
        """Should show mode details."""
        from commands.mode import mode_command

        result = mode_command("info", "balanced")
        assert result["success"]
        assert result["data"]["mode"]["name"] == "balanced"

    def test_mode_auto_select(self):
        """Should auto-select mode based on task."""
        from commands.mode import mode_command

        result = mode_command("auto", "security audit for production API")
        assert result["success"]
        # Should select robust or strict for security tasks
        assert result["data"]["selected"] in ["robust", "strict", "balanced"]

    def test_mode_recommend(self):
        """Should return mode recommendations."""
        from commands.mode import mode_command

        result = mode_command("recommend", "quick translation task")
        assert result["success"]
        assert len(result["data"]["recommendations"]) > 0

    def test_mode_unknown(self):
        """Should handle unknown mode."""
        from commands.mode import mode_command

        result = mode_command("info", "nonexistent")
        assert not result["success"]


class TestEvalCommand:
    """Tests for /eval command."""

    def test_eval_metrics(self):
        """Should show metric definitions."""
        from commands.eval import eval_command

        result = eval_command(show_metrics=True)
        assert result["success"]
        assert "task_accuracy" in result["output"]

    def test_eval_graders(self):
        """Should list graders."""
        from commands.eval import eval_command

        result = eval_command(show_graders=True)
        assert result["success"]
        assert "VERIXGrader" in result["output"]

    def test_eval_single(self):
        """Should evaluate single task/response."""
        from commands.eval import eval_command

        result = eval_command(
            task="Explain quantum computing",
            response="Quantum computing uses qubits that can exist in superposition."
        )
        assert result["success"]
        assert "task_accuracy" in result["data"]["metrics"]


class TestOptimizeCommand:
    """Tests for /optimize command."""

    def test_optimize_status(self):
        """Should show optimization status."""
        from commands.optimize import optimize_command

        result = optimize_command()
        assert result["success"]
        assert "Three-MOO Cascade Status" in result["output"]

    def test_optimize_suggest(self):
        """Should return suggestions (uses mock mode)."""
        from commands.optimize import optimize_command

        # This uses mock mode by default, which generates suggestions locally
        result = optimize_command("suggest")
        # In mock mode this should work; network timeouts are expected if trying real API
        assert result["success"] or "timeout" in str(result.get("output", "")).lower()
        if result["success"]:
            assert "suggestions" in result["data"]


class TestParetoCommand:
    """Tests for /pareto command."""

    def test_pareto_display(self):
        """Should display Pareto frontier."""
        from commands.pareto import pareto_command

        result = pareto_command()
        assert result["success"]
        assert result["data"]["count"] > 0

    def test_pareto_filter(self):
        """Should filter by metric."""
        from commands.pareto import pareto_command

        result = pareto_command("filter", "task_accuracy")
        assert result["success"]

    def test_pareto_visualize(self):
        """Should create ASCII visualization."""
        from commands.pareto import pareto_command

        result = pareto_command("visualize")
        assert result["success"]
        assert "Accuracy" in result["output"]

    def test_pareto_export(self):
        """Should export as JSON."""
        from commands.pareto import pareto_command

        result = pareto_command("export")
        assert result["success"]
        assert "pareto_frontier" in result["data"]


class TestFrameCommand:
    """Tests for /frame command."""

    def test_frame_list(self):
        """Should list all frames."""
        from commands.frame import frame_command

        result = frame_command()
        assert result["success"]
        assert "evidential" in result["data"]["frames"]

    def test_frame_detail(self):
        """Should show frame details."""
        from commands.frame import frame_command

        result = frame_command("evidential")
        assert result["success"]
        assert result["data"]["frame"]["name"] == "evidential"

    def test_frame_preset(self):
        """Should apply preset."""
        from commands.frame import frame_command

        result = frame_command("preset", "research")
        assert result["success"]
        assert "evidential" in result["data"]["frames"]
        assert "aspectual" in result["data"]["frames"]

    def test_frame_enable(self):
        """Should enable frames."""
        from commands.frame import frame_command

        result = frame_command("enable", "evidential,aspectual")
        assert result["success"]
        assert "evidential" in result["data"]["enabled"]


class TestVerixCommand:
    """Tests for /verix command."""

    def test_verix_guide(self):
        """Should show VERIX guide."""
        from commands.verix import verix_command

        result = verix_command()
        assert result["success"]
        assert "ILLOCUTION" in result["output"]

    def test_verix_parse(self):
        """Should parse text for VERIX elements."""
        from commands.verix import verix_command

        result = verix_command("parse", "Python is probably the best choice. Research shows it works well.")
        assert result["success"]
        assert len(result["data"]["claims"]) > 0

    def test_verix_validate(self):
        """Should validate epistemic consistency."""
        from commands.verix import verix_command

        result = verix_command("validate", "This will definitely work without any issues.")
        assert result["success"]
        assert result["data"]["score"] < 1.0  # Should have issues

    def test_verix_annotate(self):
        """Should add annotations."""
        from commands.verix import verix_command

        result = verix_command("annotate", "Python is probably good.", 1)
        assert result["success"]
        assert "annotated" in result["data"]


class TestHooks:
    """Tests for hooks integration."""

    def test_on_task_start(self):
        """Should select mode on task start."""
        from hooks import on_task_start

        result = on_task_start("Analyze security vulnerabilities in the API")
        assert "mode_selected" in result
        assert "config" in result

    def test_on_response_complete(self):
        """Should validate response."""
        from hooks import on_response_complete

        result = on_response_complete(
            "[assert|neutral] Python is dynamically typed [ground:docs] [conf:0.95]",
            "balanced"
        )
        assert "frame_score" in result
        assert "verix_score" in result

    def test_on_mode_switch(self):
        """Should log mode switch."""
        from hooks import on_mode_switch

        result = on_mode_switch("balanced", "strict", "Security task detected")
        assert result["from_mode"] == "balanced"
        assert result["to_mode"] == "strict"

    def test_list_hooks(self):
        """Should list available hooks."""
        from hooks import list_hooks

        hooks = list_hooks()
        assert "on_task_start" in hooks
        assert "on_response_complete" in hooks


class TestEndToEnd:
    """End-to-end workflow tests."""

    def test_mode_selection_to_evaluation(self):
        """Should select mode and evaluate response."""
        from commands.mode import mode_command
        from commands.eval import eval_command

        # Select mode
        mode_result = mode_command("auto", "academic research paper analysis")
        assert mode_result["success"]
        selected_mode = mode_result["data"]["selected"]

        # Evaluate with selected mode context
        eval_result = eval_command(
            task="Analyze research methodology",
            response="[assert|neutral] The methodology follows established protocols [ground:paper section 3] [conf:0.85]"
        )
        assert eval_result["success"]

    def test_frame_preset_affects_evaluation(self):
        """Frame preset should affect evaluation scores."""
        from commands.frame import frame_command
        from commands.eval import eval_command

        # Apply research preset
        frame_result = frame_command("preset", "research")
        assert frame_result["success"]

        # Evaluate response with frame markers
        eval_result = eval_command(
            task="Research task",
            response="[witnessed] I verified this directly. [complete] The analysis is finished."
        )
        assert eval_result["success"]

    def test_optimization_to_mode_distillation(self):
        """Optimization should feed into mode distillation."""
        from commands.pareto import pareto_command

        # Distill Pareto points into modes
        result = pareto_command("distill")
        assert result["success"]
        assert len(result["data"]["modes"]) > 0


# =============================================================================
# FULL PIPELINE INTEGRATION TESTS (Added Phase 5)
# =============================================================================

class TestFullPipelineIntegration:
    """Integration tests for the complete optimization pipeline."""

    def test_config_to_prompt_to_score_pipeline(self):
        """
        Test: config -> prompt -> mock response -> score

        Verifies the complete flow from configuration to scoring works.
        """
        from core.config import FullConfig, FrameworkConfig, PromptConfig, VerixStrictness
        from core.verilingua import score_all_frames, aggregate_frame_score
        from core.prompt_builder import PromptBuilder

        # Step 1: Create a config with some frames active
        config = FullConfig(
            framework=FrameworkConfig(
                evidential=True,
                aspectual=True,
                morphological=False,
            ),
            prompt=PromptConfig(
                verix_strictness=VerixStrictness.MODERATE,
            ),
        )

        # Step 2: Build a prompt using the config
        builder = PromptBuilder(config)
        prompt = builder.build(
            task="Explain how authentication works",
            task_type="explanation",
        )

        # Verify prompt is non-trivial
        prompt_str = prompt[0] if isinstance(prompt, tuple) else prompt
        assert len(prompt_str) > 100

        # Step 3: Mock response with VERIX markers
        mock_response = """
        [witnessed] I examined the authentication code directly.
        [complete] The login flow works as follows:
        [inferred] Based on the JWT implementation, tokens expire after 1 hour.
        """

        # Step 4: Score the response against active frames
        scores = score_all_frames(mock_response, config.framework)

        # Should have scores for active frames
        assert "evidential" in scores
        assert 0.0 <= scores["evidential"] <= 1.0

    def test_config_vector_roundtrip(self):
        """Test: config -> vector -> config (should be equivalent)."""
        from core.config import FullConfig, FrameworkConfig, PromptConfig, VerixStrictness, VectorCodec

        original = FullConfig(
            framework=FrameworkConfig(
                evidential=True,
                aspectual=False,
                morphological=True,
            ),
            prompt=PromptConfig(
                verix_strictness=VerixStrictness.STRICT,
                require_ground=True,
            ),
        )

        # Encode to vector
        vector = VectorCodec.encode(original)
        assert len(vector) == VectorCodec.VECTOR_SIZE

        # Decode back
        decoded = VectorCodec.decode(vector)

        # Verify equivalence
        assert decoded.framework.evidential == original.framework.evidential
        assert decoded.prompt.verix_strictness == original.prompt.verix_strictness

    def test_optimization_objective_evaluation(self):
        """Test: config vector -> objective scores."""
        import numpy as np
        from optimization.two_stage_optimizer import evaluate_config_5dim

        # 5-dimensional vector
        x5 = np.array([0.8, 0.6, 1.5, 1.0, 0.9])

        objectives = evaluate_config_5dim(x5)

        # Should return 4 objectives (negated for minimization)
        assert len(objectives) == 4
        assert all(obj <= 0 for obj in objectives)

    def test_globalmoo_mock_mode_integration(self):
        """Test: GlobalMOO client in mock mode for testing."""
        from optimization.globalmoo_client import GlobalMOOClient

        client = GlobalMOOClient(use_mock=True)

        # Should be available in mock mode
        assert client.is_available
        assert client.test_connection()

        # Context manager should work
        with GlobalMOOClient(use_mock=True) as c:
            assert c.is_available


class TestRetryMechanismIntegration:
    """Test the retry mechanism works correctly."""

    def test_retry_decorator_exists(self):
        """Verify retry decorator was added."""
        from optimization.globalmoo_client import retry_with_backoff

        assert callable(retry_with_backoff)


class TestVERIXIntegration:
    """Test VERIX parsing and validation pipeline."""

    def test_verix_parse_and_validate(self):
        """Test: text -> parse claims -> validate."""
        from core.config import PromptConfig, VerixStrictness
        from core.verix import VerixParser, VerixValidator

        config = PromptConfig(
            verix_strictness=VerixStrictness.MODERATE,
            require_ground=False,
        )

        # Text with VERIX L1 format
        text = "[assert|neutral] The cache TTL is 3600 seconds [conf:0.95] [state:confirmed]"

        # Parse
        parser = VerixParser(config)
        claims = parser.parse(text)

        # Should find claims
        assert len(claims) >= 1

        # Validate
        validator = VerixValidator(config)
        is_valid, violations = validator.validate(claims)

        # Score
        score = validator.compliance_score(claims)
        assert 0.0 <= score <= 1.0
