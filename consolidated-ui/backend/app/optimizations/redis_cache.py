"""
Redis Query Caching for API Performance Optimization

Features:
- TTL-based caching (5-minute default)
- Automatic cache invalidation on writes
- Cache key hashing for query parameters
- Performance metrics tracking

P4_T8: API Performance Optimization
Target: P99 latency <200ms for GET endpoints
"""

import hashlib
import json
import logging
from functools import wraps
from typing import Any, Callable, Optional

import redis.asyncio as redis
from fastapi import Request

logger = logging.getLogger(__name__)

# Redis client (initialized in main.py lifespan)
redis_client: Optional[redis.Redis] = None


async def init_redis(redis_url: str = "redis://localhost:6379") -> None:
    """
    Initialize Redis client connection pool

    Args:
        redis_url: Redis connection URL
    """
    global redis_client
    redis_client = redis.from_url(
        redis_url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=50,  # Connection pool size
        socket_keepalive=True,
        socket_timeout=5.0,
    )
    logger.info(f"✅ Redis cache initialized: {redis_url}")


async def close_redis() -> None:
    """Close Redis client connections"""
    if redis_client:
        await redis_client.close()
        logger.info("✅ Redis connections closed")


def generate_cache_key(prefix: str, **kwargs) -> str:
    """
    Generate cache key from prefix and parameters

    Args:
        prefix: Cache key prefix (e.g., "tasks", "projects")
        **kwargs: Query parameters to include in key

    Returns:
        Hashed cache key

    Example:
        generate_cache_key("tasks", user_id=1, status="enabled")
        # Returns: "tasks:a1b2c3d4..."
    """
    # Sort params for consistent hashing
    sorted_params = sorted(kwargs.items())
    params_str = json.dumps(sorted_params, sort_keys=True)

    # Create SHA256 hash of parameters
    params_hash = hashlib.sha256(params_str.encode()).hexdigest()[:16]

    return f"{prefix}:{params_hash}"


async def get_cached(key: str) -> Optional[Any]:
    """
    Get cached value from Redis

    Args:
        key: Cache key

    Returns:
        Cached value (parsed JSON) or None if not found
    """
    if not redis_client:
        return None

    try:
        cached_value = await redis_client.get(key)
        if cached_value:
            logger.debug(f"Cache HIT: {key}")
            return json.loads(cached_value)

        logger.debug(f"Cache MISS: {key}")
        return None

    except Exception as e:
        logger.error(f"Redis get error for key {key}: {e}")
        return None


async def set_cached(key: str, value: Any, ttl: int = 300) -> bool:
    """
    Set cached value in Redis with TTL

    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time-to-live in seconds (default: 5 minutes)

    Returns:
        True if successful, False otherwise
    """
    if not redis_client:
        return False

    try:
        serialized_value = json.dumps(value, default=str)
        await redis_client.setex(key, ttl, serialized_value)
        logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
        return True

    except Exception as e:
        logger.error(f"Redis set error for key {key}: {e}")
        return False


async def invalidate_cache(pattern: str) -> int:
    """
    Invalidate cache entries matching pattern

    Args:
        pattern: Redis key pattern (e.g., "tasks:*")

    Returns:
        Number of keys deleted
    """
    if not redis_client:
        return 0

    try:
        keys = await redis_client.keys(pattern)
        if keys:
            deleted = await redis_client.delete(*keys)
            logger.info(f"Cache INVALIDATE: {pattern} ({deleted} keys)")
            return deleted
        return 0

    except Exception as e:
        logger.error(f"Redis invalidate error for pattern {pattern}: {e}")
        return 0


def cached_endpoint(
    prefix: str,
    ttl: int = 300,
    key_params: Optional[list[str]] = None
):
    """
    Decorator for caching FastAPI endpoint responses

    Args:
        prefix: Cache key prefix
        ttl: Time-to-live in seconds
        key_params: Query params to include in cache key (default: all)

    Example:
        @router.get("/tasks")
        @cached_endpoint("tasks", ttl=300, key_params=["user_id", "status"])
        async def get_tasks(user_id: int, status: str):
            # Endpoint logic
            return tasks
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request object if present
            request: Optional[Request] = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            # Build cache key from specified params or all kwargs
            cache_params = {}
            if key_params:
                cache_params = {k: v for k, v in kwargs.items() if k in key_params}
            else:
                cache_params = kwargs

            cache_key = generate_cache_key(prefix, **cache_params)

            # Try to get from cache
            cached_result = await get_cached(cache_key)
            if cached_result is not None:
                if request:
                    request.state.cache_hit = True
                return cached_result

            # Cache miss - execute function
            if request:
                request.state.cache_hit = False

            result = await func(*args, **kwargs)

            # Cache the result
            await set_cached(cache_key, result, ttl)

            return result

        return wrapper
    return decorator


def invalidate_on_write(prefix: str):
    """
    Decorator for invalidating cache on write operations

    Args:
        prefix: Cache key prefix to invalidate

    Example:
        @router.post("/tasks")
        @invalidate_on_write("tasks")
        async def create_task(task: TaskCreate):
            # Create task logic
            return new_task
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Execute the write operation
            result = await func(*args, **kwargs)

            # Invalidate related cache entries
            await invalidate_cache(f"{prefix}:*")

            return result

        return wrapper
    return decorator


async def get_cache_stats() -> dict[str, Any]:
    """
    Get Redis cache statistics

    Returns:
        Dictionary with cache stats (keys, memory, hit rate)
    """
    if not redis_client:
        return {"error": "Redis not connected"}

    try:
        info = await redis_client.info("stats")

        return {
            "connected": True,
            "keys": await redis_client.dbsize(),
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
            "hit_rate": (
                info.get("keyspace_hits", 0) /
                max(1, info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0))
            ) * 100,
            "memory_used": info.get("used_memory_human", "N/A"),
        }

    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return {"error": str(e)}


# Example usage in routers:
"""
from app.optimizations.redis_cache import cached_endpoint, invalidate_on_write

@router.get("/tasks")
@cached_endpoint("tasks", ttl=300, key_params=["user_id", "status"])
async def get_tasks(
    user_id: int,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    # Query database
    query = select(ScheduledTask).where(ScheduledTask.user_id == user_id)
    if status:
        query = query.where(ScheduledTask.status == status)

    result = await db.execute(query)
    tasks = result.scalars().all()

    return [task.dict() for task in tasks]


@router.post("/tasks")
@invalidate_on_write("tasks")
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    # Create task
    new_task = ScheduledTask(**task.dict())
    db.add(new_task)
    await db.commit()

    return new_task.dict()
"""
