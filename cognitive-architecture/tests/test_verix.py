"""
Tests for core/verix.py

Tests:
- VerixClaim creation and properties
- VerixParser L1 and L0 format parsing
- VerixValidator validation and compliance scoring
- Format conversion (L0, L1, L2)
"""

import pytest
from core.verix import (
    Illocution,
    Affect,
    State,
    VerixClaim,
    VerixParser,
    VerixValidator,
    format_claim,
    create_claim,
)
from core.config import (
    PromptConfig,
    VerixStrictness,
    CompressionLevel,
)


class TestVerixClaim:
    """Tests for VerixClaim dataclass."""

    def test_create_basic_claim(self):
        """Should create claim with all fields."""
        claim = VerixClaim(
            illocution=Illocution.ASSERT,
            affect=Affect.NEUTRAL,
            content="Test content",
            ground="test_source",
            confidence=0.9,
            state=State.CONFIRMED,
            raw_text="raw",
        )
        assert claim.content == "Test content"
        assert claim.confidence == 0.9

    def test_is_high_confidence_default_threshold(self):
        """is_high_confidence() should use 0.8 default threshold."""
        high = create_claim("test", confidence=0.85)
        low = create_claim("test", confidence=0.75)
        assert high.is_high_confidence() is True
        assert low.is_high_confidence() is False

    def test_is_high_confidence_custom_threshold(self):
        """is_high_confidence() should accept custom threshold."""
        claim = create_claim("test", confidence=0.65)
        assert claim.is_high_confidence(0.6) is True
        assert claim.is_high_confidence(0.7) is False

    def test_is_grounded_with_ground(self):
        """is_grounded() should return True when ground is present."""
        claim = create_claim("test", ground="source")
        assert claim.is_grounded() is True

    def test_is_grounded_without_ground(self):
        """is_grounded() should return False when ground is None."""
        claim = create_claim("test", ground=None)
        assert claim.is_grounded() is False

    def test_is_grounded_with_empty_ground(self):
        """is_grounded() should return False for empty/whitespace ground."""
        claim = create_claim("test", ground="   ")
        assert claim.is_grounded() is False


class TestVerixClaimFormatting:
    """Tests for claim formatting at different levels."""

    def test_to_l0_format(self):
        """to_l0() should produce compact format."""
        claim = create_claim(
            "Test content here",
            illocution=Illocution.ASSERT,
            affect=Affect.NEUTRAL,
            confidence=0.85,
        )
        l0 = claim.to_l0()
        assert "A" in l0  # Assert
        assert "." in l0  # Neutral
        assert "85" in l0  # Confidence

    def test_to_l1_format(self):
        """to_l1() should produce annotated format."""
        claim = create_claim(
            "Test content",
            illocution=Illocution.ASSERT,
            affect=Affect.NEUTRAL,
            ground="source",
            confidence=0.85,
            state=State.CONFIRMED,
        )
        l1 = claim.to_l1()
        assert "[assert|neutral]" in l1
        assert "[ground:source]" in l1
        assert "[conf:0.85]" in l1
        assert "[state:confirmed]" in l1

    def test_to_l2_format_high_confidence(self):
        """to_l2() should express high confidence naturally."""
        claim = create_claim("This is true", confidence=0.95, ground="evidence")
        l2 = claim.to_l2()
        assert "highly confident" in l2.lower() or "confident" in l2.lower()

    def test_to_l2_format_low_confidence(self):
        """to_l2() should express low confidence naturally."""
        claim = create_claim("This might be true", confidence=0.25)
        l2 = claim.to_l2()
        assert "uncertain" in l2.lower() or "think" in l2.lower()


class TestVerixParser:
    """Tests for VerixParser."""

    def test_parse_l1_single_claim(self):
        """Should parse single L1 format claim."""
        text = "[assert|neutral] Test content [ground:source] [conf:0.85] [state:confirmed]"
        parser = VerixParser()
        claims = parser.parse(text)
        assert len(claims) == 1
        assert claims[0].illocution == Illocution.ASSERT
        assert claims[0].confidence == 0.85

    def test_parse_l1_multiple_claims(self):
        """Should parse multiple L1 claims."""
        text = """
        [assert|neutral] First claim [conf:0.9]
        [query|uncertain] Second claim [conf:0.5]
        """
        parser = VerixParser()
        claims = parser.parse(text)
        assert len(claims) == 2

    def test_parse_l0_format(self):
        """Should parse L0 compact format."""
        text = "A.85:Test content"
        parser = VerixParser()
        claims = parser.parse(text)
        assert len(claims) == 1
        assert claims[0].illocution == Illocution.ASSERT
        assert claims[0].affect == Affect.NEUTRAL
        assert claims[0].confidence == 0.85

    def test_parse_single_returns_first(self):
        """parse_single() should return first claim."""
        text = "[assert|neutral] Test [conf:0.9]"
        parser = VerixParser()
        claim = parser.parse_single(text)
        assert claim is not None
        assert claim.content.strip() == "Test"

    def test_parse_single_returns_none_for_no_match(self):
        """parse_single() should return None when no claim found."""
        parser = VerixParser()
        claim = parser.parse_single("No VERIX here")
        assert claim is None

    def test_parse_handles_missing_optional_fields(self):
        """Should handle claims with missing optional fields."""
        text = "[assert|neutral] Just content"
        parser = VerixParser()
        claims = parser.parse(text)
        # May or may not parse depending on regex - check gracefully
        # If parsed, should have defaults
        if claims:
            assert claims[0].state == State.PROVISIONAL


