"""
Telemetry schema for cognitive architecture execution data v3.0.

Captures real-world execution data for:
- Layer 2 optimization (per-task prompt caching)
- Layer 1 optimization (3-day language evolution)

Data flows:
  Hook captures -> Memory MCP -> Aggregator -> Dual MOO -> Named Modes

v3.0: Uses x- prefixed custom fields for Anthropic compliance
- agent_type -> x-agent-type (in serialized output)
- skill_name -> x-skill-name (in serialized output)
- command_name -> x-command-name (in serialized output)
- Backward compatibility maintained for reading old format
"""

import os
import sys
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TaskType(Enum):
    """Types of tasks for mode selection."""
    EXPLANATION = "explanation"
    DEBUGGING = "debugging"
    IMPLEMENTATION = "implementation"
    REVIEW = "review"
    RESEARCH = "research"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    GENERAL = "general"


class OutcomeSignal(Enum):
    """How we determine task success."""
    USER_ACCEPTED = "user_accepted"      # User didn't ask for redo
    TESTS_PASSED = "tests_passed"        # Downstream tests passed
    USER_RATING = "user_rating"          # Explicit 1-5 rating
    FOLLOW_UP = "follow_up_needed"       # User asked clarification
    UNKNOWN = "unknown"                  # No signal yet


