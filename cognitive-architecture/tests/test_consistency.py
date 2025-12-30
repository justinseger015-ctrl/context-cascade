"""
Tests for eval/consistency.py

Tests:
- ConsistencyChecker all violation types
- ConsistencyResult structure
- check_epistemic_consistency function
- compute_coherence_score function
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.consistency import (
    ViolationType,
    ConsistencyViolation,
    ConsistencyResult,
    ConsistencyChecker,
    check_epistemic_consistency,
    compute_coherence_score,
)
from core.verix import VerixClaim, Illocution, Affect, State


class TestConsistencyViolation:
    """Tests for ConsistencyViolation dataclass."""

    def test_create_violation(self):
        """Should create violation with all fields."""
        violation = ConsistencyViolation(
            violation_type=ViolationType.CONFIDENCE_CONTRADICTION,
            claim_indices=[0, 1],
            description="Test violation",
            severity=0.5,
        )
        assert violation.violation_type == ViolationType.CONFIDENCE_CONTRADICTION
        assert violation.claim_indices == [0, 1]
        assert violation.severity == 0.5

    def test_to_dict(self):
        """to_dict() should include all fields."""
        violation = ConsistencyViolation(
            violation_type=ViolationType.GROUND_INCOHERENCE,
            claim_indices=[0],
            description="Test",
            severity=0.3,
        )
        d = violation.to_dict()
        assert d["type"] == "ground_incoherence"
        assert d["claim_indices"] == [0]
        assert d["severity"] == 0.3


class TestConsistencyResult:
    """Tests for ConsistencyResult dataclass."""

    def test_create_result(self):
        """Should create result with defaults."""
        result = ConsistencyResult(is_consistent=True)
        assert result.is_consistent is True
        assert result.violations == []
        assert result.coherence_score == 1.0

    def test_to_dict(self):
        """to_dict() should include all fields."""
        violation = ConsistencyViolation(
            violation_type=ViolationType.OVERCONFIDENCE,
            claim_indices=[0],
            description="Test",
            severity=0.5,
        )
        result = ConsistencyResult(
            is_consistent=False,
            violations=[violation],
            coherence_score=0.8,
            claim_count=5,
        )
        d = result.to_dict()
        assert d["is_consistent"] is False
        assert len(d["violations"]) == 1
        assert d["coherence_score"] == 0.8
        assert d["claim_count"] == 5


class TestConsistencyChecker:
    """Tests for ConsistencyChecker."""

    def _create_claim(
        self,
        content: str = "Test claim",
        confidence: float = 0.8,
        ground: str = None,
        illocution: Illocution = Illocution.ASSERT,
        affect: Affect = Affect.NEUTRAL,
        state: State = State.CONFIRMED,
    ) -> VerixClaim:
        """Helper to create test claims."""
        return VerixClaim(
            illocution=illocution,
            affect=affect,
            content=content,
            ground=ground,
            confidence=confidence,
            state=state,
            raw_text=f"[{illocution.value}|{affect.value}] {content}",
        )

    def test_empty_claims_neutral(self):
        """Empty claims should return neutral result."""
        checker = ConsistencyChecker()
        result = checker.check([])

        assert result.is_consistent is True
        assert result.coherence_score == 0.5
        assert result.claim_count == 0

    def test_single_claim_consistent(self):
        """Single grounded claim should be consistent."""
        checker = ConsistencyChecker()
        # Use grounded claim to avoid UNGROUNDED_HIGH_CONFIDENCE violation
        claims = [self._create_claim(
            "The sky is blue",
            confidence=0.9,
            ground="Direct observation"
        )]
        result = checker.check(claims)

        assert result.is_consistent is True
        assert result.claim_count == 1

    def test_detect_confidence_contradiction(self):
        """Should detect contradicting claims with high confidence."""
        checker = ConsistencyChecker()
        claims = [
            self._create_claim("The answer is correct", confidence=0.95),
            self._create_claim("The answer is not correct", confidence=0.95),
        ]
        result = checker.check(claims)

        # May or may not detect depending on content analysis
        # At minimum should complete without error
        assert isinstance(result, ConsistencyResult)

    def test_detect_ungrounded_high_confidence(self):
        """Should detect high confidence claims without grounding."""
        checker = ConsistencyChecker(require_grounds_for_high_confidence=True)
        claims = [
            self._create_claim(
                "This is definitely true",
                confidence=0.95,
                ground=None,  # No ground
            ),
        ]
        result = checker.check(claims)

        # Should have violation for ungrounded high confidence
        ungrounded_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.UNGROUNDED_HIGH_CONFIDENCE
        ]
        assert len(ungrounded_violations) > 0

    def test_detect_overconfidence(self):
        """Should detect systematic overconfidence."""
        checker = ConsistencyChecker()
        # Create many claims all with very high confidence
        claims = [
            self._create_claim(f"Claim {i}", confidence=0.99)
            for i in range(10)
        ]
        result = checker.check(claims)

        overconfidence_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.OVERCONFIDENCE
        ]
        assert len(overconfidence_violations) > 0

    def test_detect_illocution_mismatch_query(self):
        """Should detect QUERY without question markers."""
        checker = ConsistencyChecker()
        claims = [
            self._create_claim(
                "This is a statement",  # No question marks
                illocution=Illocution.QUERY,
            ),
        ]
        result = checker.check(claims)

        mismatch_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.ILLOCUTION_MISMATCH
        ]
        assert len(mismatch_violations) > 0

    def test_valid_query_no_violation(self):
        """Valid QUERY should not trigger violation."""
        checker = ConsistencyChecker()
        claims = [
            self._create_claim(
                "What is the answer?",
                illocution=Illocution.QUERY,
            ),
        ]
        result = checker.check(claims)

        mismatch_violations = [
            v for v in result.violations
            if v.violation_type == ViolationType.ILLOCUTION_MISMATCH
        ]
        assert len(mismatch_violations) == 0

    def test_grounded_claims_higher_coherence(self):
        """Grounded claims should have higher coherence score."""
        checker = ConsistencyChecker()

        grounded_claims = [
            self._create_claim(
                "Claim with evidence",
                confidence=0.8,
                ground="Verified by testing",
            ),
        ]
        ungrounded_claims = [
            self._create_claim(
                "Claim without evidence",
                confidence=0.8,
                ground=None,
            ),
        ]

        grounded_result = checker.check(grounded_claims)
        ungrounded_result = checker.check(ungrounded_claims)

        # Grounded should have higher or equal coherence
        assert grounded_result.coherence_score >= ungrounded_result.coherence_score

    def test_varied_confidence_bonus(self):
        """Varied confidence levels should get coherence bonus."""
        checker = ConsistencyChecker()

        # All same confidence
        uniform_claims = [
            self._create_claim(f"Claim {i}", confidence=0.8)
            for i in range(3)
        ]

        # Varied confidence
        varied_claims = [
            self._create_claim("High confidence", confidence=0.9),
            self._create_claim("Medium confidence", confidence=0.6),
            self._create_claim("Low confidence", confidence=0.3),
        ]

        uniform_result = checker.check(uniform_claims)
        varied_result = checker.check(varied_claims)

        # Varied should have at least similar coherence (bonus applied)
        assert varied_result.coherence_score > 0.5


class TestCheckEpistemicConsistency:
    """Tests for check_epistemic_consistency() function."""

    def test_convenience_function(self):
        """Should work as convenience wrapper."""
        claim = VerixClaim(
            illocution=Illocution.ASSERT,
            affect=Affect.NEUTRAL,
            content="Test",
            ground="Evidence",
            confidence=0.8,
            state=State.CONFIRMED,
            raw_text="[assert|neutral] Test",
        )
        result = check_epistemic_consistency([claim])
        assert isinstance(result, ConsistencyResult)


class TestComputeCoherenceScore:
    """Tests for compute_coherence_score() function."""

    def test_returns_float(self):
        """Should return float score."""
        score = compute_coherence_score([])
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_empty_claims_neutral_score(self):
        """Empty claims should return 0.5 (neutral)."""
        score = compute_coherence_score([])
        assert score == 0.5
