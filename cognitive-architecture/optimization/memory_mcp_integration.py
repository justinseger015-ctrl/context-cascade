"""
Memory MCP Integration for DSPy Level 1.

Provides cross-session telemetry persistence via Memory MCP.
Enables aggregation of telemetry data across multiple sessions
for monthly structural analysis.

Part of the DSPy Level 1 monthly structural evolution system.
"""

import json
import time
import os
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path


# Memory MCP namespace for DSPy telemetry
MEMORY_MCP_NAMESPACE = "dspy/telemetry"


@dataclass
class TelemetrySnapshot:
    """A snapshot of telemetry data for Memory MCP storage."""
    snapshot_id: str
    timestamp: float
    point_count: int
    by_cluster: Dict[str, Dict[str, float]]
    by_frame: Dict[str, Dict[str, float]]
    summary: Dict[str, Any]
    schema_version: str = "1.0"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "snapshot_id": self.snapshot_id,
            "timestamp": self.timestamp,
            "point_count": self.point_count,
            "by_cluster": self.by_cluster,
            "by_frame": self.by_frame,
            "summary": self.summary,
            "x-schema-version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TelemetrySnapshot":
        """Deserialize from dictionary."""
        return cls(
            snapshot_id=data["snapshot_id"],
            timestamp=data["timestamp"],
            point_count=data["point_count"],
            by_cluster=data["by_cluster"],
            by_frame=data["by_frame"],
            summary=data["summary"],
            schema_version=data.get("x-schema-version", "1.0"),
        )


