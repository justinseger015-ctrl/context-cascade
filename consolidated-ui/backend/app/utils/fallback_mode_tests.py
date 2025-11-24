"""
Fallback Mode Tests for Memory MCP Client
Tests circuit breaker behavior and degraded mode operation

Test scenarios:
1. Memory MCP healthy - normal operation
2. Memory MCP down - fallback to PostgreSQL + Redis
3. Circuit breaker open - immediate fallback
4. Circuit breaker half-open - recovery testing
5. Stale data serving from Redis cache
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta

from .memory_mcp_client import MemoryMCPClient, create_memory_mcp_client
from .tagging_protocol import TaggingProtocol, Intent, AgentCategory
from app.utils.memory_mcp_circuit_breaker import CircuitBreaker, CircuitBreakerState


@pytest.fixture
def mock_postgres():
    """Mock PostgreSQL client"""
    mock = Mock()
    mock.execute = AsyncMock()
    mock.fetch = AsyncMock(return_value=[])
    mock.fetchrow = AsyncMock(return_value=None)
    return mock


@pytest.fixture
def mock_redis():
    """Mock Redis client"""
    mock = Mock()
    mock.setex = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    return mock


@pytest.fixture
def tagger():
    """Create test tagging protocol"""
    return TaggingProtocol(
        agent_id="test-agent",
        agent_category=AgentCategory.BACKEND,
        capabilities=["testing"],
        project_id="test-project",
        project_name="Test Project"
    )


@pytest.fixture
def circuit_breaker():
    """Create test circuit breaker"""
    return CircuitBreaker(
        failure_threshold=3,
        timeout_duration=5,  # Short timeout for testing
        half_open_max_calls=2
    )


@pytest.fixture
def client(tagger, circuit_breaker, mock_postgres, mock_redis):
    """Create test Memory MCP client"""
    return MemoryMCPClient(
        tagger=tagger,
        circuit_breaker=circuit_breaker,
        postgres_client=mock_postgres,
        redis_client=mock_redis,
        mcp_endpoint="http://localhost:3000"
    )


class TestNormalOperation:
    """Test normal operation when Memory MCP is healthy"""

    @pytest.mark.asyncio
    async def test_store_success(self, client):
        """Test successful storage to Memory MCP"""
        result = await client.store(
            content="Test content",
            intent=Intent.TESTING,
            task_id="TEST-001"
        )

        assert result["status"] == "success"
        assert result["storage"] == "memory_mcp"
        assert result["task_id"] == "TEST-001"
        assert "metadata" in result

    @pytest.mark.asyncio
    async def test_vector_search_success(self, client):
        """Test successful vector search"""
        results = await client.vector_search(
            query="test query",
            limit=10
        )

        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_health_check_healthy(self, client):
        """Test health check when Memory MCP is healthy"""
        health = await client.health_check()

        assert health["status"] == "healthy"
        assert health["degraded_mode"] is False
        assert health["mcp_available"] is True


class TestFallbackMode:
    """Test fallback mode when Memory MCP is unavailable"""

    @pytest.mark.asyncio
    async def test_store_fallback_to_postgres(self, client):
        """Test fallback to PostgreSQL when Memory MCP is down"""
        # Simulate Memory MCP failure
        with patch.object(client, '_store_to_mcp', side_effect=Exception("MCP down")):
            result = await client.store(
                content="Test content",
                intent=Intent.TESTING,
                task_id="TEST-002"
            )

            assert result["status"] == "degraded"
            assert result["storage"] == "postgresql_fallback"
            assert "warning" in result
            assert client._degraded_mode is True

    @pytest.mark.asyncio
    async def test_vector_search_fallback(self, client):
        """Test fallback to PostgreSQL text search"""
        # Simulate Memory MCP failure
        with patch.object(client, '_vector_search_mcp', side_effect=Exception("MCP down")):
            results = await client.vector_search(
                query="test query",
                limit=10
            )

            assert isinstance(results, list)
            assert client._degraded_mode is True

    @pytest.mark.asyncio
    async def test_redis_cache_fallback(self, client, mock_redis):
        """Test serving stale data from Redis cache"""
        # Mock Redis returning cached data
        cached_data = {
            "content": "Cached content",
            "metadata": {
                "project": {"task_id": "TEST-003"}
            }
        }
        import json
        mock_redis.get.return_value = json.dumps(cached_data)

        # Simulate Memory MCP failure
        with patch.object(client, '_get_task_from_mcp', side_effect=Exception("MCP down")):
            result = await client.get_task_history(task_id="TEST-003")

            assert result["source"] == "redis_cache_stale"
            assert "warning" in result
            assert result["task"]["content"] == "Cached content"


class TestCircuitBreakerBehavior:
    """Test circuit breaker state transitions"""

    @pytest.mark.asyncio
    async def test_circuit_opens_after_failures(self, client, circuit_breaker):
        """Test circuit breaker opens after consecutive failures"""
        # Simulate 3 consecutive failures (threshold)
        with patch.object(client, '_store_to_mcp', side_effect=Exception("MCP down")):
            for i in range(3):
                await client.store(
                    content=f"Test {i}",
                    intent=Intent.TESTING,
                    task_id=f"TEST-{i}"
                )

            # Circuit should be open now
            assert circuit_breaker.state == CircuitBreakerState.OPEN

    @pytest.mark.asyncio
    async def test_circuit_half_open_recovery(self, client, circuit_breaker):
        """Test circuit breaker half-open state and recovery"""
        # Open the circuit
        with patch.object(client, '_store_to_mcp', side_effect=Exception("MCP down")):
            for i in range(3):
                await client.store(
                    content=f"Test {i}",
                    intent=Intent.TESTING,
                    task_id=f"TEST-{i}"
                )

        assert circuit_breaker.state == CircuitBreakerState.OPEN

        # Wait for timeout to transition to half-open
        await asyncio.sleep(6)  # Circuit breaker timeout is 5 seconds

        # Next call should transition to half-open
        with patch.object(client, '_store_to_mcp', return_value={"success": True}):
            await client.store(
                content="Recovery test",
                intent=Intent.TESTING,
                task_id="TEST-RECOVERY"
            )

            assert circuit_breaker.state == CircuitBreakerState.HALF_OPEN

    @pytest.mark.asyncio
    async def test_circuit_closes_after_success(self, client, circuit_breaker):
        """Test circuit breaker closes after successful calls in half-open state"""
        # Open the circuit
        with patch.object(client, '_store_to_mcp', side_effect=Exception("MCP down")):
            for i in range(3):
                await client.store(
                    content=f"Test {i}",
                    intent=Intent.TESTING,
                    task_id=f"TEST-{i}"
                )

        # Wait for timeout
        await asyncio.sleep(6)

        # Make successful calls to close circuit
        with patch.object(client, '_store_to_mcp', return_value={"success": True}):
            for i in range(2):  # Half-open max calls is 2
                await client.store(
                    content=f"Success {i}",
                    intent=Intent.TESTING,
                    task_id=f"TEST-SUCCESS-{i}"
                )

            # Circuit should be closed now
            assert circuit_breaker.state == CircuitBreakerState.CLOSED


class TestHealthMonitoring:
    """Test health monitoring and degraded mode detection"""

    @pytest.mark.asyncio
    async def test_health_check_degraded(self, client):
        """Test health check in degraded mode"""
        # Simulate Memory MCP failure
        with patch.object(client, '_ping_mcp', side_effect=Exception("MCP down")):
            health = await client.health_check()

            assert health["status"] == "degraded"
            assert health["degraded_mode"] is True
            assert health["mcp_available"] is False
            assert health["fallback_available"] is True

    @pytest.mark.asyncio
    async def test_health_check_rate_limiting(self, client):
        """Test health check rate limiting"""
        # First check
        health1 = await client.health_check()

        # Immediate second check should return cached result
        health2 = await client.health_check()

        assert health2["status"] == "cached"

    @pytest.mark.asyncio
    async def test_degraded_mode_warning_banner(self, client):
        """Test that degraded mode is detectable for UI warning banner"""
        # Trigger degraded mode
        with patch.object(client, '_store_to_mcp', side_effect=Exception("MCP down")):
            await client.store(
                content="Test",
                intent=Intent.TESTING,
                task_id="TEST-001"
            )

        # Check that health check shows degraded mode
        health = await client.health_check()
        assert health["degraded_mode"] is True

        # This can be used by UI to show warning banner:
        # "Memory MCP unavailable - operating in degraded mode with limited search capabilities"


class TestTaggingProtocol:
    """Test WHO/WHEN/PROJECT/WHY tagging"""

    @pytest.mark.asyncio
    async def test_automatic_tagging(self, client):
        """Test that all storage operations include required tags"""
        result = await client.store(
            content="Test content",
            intent=Intent.IMPLEMENTATION,
            user_id="user123",
            task_id="TASK-001",
            additional_metadata={"feature": "auth"}
        )

        metadata = result["metadata"]

        # Verify WHO tags
        assert "who" in metadata
        assert metadata["who"]["agent_id"] == "test-agent"
        assert metadata["who"]["user_id"] == "user123"

        # Verify WHEN tags
        assert "when" in metadata
        assert "iso_timestamp" in metadata["when"]
        assert "unix_timestamp" in metadata["when"]
        assert "readable" in metadata["when"]

        # Verify PROJECT tags
        assert "project" in metadata
        assert metadata["project"]["task_id"] == "TASK-001"
        assert metadata["project"]["project_id"] == "test-project"

        # Verify WHY tags
        assert "why" in metadata
        assert metadata["why"]["intent"] == "implementation"

    @pytest.mark.asyncio
    async def test_auto_generated_task_id(self, client):
        """Test automatic task ID generation when not provided"""
        result = await client.store(
            content="Test content",
            intent=Intent.TESTING
        )

        metadata = result["metadata"]
        task_id = metadata["project"]["task_id"]

        # Should have auto-generated task ID
        assert task_id.startswith("auto-")
        assert len(task_id) > 5


# Integration test (requires actual Memory MCP server)
@pytest.mark.integration
class TestMemoryMCPIntegration:
    """Integration tests requiring actual Memory MCP server"""

    @pytest.mark.asyncio
    async def test_end_to_end_storage_and_retrieval(self):
        """Test end-to-end storage and retrieval with real Memory MCP"""
        # This test should only run when Memory MCP is available
        pytest.skip("Requires Memory MCP server running")

    @pytest.mark.asyncio
    async def test_kill_memory_mcp_server(self):
        """
        Manual test: Kill Memory MCP server and verify system continues

        Steps:
        1. Start Memory MCP server
        2. Store some data
        3. Kill Memory MCP server
        4. Attempt storage - should fallback to PostgreSQL
        5. Attempt search - should fallback to PostgreSQL text search
        6. Check health - should show degraded mode
        7. Restart Memory MCP server
        8. Verify circuit breaker recovers
        """
        pytest.skip("Manual test - requires external server control")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
