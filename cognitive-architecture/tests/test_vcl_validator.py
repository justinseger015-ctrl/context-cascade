"""
Tests for VCL (VERILINGUA Cognitive Language) Validator.

Tests cover:
- E1: Slot order enforcement
- E2: Confidence ceiling by EVD type
- E3: Epistemic cosplay detection
- E4: Immutable safety bounds (EVD >= 1, ASP >= 1)
- E5: L2 English purity
- E6: Bracket collision detection
- E7: L2 naturalization

Run with: pytest tests/test_vcl_validator.py -v
"""

import os
import sys
import pytest

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.vcl_validator import (
    VCLValidator,
    VCLConfig,
    ValidationResult,
    L2Naturalizer,
    EVDType,
    ASPType,
    CompressionLevel,
    CONFIDENCE_CEILINGS,
    validate_vcl,
    naturalize_to_l2,
    enforce_safety_bounds,
    compute_cluster_signature,
)


class TestSlotOrderEnforcement:
    """E1: Test VCL 7-slot order enforcement."""

    def test_correct_slot_order(self):
        """Verify correct slot order passes validation."""
        validator = VCLValidator()

        # Correct order: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
        correct_output = """
        [[HON:teineigo]] [[MOR:root:k-t-b]] [[COM:Test+Result]]
        [[CLS:one_test]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[SPC:N]]
        The test passed successfully.
        """
        result = validator.validate(correct_output)
        assert result.checks["slot_order_correct"] == True

    def test_incorrect_slot_order(self):
        """Verify incorrect slot order fails validation."""
        validator = VCLValidator()

        # Wrong order: EVD before HON
        wrong_output = """
        [[EVD:-DI<gozlem>]] [[HON:teineigo]]
        The test result is available.
        """
        result = validator.validate(wrong_output)
        assert result.checks["slot_order_correct"] == False

    def test_partial_slots_correct_order(self):
        """Verify partial slots in correct order passes."""
        validator = VCLValidator()

        # Only EVD and ASP (skipping others is OK if order maintained)
        partial_output = """
        [[EVD:-DI<gozlem>]] [[ASP:sov.]]
        I observed the test passing.
        """
        result = validator.validate(partial_output)
        assert result.checks["slot_order_correct"] == True

    def test_l2_output_no_slots(self):
        """Verify L2 output with no slots passes slot order check."""
        validator = VCLValidator()

        # Pure English L2 output
        l2_output = "I directly observed the test passing. Complete."
        result = validator.validate(l2_output)
        assert result.checks["slot_order_correct"] == True


class TestConfidenceCeiling:
    """E2: Test confidence ceiling enforcement by EVD type."""

    def test_observation_ceiling(self):
        """Observation allows up to 0.95 confidence."""
        validator = VCLValidator()

        # Good: observation with 0.95
        good_output = "[ground:observed] [conf:0.95] I observed the test passing."
        result = validator.validate(good_output)
        assert result.checks["confidence_ceiling_respected"] == True

        # Bad: observation with 0.98 (exceeds ceiling)
        bad_output = "[ground:observed] [conf:0.98] I observed the test passing."
        result = validator.validate(bad_output)
        assert result.checks["confidence_ceiling_respected"] == False

    def test_inference_ceiling(self):
        """Inference allows only up to 0.70 confidence."""
        validator = VCLValidator()

        # Good: inference with 0.70
        good_output = "I infer that [conf:0.70] the bug is in this function."
        result = validator.validate(good_output)
        assert result.checks["confidence_ceiling_respected"] == True

        # Bad: inference with 0.85 (exceeds ceiling)
        bad_output = "I infer that [conf:0.85] the bug is in this function."
        result = validator.validate(bad_output)
        assert result.checks["confidence_ceiling_respected"] == False

    def test_report_ceiling(self):
        """Report allows only up to 0.70 confidence."""
        validator = VCLValidator()

        # Good: report with 0.65
        good_output = "It's reported that [conf:0.65] the API is deprecated."
        result = validator.validate(good_output)
        assert result.checks["confidence_ceiling_respected"] == True

        # Bad: report with 0.90
        bad_output = "It's reported that [conf:0.90] the API is deprecated."
        result = validator.validate(bad_output)
        assert result.checks["confidence_ceiling_respected"] == False

    def test_research_ceiling(self):
        """Research allows up to 0.85 confidence."""
        validator = VCLValidator()

        # Good: research with 0.85
        good_output = "Research indicates [conf:0.85] this approach works."
        result = validator.validate(good_output)
        assert result.checks["confidence_ceiling_respected"] == True

    def test_no_confidence_marker(self):
        """Output without confidence marker passes ceiling check."""
        validator = VCLValidator()

        output = "I observed the test passing."
        result = validator.validate(output)
        assert result.checks["confidence_ceiling_respected"] == True


