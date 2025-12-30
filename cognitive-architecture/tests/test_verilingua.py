"""
Tests for core/verilingua.py

Tests:
- All 7 cognitive frame implementations
- FrameRegistry registration and lookup
- Frame scoring functions
- Combined activation instructions
"""

import pytest
from core.verilingua import (
    CognitiveFrame,
    EvidentialFrame,
    AspectualFrame,
    MorphologicalFrame,
    CompositionalFrame,
    HonorificFrame,
    ClassifierFrame,
    SpatialFrame,
    FrameRegistry,
    score_all_frames,
    aggregate_frame_score,
    get_combined_activation_instruction,
)
from core.config import FrameworkConfig


class TestEvidentialFrame:
    """Tests for EvidentialFrame (Turkish)."""

    def test_frame_properties(self):
        """Should have correct metadata."""
        frame = EvidentialFrame()
        assert frame.name == "evidential"
        assert frame.linguistic_source == "Turkish"
        assert "know" in frame.cognitive_force.lower()

    def test_activation_instruction_not_empty(self):
        """activation_instruction() should return non-empty string."""
        frame = EvidentialFrame()
        instruction = frame.activation_instruction()
        assert len(instruction) > 100
        assert "[witnessed]" in instruction

    def test_compliance_markers_exist(self):
        """compliance_markers() should return marker list."""
        frame = EvidentialFrame()
        markers = frame.compliance_markers()
        assert "[witnessed]" in markers
        assert "[reported]" in markers
        assert "[inferred]" in markers
        assert "[assumed]" in markers

    def test_score_response_with_markers(self):
        """score_response() should score based on marker presence."""
        frame = EvidentialFrame()
        response = "[witnessed] I saw this. [inferred] Therefore this follows."
        score = frame.score_response(response)
        assert score > 0

    def test_score_response_without_markers(self):
        """score_response() should return low score without markers."""
        frame = EvidentialFrame()
        response = "This is a statement without any markers."
        score = frame.score_response(response)
        # May return some score based on estimation
        assert 0.0 <= score <= 1.0


class TestAspectualFrame:
    """Tests for AspectualFrame (Russian)."""

    def test_frame_properties(self):
        """Should have correct metadata."""
        frame = AspectualFrame()
        assert frame.name == "aspectual"
        assert frame.linguistic_source == "Russian"
        assert "complete" in frame.cognitive_force.lower() or "ongoing" in frame.cognitive_force.lower()

    def test_compliance_markers_exist(self):
        """Should have aspect markers."""
        frame = AspectualFrame()
        markers = frame.compliance_markers()
        assert "[complete]" in markers
        assert "[ongoing]" in markers

    def test_score_response_with_markers(self):
        """Should score higher with aspect markers."""
        frame = AspectualFrame()
        response = "[complete] The task is done. [ongoing] Processing continues."
        score = frame.score_response(response)
        assert score > 0


class TestMorphologicalFrame:
    """Tests for MorphologicalFrame (Arabic)."""

    def test_frame_properties(self):
        """Should have correct metadata."""
        frame = MorphologicalFrame()
        assert frame.name == "morphological"
        assert frame.linguistic_source == "Arabic"

    def test_compliance_markers_exist(self):
        """Should have decomposition markers."""
        frame = MorphologicalFrame()
        markers = frame.compliance_markers()
        assert "[root:" in markers[0] or any("[root:" in m for m in markers)


class TestCompositionalFrame:
    """Tests for CompositionalFrame (German)."""

    def test_frame_properties(self):
        """Should have correct metadata."""
        frame = CompositionalFrame()
        assert frame.name == "compositional"
        assert frame.linguistic_source == "German"

    def test_compliance_markers_exist(self):
        """Should have compositional markers."""
        frame = CompositionalFrame()
        markers = frame.compliance_markers()
        assert any("primitive" in m.lower() for m in markers)


class TestHonorificFrame:
    """Tests for HonorificFrame (Japanese)."""

    def test_frame_properties(self):
        """Should have correct metadata."""
        frame = HonorificFrame()
        assert frame.name == "honorific"
        assert frame.linguistic_source == "Japanese"
        assert "audience" in frame.cognitive_force.lower()

    def test_compliance_markers_exist(self):
        """Should have audience markers."""
        frame = HonorificFrame()
        markers = frame.compliance_markers()
        assert any("audience" in m.lower() for m in markers)


