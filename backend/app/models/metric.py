# Metric ORM Model - Maps to agent_metrics table
# Stores performance metrics, costs, and quality scores for agents

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import uuid

class Metric(Base):
    """
    Agent Metric Model - Time-series performance and cost tracking.

    Stores individual metric records for:
    - Agent performance (execution time, success rate)
    - Cost tracking (tokens, API calls, $)
    - Quality scores (Connascence analysis)
    - Task completion statistics
    """
    __tablename__ = "agent_metrics"

    # Primary Key
    metric_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # Foreign Key to Agent
    agent_id = Column(String, ForeignKey("agent_identities.agent_id"), nullable=False, index=True)

    # Metric Type
    metric_type = Column(String, nullable=False, index=True)  # execution, cost, quality, task_completion

    # Execution Metrics
    execution_time_ms = Column(Float, nullable=True)  # Task execution time
    success = Column(Integer, nullable=True)  # 1 = success, 0 = failure

    # Cost Metrics
    tokens_used = Column(Integer, nullable=True)
    api_calls = Column(Integer, nullable=True)
    cost_usd = Column(Float, nullable=True)

    # Quality Metrics
    quality_score = Column(Float, nullable=True)  # Connascence score (0-1)
    code_violations = Column(Integer, nullable=True)  # Number of quality violations

    # Task Completion Metrics
    tasks_completed = Column(Integer, nullable=True)
    tasks_failed = Column(Integer, nullable=True)

    # Context (optional metadata)
    context = Column(JSON, nullable=True)  # Additional context (task_id, project, etc.)

    # Timestamp
    recorded_at = Column(DateTime, default=func.now(), nullable=False, index=True)

    def to_dict(self):
        """Convert Metric model to dictionary for API responses"""
        return {
            "metric_id": self.metric_id,
            "agent_id": self.agent_id,
            "metric_type": self.metric_type,
            "execution_time_ms": self.execution_time_ms,
            "success": bool(self.success) if self.success is not None else None,
            "tokens_used": self.tokens_used,
            "api_calls": self.api_calls,
            "cost_usd": self.cost_usd,
            "quality_score": self.quality_score,
            "code_violations": self.code_violations,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "context": self.context,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None
        }

    def __repr__(self):
        return f"<Metric(id={self.metric_id}, agent={self.agent_id}, type={self.metric_type})>"