class TestEpistemicCosplayDetection:
    """E3: Test epistemic cosplay detection."""

    def test_valid_observation_claim(self):
        """Valid observation with proper ground passes."""
        validator = VCLValidator()

        # Good: observation claim with observation ground
        good_output = """
        I directly observed [ground:observed:ran_test] [conf:0.90]
        that the test suite passes.
        """
        result = validator.validate(good_output)
        assert result.checks["no_epistemic_cosplay"] == True

    def test_high_confidence_from_inference(self):
        """High confidence from inference is cosplay."""
        validator = VCLValidator()

        # Bad: claiming 0.90 confidence from inference
        bad_output = "I infer that [conf:0.90] the function is correct."
        result = validator.validate(bad_output)
        assert result.checks["no_epistemic_cosplay"] == False

    def test_high_confidence_from_report(self):
        """High confidence from report is cosplay."""
        validator = VCLValidator()

        # Bad: claiming 0.88 confidence from report
        bad_output = "It's reported that [conf:0.88] the server is down."
        result = validator.validate(bad_output)
        assert result.checks["no_epistemic_cosplay"] == False

    def test_appropriate_confidence_from_report(self):
        """Appropriate confidence from report passes."""
        validator = VCLValidator()

        # Good: 0.65 confidence from report is appropriate
        good_output = "It's reported that [conf:0.65] the server is down."
        result = validator.validate(good_output)
        assert result.checks["no_epistemic_cosplay"] == True


class TestImmutableSafetyBounds:
    """E4: Test immutable safety bounds (EVD >= 1, ASP >= 1)."""

    def test_safety_bounds_enforced_in_config(self):
        """VCLConfig enforces safety bounds."""
        config = VCLConfig(evd_enforcement=0, asp_enforcement=0)
        config.enforce_safety_bounds()

        assert config.evd_enforcement >= 1, "EVD enforcement must be >= 1"
        assert config.asp_enforcement >= 1, "ASP enforcement must be >= 1"

    def test_validator_enforces_bounds(self):
        """Validator enforces safety bounds on config."""
        # Try to create config with 0 enforcement
        config = VCLConfig(evd_enforcement=0, asp_enforcement=0)
        validator = VCLValidator(config)

        # Check that bounds were enforced
        result = validator.validate("Test output")
        assert result.checks["immutable_bounds_enforced"] == True

    def test_enforce_safety_bounds_function(self):
        """Test enforce_safety_bounds utility function."""
        # Dict with vector14
        config1 = {
            "vector14": [1, 1, 1, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0]
        }
        result1 = enforce_safety_bounds(config1)
        assert result1["vector14"][4] >= 1  # EVD
        assert result1["vector14"][5] >= 1  # ASP

        # Dict with vcl_slots
        config2 = {
            "vcl_slots": {
                "EVD": {"enforcement": 0},
                "ASP": {"enforcement": 0}
            }
        }
        result2 = enforce_safety_bounds(config2)
        assert result2["vcl_slots"]["EVD"]["enforcement"] >= 1
        assert result2["vcl_slots"]["ASP"]["enforcement"] >= 1


