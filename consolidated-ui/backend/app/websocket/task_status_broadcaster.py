"""
Task Status Broadcaster - Redis Pub/Sub for Real-Time Updates
Publishes task status changes to WebSocket clients via Redis pub/sub channel

Architecture:
1. Task update endpoint publishes to Redis channel 'task_status_update'
2. WebSocket listener subscribes to Redis channel
3. Broadcaster forwards messages to all connected WebSocket clients
4. Frontend updates Zustand store and re-renders UI components

Performance Target: <100ms end-to-end latency
"""

import asyncio
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime

import redis.asyncio as aioredis
from fastapi import WebSocket

from app.core.config import settings
from .connection_manager import ConnectionManager, connection_manager
from .message_types import WSMessage, MessageType

logger = logging.getLogger(__name__)


class TaskStatusBroadcaster:
    """
    Manages real-time task status broadcasting via Redis pub/sub

    Features:
    - Redis pub/sub for multi-worker coordination
    - Automatic reconnection on Redis failure
    - Message broadcasting to all connected WebSocket clients
    - Performance monitoring and latency tracking
    """

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.redis: Optional[aioredis.Redis] = None
        self.pubsub: Optional[aioredis.client.PubSub] = None
        self.listener_task: Optional[asyncio.Task] = None
        self.channel_name = "task_status_update"
        self.is_running = False

    async def initialize(self):
        """Initialize Redis connection and pub/sub"""
        try:
            self.redis = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                max_connections=50,  # Separate pool for pub/sub
            )
            logger.info("TaskStatusBroadcaster initialized with Redis")
        except Exception as e:
            logger.error(f"Failed to initialize Redis for broadcaster: {e}")
            raise

    async def start_listening(self):
        """
        Start listening to Redis pub/sub channel for task status updates
        Runs in background as asyncio task
        """
        if self.is_running:
            logger.warning("TaskStatusBroadcaster already running")
            return

        try:
            self.pubsub = self.redis.pubsub()
            await self.pubsub.subscribe(self.channel_name)
            self.is_running = True

            logger.info(f"TaskStatusBroadcaster listening on channel: {self.channel_name}")

            # Start background listener task
            self.listener_task = asyncio.create_task(self._listen_loop())

        except Exception as e:
            logger.error(f"Failed to start Redis pub/sub listener: {e}")
            self.is_running = False
            raise

    async def stop_listening(self):
        """Stop listening to Redis pub/sub channel"""
        self.is_running = False

        if self.listener_task:
            self.listener_task.cancel()
            try:
                await self.listener_task
            except asyncio.CancelledError:
                pass

        if self.pubsub:
            await self.pubsub.unsubscribe(self.channel_name)
            await self.pubsub.close()
            self.pubsub = None

        logger.info("TaskStatusBroadcaster stopped listening")

    async def close(self):
        """Close Redis connection"""
        await self.stop_listening()

        if self.redis:
            await self.redis.close()
            self.redis = None

    async def _listen_loop(self):
        """
        Background loop that listens for Redis pub/sub messages
        and broadcasts to WebSocket clients
        """
        logger.info("TaskStatusBroadcaster listen loop started")

        try:
            while self.is_running:
                try:
                    # Get next message from Redis pub/sub channel
                    message = await self.pubsub.get_message(
                        ignore_subscribe_messages=True,
                        timeout=1.0
                    )

                    if message and message["type"] == "message":
                        await self._handle_redis_message(message)

                    # Small delay to prevent tight loop
                    await asyncio.sleep(0.01)

                except asyncio.CancelledError:
                    logger.info("Listen loop cancelled")
                    break

                except Exception as e:
                    logger.error(f"Error in listen loop: {e}", exc_info=True)
                    # Continue listening despite errors
                    await asyncio.sleep(1.0)

        finally:
            logger.info("TaskStatusBroadcaster listen loop stopped")

    async def _handle_redis_message(self, message: Dict[str, Any]):
        """
        Handle incoming Redis pub/sub message and broadcast to WebSocket clients

        Args:
            message: Redis pub/sub message containing task status update
        """
        try:
            start_time = datetime.utcnow()

            # Parse message data (already decoded as JSON string)
            data = json.loads(message["data"])

            # Validate required fields
            required_fields = ["task_id", "status", "updated_at"]
            if not all(field in data for field in required_fields):
                logger.warning(f"Invalid task status update message: missing fields - {data}")
                return

            # Create WebSocket message (compatible with existing frontend format)
            ws_message = {
                "type": "task_status_update",
                "payload": {
                    "taskId": str(data["task_id"]),
                    "status": data["status"],
                    "updatedAt": data["updated_at"],
                    "output": data.get("output"),
                    "error": data.get("error"),
                    "assignee": data.get("assignee"),
                    "projectId": data.get("project_id"),
                },
                "timestamp": start_time.isoformat()
            }

            # Broadcast to all connected WebSocket clients
            await self.connection_manager.broadcast(ws_message)

            # Calculate latency
            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000

            logger.info(
                f"Task status update broadcasted: task_id={data['task_id']}, "
                f"status={data['status']}, latency={latency_ms:.2f}ms"
            )

            # Alert if latency exceeds target
            if latency_ms > 100:
                logger.warning(
                    f"Task status broadcast latency exceeded target: {latency_ms:.2f}ms > 100ms"
                )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Redis message as JSON: {e}")

        except Exception as e:
            logger.error(f"Error handling Redis message: {e}", exc_info=True)

    async def publish_task_status_update(
        self,
        task_id: int,
        status: str,
        updated_at: datetime,
        output: Optional[str] = None,
        error: Optional[str] = None,
        assignee: Optional[str] = None,
        project_id: Optional[int] = None,
    ):
        """
        Publish task status update to Redis pub/sub channel
        Called by task update endpoints when status changes

        Args:
            task_id: Task identifier
            status: New task status (pending, running, completed, failed)
            updated_at: Update timestamp
            output: Optional task output text
            error: Optional error message
            assignee: Optional assigned agent/user
            project_id: Optional project identifier
        """
        if not self.redis:
            logger.error("Cannot publish: Redis not initialized")
            return

        try:
            message_data = {
                "task_id": task_id,
                "status": status,
                "updated_at": updated_at.isoformat(),
                "output": output,
                "error": error,
                "assignee": assignee,
                "project_id": project_id,
            }

            # Publish to Redis channel
            await self.redis.publish(
                self.channel_name,
                json.dumps(message_data)
            )

            logger.debug(
                f"Published task status update: task_id={task_id}, status={status}"
            )

        except Exception as e:
            logger.error(f"Failed to publish task status update: {e}", exc_info=True)


# Global broadcaster instance
task_status_broadcaster = TaskStatusBroadcaster(connection_manager)
