"""
Redis Pub/Sub for WebSocket Broadcasting
Enables message broadcasting across multiple FastAPI workers
"""

import asyncio
import logging
import json
from typing import Callable, Optional, Dict, Any
import redis.asyncio as aioredis

from app.core.config import settings
from .message_types import WSMessage, MessageType

logger = logging.getLogger(__name__)


class RedisPubSub:
    """
    Redis Pub/Sub manager for broadcasting WebSocket messages across workers

    Channels:
    - ws:broadcast - Broadcast to all connections
    - ws:user:{user_id} - Send to specific user's connections
    - ws:connection:{connection_id} - Send to specific connection
    """

    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self.pubsub: Optional[aioredis.client.PubSub] = None
        self.channels: Dict[str, Callable] = {}
        self._listening_task: Optional[asyncio.Task] = None

    async def initialize(self):
        """Initialize Redis pub/sub connection"""
        try:
            self.redis = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                max_connections=50,
            )
            self.pubsub = self.redis.pubsub()
            logger.info("RedisPubSub initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Redis pub/sub: {e}")
            raise

    async def close(self):
        """Close Redis pub/sub connection"""
        if self._listening_task:
            self._listening_task.cancel()
            try:
                await self._listening_task
            except asyncio.CancelledError:
                pass

        if self.pubsub:
            await self.pubsub.close()

        if self.redis:
            await self.redis.close()

    async def subscribe(
        self,
        channel: str,
        handler: Callable[[Dict[str, Any]], None]
    ):
        """
        Subscribe to a channel with a message handler

        Args:
            channel: Redis channel name
            handler: Async function to handle received messages
        """
        if not self.pubsub:
            raise RuntimeError("RedisPubSub not initialized")

        self.channels[channel] = handler
        await self.pubsub.subscribe(channel)
        logger.info(f"Subscribed to channel: {channel}")

        # Start listening if not already running
        if not self._listening_task or self._listening_task.done():
            self._listening_task = asyncio.create_task(self._listen())

    async def unsubscribe(self, channel: str):
        """
        Unsubscribe from a channel

        Args:
            channel: Redis channel name
        """
        if not self.pubsub:
            return

        await self.pubsub.unsubscribe(channel)
        self.channels.pop(channel, None)
        logger.info(f"Unsubscribed from channel: {channel}")

    async def publish_broadcast(self, message: WSMessage):
        """
        Publish message to broadcast channel

        Args:
            message: Message to broadcast to all connections
        """
        await self._publish("ws:broadcast", message.dict())

    async def publish_to_user(self, user_id: str, message: WSMessage):
        """
        Publish message to user-specific channel

        Args:
            user_id: Target user ID
            message: Message to send
        """
        channel = f"ws:user:{user_id}"
        await self._publish(channel, message.dict())

    async def publish_to_connection(
        self,
        connection_id: str,
        message: WSMessage
    ):
        """
        Publish message to connection-specific channel

        Args:
            connection_id: Target connection ID
            message: Message to send
        """
        channel = f"ws:connection:{connection_id}"
        await self._publish(channel, message.dict())

    async def _publish(self, channel: str, data: Dict[str, Any]):
        """
        Internal publish method

        Args:
            channel: Redis channel
            data: Message data (will be JSON-encoded)
        """
        if not self.redis:
            logger.warning("Cannot publish: Redis not initialized")
            return

        try:
            message_json = json.dumps(data, default=str)
            await self.redis.publish(channel, message_json)
            logger.debug(f"Published to {channel}: {data.get('type', 'unknown')}")
        except Exception as e:
            logger.error(f"Error publishing to {channel}: {e}")

    async def _listen(self):
        """
        Listen for messages on subscribed channels
        Background task that runs continuously
        """
        logger.info("Started listening for Redis pub/sub messages")

        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    channel = message["channel"]
                    data = message["data"]

                    # Parse JSON data
                    try:
                        parsed_data = json.loads(data)
                    except json.JSONDecodeError as e:
                        logger.error(f"Invalid JSON from {channel}: {e}")
                        continue

                    # Call handler
                    handler = self.channels.get(channel)
                    if handler:
                        try:
                            await handler(parsed_data)
                        except Exception as e:
                            logger.error(
                                f"Error in handler for {channel}: {e}",
                                exc_info=True
                            )
                    else:
                        logger.warning(f"No handler for channel: {channel}")

        except asyncio.CancelledError:
            logger.info("Stopped listening for Redis pub/sub messages")
            raise
        except Exception as e:
            logger.error(f"Error in pub/sub listener: {e}", exc_info=True)
            # Attempt to restart listener
            await asyncio.sleep(5)
            self._listening_task = asyncio.create_task(self._listen())

    async def get_subscriber_count(self, channel: str) -> int:
        """
        Get number of subscribers to a channel

        Args:
            channel: Channel name

        Returns:
            Number of subscribers
        """
        if not self.redis:
            return 0

        try:
            result = await self.redis.pubsub_numsub(channel)
            return result[channel] if result else 0
        except Exception as e:
            logger.error(f"Error getting subscriber count: {e}")
            return 0


# Global pub/sub instance
redis_pubsub = RedisPubSub()