class TestL2EnglishPurity:
    """E5: Test L2 English output purity."""

    def test_pure_english_passes(self):
        """Pure English L2 output passes validation."""
        config = VCLConfig(compression=CompressionLevel.L2_HUMAN)
        validator = VCLValidator(config)

        # Good: Pure English
        good_output = "I observed the test passing. The API is working correctly."
        result = validator.validate(good_output)
        assert result.checks["l2_english_output"] == True

    def test_vcl_notation_leaks_fail(self):
        """VCL notation in L2 output fails validation."""
        config = VCLConfig(compression=CompressionLevel.L2_HUMAN)
        validator = VCLValidator(config)

        # Bad: VCL notation leaked
        bad_outputs = [
            "[[EVD:-DI<gozlem>]] The test passed.",
            "[EVD:observation] Test result.",
            "Test passed [ASP:sov.]",
            "-DI<observation> direct test",
        ]

        for bad_output in bad_outputs:
            result = validator.validate(bad_output)
            assert result.checks["l2_english_output"] == False, f"Should fail: {bad_output}"

    def test_verix_markers_allowed_in_l2(self):
        """VERIX markers (ground, conf, state) are allowed in L2."""
        config = VCLConfig(compression=CompressionLevel.L2_HUMAN)
        validator = VCLValidator(config)

        # VERIX markers are allowed for auditability
        output = "I observed [ground:witnessed] [conf:0.90] [state:confirmed] the test passing."
        result = validator.validate(output)
        assert result.checks["l2_english_output"] == True

    def test_l0_l1_allow_vcl_notation(self):
        """L0 and L1 modes allow VCL notation."""
        # L1 mode
        config_l1 = VCLConfig(compression=CompressionLevel.L1_AUDIT)
        validator_l1 = VCLValidator(config_l1)

        vcl_output = "[[EVD:-DI<gozlem>]] [[ASP:sov.]] The test passed."
        result = validator_l1.validate(vcl_output)
        assert result.checks["l2_english_output"] == True  # Not enforced in L1


class TestBracketCollision:
    """E6: Test bracket collision detection."""

    def test_no_collision(self):
        """Valid VCL without bracket collision passes."""
        validator = VCLValidator()

        good_output = "[[EVD:-DI<gozlem>]] Test passed."
        result = validator.validate(good_output)
        assert result.checks["no_bracket_collision"] == True

    def test_bracket_inside_slot(self):
        """Brackets inside VCL slot body is a collision."""
        validator = VCLValidator()

        # Bad: [ ] inside slot body
        bad_output = "[[EVD:test[bad]value]] Result."
        result = validator.validate(bad_output)
        assert result.checks["no_bracket_collision"] == False


class TestL2Naturalization:
    """E7: Test L2 naturalization (VCL -> English)."""

    def test_evd_naturalization(self):
        """Test EVD type to English conversion."""
        naturalizer = L2Naturalizer()

        assert naturalizer.naturalize_evd(EVDType.OBSERVATION) == "I directly observed that"
        assert naturalizer.naturalize_evd(EVDType.RESEARCH) == "Research indicates that"
        assert naturalizer.naturalize_evd(EVDType.REPORT) == "It's reported that"
        assert naturalizer.naturalize_evd(EVDType.INFERENCE) == "I infer that"

    def test_asp_naturalization(self):
        """Test ASP type to English conversion."""
        naturalizer = L2Naturalizer()

        assert naturalizer.naturalize_asp(ASPType.PERFECTIVE) == "Complete."
        assert naturalizer.naturalize_asp(ASPType.PERFECTIVE, "all tests pass") == "Complete. (all tests pass)"
        assert naturalizer.naturalize_asp(ASPType.IMPERFECTIVE) == "In progress."

    def test_confidence_naturalization(self):
        """Test confidence to English conversion."""
        naturalizer = L2Naturalizer()

        assert "highly confident" in naturalizer.naturalize_confidence(0.95)
        assert "fairly confident" in naturalizer.naturalize_confidence(0.85)
        assert "believe" in naturalizer.naturalize_confidence(0.70).lower()
        assert "think" in naturalizer.naturalize_confidence(0.50).lower()
        assert "speculative" in naturalizer.naturalize_confidence(0.25).lower()

    def test_full_naturalization(self):
        """Test full VCL to English conversion."""
        vcl_output = "[[HON:teineigo]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] Test passed."
        english = naturalize_to_l2(vcl_output)

        # Should not contain VCL markers
        assert "[[" not in english
        assert "]]" not in english
        assert "HON:" not in english


