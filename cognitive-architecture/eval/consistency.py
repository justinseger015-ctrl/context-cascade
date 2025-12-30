"""
Epistemic consistency checking for VERIX claims.

Validates that claims within a response are internally consistent:
- No contradicting confidence levels
- Ground chains are coherent
- State transitions are valid
- Illocution-content alignment
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
from enum import Enum
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.verix import VerixClaim, VerixParser, Illocution, State, Affect


class ViolationType(Enum):
    """Types of consistency violations."""

    CONFIDENCE_CONTRADICTION = "confidence_contradiction"
    GROUND_INCOHERENCE = "ground_incoherence"
    STATE_TRANSITION_INVALID = "state_transition_invalid"
    ILLOCUTION_MISMATCH = "illocution_mismatch"
    AFFECT_INCONSISTENCY = "affect_inconsistency"
    CIRCULAR_GROUNDING = "circular_grounding"
    UNGROUNDED_HIGH_CONFIDENCE = "ungrounded_high_confidence"
    OVERCONFIDENCE = "overconfidence"


@dataclass
class ConsistencyViolation:
    """A single consistency violation."""

    violation_type: ViolationType
    claim_indices: List[int]  # Indices of claims involved
    description: str
    severity: float  # 0.0 - 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.violation_type.value,
            "claim_indices": self.claim_indices,
            "description": self.description,
            "severity": self.severity,
        }


@dataclass
class ConsistencyResult:
    """Result of consistency checking."""

    is_consistent: bool
    violations: List[ConsistencyViolation] = field(default_factory=list)
    coherence_score: float = 1.0
    claim_count: int = 0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_consistent": self.is_consistent,
            "violations": [v.to_dict() for v in self.violations],
            "coherence_score": self.coherence_score,
            "claim_count": self.claim_count,
            "details": self.details,
        }


class ConsistencyChecker:
    """Check epistemic consistency of VERIX claims."""

    # Thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.8
    OVERCONFIDENCE_THRESHOLD = 0.95

    def __init__(
        self,
        high_confidence_threshold: float = HIGH_CONFIDENCE_THRESHOLD,
        require_grounds_for_high_confidence: bool = True,
    ):
        """
        Initialize consistency checker.

        Args:
            high_confidence_threshold: Threshold for "high confidence" claims
            require_grounds_for_high_confidence: Whether high confidence needs grounding
        """
        self.high_confidence_threshold = high_confidence_threshold
        self.require_grounds_for_high_confidence = require_grounds_for_high_confidence

    def check(self, claims: List[VerixClaim]) -> ConsistencyResult:
        """
        Check consistency of a list of claims.

        Args:
            claims: List of VERIX claims to check

        Returns:
            ConsistencyResult with violations and scores
        """
        if not claims:
            return ConsistencyResult(
                is_consistent=True,
                coherence_score=0.5,  # Neutral for no claims
                claim_count=0,
            )

        violations = []

        # Run all consistency checks
        violations.extend(self._check_confidence_contradictions(claims))
        violations.extend(self._check_ground_coherence(claims))
        violations.extend(self._check_state_transitions(claims))
        violations.extend(self._check_illocution_alignment(claims))
        violations.extend(self._check_affect_consistency(claims))
        violations.extend(self._check_ungrounded_confidence(claims))
        violations.extend(self._check_overconfidence(claims))

        # Calculate coherence score
        coherence = self._calculate_coherence(claims, violations)

        return ConsistencyResult(
            is_consistent=len(violations) == 0,
            violations=violations,
            coherence_score=coherence,
            claim_count=len(claims),
            details={
                "total_violations": len(violations),
                "violation_types": list(set(v.violation_type.value for v in violations)),
                "average_confidence": sum(c.confidence for c in claims) / len(claims),
                "grounded_ratio": sum(1 for c in claims if c.ground) / len(claims),
            },
        )

    def _check_confidence_contradictions(
        self,
        claims: List[VerixClaim],
    ) -> List[ConsistencyViolation]:
        """Check for contradicting claims with high combined confidence."""
        violations = []

        for i, claim1 in enumerate(claims):
            for j, claim2 in enumerate(claims[i+1:], start=i+1):
                if self._claims_contradict(claim1, claim2):
                    # Contradicting claims should have lower combined confidence
                    combined = claim1.confidence + claim2.confidence
                    if combined > 1.0:
                        violations.append(ConsistencyViolation(
                            violation_type=ViolationType.CONFIDENCE_CONTRADICTION,
                            claim_indices=[i, j],
                            description=(
                                f"Claims {i} and {j} appear to contradict but have "
                                f"combined confidence of {combined:.2f}"
                            ),
                            severity=min(1.0, (combined - 1.0) * 2),
                        ))

        return violations

    def _check_ground_coherence(
        self,
        claims: List[VerixClaim],
    ) -> List[ConsistencyViolation]:
        """Check for incoherent or circular grounding."""
        violations = []
        ground_map: Dict[str, int] = {}  # ground -> claim index

        for i, claim in enumerate(claims):
            if not claim.ground:
                continue

            ground_key = claim.ground.lower().strip()[:100]

            # Check for circular grounding
            if ground_key in ground_map:
                original_idx = ground_map[ground_key]
                original_claim = claims[original_idx]

                # Check if original claim grounds on this claim's content
                if original_claim.ground and claim.content.lower() in original_claim.ground.lower():
                    violations.append(ConsistencyViolation(
                        violation_type=ViolationType.CIRCULAR_GROUNDING,
                        claim_indices=[original_idx, i],
                        description=(
                            f"Claims {original_idx} and {i} have circular grounding"
                        ),
                        severity=0.8,
                    ))

            ground_map[ground_key] = i

            # Check ground quality
            if len(claim.ground) < 10 and claim.confidence > 0.8:
                violations.append(ConsistencyViolation(
                    violation_type=ViolationType.GROUND_INCOHERENCE,
                    claim_indices=[i],
                    description=(
                        f"Claim {i} has weak ground '{claim.ground[:20]}...' "
                        f"but high confidence {claim.confidence:.2f}"
                    ),
                    severity=0.5,
                ))

        return violations

    def _check_state_transitions(
        self,
        claims: List[VerixClaim],
    ) -> List[ConsistencyViolation]:
        """Check for invalid state transitions."""
        violations = []

        # Track state transitions for similar content
        content_states: Dict[str, List[Tuple[int, State]]] = {}

        for i, claim in enumerate(claims):
            # Normalize content for comparison
            content_key = " ".join(claim.content.lower().split()[:10])

            if content_key in content_states:
                for prev_idx, prev_state in content_states[content_key]:
                    # Check for invalid transitions
                    if self._is_invalid_transition(prev_state, claim.state):
                        violations.append(ConsistencyViolation(
                            violation_type=ViolationType.STATE_TRANSITION_INVALID,
                            claim_indices=[prev_idx, i],
                            description=(
                                f"Invalid state transition from {prev_state.value} "
                                f"to {claim.state.value} for similar content"
                            ),
                            severity=0.6,
                        ))

                content_states[content_key].append((i, claim.state))
            else:
                content_states[content_key] = [(i, claim.state)]

        return violations

    def _check_illocution_alignment(
        self,
        claims: List[VerixClaim],
    ) -> List[ConsistencyViolation]:
        """Check that illocution matches content patterns."""
        violations = []

        for i, claim in enumerate(claims):
            content_lower = claim.content.lower()

            # QUERY should have question markers
            if claim.illocution == Illocution.QUERY:
                if "?" not in claim.content and not any(
                    word in content_lower for word in ["whether", "if", "what", "how", "why"]
                ):
                    violations.append(ConsistencyViolation(
                        violation_type=ViolationType.ILLOCUTION_MISMATCH,
                        claim_indices=[i],
                        description=(
                            f"Claim {i} marked as QUERY but content doesn't "
                            "appear to be a question"
                        ),
                        severity=0.3,
                    ))

            # DIRECT should have imperative markers
            if claim.illocution == Illocution.DIRECT:
                imperative_markers = ["should", "must", "need", "require", "ensure"]
                if not any(marker in content_lower for marker in imperative_markers):
                    violations.append(ConsistencyViolation(
                        violation_type=ViolationType.ILLOCUTION_MISMATCH,
                        claim_indices=[i],
                        description=(
                            f"Claim {i} marked as DIRECT but content doesn't "
                            "appear to be a directive"
                        ),
                        severity=0.3,
                    ))

            # COMMIT should have commitment markers
            if claim.illocution == Illocution.COMMIT:
                commitment_markers = ["will", "promise", "guarantee", "commit", "ensure"]
                if not any(marker in content_lower for marker in commitment_markers):
                    violations.append(ConsistencyViolation(
                        violation_type=ViolationType.ILLOCUTION_MISMATCH,
                        claim_indices=[i],
                        description=(
                            f"Claim {i} marked as COMMIT but content doesn't "
                            "contain commitment language"
                        ),
                        severity=0.3,
                    ))

        return violations

    def _check_affect_consistency(
        self,
        claims: List[VerixClaim],
    ) -> List[ConsistencyViolation]:
        """Check for inconsistent affect on related claims."""
        violations = []

        # Group claims by content similarity
        content_groups: Dict[str, List[int]] = {}
        for i, claim in enumerate(claims):
            key = " ".join(claim.content.lower().split()[:5])
            if key in content_groups:
                content_groups[key].append(i)
            else:
                content_groups[key] = [i]

        # Check for affect conflicts within groups
        for key, indices in content_groups.items():
            if len(indices) < 2:
                continue

            affects = [claims[i].affect for i in indices]

            # Check for opposing affects
            if Affect.POSITIVE in affects and Affect.NEGATIVE in affects:
                pos_idx = next(i for i in indices if claims[i].affect == Affect.POSITIVE)
                neg_idx = next(i for i in indices if claims[i].affect == Affect.NEGATIVE)

                violations.append(ConsistencyViolation(
                    violation_type=ViolationType.AFFECT_INCONSISTENCY,
                    claim_indices=[pos_idx, neg_idx],
                    description=(
                        f"Claims {pos_idx} and {neg_idx} have opposing affects "
                        "on similar content"
                    ),
                    severity=0.5,
                ))

        return violations

    def _check_ungrounded_confidence(
        self,
        claims: List[VerixClaim],
    ) -> List[ConsistencyViolation]:
        """Check for high confidence claims without grounding."""
        if not self.require_grounds_for_high_confidence:
            return []

        violations = []

        for i, claim in enumerate(claims):
            if claim.confidence >= self.high_confidence_threshold and not claim.ground:
                violations.append(ConsistencyViolation(
                    violation_type=ViolationType.UNGROUNDED_HIGH_CONFIDENCE,
                    claim_indices=[i],
                    description=(
                        f"Claim {i} has high confidence {claim.confidence:.2f} "
                        "but no grounding"
                    ),
                    severity=0.4,
                ))

        return violations

    def _check_overconfidence(
        self,
        claims: List[VerixClaim],
    ) -> List[ConsistencyViolation]:
        """Check for systematic overconfidence."""
        violations = []

        high_conf_claims = [c for c in claims if c.confidence >= self.OVERCONFIDENCE_THRESHOLD]

        if len(high_conf_claims) > len(claims) * 0.7:
            # More than 70% of claims have very high confidence
            violations.append(ConsistencyViolation(
                violation_type=ViolationType.OVERCONFIDENCE,
                claim_indices=list(range(len(claims))),
                description=(
                    f"{len(high_conf_claims)}/{len(claims)} claims have "
                    f"confidence >= {self.OVERCONFIDENCE_THRESHOLD}, suggesting overconfidence"
                ),
                severity=0.6,
            ))

        return violations

    def _claims_contradict(self, claim1: VerixClaim, claim2: VerixClaim) -> bool:
        """Check if two claims contradict each other."""
        content1 = claim1.content.lower()
        content2 = claim2.content.lower()

        # Check for explicit negation
        negation_patterns = [
            ("not ", ""), ("n't ", ""), ("false", "true"),
            ("incorrect", "correct"), ("wrong", "right"),
            ("no ", "yes "), ("never", "always"),
        ]

        for neg, pos in negation_patterns:
            if neg in content1 and pos in content2:
                # Check for content similarity
                core1 = content1.replace(neg, "").strip()
                core2 = content2.replace(pos, "").strip()
                if self._content_similar(core1, core2):
                    return True
            if neg in content2 and pos in content1:
                core1 = content1.replace(pos, "").strip()
                core2 = content2.replace(neg, "").strip()
                if self._content_similar(core1, core2):
                    return True

        # Check for retraction
        if claim1.state == State.CONFIRMED and claim2.state == State.RETRACTED:
            if self._content_similar(content1, content2):
                return True

        return False

    def _content_similar(self, content1: str, content2: str, threshold: float = 0.5) -> bool:
        """Check if two content strings are similar."""
        words1 = set(content1.split())
        words2 = set(content2.split())

        if not words1 or not words2:
            return False

        intersection = words1 & words2
        union = words1 | words2

        jaccard = len(intersection) / len(union)
        return jaccard >= threshold

    def _is_invalid_transition(self, from_state: State, to_state: State) -> bool:
        """Check if a state transition is invalid."""
        # Valid transitions:
        # PROVISIONAL -> CONFIRMED, RETRACTED
        # CONFIRMED -> RETRACTED (with explanation)
        # RETRACTED -> CONFIRMED (if re-evaluating)

        # Invalid: RETRACTED -> PROVISIONAL (should go to CONFIRMED or stay RETRACTED)
        if from_state == State.RETRACTED and to_state == State.PROVISIONAL:
            return True

        return False

    def _calculate_coherence(
        self,
        claims: List[VerixClaim],
        violations: List[ConsistencyViolation],
    ) -> float:
        """Calculate overall coherence score."""
        if not claims:
            return 0.5

        base_score = 1.0

        # Deduct for violations
        for violation in violations:
            base_score -= violation.severity * 0.1

        # Bonus for grounded claims
        grounded_ratio = sum(1 for c in claims if c.ground) / len(claims)
        base_score += grounded_ratio * 0.1

        # Bonus for varied confidence levels (not all 1.0 or all 0.0)
        confidences = [c.confidence for c in claims]
        if len(set(confidences)) > 1:
            base_score += 0.05

        return max(0.0, min(1.0, base_score))


def check_epistemic_consistency(claims: List[VerixClaim]) -> ConsistencyResult:
    """
    Convenience function to check consistency.

    Args:
        claims: List of VERIX claims

    Returns:
        ConsistencyResult
    """
    checker = ConsistencyChecker()
    return checker.check(claims)


def compute_coherence_score(claims: List[VerixClaim]) -> float:
    """
    Compute coherence score for claims.

    Args:
        claims: List of VERIX claims

    Returns:
        Coherence score 0.0 - 1.0
    """
    result = check_epistemic_consistency(claims)
    return result.coherence_score
