"""
YAML ↔ PostgreSQL Sync Module.

Provides bidirectional sync between schedule_config.yml and PostgreSQL database.

Main Components:
- yaml_db_sync: Core sync engine with file locking
- conflict_resolution: REST API for conflict management
- realtime_sync: WebSocket broadcasting for YAML changes
- sync_cron_job.sh: Scheduled sync safety net

Usage:
    # Import sync components
    from sync.yaml_db_sync import SyncEngine, YAMLSafeIO
    from sync.conflict_resolution import router as sync_router
    from sync.realtime_sync import start_yaml_watcher

    # Initialize sync engine
    sync_engine = SyncEngine(db_session, yaml_path="config/schedule_config.yml")

    # Sync YAML → DB
    conflicts = await sync_engine.sync_yaml_to_db()

    # Sync DB → YAML
    await sync_engine.sync_db_to_yaml(task_id=123)

    # Start file watcher
    observer = start_yaml_watcher()

    # Add sync API routes
    app.include_router(sync_router)
"""

from sync.yaml_db_sync import SyncEngine, YAMLSafeIO, SyncConflict
from sync.conflict_resolution import router as sync_router
from sync.realtime_sync import (
    start_yaml_watcher,
    stop_yaml_watcher,
    broadcast_yaml_updated,
    broadcast_conflict_detected,
    broadcast_conflict_resolved,
)

__all__ = [
    "SyncEngine",
    "YAMLSafeIO",
    "SyncConflict",
    "sync_router",
    "start_yaml_watcher",
    "stop_yaml_watcher",
    "broadcast_yaml_updated",
    "broadcast_conflict_detected",
    "broadcast_conflict_resolved",
]
