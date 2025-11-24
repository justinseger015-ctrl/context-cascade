"""
Main Application with WebSocket Integration
Example of integrating WebSocket router into FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.websocket.router import router as websocket_router, on_startup, on_shutdown

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RUV SPARC Dashboard API with WebSocket",
    description="FastAPI backend with production WebSocket support",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include WebSocket router
app.include_router(websocket_router, tags=["WebSocket"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup"""
    logger.info("Starting application...")

    try:
        # Initialize WebSocket services
        await on_startup()

        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup services on application shutdown"""
    logger.info("Shutting down application...")

    try:
        # Cleanup WebSocket services
        await on_shutdown()

        logger.info("Application shut down successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Application health check"""
    return {
        "status": "healthy",
        "service": "ruv-sparc-dashboard-api",
        "version": "1.0.0"
    }


# Example: Broadcasting task updates
@app.post("/tasks/{task_id}/broadcast-update")
async def broadcast_task_update(task_id: str, status: str, progress: int):
    """
    Example endpoint to broadcast task updates via WebSocket

    Args:
        task_id: Task identifier
        status: Task status (pending, running, completed, failed)
        progress: Task progress (0-100)
    """
    from app.websocket.redis_pubsub import redis_pubsub
    from app.websocket.message_types import TaskStatusUpdate
    import uuid

    message = TaskStatusUpdate(
        event_id=str(uuid.uuid4()),
        data={
            "task_id": task_id,
            "status": status,
            "progress": progress,
        }
    )

    # Broadcast to all connected clients
    await redis_pubsub.publish_broadcast(message)

    return {"message": "Task update broadcasted", "task_id": task_id}


# Example: Sending user-specific updates
@app.post("/users/{user_id}/send-notification")
async def send_user_notification(user_id: str, notification: dict):
    """
    Example endpoint to send user-specific notifications via WebSocket

    Args:
        user_id: User identifier
        notification: Notification data
    """
    from app.websocket.redis_pubsub import redis_pubsub
    from app.websocket.message_types import WSMessage, MessageType
    import uuid

    message = WSMessage(
        type=MessageType.AGENT_ACTIVITY_UPDATE,
        event_id=str(uuid.uuid4()),
        data=notification
    )

    # Send to specific user
    await redis_pubsub.publish_to_user(user_id, message)

    return {"message": "Notification sent", "user_id": user_id}


# Example: Calendar event creation broadcast
@app.post("/calendar/events/create")
async def create_calendar_event(event_data: dict):
    """
    Example endpoint to create and broadcast calendar events

    Args:
        event_data: Calendar event data (title, start_time, etc.)
    """
    from app.websocket.redis_pubsub import redis_pubsub
    from app.websocket.message_types import CalendarEventCreated
    import uuid

    event_id = str(uuid.uuid4())

    message = CalendarEventCreated(
        event_id=str(uuid.uuid4()),
        data={
            "event_id": event_id,
            **event_data
        }
    )

    # Broadcast to all connected clients
    await redis_pubsub.publish_broadcast(message)

    return {"message": "Calendar event created", "event_id": event_id}


if __name__ == "__main__":
    import uvicorn

    # Run with multiple workers for production
    uvicorn.run(
        "app.main_websocket_integration:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # Multiple workers for horizontal scaling
        log_level="info",
        reload=False,  # Set to True for development
    )
