"""
Integration Example: Memory MCP Client with FastAPI Application

This example shows how to integrate the Memory MCP client into a FastAPI application
with proper dependency injection, error handling, and monitoring.
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncpg
import redis.asyncio as redis
import logging

from app.utils import (
    create_memory_mcp_client,
    memory_router,
    Intent,
    MemoryMCPClient
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Global clients (initialized in lifespan)
postgres_pool = None
redis_client = None
memory_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Initializes and cleans up resources
    """
    global postgres_pool, redis_client, memory_client

    # Startup: Initialize clients
    logger.info("Initializing database connections...")

    # PostgreSQL connection pool
    postgres_pool = await asyncpg.create_pool(
        host="localhost",
        port=5432,
        database="ruv_sparc",
        user="postgres",
        password="your-password",
        min_size=10,
        max_size=20
    )

    # Redis client
    redis_client = await redis.from_url(
        "redis://localhost:6379",
        encoding="utf-8",
        decode_responses=True
    )

    # Memory MCP client with circuit breaker
    memory_client = create_memory_mcp_client(
        postgres_client=postgres_pool,
        redis_client=redis_client,
        project_id="ruv-sparc-ui-dashboard",
        project_name="RUV SPARC UI Dashboard"
    )

    logger.info("✓ All clients initialized")

    # Check Memory MCP health
    health = await memory_client.health_check()
    if health["degraded_mode"]:
        logger.warning("⚠️ Memory MCP unavailable - starting in degraded mode")
    else:
        logger.info("✓ Memory MCP operational")

    yield

    # Shutdown: Cleanup
    logger.info("Shutting down...")
    await postgres_pool.close()
    await redis_client.close()
    logger.info("✓ Cleanup complete")


