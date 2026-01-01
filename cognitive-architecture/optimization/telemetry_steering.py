"""
Telemetry-Driven Mode Steering Engine.

FIX-7 from REMEDIATION-PLAN.md (P3):
Creates a feedback loop where telemetry data steers runtime mode selection.

Problem: Telemetry is collected but doesn't steer runtime modes.

Solution:
1. TelemetrySteeringEngine analyzes collected telemetry
2. Calculates Pareto-optimal modes per task domain
3. Provides steering recommendations to ModeSelector
4. ModeSelector uses these recommendations for dynamic adjustment

This creates a closed-loop optimization system where:
- Telemetry records (mode, task_type, outcomes)
- Engine analyzes which modes work best for which domains
- Selector uses analysis to pick optimal modes
- Better outcomes feed back to improve selection
"""

import os
import sys
import json
import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
from enum import Enum
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.dspy_level1 import TelemetryAggregator, TelemetryPoint
from modes.library import Mode, ModeLibrary, ModeType, BUILTIN_MODES
from modes.selector import TaskDomain, TaskComplexity, ModeSelector, TaskContext

logger = logging.getLogger(__name__)


@dataclass
class ModePerformanceRecord:
    """Performance record for a mode in a specific context."""
    mode_name: str
    domain: str
    sample_count: int = 0
    total_accuracy: float = 0.0
    total_efficiency: float = 0.0
    total_consistency: float = 0.0
    last_updated: float = field(default_factory=time.time)

    @property
    def avg_accuracy(self) -> float:
        return self.total_accuracy / self.sample_count if self.sample_count > 0 else 0.0

    @property
    def avg_efficiency(self) -> float:
        return self.total_efficiency / self.sample_count if self.sample_count > 0 else 0.0

    @property
    def avg_consistency(self) -> float:
        return self.total_consistency / self.sample_count if self.sample_count > 0 else 0.0

    def update(self, accuracy: float, efficiency: float, consistency: float):
        """Update with new sample."""
        self.sample_count += 1
        self.total_accuracy += accuracy
        self.total_efficiency += efficiency
        self.total_consistency += consistency
        self.last_updated = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode_name": self.mode_name,
            "domain": self.domain,
            "sample_count": self.sample_count,
            "avg_accuracy": self.avg_accuracy,
            "avg_efficiency": self.avg_efficiency,
            "avg_consistency": self.avg_consistency,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModePerformanceRecord":
        record = cls(
            mode_name=data["mode_name"],
            domain=data["domain"],
            sample_count=data.get("sample_count", 0),
            last_updated=data.get("last_updated", time.time()),
        )
        # Reconstruct totals from averages and count
        if record.sample_count > 0:
            record.total_accuracy = data.get("avg_accuracy", 0.0) * record.sample_count
            record.total_efficiency = data.get("avg_efficiency", 0.0) * record.sample_count
            record.total_consistency = data.get("avg_consistency", 0.0) * record.sample_count
        return record


@dataclass
class ParetoPoint:
    """A point on the Pareto frontier."""
    mode_name: str
    accuracy: float
    efficiency: float
    is_pareto_optimal: bool = False

    def dominates(self, other: "ParetoPoint") -> bool:
        """Check if this point dominates another (better in all dimensions)."""
        return (
            self.accuracy >= other.accuracy and
            self.efficiency >= other.efficiency and
            (self.accuracy > other.accuracy or self.efficiency > other.efficiency)
        )


@dataclass
class SteeringRecommendation:
    """A recommendation from the steering engine."""
    mode_name: str
    confidence: float  # 0.0 - 1.0
    reasons: List[str]
    pareto_rank: int = 0  # 0 = Pareto optimal, higher = worse
    expected_accuracy: float = 0.0
    expected_efficiency: float = 0.0


