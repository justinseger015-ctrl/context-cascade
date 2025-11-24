"""
Agent ORM model.

Maps to agents table from P1_T2 schema.
Represents AI agents in the system.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    Index,
    CheckConstraint,
)
from app.core.database import Base


class Agent(Base):
    """
    AI agent in the system.

    Attributes:
        id: Primary key
        name: Agent name/identifier
        type: Agent type (coder, reviewer, tester, etc.)
        capabilities_json: Agent capabilities (JSON)
        status: Agent status (active, idle, busy, offline)
        last_active_at: Last activity timestamp
    """

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(100), nullable=False, index=True)
    capabilities_json = Column(JSON, default=[], nullable=False)
    status = Column(
        String(20),
        default="idle",
        nullable=False,
        index=True,
    )
    last_active_at = Column(DateTime, nullable=True)

    # Composite indexes for performance
    __table_args__ = (
        Index("ix_agents_type_status", "type", "status"),
        Index("ix_agents_status_active", "status", "last_active_at"),
        CheckConstraint(
            "status IN ('active', 'idle', 'busy', 'offline', 'error')",
            name="check_agent_status",
        ),
        CheckConstraint(
            "type IN ('coder', 'reviewer', 'tester', 'planner', 'researcher', "
            "'api-designer', 'backend-dev', 'mobile-dev', 'ml-developer', "
            "'system-architect', 'code-analyzer', 'hierarchical-coordinator', "
            "'mesh-coordinator', 'adaptive-coordinator', 'custom')",
            name="check_agent_type",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<Agent(id={self.id}, name={self.name}, "
            f"type={self.type}, status={self.status})>"
        )

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capabilities_json": self.capabilities_json,
            "status": self.status,
            "last_active_at": (
                self.last_active_at.isoformat() if self.last_active_at else None
            ),
        }