class TestClassifierFrame:
    """Tests for ClassifierFrame (Chinese)."""

    def test_frame_properties(self):
        """Should have correct metadata."""
        frame = ClassifierFrame()
        assert frame.name == "classifier"
        assert frame.linguistic_source == "Chinese"

    def test_compliance_markers_exist(self):
        """Should have classifier markers."""
        frame = ClassifierFrame()
        markers = frame.compliance_markers()
        assert any("type" in m.lower() for m in markers)


class TestSpatialFrame:
    """Tests for SpatialFrame (Guugu Yimithirr)."""

    def test_frame_properties(self):
        """Should have correct metadata."""
        frame = SpatialFrame()
        assert frame.name == "spatial"
        assert "Guugu" in frame.linguistic_source

    def test_compliance_markers_exist(self):
        """Should have spatial markers."""
        frame = SpatialFrame()
        markers = frame.compliance_markers()
        assert any("path" in m.lower() for m in markers)


class TestFrameRegistry:
    """Tests for FrameRegistry."""

    def test_get_existing_frame(self):
        """get() should return frame by name."""
        frame = FrameRegistry.get("evidential")
        assert frame is not None
        assert frame.name == "evidential"

    def test_get_nonexistent_raises(self):
        """get() should raise KeyError for unknown frame."""
        with pytest.raises(KeyError):
            FrameRegistry.get("nonexistent")

    def test_get_all_returns_all_frames(self):
        """get_all() should return dict of all frames."""
        all_frames = FrameRegistry.get_all()
        assert len(all_frames) == 7
        assert "evidential" in all_frames
        assert "spatial" in all_frames

    def test_get_active_returns_enabled_frames(self):
        """get_active() should return only enabled frames."""
        config = FrameworkConfig(
            evidential=True,
            aspectual=True,
            morphological=False,
        )
        active = FrameRegistry.get_active(config)
        active_names = [f.name for f in active]
        assert "evidential" in active_names
        assert "aspectual" in active_names
        assert "morphological" not in active_names

    def test_get_active_empty_config(self):
        """get_active() should return empty list when all disabled."""
        config = FrameworkConfig(
            evidential=False,
            aspectual=False,
            morphological=False,
            compositional=False,
            honorific=False,
            classifier=False,
            spatial=False,
        )
        active = FrameRegistry.get_active(config)
        assert len(active) == 0

    def test_list_names(self):
        """list_names() should return all frame names."""
        names = FrameRegistry.list_names()
        assert len(names) == 7
        assert "evidential" in names
        assert "spatial" in names


class TestScoringFunctions:
    """Tests for scoring utility functions."""

    def test_score_all_frames_returns_dict(self):
        """score_all_frames() should return dict of scores."""
        config = FrameworkConfig()
        response = "[witnessed] Test [complete] Done"
        scores = score_all_frames(response, config)

        # Should have scores for active frames
        assert isinstance(scores, dict)
        assert "evidential" in scores
        assert 0.0 <= scores["evidential"] <= 1.0

    def test_aggregate_frame_score_in_range(self):
        """aggregate_frame_score() should return value in [0, 1]."""
        config = FrameworkConfig()
        response = "Some response text"
        score = aggregate_frame_score(response, config)
        assert 0.0 <= score <= 1.0

    def test_aggregate_frame_score_no_frames_returns_one(self):
        """aggregate_frame_score() with no active frames returns 1.0."""
        config = FrameworkConfig(
            evidential=False,
            aspectual=False,
            morphological=False,
            compositional=False,
            honorific=False,
            classifier=False,
            spatial=False,
        )
        score = aggregate_frame_score("Test", config)
        assert score == 1.0


class TestCombinedActivation:
    """Tests for combined activation instructions."""

    def test_combined_instruction_includes_active_frames(self):
        """get_combined_activation_instruction() should include active frames."""
        config = FrameworkConfig(evidential=True, aspectual=True)
        instruction = get_combined_activation_instruction(config)

        assert "EVIDENTIAL" in instruction.upper()
        assert "ASPECTUAL" in instruction.upper()

    def test_combined_instruction_empty_when_no_frames(self):
        """get_combined_activation_instruction() should be empty with no frames."""
        config = FrameworkConfig(
            evidential=False,
            aspectual=False,
            morphological=False,
            compositional=False,
            honorific=False,
            classifier=False,
            spatial=False,
        )
        instruction = get_combined_activation_instruction(config)
        assert instruction == ""
