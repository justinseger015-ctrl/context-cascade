"""
Vector Search API for Memory MCP
FastAPI endpoints for semantic search of project/task history

Provides:
- Vector search with similarity ranking
- Task history retrieval
- Related task discovery
- Project-scoped search
- Health monitoring
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from .memory_mcp_client import MemoryMCPClient, create_memory_mcp_client
from .tagging_protocol import Intent
from app.dependencies import get_postgres_client, get_redis_client

router = APIRouter(prefix="/api/v1/memory", tags=["memory"])


# Request/Response Models

class VectorSearchRequest(BaseModel):
    """Request model for vector search"""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    project_id: Optional[str] = Field(None, description="Filter by project ID")
    task_type: Optional[str] = Field(None, description="Filter by task type (intent)")
    limit: int = Field(10, ge=1, le=50, description="Maximum results to return")


class VectorSearchResult(BaseModel):
    """Single vector search result"""
    task_id: str
    content: str
    similarity_score: float = Field(..., ge=0, le=1)
    metadata: Dict[str, Any]
    created_at: datetime


class VectorSearchResponse(BaseModel):
    """Response model for vector search"""
    query: str
    results: List[VectorSearchResult]
    total_results: int
    search_time_ms: float
    source: str = Field(..., description="memory_mcp or postgresql_fallback")


class MemoryStoreRequest(BaseModel):
    """Request model for storing data in Memory MCP"""
    content: str = Field(..., min_length=1, description="Content to store")
    intent: Intent = Field(..., description="Intent category")
    user_id: Optional[str] = Field(None, description="User identifier")
    task_id: Optional[str] = Field(None, description="Task identifier")
    additional_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class MemoryStoreResponse(BaseModel):
    """Response model for memory storage"""
    status: str
    storage: str
    task_id: str
    metadata: Dict[str, Any]
    warning: Optional[str] = None


class TaskHistoryResponse(BaseModel):
    """Response model for task history"""
    task: Dict[str, Any]
    related_tasks: List[VectorSearchResult]
    source: str
    warning: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str
    degraded_mode: bool
    circuit_breaker_state: str
    mcp_available: bool
    fallback_available: bool
    last_check: datetime
    error: Optional[str] = None


# Dependency injection

async def get_memory_client(
    postgres=Depends(get_postgres_client),
    redis=Depends(get_redis_client)
) -> MemoryMCPClient:
    """Get Memory MCP client with dependencies"""
    return create_memory_mcp_client(
        postgres_client=postgres,
        redis_client=redis
    )


# API Endpoints

@router.post("/search", response_model=VectorSearchResponse)
async def vector_search(
    request: VectorSearchRequest,
    client: MemoryMCPClient = Depends(get_memory_client)
):
    """
    Perform semantic vector search across Memory MCP

    Features:
    - Semantic similarity ranking
    - Project and task type filtering
    - Automatic fallback to PostgreSQL if Memory MCP unavailable

    Returns ranked results by similarity score.
    """
    start_time = datetime.now()

    try:
        results = await client.vector_search(
            query=request.query,
            project_id=request.project_id,
            task_type=request.task_type,
            limit=request.limit
        )

        search_time = (datetime.now() - start_time).total_seconds() * 1000

        # Determine source
        source = "memory_mcp"
        if client._degraded_mode:
            source = "postgresql_fallback"

        return VectorSearchResponse(
            query=request.query,
            results=[
                VectorSearchResult(
                    task_id=r.get("task_id"),
                    content=r.get("content"),
                    similarity_score=r.get("similarity_score", 0.0),
                    metadata=r.get("metadata", {}),
                    created_at=r.get("created_at")
                )
                for r in results
            ],
            total_results=len(results),
            search_time_ms=search_time,
            source=source
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Vector search failed: {str(e)}"
        )


@router.post("/store", response_model=MemoryStoreResponse)
async def store_memory(
    request: MemoryStoreRequest,
    client: MemoryMCPClient = Depends(get_memory_client)
):
    """
    Store data in Memory MCP with automatic WHO/WHEN/PROJECT/WHY tagging

    Features:
    - Automatic metadata tagging
    - Circuit breaker protection
    - Fallback to PostgreSQL + Redis cache

    Returns storage confirmation with metadata.
    """
    try:
        result = await client.store(
            content=request.content,
            intent=request.intent,
            user_id=request.user_id,
            task_id=request.task_id,
            additional_metadata=request.additional_metadata
        )

        return MemoryStoreResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Memory storage failed: {str(e)}"
        )


@router.get("/task/{task_id}", response_model=TaskHistoryResponse)
async def get_task_history(
    task_id: str,
    include_related: bool = Query(True, description="Include related tasks via vector search"),
    client: MemoryMCPClient = Depends(get_memory_client)
):
    """
    Get task history with optional related tasks

    Features:
    - Retrieves task data with full metadata
    - Optional semantic search for related tasks
    - Automatic fallback to Redis cache or PostgreSQL

    Returns task history and related tasks.
    """
    try:
        result = await client.get_task_history(
            task_id=task_id,
            include_related=include_related
        )

        return TaskHistoryResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {str(e)}"
        )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(
    client: MemoryMCPClient = Depends(get_memory_client)
):
    """
    Check Memory MCP health and circuit breaker state

    Returns:
    - Overall health status
    - Degraded mode indicator
    - Circuit breaker state
    - Memory MCP availability
    - Fallback system availability
    """
    try:
        health = await client.health_check()

        return HealthCheckResponse(
            status=health["status"],
            degraded_mode=health["degraded_mode"],
            circuit_breaker_state=health["circuit_breaker_state"],
            mcp_available=health.get("mcp_available", False),
            fallback_available=health.get("fallback_available", True),
            last_check=datetime.fromisoformat(health["last_check"]),
            error=health.get("error")
        )

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/projects/{project_id}/summary")
async def get_project_summary(
    project_id: str,
    client: MemoryMCPClient = Depends(get_memory_client)
):
    """
    Get project summary with task statistics

    Returns:
    - Total tasks
    - Tasks by intent category
    - Recent activity
    - Top contributors
    """
    try:
        # Search for all tasks in project
        results = await client.vector_search(
            query="",  # Empty query to get all
            project_id=project_id,
            limit=1000  # Get all for statistics
        )

        # Calculate statistics
        by_intent = {}
        by_agent = {}
        recent_tasks = []

        for task in results:
            metadata = task.get("metadata", {})

            # Count by intent
            intent = metadata.get("why", {}).get("intent", "unknown")
            by_intent[intent] = by_intent.get(intent, 0) + 1

            # Count by agent
            agent = metadata.get("who", {}).get("agent_id", "unknown")
            by_agent[agent] = by_agent.get(agent, 0) + 1

            # Track recent tasks (last 10)
            if len(recent_tasks) < 10:
                recent_tasks.append({
                    "task_id": task.get("task_id"),
                    "content": task.get("content", "")[:100],
                    "created_at": task.get("created_at")
                })

        return {
            "project_id": project_id,
            "total_tasks": len(results),
            "by_intent": by_intent,
            "by_agent": by_agent,
            "recent_tasks": recent_tasks,
            "source": "memory_mcp" if not client._degraded_mode else "postgresql_fallback"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get project summary: {str(e)}"
        )
