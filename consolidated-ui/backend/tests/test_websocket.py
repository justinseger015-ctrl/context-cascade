"""
WebSocket Tests
Comprehensive tests for WebSocket functionality
"""

import pytest
import asyncio
import uuid
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

from app.websocket.connection_manager import ConnectionManager
from app.websocket.redis_pubsub import RedisPubSub
from app.websocket.heartbeat import HeartbeatManager
from app.websocket.message_types import (
    WSMessage,
    TaskStatusUpdate,
    AgentActivityUpdate,
    CalendarEventCreated,
    MessageType,
    PingMessage,
    PongMessage,
)


class TestMessageTypes:
    """Test WebSocket message types"""

    def test_ws_message_creation(self):
        """Test basic WSMessage creation"""
        message = WSMessage(
            type=MessageType.TASK_STATUS_UPDATE,
            event_id="evt_123",
            data={"task_id": "task_1", "status": "running"}
        )

        assert message.type == MessageType.TASK_STATUS_UPDATE
        assert message.event_id == "evt_123"
        assert message.data["task_id"] == "task_1"
        assert isinstance(message.timestamp, datetime)

    def test_task_status_update(self):
        """Test TaskStatusUpdate message"""
        message = TaskStatusUpdate(
            event_id="evt_456",
            data={
                "task_id": "task_2",
                "status": "completed",
                "progress": 100
            }
        )

        assert message.type == MessageType.TASK_STATUS_UPDATE
        assert message.data["status"] == "completed"

    def test_agent_activity_update(self):
        """Test AgentActivityUpdate message"""
        message = AgentActivityUpdate(
            event_id="evt_789",
            data={
                "agent_id": "agent_1",
                "action": "processing",
                "status": "active"
            }
        )

        assert message.type == MessageType.AGENT_ACTIVITY_UPDATE
        assert message.data["agent_id"] == "agent_1"

    def test_calendar_event_created(self):
        """Test CalendarEventCreated message"""
        message = CalendarEventCreated(
            event_id="evt_abc",
            data={
                "event_id": "cal_123",
                "title": "Team Meeting",
                "start_time": "2025-11-09T10:00:00Z"
            }
        )

        assert message.type == MessageType.CALENDAR_EVENT_CREATED
        assert message.data["title"] == "Team Meeting"

    def test_message_serialization(self):
        """Test message JSON serialization"""
        message = TaskStatusUpdate(
            event_id="evt_test",
            data={"task_id": "task_test"}
        )

        json_data = message.dict()

        assert json_data["type"] == "task_status_update"
        assert json_data["event_id"] == "evt_test"
        assert "timestamp" in json_data


class TestHeartbeatManager:
    """Test heartbeat management"""

    @pytest.fixture
    def heartbeat_manager(self):
        """Create heartbeat manager instance"""
        return HeartbeatManager(ping_interval=1, pong_timeout=2)

    def test_initial_state(self, heartbeat_manager):
        """Test initial heartbeat manager state"""
        assert len(heartbeat_manager.last_pong) == 0
        assert len(heartbeat_manager.heartbeat_tasks) == 0

    @pytest.mark.asyncio
    async def test_record_pong(self, heartbeat_manager):
        """Test recording pong from client"""
        connection_id = "conn_test_1"
        heartbeat_manager.record_pong(connection_id)

        assert connection_id in heartbeat_manager.last_pong
        assert heartbeat_manager.is_connection_alive(connection_id)

    @pytest.mark.asyncio
    async def test_connection_timeout(self, heartbeat_manager):
        """Test connection timeout detection"""
        connection_id = "conn_test_2"

        # Record old pong (before timeout threshold)
        heartbeat_manager.last_pong[connection_id] = (
            datetime.utcnow() - timedelta(seconds=10)
        )

        assert not heartbeat_manager.is_connection_alive(connection_id)

    def test_get_connection_health(self, heartbeat_manager):
        """Test connection health metrics"""
        connection_id = "conn_test_3"
        heartbeat_manager.record_pong(connection_id)

        health = heartbeat_manager.get_connection_health(connection_id)

        assert health["connection_id"] == connection_id
        assert health["status"] == "alive"
        assert health["last_pong"] is not None
        assert health["seconds_since_pong"] < 1

    def test_get_all_health_metrics(self, heartbeat_manager):
        """Test all health metrics"""
        # Add some connections
        for i in range(3):
            heartbeat_manager.record_pong(f"conn_{i}")

        metrics = heartbeat_manager.get_all_health_metrics()

        assert metrics["total_connections"] == 3
        assert metrics["alive_connections"] == 3
        assert metrics["dead_connections"] == 0
        assert len(metrics["connections"]) == 3


