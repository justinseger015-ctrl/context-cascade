"""
DSPy Level 2: Per-cluster prompt expression caching.

Cadence: Minutes to hours
Scope: Compile prompts per cluster key (frame_set + verix_strictness)

This layer caches compiled prompts by cluster, reducing latency
and ensuring consistency within evaluation runs.
"""

import os
import json
import time
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec
from core.prompt_builder import PromptBuilder


@dataclass
class CompiledPrompt:
    """A compiled prompt with metadata."""

    cluster_key: str
    system_prompt: str
    user_template: str
    config_vector: List[float]
    compiled_at: float = field(default_factory=time.time)
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cluster_key": self.cluster_key,
            "system_prompt": self.system_prompt,
            "user_template": self.user_template,
            "config_vector": self.config_vector,
            "compiled_at": self.compiled_at,
            "version": self.version,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompiledPrompt":
        return cls(
            cluster_key=data["cluster_key"],
            system_prompt=data["system_prompt"],
            user_template=data["user_template"],
            config_vector=data["config_vector"],
            compiled_at=data.get("compiled_at", time.time()),
            version=data.get("version", 1),
            metadata=data.get("metadata", {}),
        )

    def age_seconds(self) -> float:
        """Get age of compiled prompt in seconds."""
        return time.time() - self.compiled_at


@dataclass
class ClusterCache:
    """Cache for compiled prompts by cluster."""

    cache_dir: Path
    max_age_seconds: float = 3600.0  # 1 hour default
    _cache: Dict[str, CompiledPrompt] = field(default_factory=dict)

    def __post_init__(self):
        self.cache_dir = Path(self.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._load_from_disk()

    def get(self, cluster_key: str) -> Optional[CompiledPrompt]:
        """
        Get cached prompt by cluster key.

        Returns None if not cached or expired.
        """
        if cluster_key in self._cache:
            prompt = self._cache[cluster_key]
            if prompt.age_seconds() < self.max_age_seconds:
                return prompt
            # Expired - remove
            del self._cache[cluster_key]

        return None

    def put(self, prompt: CompiledPrompt) -> None:
        """Cache a compiled prompt."""
        self._cache[prompt.cluster_key] = prompt
        self._save_to_disk(prompt)

    def invalidate(self, cluster_key: str) -> bool:
        """
        Invalidate cached prompt.

        Returns True if prompt was cached.
        """
        if cluster_key in self._cache:
            del self._cache[cluster_key]
            cache_file = self._cache_file(cluster_key)
            if cache_file.exists():
                cache_file.unlink()
            return True
        return False

    def invalidate_all(self) -> int:
        """Invalidate all cached prompts. Returns count."""
        count = len(self._cache)
        self._cache.clear()
        for f in self.cache_dir.glob("*.json"):
            f.unlink()
        return count

    def list_clusters(self) -> List[str]:
        """List all cached cluster keys."""
        return list(self._cache.keys())

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "cached_count": len(self._cache),
            "oldest_age": max(
                (p.age_seconds() for p in self._cache.values()),
                default=0.0
            ),
            "newest_age": min(
                (p.age_seconds() for p in self._cache.values()),
                default=0.0
            ),
        }

    def _cache_file(self, cluster_key: str) -> Path:
        """Get cache file path for cluster key."""
        safe_key = hashlib.md5(cluster_key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.json"

    def _save_to_disk(self, prompt: CompiledPrompt) -> None:
        """Persist prompt to disk."""
        cache_file = self._cache_file(prompt.cluster_key)
        with open(cache_file, "w") as f:
            json.dump(prompt.to_dict(), f, indent=2)

    def _load_from_disk(self) -> None:
        """Load cached prompts from disk."""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file) as f:
                    data = json.load(f)
                prompt = CompiledPrompt.from_dict(data)
                if prompt.age_seconds() < self.max_age_seconds:
                    self._cache[prompt.cluster_key] = prompt
                else:
                    cache_file.unlink()  # Remove expired
            except Exception:
                pass  # Skip corrupted cache files


