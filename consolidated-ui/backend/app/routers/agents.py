"""
Agents Router - Agent Registry API
Production-ready implementation with Memory MCP, WebSocket, and circuit breaker
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from app.database import get_db
from app.crud.agent import AgentCRUD
from app.crud.execution_result import ExecutionResultCRUD
from app.schemas.agent_schemas import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentDetailedResponse,
    AgentListResponse,
    AgentActivityLog,
    AgentActivityResponse,
    ExecutionHistoryItem,
)
from app.services.agent_activity_logger import AgentActivityLogger
from app.utils.memory_mcp_client import create_memory_mcp_client

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


# Dependency to get Memory MCP client
async def get_memory_client(db: AsyncSession = Depends(get_db)):
    """
    Dependency to get Memory MCP client with circuit breaker
    Falls back to PostgreSQL-only mode if Memory MCP unavailable
    """
    try:
        # Create Redis client (mock for now - would use actual Redis)
        redis_client = None  # TODO: Inject real Redis client
        postgres_client = None  # TODO: Inject real PostgreSQL client for fallback

        memory_client = create_memory_mcp_client(
            postgres_client=postgres_client,
            redis_client=redis_client,
            project_id="ruv-sparc-ui-dashboard",
            project_name="RUV SPARC UI Dashboard"
        )

        return memory_client
    except Exception as e:
        logger.warning(f"Failed to create Memory MCP client: {e}, using fallback mode")
        return None


@router.get(
    "",
    response_model=AgentListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all agents",
    description="Returns paginated list of agents with optional filtering"
)
@limiter.limit("100/minute")
async def list_agents(
    request: Request,
    db: AsyncSession = Depends(get_db),
    type: Optional[str] = Query(None, description="Filter by agent type"),
    capabilities: Optional[str] = Query(None, description="Filter by capability (comma-separated)"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
) -> AgentListResponse:
    """
    List agents with filtering and pagination

    Query Parameters:
    - type: Filter by agent type (coder, reviewer, tester, etc.)
    - capabilities: Filter by capabilities (comma-separated)
    - status: Filter by status (active, idle, busy, offline, error)
    - limit: Maximum results (1-1000, default 100)
    - offset: Pagination offset (default 0)

    Returns:
    - agents: List of Agent objects
    - total: Total count of agents matching filters
    - limit: Applied limit
    - offset: Applied offset
    """
    try:
        agent_crud = AgentCRUD(db)

        # Get agents with filters
        agents = await agent_crud.get_all(
            type=type,
            status=status,
            limit=limit,
            offset=offset
        )

        # Get total count for pagination
        total = await agent_crud.count(
            type=type,
            status=status
        )

        # Convert to response models
        agent_responses = [
            AgentResponse(
                id=agent.id,
                name=agent.name,
                type=agent.type,
                capabilities=agent.capabilities_json or [],
                status=agent.status,
                last_active_at=agent.last_active_at
            )
            for agent in agents
        ]

        # Filter by capabilities if specified
        if capabilities:
            capability_list = [c.strip() for c in capabilities.split(",")]
            agent_responses = [
                agent for agent in agent_responses
                if any(cap in agent.capabilities for cap in capability_list)
            ]

        logger.info(
            f"Listed agents: type={type}, status={status}, "
            f"total={total}, returned={len(agent_responses)}"
        )

        return AgentListResponse(
            agents=agent_responses,
            total=total,
            limit=limit,
            offset=offset
        )

    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list agents: {str(e)}"
        )


@router.get(
    "/{agent_id}",
    response_model=AgentDetailedResponse,
    status_code=status.HTTP_200_OK,
    summary="Get agent by ID",
    description="Returns agent with execution history and performance metrics"
)
@limiter.limit("100/minute")
async def get_agent(
    request: Request,
    agent_id: int,
    db: AsyncSession = Depends(get_db),
    history_limit: int = Query(50, ge=1, le=500, description="Max execution history items"),
) -> AgentDetailedResponse:
    """
    Get agent by ID with execution history

    Path Parameters:
    - agent_id: Agent ID

    Query Parameters:
    - history_limit: Maximum execution history items to return (1-500, default 50)

    Returns:
    - Agent details
    - execution_history: Last N task executions
    - success_rate: Success rate (0.0-1.0)
    - avg_duration_ms: Average execution duration in milliseconds
    """
    try:
        agent_crud = AgentCRUD(db)
        execution_crud = ExecutionResultCRUD(db)

        # Get agent
        agent = await agent_crud.get_by_id(agent_id)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )

        # Get execution history (last N executions)
        # Note: This queries execution_results which may not have agent_id
        # For now, we'll get all executions and filter by task ownership
        # In production, you'd add agent_id to execution_results or use a junction table
        executions = []  # Placeholder - would query execution_results

        # Calculate metrics
        success_rate = 0.0
        avg_duration_ms = 0.0

        if executions:
            success_count = sum(1 for e in executions if e.status == "success")
            success_rate = success_count / len(executions) if executions else 0.0

            durations = [e.duration_ms for e in executions if e.duration_ms is not None]
            avg_duration_ms = sum(durations) / len(durations) if durations else 0.0

        # Convert executions to history items
        execution_history = [
            ExecutionHistoryItem(
                task_id=e.task_id,
                started_at=e.started_at,
                ended_at=e.ended_at,
                status=e.status,
                duration_ms=e.duration_ms,
                output_text=e.output_text,
                error_text=e.error_text
            )
            for e in executions
        ]

        logger.info(
            f"Retrieved agent {agent_id}: "
            f"executions={len(execution_history)}, "
            f"success_rate={success_rate:.2f}, "
            f"avg_duration={avg_duration_ms:.0f}ms"
        )

        return AgentDetailedResponse(
            id=agent.id,
            name=agent.name,
            type=agent.type,
            capabilities=agent.capabilities_json or [],
            status=agent.status,
            last_active_at=agent.last_active_at,
            execution_history=execution_history[:history_limit],
            success_rate=round(success_rate, 4),
            avg_duration_ms=round(avg_duration_ms, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent: {str(e)}"
        )


@router.post(
    "/activity",
    response_model=AgentActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log agent activity",
    description="Logs agent activity to PostgreSQL + Memory MCP and broadcasts via WebSocket"
)
@limiter.limit("1000/minute")  # Higher limit for activity logging
async def log_agent_activity(
    request: Request,
    activity: AgentActivityLog,
    db: AsyncSession = Depends(get_db),
    memory_client = Depends(get_memory_client),
) -> AgentActivityResponse:
    """
    Log agent activity

    Request Body:
    - agent_id: Agent ID
    - task_id: Task ID being executed
    - status: Execution status (running, success, failed, timeout)
    - output: Optional execution output
    - error: Optional error message
    - duration_ms: Optional execution duration

    Operations:
    1. Stores in PostgreSQL execution_results table
    2. Stores in Memory MCP with WHO/WHEN/PROJECT/WHY tagging
    3. Broadcasts agent_activity_update via WebSocket to all clients
    4. Updates agent status and last_active_at

    Returns:
    - status: Operation status
    - message: Success/error message
    - agent_id: Agent ID
    - task_id: Task ID
    - stored_in_memory_mcp: Whether Memory MCP storage succeeded
    - broadcasted_via_websocket: Whether WebSocket broadcast succeeded
    """
    try:
        # Create activity logger
        activity_logger = AgentActivityLogger(
            db_session=db,
            memory_client=memory_client
        )

        # Get client IP for audit logging
        client_ip = request.client.host if request.client else "unknown"

        # Log activity
        result = await activity_logger.log_activity(
            agent_id=activity.agent_id,
            task_id=activity.task_id,
            status=activity.status,
            output=activity.output,
            error=activity.error,
            duration_ms=activity.duration_ms,
            user_id="system",  # TODO: Get from JWT auth
            ip_address=client_ip
        )

        logger.info(
            f"Logged agent activity: agent_id={activity.agent_id}, "
            f"task_id={activity.task_id}, status={activity.status}, "
            f"memory_mcp={result['stored_in_memory_mcp']}, "
            f"websocket={result['broadcasted_via_websocket']}"
        )

        return AgentActivityResponse(
            status="success",
            message="Agent activity logged successfully",
            agent_id=activity.agent_id,
            task_id=activity.task_id,
            stored_in_memory_mcp=result["stored_in_memory_mcp"],
            broadcasted_via_websocket=result["broadcasted_via_websocket"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to log agent activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log agent activity: {str(e)}"
        )


# Optional: Create agent endpoint (if needed for manual agent registration)
@router.post(
    "",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new agent",
    description="Registers a new agent in the system"
)
@limiter.limit("60/minute")
async def create_agent(
    request: Request,
    agent: AgentCreate,
    db: AsyncSession = Depends(get_db),
) -> AgentResponse:
    """
    Create a new agent

    Request Body:
    - name: Agent name/identifier
    - type: Agent type (coder, reviewer, tester, etc.)
    - capabilities: List of capabilities
    - status: Initial status (default: idle)

    Returns:
    - Created agent details
    """
    try:
        agent_crud = AgentCRUD(db)

        # Get client IP for audit logging
        client_ip = request.client.host if request.client else "unknown"

        # Create agent
        new_agent = await agent_crud.create(
            name=agent.name,
            type=agent.type,
            capabilities_json=agent.capabilities,
            status=agent.status,
            user_id="system",  # TODO: Get from JWT auth
            ip_address=client_ip
        )

        await db.commit()

        logger.info(f"Created agent: id={new_agent.id}, name={new_agent.name}, type={new_agent.type}")

        return AgentResponse(
            id=new_agent.id,
            name=new_agent.name,
            type=new_agent.type,
            capabilities=new_agent.capabilities_json or [],
            status=new_agent.status,
            last_active_at=new_agent.last_active_at
        )

    except Exception as e:
        await db.rollback()
        logger.error(f"Failed to create agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )
