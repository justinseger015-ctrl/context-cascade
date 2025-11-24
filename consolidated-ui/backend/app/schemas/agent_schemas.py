"""
Agent API Schemas
Pydantic models for agent registry endpoints
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class AgentBase(BaseModel):
    """Base agent schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Agent name/identifier")
    type: str = Field(..., description="Agent type (coder, reviewer, tester, etc.)")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    status: str = Field(default="idle", description="Agent status")


class AgentCreate(AgentBase):
    """Schema for creating a new agent"""
    pass


class AgentUpdate(BaseModel):
    """Schema for updating an agent (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = None
    capabilities: Optional[List[str]] = None
    status: Optional[str] = None


class ExecutionHistoryItem(BaseModel):
    """Single execution history item"""
    task_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    status: str
    duration_ms: Optional[int] = None
    output_text: Optional[str] = None
    error_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AgentResponse(AgentBase):
    """Agent response schema"""
    id: int
    last_active_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AgentDetailedResponse(AgentResponse):
    """Detailed agent response with execution history"""
    execution_history: List[ExecutionHistoryItem] = Field(
        default_factory=list,
        description="Last 50 task executions"
    )
    success_rate: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Success rate (0.0-1.0)"
    )
    avg_duration_ms: float = Field(
        default=0.0,
        ge=0.0,
        description="Average execution duration in milliseconds"
    )


class AgentListResponse(BaseModel):
    """Paginated agent list response"""
    agents: List[AgentResponse]
    total: int
    limit: int
    offset: int


class AgentActivityLog(BaseModel):
    """Schema for logging agent activity"""
    agent_id: int = Field(..., description="Agent ID")
    task_id: int = Field(..., description="Task ID being executed")
    status: str = Field(..., description="Execution status (running, success, failed, timeout)")
    output: Optional[str] = Field(None, description="Execution output")
    error: Optional[str] = Field(None, description="Error message if failed")
    duration_ms: Optional[int] = Field(None, ge=0, description="Execution duration in milliseconds")


class AgentActivityResponse(BaseModel):
    """Response for activity logging"""
    status: str
    message: str
    agent_id: int
    task_id: int
    stored_in_memory_mcp: bool
    broadcasted_via_websocket: bool
