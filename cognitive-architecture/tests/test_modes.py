"""
Tests for optimization/distill_modes.py

Tests:
- NamedMode structure
- ModeLibrary operations
- ModeDistiller distillation
- Default modes
"""

import pytest
import tempfile
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.distill_modes import (
    NamedMode,
    ModeCategory,
    ModeLibrary,
    ModeDistiller,
    create_distiller,
    load_mode,
    list_modes,
)
from optimization.globalmoo_client import ParetoPoint
from core.config import FullConfig, VectorCodec, VerixStrictness


class TestModeCategory:
    """Tests for ModeCategory enum."""

    def test_all_categories_defined(self):
        """Should have all expected categories."""
        categories = list(ModeCategory)
        assert ModeCategory.STRICT in categories
        assert ModeCategory.BALANCED in categories
        assert ModeCategory.EFFICIENT in categories
        assert ModeCategory.ROBUST in categories
        assert ModeCategory.MINIMAL in categories
        assert ModeCategory.CUSTOM in categories


class TestNamedMode:
    """Tests for NamedMode dataclass."""

    def test_create_mode(self):
        """Should create named mode."""
        config = FullConfig()
        mode = NamedMode(
            name="test-mode",
            category=ModeCategory.BALANCED,
            description="A test mode",
            config=config,
            config_vector=VectorCodec.encode(config),
            expected_outcomes={"task_accuracy": 0.8},
            use_cases=["Testing"],
        )
        assert mode.name == "test-mode"
        assert mode.category == ModeCategory.BALANCED

    def test_to_dict(self):
        """to_dict should serialize mode."""
        config = FullConfig()
        config.framework.morphological = True

        mode = NamedMode(
            name="test",
            category=ModeCategory.STRICT,
            description="Test",
            config=config,
            config_vector=VectorCodec.encode(config),
            expected_outcomes={},
        )
        d = mode.to_dict()
        assert d["name"] == "test"
        assert d["category"] == "strict"
        assert d["config"]["framework"]["morphological"] is True

    def test_from_dict(self):
        """from_dict should reconstruct mode."""
        config = FullConfig()
        config.prompt.verix_strictness = VerixStrictness.STRICT

        original = NamedMode(
            name="original",
            category=ModeCategory.EFFICIENT,
            description="Test",
            config=config,
            config_vector=VectorCodec.encode(config),
            expected_outcomes={"task_accuracy": 0.7},
        )
        d = original.to_dict()
        reconstructed = NamedMode.from_dict(d)

        assert reconstructed.name == original.name
        assert reconstructed.category == original.category
        assert reconstructed.config.prompt.verix_strictness == VerixStrictness.STRICT

    def test_to_yaml(self):
        """to_yaml should return valid YAML."""
        mode = NamedMode(
            name="yaml-test",
            category=ModeCategory.MINIMAL,
            description="YAML test",
            config=FullConfig(),
            config_vector=[0.5] * 14,
            expected_outcomes={},
        )
        yaml_str = mode.to_yaml()
        assert "yaml-test" in yaml_str
        assert "minimal" in yaml_str


class TestModeLibrary:
    """Tests for ModeLibrary."""

    def test_creates_defaults(self):
        """Library should create default modes on init."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")

            modes = library.list_modes()
            assert "default" in modes
            assert "strict" in modes
            assert "minimal" in modes

    def test_get_mode(self):
        """get should return mode by name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")

            mode = library.get("default")
            assert mode is not None
            assert mode.name == "default"

    def test_get_nonexistent_returns_none(self):
        """get should return None for unknown mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")
            assert library.get("nonexistent") is None

    def test_add_mode(self):
        """add should add new mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")

            custom = NamedMode(
                name="custom-mode",
                category=ModeCategory.CUSTOM,
                description="Custom",
                config=FullConfig(),
                config_vector=[0.5] * 14,
                expected_outcomes={},
            )
            library.add(custom)

            assert library.get("custom-mode") is not None

    def test_remove_mode(self):
        """remove should remove mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")

            # Add and remove
            custom = NamedMode(
                name="to-remove",
                category=ModeCategory.CUSTOM,
                description="",
                config=FullConfig(),
                config_vector=[],
                expected_outcomes={},
            )
            library.add(custom)
            assert library.get("to-remove") is not None

            result = library.remove("to-remove")
            assert result is True
            assert library.get("to-remove") is None

    def test_list_by_category(self):
        """list_by_category should filter modes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")

            balanced_modes = library.list_by_category(ModeCategory.BALANCED)
            assert len(balanced_modes) > 0
            assert all(m.category == ModeCategory.BALANCED for m in balanced_modes)

    def test_save_and_load(self):
        """Library should persist to disk."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "modes.yaml"

            # Create and save
            lib1 = ModeLibrary(library_path=path)
            lib1.add(NamedMode(
                name="persisted",
                category=ModeCategory.CUSTOM,
                description="Test",
                config=FullConfig(),
                config_vector=[0.5] * 14,
                expected_outcomes={},
            ))
            lib1.save()

            # Load in new instance
            lib2 = ModeLibrary(library_path=path)
            assert lib2.get("persisted") is not None


class TestModeDistiller:
    """Tests for ModeDistiller."""

    def test_create_default_modes(self):
        """create_default_modes should return standard modes."""
        defaults = ModeDistiller.create_default_modes()

        assert len(defaults) == 5
        names = [m.name for m in defaults]
        assert "default" in names
        assert "strict" in names
        assert "minimal" in names
        assert "efficient" in names
        assert "robust" in names

    def test_distill_empty_pareto(self):
        """distill with empty Pareto should return defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")
            distiller = ModeDistiller(library=library)

            modes = distiller.distill([], include_defaults=True)
            assert len(modes) >= 5  # At least defaults

    def test_distill_with_pareto_points(self):
        """distill should create modes from Pareto points."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")
            distiller = ModeDistiller(library=library)

            # Create Pareto points
            points = [
                ParetoPoint(
                    config_vector=VectorCodec.encode(FullConfig()),
                    outcomes={
                        "task_accuracy": 0.9,
                        "token_efficiency": 0.85,
                        "edge_robustness": 0.8,
                        "epistemic_consistency": 0.9,
                    },
                ),
            ]

            modes = distiller.distill(points, include_defaults=False)
            # Should select points for various categories
            assert len(modes) > 0

    def test_distill_adds_to_library(self):
        """distill should add modes to library."""
        with tempfile.TemporaryDirectory() as tmpdir:
            library = ModeLibrary(library_path=Path(tmpdir) / "modes.yaml")
            initial_count = len(library.list_modes())

            distiller = ModeDistiller(library=library)
            distiller.distill([], include_defaults=True)

            # Should have at least defaults
            assert len(library.list_modes()) >= initial_count


class TestFactoryFunctions:
    """Tests for factory functions."""

    def test_create_distiller(self):
        """create_distiller should return distiller."""
        with tempfile.TemporaryDirectory() as tmpdir:
            distiller = create_distiller(library_path=Path(tmpdir) / "modes.yaml")
            assert isinstance(distiller, ModeDistiller)

    def test_load_mode(self):
        """load_mode should load mode by name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "modes.yaml"
            # Initialize library
            ModeLibrary(library_path=path)

            mode = load_mode("default", library_path=path)
            assert mode is not None
            assert mode.name == "default"

    def test_list_modes(self):
        """list_modes should return mode names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "modes.yaml"
            # Initialize library
            ModeLibrary(library_path=path)

            modes = list_modes(library_path=path)
            assert "default" in modes
            assert "strict" in modes
