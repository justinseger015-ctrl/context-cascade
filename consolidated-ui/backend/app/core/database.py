"""
Database configuration and session management with async SQLAlchemy.

Uses async_sessionmaker for SQLAlchemy 2.0+ with asyncpg driver.
Maps to PostgreSQL schema from P1_T2.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
import os

# Database URL from environment (asyncpg driver for async PostgreSQL)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://sparc_user:sparc_password@localhost:5432/sparc_dashboard"
)

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # SQL logging for development
    future=True,  # SQLAlchemy 2.0 style
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Connection pool size
    max_overflow=20,  # Maximum overflow connections
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy loading issues
    autocommit=False,
    autoflush=False,
)

# Base class for ORM models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI endpoints to get database session.

    Yields:
        AsyncSession: Database session for executing queries.

    Example:
        @app.get("/tasks")
        async def get_tasks(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(ScheduledTask))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database tables.

    Creates all tables defined in Base metadata.
    Should be called during application startup.
    """
    async with engine.begin() as conn:
        # Import all models to ensure they're registered with Base
        from app.models.scheduled_task import ScheduledTask
        from app.models.project import Project
        from app.models.agent import Agent
        from app.models.execution_result import ExecutionResult
        from app.models.audit_log import AuditLog

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close database connections.

    Should be called during application shutdown.
    """
    await engine.dispose()