class DSPyLevel2Optimizer:
    """
    Level 2 prompt optimization: per-cluster caching.

    Compiles prompts for each unique cluster (config combination)
    and caches them for fast repeated access during evaluation.
    """

    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        max_cache_age: float = 3600.0,
    ):
        """
        Initialize L2 optimizer.

        Args:
            cache_dir: Directory for cache storage
            max_cache_age: Maximum cache age in seconds
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "storage" / "prompts"

        self.cache = ClusterCache(
            cache_dir=cache_dir,
            max_age_seconds=max_cache_age,
        )
        self._compile_count = 0
        self._cache_hits = 0

    def get_prompt(
        self,
        config: FullConfig,
        task_type: str = "default",
    ) -> CompiledPrompt:
        """
        Get compiled prompt for configuration.

        Uses cache if available, otherwise compiles and caches.

        Args:
            config: Full configuration
            task_type: Type of task

        Returns:
            Compiled prompt
        """
        cluster_key = VectorCodec.cluster_key(config)
        cache_key = f"{cluster_key}:{task_type}"

        # Check cache
        cached = self.cache.get(cache_key)
        if cached:
            self._cache_hits += 1
            return cached

        # Compile new prompt
        prompt = self._compile(config, task_type)
        self.cache.put(prompt)
        self._compile_count += 1

        return prompt

    def get_prompts_for_vector(
        self,
        vector: List[float],
        task_type: str = "default",
    ) -> CompiledPrompt:
        """
        Get compiled prompt for config vector.

        Args:
            vector: Configuration vector
            task_type: Type of task

        Returns:
            Compiled prompt
        """
        config = VectorCodec.decode(vector)
        return self.get_prompt(config, task_type)

    def compile_batch(
        self,
        configs: List[FullConfig],
        task_type: str = "default",
    ) -> List[CompiledPrompt]:
        """
        Pre-compile prompts for multiple configurations.

        Args:
            configs: List of configurations
            task_type: Type of task

        Returns:
            List of compiled prompts
        """
        prompts = []
        for config in configs:
            prompt = self.get_prompt(config, task_type)
            prompts.append(prompt)
        return prompts

    def warm_cache(
        self,
        vectors: List[List[float]],
        task_type: str = "default",
    ) -> int:
        """
        Warm cache with config vectors.

        Args:
            vectors: List of config vectors
            task_type: Type of task

        Returns:
            Number of new prompts compiled
        """
        new_count = 0
        for vector in vectors:
            config = VectorCodec.decode(vector)
            cluster_key = VectorCodec.cluster_key(config)
            cache_key = f"{cluster_key}:{task_type}"

            if self.cache.get(cache_key) is None:
                self.get_prompt(config, task_type)
                new_count += 1

        return new_count

    def stats(self) -> Dict[str, Any]:
        """Get optimizer statistics."""
        cache_stats = self.cache.stats()
        total_requests = self._compile_count + self._cache_hits
        hit_rate = self._cache_hits / total_requests if total_requests > 0 else 0.0

        return {
            "compile_count": self._compile_count,
            "cache_hits": self._cache_hits,
            "hit_rate": hit_rate,
            **cache_stats,
        }

    def _compile(
        self,
        config: FullConfig,
        task_type: str,
    ) -> CompiledPrompt:
        """Compile prompt for configuration."""
        builder = PromptBuilder(config)
        system_prompt, user_template = builder.build("{task}", task_type)

        cluster_key = VectorCodec.cluster_key(config)
        cache_key = f"{cluster_key}:{task_type}"

        return CompiledPrompt(
            cluster_key=cache_key,
            system_prompt=system_prompt,
            user_template=user_template,
            config_vector=VectorCodec.encode(config),
            metadata={
                "task_type": task_type,
                "frame_count": config.framework.frame_count(),
                "verix_strictness": config.prompt.verix_strictness.value,
            },
        )


# Anti-Goodhart Metrics (Phase B.3)

@dataclass
class AntiGoodhartMetrics:
    """
    Metrics that prevent overfitting to a single objective.

    These metrics penalize behaviors that indicate Goodhart's Law
    (optimizing the metric instead of the underlying goal):
    - diversity_score: Penalize output monoculture
    - coverage_breadth: Reward testing edge cases
    - calibration_error: Penalize overconfidence
    - regression_rate: Track capability preservation
    """

    diversity_score: float = 0.0       # Entropy of output distribution
    coverage_breadth: float = 0.0      # % of edge cases tested
    calibration_error: float = 0.0     # |predicted_confidence - actual_accuracy|
    regression_rate: float = 0.0       # % of capabilities regressed
    timestamp: float = field(default_factory=time.time)

    def composite_score(self) -> float:
        """
        Compute composite anti-Goodhart score.

        Higher is better (more robust against overfitting).
        """
        # Normalize components (all should be in [0, 1])
        div_contrib = min(1.0, self.diversity_score)
        cov_contrib = min(1.0, self.coverage_breadth)
        cal_contrib = max(0.0, 1.0 - self.calibration_error)  # Invert: lower error = better
        reg_contrib = max(0.0, 1.0 - self.regression_rate)    # Invert: lower regression = better

        # Weighted average (equal weights for now)
        return (div_contrib + cov_contrib + cal_contrib + reg_contrib) / 4.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "diversity_score": self.diversity_score,
            "coverage_breadth": self.coverage_breadth,
            "calibration_error": self.calibration_error,
            "regression_rate": self.regression_rate,
            "composite_score": self.composite_score(),
            "timestamp": self.timestamp,
        }


class PromptClusterManager:
    """
    Manager for prompt clusters (Phase B.2).

    Provides higher-level operations on clusters:
    - Cluster lifecycle management
    - Cross-cluster statistics
    - Cluster migration and versioning
    - Anti-Goodhart metric tracking per cluster
    """

    def __init__(
        self,
        optimizer: DSPyLevel2Optimizer,
        metrics_dir: Optional[Path] = None,
    ):
        """
        Initialize cluster manager.

        Args:
            optimizer: L2 optimizer instance
            metrics_dir: Directory for metrics storage
        """
        self.optimizer = optimizer
        self._cluster_metrics: Dict[str, AntiGoodhartMetrics] = {}

        if metrics_dir is None:
            metrics_dir = Path(__file__).parent.parent / "storage" / "metrics"
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

        self._load_metrics()

    def get_cluster_signature(self, config: FullConfig) -> str:
        """
        Compute cluster signature for a configuration.

        The signature uniquely identifies the prompt cluster
        that should be used for this configuration.

        Args:
            config: Full configuration

        Returns:
            Cluster signature string
        """
        return VectorCodec.cluster_key(config)

    def list_active_clusters(self) -> List[str]:
        """List all active prompt clusters."""
        return self.optimizer.cache.list_clusters()

    def get_cluster_stats(self, cluster_key: str) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a specific cluster.

        Args:
            cluster_key: Cluster identifier

        Returns:
            Dict with cluster statistics or None if cluster not found
        """
        prompt = self.optimizer.cache.get(cluster_key)
        if prompt is None:
            return None

        metrics = self._cluster_metrics.get(cluster_key)

        return {
            "cluster_key": cluster_key,
            "compiled_at": prompt.compiled_at,
            "age_seconds": prompt.age_seconds(),
            "version": prompt.version,
            "config_vector": prompt.config_vector,
            "anti_goodhart": metrics.to_dict() if metrics else None,
        }

    def get_all_cluster_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for all active clusters."""
        stats = []
        for cluster_key in self.list_active_clusters():
            cluster_stats = self.get_cluster_stats(cluster_key)
            if cluster_stats:
                stats.append(cluster_stats)
        return stats

    def update_metrics(
        self,
        cluster_key: str,
        metrics: AntiGoodhartMetrics,
    ) -> None:
        """
        Update anti-Goodhart metrics for a cluster.

        Args:
            cluster_key: Cluster identifier
            metrics: New metrics
        """
        self._cluster_metrics[cluster_key] = metrics
        self._save_metrics()

    def compute_diversity_score(
        self,
        outputs: List[str],
    ) -> float:
        """
        Compute diversity score from a list of outputs.

        Uses Shannon entropy of n-gram distribution.

        Args:
            outputs: List of model outputs

        Returns:
            Diversity score in [0, 1]
        """
        if not outputs:
            return 0.0

        # Count unique 3-grams across all outputs
        ngram_counts: Dict[str, int] = {}
        total_ngrams = 0

        for output in outputs:
            words = output.lower().split()
            for i in range(len(words) - 2):
                ngram = " ".join(words[i:i+3])
                ngram_counts[ngram] = ngram_counts.get(ngram, 0) + 1
                total_ngrams += 1

        if total_ngrams == 0:
            return 0.0

        # Shannon entropy normalized to [0, 1]
        import math
        entropy = 0.0
        for count in ngram_counts.values():
            p = count / total_ngrams
            if p > 0:
                entropy -= p * math.log2(p)

        # Normalize by max possible entropy (log2 of unique ngrams)
        max_entropy = math.log2(len(ngram_counts)) if ngram_counts else 1.0
        return entropy / max_entropy if max_entropy > 0 else 0.0

    def compute_calibration_error(
        self,
        predictions: List[Tuple[float, bool]],
    ) -> float:
        """
        Compute calibration error from confidence/correctness pairs.

        Args:
            predictions: List of (confidence, was_correct) tuples

        Returns:
            Expected calibration error in [0, 1]
        """
        if not predictions:
            return 0.0

        # Bin predictions by confidence
        bins: Dict[int, List[Tuple[float, bool]]] = {}
        for conf, correct in predictions:
            bin_idx = int(conf * 10)  # 10 bins: [0-0.1), [0.1-0.2), ...
            bin_idx = min(9, max(0, bin_idx))
            if bin_idx not in bins:
                bins[bin_idx] = []
            bins[bin_idx].append((conf, correct))

        # Compute ECE (Expected Calibration Error)
        total_error = 0.0
        for bin_idx, bin_preds in bins.items():
            avg_conf = sum(p[0] for p in bin_preds) / len(bin_preds)
            accuracy = sum(1 for p in bin_preds if p[1]) / len(bin_preds)
            weight = len(bin_preds) / len(predictions)
            total_error += weight * abs(avg_conf - accuracy)

        return total_error

    def migrate_cluster(
        self,
        old_key: str,
        new_config: FullConfig,
    ) -> Optional[str]:
        """
        Migrate a cluster to a new configuration.

        Preserves metrics and increments version.

        Args:
            old_key: Current cluster key
            new_config: New configuration

        Returns:
            New cluster key or None if migration failed
        """
        # Get old prompt
        old_prompt = self.optimizer.cache.get(old_key)
        if old_prompt is None:
            return None

        # Compile new prompt
        new_prompt = self.optimizer.get_prompt(new_config)
        new_key = new_prompt.cluster_key

        # Copy metrics with version bump
        if old_key in self._cluster_metrics:
            old_metrics = self._cluster_metrics[old_key]
            self._cluster_metrics[new_key] = AntiGoodhartMetrics(
                diversity_score=old_metrics.diversity_score,
                coverage_breadth=old_metrics.coverage_breadth,
                calibration_error=old_metrics.calibration_error,
                regression_rate=old_metrics.regression_rate,
            )
            self._save_metrics()

        # Invalidate old cluster (optional: keep for rollback)
        # self.optimizer.cache.invalidate(old_key)

        return new_key

    def summary(self) -> Dict[str, Any]:
        """Get manager summary statistics."""
        clusters = self.list_active_clusters()
        metrics_count = len(self._cluster_metrics)

        avg_composite = 0.0
        if metrics_count > 0:
            avg_composite = sum(
                m.composite_score() for m in self._cluster_metrics.values()
            ) / metrics_count

        return {
            "total_clusters": len(clusters),
            "clusters_with_metrics": metrics_count,
            "avg_anti_goodhart_score": avg_composite,
            "optimizer_stats": self.optimizer.stats(),
        }

    def _save_metrics(self) -> None:
        """Persist metrics to disk."""
        metrics_file = self.metrics_dir / "cluster_metrics.json"
        data = {
            key: metrics.to_dict()
            for key, metrics in self._cluster_metrics.items()
        }
        with open(metrics_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_metrics(self) -> None:
        """Load metrics from disk."""
        metrics_file = self.metrics_dir / "cluster_metrics.json"
        if not metrics_file.exists():
            return

        try:
            with open(metrics_file) as f:
                data = json.load(f)
            for key, metrics_dict in data.items():
                self._cluster_metrics[key] = AntiGoodhartMetrics(
                    diversity_score=metrics_dict.get("diversity_score", 0.0),
                    coverage_breadth=metrics_dict.get("coverage_breadth", 0.0),
                    calibration_error=metrics_dict.get("calibration_error", 0.0),
                    regression_rate=metrics_dict.get("regression_rate", 0.0),
                    timestamp=metrics_dict.get("timestamp", time.time()),
                )
        except Exception:
            pass  # Skip corrupted metrics file


# Utility functions

def create_l2_optimizer(
    cache_dir: Optional[Path] = None,
    max_cache_age: float = 3600.0,
) -> DSPyLevel2Optimizer:
    """Create L2 optimizer with default settings."""
    return DSPyLevel2Optimizer(
        cache_dir=cache_dir,
        max_cache_age=max_cache_age,
    )


def create_cluster_manager(
    cache_dir: Optional[Path] = None,
    metrics_dir: Optional[Path] = None,
    max_cache_age: float = 3600.0,
) -> PromptClusterManager:
    """Create cluster manager with default settings."""
    optimizer = create_l2_optimizer(cache_dir, max_cache_age)
    return PromptClusterManager(optimizer, metrics_dir)


def get_cluster_key(config: FullConfig) -> str:
    """Get cluster key for configuration."""
    return VectorCodec.cluster_key(config)


def compute_cluster_signature(config: FullConfig) -> str:
    """
    Compute stable cluster signature for a configuration.

    This is the canonical way to get a cluster identifier.
    Alias for get_cluster_key for semantic clarity.
    """
    return VectorCodec.cluster_key(config)
