"""
Pareto frontier distillation into named modes.

Converts Pareto-optimal configurations from the Three-MOO Cascade
into human-readable named modes for production use.

Modes:
- strict: Maximum epistemic consistency
- balanced: Good tradeoff across all objectives
- efficient: Optimized for token efficiency
- robust: Optimized for edge case handling
- minimal: Lightweight with few frames
"""

import os
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from enum import Enum
import yaml
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec, VerixStrictness, CompressionLevel
from optimization.globalmoo_client import ParetoPoint


class ModeCategory(Enum):
    """Categories of modes based on optimization focus."""
    STRICT = "strict"
    BALANCED = "balanced"
    EFFICIENT = "efficient"
    ROBUST = "robust"
    MINIMAL = "minimal"
    CUSTOM = "custom"


@dataclass
class NamedMode:
    """A named configuration mode."""

    name: str
    category: ModeCategory
    description: str
    config: FullConfig
    config_vector: List[float]
    expected_outcomes: Dict[str, float]
    use_cases: List[str] = field(default_factory=list)
    version: int = 1
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "config_vector": self.config_vector,
            "expected_outcomes": self.expected_outcomes,
            "use_cases": self.use_cases,
            "version": self.version,
            "created_at": self.created_at,
            "config": {
                "framework": {
                    "evidential": self.config.framework.evidential,
                    "aspectual": self.config.framework.aspectual,
                    "morphological": self.config.framework.morphological,
                    "compositional": self.config.framework.compositional,
                    "honorific": self.config.framework.honorific,
                    "classifier": self.config.framework.classifier,
                    "spatial": self.config.framework.spatial,
                },
                "prompt": {
                    "verix_strictness": self.config.prompt.verix_strictness.value,
                    "compression_level": self.config.prompt.compression_level.value,
                    "require_ground": self.config.prompt.require_ground,
                    "require_confidence": self.config.prompt.require_confidence,
                },
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NamedMode":
        # Reconstruct config
        config = FullConfig()
        if "config" in data:
            fw = data["config"].get("framework", {})
            config.framework.evidential = fw.get("evidential", True)
            config.framework.aspectual = fw.get("aspectual", True)
            config.framework.morphological = fw.get("morphological", False)
            config.framework.compositional = fw.get("compositional", False)
            config.framework.honorific = fw.get("honorific", False)
            config.framework.classifier = fw.get("classifier", False)
            config.framework.spatial = fw.get("spatial", False)

            pr = data["config"].get("prompt", {})
            config.prompt.verix_strictness = VerixStrictness(pr.get("verix_strictness", 1))
            config.prompt.compression_level = CompressionLevel(pr.get("compression_level", 1))
            config.prompt.require_ground = pr.get("require_ground", True)
            config.prompt.require_confidence = pr.get("require_confidence", True)

        return cls(
            name=data["name"],
            category=ModeCategory(data.get("category", "custom")),
            description=data.get("description", ""),
            config=config,
            config_vector=data.get("config_vector", VectorCodec.encode(config)),
            expected_outcomes=data.get("expected_outcomes", {}),
            use_cases=data.get("use_cases", []),
            version=data.get("version", 1),
            created_at=data.get("created_at", time.time()),
        )

    def to_yaml(self) -> str:
        """Convert to YAML format."""
        return yaml.dump(self.to_dict(), default_flow_style=False)


class ModeLibrary:
    """Library of named modes."""

    def __init__(self, library_path: Optional[Path] = None):
        """
        Initialize mode library.

        Args:
            library_path: Path to modes.yaml file
        """
        if library_path is None:
            library_path = Path(__file__).parent.parent / "modes" / "modes.yaml"

        self.library_path = Path(library_path)
        self.library_path.parent.mkdir(parents=True, exist_ok=True)

        self._modes: Dict[str, NamedMode] = {}
        self._load()

    def get(self, name: str) -> Optional[NamedMode]:
        """Get mode by name."""
        return self._modes.get(name)

    def list_modes(self) -> List[str]:
        """List all mode names."""
        return list(self._modes.keys())

    def list_by_category(self, category: ModeCategory) -> List[NamedMode]:
        """List modes by category."""
        return [m for m in self._modes.values() if m.category == category]

    def add(self, mode: NamedMode) -> None:
        """Add or update a mode."""
        self._modes[mode.name] = mode

    def remove(self, name: str) -> bool:
        """Remove a mode. Returns True if found."""
        if name in self._modes:
            del self._modes[name]
            return True
        return False

    def save(self) -> None:
        """Save library to disk."""
        data = {
            "version": "1.0",
            "generated_at": time.time(),
            "modes": {name: mode.to_dict() for name, mode in self._modes.items()},
        }

        with open(self.library_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

    def _load(self) -> None:
        """Load library from disk."""
        if not self.library_path.exists():
            # Create with defaults
            self._create_defaults()
            return

        with open(self.library_path) as f:
            data = yaml.safe_load(f)

        if data and "modes" in data:
            for name, mode_data in data["modes"].items():
                self._modes[name] = NamedMode.from_dict(mode_data)

    def _create_defaults(self) -> None:
        """Create default modes."""
        defaults = ModeDistiller.create_default_modes()
        for mode in defaults:
            self.add(mode)
        self.save()


class ModeDistiller:
    """
    Distill Pareto frontier into named modes.

    Uses clustering and selection heuristics to pick
    representative configurations from the Pareto frontier.
    """

    # Mode selection criteria
    MODE_CRITERIA = {
        ModeCategory.STRICT: {
            "primary": "epistemic_consistency",
            "min_threshold": 0.85,
            "description": "Maximum epistemic consistency with strict VERIX requirements",
        },
        ModeCategory.BALANCED: {
            "primary": None,  # Balanced across all
            "min_threshold": 0.7,
            "description": "Good tradeoff across all objectives",
        },
        ModeCategory.EFFICIENT: {
            "primary": "token_efficiency",
            "min_threshold": 0.85,
            "description": "Optimized for minimal token usage",
        },
        ModeCategory.ROBUST: {
            "primary": "edge_robustness",
            "min_threshold": 0.8,
            "description": "Handles edge cases and adversarial inputs",
        },
        ModeCategory.MINIMAL: {
            "primary": "token_efficiency",
            "max_frames": 2,
            "description": "Lightweight with minimal cognitive frames",
        },
    }

    def __init__(self, library: Optional[ModeLibrary] = None):
        """
        Initialize distiller.

        Args:
            library: Mode library to populate
        """
        self.library = library or ModeLibrary()

    def distill(
        self,
        pareto_points: List[ParetoPoint],
        include_defaults: bool = True,
    ) -> List[NamedMode]:
        """
        Distill Pareto points into named modes.

        Args:
            pareto_points: Pareto-optimal configurations
            include_defaults: Include default modes even if not in Pareto

        Returns:
            List of generated modes
        """
        modes = []

        if include_defaults:
            modes.extend(self.create_default_modes())

        if not pareto_points:
            return modes

        # Select best for each category
        for category in ModeCategory:
            if category == ModeCategory.CUSTOM:
                continue

            criteria = self.MODE_CRITERIA.get(category)
            if not criteria:
                continue

            best_point = self._select_best_for_category(
                pareto_points,
                category,
                criteria,
            )

            if best_point:
                mode = self._create_mode_from_point(
                    best_point,
                    category,
                    criteria["description"],
                )
                modes.append(mode)

        # Add to library
        for mode in modes:
            self.library.add(mode)

        return modes

    def _select_best_for_category(
        self,
        points: List[ParetoPoint],
        category: ModeCategory,
        criteria: Dict[str, Any],
    ) -> Optional[ParetoPoint]:
        """Select best Pareto point for a category."""
        primary = criteria.get("primary")
        min_threshold = criteria.get("min_threshold", 0.0)
        max_frames = criteria.get("max_frames")

        # Filter by constraints
        candidates = []
        for point in points:
            # Check min threshold
            if primary and point.outcomes.get(primary, 0.0) < min_threshold:
                continue

            # Check max frames
            if max_frames:
                config = VectorCodec.decode(point.config_vector)
                if config.framework.frame_count() > max_frames:
                    continue

            candidates.append(point)

        if not candidates:
            return None

        # Select best
        if primary:
            # Best for primary objective
            return max(candidates, key=lambda p: p.outcomes.get(primary, 0.0))
        else:
            # Balanced: best average
            return max(
                candidates,
                key=lambda p: sum(p.outcomes.values()) / len(p.outcomes),
            )

    def _create_mode_from_point(
        self,
        point: ParetoPoint,
        category: ModeCategory,
        description: str,
    ) -> NamedMode:
        """Create named mode from Pareto point."""
        config = VectorCodec.decode(point.config_vector)

        # Generate use cases based on category
        use_cases = self._generate_use_cases(category)

        return NamedMode(
            name=f"{category.value}_v1",
            category=category,
            description=description,
            config=config,
            config_vector=point.config_vector,
            expected_outcomes=point.outcomes,
            use_cases=use_cases,
        )

    def _generate_use_cases(self, category: ModeCategory) -> List[str]:
        """Generate use cases for a category."""
        use_cases = {
            ModeCategory.STRICT: [
                "Academic research requiring rigorous sourcing",
                "Legal document analysis",
                "Medical diagnosis support",
                "Financial compliance reporting",
            ],
            ModeCategory.BALANCED: [
                "General-purpose assistant tasks",
                "Code review and analysis",
                "Technical documentation",
                "Customer support automation",
            ],
            ModeCategory.EFFICIENT: [
                "High-volume API endpoints",
                "Real-time chat applications",
                "Cost-sensitive deployments",
                "Quick summaries and translations",
            ],
            ModeCategory.ROBUST: [
                "User-facing applications with unpredictable input",
                "Security-sensitive contexts",
                "Multi-language support",
                "Error-prone data sources",
            ],
            ModeCategory.MINIMAL: [
                "Embedded systems with limited compute",
                "Simple Q&A tasks",
                "Rapid prototyping",
                "Baseline comparison",
            ],
        }
        return use_cases.get(category, [])

    @staticmethod
    def create_default_modes() -> List[NamedMode]:
        """Create default modes without Pareto optimization."""
        from core.config import STRICT_CONFIG, MINIMAL_CONFIG, DEFAULT_CONFIG

        defaults = []

        # Default balanced mode
        default_config = FullConfig()
        defaults.append(NamedMode(
            name="default",
            category=ModeCategory.BALANCED,
            description="Default balanced configuration",
            config=default_config,
            config_vector=VectorCodec.encode(default_config),
            expected_outcomes={
                "task_accuracy": 0.8,
                "token_efficiency": 0.75,
                "edge_robustness": 0.7,
                "epistemic_consistency": 0.8,
            },
            use_cases=["General-purpose tasks", "Starting point for optimization"],
        ))

        # Strict mode
        defaults.append(NamedMode(
            name="strict",
            category=ModeCategory.STRICT,
            description="Maximum epistemic rigor with all frames and strict VERIX",
            config=STRICT_CONFIG,
            config_vector=VectorCodec.encode(STRICT_CONFIG),
            expected_outcomes={
                "task_accuracy": 0.85,
                "token_efficiency": 0.6,
                "edge_robustness": 0.8,
                "epistemic_consistency": 0.95,
            },
            use_cases=["Academic research", "Legal analysis", "Medical support"],
        ))

        # Minimal mode
        defaults.append(NamedMode(
            name="minimal",
            category=ModeCategory.MINIMAL,
            description="Lightweight with minimal frames and relaxed VERIX",
            config=MINIMAL_CONFIG,
            config_vector=VectorCodec.encode(MINIMAL_CONFIG),
            expected_outcomes={
                "task_accuracy": 0.7,
                "token_efficiency": 0.95,
                "edge_robustness": 0.6,
                "epistemic_consistency": 0.6,
            },
            use_cases=["Quick tasks", "High-volume APIs", "Cost optimization"],
        ))

        # Efficient mode
        efficient_config = FullConfig()
        efficient_config.prompt.compression_level = CompressionLevel.L0_AI_AI
        efficient_config.framework.morphological = False
        efficient_config.framework.compositional = False
        efficient_config.framework.honorific = False
        efficient_config.framework.classifier = False
        efficient_config.framework.spatial = False

        defaults.append(NamedMode(
            name="efficient",
            category=ModeCategory.EFFICIENT,
            description="Optimized for token efficiency with L0 compression",
            config=efficient_config,
            config_vector=VectorCodec.encode(efficient_config),
            expected_outcomes={
                "task_accuracy": 0.75,
                "token_efficiency": 0.9,
                "edge_robustness": 0.65,
                "epistemic_consistency": 0.75,
            },
            use_cases=["High-throughput systems", "Real-time chat", "Cost-sensitive"],
        ))

        # Robust mode
        robust_config = FullConfig()
        robust_config.framework.evidential = True
        robust_config.framework.aspectual = True
        robust_config.framework.compositional = True
        robust_config.prompt.verix_strictness = VerixStrictness.MODERATE
        robust_config.prompt.require_ground = True

        defaults.append(NamedMode(
            name="robust",
            category=ModeCategory.ROBUST,
            description="Optimized for edge case handling",
            config=robust_config,
            config_vector=VectorCodec.encode(robust_config),
            expected_outcomes={
                "task_accuracy": 0.8,
                "token_efficiency": 0.7,
                "edge_robustness": 0.9,
                "epistemic_consistency": 0.85,
            },
            use_cases=["User-facing apps", "Security contexts", "Adversarial inputs"],
        ))

        return defaults


# Factory functions

def create_distiller(library_path: Optional[Path] = None) -> ModeDistiller:
    """Create mode distiller with library."""
    library = ModeLibrary(library_path)
    return ModeDistiller(library)


def load_mode(name: str, library_path: Optional[Path] = None) -> Optional[NamedMode]:
    """Load a mode by name."""
    library = ModeLibrary(library_path)
    return library.get(name)


def list_modes(library_path: Optional[Path] = None) -> List[str]:
    """List all available modes."""
    library = ModeLibrary(library_path)
    return library.list_modes()
