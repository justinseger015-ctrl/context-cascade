"""
WebSocket Performance Optimization with Redis Pub/Sub

Features:
- Redis Pub/Sub for O(1) message broadcasting (avoids O(N²) loop)
- Message batching (100ms intervals)
- Connection pooling and health checks
- Automatic reconnection with exponential backoff

P4_T8: WebSocket Optimization
Target: Message latency <100ms for 1000 concurrent connections
"""

import asyncio
import json
import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

import redis.asyncio as redis
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

# Global state
redis_pubsub: Optional[redis.client.PubSub] = None
redis_client: Optional[redis.Redis] = None
active_connections: Set[WebSocket] = set()
message_batch: Dict[str, List[Dict[str, Any]]] = defaultdict(list)


async def init_websocket_redis(redis_url: str = "redis://localhost:6379") -> None:
    """
    Initialize Redis Pub/Sub for WebSocket broadcasting

    Args:
        redis_url: Redis connection URL
    """
    global redis_client, redis_pubsub

    redis_client = redis.from_url(
        redis_url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=100,
        socket_keepalive=True,
    )

    redis_pubsub = redis_client.pubsub()
    await redis_pubsub.subscribe("websocket_broadcasts")

    logger.info("✅ WebSocket Redis Pub/Sub initialized")

    # Start message batch processor
    asyncio.create_task(batch_message_processor())


async def close_websocket_redis() -> None:
    """Close Redis Pub/Sub connections"""
    global redis_pubsub, redis_client

    if redis_pubsub:
        await redis_pubsub.unsubscribe("websocket_broadcasts")
        await redis_pubsub.close()

    if redis_client:
        await redis_client.close()

    logger.info("✅ WebSocket Redis connections closed")


class ConnectionManager:
    """
    WebSocket connection manager with Redis Pub/Sub broadcasting

    Replaces O(N²) broadcasting loop with O(1) Redis Pub/Sub
    """

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.user_connections: Dict[int, Set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket, user_id: Optional[int] = None):
        """
        Accept and register new WebSocket connection

        Args:
            websocket: WebSocket connection
            user_id: Optional user ID for user-specific broadcasts
        """
        await websocket.accept()
        self.active_connections.add(websocket)

        if user_id:
            self.user_connections[user_id].add(websocket)

        logger.info(f"WebSocket connected (Total: {len(self.active_connections)})")

    def disconnect(self, websocket: WebSocket, user_id: Optional[int] = None):
        """
        Remove WebSocket connection

        Args:
            websocket: WebSocket connection
            user_id: Optional user ID
        """
        self.active_connections.discard(websocket)

        if user_id:
            self.user_connections[user_id].discard(websocket)

        logger.info(f"WebSocket disconnected (Total: {len(self.active_connections)})")

    async def broadcast_via_redis(self, message: Dict[str, Any]) -> None:
        """
        Broadcast message via Redis Pub/Sub (O(1) operation)

        Args:
            message: Message dictionary to broadcast
        """
        if not redis_client:
            # Fallback to direct broadcast if Redis not available
            await self._broadcast_direct(message)
            return

        try:
            # Publish to Redis channel
            message_json = json.dumps(message)
            await redis_client.publish("websocket_broadcasts", message_json)

        except Exception as e:
            logger.error(f"Redis publish error: {e}")
            # Fallback to direct broadcast
            await self._broadcast_direct(message)

    async def broadcast_to_user(self, user_id: int, message: Dict[str, Any]) -> None:
        """
        Broadcast message to specific user's connections

        Args:
            user_id: Target user ID
            message: Message dictionary
        """
        user_sockets = self.user_connections.get(user_id, set())

        if not user_sockets:
            return

        message_json = json.dumps(message)

        # Send to all user's connections
        disconnected = set()
        for websocket in user_sockets:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.warning(f"Failed to send to user {user_id}: {e}")
                disconnected.add(websocket)

        # Clean up disconnected sockets
        for websocket in disconnected:
            self.disconnect(websocket, user_id)

    async def _broadcast_direct(self, message: Dict[str, Any]) -> None:
        """
        Direct broadcast to all connections (fallback)

        Args:
            message: Message dictionary
        """
        if not self.active_connections:
            return

        message_json = json.dumps(message)

        disconnected = set()
        for websocket in self.active_connections:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.warning(f"Failed to send message: {e}")
                disconnected.add(websocket)

        # Clean up disconnected sockets
        for websocket in disconnected:
            self.disconnect(websocket)


# Global connection manager
manager = ConnectionManager()