@dataclass
class ExecutionTelemetry:
    """
    Complete telemetry record for a single task execution.

    Captured by hooks and stored in memory-mcp for aggregation.
    """
    # Identity
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    session_id: Optional[str] = None

    # INPUT: Configuration used
    config_vector: List[float] = field(default_factory=list)  # 14-dim from VectorCodec
    active_frames: List[str] = field(default_factory=list)    # ["evidential", "aspectual", ...]
    verix_strictness: int = 1                                  # 0=RELAXED, 1=MODERATE, 2=STRICT
    compression_level: int = 1                                 # 0=L0, 1=L1, 2=L2

    # INPUT: Task metadata
    task_type: str = "general"
    task_prompt_hash: str = ""           # Hash of prompt for dedup
    task_prompt_length: int = 0

    # OUTPUT: Response metrics
    response_tokens: int = 0
    response_length: int = 0
    latency_ms: int = 0

    # OUTPUT: Frame compliance scores (0.0 - 1.0)
    frame_scores: Dict[str, float] = field(default_factory=dict)
    aggregate_frame_score: float = 0.0

    # OUTPUT: VERIX metrics
    verix_claims_count: int = 0
    verix_grounded_claims: int = 0
    verix_compliance_score: float = 0.0

    # OUTCOME: Success signals
    outcome_signal: str = "unknown"
    task_success: Optional[bool] = None
    user_rating: Optional[int] = None    # 1-5 if provided
    follow_up_needed: bool = False
    error_occurred: bool = False
    error_message: Optional[str] = None

    # Metadata
    agent_type: Optional[str] = None
    skill_name: Optional[str] = None
    command_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        v3.0: Outputs x- prefixed custom fields for Anthropic compliance.
        """
        base = asdict(self)

        # v3.0: Convert custom metadata fields to x- prefix format
        result = {}
        for key, value in base.items():
            if key in ('agent_type', 'skill_name', 'command_name'):
                # Custom metadata fields use x- prefix
                result[f'x-{key.replace("_", "-")}'] = value
            else:
                result[key] = value

        # Add schema version marker
        result['_schema_version'] = '3.0'
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionTelemetry":
        """Create from dictionary.

        v3.0: Supports both old format and new x- prefixed format.
        """
        # Normalize x- prefixed fields back to internal format
        normalized = {}
        for key, value in data.items():
            if key.startswith('x-'):
                # Convert x-agent-type -> agent_type
                internal_key = key[2:].replace('-', '_')
                normalized[internal_key] = value
            elif key == '_schema_version':
                # Skip schema version marker
                continue
            else:
                normalized[key] = value

        return cls(**{k: v for k, v in normalized.items() if k in cls.__dataclass_fields__})

    def memory_key(self) -> str:
        """Generate memory-mcp key for this record."""
        date = self.timestamp[:10]  # YYYY-MM-DD
        return f"telemetry/executions/{date}/{self.task_id}"


@dataclass
class TelemetryBatch:
    """Batch of telemetry records for aggregation."""
    records: List[ExecutionTelemetry] = field(default_factory=list)
    start_date: str = ""
    end_date: str = ""

    def add(self, record: ExecutionTelemetry) -> None:
        """Add a record to the batch."""
        self.records.append(record)
        if not self.start_date or record.timestamp < self.start_date:
            self.start_date = record.timestamp
        if not self.end_date or record.timestamp > self.end_date:
            self.end_date = record.timestamp

    def filter_by_task_type(self, task_type: str) -> List[ExecutionTelemetry]:
        """Get records for a specific task type."""
        return [r for r in self.records if r.task_type == task_type]

    def filter_successful(self) -> List[ExecutionTelemetry]:
        """Get only successful executions."""
        return [r for r in self.records if r.task_success is True]

    def compute_statistics(self) -> Dict[str, Any]:
        """Compute aggregate statistics for MOO objectives."""
        if not self.records:
            return {}

        successful = self.filter_successful()

        return {
            "total_records": len(self.records),
            "successful_records": len(successful),
            "success_rate": len(successful) / len(self.records) if self.records else 0,
            "avg_frame_score": sum(r.aggregate_frame_score for r in self.records) / len(self.records),
            "avg_verix_compliance": sum(r.verix_compliance_score for r in self.records) / len(self.records),
            "avg_response_tokens": sum(r.response_tokens for r in self.records) / len(self.records),
            "avg_latency_ms": sum(r.latency_ms for r in self.records) / len(self.records),
            "task_type_distribution": self._task_type_distribution(),
            "frame_usage": self._frame_usage(),
        }

    def _task_type_distribution(self) -> Dict[str, int]:
        """Count records by task type."""
        dist = {}
        for r in self.records:
            dist[r.task_type] = dist.get(r.task_type, 0) + 1
        return dist

    def _frame_usage(self) -> Dict[str, int]:
        """Count how often each frame is used."""
        usage = {}
        for r in self.records:
            for frame in r.active_frames:
                usage[frame] = usage.get(frame, 0) + 1
        return usage


class TelemetryStore:
    """
    Persistent storage for telemetry data.

    Uses file-based storage with memory-mcp compatible structure.
    """

    def __init__(self, base_path: Optional[str] = None):
        """Initialize store with base path."""
        if base_path is None:
            base_path = os.path.expanduser("~/.claude/memory-mcp-data/telemetry")
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def store(self, record: ExecutionTelemetry) -> str:
        """Store a telemetry record, return the key."""
        key = record.memory_key()
        file_path = self.base_path / f"{key.replace('/', '_')}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as f:
            json.dump(record.to_dict(), f, indent=2)

        return key

    def load_range(self, start_date: str, end_date: str) -> TelemetryBatch:
        """Load all records in a date range."""
        batch = TelemetryBatch()

        for file_path in self.base_path.glob("telemetry_executions_*.json"):
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    record = ExecutionTelemetry.from_dict(data)

                    # Filter by date
                    if start_date <= record.timestamp[:10] <= end_date:
                        batch.add(record)
            except Exception:
                continue

        return batch

    def load_last_n_days(self, days: int = 3) -> TelemetryBatch:
        """Load records from the last N days."""
        from datetime import timedelta

        end = datetime.utcnow()
        start = end - timedelta(days=days)

        return self.load_range(
            start.strftime("%Y-%m-%d"),
            end.strftime("%Y-%m-%d")
        )


# Convenience functions for hook integration
def create_telemetry_record(
    task_type: str = "general",
    config_vector: Optional[List[float]] = None,
    active_frames: Optional[List[str]] = None,
) -> ExecutionTelemetry:
    """Create a new telemetry record with defaults."""
    return ExecutionTelemetry(
        task_type=task_type,
        config_vector=config_vector or [],
        active_frames=active_frames or [],
    )


def get_telemetry_store() -> TelemetryStore:
    """Get the default telemetry store."""
    return TelemetryStore()
