"""
FastAPI WebSocket Module
Production-ready WebSocket implementation with Redis pub/sub
"""

from .connection_manager import ConnectionManager
from .redis_pubsub import RedisPubSub
from .heartbeat import HeartbeatManager
from .message_types import (
    WSMessage,
    TaskStatusUpdate,
    AgentActivityUpdate,
    CalendarEventCreated,
    MessageType,
)

__all__ = [
    "ConnectionManager",
    "RedisPubSub",
    "HeartbeatManager",
    "WSMessage",
    "TaskStatusUpdate",
    "AgentActivityUpdate",
    "CalendarEventCreated",
    "MessageType",
]
