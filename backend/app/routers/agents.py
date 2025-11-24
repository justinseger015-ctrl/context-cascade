# Agent Management API Router
# CRUD operations for 207 agents with RBAC enforcement

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from ..database import get_db
from ..models.agent import Agent

router = APIRouter()

# Pydantic schemas for request/response validation
class AgentCreate(BaseModel):
    """Schema for creating a new agent"""
    name: str = Field(..., pattern="^[a-z0-9-]+$", description="Agent name (lowercase, alphanumeric, hyphens)")
    role: str = Field(..., description="RBAC role (admin, developer, reviewer, etc.)")
    role_confidence: Optional[float] = Field(0.0, ge=0.0, le=1.0, description="Role assignment confidence")
    capabilities: List[str] = Field(..., description="List of agent capabilities")
    rbac_allowed_tools: List[str] = Field(..., description="Allowed tools")
    rbac_path_scopes: List[str] = Field(..., description="File path scopes (glob patterns)")
    rbac_api_access: Optional[List[str]] = Field(default=[], description="External API access")
    budget_max_tokens_per_session: int = Field(..., gt=0, description="Max tokens per session")
    budget_max_cost_per_day: float = Field(..., gt=0, description="Max cost per day (USD)")
    metadata_category: str = Field(..., description="Agent category (delivery, foundry, operations, etc.)")
    metadata_specialist: Optional[bool] = Field(default=False, description="Is specialist agent")
    metadata_tags: Optional[List[str]] = Field(default=[], description="Searchable tags")

class AgentUpdate(BaseModel):
    """Schema for updating an existing agent (all fields optional)"""
    role: Optional[str] = None
    capabilities: Optional[List[str]] = None
    rbac_allowed_tools: Optional[List[str]] = None
    rbac_path_scopes: Optional[List[str]] = None
    rbac_api_access: Optional[List[str]] = None
    budget_max_tokens_per_session: Optional[int] = None
    budget_max_cost_per_day: Optional[float] = None
    metadata_category: Optional[str] = None
    metadata_tags: Optional[List[str]] = None

class AgentResponse(BaseModel):
    """Schema for agent API responses"""
    agent_id: str
    name: str
    role: str
    capabilities: List[str]
    rbac: dict
    budget: dict
    metadata: dict
    performance: dict
    timestamps: dict

    class Config:
        from_attributes = True

# Endpoints
@router.post("/", response_model=AgentResponse, status_code=201)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """
    Create a new agent with identity and RBAC metadata.

    **Security**: Requires admin role (enforced by Phase 2 RBAC hooks)
    """
    # Check if agent with this name already exists
    existing = db.query(Agent).filter(Agent.name == agent.name).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Agent with name '{agent.name}' already exists")

    # Create new agent
    new_agent = Agent(
        name=agent.name,
        role=agent.role,
        role_confidence=agent.role_confidence,
        capabilities=agent.capabilities,
        rbac_allowed_tools=agent.rbac_allowed_tools,
        rbac_path_scopes=agent.rbac_path_scopes,
        rbac_api_access=agent.rbac_api_access,
        budget_max_tokens_per_session=agent.budget_max_tokens_per_session,
        budget_max_cost_per_day=agent.budget_max_cost_per_day,
        metadata_category=agent.metadata_category,
        metadata_specialist=agent.metadata_specialist,
        metadata_tags=agent.metadata_tags
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent.to_dict()

@router.get("/", response_model=List[AgentResponse])
def list_agents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max records to return"),
    role: Optional[str] = Query(None, description="Filter by role"),
    category: Optional[str] = Query(None, description="Filter by category"),
    specialist: Optional[bool] = Query(None, description="Filter by specialist flag"),
    db: Session = Depends(get_db)
):
    """
    List all agents with optional filters and pagination.

    **Filters**:
    - role: Filter by RBAC role (admin, developer, etc.)
    - category: Filter by metadata category (delivery, foundry, etc.)
    - specialist: Filter by specialist flag (true/false)

    **Pagination**: Use `skip` and `limit` parameters
    """
    query = db.query(Agent)

    # Apply filters
    if role:
        query = query.filter(Agent.role == role)
    if category:
        query = query.filter(Agent.metadata_category == category)
    if specialist is not None:
        query = query.filter(Agent.metadata_specialist == specialist)

    # Pagination
    agents = query.offset(skip).limit(limit).all()

    return [agent.to_dict() for agent in agents]

