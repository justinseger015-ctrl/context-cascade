"""
Real-time WebSocket Sync Broadcaster.

Broadcasts schedule_config.yml changes to all connected clients via WebSocket.
Integrates with P2_T3 WebSocket infrastructure.

Features:
- Broadcast 'schedule_config_updated' events when YAML changes
- File system watcher for YAML file changes
- Client notification for conflict resolution
- Automatic reconnection handling

Events:
- schedule_config_updated: YAML file was modified
- sync_conflict_detected: Conflict found during sync
- sync_conflict_resolved: Conflict was resolved
- sync_status_changed: Sync status changed
"""

import asyncio
from datetime import datetime
from typing import Dict, Set
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from fastapi import WebSocket
from app.main_websocket_integration import manager  # WebSocket manager from P2_T3


# WebSocket connection tracking
active_sync_clients: Set[WebSocket] = set()


class YAMLFileWatcher(FileSystemEventHandler):
    """
    File system watcher for schedule_config.yml changes.

    Uses watchdog library to detect YAML file modifications
    and broadcasts events to connected WebSocket clients.
    """

    def __init__(self, yaml_path: str, broadcast_callback):
        super().__init__()
        self.yaml_path = Path(yaml_path).resolve()
        self.broadcast_callback = broadcast_callback
        self.last_modified = None

    def on_modified(self, event):
        """Handle file modification events."""
        if isinstance(event, FileModifiedEvent):
            event_path = Path(event.src_path).resolve()

            # Check if it's our YAML file
            if event_path == self.yaml_path:
                # Debounce: Ignore duplicate events within 1 second
                now = datetime.utcnow()
                if self.last_modified and (now - self.last_modified).total_seconds() < 1:
                    return

                self.last_modified = now

                # Broadcast update event
                asyncio.create_task(self.broadcast_callback())


async def broadcast_yaml_updated():
    """
    Broadcast schedule_config_updated event to all connected clients.

    Sent when schedule_config.yml is modified externally
    (e.g., manual edit, cron job sync).
    """
    event_data = {
        "event": "schedule_config_updated",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Schedule configuration was updated. Reload tasks.",
    }

    # Broadcast to all connected clients
    await manager.broadcast(event_data)

    print(f"📢 Broadcasted schedule_config_updated to {len(active_sync_clients)} clients")


async def broadcast_conflict_detected(conflict_id: str, task_id: int, reason: str):
    """
    Broadcast sync_conflict_detected event.

    Args:
        conflict_id: Unique conflict identifier
        task_id: Task ID with conflict
        reason: Conflict reason description
    """
    event_data = {
        "event": "sync_conflict_detected",
        "conflict_id": conflict_id,
        "task_id": task_id,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
        "action_required": True,
    }

    await manager.broadcast(event_data)

    print(f"⚠️  Broadcasted conflict detected: {conflict_id}")


async def broadcast_conflict_resolved(conflict_id: str, resolution: str):
    """
    Broadcast sync_conflict_resolved event.

    Args:
        conflict_id: Unique conflict identifier
        resolution: Resolution strategy used (keep_yaml, keep_db, merge)
    """
    event_data = {
        "event": "sync_conflict_resolved",
        "conflict_id": conflict_id,
        "resolution": resolution,
        "timestamp": datetime.utcnow().isoformat(),
    }

    await manager.broadcast(event_data)

    print(f"✅ Broadcasted conflict resolved: {conflict_id} ({resolution})")


async def broadcast_sync_status(status: Dict):
    """
    Broadcast sync_status_changed event.

    Args:
        status: Sync status dictionary (last_sync, total_tasks, conflicts)
    """
    event_data = {
        "event": "sync_status_changed",
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
    }

    await manager.broadcast(event_data)


# WebSocket endpoint for sync events

async def websocket_sync_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time sync events.

    Clients connect to this endpoint to receive:
    - schedule_config_updated events
    - sync_conflict_detected events
    - sync_conflict_resolved events
    - sync_status_changed events

    Usage (client-side):
        ws = new WebSocket('ws://localhost:8000/ws/sync');
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.event === 'schedule_config_updated') {
                // Reload tasks from server
            }
        };
    """
    await websocket.accept()
    active_sync_clients.add(websocket)

    try:
        # Send initial sync status
        await websocket.send_json({
            "event": "connection_established",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Connected to sync event stream",
        })

        # Keep connection alive
        while True:
            # Wait for client messages (heartbeat, etc.)
            data = await websocket.receive_text()

            # Handle client requests
            if data == "ping":
                await websocket.send_json({"event": "pong"})

    except Exception as e:
        print(f"WebSocket sync error: {e}")

    finally:
        # Remove client on disconnect
        active_sync_clients.remove(websocket)


# File watcher setup

def start_yaml_watcher(yaml_path: str = "config/schedule_config.yml"):
    """
    Start file system watcher for YAML file changes.

    Args:
        yaml_path: Path to schedule_config.yml

    Returns:
        Observer instance (call observer.stop() to stop watching)
    """
    yaml_path_obj = Path(yaml_path).resolve()

    # Create watcher
    event_handler = YAMLFileWatcher(
        yaml_path=str(yaml_path_obj),
        broadcast_callback=broadcast_yaml_updated
    )

    # Start observer
    observer = Observer()
    observer.schedule(
        event_handler,
        path=str(yaml_path_obj.parent),
        recursive=False
    )
    observer.start()

    print(f"🔍 Started YAML file watcher for {yaml_path}")

    return observer


# Shutdown handler

def stop_yaml_watcher(observer: Observer):
    """Stop file system watcher."""
    observer.stop()
    observer.join()
    print("🛑 Stopped YAML file watcher")
