"""
Example FastAPI main.py with YAML ↔ DB Sync Integration.

This example shows how to integrate the sync system into your FastAPI application.
Copy the relevant sections to your actual app/main.py.

Features added:
- YAML ↔ DB sync on startup
- File watcher for real-time updates
- Sync API endpoints (/api/sync/*)
- WebSocket broadcasting
- Graceful shutdown
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Database and models
from app.core.database import engine, get_db
from app.models import Base

# Sync system integration
from app.main_sync_integration import integrate_sync_system
from sync import start_yaml_watcher, stop_yaml_watcher
from sync.conflict_resolution import startup_sync

# File watcher global
file_watcher = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Startup:
    - Create database tables
    - Run initial YAML → DB sync
    - Start file watcher

    Shutdown:
    - Stop file watcher
    - Close database connections
    """
    global file_watcher

    # STARTUP
    print("🚀 Starting FastAPI application...")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")

    # Run initial YAML → DB sync
    async for db in get_db():
        conflicts = await startup_sync(db)
        if conflicts:
            print(f"⚠️  {len(conflicts)} sync conflicts detected. Resolve via /api/sync/conflicts")
        break

    # Start YAML file watcher
    file_watcher = start_yaml_watcher(yaml_path="config/schedule_config.yml")
    print("✅ YAML file watcher started")

    yield

    # SHUTDOWN
    print("🛑 Shutting down FastAPI application...")

    # Stop file watcher
    if file_watcher:
        stop_yaml_watcher(file_watcher)
        print("✅ YAML file watcher stopped")

    # Close database
    await engine.dispose()
    print("✅ Database connections closed")


# Create FastAPI app
app = FastAPI(
    title="RUV-SPARC Dashboard API",
    description="SPARC methodology dashboard with YAML ↔ DB sync",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Integrate sync system (adds /api/sync/* routes)
integrate_sync_system(app)


# Example routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "RUV-SPARC Dashboard API",
        "version": "1.0.0",
        "features": {
            "yaml_db_sync": True,
            "realtime_updates": True,
            "conflict_resolution": True,
        },
        "sync_endpoints": {
            "conflicts": "/api/sync/conflicts",
            "status": "/api/sync/status",
            "trigger": "/api/sync/trigger",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "file_watcher": "running" if file_watcher else "stopped",
    }


# Run with: uvicorn examples.main_with_sync_integration:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "examples.main_with_sync_integration:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
