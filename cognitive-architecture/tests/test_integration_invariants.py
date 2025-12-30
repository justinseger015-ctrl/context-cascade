"""
Integration Invariant Tests

These tests verify the NON-NEGOTIABLE INVARIANTS of the integration:
1. Thin waist contract unchanged
2. Harness is authoritative (no model-reported metrics)
3. Bridge is the only writer of runtime_config.json
4. Events are append-only
5. Ralph E2E smoke test
6. Regression gate works
7. Cache key includes config

Run with: pytest tests/test_integration_invariants.py -v
"""

import os
import sys
import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.prompt_builder import PromptBuilder, build_prompt
from core.config import FullConfig, VectorCodec
from integration.unified_bridge import UnifiedBridge, BridgeInput, UnifiedEvent, compute_cache_key
from integration.auditors import AuditorPanel, SkillAuditor, OutputAuditor
from loopctl.core import ralph_iteration_complete, FrozenHarness


class TestThinWaistContract:
    """E1: test_thin_waist_contract_unchanged"""

    def test_build_signature_returns_tuple(self):
        """Verify build() returns a tuple of two strings."""
        builder = PromptBuilder(FullConfig())
        result = builder.build("Test task", "default")

        assert isinstance(result, tuple), "build() must return a tuple"
        assert len(result) == 2, "build() must return exactly 2 elements"
        assert isinstance(result[0], str), "First element must be string (system_prompt)"
        assert isinstance(result[1], str), "Second element must be string (user_prompt)"

    def test_build_signature_accepts_task_and_type(self):
        """Verify build() accepts task and task_type arguments."""
        builder = PromptBuilder(FullConfig())

        # These should not raise
        builder.build("task", "reasoning")
        builder.build("task", "coding")
        builder.build("task", "analysis")
        builder.build("task", "creative")
        builder.build("task", "conversational")
        builder.build("task", "default")

    def test_convenience_function_matches_class(self):
        """Verify build_prompt() function matches PromptBuilder.build()."""
        config = FullConfig()
        task = "Test task"
        task_type = "reasoning"

        builder = PromptBuilder(config)
        class_result = builder.build(task, task_type)
        func_result = build_prompt(task, task_type, config)

        assert class_result == func_result, "Convenience function must match class method"


