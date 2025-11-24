# Registry API Router - Frontend compatibility layer
# Provides /registry/agents endpoint expected by frontend

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models.agent import Agent
from .agents import AgentResponse

router = APIRouter()

@router.get("/agents", response_model=List[AgentResponse])
def get_registry_agents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    role: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get agents from registry (alias for /agents endpoint)"""
    query = db.query(Agent)
    if role:
        query = query.filter(Agent.role == role)
    agents = query.offset(skip).limit(limit).all()
    return [
        AgentResponse(
            agent_id=str(agent.agent_id),
            name=agent.name,
            role=agent.role,
            capabilities=agent.capabilities,
            rbac={"allowed_tools": agent.rbac_allowed_tools, "path_scopes": agent.rbac_path_scopes, "api_access": agent.rbac_api_access},
            budget={"max_tokens_per_session": agent.budget_max_tokens_per_session, "max_cost_per_day": agent.budget_max_cost_per_day},
            metadata={"category": agent.metadata_category, "specialist": agent.metadata_specialist, "tags": agent.metadata_tags},
            performance={"tasks_completed": 0, "success_rate": 0.0, "avg_execution_time": 0.0},
            timestamps={"created_at": agent.created_at.isoformat(), "updated_at": agent.updated_at.isoformat() if agent.updated_at else None}
        )
        for agent in agents
    ]
