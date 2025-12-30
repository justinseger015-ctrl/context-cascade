"""
Core evaluation metrics for cognitive architecture.

Metrics:
- task_accuracy: Correctness of task completion
- token_efficiency: Cost per task (tokens used)
- edge_robustness: Performance on adversarial inputs
- epistemic_consistency: VERIX claim coherence

Anti-Gaming:
- Length normalization
- Format compliance as sub-metric
- Holdout regression set (never optimized on)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Tuple
from enum import Enum
import math
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.verix import VerixClaim, VerixParser, VerixValidator
from core.config import FullConfig, PromptConfig


class MetricType(Enum):
    """Types of evaluation metrics."""
    TASK_ACCURACY = "task_accuracy"
    TOKEN_EFFICIENCY = "token_efficiency"
    EDGE_ROBUSTNESS = "edge_robustness"
    EPISTEMIC_CONSISTENCY = "epistemic_consistency"


@dataclass
class EvaluationResult:
    """Result of evaluating a single task."""

    task_id: str
    task_accuracy: float  # 0.0 - 1.0
    token_efficiency: float  # 0.0 - 1.0 (normalized)
    edge_robustness: float  # 0.0 - 1.0
    epistemic_consistency: float  # 0.0 - 1.0
    raw_metrics: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate all metrics are in valid range."""
        for name in ["task_accuracy", "token_efficiency", "edge_robustness", "epistemic_consistency"]:
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0.0, 1.0], got {value}")

    @property
    def composite_score(self) -> float:
        """
        Weighted composite score.

        Weights:
        - task_accuracy: 0.4 (most important)
        - token_efficiency: 0.2
        - edge_robustness: 0.2
        - epistemic_consistency: 0.2
        """
        return (
            0.4 * self.task_accuracy +
            0.2 * self.token_efficiency +
            0.2 * self.edge_robustness +
            0.2 * self.epistemic_consistency
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "task_accuracy": self.task_accuracy,
            "token_efficiency": self.token_efficiency,
            "edge_robustness": self.edge_robustness,
            "epistemic_consistency": self.epistemic_consistency,
            "composite_score": self.composite_score,
            "raw_metrics": self.raw_metrics,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvaluationResult":
        """Create from dictionary."""
        return cls(
            task_id=data["task_id"],
            task_accuracy=data["task_accuracy"],
            token_efficiency=data["token_efficiency"],
            edge_robustness=data["edge_robustness"],
            epistemic_consistency=data["epistemic_consistency"],
            raw_metrics=data.get("raw_metrics", {}),
        )


class MetricCalculator:
    """Calculate all metrics for a response."""

    # Default baselines
    DEFAULT_TOKEN_BASELINE = 500
    DEFAULT_LENGTH_TARGET = 1000

    def __init__(
        self,
        config: Optional[FullConfig] = None,
        token_baseline: int = DEFAULT_TOKEN_BASELINE,
        length_target: int = DEFAULT_LENGTH_TARGET,
    ):
        """
        Initialize metric calculator.

        Args:
            config: Full configuration for VERIX validation
            token_baseline: Expected token count for efficiency calculation
            length_target: Target response length for normalization
        """
        self.config = config or FullConfig()
        self.token_baseline = token_baseline
        self.length_target = length_target
        self.verix_parser = VerixParser()
        self.verix_validator = VerixValidator(self.config.prompt)

    def calculate(
        self,
        task: Dict[str, Any],
        response: str,
        expected: Any,
        token_count: int,
        edge_type: Optional[str] = None,
    ) -> EvaluationResult:
        """
        Calculate all metrics for a single task.

        Args:
            task: Task definition with id, type, description
            response: Model's response text
            expected: Expected output or acceptance criteria
            token_count: Number of tokens in response
            edge_type: Type of edge case if applicable

        Returns:
            EvaluationResult with all metrics
        """
        task_id = task.get("id", "unknown")
        task_type = task.get("task_type", "default")

        # Calculate each metric
        accuracy = self.task_accuracy(response, expected, task_type)
        efficiency = self.token_efficiency(token_count, self.token_baseline)
        robustness = self.edge_robustness(response, edge_type) if edge_type else 1.0

        # Parse VERIX claims for consistency check
        claims = self.verix_parser.parse(response)
        consistency = self.epistemic_consistency(claims)

        # Apply anti-gaming penalties
        length_penalty = length_normalize(accuracy, len(response), self.length_target)
        format_penalty = format_compliance_penalty(response, task_type)

        # Adjusted accuracy with penalties
        adjusted_accuracy = accuracy * length_penalty * format_penalty

        return EvaluationResult(
            task_id=task_id,
            task_accuracy=min(1.0, max(0.0, adjusted_accuracy)),
            token_efficiency=efficiency,
            edge_robustness=robustness,
            epistemic_consistency=consistency,
            raw_metrics={
                "raw_accuracy": accuracy,
                "length_penalty": length_penalty,
                "format_penalty": format_penalty,
                "token_count": token_count,
                "claim_count": len(claims),
                "response_length": len(response),
            },
        )

    def task_accuracy(
        self,
        response: str,
        expected: Any,
        task_type: str,
    ) -> float:
        """
        Measure task completion accuracy.

        Uses deterministic checks where possible, returns estimate for subjective tasks.

        Args:
            response: Model's response text
            expected: Expected output or criteria
            task_type: Type of task (reasoning, coding, analysis, etc.)

        Returns:
            Accuracy score 0.0 - 1.0
        """
        if expected is None:
            # No expected output - use format heuristics
            return self._heuristic_accuracy(response, task_type)

        if isinstance(expected, str):
            # String matching (case-insensitive)
            if expected.lower() in response.lower():
                return 1.0
            # Partial match
            words_expected = set(expected.lower().split())
            words_response = set(response.lower().split())
            overlap = len(words_expected & words_response)
            return overlap / len(words_expected) if words_expected else 0.0

        if isinstance(expected, list):
            # Check each expected item
            found = sum(1 for item in expected if str(item).lower() in response.lower())
            return found / len(expected) if expected else 0.0

        if isinstance(expected, dict):
            # Check key-value pairs
            found = 0
            total = 0
            for key, value in expected.items():
                total += 1
                if str(key).lower() in response.lower():
                    if str(value).lower() in response.lower():
                        found += 1
                    else:
                        found += 0.5  # Key present but not value
            return found / total if total else 0.0

        return 0.0

    def _heuristic_accuracy(self, response: str, task_type: str) -> float:
        """Heuristic accuracy based on response quality signals."""
        score = 0.5  # Base score

        # Length check - not too short
        if len(response) > 100:
            score += 0.1
        if len(response) > 500:
            score += 0.1

        # Structure check
        if any(marker in response for marker in ["1.", "2.", "- ", "* "]):
            score += 0.1

        # Code task specifics
        if task_type == "coding":
            if "```" in response or "def " in response or "function " in response:
                score += 0.1

        # Reasoning task specifics
        if task_type == "reasoning":
            reasoning_markers = ["therefore", "because", "since", "thus", "hence"]
            if any(marker in response.lower() for marker in reasoning_markers):
                score += 0.1

        return min(1.0, score)

    def token_efficiency(self, token_count: int, baseline: int) -> float:
        """
        Measure token usage efficiency.

        Returns normalized score where 1.0 = at or below baseline,
        and score decreases as tokens exceed baseline.

        Args:
            token_count: Actual tokens used
            baseline: Expected baseline token count

        Returns:
            Efficiency score 0.0 - 1.0
        """
        if token_count <= 0:
            return 0.0
        if token_count <= baseline:
            return 1.0

        # Exponential decay for over-baseline
        excess_ratio = (token_count - baseline) / baseline
        return max(0.0, math.exp(-0.5 * excess_ratio))

    def edge_robustness(self, response: str, edge_type: Optional[str]) -> float:
        """
        Measure robustness to edge cases.

        Edge types:
        - ambiguous: Unclear or underspecified input
        - adversarial: Intentionally misleading input
        - out_of_distribution: Unusual or rare input
        - contradictory: Self-contradicting input

        Args:
            response: Model's response
            edge_type: Type of edge case

        Returns:
            Robustness score 0.0 - 1.0
        """
        if not edge_type:
            return 1.0

        # Check for appropriate handling
        score = 0.5  # Base score for any response

        # Check for acknowledgment of difficulty
        difficulty_markers = [
            "unclear", "ambiguous", "uncertain", "assumption",
            "interpret", "clarification", "context", "depends"
        ]
        if any(marker in response.lower() for marker in difficulty_markers):
            score += 0.2

        # Check for hedging (appropriate for edge cases)
        hedge_markers = [
            "may", "might", "could", "possibly", "potentially",
            "likely", "probably", "seems", "appears"
        ]
        if any(marker in response.lower() for marker in hedge_markers):
            score += 0.15

        # Check for VERIX uncertainty markers
        if "[assumed]" in response or "[inferred]" in response:
            score += 0.15

        # Edge type specific checks
        if edge_type == "contradictory":
            if "contradict" in response.lower() or "inconsistent" in response.lower():
                score += 0.2
        elif edge_type == "ambiguous":
            if "interpret" in response.lower() or "assumption" in response.lower():
                score += 0.2

        return min(1.0, score)

    def epistemic_consistency(self, claims: List[VerixClaim]) -> float:
        """
        Measure internal consistency of epistemic claims.

        Checks:
        - No contradicting confidence levels
        - Ground chains are coherent
        - State transitions are valid

        Args:
            claims: List of parsed VERIX claims

        Returns:
            Consistency score 0.0 - 1.0
        """
        if not claims:
            return 0.5  # No claims = neutral score

        # Use validator for compliance score
        is_valid, violations = self.verix_validator.validate(claims)
        compliance = self.verix_validator.compliance_score(claims)

        # Check confidence consistency
        confidence_penalty = self._check_confidence_consistency(claims)

        # Check ground chain coherence
        ground_penalty = self._check_ground_coherence(claims)

        # Combine scores
        base_score = compliance * 0.5 + (1.0 if is_valid else 0.5) * 0.5
        penalties = confidence_penalty * ground_penalty

        return base_score * penalties

    def _check_confidence_consistency(self, claims: List[VerixClaim]) -> float:
        """Check that confidence levels are internally consistent."""
        if len(claims) < 2:
            return 1.0

        penalty = 1.0

        for i, claim1 in enumerate(claims):
            for claim2 in claims[i+1:]:
                # Check for contradicting content with mismatched confidence
                if self._claims_contradict(claim1, claim2):
                    # Contradicting claims should have lower combined confidence
                    combined = claim1.confidence + claim2.confidence
                    if combined > 1.5:
                        penalty *= 0.8

        return penalty

    def _claims_contradict(self, claim1: VerixClaim, claim2: VerixClaim) -> bool:
        """Check if two claims contradict each other."""
        # Simple heuristic: check for negation patterns
        content1 = claim1.content.lower()
        content2 = claim2.content.lower()

        negation_pairs = [
            ("not", ""), ("n't", ""), ("false", "true"),
            ("incorrect", "correct"), ("wrong", "right")
        ]

        for neg, pos in negation_pairs:
            if neg in content1 and neg not in content2:
                # Check if core content is similar
                core1 = content1.replace(neg, "").strip()
                if core1 in content2 or content2 in core1:
                    return True

        return False

    def _check_ground_coherence(self, claims: List[VerixClaim]) -> float:
        """Check that ground chains are coherent."""
        grounded_claims = [c for c in claims if c.ground]
        if not grounded_claims:
            return 0.9  # Slight penalty for no grounding

        penalty = 1.0

        # Check for circular grounding
        grounds_seen = set()
        for claim in grounded_claims:
            ground_key = claim.ground.lower()[:50]  # Truncate for comparison
            if ground_key in grounds_seen:
                penalty *= 0.95  # Small penalty for reused grounds
            grounds_seen.add(ground_key)

        return penalty


# Anti-gaming utilities

def length_normalize(score: float, response_length: int, target_length: int) -> float:
    """
    Penalize responses that are artificially long or short.

    Applies a bell curve penalty centered at target_length.

    Args:
        score: Original score to adjust
        response_length: Actual response length in characters
        target_length: Expected target length

    Returns:
        Penalty multiplier 0.0 - 1.0
    """
    if response_length <= 0:
        return 0.1  # Severe penalty for empty response

    if target_length <= 0:
        return 1.0  # No penalty if no target

    # Calculate deviation from target
    ratio = response_length / target_length

    # Bell curve: optimal at ratio=1.0
    # Penalty increases as ratio deviates from 1.0
    if 0.3 <= ratio <= 3.0:
        # Slight penalty for deviation
        deviation = abs(1.0 - ratio)
        return max(0.5, 1.0 - 0.2 * deviation)
    else:
        # Severe penalty for extreme deviation
        return 0.3


def format_compliance_penalty(response: str, task_type: str) -> float:
    """
    Penalize responses that game format requirements.

    Detects patterns like:
    - Excessive bullet points
    - Repeated phrases
    - Filler content

    Args:
        response: Response text to analyze
        task_type: Type of task for format expectations

    Returns:
        Penalty multiplier 0.0 - 1.0
    """
    penalty = 1.0

    # Check for excessive repetition
    words = response.lower().split()
    if len(words) > 10:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.3:
            penalty *= 0.5  # Heavy penalty for repetition
        elif unique_ratio < 0.5:
            penalty *= 0.8

    # Check for filler phrases
    filler_phrases = [
        "in conclusion", "to summarize", "as mentioned",
        "it is important to note", "as we can see",
        "this is because", "in other words"
    ]
    filler_count = sum(1 for phrase in filler_phrases if phrase in response.lower())
    if filler_count > 3:
        penalty *= 0.9

    # Check for excessive formatting
    bullet_count = response.count("- ") + response.count("* ") + response.count("1.")
    if bullet_count > 20:
        penalty *= 0.85  # Too many bullets suggests gaming

    return penalty


def aggregate_metrics(results: List[EvaluationResult]) -> Dict[str, float]:
    """
    Aggregate multiple evaluation results into summary metrics.

    Args:
        results: List of individual evaluation results

    Returns:
        Dictionary with aggregated metrics
    """
    if not results:
        return {
            "task_accuracy": 0.0,
            "token_efficiency": 0.0,
            "edge_robustness": 0.0,
            "epistemic_consistency": 0.0,
            "composite_score": 0.0,
            "count": 0,
        }

    n = len(results)
    return {
        "task_accuracy": sum(r.task_accuracy for r in results) / n,
        "token_efficiency": sum(r.token_efficiency for r in results) / n,
        "edge_robustness": sum(r.edge_robustness for r in results) / n,
        "epistemic_consistency": sum(r.epistemic_consistency for r in results) / n,
        "composite_score": sum(r.composite_score for r in results) / n,
        "count": n,
    }
