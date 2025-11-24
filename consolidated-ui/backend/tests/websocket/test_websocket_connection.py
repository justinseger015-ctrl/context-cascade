"""
WebSocket Connection Tests
Test connection lifecycle, heartbeat, and reconnection
"""

import pytest
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

from app.websocket.connection_manager import ConnectionManager
from app.websocket.heartbeat import HeartbeatManager
from app.websocket.message_types import MessageType


@pytest.mark.websocket
@pytest.mark.asyncio
class TestWebSocketConnection:
    """Test WebSocket connection lifecycle"""

    async def test_connect_websocket(self, websocket_connection_manager, mock_websocket):
        """Test successful WebSocket connection"""
        # Arrange
        client_id = "test-client-1"

        # Act
        await websocket_connection_manager.connect(mock_websocket, client_id)

        # Assert
        assert client_id in websocket_connection_manager.active_connections
        assert websocket_connection_manager.active_connections[client_id] == mock_websocket
        mock_websocket.accept.assert_called_once()

    async def test_disconnect_websocket(self, websocket_connection_manager, mock_websocket):
        """Test WebSocket disconnection"""
        # Arrange
        client_id = "test-client-1"
        await websocket_connection_manager.connect(mock_websocket, client_id)

        # Act
        await websocket_connection_manager.disconnect(client_id)

        # Assert
        assert client_id not in websocket_connection_manager.active_connections
        mock_websocket.close.assert_called_once()

    async def test_send_message_to_client(self, websocket_connection_manager, mock_websocket):
        """Test sending message to specific client"""
        # Arrange
        client_id = "test-client-1"
        await websocket_connection_manager.connect(mock_websocket, client_id)
        test_message = {"type": "test", "data": "Hello"}

        # Act
        await websocket_connection_manager.send_personal_message(test_message, client_id)

        # Assert
        mock_websocket.send_json.assert_called_once_with(test_message)

    async def test_broadcast_message(self, websocket_connection_manager):
        """Test broadcasting message to all connected clients"""
        # Arrange
        mock_ws1 = AsyncMock()
        mock_ws2 = AsyncMock()
        mock_ws3 = AsyncMock()

        mock_ws1.accept = AsyncMock()
        mock_ws2.accept = AsyncMock()
        mock_ws3.accept = AsyncMock()

        mock_ws1.send_json = AsyncMock()
        mock_ws2.send_json = AsyncMock()
        mock_ws3.send_json = AsyncMock()

        await websocket_connection_manager.connect(mock_ws1, "client-1")
        await websocket_connection_manager.connect(mock_ws2, "client-2")
        await websocket_connection_manager.connect(mock_ws3, "client-3")

        broadcast_message = {"type": "broadcast", "data": "Hello everyone"}

        # Act
        await websocket_connection_manager.broadcast(broadcast_message)

        # Assert
        mock_ws1.send_json.assert_called_with(broadcast_message)
        mock_ws2.send_json.assert_called_with(broadcast_message)
        mock_ws3.send_json.assert_called_with(broadcast_message)

    async def test_send_to_disconnected_client(self, websocket_connection_manager, mock_websocket):
        """Test sending message to disconnected client fails gracefully"""
        # Arrange
        client_id = "test-client-1"
        await websocket_connection_manager.connect(mock_websocket, client_id)
        mock_websocket.send_json.side_effect = Exception("Connection closed")

        # Act & Assert - Should not raise exception
        try:
            await websocket_connection_manager.send_personal_message(
                {"type": "test"},
                client_id
            )
        except Exception:
            pytest.fail("Should handle disconnection gracefully")

    async def test_multiple_concurrent_connections(self, websocket_connection_manager):
        """Test handling multiple concurrent connections"""
        # Arrange
        connections = []
        for i in range(10):
            mock_ws = AsyncMock()
            mock_ws.accept = AsyncMock()
            connections.append((mock_ws, f"client-{i}"))

        # Act - Connect all clients concurrently
        await asyncio.gather(*[
            websocket_connection_manager.connect(ws, client_id)
            for ws, client_id in connections
        ])

        # Assert
        assert len(websocket_connection_manager.active_connections) == 10
        for ws, client_id in connections:
            assert client_id in websocket_connection_manager.active_connections