class TestClusterSignature:
    """Test DSPy cluster signature computation."""

    def test_same_config_same_hash(self):
        """Same configuration produces same hash."""
        config = VCLConfig()

        hash1 = compute_cluster_signature(config)
        hash2 = compute_cluster_signature(config)

        assert hash1 == hash2

    def test_different_config_different_hash(self):
        """Different configurations produce different hashes."""
        config1 = VCLConfig(evd_enforcement=1)
        config2 = VCLConfig(evd_enforcement=2)

        hash1 = compute_cluster_signature(config1)
        hash2 = compute_cluster_signature(config2)

        assert hash1 != hash2

    def test_hash_is_8_chars(self):
        """Hash is exactly 8 characters."""
        config = VCLConfig()
        hash_value = compute_cluster_signature(config)

        assert len(hash_value) == 8


class TestValidationResult:
    """Test ValidationResult structure."""

    def test_passed_when_all_checks_pass(self):
        """ValidationResult.passed is True when all checks pass."""
        config = VCLConfig(compression=CompressionLevel.L2_HUMAN)
        validator = VCLValidator(config)

        # Good L2 output
        good_output = """
        I observed the test suite passing. [ground:witnessed:ran_pytest]
        [conf:0.90] [state:confirmed] All tests complete.
        """
        result = validator.validate(good_output)

        assert result.passed == True
        assert result.vcl_compliance_score > 0.9

    def test_failed_with_violations(self):
        """ValidationResult contains violations when checks fail."""
        config = VCLConfig(compression=CompressionLevel.L2_HUMAN)
        validator = VCLValidator(config)

        # Bad: VCL notation leaked in L2
        bad_output = "[[EVD:-DI<gozlem>]] Test passed."
        result = validator.validate(bad_output)

        assert result.passed == False
        assert len(result.violations) > 0
        assert any("l2_english_output" in v for v in result.violations)


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_validate_vcl_function(self):
        """Test validate_vcl convenience function."""
        result = validate_vcl("I observed the test passing.")
        assert isinstance(result, ValidationResult)

    def test_naturalize_to_l2_function(self):
        """Test naturalize_to_l2 convenience function."""
        vcl = "[[EVD:-DI<gozlem>]] Test passed."
        english = naturalize_to_l2(vcl)
        assert "[[" not in english


class TestConfidenceCeilingConstants:
    """Test confidence ceiling constants."""

    def test_all_evd_types_have_ceilings(self):
        """All EVD types must have defined ceilings."""
        for evd_type in EVDType:
            assert evd_type in CONFIDENCE_CEILINGS, f"Missing ceiling for {evd_type}"

    def test_ceiling_values_are_reasonable(self):
        """Ceiling values must be in valid range."""
        for evd_type, ceiling in CONFIDENCE_CEILINGS.items():
            assert 0.0 <= ceiling <= 1.0, f"Invalid ceiling for {evd_type}: {ceiling}"

    def test_observation_has_highest_ceiling(self):
        """Observation and definition have highest ceilings."""
        assert CONFIDENCE_CEILINGS[EVDType.OBSERVATION] >= 0.95
        assert CONFIDENCE_CEILINGS[EVDType.DEFINITION] >= 0.95

    def test_inference_has_lowest_ceiling(self):
        """Inference and report have lowest ceilings."""
        assert CONFIDENCE_CEILINGS[EVDType.INFERENCE] <= 0.70
        assert CONFIDENCE_CEILINGS[EVDType.REPORT] <= 0.70


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
