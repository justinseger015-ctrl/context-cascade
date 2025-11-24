"""
Conflict Resolution UI and API for YAML ↔ Database Sync.

Provides REST API endpoints and conflict resolution logic for handling
sync conflicts between schedule_config.yml and PostgreSQL database.

Features:
- Conflict detection and reporting
- User-driven conflict resolution (keep YAML, keep DB, merge)
- Conflict history tracking
- Automatic conflict notification via WebSocket

Endpoints:
- GET  /api/sync/conflicts - List all pending conflicts
- POST /api/sync/conflicts/{conflict_id}/resolve - Resolve specific conflict
- GET  /api/sync/status - Get sync status and last sync timestamp
- POST /api/sync/trigger - Manually trigger sync operation
"""

from datetime import datetime
from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.core.database import get_db
from sync.yaml_db_sync import SyncEngine, SyncConflict


# Pydantic Models for API

class ConflictResponse(BaseModel):
    """Response model for conflict data."""
    conflict_id: str
    task_id: int
    yaml_updated_at: str
    db_updated_at: str
    conflict_reason: str
    yaml_data: Dict
    db_data: Dict

    class Config:
        from_attributes = True


class ConflictResolutionRequest(BaseModel):
    """Request model for conflict resolution."""
    choice: str = Field(
        ...,
        description="Resolution choice: 'keep_yaml', 'keep_db', or 'merge'"
    )

    class Config:
        schema_extra = {
            "example": {
                "choice": "keep_yaml"
            }
        }


class SyncStatusResponse(BaseModel):
    """Response model for sync status."""
    last_sync_timestamp: Optional[str]
    total_tasks: int
    pending_conflicts: int
    sync_source: str  # "yaml", "database", or "manual"


class SyncTriggerRequest(BaseModel):
    """Request model for manual sync trigger."""
    direction: str = Field(
        ...,
        description="Sync direction: 'yaml_to_db', 'db_to_yaml', or 'bidirectional'"
    )
    force: bool = Field(
        default=False,
        description="Force sync even if conflicts exist"
    )


# In-memory conflict storage (replace with Redis/DB in production)
conflict_store: Dict[str, SyncConflict] = {}


# FastAPI Router

router = APIRouter(prefix="/api/sync", tags=["sync"])


@router.get("/conflicts", response_model=List[ConflictResponse])
async def list_conflicts(
    db: AsyncSession = Depends(get_db)
):
    """
    List all pending sync conflicts.

    Returns:
        List of conflicts with YAML and DB data for comparison
    """
    conflicts = []

    for conflict_id, conflict in conflict_store.items():
        conflict_response = ConflictResponse(
            conflict_id=conflict_id,
            task_id=conflict.task_id,
            yaml_updated_at=conflict.yaml_updated_at.isoformat(),
            db_updated_at=conflict.db_updated_at.isoformat(),
            conflict_reason=conflict.conflict_reason,
            yaml_data=conflict.yaml_task,
            db_data=conflict.db_task.to_dict(),
        )
        conflicts.append(conflict_response)

    return conflicts


