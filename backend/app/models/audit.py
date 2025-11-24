# AuditLog ORM Model - Maps to agent_audit_log table
# Stores immutable audit trail for security compliance and incident investigation

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text
from sqlalchemy.sql import func
from ..database import Base
import uuid

class AuditLog(Base):
    """
    Agent Audit Log Model - Immutable audit trail for all agent operations.

    Stores:
    - Agent identity and role
    - Operation performed (tool used, API called)
    - Target resources (files accessed, APIs called)
    - RBAC decision (allowed/denied)
    - Timestamp for compliance (90-day retention)
    """
    __tablename__ = "agent_audit_log"

    # Primary Key
    audit_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)

    # Agent Identity
    agent_id = Column(String, nullable=False, index=True)
    agent_name = Column(String, nullable=False, index=True)
    agent_role = Column(String, nullable=False, index=True)

    # Operation
    operation_type = Column(String, nullable=False, index=True)  # tool_use, api_call, file_access, agent_spawn
    operation_detail = Column(String, nullable=False)  # Specific operation (e.g., "Read file.txt", "POST /api/v1/agents")

    # Target
    target_resource = Column(String, nullable=True)  # Resource accessed (file path, API endpoint, etc.)
    target_type = Column(String, nullable=True)  # file, api, database, agent

    # RBAC Decision
    rbac_decision = Column(String, nullable=False, index=True)  # allowed, denied, requires_approval
    rbac_reason = Column(Text, nullable=True)  # Reason for decision (e.g., "Permission denied: not in path_scopes")

    # Cost
    cost_usd = Column(Float, nullable=True)  # Cost of operation (if applicable)
    tokens_used = Column(Integer, nullable=True)  # Tokens used (if applicable)

    # Context
    context = Column(JSON, nullable=True)  # Additional context (session_id, task_id, etc.)

    # Timestamp (immutable)
    timestamp = Column(DateTime, default=func.now(), nullable=False, index=True)

    def to_dict(self):
        """Convert AuditLog model to dictionary for API responses"""
        return {
            "audit_id": self.audit_id,
            "agent": {
                "agent_id": self.agent_id,
                "name": self.agent_name,
                "role": self.agent_role
            },
            "operation": {
                "type": self.operation_type,
                "detail": self.operation_detail
            },
            "target": {
                "resource": self.target_resource,
                "type": self.target_type
            },
            "rbac": {
                "decision": self.rbac_decision,
                "reason": self.rbac_reason
            },
            "cost": {
                "usd": self.cost_usd,
                "tokens_used": self.tokens_used
            },
            "context": self.context,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

    def __repr__(self):
        return f"<AuditLog(id={self.audit_id}, agent={self.agent_name}, operation={self.operation_type}, decision={self.rbac_decision})>"
