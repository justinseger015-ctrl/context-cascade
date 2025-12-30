"""
Tests for core/config.py

Tests:
- FrameworkConfig creation and frame listing
- PromptConfig creation and mode detection
- FullConfig combination
- VectorCodec encode/decode roundtrip
- VectorCodec cluster_key generation
- VectorCodec distance and interpolation
"""

import pytest
from core.config import (
    FrameworkConfig,
    PromptConfig,
    FullConfig,
    VectorCodec,
    VerixStrictness,
    CompressionLevel,
    DEFAULT_CONFIG,
    MINIMAL_CONFIG,
    STRICT_CONFIG,
)


class TestFrameworkConfig:
    """Tests for FrameworkConfig."""

    def test_default_config_has_evidential_and_aspectual(self):
        """Default config should have evidential and aspectual active."""
        config = FrameworkConfig()
        assert config.evidential is True
        assert config.aspectual is True

    def test_default_config_has_others_inactive(self):
        """Default config should have other frames inactive."""
        config = FrameworkConfig()
        assert config.morphological is False
        assert config.compositional is False
        assert config.honorific is False
        assert config.classifier is False
        assert config.spatial is False

    def test_active_frames_returns_list(self):
        """active_frames() should return list of active frame names."""
        config = FrameworkConfig()
        active = config.active_frames()
        assert "evidential" in active
        assert "aspectual" in active
        assert "morphological" not in active

    def test_frame_count_matches_active(self):
        """frame_count() should match length of active_frames()."""
        config = FrameworkConfig()
        assert config.frame_count() == len(config.active_frames())

    def test_all_frames_active(self):
        """Config with all frames should have 7 active."""
        config = FrameworkConfig(
            evidential=True,
            aspectual=True,
            morphological=True,
            compositional=True,
            honorific=True,
            classifier=True,
            spatial=True,
        )
        assert config.frame_count() == 7


class TestPromptConfig:
    """Tests for PromptConfig."""

    def test_default_strictness_is_moderate(self):
        """Default VERIX strictness should be MODERATE."""
        config = PromptConfig()
        assert config.verix_strictness == VerixStrictness.MODERATE

    def test_is_strict_true_for_strict_mode(self):
        """is_strict() should return True for STRICT mode."""
        config = PromptConfig(verix_strictness=VerixStrictness.STRICT)
        assert config.is_strict() is True

    def test_is_strict_false_for_moderate(self):
        """is_strict() should return False for non-STRICT modes."""
        config = PromptConfig(verix_strictness=VerixStrictness.MODERATE)
        assert config.is_strict() is False

    def test_is_relaxed_true_for_relaxed_mode(self):
        """is_relaxed() should return True for RELAXED mode."""
        config = PromptConfig(verix_strictness=VerixStrictness.RELAXED)
        assert config.is_relaxed() is True


class TestFullConfig:
    """Tests for FullConfig."""

    def test_default_full_config(self):
        """FullConfig should have nested default configs."""
        config = FullConfig()
        assert config.framework is not None
        assert config.prompt is not None

    def test_summary_includes_frames(self):
        """summary() should include active frame names."""
        config = FullConfig()
        summary = config.summary()
        assert "evidential" in summary
        assert "aspectual" in summary

    def test_summary_includes_strictness(self):
        """summary() should include VERIX strictness."""
        config = FullConfig()
        summary = config.summary()
        assert "MODERATE" in summary


