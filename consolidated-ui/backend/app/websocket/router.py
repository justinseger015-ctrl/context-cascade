"""
WebSocket Router
FastAPI router for WebSocket endpoint with authentication and multi-worker support
"""

import asyncio
import logging
import uuid
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from datetime import datetime

from .connection_manager import connection_manager
from .redis_pubsub import redis_pubsub
from .heartbeat import heartbeat_manager
from .message_types import (
    WSMessage,
    MessageType,
    PongMessage,
    ErrorMessage,
    AckMessage,
)

logger = logging.getLogger(__name__)

router = APIRouter()


async def on_startup():
    """Initialize WebSocket services on application startup"""
    try:
        await connection_manager.initialize()
        await redis_pubsub.initialize()

        # Subscribe to broadcast channel
        await redis_pubsub.subscribe(
            "ws:broadcast",
            handle_broadcast_message
        )

        logger.info("WebSocket services initialized")
    except Exception as e:
        logger.error(f"Failed to initialize WebSocket services: {e}")
        raise


async def on_shutdown():
    """Cleanup WebSocket services on application shutdown"""
    try:
        await redis_pubsub.close()
        await connection_manager.close()
        logger.info("WebSocket services closed")
    except Exception as e:
        logger.error(f"Error during WebSocket shutdown: {e}")


async def handle_broadcast_message(data: dict):
    """
    Handler for broadcast messages from Redis pub/sub

    Args:
        data: Message data from Redis
    """
    try:
        message = WSMessage(**data)
        await connection_manager.broadcast(message)
        logger.debug(f"Broadcast message: {message.type}")
    except Exception as e:
        logger.error(f"Error handling broadcast message: {e}")


async def handle_disconnect(connection_id: str):
    """
    Callback when connection fails heartbeat

    Args:
        connection_id: Connection identifier
    """
    logger.info(f"Disconnecting stale connection: {connection_id}")
    await connection_manager.disconnect(connection_id)
    heartbeat_manager.stop_heartbeat(connection_id)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="JWT authentication token"),
    connection_id: Optional[str] = Query(
        None,
        description="Connection ID for reconnection"
    ),
    last_event_id: Optional[str] = Query(
        None,
        description="Last event ID received (for replay)"
    )
):
    """
    WebSocket endpoint with authentication and reconnection support

    Features:
    - JWT authentication
    - Automatic heartbeat (ping/pong)
    - Reconnection with event replay
    - Multi-worker coordination via Redis

    Args:
        websocket: WebSocket connection
        token: JWT authentication token
        connection_id: Optional connection ID for reconnection
        last_event_id: Optional last event ID for event replay
    """
    conn_id = None
    user_id = None

    try:
        # Connect and authenticate
        conn_id, user_id = await connection_manager.connect(
            websocket,
            token,
            connection_id
        )

        # Start heartbeat
        heartbeat_manager.start_heartbeat(
            conn_id,
            websocket,
            on_disconnect_callback=handle_disconnect
        )

        # Subscribe to user-specific channel
        user_channel = f"ws:user:{user_id}"
        await redis_pubsub.subscribe(
            user_channel,
            lambda data: handle_user_message(conn_id, data)
        )

        # Send acknowledgment
        ack_message = AckMessage(
            event_id=str(uuid.uuid4()),
            ack_event_id=last_event_id or "initial_connect"
        )
        await websocket.send_json(ack_message.dict())

        # TODO: If last_event_id provided, replay missed events from Redis/DB
        if last_event_id:
            logger.info(
                f"Reconnection requested with last_event_id={last_event_id} "
                f"(replay not yet implemented)"
            )

        # Listen for client messages
        while True:
            try:
                data = await websocket.receive_json()
                await handle_client_message(conn_id, user_id, data)
            except WebSocketDisconnect:
                logger.info(f"Client disconnected: {conn_id}")
                break
            except Exception as e:
                logger.error(f"Error receiving message from {conn_id}: {e}")
                error_message = ErrorMessage(
                    event_id=str(uuid.uuid4()),
                    error="Invalid message format",
                    details={"error": str(e)}
                )
                await websocket.send_json(error_message.dict())

    except ValueError as e:
        # Authentication failed
        logger.warning(f"Authentication failed: {e}")
        return

    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)

    finally:
        # Cleanup
        if conn_id:
            await connection_manager.disconnect(conn_id)
            heartbeat_manager.stop_heartbeat(conn_id)

            if user_id:
                user_channel = f"ws:user:{user_id}"
                await redis_pubsub.unsubscribe(user_channel)


async def handle_client_message(
    connection_id: str,
    user_id: str,
    data: dict
):
    """
    Handle messages from WebSocket client

    Args:
        connection_id: Connection identifier
        user_id: User identifier
        data: Message data from client
    """
    try:
        message_type = data.get("type")

        if message_type == MessageType.PONG:
            # Record pong for heartbeat
            heartbeat_manager.record_pong(connection_id)

            # Refresh connection TTL in Redis
            await connection_manager.refresh_connection_ttl(connection_id)

        elif message_type == MessageType.ACK:
            # Client acknowledging receipt of message
            ack_event_id = data.get("ack_event_id")
            logger.debug(f"Client ack for event {ack_event_id}")

        else:
            logger.warning(f"Unknown message type from client: {message_type}")

    except Exception as e:
        logger.error(f"Error handling client message: {e}", exc_info=True)


async def handle_user_message(connection_id: str, data: dict):
    """
    Handler for user-specific messages from Redis pub/sub

    Args:
        connection_id: Target connection ID
        data: Message data from Redis
    """
    try:
        message = WSMessage(**data)
        await connection_manager.send_personal_message(message, connection_id)
        logger.debug(f"Sent user message to {connection_id}: {message.type}")
    except Exception as e:
        logger.error(f"Error handling user message: {e}")


@router.get("/ws/health")
async def websocket_health():
    """
    WebSocket health endpoint
    Returns connection statistics and health metrics
    """
    total_connections = await connection_manager.get_connection_count()
    health_metrics = heartbeat_manager.get_all_health_metrics()

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "connections": {
            "total": total_connections,
            "local": len(connection_manager.active_connections),
            "alive": health_metrics["alive_connections"],
            "dead": health_metrics["dead_connections"],
        },
        "redis": {
            "connected": connection_manager.redis is not None,
            "pubsub_connected": redis_pubsub.redis is not None,
        }
    }