class TelemetrySteeringEngine:
    """
    Analyzes telemetry to steer mode selection.

    Uses collected performance data to:
    1. Track mode performance per domain
    2. Calculate Pareto-optimal frontiers
    3. Provide steering recommendations

    The engine maintains a performance database that maps
    (mode, domain) -> performance metrics.
    """

    # Minimum samples before trusting a mode's performance
    MIN_SAMPLES_FOR_TRUST = 5

    # Decay factor for old data (per day)
    TIME_DECAY_FACTOR = 0.95

    # Weight for different objectives in scoring
    OBJECTIVE_WEIGHTS = {
        "accuracy": 0.5,
        "efficiency": 0.3,
        "consistency": 0.2,
    }

    def __init__(
        self,
        telemetry: Optional[TelemetryAggregator] = None,
        storage_dir: Optional[Path] = None,
    ):
        """
        Initialize steering engine.

        Args:
            telemetry: Telemetry aggregator for data access
            storage_dir: Directory for performance database
        """
        self.telemetry = telemetry or TelemetryAggregator()

        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / "storage" / "steering"
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Performance database: (mode_name, domain) -> record
        self._performance_db: Dict[Tuple[str, str], ModePerformanceRecord] = {}

        # Pareto frontiers per domain
        self._pareto_frontiers: Dict[str, List[ParetoPoint]] = {}

        # Load existing data
        self._load_performance_db()

    def record_outcome(
        self,
        mode_name: str,
        domain: str,
        accuracy: float,
        efficiency: float,
        consistency: float = 0.5,
    ) -> None:
        """
        Record a mode outcome for steering analysis.

        Args:
            mode_name: Name of the mode used
            domain: Task domain (coding, research, etc.)
            accuracy: Task accuracy (0.0 - 1.0)
            efficiency: Token efficiency (0.0 - 1.0)
            consistency: Epistemic consistency (0.0 - 1.0)
        """
        key = (mode_name, domain)

        if key not in self._performance_db:
            self._performance_db[key] = ModePerformanceRecord(
                mode_name=mode_name,
                domain=domain,
            )

        self._performance_db[key].update(accuracy, efficiency, consistency)

        # Recalculate Pareto frontier for this domain
        self._update_pareto_frontier(domain)

        logger.debug(
            f"Recorded outcome for {mode_name}/{domain}: "
            f"acc={accuracy:.2f}, eff={efficiency:.2f}"
        )

    def ingest_telemetry(self) -> int:
        """
        Ingest telemetry data into performance database.

        Returns:
            Number of points ingested
        """
        points = self.telemetry.get_points()
        ingested = 0

        for point in points:
            # Extract mode from config vector (need to decode)
            # For now, we'll use a heuristic based on config
            mode_name = self._infer_mode_from_vector(point.config_vector)

            # Map task_type to domain
            domain = self._task_type_to_domain(point.task_type)

            # Extract outcomes
            accuracy = point.outcomes.get("task_accuracy", 0.5)
            efficiency = point.outcomes.get("token_efficiency", 0.5)
            consistency = point.outcomes.get("epistemic_consistency", 0.5)

            self.record_outcome(mode_name, domain, accuracy, efficiency, consistency)
            ingested += 1

        return ingested

    def _infer_mode_from_vector(self, vector: List[float]) -> str:
        """Infer mode name from config vector."""
        # Count active frames (indices 0-6)
        active_frame_count = sum(1 for i in range(7) if vector[i] > 0.5)

        # Get strictness level (index 7)
        strictness = int(vector[7]) if len(vector) > 7 else 1

        # Heuristic mode inference
        if active_frame_count <= 1:
            return "minimal"
        elif active_frame_count == 2 and strictness <= 1:
            return "efficient"
        elif strictness >= 2:
            return "strict"
        elif active_frame_count >= 5:
            return "robust"
        else:
            return "balanced"

    def _task_type_to_domain(self, task_type: str) -> str:
        """Map task type to domain string."""
        mapping = {
            "coding": "coding",
            "reasoning": "analysis",
            "analysis": "analysis",
            "creative": "creative",
            "conversational": "support",
            "default": "general",
        }
        return mapping.get(task_type.lower(), "general")

    def _update_pareto_frontier(self, domain: str) -> None:
        """Update Pareto frontier for a domain."""
        # Get all points for this domain
        points = []
        for (mode_name, d), record in self._performance_db.items():
            if d == domain and record.sample_count >= self.MIN_SAMPLES_FOR_TRUST:
                points.append(ParetoPoint(
                    mode_name=mode_name,
                    accuracy=record.avg_accuracy,
                    efficiency=record.avg_efficiency,
                ))

        if not points:
            self._pareto_frontiers[domain] = []
            return

        # Calculate Pareto optimal points
        for p in points:
            p.is_pareto_optimal = not any(
                other.dominates(p) for other in points if other != p
            )

        # Store frontier (Pareto optimal points sorted by accuracy)
        frontier = [p for p in points if p.is_pareto_optimal]
        frontier.sort(key=lambda p: p.accuracy, reverse=True)
        self._pareto_frontiers[domain] = frontier

    def get_steering_recommendation(
        self,
        domain: str,
        prefer_accuracy: bool = True,
    ) -> Optional[SteeringRecommendation]:
        """
        Get steering recommendation for a domain.

        Args:
            domain: Task domain
            prefer_accuracy: If True, prefer accuracy over efficiency

        Returns:
            Steering recommendation or None if insufficient data
        """
        frontier = self._pareto_frontiers.get(domain, [])

        if not frontier:
            # Check if we have any data for this domain
            domain_records = [
                r for (m, d), r in self._performance_db.items()
                if d == domain
            ]

            if not domain_records:
                return None

            # Use best available even if not enough samples
            best = max(domain_records, key=lambda r: r.avg_accuracy)
            return SteeringRecommendation(
                mode_name=best.mode_name,
                confidence=min(0.5, best.sample_count / self.MIN_SAMPLES_FOR_TRUST),
                reasons=["Best available (insufficient data for Pareto analysis)"],
                pareto_rank=1,
                expected_accuracy=best.avg_accuracy,
                expected_efficiency=best.avg_efficiency,
            )

        # Pick from Pareto frontier based on preference
        if prefer_accuracy:
            best = max(frontier, key=lambda p: p.accuracy)
        else:
            best = max(frontier, key=lambda p: p.efficiency)

        # Get the full record for confidence calculation
        key = (best.mode_name, domain)
        record = self._performance_db.get(key)

        if not record:
            return None

        # Calculate confidence based on sample count
        confidence = min(1.0, record.sample_count / (self.MIN_SAMPLES_FOR_TRUST * 4))

        reasons = ["Pareto optimal for this domain"]
        if prefer_accuracy:
            reasons.append(f"Best accuracy: {best.accuracy:.2f}")
        else:
            reasons.append(f"Best efficiency: {best.efficiency:.2f}")

        return SteeringRecommendation(
            mode_name=best.mode_name,
            confidence=confidence,
            reasons=reasons,
            pareto_rank=0,
            expected_accuracy=best.accuracy,
            expected_efficiency=best.efficiency,
        )

    def get_all_recommendations(
        self,
        domain: str,
    ) -> List[SteeringRecommendation]:
        """
        Get all mode recommendations ranked for a domain.

        Args:
            domain: Task domain

        Returns:
            List of recommendations sorted by score
        """
        recommendations = []

        for (mode_name, d), record in self._performance_db.items():
            if d != domain:
                continue

            # Calculate weighted score
            score = (
                self.OBJECTIVE_WEIGHTS["accuracy"] * record.avg_accuracy +
                self.OBJECTIVE_WEIGHTS["efficiency"] * record.avg_efficiency +
                self.OBJECTIVE_WEIGHTS["consistency"] * record.avg_consistency
            )

            # Check Pareto optimality
            frontier = self._pareto_frontiers.get(domain, [])
            pareto_rank = 0 if any(
                p.mode_name == mode_name for p in frontier
            ) else 1

            # Confidence based on samples
            confidence = min(1.0, record.sample_count / (self.MIN_SAMPLES_FOR_TRUST * 4))

            reasons = []
            if pareto_rank == 0:
                reasons.append("Pareto optimal")
            if record.avg_accuracy >= 0.8:
                reasons.append(f"High accuracy: {record.avg_accuracy:.2f}")
            if record.avg_efficiency >= 0.8:
                reasons.append(f"High efficiency: {record.avg_efficiency:.2f}")

            recommendations.append(SteeringRecommendation(
                mode_name=mode_name,
                confidence=confidence,
                reasons=reasons or ["Sufficient data available"],
                pareto_rank=pareto_rank,
                expected_accuracy=record.avg_accuracy,
                expected_efficiency=record.avg_efficiency,
            ))

        # Sort by weighted score (using Pareto rank as tiebreaker)
        recommendations.sort(
            key=lambda r: (
                -r.pareto_rank,
                r.expected_accuracy * 0.6 + r.expected_efficiency * 0.4
            ),
            reverse=True,
        )

        return recommendations

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of performance data."""
        domains = set(d for (_, d) in self._performance_db.keys())

        summary = {
            "total_records": len(self._performance_db),
            "domains": list(domains),
            "pareto_frontiers": {},
            "top_modes_by_domain": {},
        }

        for domain in domains:
            frontier = self._pareto_frontiers.get(domain, [])
            summary["pareto_frontiers"][domain] = [
                {"mode": p.mode_name, "accuracy": p.accuracy, "efficiency": p.efficiency}
                for p in frontier
            ]

            # Get top mode for domain
            recs = self.get_all_recommendations(domain)
            if recs:
                summary["top_modes_by_domain"][domain] = recs[0].mode_name

        return summary

    def _save_performance_db(self) -> None:
        """Save performance database to disk."""
        filepath = self.storage_dir / "performance_db.json"

        data = {
            "records": {
                f"{k[0]}:{k[1]}": v.to_dict()
                for k, v in self._performance_db.items()
            },
            "saved_at": time.time(),
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def _load_performance_db(self) -> None:
        """Load performance database from disk."""
        filepath = self.storage_dir / "performance_db.json"

        if not filepath.exists():
            return

        try:
            with open(filepath) as f:
                data = json.load(f)

            for key_str, record_data in data.get("records", {}).items():
                mode_name, domain = key_str.split(":", 1)
                record = ModePerformanceRecord.from_dict(record_data)
                self._performance_db[(mode_name, domain)] = record

            # Rebuild Pareto frontiers
            domains = set(d for (_, d) in self._performance_db.keys())
            for domain in domains:
                self._update_pareto_frontier(domain)

            logger.info(f"Loaded {len(self._performance_db)} performance records")

        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Could not load performance database: {e}")

    def save(self) -> None:
        """Save all data."""
        self._save_performance_db()


class TelemetryDrivenModeSelector(ModeSelector):
    """
    Mode selector enhanced with telemetry-driven steering.

    Extends ModeSelector to incorporate historical performance data
    when making mode selections.
    """

    def __init__(
        self,
        library: Optional[ModeLibrary] = None,
        steering_engine: Optional[TelemetrySteeringEngine] = None,
        steering_weight: float = 0.3,
    ):
        """
        Initialize telemetry-driven selector.

        Args:
            library: Mode library
            steering_engine: Telemetry steering engine
            steering_weight: Weight for steering recommendations (0.0-1.0)
        """
        super().__init__(library)
        self.steering_engine = steering_engine or TelemetrySteeringEngine()
        self.steering_weight = steering_weight
        self._last_selected_mode: Optional[str] = None
        self._last_domain: Optional[str] = None

    def select(self, context: TaskContext) -> Mode:
        """
        Select best mode using both heuristics and telemetry.

        Args:
            context: Task context

        Returns:
            Selected mode
        """
        # Get heuristic recommendation
        heuristic_recs = self.recommend(context, top_k=3)

        # Get steering recommendation based on domain
        domain = context.domain.value if context.domain else "general"
        steering_rec = self.steering_engine.get_steering_recommendation(domain)

        # If no steering data, use heuristic only
        if not steering_rec or steering_rec.confidence < 0.3:
            selected = heuristic_recs[0].mode if heuristic_recs else self._fallback_mode()
            self._last_selected_mode = selected.name
            self._last_domain = domain
            return selected

        # Combine recommendations
        final_scores: Dict[str, float] = {}

        # Add heuristic scores
        for rec in heuristic_recs:
            final_scores[rec.mode.name] = rec.score * (1 - self.steering_weight)

        # Add steering score
        steering_score = steering_rec.confidence * self.steering_weight
        if steering_rec.mode_name in final_scores:
            final_scores[steering_rec.mode_name] += steering_score
        else:
            final_scores[steering_rec.mode_name] = steering_score

        # Select highest scoring mode
        best_mode_name = max(final_scores.keys(), key=lambda k: final_scores[k])

        # Get the mode object
        mode = self.library.get(best_mode_name)
        if not mode:
            mode = self._fallback_mode()

        self._last_selected_mode = mode.name
        self._last_domain = domain

        logger.info(
            f"Selected mode {mode.name} (heuristic + steering) "
            f"for domain {domain}"
        )

        return mode

    def _fallback_mode(self) -> Mode:
        """Get fallback mode."""
        return self.library.get("balanced") or list(BUILTIN_MODES.values())[0]

    def record_outcome(
        self,
        accuracy: float,
        efficiency: float,
        consistency: float = 0.5,
    ) -> None:
        """
        Record outcome for the last selected mode.

        Call this after task completion to feed back results.

        Args:
            accuracy: Task accuracy (0.0 - 1.0)
            efficiency: Token efficiency (0.0 - 1.0)
            consistency: Epistemic consistency (0.0 - 1.0)
        """
        if self._last_selected_mode and self._last_domain:
            self.steering_engine.record_outcome(
                self._last_selected_mode,
                self._last_domain,
                accuracy,
                efficiency,
                consistency,
            )


# Factory functions

def create_steering_engine(
    telemetry_dir: Optional[Path] = None,
    steering_dir: Optional[Path] = None,
) -> TelemetrySteeringEngine:
    """Create steering engine with optional custom directories."""
    telemetry = TelemetryAggregator(storage_dir=telemetry_dir)
    return TelemetrySteeringEngine(
        telemetry=telemetry,
        storage_dir=steering_dir,
    )


def create_telemetry_driven_selector(
    steering_weight: float = 0.3,
) -> TelemetryDrivenModeSelector:
    """Create telemetry-driven mode selector."""
    return TelemetryDrivenModeSelector(steering_weight=steering_weight)


# Integration with existing mode selector
_steering_engine: Optional[TelemetrySteeringEngine] = None


def get_steering_engine() -> TelemetrySteeringEngine:
    """Get or create the global steering engine."""
    global _steering_engine
    if _steering_engine is None:
        _steering_engine = TelemetrySteeringEngine()
    return _steering_engine


def steer_mode_selection(
    context: TaskContext,
    current_recommendation: str,
) -> Tuple[str, float]:
    """
    Apply telemetry steering to a mode recommendation.

    Args:
        context: Task context
        current_recommendation: Currently recommended mode name

    Returns:
        (mode_name, confidence) - possibly adjusted recommendation
    """
    engine = get_steering_engine()
    domain = context.domain.value if context.domain else "general"

    steering = engine.get_steering_recommendation(domain)

    if steering and steering.confidence > 0.5:
        # Override if steering has high confidence
        return steering.mode_name, steering.confidence

    return current_recommendation, 0.5