@router.post("/conflicts/{conflict_id}/resolve")
async def resolve_conflict(
    conflict_id: str,
    resolution: ConflictResolutionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Resolve a specific sync conflict.

    Args:
        conflict_id: Conflict identifier
        resolution: Resolution choice (keep_yaml, keep_db, merge)

    Returns:
        Success message

    Raises:
        HTTPException: If conflict not found or resolution fails
    """
    # Validate resolution choice
    valid_choices = {"keep_yaml", "keep_db", "merge"}
    if resolution.choice not in valid_choices:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid choice. Must be one of {valid_choices}"
        )

    # Get conflict from store
    conflict = conflict_store.get(conflict_id)
    if not conflict:
        raise HTTPException(
            status_code=404,
            detail=f"Conflict {conflict_id} not found"
        )

    # Resolve conflict
    sync_engine = SyncEngine(db)
    await sync_engine.resolve_conflict(conflict, resolution.choice)

    # Remove from conflict store
    del conflict_store[conflict_id]

    # Broadcast resolution via WebSocket
    # await broadcast_conflict_resolved(conflict_id, resolution.choice)

    return {
        "status": "success",
        "message": f"Conflict {conflict_id} resolved using strategy: {resolution.choice}",
        "task_id": conflict.task_id,
    }


@router.get("/status", response_model=SyncStatusResponse)
async def get_sync_status(
    db: AsyncSession = Depends(get_db)
):
    """
    Get current sync status.

    Returns:
        Sync status including last sync timestamp and conflict count
    """
    sync_engine = SyncEngine(db)

    # Get YAML metadata
    yaml_metadata = sync_engine.yaml_io.get_metadata()
    last_sync = yaml_metadata.get("last_updated") if yaml_metadata else None

    # Count tasks
    from app.crud.scheduled_task import ScheduledTaskCRUD
    crud = ScheduledTaskCRUD(db)
    total_tasks = await crud.count()

    return SyncStatusResponse(
        last_sync_timestamp=last_sync,
        total_tasks=total_tasks,
        pending_conflicts=len(conflict_store),
        sync_source=yaml_metadata.get("sync_source", "unknown") if yaml_metadata else "unknown",
    )


@router.post("/trigger")
async def trigger_sync(
    request: SyncTriggerRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger sync operation.

    Args:
        request: Sync configuration (direction, force)

    Returns:
        Sync results including conflicts detected

    Raises:
        HTTPException: If sync fails or conflicts exist (unless forced)
    """
    sync_engine = SyncEngine(db)

    # Validate direction
    valid_directions = {"yaml_to_db", "db_to_yaml", "bidirectional"}
    if request.direction not in valid_directions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid direction. Must be one of {valid_directions}"
        )

    conflicts_detected = []

    try:
        # Execute sync based on direction
        if request.direction == "yaml_to_db":
            conflicts_detected = await sync_engine.sync_yaml_to_db()

        elif request.direction == "db_to_yaml":
            await sync_engine.sync_db_to_yaml()

        elif request.direction == "bidirectional":
            # First YAML → DB
            conflicts_detected = await sync_engine.sync_yaml_to_db()

            # Then DB → YAML (only if no conflicts or forced)
            if not conflicts_detected or request.force:
                await sync_engine.sync_db_to_yaml()

        # Store conflicts for resolution
        if conflicts_detected:
            for conflict in conflicts_detected:
                conflict_id = f"conflict_{conflict.task_id}_{datetime.utcnow().timestamp()}"
                conflict_store[conflict_id] = conflict

            # If not forced, raise error
            if not request.force:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "message": f"Sync detected {len(conflicts_detected)} conflicts",
                        "conflicts": [
                            {
                                "task_id": c.task_id,
                                "reason": c.conflict_reason
                            }
                            for c in conflicts_detected
                        ]
                    }
                )

        return {
            "status": "success",
            "direction": request.direction,
            "conflicts_detected": len(conflicts_detected),
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Sync failed: {str(e)}"
        )


@router.delete("/conflicts")
async def clear_conflicts():
    """
    Clear all pending conflicts (use with caution).

    Returns:
        Number of conflicts cleared
    """
    count = len(conflict_store)
    conflict_store.clear()

    return {
        "status": "success",
        "conflicts_cleared": count,
    }


# Startup hook: Trigger initial sync

async def startup_sync(db: AsyncSession):
    """
    Run sync on application startup.

    Called from main.py startup event.
    Performs YAML → DB sync and stores conflicts.
    """
    sync_engine = SyncEngine(db)
    conflicts = await sync_engine.sync_yaml_to_db()

    if conflicts:
        print(f"⚠️  Startup sync detected {len(conflicts)} conflicts")
        for conflict in conflicts:
            conflict_id = f"startup_conflict_{conflict.task_id}"
            conflict_store[conflict_id] = conflict
    else:
        print("✅ Startup sync completed successfully, no conflicts")
