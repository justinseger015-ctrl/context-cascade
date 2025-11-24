# FastAPI Main Application - Agent Reality Map Backend API
# Production-ready API with RBAC integration, WebSocket streaming, and comprehensive endpoints

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from .database import init_db, engine
from .routers import agents, metrics, events, agent_activity_router, registry, ai_chat
from .websocket import agent_activity
from .models import Agent, Metric, AuditLog

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    print("Starting Agent Reality Map Backend API...")
    init_db()
    print("Database initialized successfully")
    yield
    # Shutdown: Cleanup
    print("Shutting down Agent Reality Map Backend API...")
    engine.dispose()

# FastAPI app instance
app = FastAPI(
    title="Agent Reality Map Backend API",
    description="Production-grade backend API for Agent Reality Map integration with RBAC, real-time streaming, and comprehensive agent management",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(agent_activity.router, prefix="/api/v1", tags=["websocket"])
app.include_router(agent_activity_router.router, prefix="/api/v1", tags=["activity"])
app.include_router(registry.router, prefix="/api/v1/registry", tags=["registry"])
app.include_router(ai_chat.router, prefix="/api/v1", tags=["ai"])

# Health check endpoint
@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Agent Reality Map Backend API",
        "version": "1.0.0",
        "message": "Backend API is operational"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check with database status"""
    try:
        # Test database connection
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "api": "operational"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    # Run with: python -m backend.app.main
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


# Simple /ws WebSocket endpoint for frontend compatibility
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Simple WebSocket endpoint at /ws for frontend compatibility.
    No authentication required for development.
    """
    from datetime import datetime
    import json
    
    await websocket.accept()
    
    try:
        # Send connection success message
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "message": "WebSocket connection established",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep connection alive
        while True:
            try:
                data = await websocket.receive_text()
                # Echo back
                await websocket.send_json({
                    "type": "echo",
                    "data": data,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                break
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass
