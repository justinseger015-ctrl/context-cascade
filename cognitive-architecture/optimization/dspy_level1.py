"""
DSPy Level 1: Monthly structural evolution.

Cadence: Monthly
Scope: Analyze aggregated telemetry, propose structural changes

This layer analyzes optimization results over time and proposes
structural improvements to the prompt architecture itself.
"""

import os
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from enum import Enum
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec


class ProposalType(Enum):
    """Types of evolution proposals."""
    FRAME_ACTIVATION = "frame_activation"  # Change default frames
    VERIX_ADJUSTMENT = "verix_adjustment"  # Change VERIX defaults
    PROMPT_STRUCTURE = "prompt_structure"  # Change prompt template
    COMPRESSION_LEVEL = "compression_level"  # Change compression default
    NEW_FRAME = "new_frame"  # Propose new cognitive frame


class ProposalStatus(Enum):
    """Status of evolution proposal."""
    PROPOSED = "proposed"
    TESTING = "testing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class TelemetryPoint:
    """A single telemetry data point."""
    config_vector: List[float]
    outcomes: Dict[str, float]
    task_type: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvolutionProposal:
    """A proposed structural change."""

    proposal_id: str
    proposal_type: ProposalType
    description: str
    rationale: str
    changes: Dict[str, Any]
    expected_impact: Dict[str, float]
    status: ProposalStatus = ProposalStatus.PROPOSED
    created_at: float = field(default_factory=time.time)
    test_results: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "proposal_type": self.proposal_type.value,
            "description": self.description,
            "rationale": self.rationale,
            "changes": self.changes,
            "expected_impact": self.expected_impact,
            "status": self.status.value,
            "created_at": self.created_at,
            "test_results": self.test_results,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvolutionProposal":
        return cls(
            proposal_id=data["proposal_id"],
            proposal_type=ProposalType(data["proposal_type"]),
            description=data["description"],
            rationale=data["rationale"],
            changes=data["changes"],
            expected_impact=data["expected_impact"],
            status=ProposalStatus(data.get("status", "proposed")),
            created_at=data.get("created_at", time.time()),
            test_results=data.get("test_results"),
        )


class TelemetryAggregator:
    """Aggregate telemetry data for analysis."""

    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize aggregator.

        Args:
            storage_dir: Directory for telemetry storage
        """
        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / "storage" / "telemetry"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._points: List[TelemetryPoint] = []

    def record(self, point: TelemetryPoint) -> None:
        """Record a telemetry point."""
        self._points.append(point)

    def record_outcome(
        self,
        config_vector: List[float],
        outcomes: Dict[str, float],
        task_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an evaluation outcome."""
        point = TelemetryPoint(
            config_vector=config_vector,
            outcomes=outcomes,
            task_type=task_type,
            timestamp=time.time(),
            metadata=metadata or {},
        )
        self.record(point)

    def get_points(
        self,
        since: Optional[float] = None,
        task_type: Optional[str] = None,
    ) -> List[TelemetryPoint]:
        """
        Get telemetry points with optional filtering.

        Args:
            since: Only points after this timestamp
            task_type: Only points for this task type
        """
        points = self._points

        if since is not None:
            points = [p for p in points if p.timestamp >= since]

        if task_type is not None:
            points = [p for p in points if p.task_type == task_type]

        return points

    def aggregate_by_cluster(self) -> Dict[str, Dict[str, float]]:
        """
        Aggregate outcomes by cluster key.

        Returns:
            Dict mapping cluster_key -> average outcomes
        """
        clusters: Dict[str, List[Dict[str, float]]] = {}

        for point in self._points:
            config = VectorCodec.decode(point.config_vector)
            cluster_key = VectorCodec.cluster_key(config)

            if cluster_key not in clusters:
                clusters[cluster_key] = []
            clusters[cluster_key].append(point.outcomes)

        # Average outcomes per cluster
        aggregated = {}
        for cluster_key, outcome_list in clusters.items():
            if not outcome_list:
                continue

            avg_outcomes = {}
            for key in outcome_list[0].keys():
                values = [o.get(key, 0.0) for o in outcome_list]
                avg_outcomes[key] = sum(values) / len(values)

            aggregated[cluster_key] = avg_outcomes

        return aggregated

    def aggregate_by_frame(self) -> Dict[str, Dict[str, float]]:
        """
        Aggregate outcomes by frame activation.

        Returns:
            Dict mapping frame_name -> average outcomes when activated
        """
        frame_names = [
            "evidential", "aspectual", "morphological",
            "compositional", "honorific", "classifier", "spatial"
        ]

        frame_outcomes: Dict[str, List[Dict[str, float]]] = {
            f: [] for f in frame_names
        }

        for point in self._points:
            config = VectorCodec.decode(point.config_vector)

            # Check each frame
            for i, frame in enumerate(frame_names):
                is_active = point.config_vector[i] > 0.5
                if is_active:
                    frame_outcomes[frame].append(point.outcomes)

        # Average per frame
        aggregated = {}
        for frame, outcome_list in frame_outcomes.items():
            if not outcome_list:
                continue

            avg_outcomes = {}
            for key in outcome_list[0].keys():
                values = [o.get(key, 0.0) for o in outcome_list]
                avg_outcomes[key] = sum(values) / len(values)

            aggregated[frame] = avg_outcomes

        return aggregated

    def save(self, filename: str = "telemetry.jsonl") -> int:
        """Save telemetry to disk. Returns point count."""
        filepath = self.storage_dir / filename

        with open(filepath, "w") as f:
            for point in self._points:
                data = {
                    "config_vector": point.config_vector,
                    "outcomes": point.outcomes,
                    "task_type": point.task_type,
                    "timestamp": point.timestamp,
                    "metadata": point.metadata,
                }
                f.write(json.dumps(data) + "\n")

        return len(self._points)

    def load(self, filename: str = "telemetry.jsonl") -> int:
        """Load telemetry from disk. Returns point count."""
        filepath = self.storage_dir / filename

        if not filepath.exists():
            return 0

        self._points = []
        with open(filepath) as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    point = TelemetryPoint(
                        config_vector=data["config_vector"],
                        outcomes=data["outcomes"],
                        task_type=data["task_type"],
                        timestamp=data["timestamp"],
                        metadata=data.get("metadata", {}),
                    )
                    self._points.append(point)

        return len(self._points)