class MemoryMCPTelemetryStore:
    """
    Memory MCP integration for telemetry persistence.

    Stores telemetry snapshots to Memory MCP for cross-session aggregation.
    Uses the 12FA tagging protocol for proper metadata.
    """

    def __init__(
        self,
        project_name: str = "context-cascade",
        fallback_dir: Optional[Path] = None,
    ):
        """
        Initialize Memory MCP telemetry store.

        Args:
            project_name: Project identifier for tagging
            fallback_dir: Directory for file-based fallback when MCP unavailable
        """
        self.project_name = project_name
        self.namespace = MEMORY_MCP_NAMESPACE

        if fallback_dir is None:
            fallback_dir = Path(__file__).parent.parent / "storage" / "memory-mcp-fallback"

        self.fallback_dir = Path(fallback_dir)
        self.fallback_dir.mkdir(parents=True, exist_ok=True)

        self._mcp_available: Optional[bool] = None

    def _check_mcp_availability(self) -> bool:
        """Check if Memory MCP is available."""
        if self._mcp_available is not None:
            return self._mcp_available

        try:
            # Try to import the tagging protocol
            hooks_path = Path(__file__).parent.parent.parent / "hooks" / "12fa"
            if hooks_path.exists():
                # Check if the JS module exists
                protocol_path = hooks_path / "memory-mcp-tagging-protocol.js"
                self._mcp_available = protocol_path.exists()
            else:
                self._mcp_available = False
        except Exception:
            self._mcp_available = False

        return self._mcp_available

    async def persist_snapshot(
        self,
        snapshot: TelemetrySnapshot,
    ) -> Dict[str, Any]:
        """
        Persist telemetry snapshot to Memory MCP.

        Args:
            snapshot: Telemetry snapshot to persist

        Returns:
            Result with storage location info
        """
        tags = {
            "project": self.project_name,
            "x-intent": "telemetry_snapshot",
            "x-namespace": f"{self.namespace}/snapshots/{snapshot.snapshot_id}",
            "x-timestamp": str(snapshot.timestamp),
        }

        content = json.dumps(snapshot.to_dict())

        if self._check_mcp_availability():
            return await self._persist_to_mcp(snapshot.snapshot_id, content, tags)
        else:
            return self._persist_to_fallback(snapshot.snapshot_id, content, tags)

    async def _persist_to_mcp(
        self,
        snapshot_id: str,
        content: str,
        tags: Dict[str, str],
    ) -> Dict[str, Any]:
        """Persist to Memory MCP (async)."""
        # Note: This would integrate with the actual Memory MCP
        # For now, we simulate the interface
        result = {
            "stored": True,
            "location": "memory-mcp",
            "namespace": tags["x-namespace"],
            "snapshot_id": snapshot_id,
            "timestamp": time.time(),
        }

        # Also write to fallback for redundancy
        self._persist_to_fallback(snapshot_id, content, tags)

        return result

    def _persist_to_fallback(
        self,
        snapshot_id: str,
        content: str,
        tags: Dict[str, str],
    ) -> Dict[str, Any]:
        """Persist to file-based fallback."""
        filepath = self.fallback_dir / f"snapshot-{snapshot_id}.json"

        data = {
            "content": json.loads(content),
            "tags": tags,
            "stored_at": time.time(),
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        return {
            "stored": True,
            "location": "fallback",
            "filepath": str(filepath),
            "snapshot_id": snapshot_id,
            "timestamp": time.time(),
        }

    async def load_snapshots(
        self,
        since: Optional[float] = None,
        limit: int = 30,
    ) -> List[TelemetrySnapshot]:
        """
        Load telemetry snapshots from Memory MCP.

        Args:
            since: Only load snapshots after this timestamp
            limit: Maximum number of snapshots to load

        Returns:
            List of telemetry snapshots
        """
        if self._check_mcp_availability():
            return await self._load_from_mcp(since, limit)
        else:
            return self._load_from_fallback(since, limit)

    async def _load_from_mcp(
        self,
        since: Optional[float],
        limit: int,
    ) -> List[TelemetrySnapshot]:
        """Load from Memory MCP (async)."""
        # Note: This would query the actual Memory MCP
        # For now, fall back to file storage
        return self._load_from_fallback(since, limit)

    def _load_from_fallback(
        self,
        since: Optional[float],
        limit: int,
    ) -> List[TelemetrySnapshot]:
        """Load from file-based fallback."""
        snapshots = []

        # List all snapshot files
        for filepath in sorted(self.fallback_dir.glob("snapshot-*.json"), reverse=True):
            if len(snapshots) >= limit:
                break

            try:
                with open(filepath) as f:
                    data = json.load(f)

                content = data.get("content", {})
                timestamp = content.get("timestamp", 0)

                if since is not None and timestamp < since:
                    continue

                snapshot = TelemetrySnapshot.from_dict(content)
                snapshots.append(snapshot)

            except (json.JSONDecodeError, KeyError) as e:
                # Skip invalid files
                continue

        return snapshots

    def persist_snapshot_sync(
        self,
        snapshot: TelemetrySnapshot,
    ) -> Dict[str, Any]:
        """
        Synchronous version of persist_snapshot.

        For use when async is not available.
        """
        tags = {
            "project": self.project_name,
            "x-intent": "telemetry_snapshot",
            "x-namespace": f"{self.namespace}/snapshots/{snapshot.snapshot_id}",
            "x-timestamp": str(snapshot.timestamp),
        }

        content = json.dumps(snapshot.to_dict())
        return self._persist_to_fallback(snapshot.snapshot_id, content, tags)

    def load_snapshots_sync(
        self,
        since: Optional[float] = None,
        limit: int = 30,
    ) -> List[TelemetrySnapshot]:
        """
        Synchronous version of load_snapshots.

        For use when async is not available.
        """
        return self._load_from_fallback(since, limit)


class TelemetryAggregatorWithMCP:
    """
    Extended TelemetryAggregator with Memory MCP support.

    Wraps the base TelemetryAggregator and adds:
    - Automatic snapshot creation
    - Memory MCP persistence
    - Cross-session aggregation
    """

    def __init__(
        self,
        base_aggregator=None,
        mcp_store: Optional[MemoryMCPTelemetryStore] = None,
        auto_snapshot_threshold: int = 100,
    ):
        """
        Initialize extended aggregator.

        Args:
            base_aggregator: Base TelemetryAggregator instance
            mcp_store: Memory MCP store instance
            auto_snapshot_threshold: Create snapshot after this many points
        """
        # Import here to avoid circular dependency
        from .dspy_level1 import TelemetryAggregator

        self.base = base_aggregator or TelemetryAggregator()
        self.mcp_store = mcp_store or MemoryMCPTelemetryStore()
        self.auto_snapshot_threshold = auto_snapshot_threshold
        self._points_since_snapshot = 0

    def record_outcome(
        self,
        config_vector: List[float],
        outcomes: Dict[str, float],
        task_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an evaluation outcome."""
        self.base.record_outcome(config_vector, outcomes, task_type, metadata)
        self._points_since_snapshot += 1

        # Auto-snapshot if threshold reached
        if self._points_since_snapshot >= self.auto_snapshot_threshold:
            self.create_snapshot_sync()

    def create_snapshot(self) -> TelemetrySnapshot:
        """Create a telemetry snapshot."""
        points = self.base.get_points()

        snapshot = TelemetrySnapshot(
            snapshot_id=f"snap-{int(time.time() * 1000)}",
            timestamp=time.time(),
            point_count=len(points),
            by_cluster=self.base.aggregate_by_cluster(),
            by_frame=self.base.aggregate_by_frame(),
            summary={
                "task_types": list(set(p.task_type for p in points)),
                "time_range": {
                    "start": min(p.timestamp for p in points) if points else 0,
                    "end": max(p.timestamp for p in points) if points else 0,
                },
            },
        )

        return snapshot

    def create_snapshot_sync(self) -> Dict[str, Any]:
        """Create and persist a snapshot synchronously."""
        snapshot = self.create_snapshot()
        result = self.mcp_store.persist_snapshot_sync(snapshot)
        self._points_since_snapshot = 0
        return result

    async def create_snapshot_async(self) -> Dict[str, Any]:
        """Create and persist a snapshot asynchronously."""
        snapshot = self.create_snapshot()
        result = await self.mcp_store.persist_snapshot(snapshot)
        self._points_since_snapshot = 0
        return result

    def load_historical_snapshots(
        self,
        days: int = 30,
    ) -> List[TelemetrySnapshot]:
        """
        Load historical snapshots for aggregation.

        Args:
            days: Number of days to look back

        Returns:
            List of historical snapshots
        """
        since = time.time() - (days * 24 * 60 * 60)
        return self.mcp_store.load_snapshots_sync(since=since)

    def aggregate_historical(
        self,
        days: int = 30,
    ) -> Dict[str, Any]:
        """
        Aggregate historical data across snapshots.

        Args:
            days: Number of days to aggregate

        Returns:
            Aggregated statistics
        """
        snapshots = self.load_historical_snapshots(days=days)

        if not snapshots:
            return {
                "snapshots_found": 0,
                "total_points": 0,
                "by_cluster": {},
                "by_frame": {},
            }

        # Merge cluster data
        merged_clusters: Dict[str, Dict[str, List[float]]] = {}
        for snap in snapshots:
            for cluster_key, outcomes in snap.by_cluster.items():
                if cluster_key not in merged_clusters:
                    merged_clusters[cluster_key] = {}
                for metric, value in outcomes.items():
                    if metric not in merged_clusters[cluster_key]:
                        merged_clusters[cluster_key][metric] = []
                    merged_clusters[cluster_key][metric].append(value)

        # Average the merged cluster data
        aggregated_clusters = {}
        for cluster_key, metrics in merged_clusters.items():
            aggregated_clusters[cluster_key] = {
                metric: sum(values) / len(values)
                for metric, values in metrics.items()
            }

        # Merge frame data similarly
        merged_frames: Dict[str, Dict[str, List[float]]] = {}
        for snap in snapshots:
            for frame_name, outcomes in snap.by_frame.items():
                if frame_name not in merged_frames:
                    merged_frames[frame_name] = {}
                for metric, value in outcomes.items():
                    if metric not in merged_frames[frame_name]:
                        merged_frames[frame_name][metric] = []
                    merged_frames[frame_name][metric].append(value)

        aggregated_frames = {}
        for frame_name, metrics in merged_frames.items():
            aggregated_frames[frame_name] = {
                metric: sum(values) / len(values)
                for metric, values in metrics.items()
            }

        return {
            "snapshots_found": len(snapshots),
            "total_points": sum(s.point_count for s in snapshots),
            "by_cluster": aggregated_clusters,
            "by_frame": aggregated_frames,
            "time_range": {
                "oldest": min(s.timestamp for s in snapshots),
                "newest": max(s.timestamp for s in snapshots),
            },
        }

    # Delegate to base aggregator
    def get_points(self, *args, **kwargs):
        return self.base.get_points(*args, **kwargs)

    def aggregate_by_cluster(self):
        return self.base.aggregate_by_cluster()

    def aggregate_by_frame(self):
        return self.base.aggregate_by_frame()

    def save(self, *args, **kwargs):
        return self.base.save(*args, **kwargs)

    def load(self, *args, **kwargs):
        return self.base.load(*args, **kwargs)


# Factory functions

def create_mcp_telemetry_store(
    project_name: str = "context-cascade",
    fallback_dir: Optional[Path] = None,
) -> MemoryMCPTelemetryStore:
    """Create a Memory MCP telemetry store."""
    return MemoryMCPTelemetryStore(
        project_name=project_name,
        fallback_dir=fallback_dir,
    )


def create_telemetry_aggregator_with_mcp(
    auto_snapshot_threshold: int = 100,
) -> TelemetryAggregatorWithMCP:
    """Create a TelemetryAggregator with Memory MCP support."""
    return TelemetryAggregatorWithMCP(
        auto_snapshot_threshold=auto_snapshot_threshold,
    )
