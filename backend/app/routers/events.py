# Events API Router
# Hook event ingestion from Phase 2 RBAC system

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..database import get_db
from ..models.audit import AuditLog

router = APIRouter()

# Pydantic schemas
class EventIngest(BaseModel):
    """Schema for ingesting hook events from Phase 2"""
    agent_id: Optional[str] = Field(None, description="Agent ID")
    agent_name: Optional[str] = Field("unknown", description="Agent name")
    agent_role: Optional[str] = Field("unknown", description="Agent role")
    operation_type: Optional[str] = Field("unknown", description="Operation type (tool_use, api_call, file_access, agent_spawn)")
    operation_detail: Optional[str] = Field("unknown", description="Specific operation detail")
    target_resource: Optional[str] = Field(None, description="Target resource (file, API, etc.)")
    target_type: Optional[str] = Field(None, description="Target type (file, api, database, agent)")
    rbac_decision: Optional[str] = Field("unknown", description="RBAC decision (allowed, denied, requires_approval)")
    rbac_reason: Optional[str] = Field(None, description="Reason for RBAC decision")
    cost_usd: Optional[float] = Field(None, description="Cost of operation (USD)")
    tokens_used: Optional[int] = Field(None, description="Tokens used")
    context: Optional[dict] = Field(None, description="Additional context")

class AuditLogResponse(BaseModel):
    """Schema for audit log API responses"""
    audit_id: str
    agent: dict
    operation: dict
    target: dict
    rbac: dict
    cost: dict
    context: Optional[dict]
    timestamp: str

    class Config:
        from_attributes = True

# Endpoints
@router.post("/ingest", response_model=AuditLogResponse, status_code=201)
def ingest_event(event: EventIngest, db: Session = Depends(get_db)):
    """
    Ingest a hook event from Phase 2 RBAC system.

    **Use case**: Called by Phase 2 post-audit-trail hook to log all agent operations

    **Security**: Immutable audit log (no updates or deletes allowed)
    """
    # Create audit log entry
    audit_entry = AuditLog(
        agent_id=event.agent_id,
        agent_name=event.agent_name,
        agent_role=event.agent_role,
        operation_type=event.operation_type,
        operation_detail=event.operation_detail,
        target_resource=event.target_resource,
        target_type=event.target_type,
        rbac_decision=event.rbac_decision,
        rbac_reason=event.rbac_reason,
        cost_usd=event.cost_usd,
        tokens_used=event.tokens_used,
        context=event.context
    )

    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)

    return audit_entry.to_dict()

@router.get("/audit", response_model=list[AuditLogResponse])
def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    agent_id: Optional[str] = None,
    operation_type: Optional[str] = None,
    rbac_decision: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Query audit logs with filters.

    **Filters**:
    - agent_id: Filter by specific agent
    - operation_type: Filter by operation type
    - rbac_decision: Filter by RBAC decision (allowed, denied, requires_approval)

    **Security**: Read-only endpoint (no updates/deletes on audit logs)
    """
    query = db.query(AuditLog)

    # Apply filters
    if agent_id:
        query = query.filter(AuditLog.agent_id == agent_id)
    if operation_type:
        query = query.filter(AuditLog.operation_type == operation_type)
    if rbac_decision:
        query = query.filter(AuditLog.rbac_decision == rbac_decision)

    # Order by most recent first
    query = query.order_by(AuditLog.timestamp.desc())

    # Pagination
    logs = query.offset(skip).limit(limit).all()

    return [log.to_dict() for log in logs]

@router.get("/audit/stats")
def get_audit_stats(db: Session = Depends(get_db)):
    """
    Get aggregate audit statistics.

    **Returns**:
    - Total operations
    - Allowed vs denied operations
    - Operations by type
    - Operations by agent role
    """
    from sqlalchemy import func

    total = db.query(func.count(AuditLog.audit_id)).scalar()

    # RBAC decisions
    decisions = db.query(AuditLog.rbac_decision, func.count(AuditLog.audit_id)).group_by(AuditLog.rbac_decision).all()
    decision_counts = {decision: count for decision, count in decisions}

    # Operation types
    operations = db.query(AuditLog.operation_type, func.count(AuditLog.audit_id)).group_by(AuditLog.operation_type).all()
    operation_counts = {op: count for op, count in operations}

    # Agent roles
    roles = db.query(AuditLog.agent_role, func.count(AuditLog.audit_id)).group_by(AuditLog.agent_role).all()
    role_counts = {role: count for role, count in roles}

    return {
        "total_operations": total,
        "rbac_decisions": decision_counts,
        "operation_types": operation_counts,
        "agent_roles": role_counts
    }


@router.get("/", response_model=list[AuditLogResponse])
def get_events(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    agent_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of events with pagination"""
    query = db.query(AuditLog)
    if agent_id:
        query = query.filter(AuditLog.agent_id == agent_id)
    events = query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
    return [
        AuditLogResponse(
            audit_id=str(event.audit_id),
            agent={"id": event.agent_id, "name": event.agent_name, "role": event.agent_role},
            operation={"type": event.operation_type, "detail": event.operation_detail},
            target={"resource": event.target_resource, "type": event.target_type},
            rbac={"decision": event.rbac_decision, "reason": event.rbac_reason},
            cost={"usd": event.cost_usd, "tokens": event.tokens_used},
            context=event.context,
            timestamp=event.timestamp.isoformat()
        )
        for event in events
    ]