class TestVectorCodec:
    """Tests for VectorCodec encode/decode."""

    def test_vector_size_is_14(self):
        """Vector size constant should be 14."""
        assert VectorCodec.VECTOR_SIZE == 14

    def test_encode_returns_14_floats(self):
        """encode() should return list of 14 floats."""
        config = FullConfig()
        vector = VectorCodec.encode(config)
        assert len(vector) == 14
        assert all(isinstance(v, float) for v in vector)

    def test_encode_decode_roundtrip_default(self):
        """encode->decode should preserve default config."""
        original = FullConfig()
        vector = VectorCodec.encode(original)
        decoded = VectorCodec.decode(vector)

        assert decoded.framework.evidential == original.framework.evidential
        assert decoded.framework.aspectual == original.framework.aspectual
        assert decoded.prompt.verix_strictness == original.prompt.verix_strictness

    def test_encode_decode_roundtrip_all_frames(self):
        """encode->decode should preserve all-frames config."""
        original = STRICT_CONFIG
        vector = VectorCodec.encode(original)
        decoded = VectorCodec.decode(vector)

        assert decoded.framework.frame_count() == 7
        assert decoded.prompt.verix_strictness == VerixStrictness.STRICT

    def test_encode_decode_roundtrip_minimal(self):
        """encode->decode should preserve minimal config."""
        original = MINIMAL_CONFIG
        vector = VectorCodec.encode(original)
        decoded = VectorCodec.decode(vector)

        assert decoded.framework.evidential is True
        assert decoded.framework.aspectual is False
        assert decoded.prompt.verix_strictness == VerixStrictness.RELAXED

    def test_decode_invalid_vector_size_raises(self):
        """decode() should raise ValueError for wrong vector size."""
        with pytest.raises(ValueError, match="14 dimensions"):
            VectorCodec.decode([0.0] * 10)

    def test_decode_clamps_invalid_enum_values(self):
        """decode() should clamp out-of-range enum values."""
        vector = [0.0] * 14
        vector[VectorCodec.IDX_VERIX_STRICTNESS] = 10.0  # Invalid
        config = VectorCodec.decode(vector)
        # Should clamp to valid range
        assert config.prompt.verix_strictness in VerixStrictness

    def test_cluster_key_deterministic(self):
        """cluster_key() should return same key for same config."""
        config = FullConfig()
        key1 = VectorCodec.cluster_key(config)
        key2 = VectorCodec.cluster_key(config)
        assert key1 == key2

    def test_cluster_key_differs_for_different_configs(self):
        """cluster_key() should differ for different configs."""
        key_default = VectorCodec.cluster_key(DEFAULT_CONFIG)
        key_strict = VectorCodec.cluster_key(STRICT_CONFIG)
        key_minimal = VectorCodec.cluster_key(MINIMAL_CONFIG)

        assert key_default != key_strict
        assert key_default != key_minimal
        assert key_strict != key_minimal

    def test_distance_zero_for_same_vector(self):
        """distance() should return 0 for identical vectors."""
        vector = VectorCodec.encode(FullConfig())
        assert VectorCodec.distance(vector, vector) == 0.0

    def test_distance_positive_for_different_vectors(self):
        """distance() should return positive for different vectors."""
        v1 = VectorCodec.encode(DEFAULT_CONFIG)
        v2 = VectorCodec.encode(STRICT_CONFIG)
        assert VectorCodec.distance(v1, v2) > 0.0

    def test_interpolate_at_zero_returns_v1(self):
        """interpolate(v1, v2, 0) should return v1."""
        v1 = [0.0] * 14
        v2 = [1.0] * 14
        result = VectorCodec.interpolate(v1, v2, 0.0)
        assert result == v1

    def test_interpolate_at_one_returns_v2(self):
        """interpolate(v1, v2, 1) should return v2."""
        v1 = [0.0] * 14
        v2 = [1.0] * 14
        result = VectorCodec.interpolate(v1, v2, 1.0)
        assert result == v2

    def test_interpolate_at_half_returns_midpoint(self):
        """interpolate(v1, v2, 0.5) should return midpoint."""
        v1 = [0.0] * 14
        v2 = [1.0] * 14
        result = VectorCodec.interpolate(v1, v2, 0.5)
        assert all(v == 0.5 for v in result)


class TestPresetConfigs:
    """Tests for preset configuration objects."""

    def test_default_config_exists(self):
        """DEFAULT_CONFIG should exist and be valid."""
        assert DEFAULT_CONFIG is not None
        assert isinstance(DEFAULT_CONFIG, FullConfig)

    def test_minimal_config_has_one_frame(self):
        """MINIMAL_CONFIG should have only evidential active."""
        assert MINIMAL_CONFIG.framework.evidential is True
        assert MINIMAL_CONFIG.framework.frame_count() == 1

    def test_strict_config_has_all_frames(self):
        """STRICT_CONFIG should have all 7 frames active."""
        assert STRICT_CONFIG.framework.frame_count() == 7
        assert STRICT_CONFIG.prompt.verix_strictness == VerixStrictness.STRICT