@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Get a single agent by ID.

    **Returns**: Complete agent identity with RBAC, budget, performance, and metadata
    """
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID '{agent_id}' not found")

    return agent.to_dict()

@router.get("/name/{agent_name}", response_model=AgentResponse)
def get_agent_by_name(agent_name: str, db: Session = Depends(get_db)):
    """
    Get a single agent by name (alternative to ID lookup).

    **Returns**: Complete agent identity with RBAC, budget, performance, and metadata
    """
    agent = db.query(Agent).filter(Agent.name == agent_name).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with name '{agent_name}' not found")

    return agent.to_dict()

@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: str, updates: AgentUpdate, db: Session = Depends(get_db)):
    """
    Update an existing agent's configuration.

    **Security**: Requires admin role (enforced by Phase 2 RBAC hooks)

    **Updatable fields**: role, capabilities, RBAC rules, budget limits, metadata
    """
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID '{agent_id}' not found")

    # Update only provided fields
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field in ["rbac_allowed_tools", "rbac_path_scopes", "rbac_api_access"]:
            setattr(agent, field, value)
        elif field.startswith("budget_"):
            setattr(agent, field, value)
        elif field.startswith("metadata_"):
            setattr(agent, field, value)
        elif field in ["role", "capabilities"]:
            setattr(agent, field, value)

    db.commit()
    db.refresh(agent)

    return agent.to_dict()

@router.delete("/{agent_id}", status_code=204)
def delete_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Delete an agent by ID.

    **Security**: Requires admin role (enforced by Phase 2 RBAC hooks)
    **Warning**: This action is irreversible
    """
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID '{agent_id}' not found")

    db.delete(agent)
    db.commit()

    return None

@router.post("/{agent_id}/activate", response_model=AgentResponse)
def activate_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Mark an agent as active (updates last_active_at timestamp).

    **Use case**: Called when an agent starts a task
    """
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID '{agent_id}' not found")

    agent.last_active_at = datetime.utcnow()
    db.commit()
    db.refresh(agent)

    return agent.to_dict()

@router.get("/stats/summary")
def get_agent_stats(db: Session = Depends(get_db)):
    """
    Get aggregate statistics across all agents.

    **Returns**: Total count, role distribution, category distribution, specialist count
    """
    from sqlalchemy import func

    total_count = db.query(func.count(Agent.agent_id)).scalar()

    # Role distribution
    role_dist = db.query(Agent.role, func.count(Agent.agent_id)).group_by(Agent.role).all()
    role_distribution = {role: count for role, count in role_dist}

    # Category distribution
    category_dist = db.query(Agent.metadata_category, func.count(Agent.agent_id)).group_by(Agent.metadata_category).all()
    category_distribution = {cat: count for cat, count in category_dist}

    # Specialist count
    specialist_count = db.query(func.count(Agent.agent_id)).filter(Agent.metadata_specialist == True).scalar()

    return {
        "total_agents": total_count,
        "role_distribution": role_distribution,
        "category_distribution": category_distribution,
        "specialists": specialist_count,
        "generalists": total_count - specialist_count
    }


# Alias endpoint for /registry (frontend compatibility)
@router.get("/registry", response_model=List[AgentResponse])
def get_agents_registry(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    role: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Alias for GET /agents - frontend expects /registry path"""
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
            created_at=agent.created_at.isoformat(),
            updated_at=agent.updated_at.isoformat() if agent.updated_at else None
        )
        for agent in agents
    ]
