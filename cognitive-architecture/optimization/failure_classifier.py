"""
Failure Classifier for DSPy Level 1.

Classifies failures from evaluation outcomes into 12 types across 4 categories:
- EPISTEMIC (4): overconfidence, underconfidence, grounding_failure, inconsistency
- STRUCTURAL (3): frame_ignored, verix_violation, focus_drift
- PERFORMANCE (3): verbosity, terseness, latency
- DOMAIN (2): math_error, factual_error

Part of the DSPy Level 1 monthly structural evolution system.
"""

import time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict


class FailureCategory(Enum):
    """Top-level failure categories."""
    EPISTEMIC = "epistemic"       # Confidence/evidence issues
    STRUCTURAL = "structural"     # VCL/VERIX format issues
    PERFORMANCE = "performance"   # Efficiency issues
    DOMAIN = "domain"             # Factual/calculation errors


class FailureType(Enum):
    """Specific failure types (12 total)."""

    # EPISTEMIC (4 types) - Confidence/evidence issues
    OVERCONFIDENCE = "overconfidence"         # Stated confidence > actual accuracy
    UNDERCONFIDENCE = "underconfidence"       # Stated confidence < actual accuracy
    GROUNDING_FAILURE = "grounding_failure"   # Claims without evidence
    INCONSISTENCY = "inconsistency"           # Self-contradicting statements

    # STRUCTURAL (3 types) - VCL/VERIX issues
    FRAME_IGNORED = "frame_ignored"           # Required frame not activated
    VERIX_VIOLATION = "verix_violation"       # VERIX format error
    FOCUS_DRIFT = "focus_drift"               # Wandered from task

    # PERFORMANCE (3 types) - Efficiency issues
    VERBOSITY = "verbosity"                   # Excessive tokens
    TERSENESS = "terseness"                   # Insufficient detail
    LATENCY = "latency"                       # Too slow (timeout risk)

    # DOMAIN (2 types) - Factual errors
    MATH_ERROR = "math_error"                 # Calculation mistake
    FACTUAL_ERROR = "factual_error"           # Wrong fact stated


# Map failure types to their categories
FAILURE_CATEGORY_MAP: Dict[FailureType, FailureCategory] = {
    # Epistemic
    FailureType.OVERCONFIDENCE: FailureCategory.EPISTEMIC,
    FailureType.UNDERCONFIDENCE: FailureCategory.EPISTEMIC,
    FailureType.GROUNDING_FAILURE: FailureCategory.EPISTEMIC,
    FailureType.INCONSISTENCY: FailureCategory.EPISTEMIC,
    # Structural
    FailureType.FRAME_IGNORED: FailureCategory.STRUCTURAL,
    FailureType.VERIX_VIOLATION: FailureCategory.STRUCTURAL,
    FailureType.FOCUS_DRIFT: FailureCategory.STRUCTURAL,
    # Performance
    FailureType.VERBOSITY: FailureCategory.PERFORMANCE,
    FailureType.TERSENESS: FailureCategory.PERFORMANCE,
    FailureType.LATENCY: FailureCategory.PERFORMANCE,
    # Domain
    FailureType.MATH_ERROR: FailureCategory.DOMAIN,
    FailureType.FACTUAL_ERROR: FailureCategory.DOMAIN,
}


@dataclass
class FailureInstance:
    """A classified failure instance."""
    failure_type: FailureType
    category: FailureCategory
    severity: float                    # 0.0 = minor, 1.0 = critical
    config_vector: List[float]
    task_type: str
    description: str
    evidence: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "failure_type": self.failure_type.value,
            "category": self.category.value,
            "severity": self.severity,
            "config_vector": self.config_vector,
            "task_type": self.task_type,
            "description": self.description,
            "evidence": self.evidence,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FailureInstance":
        """Deserialize from dictionary."""
        return cls(
            failure_type=FailureType(data["failure_type"]),
            category=FailureCategory(data["category"]),
            severity=data["severity"],
            config_vector=data["config_vector"],
            task_type=data["task_type"],
            description=data["description"],
            evidence=data["evidence"],
            timestamp=data.get("timestamp", time.time()),
        )


