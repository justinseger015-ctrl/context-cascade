"""
Tests for optimization/dspy_level2.py and optimization/dspy_level1.py

Tests:
- DSPyLevel2Optimizer caching
- ClusterCache operations
- DSPyLevel1Analyzer telemetry
- EvolutionProposal generation
"""

import pytest
import tempfile
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.dspy_level2 import (
    DSPyLevel2Optimizer,
    ClusterCache,
    CompiledPrompt,
    create_l2_optimizer,
    get_cluster_key,
)
from optimization.dspy_level1 import (
    DSPyLevel1Analyzer,
    TelemetryAggregator,
    TelemetryPoint,
    EvolutionProposal,
    ProposalType,
    ProposalStatus,
    create_l1_analyzer,
)
from core.config import FullConfig, VectorCodec


class TestCompiledPrompt:
    """Tests for CompiledPrompt dataclass."""

    def test_create_prompt(self):
        """Should create compiled prompt."""
        prompt = CompiledPrompt(
            cluster_key="test-cluster",
            system_prompt="System instruction",
            user_template="User: {task}",
            config_vector=[0.5] * 14,
        )
        assert prompt.cluster_key == "test-cluster"
        assert "{task}" in prompt.user_template

    def test_to_dict(self):
        """to_dict should serialize all fields."""
        prompt = CompiledPrompt(
            cluster_key="test",
            system_prompt="System",
            user_template="User",
            config_vector=[1.0] * 14,
            metadata={"test": True},
        )
        d = prompt.to_dict()
        assert d["cluster_key"] == "test"
        assert d["metadata"]["test"] is True

    def test_from_dict(self):
        """from_dict should reconstruct prompt."""
        original = CompiledPrompt(
            cluster_key="test",
            system_prompt="System",
            user_template="User",
            config_vector=[0.5] * 14,
        )
        d = original.to_dict()
        reconstructed = CompiledPrompt.from_dict(d)
        assert reconstructed.cluster_key == original.cluster_key

    def test_age_seconds(self):
        """age_seconds should return positive value."""
        prompt = CompiledPrompt(
            cluster_key="test",
            system_prompt="",
            user_template="",
            config_vector=[],
        )
        age = prompt.age_seconds()
        assert age >= 0