# Create FastAPI app with lifespan
app = FastAPI(
    title="RUV SPARC UI Dashboard API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency injection
async def get_memory_client() -> MemoryMCPClient:
    """Get Memory MCP client instance"""
    if memory_client is None:
        raise HTTPException(
            status_code=503,
            detail="Memory MCP client not initialized"
        )
    return memory_client


async def get_postgres():
    """Get PostgreSQL connection"""
    if postgres_pool is None:
        raise HTTPException(
            status_code=503,
            detail="Database not initialized"
        )
    async with postgres_pool.acquire() as conn:
        yield conn


async def get_redis():
    """Get Redis client"""
    if redis_client is None:
        raise HTTPException(
            status_code=503,
            detail="Redis not initialized"
        )
    return redis_client


# Include Memory MCP router
app.include_router(memory_router)


# Middleware for degraded mode warning
@app.middleware("http")
async def degraded_mode_middleware(request: Request, call_next):
    """
    Add degraded mode warning header if Memory MCP is unavailable
    Frontend can show warning banner based on this header
    """
    response = await call_next(request)

    # Check if in degraded mode
    if memory_client and memory_client._degraded_mode:
        response.headers["X-Degraded-Mode"] = "true"
        response.headers["X-Degraded-Reason"] = "Memory MCP unavailable"

    return response


# Example application endpoints using Memory MCP

@app.post("/api/v1/tasks")
async def create_task(
    task_data: dict,
    client: MemoryMCPClient = Depends(get_memory_client)
):
    """
    Create task and store in Memory MCP with automatic tagging
    """
    try:
        # Create task in database (your existing logic)
        task_id = task_data.get("id", "TASK-001")

        # Store in Memory MCP with tagging
        memory_result = await client.store(
            content=f"Created task: {task_data.get('title', 'Untitled')}",
            intent=Intent.IMPLEMENTATION,
            task_id=task_id,
            additional_metadata={
                "task_type": task_data.get("type"),
                "priority": task_data.get("priority"),
                "assignee": task_data.get("assignee")
            }
        )

        logger.info(f"Task {task_id} stored in {memory_result['storage']}")

        return {
            "task_id": task_id,
            "memory_storage": memory_result["storage"],
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/bugs/{bug_id}/fix")
async def record_bug_fix(
    bug_id: str,
    fix_data: dict,
    client: MemoryMCPClient = Depends(get_memory_client)
):
    """
    Record bug fix in Memory MCP for future reference
    """
    try:
        # Store bug fix with BUGFIX intent
        await client.store(
            content=fix_data.get("description", "Bug fix"),
            intent=Intent.BUGFIX,
            task_id=bug_id,
            additional_metadata={
                "root_cause": fix_data.get("root_cause"),
                "solution": fix_data.get("solution"),
                "tests_added": fix_data.get("tests_added", False),
                "severity": fix_data.get("severity")
            }
        )

        return {"status": "success", "bug_id": bug_id}

    except Exception as e:
        logger.error(f"Failed to record bug fix: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/tasks/{task_id}/similar")
async def find_similar_tasks(
    task_id: str,
    limit: int = 10,
    client: MemoryMCPClient = Depends(get_memory_client),
    postgres=Depends(get_postgres)
):
    """
    Find similar tasks using vector search
    """
    try:
        # Get the task content
        task = await postgres.fetchrow(
            "SELECT title, description FROM tasks WHERE id = $1",
            task_id
        )

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Vector search for similar tasks
        similar = await client.vector_search(
            query=f"{task['title']} {task['description']}",
            limit=limit
        )

        return {
            "task_id": task_id,
            "similar_tasks": similar,
            "total": len(similar)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to find similar tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/health")
async def health_check(
    client: MemoryMCPClient = Depends(get_memory_client)
):
    """
    Comprehensive health check including Memory MCP status
    """
    try:
        # Check Memory MCP
        mcp_health = await client.health_check()

        # Check PostgreSQL
        postgres_healthy = postgres_pool is not None
        if postgres_healthy:
            async with postgres_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")

        # Check Redis
        redis_healthy = redis_client is not None
        if redis_healthy:
            await redis_client.ping()

        return {
            "status": "healthy" if not mcp_health["degraded_mode"] else "degraded",
            "components": {
                "memory_mcp": {
                    "status": "healthy" if mcp_health["mcp_available"] else "degraded",
                    "circuit_breaker": mcp_health["circuit_breaker_state"],
                    "degraded_mode": mcp_health["degraded_mode"]
                },
                "postgresql": {
                    "status": "healthy" if postgres_healthy else "unhealthy"
                },
                "redis": {
                    "status": "healthy" if redis_healthy else "unhealthy"
                }
            }
        }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# Example CLI commands for manual testing
if __name__ == "__main__":
    import uvicorn

    print("""
    RUV SPARC UI Dashboard API with Memory MCP Integration

    Starting server...

    Available endpoints:
    - POST /api/v1/tasks - Create task with Memory MCP storage
    - POST /api/v1/bugs/{bug_id}/fix - Record bug fix
    - GET /api/v1/tasks/{task_id}/similar - Find similar tasks
    - GET /api/v1/health - Health check

    Memory MCP endpoints:
    - POST /api/v1/memory/search - Vector search
    - POST /api/v1/memory/store - Store data
    - GET /api/v1/memory/task/{task_id} - Get task history
    - GET /api/v1/memory/health - Memory MCP health

    Test commands:

    # Create task
    curl -X POST http://localhost:8000/api/v1/tasks \\
      -H "Content-Type: application/json" \\
      -d '{"id": "TASK-001", "title": "Test task", "type": "feature"}'

    # Record bug fix
    curl -X POST http://localhost:8000/api/v1/bugs/BUG-001/fix \\
      -H "Content-Type: application/json" \\
      -d '{"description": "Fixed null pointer", "severity": "high"}'

    # Vector search
    curl -X POST http://localhost:8000/api/v1/memory/search \\
      -H "Content-Type: application/json" \\
      -d '{"query": "authentication implementation", "limit": 10}'

    # Health check
    curl http://localhost:8000/api/v1/health

    # Memory MCP health
    curl http://localhost:8000/api/v1/memory/health
    """)

    uvicorn.run(
        "INTEGRATION_EXAMPLE:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
