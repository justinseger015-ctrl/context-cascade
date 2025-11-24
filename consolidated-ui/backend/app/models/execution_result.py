"""
ExecutionResult ORM model.

Maps to execution_results table from P1_T2 schema.
Represents task execution outcomes with performance metrics.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Index,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class ExecutionResult(Base):
    """
    Task execution result with metrics.

    Attributes:
        id: Primary key
        task_id: Foreign key to scheduled_tasks
        started_at: Execution start timestamp
        ended_at: Execution end timestamp
        status: Execution status (success, failed, timeout)
        output_text: Execution output/logs
        error_text: Error messages if failed
        duration_ms: Execution duration in milliseconds
    """

    __tablename__ = "execution_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(
        Integer,
        ForeignKey("scheduled_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    started_at = Column(DateTime, nullable=False, index=True)
    ended_at = Column(DateTime, nullable=True)
    status = Column(
        String(20),
        nullable=False,
        index=True,
    )
    output_text = Column(Text, nullable=True)
    error_text = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)

    # Relationships
    task = relationship("ScheduledTask", back_populates="execution_results")

    # Composite indexes for performance
    __table_args__ = (
        Index("ix_execution_results_task_started", "task_id", "started_at"),
        Index("ix_execution_results_status_started", "status", "started_at"),
        CheckConstraint(
            "status IN ('success', 'failed', 'timeout', 'cancelled')",
            name="check_execution_result_status",
        ),
        CheckConstraint(
            "duration_ms >= 0",
            name="check_duration_positive",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<ExecutionResult(id={self.id}, task_id={self.task_id}, "
            f"status={self.status}, duration={self.duration_ms}ms)>"
        )

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "task_id": self.task_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "status": self.status,
            "output_text": self.output_text,
            "error_text": self.error_text,
            "duration_ms": self.duration_ms,
        }