@dataclass
class FailurePattern:
    """A pattern of correlated failures."""
    failure_types: List[FailureType]
    correlation: float                  # How strongly correlated
    config_signature: str               # Which config dimensions correlate
    frequency: float                    # How often this pattern occurs
    remediation: str                    # Suggested fix

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "failure_types": [ft.value for ft in self.failure_types],
            "correlation": self.correlation,
            "config_signature": self.config_signature,
            "frequency": self.frequency,
            "remediation": self.remediation,
        }


class FailureClassifier:
    """
    Classifies failures from evaluation outcomes.

    Uses heuristics to detect failure types from:
    - Outcome metrics (accuracy, confidence, etc.)
    - Output analysis (length, structure, etc.)
    - Config vector correlation
    """

    # Detection thresholds
    OVERCONFIDENCE_THRESHOLD = 0.15     # |stated_conf - actual_acc| > 0.15
    UNDERCONFIDENCE_THRESHOLD = 0.15    # Same threshold for under
    GROUNDING_THRESHOLD = 0.5           # grounding_score < 0.5
    CONSISTENCY_THRESHOLD = 0.7         # consistency < 0.7
    VERIX_THRESHOLD = 0.8               # verix_valid < 0.8
    RELEVANCE_THRESHOLD = 0.7           # task_relevance < 0.7
    VERBOSITY_RATIO = 2.0               # tokens > 2x expected
    TERSENESS_RATIO = 0.3               # tokens < 0.3x expected
    LATENCY_WARNING_RATIO = 0.8         # latency > 0.8 * limit
    MATH_ACCURACY_THRESHOLD = 0.9       # math_accuracy < 0.9
    FACTUAL_ACCURACY_THRESHOLD = 0.9    # factual_accuracy < 0.9

    def __init__(self):
        """Initialize classifier."""
        self._failures: List[FailureInstance] = []
        self._patterns: List[FailurePattern] = []

    def classify_outcome(
        self,
        config_vector: List[float],
        outcomes: Dict[str, float],
        output_metadata: Dict[str, Any],
        task_type: str,
    ) -> List[FailureInstance]:
        """
        Classify failures in a single evaluation outcome.

        Args:
            config_vector: The configuration used
            outcomes: Measured outcomes (accuracy, efficiency, etc.)
            output_metadata: Additional info (token_count, confidence_stated, etc.)
            task_type: Type of task evaluated

        Returns:
            List of detected failures
        """
        failures = []

        # Check EPISTEMIC failures
        failures.extend(self._check_epistemic(
            config_vector, outcomes, output_metadata, task_type
        ))

        # Check STRUCTURAL failures
        failures.extend(self._check_structural(
            config_vector, outcomes, output_metadata, task_type
        ))

        # Check PERFORMANCE failures
        failures.extend(self._check_performance(
            config_vector, outcomes, output_metadata, task_type
        ))

        # Check DOMAIN failures
        failures.extend(self._check_domain(
            config_vector, outcomes, output_metadata, task_type
        ))

        self._failures.extend(failures)
        return failures

    def _check_epistemic(
        self,
        config: List[float],
        outcomes: Dict[str, float],
        metadata: Dict[str, Any],
        task: str,
    ) -> List[FailureInstance]:
        """Check for epistemic failures."""
        failures = []

        # Get relevant metrics
        stated_conf = metadata.get("confidence_stated", 0.5)
        actual_acc = outcomes.get("task_accuracy", 0.5)
        grounding_score = outcomes.get("grounding_score", 1.0)
        consistency = outcomes.get("epistemic_consistency", 1.0)

        # Overconfidence: stated confidence exceeds actual accuracy
        conf_gap = stated_conf - actual_acc
        if conf_gap > self.OVERCONFIDENCE_THRESHOLD:
            severity = min(1.0, conf_gap / 0.5)  # Normalize to [0, 1]
            failures.append(FailureInstance(
                failure_type=FailureType.OVERCONFIDENCE,
                category=FailureCategory.EPISTEMIC,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Stated {stated_conf:.2f} confidence but achieved {actual_acc:.2f} accuracy",
                evidence={
                    "stated_confidence": stated_conf,
                    "actual_accuracy": actual_acc,
                    "gap": conf_gap,
                },
            ))

        # Underconfidence: actual accuracy exceeds stated confidence
        under_gap = actual_acc - stated_conf
        if under_gap > self.UNDERCONFIDENCE_THRESHOLD:
            severity = min(1.0, under_gap / 0.5)
            failures.append(FailureInstance(
                failure_type=FailureType.UNDERCONFIDENCE,
                category=FailureCategory.EPISTEMIC,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Stated {stated_conf:.2f} confidence but achieved {actual_acc:.2f} accuracy",
                evidence={
                    "stated_confidence": stated_conf,
                    "actual_accuracy": actual_acc,
                    "gap": under_gap,
                },
            ))

        # Grounding failure: claims without evidence
        if grounding_score < self.GROUNDING_THRESHOLD:
            severity = 1.0 - grounding_score
            failures.append(FailureInstance(
                failure_type=FailureType.GROUNDING_FAILURE,
                category=FailureCategory.EPISTEMIC,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Low grounding score: {grounding_score:.2f}",
                evidence={"grounding_score": grounding_score},
            ))

        # Inconsistency: self-contradicting statements
        if consistency < self.CONSISTENCY_THRESHOLD:
            severity = 1.0 - consistency
            failures.append(FailureInstance(
                failure_type=FailureType.INCONSISTENCY,
                category=FailureCategory.EPISTEMIC,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Inconsistent statements detected: {consistency:.2f} consistency score",
                evidence={"consistency_score": consistency},
            ))

        return failures

    def _check_structural(
        self,
        config: List[float],
        outcomes: Dict[str, float],
        metadata: Dict[str, Any],
        task: str,
    ) -> List[FailureInstance]:
        """Check for structural VCL/VERIX failures."""
        failures = []

        # Frame ignored: required frame not activated
        frames_expected = set(metadata.get("frames_expected", []))
        frames_used = set(metadata.get("frames_used", []))
        ignored_frames = frames_expected - frames_used

        if ignored_frames:
            severity = len(ignored_frames) / max(1, len(frames_expected))
            failures.append(FailureInstance(
                failure_type=FailureType.FRAME_IGNORED,
                category=FailureCategory.STRUCTURAL,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Required frames not activated: {', '.join(ignored_frames)}",
                evidence={
                    "frames_expected": list(frames_expected),
                    "frames_used": list(frames_used),
                    "frames_ignored": list(ignored_frames),
                },
            ))

        # VERIX violation: format errors
        verix_valid = outcomes.get("verix_format_valid", 1.0)
        if verix_valid < self.VERIX_THRESHOLD:
            severity = 1.0 - verix_valid
            failures.append(FailureInstance(
                failure_type=FailureType.VERIX_VIOLATION,
                category=FailureCategory.STRUCTURAL,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"VERIX format errors: {(1-verix_valid)*100:.0f}% invalid",
                evidence={"verix_format_valid": verix_valid},
            ))

        # Focus drift: output wandered from task
        relevance = outcomes.get("task_relevance", 1.0)
        if relevance < self.RELEVANCE_THRESHOLD:
            severity = 1.0 - relevance
            failures.append(FailureInstance(
                failure_type=FailureType.FOCUS_DRIFT,
                category=FailureCategory.STRUCTURAL,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Output drifted from task: {relevance:.2f} relevance score",
                evidence={"task_relevance": relevance},
            ))

        return failures

    def _check_performance(
        self,
        config: List[float],
        outcomes: Dict[str, float],
        metadata: Dict[str, Any],
        task: str,
    ) -> List[FailureInstance]:
        """Check for performance failures."""
        failures = []

        token_count = metadata.get("token_count", 0)
        expected_tokens = metadata.get("expected_tokens", 500)
        latency_ms = metadata.get("latency_ms", 0)
        latency_limit_ms = metadata.get("latency_limit_ms", 30000)

        # Verbosity: excessive tokens
        if expected_tokens > 0 and token_count > expected_tokens * self.VERBOSITY_RATIO:
            ratio = token_count / expected_tokens
            severity = min(1.0, (ratio - 1) / 3)  # Normalize: 2x -> 0.33, 4x -> 1.0
            failures.append(FailureInstance(
                failure_type=FailureType.VERBOSITY,
                category=FailureCategory.PERFORMANCE,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Excessive tokens: {token_count} (expected ~{expected_tokens})",
                evidence={
                    "token_count": token_count,
                    "expected_tokens": expected_tokens,
                    "ratio": ratio,
                },
            ))

        # Terseness: insufficient detail
        if expected_tokens > 0 and token_count < expected_tokens * self.TERSENESS_RATIO:
            ratio = token_count / expected_tokens if expected_tokens > 0 else 0
            severity = min(1.0, 1 - ratio / self.TERSENESS_RATIO)
            failures.append(FailureInstance(
                failure_type=FailureType.TERSENESS,
                category=FailureCategory.PERFORMANCE,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Too brief: {token_count} tokens (expected ~{expected_tokens})",
                evidence={
                    "token_count": token_count,
                    "expected_tokens": expected_tokens,
                    "ratio": ratio,
                },
            ))

        # Latency: near timeout
        if latency_limit_ms > 0 and latency_ms > latency_limit_ms * self.LATENCY_WARNING_RATIO:
            severity = min(1.0, latency_ms / latency_limit_ms)
            failures.append(FailureInstance(
                failure_type=FailureType.LATENCY,
                category=FailureCategory.PERFORMANCE,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Near timeout: {latency_ms}ms (limit {latency_limit_ms}ms)",
                evidence={
                    "latency_ms": latency_ms,
                    "latency_limit_ms": latency_limit_ms,
                    "utilization": latency_ms / latency_limit_ms,
                },
            ))

        return failures

    def _check_domain(
        self,
        config: List[float],
        outcomes: Dict[str, float],
        metadata: Dict[str, Any],
        task: str,
    ) -> List[FailureInstance]:
        """Check for domain-specific failures."""
        failures = []

        # Math error (only if task involves math)
        math_accuracy = outcomes.get("math_accuracy")
        if math_accuracy is not None and math_accuracy < self.MATH_ACCURACY_THRESHOLD:
            severity = 1.0 - math_accuracy
            failures.append(FailureInstance(
                failure_type=FailureType.MATH_ERROR,
                category=FailureCategory.DOMAIN,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Math errors detected: {(1-math_accuracy)*100:.0f}% incorrect",
                evidence={"math_accuracy": math_accuracy},
            ))

        # Factual error (only if task involves facts)
        factual_accuracy = outcomes.get("factual_accuracy")
        if factual_accuracy is not None and factual_accuracy < self.FACTUAL_ACCURACY_THRESHOLD:
            severity = 1.0 - factual_accuracy
            failures.append(FailureInstance(
                failure_type=FailureType.FACTUAL_ERROR,
                category=FailureCategory.DOMAIN,
                severity=severity,
                config_vector=config,
                task_type=task,
                description=f"Factual errors detected: {(1-factual_accuracy)*100:.0f}% incorrect",
                evidence={"factual_accuracy": factual_accuracy},
            ))

        return failures

    def find_patterns(self, min_correlation: float = 0.3) -> List[FailurePattern]:
        """
        Find correlated failure patterns.

        Identifies which failure types tend to occur together
        and correlates with specific config dimensions.

        Args:
            min_correlation: Minimum correlation to report

        Returns:
            List of detected patterns
        """
        if len(self._failures) < 10:
            return []

        patterns = []

        # Group failures by task
        by_task: Dict[str, List[FailureInstance]] = defaultdict(list)
        for f in self._failures:
            task_key = f"{f.task_type}_{int(f.timestamp)}"
            by_task[task_key].append(f)

        # Find co-occurring failure types
        cooccurrence: Dict[tuple, int] = defaultdict(int)
        total_tasks = len(by_task)

        for task_failures in by_task.values():
            types = set(f.failure_type for f in task_failures)
            for t1 in types:
                for t2 in types:
                    if t1.value < t2.value:  # Avoid duplicates
                        cooccurrence[(t1, t2)] += 1

        # Convert to patterns
        for (t1, t2), count in cooccurrence.items():
            frequency = count / total_tasks
            if frequency >= min_correlation:
                patterns.append(FailurePattern(
                    failure_types=[t1, t2],
                    correlation=frequency,
                    config_signature=self._infer_config_signature([t1, t2]),
                    frequency=frequency,
                    remediation=self._suggest_remediation([t1, t2]),
                ))

        self._patterns = sorted(patterns, key=lambda p: -p.correlation)
        return self._patterns

    def _infer_config_signature(self, failure_types: List[FailureType]) -> str:
        """Infer which config dimensions correlate with failures."""
        # Simplified: map failure categories to likely config dimensions
        signatures = []
        categories = set(FAILURE_CATEGORY_MAP[ft] for ft in failure_types)

        if FailureCategory.EPISTEMIC in categories:
            signatures.append("verix_strictness")
        if FailureCategory.STRUCTURAL in categories:
            signatures.append("frame_activation")
        if FailureCategory.PERFORMANCE in categories:
            signatures.append("compression_level")

        return ",".join(signatures) if signatures else "unknown"

    def _suggest_remediation(self, failure_types: List[FailureType]) -> str:
        """Suggest remediation for failure pattern."""
        remediations = {
            FailureType.OVERCONFIDENCE: "Increase VERIX strictness or add confidence calibration",
            FailureType.UNDERCONFIDENCE: "Review confidence scoring thresholds",
            FailureType.GROUNDING_FAILURE: "Enforce evidential frame activation",
            FailureType.INCONSISTENCY: "Add self-consistency checking",
            FailureType.FRAME_IGNORED: "Review frame activation routing",
            FailureType.VERIX_VIOLATION: "Add VERIX format validation",
            FailureType.FOCUS_DRIFT: "Add task relevance monitoring",
            FailureType.VERBOSITY: "Increase compression level",
            FailureType.TERSENESS: "Decrease compression level",
            FailureType.LATENCY: "Optimize prompt or reduce frame count",
            FailureType.MATH_ERROR: "Enable math verification frame",
            FailureType.FACTUAL_ERROR: "Enable grounding frame with fact-checking",
        }

        suggestions = [remediations.get(ft, "Unknown") for ft in failure_types]
        return " | ".join(set(suggestions))

    def get_failures(
        self,
        category: Optional[FailureCategory] = None,
        failure_type: Optional[FailureType] = None,
        min_severity: float = 0.0,
    ) -> List[FailureInstance]:
        """
        Get failures with optional filtering.

        Args:
            category: Filter by category
            failure_type: Filter by specific type
            min_severity: Minimum severity threshold
        """
        failures = self._failures

        if category is not None:
            failures = [f for f in failures if f.category == category]

        if failure_type is not None:
            failures = [f for f in failures if f.failure_type == failure_type]

        if min_severity > 0:
            failures = [f for f in failures if f.severity >= min_severity]

        return failures

    def get_summary(self) -> Dict[str, Any]:
        """Get failure summary statistics."""
        by_type: Dict[str, int] = defaultdict(int)
        by_category: Dict[str, int] = defaultdict(int)
        severity_sum = 0.0

        for f in self._failures:
            by_type[f.failure_type.value] += 1
            by_category[f.category.value] += 1
            severity_sum += f.severity

        return {
            "total_failures": len(self._failures),
            "by_type": dict(by_type),
            "by_category": dict(by_category),
            "avg_severity": severity_sum / max(1, len(self._failures)),
            "patterns_found": len(self._patterns),
        }

    def clear(self) -> None:
        """Clear all recorded failures and patterns."""
        self._failures = []
        self._patterns = []


# Factory function
def create_failure_classifier() -> FailureClassifier:
    """Create a new FailureClassifier instance."""
    return FailureClassifier()
