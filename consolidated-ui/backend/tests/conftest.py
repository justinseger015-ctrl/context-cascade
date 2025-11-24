"""
Pytest Configuration and Fixtures
Provides shared fixtures for all test suites
"""

import asyncio
import os
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["DATABASE_URL"] = "postgresql+asyncpg://test:test@localhost:5432/test_db"
os.environ["REDIS_URL"] = "redis://localhost:6379/1"


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Database fixtures
@pytest_asyncio.fixture(scope="function")
async def test_db_engine():
    """Create test database engine"""
    from app.models import Base

    engine = create_async_engine(
        os.getenv("DATABASE_URL"),
        echo=False,
        poolclass=NullPool,  # No connection pooling in tests
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async_session = sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client with database session override"""
    from app.database import get_db
    from app.main import app

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# Mock fixtures for unit tests
@pytest.fixture
def mock_db_session():
    """Mock database session for unit tests"""
    mock = AsyncMock(spec=AsyncSession)
    mock.commit = AsyncMock()
    mock.rollback = AsyncMock()
    mock.refresh = AsyncMock()
    mock.execute = AsyncMock()
    mock.scalar = AsyncMock()
    mock.scalars = AsyncMock()
    mock.add = MagicMock()
    mock.delete = AsyncMock()
    mock.flush = AsyncMock()
    return mock


@pytest.fixture
def mock_redis_client():
    """Mock Redis client for unit tests"""
    mock = AsyncMock()
    mock.publish = AsyncMock(return_value=1)
    mock.subscribe = AsyncMock()
    mock.unsubscribe = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock(return_value=True)
    mock.delete = AsyncMock(return_value=1)
    mock.ping = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_memory_mcp_client():
    """Mock Memory MCP client for unit tests"""
    mock = Mock()
    mock.is_healthy = Mock(return_value=True)
    mock.vector_search = AsyncMock(return_value={
        "results": [],
        "total": 0
    })
    mock.memory_store = AsyncMock(return_value={
        "success": True,
        "key": "test-key"
    })
    mock.fallback_mode = False
    mock.circuit_state = "CLOSED"
    return mock


# Sample data fixtures
@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        "name": "Test Project",
        "description": "A test project",
        "status": "active",
        "sparc_mode": "specification",
        "metadata": {
            "created_by": "test_user",
            "tags": ["test", "sample"]
        }
    }


@pytest.fixture
def sample_agent_data():
    """Sample agent data for testing"""
    return {
        "name": "test-agent",
        "agent_type": "researcher",
        "status": "active",
        "capabilities": ["research", "analysis"],
        "metadata": {
            "version": "1.0.0",
            "environment": "test"
        }
    }


@pytest.fixture
def sample_task_data():
    """Sample scheduled task data for testing"""
    return {
        "name": "test-task",
        "description": "A test scheduled task",
        "cron_expression": "0 0 * * *",
        "command": "echo 'test'",
        "enabled": True,
        "metadata": {
            "timeout": 300,
            "retries": 3
        }
    }


@pytest.fixture
def sample_execution_result_data():
    """Sample execution result data for testing"""
    return {
        "status": "success",
        "output": "Test output",
        "error": None,
        "duration_seconds": 1.5,
        "metadata": {
            "exit_code": 0,
            "memory_used": "100MB"
        }
    }


# WebSocket fixtures
@pytest.fixture
def mock_websocket():
    """Mock WebSocket connection for testing"""
    mock = AsyncMock()
    mock.accept = AsyncMock()
    mock.send_text = AsyncMock()
    mock.send_json = AsyncMock()
    mock.receive_text = AsyncMock()
    mock.receive_json = AsyncMock()
    mock.close = AsyncMock()
    mock.client = Mock()
    mock.client.host = "127.0.0.1"
    return mock


@pytest_asyncio.fixture
async def websocket_connection_manager():
    """WebSocket ConnectionManager instance for testing"""
    from app.websocket.connection_manager import ConnectionManager

    manager = ConnectionManager()
    yield manager

    # Cleanup all connections
    await manager.disconnect_all()


# Performance testing fixtures
@pytest.fixture
def performance_tracker():
    """Track performance metrics for tests"""
    import time

    class PerformanceTracker:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        def start(self):
            self.start_time = time.time()

        def stop(self):
            self.end_time = time.time()

        @property
        def duration(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None

    return PerformanceTracker()


# Concurrent testing fixtures
@pytest.fixture
def concurrent_executor():
    """Execute multiple async tasks concurrently for testing race conditions"""
    async def execute_concurrent(tasks, count=10):
        """Execute task multiple times concurrently"""
        return await asyncio.gather(*[tasks() for _ in range(count)])

    return execute_concurrent


# Pytest markers
def pytest_configure(config):
    """Register custom pytest markers"""
    config.addinivalue_line("markers", "unit: Unit tests with mocked dependencies")
    config.addinivalue_line("markers", "integration: Integration tests with real database")
    config.addinivalue_line("markers", "websocket: WebSocket connection tests")
    config.addinivalue_line("markers", "circuit_breaker: Circuit breaker and fallback tests")
    config.addinivalue_line("markers", "performance: Performance and load tests")
    config.addinivalue_line("markers", "concurrent: Concurrent operation tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


# Cleanup hooks
@pytest.fixture(autouse=True)
async def cleanup_after_test():
    """Cleanup resources after each test"""
    yield
    # Add any global cleanup logic here
    await asyncio.sleep(0)  # Allow pending tasks to complete