class TestConnectionManager:
    """Test connection manager"""

    @pytest.fixture
    async def connection_manager(self):
        """Create connection manager instance"""
        manager = ConnectionManager()

        # Mock Redis for testing
        manager.redis = AsyncMock()

        return manager

    @pytest.mark.asyncio
    async def test_authenticate_connection_valid(self, connection_manager):
        """Test valid JWT authentication"""
        # Mock JWT decoding
        with patch('app.websocket.connection_manager.jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user_123"}

            user_id = await connection_manager.authenticate_connection("valid_token")

            assert user_id == "user_123"
            mock_decode.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_connection_invalid(self, connection_manager):
        """Test invalid JWT authentication"""
        with patch('app.websocket.connection_manager.jwt.decode') as mock_decode:
            from jose import JWTError
            mock_decode.side_effect = JWTError("Invalid token")

            user_id = await connection_manager.authenticate_connection("invalid_token")

            assert user_id is None

    @pytest.mark.asyncio
    async def test_get_user_id(self, connection_manager):
        """Test getting user ID for connection"""
        connection_id = "conn_test"
        user_id = "user_123"

        # Set up test data
        connection_manager.user_connections[user_id] = {connection_id}
        connection_manager.redis.hget.return_value = user_id

        retrieved_user_id = await connection_manager.get_user_id(connection_id)

        assert retrieved_user_id == user_id

    @pytest.mark.asyncio
    async def test_send_personal_message(self, connection_manager):
        """Test sending message to specific connection"""
        connection_id = "conn_test"
        mock_websocket = AsyncMock()

        connection_manager.active_connections[connection_id] = mock_websocket

        message = WSMessage(
            type=MessageType.TASK_STATUS_UPDATE,
            event_id="evt_test",
            data={"test": "data"}
        )

        await connection_manager.send_personal_message(message, connection_id)

        mock_websocket.send_json.assert_called_once()

    @pytest.mark.asyncio
    async def test_broadcast(self, connection_manager):
        """Test broadcasting to all connections"""
        # Create mock connections
        mock_ws1 = AsyncMock()
        mock_ws2 = AsyncMock()
        mock_ws3 = AsyncMock()

        connection_manager.active_connections = {
            "conn_1": mock_ws1,
            "conn_2": mock_ws2,
            "conn_3": mock_ws3,
        }

        message = WSMessage(
            type=MessageType.AGENT_ACTIVITY_UPDATE,
            event_id="evt_broadcast",
            data={"broadcast": "test"}
        )

        await connection_manager.broadcast(message)

        # Verify all connections received message
        mock_ws1.send_json.assert_called_once()
        mock_ws2.send_json.assert_called_once()
        mock_ws3.send_json.assert_called_once()


class TestRedisPubSub:
    """Test Redis pub/sub functionality"""

    @pytest.fixture
    async def redis_pubsub(self):
        """Create Redis pub/sub instance"""
        pubsub = RedisPubSub()

        # Mock Redis for testing
        pubsub.redis = AsyncMock()
        pubsub.pubsub = AsyncMock()

        return pubsub

    @pytest.mark.asyncio
    async def test_publish_broadcast(self, redis_pubsub):
        """Test publishing broadcast message"""
        message = WSMessage(
            type=MessageType.TASK_STATUS_UPDATE,
            event_id="evt_test",
            data={"test": "broadcast"}
        )

        await redis_pubsub.publish_broadcast(message)

        redis_pubsub.redis.publish.assert_called_once()
        call_args = redis_pubsub.redis.publish.call_args
        assert call_args[0][0] == "ws:broadcast"

    @pytest.mark.asyncio
    async def test_publish_to_user(self, redis_pubsub):
        """Test publishing to user-specific channel"""
        user_id = "user_123"
        message = WSMessage(
            type=MessageType.AGENT_ACTIVITY_UPDATE,
            event_id="evt_user",
            data={"user": "message"}
        )

        await redis_pubsub.publish_to_user(user_id, message)

        redis_pubsub.redis.publish.assert_called_once()
        call_args = redis_pubsub.redis.publish.call_args
        assert call_args[0][0] == f"ws:user:{user_id}"

    @pytest.mark.asyncio
    async def test_publish_to_connection(self, redis_pubsub):
        """Test publishing to connection-specific channel"""
        connection_id = "conn_123"
        message = WSMessage(
            type=MessageType.CALENDAR_EVENT_CREATED,
            event_id="evt_conn",
            data={"connection": "message"}
        )

        await redis_pubsub.publish_to_connection(connection_id, message)

        redis_pubsub.redis.publish.assert_called_once()
        call_args = redis_pubsub.redis.publish.call_args
        assert call_args[0][0] == f"ws:connection:{connection_id}"

    @pytest.mark.asyncio
    async def test_subscribe(self, redis_pubsub):
        """Test subscribing to channel"""
        channel = "test_channel"

        async def handler(data):
            pass

        await redis_pubsub.subscribe(channel, handler)

        redis_pubsub.pubsub.subscribe.assert_called_once_with(channel)
        assert channel in redis_pubsub.channels


# Integration test example
@pytest.mark.integration
class TestWebSocketIntegration:
    """Integration tests for WebSocket system"""

    @pytest.mark.asyncio
    async def test_full_connection_flow(self):
        """Test complete connection flow"""
        # This would require a running FastAPI app and Redis
        # For now, this is a placeholder for integration tests
        pass

    @pytest.mark.asyncio
    async def test_multi_worker_broadcast(self):
        """Test broadcasting across multiple workers"""
        # This would test Redis pub/sub across multiple FastAPI workers
        pass

    @pytest.mark.asyncio
    async def test_reconnection_with_event_replay(self):
        """Test reconnection with event replay"""
        # This would test client reconnection and event replay
        pass


# Load testing example
@pytest.mark.load
class TestWebSocketLoad:
    """Load tests for WebSocket system"""

    @pytest.mark.asyncio
    async def test_10k_concurrent_connections(self):
        """Test 10k concurrent connections"""
        # This would create 10k WebSocket connections
        pass

    @pytest.mark.asyncio
    async def test_50k_concurrent_connections(self):
        """Test 50k concurrent connections (target)"""
        # This would create 50k WebSocket connections
        pass

    @pytest.mark.asyncio
    async def test_message_latency_under_load(self):
        """Test message latency with high load"""
        # This would measure message latency with many connections
        pass
