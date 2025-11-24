# WebSocket Server - Real-time agent activity streaming for dashboard
# Broadcasts agent events to connected clients for live monitoring

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
import json
import asyncio
from datetime import datetime

from ..database import get_db
from ..models.agent import Agent

router = APIRouter()

# Connection manager for WebSocket clients
class ConnectionManager:
    """Manages WebSocket connections and broadcasts to all connected clients"""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket"""
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific client"""
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                # Remove dead connection
                self.disconnect(connection)

# Global connection manager instance
manager = ConnectionManager()

@router.websocket("/agents/activity/stream")
async def agent_activity_stream(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for real-time agent activity streaming.

    **Usage**:
    ```javascript
    const ws = new WebSocket("ws://localhost:8000/api/v1/agents/activity/stream");

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("Agent activity:", data);
    };
    ```

    **Events sent to clients**:
    - agent_activated: When agent starts a task
    - agent_completed: When agent finishes a task
    - budget_updated: When agent budget changes
    - rbac_decision: When RBAC decision is made
    - metric_recorded: When new metric is recorded
    """
    await manager.connect(websocket)

    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to Agent Reality Map WebSocket",
            "timestamp": datetime.utcnow().isoformat()
        })

        # Send current agent stats on connect
        total_agents = db.query(Agent).count()
        await websocket.send_json({
            "type": "stats",
            "data": {
                "total_agents": total_agents,
                "active_connections": len(manager.active_connections)
            },
            "timestamp": datetime.utcnow().isoformat()
        })

        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()

            # Echo back for now (can add client commands later)
            await websocket.send_json({
                "type": "echo",
                "message": f"Received: {data}",
                "timestamp": datetime.utcnow().isoformat()
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("WebSocket disconnected gracefully")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Helper function to broadcast events (called by API endpoints)
async def broadcast_agent_event(event_type: str, data: Dict):
    """
    Broadcast an agent event to all connected WebSocket clients.

    **Use case**: Call this from API endpoints to push real-time updates

    **Example**:
    ```python
    from ..websocket.agent_activity import broadcast_agent_event

    # In an API endpoint after updating an agent
    await broadcast_agent_event("agent_activated", {
        "agent_id": agent.agent_id,
        "agent_name": agent.name,
        "timestamp": datetime.utcnow().isoformat()
    })
    ```
    """
    message = {
        "type": event_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }
    await manager.broadcast(json.dumps(message))

# Health check endpoint for WebSocket server
@router.get("/websocket/health")
async def websocket_health():
    """Health check for WebSocket server"""
    return {
        "status": "operational",
        "active_connections": len(manager.active_connections),
        "endpoint": "/api/v1/agents/activity/stream"
    }