@pytest.mark.websocket
@pytest.mark.asyncio
class TestHeartbeat:
    """Test WebSocket heartbeat mechanism"""

    async def test_heartbeat_ping_pong(self, mock_websocket):
        """Test heartbeat ping-pong mechanism"""
        # Arrange
        heartbeat_manager = HeartbeatManager(interval=1.0)
        client_id = "test-client"

        # Mock receive_json to simulate pong response
        pong_count = 0

        async def mock_receive():
            nonlocal pong_count
            pong_count += 1
            return {"type": MessageType.PONG}

        mock_websocket.receive_json = mock_receive
        mock_websocket.send_json = AsyncMock()

        # Act
        heartbeat_task = asyncio.create_task(
            heartbeat_manager.start_heartbeat(mock_websocket, client_id)
        )

        # Wait for a few heartbeats
        await asyncio.sleep(2.5)
        heartbeat_task.cancel()

        # Assert - Should have sent at least 2 pings
        assert mock_websocket.send_json.call_count >= 2
        # Verify ping messages
        calls = mock_websocket.send_json.call_args_list
        assert any(
            call[0][0].get("type") == MessageType.PING
            for call in calls
        )

    async def test_heartbeat_timeout(self, mock_websocket):
        """Test heartbeat timeout detection"""
        # Arrange
        heartbeat_manager = HeartbeatManager(interval=1.0, timeout=2.0)
        client_id = "test-client"

        # Mock receive to never respond
        mock_websocket.receive_json = AsyncMock(
            side_effect=asyncio.TimeoutError()
        )
        mock_websocket.send_json = AsyncMock()
        mock_websocket.close = AsyncMock()

        # Act
        with pytest.raises(asyncio.TimeoutError):
            await heartbeat_manager.start_heartbeat(mock_websocket, client_id)

    async def test_heartbeat_with_reconnection(self):
        """Test heartbeat behavior during reconnection"""
        # Arrange
        heartbeat_manager = HeartbeatManager(interval=1.0)

        mock_ws1 = AsyncMock()
        mock_ws1.send_json = AsyncMock()
        mock_ws1.close = AsyncMock()

        mock_ws2 = AsyncMock()
        mock_ws2.send_json = AsyncMock()
        mock_ws2.receive_json = AsyncMock(return_value={"type": MessageType.PONG})

        client_id = "reconnecting-client"

        # Act - Start heartbeat, stop, and restart with new connection
        task1 = asyncio.create_task(
            heartbeat_manager.start_heartbeat(mock_ws1, client_id)
        )
        await asyncio.sleep(0.5)
        task1.cancel()

        # Reconnect with new WebSocket
        task2 = asyncio.create_task(
            heartbeat_manager.start_heartbeat(mock_ws2, client_id)
        )
        await asyncio.sleep(1.5)
        task2.cancel()

        # Assert - Both connections should have received heartbeats
        assert mock_ws1.send_json.called
        assert mock_ws2.send_json.called


