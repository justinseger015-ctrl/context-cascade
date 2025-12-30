"""
Holdout Validator for Cognitive Architecture Optimization.

Prevents overfitting by reserving 20% of evaluation tasks that are NEVER
exposed to the optimizer. Compares training vs holdout performance to
detect when optimization is fitting noise rather than signal.

This is CRITICAL for the meta-loop: without holdout validation, the
optimizer could create configurations that perform well on training
tasks but fail on new, unseen tasks.

Usage:
    from optimization.holdout_validator import HoldoutValidator, ValidationResult

    # Initialize with full task set
    validator = HoldoutValidator(all_tasks, evaluation_fn, seed=42)

    # Get training tasks for optimization (80%)
    training_tasks = validator.get_training_tasks()

    # After optimization, validate on holdout set
    result = validator.validate(pareto_configs)
    if not result.passed:
        print(f"WARNING: Overfitting detected! Gap: {result.gap:.2%}")
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict, Set, Any, Optional, Callable
import time
import json
from pathlib import Path


@dataclass
class ValidationResult:
    """Result of holdout validation."""
    passed: bool
    training_score: float
    holdout_score: float
    gap: float  # training_score - holdout_score
    overfitting_detected: bool
    reason: str

    # Detailed metrics
    training_task_count: int = 0
    holdout_task_count: int = 0
    config_count: int = 0
    validation_time: float = 0.0
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "passed": self.passed,
            "training_score": self.training_score,
            "holdout_score": self.holdout_score,
            "gap": self.gap,
            "overfitting_detected": self.overfitting_detected,
            "reason": self.reason,
            "training_task_count": self.training_task_count,
            "holdout_task_count": self.holdout_task_count,
            "config_count": self.config_count,
            "validation_time": self.validation_time,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ValidationResult":
        """Create from dictionary."""
        return cls(
            passed=data.get("passed", False),
            training_score=data.get("training_score", 0.0),
            holdout_score=data.get("holdout_score", 0.0),
            gap=data.get("gap", 0.0),
            overfitting_detected=data.get("overfitting_detected", False),
            reason=data.get("reason", ""),
            training_task_count=data.get("training_task_count", 0),
            holdout_task_count=data.get("holdout_task_count", 0),
            config_count=data.get("config_count", 0),
            validation_time=data.get("validation_time", 0.0),
            timestamp=data.get("timestamp", time.time()),
        )


@dataclass
class ValidationHistory:
    """History of validation results for trend analysis."""
    results: List[ValidationResult] = field(default_factory=list)

    def add_result(self, result: ValidationResult):
        """Add a validation result to history."""
        self.results.append(result)

    def get_trend(self, window: int = 5) -> Dict[str, float]:
        """Get trend metrics over recent validations."""
        if len(self.results) < 2:
            return {"gap_trend": 0.0, "pass_rate": 0.0}

        recent = self.results[-window:]
        gaps = [r.gap for r in recent]

        # Gap trend (positive = gap increasing = worse)
        if len(gaps) >= 2:
            gap_trend = (gaps[-1] - gaps[0]) / max(len(gaps) - 1, 1)
        else:
            gap_trend = 0.0

        # Pass rate
        pass_rate = sum(1 for r in recent if r.passed) / len(recent)

        return {
            "gap_trend": gap_trend,
            "pass_rate": pass_rate,
            "avg_gap": sum(gaps) / len(gaps),
            "min_gap": min(gaps),
            "max_gap": max(gaps),
        }

    def save(self, path: Path):
        """Save history to file."""
        data = {"results": [r.to_dict() for r in self.results]}
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "ValidationHistory":
        """Load history from file."""
        if not path.exists():
            return cls()

        with open(path) as f:
            data = json.load(f)

        history = cls()
        for r_data in data.get("results", []):
            history.results.append(ValidationResult.from_dict(r_data))

        return history


class HoldoutValidator:
    """
    Holdout validation to detect overfitting.

    Reserves 20% of evaluation tasks that are NEVER exposed to the optimizer.
    Compares training vs holdout performance to detect overfitting.

    CRITICAL: The holdout set must remain pristine. Only call validate()
    after optimization is complete, never during the optimization loop.
    """

    # Configuration
    HOLDOUT_RATIO = 0.20  # 20% holdout
    OVERFITTING_THRESHOLD = 0.20  # Flag if gap > 20%
    WARNING_THRESHOLD = 0.10  # Warn if gap > 10%

    def __init__(
        self,
        all_tasks: List[Dict[str, Any]],
        evaluation_fn: Callable,
        seed: int = 42,
        stratify_by: Optional[str] = None,
    ):
        """
        Initialize holdout validator.

        Args:
            all_tasks: Complete set of evaluation tasks
            evaluation_fn: Function(config_vector, task) -> Dict[str, float]
                          Returns dict with at least 'task_accuracy' key
            seed: Random seed for reproducible splits
            stratify_by: Optional task key to stratify split by
        """
        self.evaluation_fn = evaluation_fn
        self.seed = seed

        # Ensure tasks have IDs
        for i, task in enumerate(all_tasks):
            if "id" not in task:
                task["id"] = f"task_{i}"

        # Split into training and holdout
        if stratify_by and all(stratify_by in t for t in all_tasks):
            self.training_tasks, self.holdout_tasks = self._stratified_split(
                all_tasks, stratify_by
            )
        else:
            self.training_tasks, self.holdout_tasks = self._random_split(all_tasks)

        # Track holdout IDs for protection
        self.holdout_ids: Set[str] = {t["id"] for t in self.holdout_tasks}

        # Validation history
        self.history = ValidationHistory()

        # Guard: track if holdout has been accessed
        self._holdout_accessed = False

    def _random_split(
        self, tasks: List[Dict]
    ) -> tuple[List[Dict], List[Dict]]:
        """Random 80/20 split."""
        random.seed(self.seed)
        shuffled = list(tasks)
        random.shuffle(shuffled)

        split_idx = int(len(shuffled) * (1 - self.HOLDOUT_RATIO))
        return shuffled[:split_idx], shuffled[split_idx:]

    def _stratified_split(
        self, tasks: List[Dict], stratify_key: str
    ) -> tuple[List[Dict], List[Dict]]:
        """Stratified split maintaining class distribution."""
        random.seed(self.seed)

        # Group by stratify key
        groups: Dict[str, List[Dict]] = {}
        for task in tasks:
            key = str(task.get(stratify_key, "unknown"))
            if key not in groups:
                groups[key] = []
            groups[key].append(task)

        # Split each group
        training = []
        holdout = []

        for group_tasks in groups.values():
            random.shuffle(group_tasks)
            split_idx = int(len(group_tasks) * (1 - self.HOLDOUT_RATIO))
            training.extend(group_tasks[:split_idx])
            holdout.extend(group_tasks[split_idx:])

        # Final shuffle
        random.shuffle(training)
        random.shuffle(holdout)

        return training, holdout

    def is_holdout(self, task_id: str) -> bool:
        """Check if a task is in the holdout set."""
        return task_id in self.holdout_ids

    def get_training_tasks(self) -> List[Dict]:
        """Get training tasks (safe to use for optimization)."""
        return self.training_tasks

    def get_task_counts(self) -> Dict[str, int]:
        """Get task counts for training and holdout sets."""
        return {
            "total": len(self.training_tasks) + len(self.holdout_tasks),
            "training": len(self.training_tasks),
            "holdout": len(self.holdout_tasks),
        }

    def validate(
        self,
        configs: List[Any],  # List of ParetoPoint or config vectors
        metric_key: str = "task_accuracy",
    ) -> ValidationResult:
        """
        Validate configurations against holdout tasks.

        CRITICAL: This is the ONLY place holdout tasks are evaluated.
        Call only AFTER optimization is complete.

        Args:
            configs: List of configurations to validate (ParetoPoint or vectors)
            metric_key: Which metric to use for comparison

        Returns:
            ValidationResult with pass/fail and detailed metrics
        """
        start_time = time.time()
        self._holdout_accessed = True

        if not configs:
            return ValidationResult(
                passed=False,
                training_score=0.0,
                holdout_score=0.0,
                gap=0.0,
                overfitting_detected=False,
                reason="No configs to validate",
                config_count=0,
            )

        # Extract config vectors
        config_vectors = []
        for config in configs:
            if hasattr(config, "config_vector"):
                config_vectors.append(config.config_vector)
            elif isinstance(config, (list, tuple)):
                config_vectors.append(list(config))
            else:
                # Assume it's a config object with encode method
                try:
                    from core.config import VectorCodec
                    config_vectors.append(VectorCodec.encode(config))
                except Exception:
                    continue

        if not config_vectors:
            return ValidationResult(
                passed=False,
                training_score=0.0,
                holdout_score=0.0,
                gap=0.0,
                overfitting_detected=False,
                reason="No valid config vectors extracted",
                config_count=0,
            )

        # Evaluate on training tasks
        training_scores = []
        for config_vec in config_vectors:
            for task in self.training_tasks:
                try:
                    outcome = self.evaluation_fn(config_vec, task)
                    score = outcome.get(metric_key, 0.0)
                    training_scores.append(score)
                except Exception as e:
                    # Skip failed evaluations
                    continue

        training_avg = (
            sum(training_scores) / len(training_scores)
            if training_scores else 0.0
        )

        # Evaluate on holdout tasks
        holdout_scores = []
        for config_vec in config_vectors:
            for task in self.holdout_tasks:
                try:
                    outcome = self.evaluation_fn(config_vec, task)
                    score = outcome.get(metric_key, 0.0)
                    holdout_scores.append(score)
                except Exception as e:
                    # Skip failed evaluations
                    continue

        holdout_avg = (
            sum(holdout_scores) / len(holdout_scores)
            if holdout_scores else 0.0
        )

        # Compute gap
        gap = training_avg - holdout_avg

        # Check for overfitting
        overfitting = gap > self.OVERFITTING_THRESHOLD
        warning = gap > self.WARNING_THRESHOLD

        # Build reason string
        if overfitting:
            reason = f"OVERFITTING: Gap {gap:.2%} exceeds threshold {self.OVERFITTING_THRESHOLD:.2%}"
        elif warning:
            reason = f"WARNING: Gap {gap:.2%} exceeds warning threshold {self.WARNING_THRESHOLD:.2%}"
        elif gap < 0:
            reason = f"EXCELLENT: Holdout outperforms training by {-gap:.2%}"
        else:
            reason = f"PASSED: Gap {gap:.2%} within acceptable bounds"

        validation_time = time.time() - start_time

        result = ValidationResult(
            passed=not overfitting,
            training_score=training_avg,
            holdout_score=holdout_avg,
            gap=gap,
            overfitting_detected=overfitting,
            reason=reason,
            training_task_count=len(self.training_tasks),
            holdout_task_count=len(self.holdout_tasks),
            config_count=len(config_vectors),
            validation_time=validation_time,
        )

        # Add to history
        self.history.add_result(result)

        return result

    def get_validation_trend(self, window: int = 5) -> Dict[str, float]:
        """Get trend in validation results."""
        return self.history.get_trend(window)

    def save_history(self, path: Path):
        """Save validation history."""
        self.history.save(path)

    def load_history(self, path: Path):
        """Load validation history."""
        self.history = ValidationHistory.load(path)


def create_holdout_validator(
    task_source: str = "synthetic",
    task_count: int = 100,
    seed: int = 42,
) -> HoldoutValidator:
    """
    Factory function to create holdout validator.

    Args:
        task_source: "synthetic" for generated tasks, or path to task file
        task_count: Number of synthetic tasks to generate
        seed: Random seed

    Returns:
        Configured HoldoutValidator
    """
    if task_source == "synthetic":
        # Generate synthetic tasks
        tasks = _generate_synthetic_tasks(task_count, seed)
        eval_fn = _create_synthetic_evaluator()
    else:
        # Load from file
        with open(task_source) as f:
            tasks = json.load(f)
        eval_fn = _create_synthetic_evaluator()  # Still use synthetic for now

    return HoldoutValidator(tasks, eval_fn, seed)


def _generate_synthetic_tasks(count: int, seed: int) -> List[Dict[str, Any]]:
    """Generate synthetic evaluation tasks."""
    random.seed(seed)

    task_types = ["coding", "analysis", "writing", "math", "research"]
    difficulty_levels = ["easy", "medium", "hard"]
    domains = ["general", "technical", "creative", "scientific"]

    tasks = []
    for i in range(count):
        task = {
            "id": f"task_{i:04d}",
            "type": random.choice(task_types),
            "difficulty": random.choice(difficulty_levels),
            "domain": random.choice(domains),
            "content": f"Synthetic task {i}",
            "expected_frames": random.sample(
                ["evidential", "aspectual", "morphological", "compositional"],
                k=random.randint(1, 3)
            ),
        }
        tasks.append(task)

    return tasks


def _create_synthetic_evaluator() -> Callable:
    """Create synthetic evaluation function for testing."""

    def evaluate(config_vector: List[float], task: Dict) -> Dict[str, float]:
        """Synthetic evaluation based on config-task matching."""
        # Simple heuristic: higher frame activation = better accuracy
        # but only if task expects those frames

        expected_frames = task.get("expected_frames", [])
        frame_indices = {
            "evidential": 0,
            "aspectual": 1,
            "morphological": 2,
            "compositional": 3,
        }

        # Base score
        score = 0.5

        # Bonus for matching frames
        for frame in expected_frames:
            if frame in frame_indices:
                idx = frame_indices[frame]
                if idx < len(config_vector):
                    score += 0.1 * config_vector[idx]

        # Difficulty penalty
        difficulty = task.get("difficulty", "medium")
        if difficulty == "hard":
            score *= 0.8
        elif difficulty == "easy":
            score *= 1.1

        # Add some noise
        noise = random.gauss(0, 0.05)
        score = max(0, min(1, score + noise))

        return {
            "task_accuracy": score,
            "token_efficiency": 0.8 - 0.1 * sum(config_vector[:4]),
            "edge_robustness": score * 0.9,
            "epistemic_consistency": score * 0.95,
        }

    return evaluate


# Integration with TwoStageOptimizer
def integrate_with_optimizer(
    optimizer: Any,
    validator: HoldoutValidator,
) -> None:
    """
    Integrate holdout validator with TwoStageOptimizer.

    Sets up the validator to automatically validate after optimization.
    """
    optimizer.holdout = validator


if __name__ == "__main__":
    # Demo usage
    print("Holdout Validator Demo")
    print("=" * 50)

    # Create validator with synthetic tasks
    validator = create_holdout_validator(
        task_source="synthetic",
        task_count=100,
        seed=42,
    )

    counts = validator.get_task_counts()
    print(f"Task split: {counts['training']} training, {counts['holdout']} holdout")

    # Simulate some configs
    test_configs = [
        [1.0, 1.0, 0.5, 0.3, 0.0, 0.0, 0.0, 0.8, 0.7, 1.0, 0.8, 0.5, 0.5, 0.5],
        [0.8, 0.8, 0.3, 0.3, 0.5, 0.5, 0.0, 0.6, 0.5, 0.8, 0.7, 0.6, 0.4, 0.4],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    ]

    # Validate
    result = validator.validate(test_configs)

    print(f"\nValidation Result:")
    print(f"  Passed: {result.passed}")
    print(f"  Training Score: {result.training_score:.3f}")
    print(f"  Holdout Score: {result.holdout_score:.3f}")
    print(f"  Gap: {result.gap:.2%}")
    print(f"  Reason: {result.reason}")
    print(f"  Validation Time: {result.validation_time:.3f}s")