class TestClusterCache:
    """Tests for ClusterCache."""

    def test_put_and_get(self):
        """Should cache and retrieve prompts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = ClusterCache(cache_dir=Path(tmpdir))

            prompt = CompiledPrompt(
                cluster_key="test-key",
                system_prompt="System",
                user_template="User",
                config_vector=[0.5] * 14,
            )
            cache.put(prompt)

            retrieved = cache.get("test-key")
            assert retrieved is not None
            assert retrieved.cluster_key == "test-key"

    def test_get_missing_returns_none(self):
        """get() should return None for missing keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = ClusterCache(cache_dir=Path(tmpdir))
            assert cache.get("nonexistent") is None

    def test_invalidate(self):
        """invalidate should remove cached prompt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = ClusterCache(cache_dir=Path(tmpdir))

            prompt = CompiledPrompt(
                cluster_key="to-invalidate",
                system_prompt="",
                user_template="",
                config_vector=[],
            )
            cache.put(prompt)
            assert cache.get("to-invalidate") is not None

            result = cache.invalidate("to-invalidate")
            assert result is True
            assert cache.get("to-invalidate") is None

    def test_list_clusters(self):
        """list_clusters should return cached keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = ClusterCache(cache_dir=Path(tmpdir))

            for i in range(3):
                prompt = CompiledPrompt(
                    cluster_key=f"cluster-{i}",
                    system_prompt="",
                    user_template="",
                    config_vector=[],
                )
                cache.put(prompt)

            clusters = cache.list_clusters()
            assert len(clusters) == 3

    def test_stats(self):
        """stats should return cache statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = ClusterCache(cache_dir=Path(tmpdir))

            prompt = CompiledPrompt(
                cluster_key="test",
                system_prompt="",
                user_template="",
                config_vector=[],
            )
            cache.put(prompt)

            stats = cache.stats()
            assert stats["cached_count"] == 1


class TestDSPyLevel2Optimizer:
    """Tests for DSPyLevel2Optimizer."""

    def test_get_prompt_caches(self):
        """get_prompt should cache compiled prompts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            optimizer = DSPyLevel2Optimizer(cache_dir=Path(tmpdir))

            config = FullConfig()
            prompt1 = optimizer.get_prompt(config, "reasoning")
            prompt2 = optimizer.get_prompt(config, "reasoning")

            # Should be same object (cached)
            assert prompt1.cluster_key == prompt2.cluster_key

            stats = optimizer.stats()
            assert stats["cache_hits"] >= 1

    def test_get_prompts_for_vector(self):
        """get_prompts_for_vector should work with vectors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            optimizer = DSPyLevel2Optimizer(cache_dir=Path(tmpdir))

            vector = VectorCodec.encode(FullConfig())
            prompt = optimizer.get_prompts_for_vector(vector, "default")

            assert prompt is not None
            assert len(prompt.system_prompt) > 0

    def test_compile_batch(self):
        """compile_batch should compile multiple configs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            optimizer = DSPyLevel2Optimizer(cache_dir=Path(tmpdir))

            configs = [FullConfig() for _ in range(3)]
            prompts = optimizer.compile_batch(configs, "coding")

            assert len(prompts) == 3

    def test_stats_tracks_hits_and_compiles(self):
        """stats should track cache hits and compiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            optimizer = DSPyLevel2Optimizer(cache_dir=Path(tmpdir))

            config = FullConfig()
            optimizer.get_prompt(config)  # Compile
            optimizer.get_prompt(config)  # Hit

            stats = optimizer.stats()
            assert stats["compile_count"] >= 1
            assert stats["cache_hits"] >= 1
            assert stats["hit_rate"] > 0


class TestTelemetryAggregator:
    """Tests for TelemetryAggregator."""

    def test_record_outcome(self):
        """record_outcome should store points."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agg = TelemetryAggregator(storage_dir=Path(tmpdir))

            agg.record_outcome(
                config_vector=[0.5] * 14,
                outcomes={"task_accuracy": 0.8},
                task_type="reasoning",
            )

            points = agg.get_points()
            assert len(points) == 1
            assert points[0].outcomes["task_accuracy"] == 0.8

    def test_get_points_with_filter(self):
        """get_points should filter by task_type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agg = TelemetryAggregator(storage_dir=Path(tmpdir))

            agg.record_outcome([0.5] * 14, {"a": 1}, "reasoning")
            agg.record_outcome([0.5] * 14, {"a": 2}, "coding")

            reasoning_points = agg.get_points(task_type="reasoning")
            assert len(reasoning_points) == 1

    def test_aggregate_by_cluster(self):
        """aggregate_by_cluster should average outcomes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agg = TelemetryAggregator(storage_dir=Path(tmpdir))

            config = FullConfig()
            vector = VectorCodec.encode(config)

            agg.record_outcome(vector, {"accuracy": 0.8}, "default")
            agg.record_outcome(vector, {"accuracy": 0.9}, "default")

            aggregated = agg.aggregate_by_cluster()
            assert len(aggregated) > 0

    def test_save_and_load(self):
        """save and load should persist telemetry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agg1 = TelemetryAggregator(storage_dir=Path(tmpdir))
            agg1.record_outcome([0.5] * 14, {"m": 0.7}, "test")
            agg1.save("test.jsonl")

            agg2 = TelemetryAggregator(storage_dir=Path(tmpdir))
            count = agg2.load("test.jsonl")
            assert count == 1


class TestEvolutionProposal:
    """Tests for EvolutionProposal dataclass."""

    def test_create_proposal(self):
        """Should create proposal."""
        proposal = EvolutionProposal(
            proposal_id="L1-0001",
            proposal_type=ProposalType.FRAME_ACTIVATION,
            description="Disable spatial frame",
            rationale="Low accuracy when enabled",
            changes={"frame": "spatial", "enabled": False},
            expected_impact={"task_accuracy": 0.05},
        )
        assert proposal.status == ProposalStatus.PROPOSED

    def test_to_dict(self):
        """to_dict should serialize proposal."""
        proposal = EvolutionProposal(
            proposal_id="test",
            proposal_type=ProposalType.VERIX_ADJUSTMENT,
            description="Test",
            rationale="Test",
            changes={},
            expected_impact={},
        )
        d = proposal.to_dict()
        assert d["proposal_id"] == "test"
        assert d["proposal_type"] == "verix_adjustment"


class TestDSPyLevel1Analyzer:
    """Tests for DSPyLevel1Analyzer."""

    def test_analyze_needs_samples(self):
        """analyze should return empty with few samples."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = DSPyLevel1Analyzer(
                telemetry=TelemetryAggregator(storage_dir=Path(tmpdir)),
                proposals_dir=Path(tmpdir) / "proposals",
            )

            # No telemetry - should return empty
            proposals = analyzer.analyze(min_samples=50)
            assert len(proposals) == 0

    def test_accept_proposal(self):
        """accept_proposal should change status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = DSPyLevel1Analyzer(proposals_dir=Path(tmpdir))

            # Manually add proposal
            proposal = EvolutionProposal(
                proposal_id="test-001",
                proposal_type=ProposalType.FRAME_ACTIVATION,
                description="Test",
                rationale="Test",
                changes={},
                expected_impact={},
            )
            analyzer._proposals.append(proposal)

            result = analyzer.accept_proposal("test-001")
            assert result is True
            assert proposal.status == ProposalStatus.ACCEPTED

    def test_get_proposals_by_status(self):
        """get_proposals should filter by status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = DSPyLevel1Analyzer(proposals_dir=Path(tmpdir))

            # Add proposals with different statuses
            p1 = EvolutionProposal("p1", ProposalType.FRAME_ACTIVATION, "", "", {}, {})
            p2 = EvolutionProposal("p2", ProposalType.FRAME_ACTIVATION, "", "", {}, {})
            p2.status = ProposalStatus.ACCEPTED

            analyzer._proposals.extend([p1, p2])

            proposed = analyzer.get_proposals(ProposalStatus.PROPOSED)
            assert len(proposed) == 1


class TestFactoryFunctions:
    """Tests for factory functions."""

    def test_create_l2_optimizer(self):
        """create_l2_optimizer should return optimizer."""
        with tempfile.TemporaryDirectory() as tmpdir:
            optimizer = create_l2_optimizer(cache_dir=Path(tmpdir))
            assert isinstance(optimizer, DSPyLevel2Optimizer)

    def test_create_l1_analyzer(self):
        """create_l1_analyzer should return analyzer."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = create_l1_analyzer(
                telemetry_dir=Path(tmpdir) / "telemetry",
                proposals_dir=Path(tmpdir) / "proposals",
            )
            assert isinstance(analyzer, DSPyLevel1Analyzer)

    def test_get_cluster_key(self):
        """get_cluster_key should return string."""
        config = FullConfig()
        key = get_cluster_key(config)
        assert isinstance(key, str)
        assert len(key) > 0