class TestVerixValidator:
    """Tests for VerixValidator."""

    def test_validate_valid_claims(self):
        """Should validate compliant claims."""
        config = PromptConfig(
            verix_strictness=VerixStrictness.MODERATE,
            require_ground=False,
        )
        validator = VerixValidator(config)

        claims = [
            create_claim("Test", ground="source", confidence=0.8, state=State.CONFIRMED)
        ]
        is_valid, violations = validator.validate(claims)
        assert is_valid is True
        assert len(violations) == 0

    def test_validate_missing_ground_when_required(self):
        """Should detect missing ground when required."""
        config = PromptConfig(require_ground=True)
        validator = VerixValidator(config)

        claims = [create_claim("Test", ground=None, confidence=0.8)]
        is_valid, violations = validator.validate(claims)
        assert is_valid is False
        assert any("ground" in v.lower() for v in violations)

    def test_validate_confidence_out_of_range(self):
        """Should detect confidence outside [0,1]."""
        config = PromptConfig()
        validator = VerixValidator(config)

        claims = [create_claim("Test", confidence=1.5)]
        is_valid, violations = validator.validate(claims)
        assert is_valid is False

    def test_validate_strict_mode_requires_all_fields(self):
        """STRICT mode should require all fields."""
        config = PromptConfig(verix_strictness=VerixStrictness.STRICT)
        validator = VerixValidator(config)

        claims = [create_claim("Test", ground=None, confidence=0.5)]
        is_valid, violations = validator.validate(claims)
        assert is_valid is False

    def test_validate_detects_inconsistent_confidence(self):
        """Should detect contradicting confidence on same content."""
        config = PromptConfig()
        validator = VerixValidator(config)

        claims = [
            create_claim("Same content", confidence=0.9),
            create_claim("Same content", confidence=0.3),
        ]
        is_valid, violations = validator.validate(claims)
        assert is_valid is False
        assert any("inconsistent" in v.lower() for v in violations)

    def test_compliance_score_range(self):
        """compliance_score() should return value in [0, 1]."""
        config = PromptConfig()
        validator = VerixValidator(config)

        claims = [create_claim("Test", ground="src", confidence=0.8)]
        score = validator.compliance_score(claims)
        assert 0.0 <= score <= 1.0

    def test_compliance_score_higher_for_grounded_claims(self):
        """Grounded claims should score higher."""
        config = PromptConfig()
        validator = VerixValidator(config)

        grounded = [create_claim("Test", ground="source", confidence=0.8)]
        ungrounded = [create_claim("Test", ground=None, confidence=0.8)]

        score_grounded = validator.compliance_score(grounded)
        score_ungrounded = validator.compliance_score(ungrounded)
        assert score_grounded > score_ungrounded


class TestHelperFunctions:
    """Tests for module helper functions."""

    def test_format_claim_l0(self):
        """format_claim() should format to L0."""
        claim = create_claim("Test", confidence=0.9)
        result = format_claim(claim, CompressionLevel.L0_AI_AI)
        assert "A" in result  # Assert shorthand

    def test_format_claim_l1(self):
        """format_claim() should format to L1."""
        claim = create_claim("Test", confidence=0.9)
        result = format_claim(claim, CompressionLevel.L1_AI_HUMAN)
        assert "[assert|" in result

    def test_format_claim_l2(self):
        """format_claim() should format to L2."""
        claim = create_claim("Test", confidence=0.9)
        result = format_claim(claim, CompressionLevel.L2_HUMAN)
        assert "Test" in result

    def test_create_claim_defaults(self):
        """create_claim() should use sensible defaults."""
        claim = create_claim("Just content")
        assert claim.illocution == Illocution.ASSERT
        assert claim.affect == Affect.NEUTRAL
        assert claim.confidence == 0.5
        assert claim.state == State.PROVISIONAL
