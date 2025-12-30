"""
Tests for telemetry schema and real evaluator.
"""

import pytest
import sys
import os
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.telemetry_schema import (
    ExecutionTelemetry,
    TelemetryBatch,
    TelemetryStore,
    TaskType,
    OutcomeSignal,
    create_telemetry_record,
)
from optimization.real_evaluator import (
    Task,
    RealTaskEvaluator,
    MockRuntime,
    create_mock_evaluator,
    EvaluationResult,
)
from core.config import FullConfig, FrameworkConfig, PromptConfig, VerixStrictness


class TestExecutionTelemetry:
    """Tests for ExecutionTelemetry dataclass."""

    def test_create_default_telemetry(self):
        """Should create telemetry with default values."""
        telemetry = ExecutionTelemetry()

        assert telemetry.task_id is not None
        assert telemetry.timestamp is not None
        assert telemetry.task_type == "general"
        assert telemetry.verix_strictness == 1

    def test_to_dict_roundtrip(self):
        """Should serialize and deserialize correctly."""
        original = ExecutionTelemetry(
            task_type="debugging",
            active_frames=["evidential", "aspectual"],
            verix_strictness=2,
            task_success=True,
        )

        data = original.to_dict()
        restored = ExecutionTelemetry.from_dict(data)

        assert restored.task_type == original.task_type
        assert restored.active_frames == original.active_frames
        assert restored.verix_strictness == original.verix_strictness
        assert restored.task_success == original.task_success

    def test_memory_key_format(self):
        """Should generate valid memory key."""
        telemetry = ExecutionTelemetry()
        key = telemetry.memory_key()

        assert key.startswith("telemetry/executions/")
        assert telemetry.task_id in key


class TestTelemetryBatch:
    """Tests for TelemetryBatch."""

    def test_add_records(self):
        """Should add records and track dates."""
        batch = TelemetryBatch()

        batch.add(ExecutionTelemetry(timestamp="2025-01-01T10:00:00Z"))
        batch.add(ExecutionTelemetry(timestamp="2025-01-02T10:00:00Z"))

        assert len(batch.records) == 2
        assert batch.start_date == "2025-01-01T10:00:00Z"
        assert batch.end_date == "2025-01-02T10:00:00Z"

    def test_filter_by_task_type(self):
        """Should filter records by task type."""
        batch = TelemetryBatch()
        batch.add(ExecutionTelemetry(task_type="debugging"))
        batch.add(ExecutionTelemetry(task_type="explanation"))
        batch.add(ExecutionTelemetry(task_type="debugging"))

        debugging = batch.filter_by_task_type("debugging")
        assert len(debugging) == 2

    def test_compute_statistics(self):
        """Should compute aggregate statistics."""
        batch = TelemetryBatch()
        batch.add(ExecutionTelemetry(
            task_success=True,
            aggregate_frame_score=0.8,
            verix_compliance_score=0.7,
            response_tokens=100,
        ))
        batch.add(ExecutionTelemetry(
            task_success=False,
            aggregate_frame_score=0.6,
            verix_compliance_score=0.5,
            response_tokens=200,
        ))

        stats = batch.compute_statistics()

        assert stats["total_records"] == 2
        assert stats["successful_records"] == 1
        assert stats["success_rate"] == 0.5
        assert stats["avg_frame_score"] == 0.7
        assert stats["avg_verix_compliance"] == 0.6


class TestTelemetryStore:
    """Tests for TelemetryStore."""

    def test_store_and_load(self):
        """Should store and load telemetry records."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TelemetryStore(base_path=tmpdir)

            record = ExecutionTelemetry(
                task_type="testing",
                task_success=True,
            )

            key = store.store(record)
            assert key is not None

            # Verify file was created
            files = list(store.base_path.glob("*.json"))
            assert len(files) == 1


class TestTask:
    """Tests for Task dataclass."""

    def test_prompt_hash(self):
        """Should generate consistent hash."""
        task = Task(prompt="Test prompt")
        hash1 = task.prompt_hash()
        hash2 = task.prompt_hash()

        assert hash1 == hash2
        assert len(hash1) == 12


class TestMockRuntime:
    """Tests for MockRuntime."""

    def test_execute_returns_response(self):
        """Should return mock response."""
        runtime = MockRuntime()
        result = runtime.execute("Test prompt")

        assert result.success is True
        assert len(result.response) > 0
        assert result.tokens_used > 0

    def test_custom_response_generator(self):
        """Should use custom response generator."""
        def custom_gen(prompt):
            return f"Custom: {prompt}"

        runtime = MockRuntime(response_generator=custom_gen)
        result = runtime.execute("Test")

        assert "Custom: Test" in result.response


class TestRealTaskEvaluator:
    """Tests for RealTaskEvaluator."""

    def test_evaluate_with_mock(self):
        """Should evaluate task and return result."""
        evaluator = create_mock_evaluator()

        config = FullConfig(
            framework=FrameworkConfig(evidential=True, aspectual=True),
            prompt=PromptConfig(verix_strictness=VerixStrictness.MODERATE),
        )
        task = Task(prompt="Explain authentication", task_type="explanation")

        result = evaluator.evaluate(config, task)

        assert isinstance(result, EvaluationResult)
        assert result.execution.success is True
        assert 0.0 <= result.task_accuracy <= 1.0
        assert 0.0 <= result.token_efficiency <= 1.0
        assert 0.0 <= result.frame_compliance <= 1.0

    def test_evaluate_stores_telemetry(self):
        """Should store telemetry when enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            evaluator = RealTaskEvaluator(
                runtime=MockRuntime(),
                store_telemetry=True,
            )
            evaluator.telemetry_store = TelemetryStore(base_path=tmpdir)

            config = FullConfig()
            task = Task(prompt="Test")

            evaluator.evaluate(config, task)

            # Check telemetry was stored
            files = list(evaluator.telemetry_store.base_path.glob("*.json"))
            assert len(files) == 1

    def test_to_objectives(self):
        """Should return objectives dict."""
        evaluator = create_mock_evaluator()
        config = FullConfig()
        task = Task(prompt="Test")

        result = evaluator.evaluate(config, task)
        objectives = result.to_objectives()

        assert "task_accuracy" in objectives
        assert "token_efficiency" in objectives
        assert "frame_compliance" in objectives
        assert "verix_compliance" in objectives

    def test_evaluate_batch(self):
        """Should evaluate multiple tasks."""
        evaluator = create_mock_evaluator()
        config = FullConfig()
        tasks = [
            Task(prompt="Task 1"),
            Task(prompt="Task 2"),
            Task(prompt="Task 3"),
        ]

        results = evaluator.evaluate_batch(config, tasks)

        assert len(results) == 3
        assert all(isinstance(r, EvaluationResult) for r in results)