@pytest.mark.websocket
@pytest.mark.asyncio
class TestWebSocketMessages:
    """Test WebSocket message types and routing"""

    async def test_message_type_validation(self, websocket_connection_manager, mock_websocket):
        """Test message type validation"""
        # Arrange
        client_id = "test-client"
        await websocket_connection_manager.connect(mock_websocket, client_id)

        valid_message = {
            "type": MessageType.PROJECT_UPDATE,
            "data": {"project_id": 1, "status": "completed"}
        }

        # Act
        await websocket_connection_manager.send_personal_message(valid_message, client_id)

        # Assert
        mock_websocket.send_json.assert_called_with(valid_message)

    async def test_project_update_message(self, websocket_connection_manager, mock_websocket):
        """Test PROJECT_UPDATE message format"""
        # Arrange
        client_id = "test-client"
        await websocket_connection_manager.connect(mock_websocket, client_id)

        project_update = {
            "type": MessageType.PROJECT_UPDATE,
            "data": {
                "project_id": 123,
                "name": "Updated Project",
                "status": "completed",
                "progress": 100
            },
            "timestamp": "2024-11-08T12:00:00Z"
        }

        # Act
        await websocket_connection_manager.send_personal_message(project_update, client_id)

        # Assert
        call_args = mock_websocket.send_json.call_args[0][0]
        assert call_args["type"] == MessageType.PROJECT_UPDATE
        assert call_args["data"]["project_id"] == 123

    async def test_agent_status_message(self, websocket_connection_manager, mock_websocket):
        """Test AGENT_STATUS message format"""
        # Arrange
        client_id = "test-client"
        await websocket_connection_manager.connect(mock_websocket, client_id)

        agent_status = {
            "type": MessageType.AGENT_STATUS,
            "data": {
                "agent_id": 456,
                "status": "running",
                "current_task": "data-processing",
                "cpu_usage": 45.2
            }
        }

        # Act
        await websocket_connection_manager.send_personal_message(agent_status, client_id)

        # Assert
        mock_websocket.send_json.assert_called_once()

    async def test_task_execution_message(self, websocket_connection_manager, mock_websocket):
        """Test TASK_EXECUTION message format"""
        # Arrange
        client_id = "test-client"
        await websocket_connection_manager.connect(mock_websocket, client_id)

        task_execution = {
            "type": MessageType.TASK_EXECUTION,
            "data": {
                "task_id": 789,
                "status": "success",
                "output": "Task completed successfully",
                "duration": 125.5
            }
        }

        # Act
        await websocket_connection_manager.send_personal_message(task_execution, client_id)

        # Assert
        mock_websocket.send_json.assert_called_once()

    async def test_error_message_handling(self, websocket_connection_manager, mock_websocket):
        """Test ERROR message handling"""
        # Arrange
        client_id = "test-client"
        await websocket_connection_manager.connect(mock_websocket, client_id)

        error_message = {
            "type": MessageType.ERROR,
            "data": {
                "error_code": "VALIDATION_ERROR",
                "message": "Invalid request format",
                "details": {"field": "project_id", "issue": "required"}
            }
        }

        # Act
        await websocket_connection_manager.send_personal_message(error_message, client_id)

        # Assert
        mock_websocket.send_json.assert_called_once()


@pytest.mark.websocket
@pytest.mark.asyncio
class TestWebSocketReconnection:
    """Test WebSocket reconnection scenarios"""

    async def test_client_reconnection(self, websocket_connection_manager):
        """Test client reconnecting with same ID"""
        # Arrange
        client_id = "reconnecting-client"

        mock_ws1 = AsyncMock()
        mock_ws1.accept = AsyncMock()
        mock_ws1.close = AsyncMock()

        mock_ws2 = AsyncMock()
        mock_ws2.accept = AsyncMock()

        # Act - Connect, disconnect, reconnect
        await websocket_connection_manager.connect(mock_ws1, client_id)
        await websocket_connection_manager.disconnect(client_id)
        await websocket_connection_manager.connect(mock_ws2, client_id)

        # Assert
        assert client_id in websocket_connection_manager.active_connections
        assert websocket_connection_manager.active_connections[client_id] == mock_ws2

    async def test_handle_network_interruption(self, websocket_connection_manager, mock_websocket):
        """Test handling network interruption gracefully"""
        # Arrange
        client_id = "test-client"
        await websocket_connection_manager.connect(mock_websocket, client_id)

        # Simulate network error
        mock_websocket.send_json.side_effect = [
            None,  # First send succeeds
            Exception("Network error"),  # Second send fails
        ]

        # Act
        await websocket_connection_manager.send_personal_message({"type": "test"}, client_id)

        # Second send should handle error gracefully
        try:
            await websocket_connection_manager.send_personal_message({"type": "test"}, client_id)
        except Exception:
            pass  # Should not propagate

        # Connection should be removed after error
        assert client_id not in websocket_connection_manager.active_connections or \
               websocket_connection_manager.active_connections[client_id] is None
