# Agent ORM Model - Maps to agent_identities table
# Stores agent identity, RBAC rules, budget limits, and performance metrics

from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from ..database import Base
import uuid

class Agent(Base):
    """
    Agent Identity Model - First-class agent representation with RBAC and budget controls.

    Represents a single agent in the Agent Reality Map system with:
    - Unique UUID identity
    - RBAC role and permissions
    - Budget limits and usage tracking
    - Performance metrics
    - Metadata (category, specialist, version, tags)
    """
    __tablename__ = "agent_identities"

    # Primary Key
    agent_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # Basic Identity
    name = Column(String, nullable=False, index=True, unique=True)
    role = Column(String, nullable=False, index=True)  # admin, developer, reviewer, etc.
    role_confidence = Column(Float, default=0.0)  # 0.0-1.0 confidence score
    role_reasoning = Column(String, nullable=True)  # Why this role was assigned

    # Capabilities
    capabilities = Column(JSON, nullable=False)  # List of agent capabilities

    # RBAC (Role-Based Access Control)
    rbac_allowed_tools = Column(JSON, nullable=False)  # List of allowed tools
    rbac_denied_tools = Column(JSON, default=list)  # List of denied tools
    rbac_path_scopes = Column(JSON, nullable=False)  # File path patterns (glob)
    rbac_api_access = Column(JSON, default=list)  # External APIs
    rbac_requires_approval = Column(Boolean, default=False)  # High-risk flag
    rbac_approval_threshold = Column(Float, default=10.0)  # Cost threshold for approval

    # Budget
    budget_max_tokens_per_session = Column(Integer, nullable=False)
    budget_max_cost_per_day = Column(Float, nullable=False)
    budget_currency = Column(String, default="USD")

    # Current Usage (updated in real-time)
    budget_tokens_used_today = Column(Integer, default=0)
    budget_cost_used_today = Column(Float, default=0.0)
    budget_last_reset = Column(DateTime, default=func.now())

    # Metadata
    metadata_category = Column(String, nullable=False, index=True)  # delivery, foundry, operations, etc.
    metadata_specialist = Column(Boolean, default=False)
    metadata_version = Column(String, default="1.0.0")
    metadata_tags = Column(JSON, default=list)  # Searchable tags

    # Performance Metrics (optional, tracked at runtime)
    performance_success_rate = Column(Float, default=0.0)  # 0.0-1.0
    performance_avg_execution_time_ms = Column(Float, default=0.0)
    performance_quality_score = Column(Float, default=0.0)  # Connascence score
    performance_total_tasks_completed = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    last_active_at = Column(DateTime, nullable=True)

    def to_dict(self):
        """Convert Agent model to dictionary for API responses"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "role_confidence": self.role_confidence,
            "capabilities": self.capabilities,
            "rbac": {
                "allowed_tools": self.rbac_allowed_tools,
                "denied_tools": self.rbac_denied_tools,
                "path_scopes": self.rbac_path_scopes,
                "api_access": self.rbac_api_access,
                "requires_approval": self.rbac_requires_approval,
                "approval_threshold": self.rbac_approval_threshold
            },
            "budget": {
                "max_tokens_per_session": self.budget_max_tokens_per_session,
                "max_cost_per_day": self.budget_max_cost_per_day,
                "currency": self.budget_currency,
                "tokens_used_today": self.budget_tokens_used_today,
                "cost_used_today": self.budget_cost_used_today,
                "last_reset": self.budget_last_reset.isoformat() if self.budget_last_reset else None
            },
            "metadata": {
                "category": self.metadata_category,
                "specialist": self.metadata_specialist,
                "version": self.metadata_version,
                "tags": self.metadata_tags
            },
            "performance": {
                "success_rate": self.performance_success_rate,
                "avg_execution_time_ms": self.performance_avg_execution_time_ms,
                "quality_score": self.performance_quality_score,
                "total_tasks_completed": self.performance_total_tasks_completed
            },
            "timestamps": {
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "last_active_at": self.last_active_at.isoformat() if self.last_active_at else None
            }
        }

    def __repr__(self):
        return f"<Agent(id={self.agent_id}, name={self.name}, role={self.role})>"
