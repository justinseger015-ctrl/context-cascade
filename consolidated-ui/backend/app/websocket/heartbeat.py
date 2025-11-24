"""
WebSocket Heartbeat Manager
Implements ping/pong heartbeat with automatic connection cleanup
Ping every 30s, disconnect if no pong after 60s
"""

import asyncio
import logging
import uuid
from typing import Dict, Optional
from datetime import datetime, timedelta
from fastapi import WebSocket

from .message_types import PingMessage, PongMessage, MessageType

logger = logging.getLogger(__name__)


class HeartbeatManager:
    """
    Manages WebSocket heartbeat (ping/pong) for connection health monitoring

    Features:
    - Send ping every 30 seconds
    - Expect pong within 60 seconds
    - Auto-disconnect stale connections
    - Track last activity per connection
    """

    def __init__(
        self,
        ping_interval: int = 30,
        pong_timeout: int = 60
    ):
        """
        Initialize heartbeat manager

        Args:
            ping_interval: Seconds between ping messages (default 30)
            pong_timeout: Seconds to wait for pong before disconnecting (default 60)
        """
        self.ping_interval = ping_interval
        self.pong_timeout = pong_timeout

        # Track last pong time for each connection
        self.last_pong: Dict[str, datetime] = {}

        # Track heartbeat tasks
        self.heartbeat_tasks: Dict[str, asyncio.Task] = {}

    def start_heartbeat(
        self,
        connection_id: str,
        websocket: WebSocket,
        on_disconnect_callback: Optional[callable] = None
    ):
        """
        Start heartbeat for a connection

        Args:
            connection_id: Connection identifier
            websocket: WebSocket instance
            on_disconnect_callback: Optional callback when connection fails heartbeat
        """
        # Initialize last pong time
        self.last_pong[connection_id] = datetime.utcnow()

        # Create heartbeat task
        task = asyncio.create_task(
            self._heartbeat_loop(
                connection_id,
                websocket,
                on_disconnect_callback
            )
        )
        self.heartbeat_tasks[connection_id] = task

        logger.info(f"Started heartbeat for connection {connection_id}")

    def stop_heartbeat(self, connection_id: str):
        """
        Stop heartbeat for a connection

        Args:
            connection_id: Connection identifier
        """
        # Cancel heartbeat task
        task = self.heartbeat_tasks.pop(connection_id, None)
        if task and not task.done():
            task.cancel()

        # Remove last pong tracking
        self.last_pong.pop(connection_id, None)

        logger.info(f"Stopped heartbeat for connection {connection_id}")

    def record_pong(self, connection_id: str):
        """
        Record pong received from client

        Args:
            connection_id: Connection identifier
        """
        self.last_pong[connection_id] = datetime.utcnow()
        logger.debug(f"Pong received from {connection_id}")

    def is_connection_alive(self, connection_id: str) -> bool:
        """
        Check if connection is alive based on last pong

        Args:
            connection_id: Connection identifier

        Returns:
            True if connection is alive, False otherwise
        """
        last_pong_time = self.last_pong.get(connection_id)
        if not last_pong_time:
            return False

        time_since_pong = (datetime.utcnow() - last_pong_time).total_seconds()
        return time_since_pong < self.pong_timeout

    async def _heartbeat_loop(
        self,
        connection_id: str,
        websocket: WebSocket,
        on_disconnect_callback: Optional[callable] = None
    ):
        """
        Heartbeat loop that sends pings and monitors pongs

        Args:
            connection_id: Connection identifier
            websocket: WebSocket instance
            on_disconnect_callback: Callback when connection dies
        """
        try:
            while True:
                # Wait for ping interval
                await asyncio.sleep(self.ping_interval)

                # Check if last pong is too old
                if not self.is_connection_alive(connection_id):
                    logger.warning(
                        f"Connection {connection_id} failed heartbeat "
                        f"(no pong for {self.pong_timeout}s)"
                    )

                    # Trigger disconnect callback
                    if on_disconnect_callback:
                        await on_disconnect_callback(connection_id)

                    break

                # Send ping
                try:
                    ping_message = PingMessage(
                        event_id=str(uuid.uuid4())
                    )
                    await websocket.send_json(ping_message.dict())
                    logger.debug(f"Sent ping to {connection_id}")
                except Exception as e:
                    logger.error(f"Error sending ping to {connection_id}: {e}")

                    # Trigger disconnect callback
                    if on_disconnect_callback:
                        await on_disconnect_callback(connection_id)

                    break

        except asyncio.CancelledError:
            logger.info(f"Heartbeat cancelled for {connection_id}")
            raise
        except Exception as e:
            logger.error(
                f"Heartbeat error for {connection_id}: {e}",
                exc_info=True
            )

    def get_connection_health(self, connection_id: str) -> dict:
        """
        Get health metrics for a connection

        Args:
            connection_id: Connection identifier

        Returns:
            Dictionary with health metrics
        """
        last_pong_time = self.last_pong.get(connection_id)

        if not last_pong_time:
            return {
                "connection_id": connection_id,
                "status": "unknown",
                "last_pong": None,
                "seconds_since_pong": None
            }

        seconds_since_pong = (datetime.utcnow() - last_pong_time).total_seconds()

        return {
            "connection_id": connection_id,
            "status": "alive" if self.is_connection_alive(connection_id) else "dead",
            "last_pong": last_pong_time.isoformat(),
            "seconds_since_pong": seconds_since_pong
        }

    def get_all_health_metrics(self) -> dict:
        """
        Get health metrics for all connections

        Returns:
            Dictionary with all connection health metrics
        """
        return {
            "total_connections": len(self.last_pong),
            "alive_connections": sum(
                1 for conn_id in self.last_pong
                if self.is_connection_alive(conn_id)
            ),
            "dead_connections": sum(
                1 for conn_id in self.last_pong
                if not self.is_connection_alive(conn_id)
            ),
            "connections": [
                self.get_connection_health(conn_id)
                for conn_id in self.last_pong.keys()
            ]
        }


# Global heartbeat manager instance
heartbeat_manager = HeartbeatManager()
