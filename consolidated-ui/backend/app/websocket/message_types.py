"""
WebSocket Message Types
Defines all message schemas for WebSocket communication
"""

from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """WebSocket message types"""
    TASK_STATUS_UPDATE = "task_status_update"
    AGENT_ACTIVITY_UPDATE = "agent_activity_update"
    CALENDAR_EVENT_CREATED = "calendar_event_created"
    PING = "ping"
    PONG = "pong"
    ERROR = "error"
    ACK = "ack"


class WSMessage(BaseModel):
    """Base WebSocket message"""
    type: MessageType
    event_id: str = Field(description="Unique event ID for replay")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TaskStatusUpdate(BaseModel):
    """Task status update message"""
    type: MessageType = MessageType.TASK_STATUS_UPDATE
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(
        description="Task status data including task_id, status, progress, etc."
    )

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentActivityUpdate(BaseModel):
    """Agent activity update message"""
    type: MessageType = MessageType.AGENT_ACTIVITY_UPDATE
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(
        description="Agent activity data including agent_id, action, status, etc."
    )

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CalendarEventCreated(BaseModel):
    """Calendar event created message"""
    type: MessageType = MessageType.CALENDAR_EVENT_CREATED
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(
        description="Calendar event data including event_id, title, start_time, etc."
    )

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PingMessage(BaseModel):
    """Ping message for heartbeat"""
    type: MessageType = MessageType.PING
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PongMessage(BaseModel):
    """Pong response for heartbeat"""
    type: MessageType = MessageType.PONG
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorMessage(BaseModel):
    """Error message"""
    type: MessageType = MessageType.ERROR
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: str
    details: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AckMessage(BaseModel):
    """Acknowledgment message"""
    type: MessageType = MessageType.ACK
    event_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ack_event_id: str = Field(description="Event ID being acknowledged")

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
