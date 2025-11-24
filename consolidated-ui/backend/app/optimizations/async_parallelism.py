"""
Async Parallelism Utilities for FastAPI Performance Optimization

Features:
- Parallel database queries with asyncio.gather()
- Batch operations for bulk inserts/updates
- Concurrent API calls
- Error handling with partial failures

P4_T8: API Performance Optimization
Target: Reduce latency through parallel execution
"""

import asyncio
import logging
from typing import Any, Callable, Coroutine, List, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

T = TypeVar('T')


async def gather_with_concurrency(
    n: int,
    *coros: Coroutine,
    return_exceptions: bool = False
) -> List[Any]:
    """
    Run coroutines with limited concurrency

    Args:
        n: Maximum concurrent coroutines
        *coros: Coroutines to execute
        return_exceptions: If True, return exceptions instead of raising

    Returns:
        List of results in same order as input coroutines

    Example:
        results = await gather_with_concurrency(
            5,
            fetch_tasks(),
            fetch_projects(),
            fetch_agents()
        )
    """
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro: Coroutine) -> Any:
        async with semaphore:
            return await coro

    return await asyncio.gather(
        *(sem_coro(c) for c in coros),
        return_exceptions=return_exceptions
    )


async def parallel_queries(
    db: AsyncSession,
    *queries
) -> List[Any]:
    """
    Execute multiple database queries in parallel

    Args:
        db: Database session
        *queries: SQLAlchemy select statements

    Returns:
        List of query results

    Example:
        tasks_query = select(ScheduledTask).where(...)
        projects_query = select(Project).where(...)

        tasks, projects = await parallel_queries(
            db,
            tasks_query,
            projects_query
        )
    """
    async def execute_query(query):
        result = await db.execute(query)
        return result.scalars().all()

    results = await asyncio.gather(
        *(execute_query(q) for q in queries),
        return_exceptions=False
    )

    return results


async def batch_insert(
    db: AsyncSession,
    model_class,
    data: List[dict],
    batch_size: int = 100
) -> List[Any]:
    """
    Batch insert records for improved performance

    Args:
        db: Database session
        model_class: SQLAlchemy model class
        data: List of dictionaries to insert
        batch_size: Number of records per batch

    Returns:
        List of created model instances

    Example:
        tasks_data = [
            {"name": "Task 1", "user_id": 1},
            {"name": "Task 2", "user_id": 1},
            ...
        ]

        created_tasks = await batch_insert(
            db,
            ScheduledTask,
            tasks_data,
            batch_size=50
        )
    """
    all_instances = []

    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        instances = [model_class(**item) for item in batch]

        db.add_all(instances)
        all_instances.extend(instances)

        logger.debug(f"Batch insert: {len(instances)} records")

    await db.commit()

    logger.info(f"Total inserted: {len(all_instances)} records")
    return all_instances


async def batch_update(
    db: AsyncSession,
    model_class,
    updates: List[tuple[int, dict]],
    batch_size: int = 100
) -> int:
    """
    Batch update records by ID

    Args:
        db: Database session
        model_class: SQLAlchemy model class
        updates: List of (id, update_dict) tuples
        batch_size: Number of updates per batch

    Returns:
        Number of records updated

    Example:
        updates = [
            (1, {"status": "completed"}),
            (2, {"status": "completed"}),
            ...
        ]

        updated_count = await batch_update(
            db,
            ScheduledTask,
            updates,
            batch_size=50
        )
    """
    updated_count = 0

    for i in range(0, len(updates), batch_size):
        batch = updates[i:i + batch_size]

        # Fetch instances in batch
        ids = [update[0] for update in batch]
        query = select(model_class).where(model_class.id.in_(ids))
        result = await db.execute(query)
        instances = {inst.id: inst for inst in result.scalars().all()}

        # Apply updates
        for record_id, update_data in batch:
            instance = instances.get(record_id)
            if instance:
                for key, value in update_data.items():
                    setattr(instance, key, value)
                updated_count += 1

        logger.debug(f"Batch update: {len(batch)} records")

    await db.commit()

    logger.info(f"Total updated: {updated_count} records")
    return updated_count


async def parallel_fetch_with_fallback(
    primary_fn: Callable[[], Coroutine[Any, Any, T]],
    fallback_fn: Callable[[], Coroutine[Any, Any, T]],
    timeout: float = 5.0
) -> T:
    """
    Fetch data with fallback if primary source times out

    Args:
        primary_fn: Primary async function to execute
        fallback_fn: Fallback async function if primary fails/timeouts
        timeout: Timeout in seconds for primary function

    Returns:
        Result from primary or fallback function

    Example:
        result = await parallel_fetch_with_fallback(
            lambda: fetch_from_cache(),
            lambda: fetch_from_database(),
            timeout=2.0
        )
    """
    try:
        result = await asyncio.wait_for(primary_fn(), timeout=timeout)
        return result

    except asyncio.TimeoutError:
        logger.warning(f"Primary function timed out after {timeout}s, using fallback")
        return await fallback_fn()

    except Exception as e:
        logger.error(f"Primary function failed: {e}, using fallback")
        return await fallback_fn()


async def map_async(
    fn: Callable[[T], Coroutine[Any, Any, Any]],
    items: List[T],
    max_concurrent: int = 10
) -> List[Any]:
    """
    Map async function over list with concurrency limit

    Args:
        fn: Async function to apply to each item
        items: List of items to process
        max_concurrent: Maximum concurrent executions

    Returns:
        List of results

    Example:
        async def process_task(task_id: int):
            # Process task
            return result

        results = await map_async(
            process_task,
            [1, 2, 3, 4, 5],
            max_concurrent=3
        )
    """
    return await gather_with_concurrency(
        max_concurrent,
        *(fn(item) for item in items)
    )


async def background_task(
    fn: Callable[[], Coroutine],
    on_error: Optional[Callable[[Exception], None]] = None
) -> asyncio.Task:
    """
    Execute async function as background task with error handling

    Args:
        fn: Async function to execute in background
        on_error: Optional error callback

    Returns:
        AsyncIO Task object

    Example:
        task = await background_task(
            lambda: send_notifications(),
            on_error=lambda e: logger.error(f"Notification failed: {e}")
        )
    """
    async def wrapped_fn():
        try:
            await fn()
        except Exception as e:
            logger.error(f"Background task error: {e}")
            if on_error:
                on_error(e)

    task = asyncio.create_task(wrapped_fn())
    return task


# Example usage in API endpoints:
"""
from app.optimizations.async_parallelism import parallel_queries, batch_insert

@router.get("/dashboard")
async def get_dashboard(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Execute multiple queries in parallel
    tasks_query = select(ScheduledTask).where(ScheduledTask.user_id == user_id)
    projects_query = select(Project).where(Project.user_id == user_id)
    agents_query = select(Agent).where(Agent.user_id == user_id)

    tasks, projects, agents = await parallel_queries(
        db,
        tasks_query,
        projects_query,
        agents_query
    )

    return {
        "tasks": [t.dict() for t in tasks],
        "projects": [p.dict() for p in projects],
        "agents": [a.dict() for a in agents]
    }


@router.post("/tasks/bulk")
async def bulk_create_tasks(
    tasks_data: List[TaskCreate],
    db: AsyncSession = Depends(get_db)
):
    # Batch insert for improved performance
    created_tasks = await batch_insert(
        db,
        ScheduledTask,
        [t.dict() for t in tasks_data],
        batch_size=100
    )

    return {"created": len(created_tasks)}
"""