class TestHarnessAuthority:
    """E2: test_harness_is_authoritative"""

    def test_harness_produces_metrics(self):
        """Verify FrozenHarness produces metrics dict."""
        with tempfile.TemporaryDirectory() as tmpdir:
            harness = FrozenHarness(Path(tmpdir))

            # Create test artifact
            artifact_path = Path(tmpdir) / "test_artifact.txt"
            artifact_path.write_text("This is a test artifact with [assert|confident] VERIX markers")

            metrics = harness.grade(artifact_path)

            assert isinstance(metrics, dict), "Harness must return dict"
            assert "task_accuracy" in metrics, "Must have task_accuracy"
            assert "token_efficiency" in metrics, "Must have token_efficiency"
            assert "edge_robustness" in metrics, "Must have edge_robustness"
            assert "epistemic_consistency" in metrics, "Must have epistemic_consistency"
            assert "overall" in metrics, "Must have overall score"

    def test_bridge_rejects_model_reported_metrics(self):
        """Verify bridge rejects history entries with model-reported metrics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loop_dir = Path(tmpdir)
            self._setup_loop_dir(loop_dir)

            bridge = UnifiedBridge(loop_dir)

            # Create input with model-reported metrics (VIOLATION)
            bridge_input = BridgeInput(
                iteration=1,
                artifact_path=None,
                eval_report={"metrics": {}},
                history=[{"model_reported_metrics": {"accuracy": 0.9}}],  # VIOLATION
                policy={},
                task_metadata={},
                current_config=bridge._default_config(),
            )

            with pytest.raises(ValueError, match="model-reported metrics"):
                bridge.propose_next_config(bridge_input)

    def _setup_loop_dir(self, loop_dir: Path):
        """Set up minimal .loop/ directory."""
        loop_dir.mkdir(exist_ok=True)
        (loop_dir / "runtime_config.json").write_text(json.dumps({
            "mode": "balanced",
            "vector14": [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            "verix": {},
            "frames": {},
            "iteration": 0,
            "previous_harness_score": 0.0,
        }))
        (loop_dir / "policy.json").write_text(json.dumps({
            "regression_threshold": 0.03,
            "max_iterations": 50,
        }))
        (loop_dir / "events.jsonl").write_text("")


class TestBridgeOnlyWriter:
    """E3: test_bridge_only_writer"""

    def test_write_config_only_through_bridge(self):
        """Verify runtime_config.json can only be written by bridge."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loop_dir = Path(tmpdir)
            loop_dir.mkdir(exist_ok=True)

            # Initialize with default
            config_path = loop_dir / "runtime_config.json"
            config_path.write_text(json.dumps({"iteration": 0}))

            bridge = UnifiedBridge(loop_dir)

            # Create mock BridgeOutput
            from integration.unified_bridge import BridgeOutput, DecisionIntent
            mock_output = BridgeOutput(
                decision_intent=DecisionIntent.CONTINUE,
                mode="balanced",
                vector14=[1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                verix={"strictness": "MODERATE"},
                frames={"evidential": True},
                reasons=["Test"],
            )

            # Write through bridge
            bridge.write_config(mock_output, iteration=1, prev_score=0.5)

            # Verify file was updated
            config = json.loads(config_path.read_text())
            assert config["iteration"] == 1, "Iteration should be updated"
            assert config["mode"] == "balanced", "Mode should be set"
            assert "_comment" in config, "Bridge adds comment marker"


class TestEventsAppendOnly:
    """E4: test_events_append_only"""

    def test_events_are_appended(self):
        """Verify events.jsonl is append-only."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loop_dir = Path(tmpdir)
            loop_dir.mkdir(exist_ok=True)
            events_path = loop_dir / "events.jsonl"
            events_path.write_text("")

            bridge = UnifiedBridge(loop_dir)

            # Append first event
            event1 = UnifiedEvent(
                task_id="test_1",
                iteration=1,
                decision="continue",
            )
            bridge.append_event(event1)

            # Append second event
            event2 = UnifiedEvent(
                task_id="test_2",
                iteration=2,
                decision="continue",
            )
            bridge.append_event(event2)

            # Verify both events exist
            lines = events_path.read_text().strip().split("\n")
            assert len(lines) == 2, "Should have 2 events"

            parsed = [json.loads(line) for line in lines]
            assert parsed[0]["task_id"] == "test_1"
            assert parsed[1]["task_id"] == "test_2"

    def test_events_have_monotonic_timestamps(self):
        """Verify events have monotonically increasing timestamps."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loop_dir = Path(tmpdir)
            loop_dir.mkdir(exist_ok=True)
            events_path = loop_dir / "events.jsonl"
            events_path.write_text("")

            bridge = UnifiedBridge(loop_dir)

            # Append events
            for i in range(3):
                event = UnifiedEvent(task_id=f"test_{i}", iteration=i)
                bridge.append_event(event)

            # Verify timestamps are monotonic
            lines = events_path.read_text().strip().split("\n")
            timestamps = [json.loads(line)["timestamp"] for line in lines]

            for i in range(1, len(timestamps)):
                assert timestamps[i] >= timestamps[i-1], "Timestamps must be monotonic"


class TestRalphE2ESmoke:
    """E5: test_ralph_e2e_smoke"""

    def test_two_iterations(self):
        """Simulate 2 iterations of Ralph loop."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loop_dir = Path(tmpdir)
            self._setup_full_loop_dir(loop_dir)

            # Create artifact for iteration 1
            artifact_path = loop_dir / "output" / "latest.txt"
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text("Iteration 1 output with [assert|confident] markers")

            # Run iteration 1
            result1 = ralph_iteration_complete(
                state_path=str(loop_dir / "state.md"),
                loop_dir=str(loop_dir),
                output_path=str(artifact_path),
                iteration=0,
            )

            assert "decision" in result1, "Must return decision"
            assert result1["decision"] in ["block", "allow"], "Decision must be block or allow"

            # If blocked, run iteration 2
            if result1["decision"] == "block":
                artifact_path.write_text("Iteration 2 improved output [assert|confident] [conf:0.95]")

                result2 = ralph_iteration_complete(
                    state_path=str(loop_dir / "state.md"),
                    loop_dir=str(loop_dir),
                    output_path=str(artifact_path),
                    iteration=1,
                )

                assert "decision" in result2

    def _setup_full_loop_dir(self, loop_dir: Path):
        """Set up complete .loop/ directory for testing."""
        loop_dir.mkdir(exist_ok=True)

        (loop_dir / "runtime_config.json").write_text(json.dumps({
            "_schema_version": "1.0.0",
            "mode": "balanced",
            "vector14": [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            "verix": {"strictness": "MODERATE", "compression": "L1"},
            "frames": {"evidential": True, "aspectual": True},
            "iteration": 0,
            "previous_harness_score": 0.0,
        }))

        (loop_dir / "policy.json").write_text(json.dumps({
            "regression_threshold": 0.03,
            "max_iterations": 50,
            "harness_hash": "frozen_eval_harness_v1.0.0",
        }))

        (loop_dir / "history.json").write_text(json.dumps({"iterations": []}))
        (loop_dir / "events.jsonl").write_text("")
        (loop_dir / "task_metadata.json").write_text(json.dumps({"task_type": "general"}))
        (loop_dir / "state.md").write_text("---\niteration: 0\n---\nTest task")


class TestRegressionGate:
    """E6: test_regression_gate"""

    def test_regression_triggers_halt(self):
        """Verify regression above threshold triggers HALT."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loop_dir = Path(tmpdir)
            loop_dir.mkdir(exist_ok=True)

            # Set up with previous score higher than current
            (loop_dir / "runtime_config.json").write_text(json.dumps({
                "mode": "balanced",
                "vector14": [1]*14,
                "verix": {},
                "frames": {},
                "iteration": 5,
                "previous_harness_score": 0.85,  # Previous was good
            }))

            (loop_dir / "policy.json").write_text(json.dumps({
                "regression_threshold": 0.03,
                "max_iterations": 50,
            }))

            (loop_dir / "events.jsonl").write_text("")

            bridge = UnifiedBridge(loop_dir)

            # Current score is much lower (regression)
            bridge_input = BridgeInput(
                iteration=5,
                artifact_path=None,
                eval_report={"metrics": {"overall": 0.50}},  # Significant regression
                history=[],
                policy={"regression_threshold": 0.03},
                task_metadata={},
                current_config=bridge.load_runtime_config(),
            )

            result = bridge.propose_next_config(bridge_input)

            from integration.unified_bridge import DecisionIntent
            assert result.decision_intent == DecisionIntent.HALT, "Should HALT on regression"


class TestCacheKeyIncludesConfig:
    """E7: test_cache_key_includes_config"""

    def test_different_configs_different_keys(self):
        """Verify same task with different configs produces different cache keys."""
        task = "Analyze this code"

        config1 = {
            "vector14": [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            "frames": {"evidential": True},
            "verix": {"strictness": "MODERATE"},
        }

        config2 = {
            "vector14": [1, 1, 1, 1, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0],  # Different
            "frames": {"evidential": True, "morphological": True},
            "verix": {"strictness": "STRICT"},
        }

        key1 = compute_cache_key(task, config1)
        key2 = compute_cache_key(task, config2)

        assert key1 != key2, "Different configs must produce different cache keys"

    def test_same_config_same_key(self):
        """Verify same task and config produces same cache key."""
        task = "Analyze this code"

        config = {
            "vector14": [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            "frames": {"evidential": True},
            "verix": {"strictness": "MODERATE"},
        }

        key1 = compute_cache_key(task, config)
        key2 = compute_cache_key(task, config)

        assert key1 == key2, "Same config must produce same cache key"


class TestAuditorOutput:
    """Additional tests for VERIX-speaking auditors."""

    def test_auditors_emit_valid_json(self):
        """Verify all auditors emit valid JSON with required fields."""
        panel = AuditorPanel()

        result = panel.audit_all(
            artifact="Test artifact content",
            eval_report={"metrics": {"task_accuracy": 0.7, "overall": 0.7}},
            runtime_config={"mode": "balanced", "frames": {}},
        )

        assert "auditor_results" in result
        assert len(result["auditor_results"]) == 4  # 4 auditors

        for auditor_result in result["auditor_results"]:
            assert "auditor_type" in auditor_result
            assert "verix" in auditor_result
            assert "claims" in auditor_result
            assert "action_class" in auditor_result
            assert "confidence" in auditor_result
            assert "grounds" in auditor_result

    def test_auditor_consensus_detection(self):
        """Verify consensus and disagreement detection works."""
        panel = AuditorPanel()

        # High scores should produce consensus ACCEPT
        result_high = panel.audit_all(
            artifact="Test with [assert|confident] markers [conf:0.95]",
            eval_report={"metrics": {
                "task_accuracy": 0.9,
                "token_efficiency": 0.8,
                "edge_robustness": 0.85,
                "epistemic_consistency": 0.9,
                "overall": 0.86,
            }},
            runtime_config={"mode": "balanced", "frames": {"evidential": True}},
        )

        assert result_high["consensus"]["accept_count"] >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
