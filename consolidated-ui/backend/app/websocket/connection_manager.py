"""
WebSocket Connection Manager
Manages active WebSocket connections with Redis backing for multi-worker support
Targets 45-50k concurrent connections
"""

import asyncio
import logging
import uuid
from typing import Dict, Set, Optional
from datetime import datetime, timedelta
from fastapi import WebSocket, WebSocketDisconnect
import redis.asyncio as aioredis
from jose import JWTError, jwt

from app.core.config import settings
from .message_types import WSMessage, ErrorMessage, MessageType

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections with Redis backing for horizontal scaling

    Features:
    - Connection tracking with Redis SET (TTL-based cleanup)
    - JWT authentication on connection
    - Multi-worker coordination via Redis
    - Connection metadata storage
    - Target: 45-50k concurrent connections
    """

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, Set[str]] = {}  # user_id -> set of connection_ids
        self.redis: Optional[aioredis.Redis] = None
        self.connection_ttl = 3600  # 1 hour TTL for connection tracking

    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self.redis = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                max_connections=100,  # Connection pool for high concurrency
            )
            logger.info("ConnectionManager initialized with Redis")
        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()

    async def authenticate_connection(self, token: str) -> Optional[str]:
        """
        Authenticate WebSocket connection using JWT token

        Args:
            token: JWT token from client

        Returns:
            user_id if authentication successful, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                logger.warning("JWT token missing 'sub' claim")
                return None
            return user_id
        except JWTError as e:
            logger.warning(f"JWT authentication failed: {e}")
            return None

    async def connect(
        self,
        websocket: WebSocket,
        token: str,
        connection_id: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Accept and register a new WebSocket connection

        Args:
            websocket: FastAPI WebSocket instance
            token: JWT authentication token
            connection_id: Optional existing connection ID for reconnection

        Returns:
            Tuple of (connection_id, user_id)

        Raises:
            ValueError: If authentication fails
        """
        # Authenticate
        user_id = await self.authenticate_connection(token)
        if not user_id:
            await websocket.close(code=1008, reason="Authentication failed")
            raise ValueError("Authentication failed")

        # Accept connection
        await websocket.accept()

        # Generate or reuse connection ID
        if not connection_id:
            connection_id = str(uuid.uuid4())

        # Store connection locally
        self.active_connections[connection_id] = websocket

        # Track user connections
        if user_id not in self.user_connections:
            self.user_connections[user_id] = set()
        self.user_connections[user_id].add(connection_id)

        # Store in Redis with TTL
        await self._store_connection_in_redis(connection_id, user_id)

        logger.info(
            f"WebSocket connected: connection_id={connection_id}, "
            f"user_id={user_id}, total_connections={len(self.active_connections)}"
        )

        return connection_id, user_id

    async def disconnect(self, connection_id: str):
        """
        Remove a WebSocket connection

        Args:
            connection_id: Connection identifier
        """
        # Remove from local storage
        websocket = self.active_connections.pop(connection_id, None)

        # Find and remove from user_connections
        user_id = None
        for uid, conn_ids in self.user_connections.items():
            if connection_id in conn_ids:
                conn_ids.remove(connection_id)
                user_id = uid
                if not conn_ids:
                    del self.user_connections[uid]
                break

        # Remove from Redis
        await self._remove_connection_from_redis(connection_id)

        if websocket:
            try:
                await websocket.close()
            except Exception as e:
                logger.warning(f"Error closing websocket {connection_id}: {e}")

        logger.info(
            f"WebSocket disconnected: connection_id={connection_id}, "
            f"user_id={user_id}, remaining_connections={len(self.active_connections)}"
        )

    async def send_personal_message(
        self,
        message: WSMessage,
        connection_id: str
    ):
        """
        Send message to specific connection

        Args:
            message: Message to send
            connection_id: Target connection ID
        """
        websocket = self.active_connections.get(connection_id)
        if websocket:
            try:
                await websocket.send_json(message.dict())
            except Exception as e:
                logger.error(f"Error sending message to {connection_id}: {e}")
                await self.disconnect(connection_id)

    async def send_to_user(
        self,
        message: WSMessage,
        user_id: str
    ):
        """
        Send message to all connections of a user

        Args:
            message: Message to send
            user_id: Target user ID
        """
        connection_ids = self.user_connections.get(user_id, set())

        # Send to local connections
        for connection_id in list(connection_ids):
            await self.send_personal_message(message, connection_id)

    async def broadcast(self, message):
        """
        Broadcast message to all active connections

        Args:
            message: Message to broadcast (dict or WSMessage)
        """
        disconnected = []

        # Convert message to dict if needed
        message_dict = message.dict() if hasattr(message, 'dict') else message

        for connection_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message_dict)
            except Exception as e:
                logger.error(f"Error broadcasting to {connection_id}: {e}")
                disconnected.append(connection_id)

        # Clean up disconnected connections
        for connection_id in disconnected:
            await self.disconnect(connection_id)

    async def get_user_id(self, connection_id: str) -> Optional[str]:
        """
        Get user ID for a connection

        Args:
            connection_id: Connection identifier

        Returns:
            user_id or None
        """
        # Check Redis first for cross-worker support
        if self.redis:
            user_id = await self.redis.hget(
                f"ws:connection:{connection_id}",
                "user_id"
            )
            if user_id:
                return user_id

        # Fallback to local lookup
        for user_id, conn_ids in self.user_connections.items():
            if connection_id in conn_ids:
                return user_id

        return None

    async def get_connection_count(self) -> int:
        """
        Get total active connection count across all workers

        Returns:
            Total connection count
        """
        if self.redis:
            # Count connections in Redis
            keys = await self.redis.keys("ws:connection:*")
            return len(keys)

        return len(self.active_connections)

    async def _store_connection_in_redis(
        self,
        connection_id: str,
        user_id: str
    ):
        """Store connection metadata in Redis"""
        if self.redis:
            key = f"ws:connection:{connection_id}"
            await self.redis.hset(
                key,
                mapping={
                    "user_id": user_id,
                    "connected_at": datetime.utcnow().isoformat(),
                }
            )
            await self.redis.expire(key, self.connection_ttl)

            # Add to user's connection set
            user_set_key = f"ws:user:{user_id}:connections"
            await self.redis.sadd(user_set_key, connection_id)
            await self.redis.expire(user_set_key, self.connection_ttl)

    async def _remove_connection_from_redis(self, connection_id: str):
        """Remove connection from Redis"""
        if self.redis:
            # Get user_id before deleting
            key = f"ws:connection:{connection_id}"
            user_id = await self.redis.hget(key, "user_id")

            # Delete connection
            await self.redis.delete(key)

            # Remove from user's connection set
            if user_id:
                user_set_key = f"ws:user:{user_id}:connections"
                await self.redis.srem(user_set_key, connection_id)

    async def refresh_connection_ttl(self, connection_id: str):
        """
        Refresh connection TTL in Redis (called by heartbeat)

        Args:
            connection_id: Connection to refresh
        """
        if self.redis:
            key = f"ws:connection:{connection_id}"
            await self.redis.expire(key, self.connection_ttl)

            # Refresh user set TTL too
            user_id = await self.redis.hget(key, "user_id")
            if user_id:
                user_set_key = f"ws:user:{user_id}:connections"
                await self.redis.expire(user_set_key, self.connection_ttl)


# Global connection manager instance
connection_manager = ConnectionManager()
