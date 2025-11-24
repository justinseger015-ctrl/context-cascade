# Agent Activity API Router
# GET endpoint for retrieving agent activity logs (separate from WebSocket)

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from ..database import get_db
from ..models.audit import AuditLog

router = APIRouter()

@router.get("/agent-activity", response_model=list[dict])
def get_agent_activity(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    agent_id: Optional[str] = Query(None),
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Get recent agent activity from audit logs for dashboard"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    query = db.query(AuditLog).filter(AuditLog.timestamp >= cutoff_time)
    if agent_id:
        query = query.filter(AuditLog.agent_id == agent_id)
    activities = query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
    return [
        {
            "activity_id": str(activity.audit_id),
            "agent_id": activity.agent_id,
            "agent_name": activity.agent_name,
            "operation_type": activity.operation_type,
            "operation_detail": activity.operation_detail,
            "rbac_decision": activity.rbac_decision,
            "timestamp": activity.timestamp.isoformat(),
            "cost_usd": activity.cost_usd,
            "tokens_used": activity.tokens_used
        }
        for activity in activities
    ]
