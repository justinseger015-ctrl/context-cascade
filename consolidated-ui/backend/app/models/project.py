"""
Project ORM model.

Maps to projects table from P1_T2 schema.
Represents user projects/workspaces.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Index,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Project(Base):
    """
    User project/workspace.

    Attributes:
        id: Primary key
        name: Project name
        description: Project description
        created_at: Creation timestamp
        updated_at: Last update timestamp
        tasks_count: Cached count of associated tasks
        user_id: User who owns the project
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    tasks_count = Column(Integer, default=0, nullable=False)
    user_id = Column(String(255), nullable=True, index=True)

    # Relationships (if we add task-project association later)
    # tasks = relationship("ScheduledTask", back_populates="project")

    # Composite indexes for performance
    __table_args__ = (
        Index("ix_projects_user_created", "user_id", "created_at"),
        Index("ix_projects_name_user", "name", "user_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<Project(id={self.id}, name={self.name}, "
            f"tasks={self.tasks_count}, user={self.user_id})>"
        )

    def to_dict(self) -> dict:
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "tasks_count": self.tasks_count,
            "user_id": self.user_id,
        }