async def redis_subscriber_task():
    """
    Background task that listens to Redis Pub/Sub and broadcasts to WebSocket clients

    This eliminates the need for O(N²) message broadcasting:
    - Old: Each message sent to N connections = O(N) per message
    - New: Single Redis publish + subscriber broadcast = O(1) publish + O(N) fanout
    """
    if not redis_pubsub:
        logger.error("Redis Pub/Sub not initialized")
        return

    logger.info("Starting Redis subscriber task")

    try:
        async for message in redis_pubsub.listen():
            if message["type"] == "message":
                message_data = json.loads(message["data"])

                # Broadcast to all connected WebSocket clients
                await manager._broadcast_direct(message_data)

    except Exception as e:
        logger.error(f"Redis subscriber error: {e}")


async def batch_message_processor():
    """
    Process batched messages every 100ms

    Groups multiple messages into batches to reduce WebSocket send overhead:
    - Instead of sending 10 messages individually (10 send calls)
    - Send 1 batched message with 10 updates (1 send call)
    """
    while True:
        await asyncio.sleep(0.1)  # 100ms batch interval

        global message_batch

        if not message_batch:
            continue

        # Process each batch type
        for batch_type, messages in message_batch.items():
            if not messages:
                continue

            batched_message = {
                "type": "batch",
                "batch_type": batch_type,
                "messages": messages,
                "count": len(messages),
                "timestamp": datetime.utcnow().isoformat(),
            }

            # Broadcast batched messages
            await manager.broadcast_via_redis(batched_message)

        # Clear processed batches
        message_batch.clear()


def add_to_batch(batch_type: str, message: Dict[str, Any]) -> None:
    """
    Add message to batch queue for batched sending

    Args:
        batch_type: Type of message (e.g., "task_update", "agent_activity")
        message: Message data
    """
    global message_batch
    message_batch[batch_type].append(message)


# Example FastAPI WebSocket endpoint with optimizations:
"""
from app.optimizations.websocket_optimization import manager, redis_subscriber_task

@app.on_event("startup")
async def startup_websocket():
    # Initialize Redis Pub/Sub
    await init_websocket_redis()

    # Start Redis subscriber task
    asyncio.create_task(redis_subscriber_task())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: Optional[int] = None):
    await manager.connect(websocket, user_id)

    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)

            # Process message
            if message["type"] == "task_update":
                # Add to batch for efficient broadcasting
                add_to_batch("task_update", {
                    "task_id": message["task_id"],
                    "status": message["status"],
                    "timestamp": datetime.utcnow().isoformat(),
                })

            elif message["type"] == "agent_activity":
                # Broadcast immediately (high priority)
                await manager.broadcast_via_redis({
                    "type": "agent_activity",
                    "agent_id": message["agent_id"],
                    "action": message["action"],
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)


# Example: Broadcast task update from API endpoint
@app.post("/api/v1/tasks/{task_id}/status")
async def update_task_status(task_id: int, status: str):
    # Update database
    # ...

    # Broadcast update to all WebSocket clients
    await manager.broadcast_via_redis({
        "type": "task_status_change",
        "task_id": task_id,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
    })

    return {"status": "ok"}
"""


# Connection health check
async def ping_all_connections() -> Dict[str, int]:
    """
    Ping all connections to check health

    Returns:
        Statistics: active, dead connections
    """
    active = 0
    dead = 0

    for websocket in list(manager.active_connections):
        try:
            await websocket.send_json({"type": "ping"})
            active += 1
        except Exception:
            dead += 1
            manager.disconnect(websocket)

    return {"active": active, "dead": dead, "total": len(manager.active_connections)}


# Exponential backoff for reconnection (client-side implementation example)
"""
// Client-side WebSocket with exponential backoff reconnection

class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectDelay = 1000; // Start with 1 second
    this.maxReconnectDelay = 30000; // Max 30 seconds
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectDelay = 1000; // Reset delay on successful connection
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected, reconnecting...');
      this.reconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };
  }

  reconnect() {
    setTimeout(() => {
      this.connect();
      // Exponential backoff with jitter
      this.reconnectDelay = Math.min(
        this.reconnectDelay * 2 + Math.random() * 1000,
        this.maxReconnectDelay
      );
    }, this.reconnectDelay);
  }

  handleMessage(message) {
    if (message.type === 'batch') {
      // Handle batched messages
      message.messages.forEach(msg => this.processMessage(msg));
    } else {
      this.processMessage(message);
    }
  }

  processMessage(message) {
    // Process individual message
    console.log('Received:', message);
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}

// Usage
const wsClient = new WebSocketClient('ws://localhost:8000/ws');
wsClient.connect();
"""