class DSPyLevel1Analyzer:
    """
    Level 1 structural evolution analyzer.

    Analyzes aggregated telemetry to propose structural improvements
    to the prompt architecture.
    """

    def __init__(
        self,
        telemetry: Optional[TelemetryAggregator] = None,
        proposals_dir: Optional[Path] = None,
    ):
        """
        Initialize L1 analyzer.

        Args:
            telemetry: Telemetry aggregator
            proposals_dir: Directory for proposals
        """
        self.telemetry = telemetry or TelemetryAggregator()

        if proposals_dir is None:
            proposals_dir = Path(__file__).parent.parent / "storage" / "proposals"

        self.proposals_dir = Path(proposals_dir)
        self.proposals_dir.mkdir(parents=True, exist_ok=True)

        self._proposals: List[EvolutionProposal] = []
        self._proposal_counter = 0

    def analyze(self, min_samples: int = 50) -> List[EvolutionProposal]:
        """
        Analyze telemetry and generate proposals.

        Args:
            min_samples: Minimum samples needed for analysis

        Returns:
            List of generated proposals
        """
        points = self.telemetry.get_points()

        if len(points) < min_samples:
            return []

        proposals = []

        # Analyze frame effectiveness
        frame_proposals = self._analyze_frames()
        proposals.extend(frame_proposals)

        # Analyze VERIX strictness impact
        verix_proposals = self._analyze_verix()
        proposals.extend(verix_proposals)

        # Analyze compression level impact
        compression_proposals = self._analyze_compression()
        proposals.extend(compression_proposals)

        self._proposals.extend(proposals)
        return proposals

    def _analyze_frames(self) -> List[EvolutionProposal]:
        """Analyze frame activation patterns."""
        proposals = []
        frame_data = self.telemetry.aggregate_by_frame()

        if not frame_data:
            return proposals

        # Find underperforming frames
        for frame, outcomes in frame_data.items():
            avg_accuracy = outcomes.get("task_accuracy", 0.5)

            if avg_accuracy < 0.6:
                self._proposal_counter += 1
                proposal = EvolutionProposal(
                    proposal_id=f"L1-{self._proposal_counter:04d}",
                    proposal_type=ProposalType.FRAME_ACTIVATION,
                    description=f"Disable {frame} frame by default",
                    rationale=f"Frame shows low average accuracy ({avg_accuracy:.2f})",
                    changes={
                        "frame": frame,
                        "default_enabled": False,
                    },
                    expected_impact={
                        "task_accuracy": 0.05,
                        "token_efficiency": 0.02,
                    },
                )
                proposals.append(proposal)

        return proposals

    def _analyze_verix(self) -> List[EvolutionProposal]:
        """Analyze VERIX strictness impact."""
        proposals = []
        cluster_data = self.telemetry.aggregate_by_cluster()

        if not cluster_data:
            return proposals

        # Group by VERIX strictness level
        strictness_outcomes: Dict[int, List[Dict[str, float]]] = {0: [], 1: [], 2: []}

        for point in self.telemetry.get_points():
            strictness = int(point.config_vector[7])  # Index 7 = verix_strictness
            if strictness in strictness_outcomes:
                strictness_outcomes[strictness].append(point.outcomes)

        # Analyze each level
        best_strictness = 1  # Default
        best_avg = 0.0

        for strictness, outcomes in strictness_outcomes.items():
            if not outcomes:
                continue

            avg_consistency = sum(o.get("epistemic_consistency", 0.0) for o in outcomes) / len(outcomes)

            if avg_consistency > best_avg:
                best_avg = avg_consistency
                best_strictness = strictness

        if best_strictness != 1:  # Not the current default
            self._proposal_counter += 1
            proposal = EvolutionProposal(
                proposal_id=f"L1-{self._proposal_counter:04d}",
                proposal_type=ProposalType.VERIX_ADJUSTMENT,
                description=f"Change default VERIX strictness to {best_strictness}",
                rationale=f"Strictness {best_strictness} shows best consistency ({best_avg:.2f})",
                changes={
                    "verix_strictness": best_strictness,
                },
                expected_impact={
                    "epistemic_consistency": best_avg - 0.5,
                },
            )
            proposals.append(proposal)

        return proposals

    def _analyze_compression(self) -> List[EvolutionProposal]:
        """Analyze compression level impact."""
        proposals = []

        compression_outcomes: Dict[int, List[Dict[str, float]]] = {0: [], 1: [], 2: []}

        for point in self.telemetry.get_points():
            compression = int(point.config_vector[8])  # Index 8 = compression_level
            if compression in compression_outcomes:
                compression_outcomes[compression].append(point.outcomes)

        # Find best for token efficiency
        best_compression = 1
        best_efficiency = 0.0

        for compression, outcomes in compression_outcomes.items():
            if not outcomes:
                continue

            avg_efficiency = sum(o.get("token_efficiency", 0.0) for o in outcomes) / len(outcomes)

            if avg_efficiency > best_efficiency:
                best_efficiency = avg_efficiency
                best_compression = compression

        if best_compression != 1 and best_efficiency > 0.7:
            self._proposal_counter += 1
            proposal = EvolutionProposal(
                proposal_id=f"L1-{self._proposal_counter:04d}",
                proposal_type=ProposalType.COMPRESSION_LEVEL,
                description=f"Change default compression to L{best_compression}",
                rationale=f"L{best_compression} shows best efficiency ({best_efficiency:.2f})",
                changes={
                    "compression_level": best_compression,
                },
                expected_impact={
                    "token_efficiency": best_efficiency - 0.5,
                },
            )
            proposals.append(proposal)

        return proposals

    def get_proposals(
        self,
        status: Optional[ProposalStatus] = None,
    ) -> List[EvolutionProposal]:
        """Get proposals with optional status filter."""
        if status is None:
            return self._proposals

        return [p for p in self._proposals if p.status == status]

    def accept_proposal(self, proposal_id: str) -> bool:
        """Accept a proposal. Returns True if found."""
        for proposal in self._proposals:
            if proposal.proposal_id == proposal_id:
                proposal.status = ProposalStatus.ACCEPTED
                return True
        return False

    def reject_proposal(self, proposal_id: str) -> bool:
        """Reject a proposal. Returns True if found."""
        for proposal in self._proposals:
            if proposal.proposal_id == proposal_id:
                proposal.status = ProposalStatus.REJECTED
                return True
        return False

    def save_proposals(self, filename: str = "proposals.json") -> int:
        """Save proposals to disk. Returns count."""
        filepath = self.proposals_dir / filename

        with open(filepath, "w") as f:
            json.dump(
                [p.to_dict() for p in self._proposals],
                f,
                indent=2,
            )

        return len(self._proposals)

    def load_proposals(self, filename: str = "proposals.json") -> int:
        """Load proposals from disk. Returns count."""
        filepath = self.proposals_dir / filename

        if not filepath.exists():
            return 0

        with open(filepath) as f:
            data = json.load(f)
            self._proposals = [EvolutionProposal.from_dict(p) for p in data]

        return len(self._proposals)


# Factory functions

def create_l1_analyzer(
    telemetry_dir: Optional[Path] = None,
    proposals_dir: Optional[Path] = None,
) -> DSPyLevel1Analyzer:
    """Create L1 analyzer with default settings."""
    telemetry = TelemetryAggregator(storage_dir=telemetry_dir)
    return DSPyLevel1Analyzer(
        telemetry=telemetry,
        proposals_dir=proposals_dir,
    )
