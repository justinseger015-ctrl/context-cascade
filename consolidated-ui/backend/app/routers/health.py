"""
Health Check Endpoint
Monitors system health, database connectivity, and Memory MCP availability
"""

import asyncio
import logging
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.database import get_db

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    database: str
    memory_mcp: str
    version: str = "1.0.0"


class DetailedHealthResponse(HealthResponse):
    """Detailed health check response with additional metrics"""
    uptime_seconds: float
    environment: str
    workers: int


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic health check",
    description="Returns basic health status of the API and its dependencies"
)
async def health_check(
    db: AsyncSession = Depends(get_db)
) -> HealthResponse:
    """
    Basic health check endpoint

    Checks:
    - API is running
    - Database connectivity
    - Memory MCP availability

    Returns:
        HealthResponse with status of all services
    """

    # Check database
    database_status = await check_database(db)

    # Check Memory MCP
    memory_mcp_status = await check_memory_mcp()

    # Determine overall status
    overall_status = "healthy"
    if database_status != "connected" or memory_mcp_status != "available":
        overall_status = "degraded"

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        database=database_status,
        memory_mcp=memory_mcp_status
    )


@router.get(
    "/health/detailed",
    response_model=DetailedHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Detailed health check",
    description="Returns detailed health status with additional metrics"
)
async def detailed_health_check(
    db: AsyncSession = Depends(get_db)
) -> DetailedHealthResponse:
    """
    Detailed health check endpoint with metrics

    Returns:
        DetailedHealthResponse with comprehensive status information
    """
    import time

    # Check database
    database_status = await check_database(db)

    # Check Memory MCP
    memory_mcp_status = await check_memory_mcp()

    # Calculate uptime (simplified - would use process start time in production)
    uptime = time.time() % 86400  # Seconds since midnight

    # Determine overall status
    overall_status = "healthy"
    if database_status != "connected" or memory_mcp_status != "available":
        overall_status = "degraded"

    return DetailedHealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        database=database_status,
        memory_mcp=memory_mcp_status,
        uptime_seconds=uptime,
        environment=settings.ENVIRONMENT,
        workers=settings.WORKERS
    )


async def check_database(db: AsyncSession) -> str:
    """
    Check database connectivity

    Args:
        db: Database session

    Returns:
        "connected" if database is accessible, "disconnected" otherwise
    """
    try:
        # Simple SELECT 1 query to test connectivity
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        return "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return "disconnected"


async def check_memory_mcp() -> str:
    """
    Check Memory MCP availability

    Returns:
        "available" if Memory MCP is accessible, "unavailable" otherwise
    """
    if not settings.MEMORY_MCP_ENABLED:
        return "disabled"

    try:
        # Attempt to connect to Memory MCP with timeout
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{settings.MEMORY_MCP_URL}/health")

            if response.status_code == 200:
                return "available"
            else:
                logger.warning(f"Memory MCP returned status {response.status_code}")
                return "degraded"

    except asyncio.TimeoutError:
        logger.warning("Memory MCP health check timed out")
        return "timeout"

    except httpx.ConnectError:
        logger.warning("Memory MCP connection failed")
        return "unavailable"

    except Exception as e:
        logger.error(f"Memory MCP health check failed: {e}")
        return "error"


@router.get(
    "/readiness",
    status_code=status.HTTP_200_OK,
    summary="Readiness probe",
    description="Kubernetes readiness probe endpoint"
)
async def readiness_check(
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Readiness probe for Kubernetes/container orchestration
    Returns 200 if service is ready to accept traffic
    """
    database_status = await check_database(db)

    if database_status != "connected":
        return {
            "ready": False,
            "reason": "database_unavailable"
        }

    return {
        "ready": True,
        "timestamp": datetime.utcnow()
    }


@router.get(
    "/liveness",
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
    description="Kubernetes liveness probe endpoint"
)
async def liveness_check() -> dict:
    """
    Liveness probe for Kubernetes/container orchestration
    Returns 200 if service is alive (simple check)
    """
    return {
        "alive": True,
        "timestamp": datetime.utcnow()
    }
