"""
Main Application Integration for YAML ↔ DB Sync.

Integrates sync system into FastAPI application:
- Startup sync (YAML → DB)
- File watcher for real-time updates
- Sync API endpoints
- WebSocket broadcasting

Add to main.py:
    from app.main_sync_integration import integrate_sync_system
    integrate_sync_system(app)
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from sync import sync_router, start_yaml_watcher, stop_yaml_watcher
from sync.yaml_db_sync import SyncEngine
from sync.conflict_resolution import startup_sync
from app.core.database import get_db


# Global file watcher
file_watcher = None


@asynccontextmanager
async def sync_lifespan(app: FastAPI):
    """
    Lifespan context manager for sync system.

    Startup:
    - Run initial YAML → DB sync
    - Start file watcher for YAML changes

    Shutdown:
    - Stop file watcher
    """
    global file_watcher

    # Startup
    print("🔄 Starting YAML ↔ DB sync system...")

    # Run initial sync
    async for db in get_db():
        await startup_sync(db)
        break

    # Start file watcher
    file_watcher = start_yaml_watcher(yaml_path="config/schedule_config.yml")

    yield

    # Shutdown
    print("🛑 Stopping YAML ↔ DB sync system...")
    if file_watcher:
        stop_yaml_watcher(file_watcher)


def integrate_sync_system(app: FastAPI):
    """
    Integrate sync system into FastAPI application.

    Args:
        app: FastAPI application instance

    Adds:
    - Sync API routes (/api/sync/*)
    - Startup sync (YAML → DB)
    - File watcher for real-time updates
    - Shutdown cleanup
    """
    # Add sync router
    app.include_router(sync_router)

    # Add lifespan events
    # Note: This requires FastAPI 0.109+ lifespan parameter
    # For older versions, use @app.on_event("startup") and @app.on_event("shutdown")

    @app.on_event("startup")
    async def on_startup():
        """Run startup sync."""
        async for db in get_db():
            await startup_sync(db)
            break

        # Start file watcher
        global file_watcher
        file_watcher = start_yaml_watcher(yaml_path="config/schedule_config.yml")

    @app.on_event("shutdown")
    async def on_shutdown():
        """Stop file watcher."""
        if file_watcher:
            stop_yaml_watcher(file_watcher)

    print("✅ YAML ↔ DB sync system integrated")


# Manual sync trigger for API routes
async def trigger_manual_sync(db_session, direction: str = "bidirectional"):
    """
    Manually trigger sync operation.

    Args:
        db_session: Database session
        direction: Sync direction ("yaml_to_db", "db_to_yaml", "bidirectional")

    Returns:
        List of conflicts detected (empty if no conflicts)
    """
    sync_engine = SyncEngine(db_session, yaml_path="config/schedule_config.yml")

    if direction == "yaml_to_db":
        conflicts = await sync_engine.sync_yaml_to_db()
        await db_session.commit()
        return conflicts

    elif direction == "db_to_yaml":
        await sync_engine.sync_db_to_yaml()
        await db_session.commit()
        return []

    elif direction == "bidirectional":
        # First YAML → DB
        conflicts = await sync_engine.sync_yaml_to_db()

        # Then DB → YAML (if no conflicts)
        if not conflicts:
            await sync_engine.sync_db_to_yaml()

        await db_session.commit()
        return conflicts

    else:
        raise ValueError(f"Invalid direction: {direction}")
