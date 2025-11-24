"""
ScheduledTask ORM model.

Maps to scheduled_tasks table from P1_T2 schema.
Represents automated task execution schedules.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    Index,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class ScheduledTask(Base):
    """
    Scheduled task for automated skill/agent execution.

    Attributes:
        id: Primary key
        skill_name: Name of skill to execute
        schedule_cron: Cron expression for scheduling
        next_run_at: Next scheduled execution time
        params_json: Execution parameters (JSON)
        status: Task status (pending, running, completed, failed)
        created_at: Creation timestamp
        updated_at: Last update timestamp
        user_id: User who created the task
    """

    __tablename__ = "scheduled_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    skill_name = Column(String(255), nullable=False)
    schedule_cron = Column(String(100), nullable=False)
    next_run_at = Column(DateTime, nullable=False, index=True)
    params_json = Column(JSON, default={}, nullable=False)
    status = Column(
        String(20),
        default="pending",
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    user_id = Column(String(255), nullable=True, index=True)

    # Relationships
    execution_results = relationship(
        "ExecutionResult",
        back_populates="task",
        cascade="all, delete-orphan",
    )

    # Composite indexes for performance
    __table_args__ = (
        Index("ix_scheduled_tasks_user_status", "user_id", "status"),
        Index("ix_scheduled_tasks_status_next_run", "status", "next_run_at"),
        CheckConstraint(
            "status IN ('pending', 'running', 'completed', 'failed', 'disabled')",
            name="check_scheduled_task_status",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<ScheduledTask(id={self.id}, skill={self.skill_name}, "
            f"status={self.status}, next_run={self.next_run_at})>"
        )

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "skill_name": self.skill_name,
            "schedule_cron": self.schedule_cron,
            "next_run_at": self.next_run_at.isoformat() if self.next_run_at else None,
            "params_json": self.params_json,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
        }
