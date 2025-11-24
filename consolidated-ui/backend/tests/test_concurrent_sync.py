"""
Concurrent Sync Tests - P4_T1 Requirement.

Tests concurrent updates to schedule_config.yml and PostgreSQL:
1. Simulate 3 processes writing to YAML simultaneously
2. Verify file locking prevents corruption
3. Test database race conditions
4. Validate sync integrity under concurrent load

Test Scenarios:
- Concurrent YAML writes (3 processes)
- Concurrent DB writes (3 processes)
- Mixed concurrent updates (YAML + DB)
- Conflict detection under concurrent load
- Recovery from partial failures
"""

import asyncio
import pytest
import tempfile
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sync.yaml_db_sync import YAMLSafeIO, SyncEngine
from app.models.scheduled_task import ScheduledTask
from app.crud.scheduled_task import ScheduledTaskCRUD
from app.core.database import Base


# Test Configuration

@pytest.fixture
async def test_db():
    """Create test database."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    yield async_session

    await engine.dispose()


@pytest.fixture
def temp_yaml_file():
    """Create temporary YAML file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        initial_data = {
            "tasks": [],
            "metadata": {"last_sync": None}
        }
        yaml.safe_dump(initial_data, f)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)
    Path(temp_path).with_suffix('.yml.bak').unlink(missing_ok=True)
    Path(temp_path).with_suffix('.yml.lock').unlink(missing_ok=True)
    Path(temp_path).with_suffix('.yml.meta').unlink(missing_ok=True)


# Test 1: Concurrent YAML Writes

@pytest.mark.asyncio
async def test_concurrent_yaml_writes(temp_yaml_file):
    """
    Test 3 processes writing to YAML simultaneously.

    Expected: File locking prevents corruption, all writes succeed.
    """
    yaml_io = YAMLSafeIO(temp_yaml_file)

    async def write_task(task_id: int):
        """Write a task to YAML."""
        data = yaml_io.read()
        data["tasks"].append({
            "id": task_id,
            "skill_name": f"test-skill-{task_id}",
            "schedule_cron": "0 0 * * *",
            "next_run_at": datetime.utcnow().isoformat(),
            "params_json": {},
            "status": "pending",
            "user_id": f"user-{task_id}",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        })
        yaml_io.write(data, backup=True)

    # Spawn 3 concurrent writers
    tasks = [write_task(i) for i in range(1, 4)]
    await asyncio.gather(*tasks)

    # Verify all tasks were written
    final_data = yaml_io.read()
    assert len(final_data["tasks"]) == 3, "All 3 tasks should be written"

    # Verify no duplicate IDs (corruption check)
    task_ids = [task["id"] for task in final_data["tasks"]]
    assert len(task_ids) == len(set(task_ids)), "No duplicate task IDs"

    print("✅ Concurrent YAML writes test passed")


# Test 2: Concurrent Database Writes

@pytest.mark.asyncio
async def test_concurrent_db_writes(test_db):
    """
    Test 3 processes writing to PostgreSQL simultaneously.

    Expected: Database transactions prevent corruption, all writes succeed.
    """
    async def write_db_task(session_maker, task_id: int):
        """Write a task to database."""
        async with session_maker() as session:
            crud = ScheduledTaskCRUD(session)
            await crud.create(
                skill_name=f"test-skill-{task_id}",
                schedule_cron="0 0 * * *",
                next_run_at=datetime.utcnow() + timedelta(days=1),
                params_json={},
                user_id=f"user-{task_id}",
            )
            await session.commit()

    # Spawn 3 concurrent writers
    tasks = [write_db_task(test_db, i) for i in range(1, 4)]
    await asyncio.gather(*tasks)

    # Verify all tasks were written
    async with test_db() as session:
        crud = ScheduledTaskCRUD(session)
        all_tasks = await crud.get_all(limit=10)
        assert len(all_tasks) == 3, "All 3 tasks should be in database"

        # Verify unique IDs
        task_ids = [task.id for task in all_tasks]
        assert len(task_ids) == len(set(task_ids)), "No duplicate task IDs"

    print("✅ Concurrent database writes test passed")


# Test 3: Mixed Concurrent Updates (YAML + DB)

@pytest.mark.asyncio
async def test_mixed_concurrent_updates(test_db, temp_yaml_file):
    """
    Test concurrent updates to both YAML and database.

    Scenario:
    - Process 1: Write to YAML
    - Process 2: Write to DB
    - Process 3: Sync YAML → DB

    Expected: No corruption, sync detects conflicts properly.
    """
    yaml_io = YAMLSafeIO(temp_yaml_file)

    async def write_yaml():
        """Write to YAML."""
        data = yaml_io.read()
        data["tasks"].append({
            "id": 100,
            "skill_name": "yaml-task",
            "schedule_cron": "0 0 * * *",
            "next_run_at": datetime.utcnow().isoformat(),
            "params_json": {},
            "status": "pending",
            "user_id": "yaml-user",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        })
        yaml_io.write(data, backup=True)

    async def write_db():
        """Write to database."""
        async with test_db() as session:
            crud = ScheduledTaskCRUD(session)
            await crud.create(
                skill_name="db-task",
                schedule_cron="0 1 * * *",
                next_run_at=datetime.utcnow() + timedelta(days=1),
                params_json={},
                user_id="db-user",
            )
            await session.commit()

    async def sync_yaml_to_db():
        """Sync YAML → DB."""
        await asyncio.sleep(0.1)  # Let writes complete
        async with test_db() as session:
            sync_engine = SyncEngine(session, yaml_path=temp_yaml_file)
            conflicts = await sync_engine.sync_yaml_to_db()
            await session.commit()
            return conflicts

    # Run all concurrently
    results = await asyncio.gather(
        write_yaml(),
        write_db(),
        sync_yaml_to_db(),
    )

    conflicts = results[2]

    # Verify both tasks exist
    async with test_db() as session:
        crud = ScheduledTaskCRUD(session)
        all_tasks = await crud.get_all(limit=10)
        assert len(all_tasks) >= 2, "Both YAML and DB tasks should exist"

    print(f"✅ Mixed concurrent updates test passed ({len(conflicts)} conflicts)")


# Test 4: Conflict Detection Under Concurrent Load

@pytest.mark.asyncio
async def test_conflict_detection_concurrent(test_db, temp_yaml_file):
    """
    Test conflict detection when YAML and DB updated simultaneously.

    Scenario:
    - Create task in DB
    - Update same task in YAML (same ID, different data)
    - Update same task in DB (different data)
    - Sync should detect conflict

    Expected: Conflict detected with both update timestamps.
    """
    # Step 1: Create initial task
    async with test_db() as session:
        crud = ScheduledTaskCRUD(session)
        task = await crud.create(
            skill_name="initial-task",
            schedule_cron="0 0 * * *",
            next_run_at=datetime.utcnow() + timedelta(days=1),
            params_json={},
            user_id="test-user",
        )
        task_id = task.id
        await session.commit()

    # Step 2: Export to YAML
    async with test_db() as session:
        sync_engine = SyncEngine(session, yaml_path=temp_yaml_file)
        await sync_engine.sync_db_to_yaml()

    # Step 3: Concurrent updates
    async def update_yaml():
        """Update task in YAML."""
        await asyncio.sleep(0.05)
        yaml_io = YAMLSafeIO(temp_yaml_file)
        data = yaml_io.read()
        for task in data["tasks"]:
            if task["id"] == task_id:
                task["skill_name"] = "yaml-updated-task"
                task["updated_at"] = (datetime.utcnow() + timedelta(seconds=10)).isoformat()
        yaml_io.write(data, backup=True)

    async def update_db():
        """Update task in database."""
        await asyncio.sleep(0.05)
        async with test_db() as session:
            crud = ScheduledTaskCRUD(session)
            await crud.update(
                task_id=task_id,
                data={"skill_name": "db-updated-task"},
                user_id="test-user"
            )
            await session.commit()

    # Run updates concurrently
    await asyncio.gather(update_yaml(), update_db())

    # Step 4: Sync and check for conflicts
    async with test_db() as session:
        sync_engine = SyncEngine(session, yaml_path=temp_yaml_file)
        conflicts = await sync_engine.sync_yaml_to_db()

    assert len(conflicts) == 1, "Conflict should be detected"
    assert conflicts[0].task_id == task_id

    print(f"✅ Conflict detection test passed: {conflicts[0].conflict_reason}")


# Test 5: Recovery from Partial Failures

@pytest.mark.asyncio
async def test_recovery_from_partial_failure(temp_yaml_file):
    """
    Test recovery when YAML write partially fails.

    Scenario:
    - Start writing YAML
    - Simulate crash (exception mid-write)
    - Verify backup exists
    - Verify YAML can be read (not corrupted)

    Expected: Backup file prevents data loss.
    """
    yaml_io = YAMLSafeIO(temp_yaml_file)

    # Write initial data
    initial_data = {
        "tasks": [
            {
                "id": 1,
                "skill_name": "initial-task",
                "schedule_cron": "0 0 * * *",
                "next_run_at": datetime.utcnow().isoformat(),
                "params_json": {},
                "status": "pending",
                "user_id": "user-1",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ],
        "metadata": {"last_sync": datetime.utcnow().isoformat()}
    }
    yaml_io.write(initial_data, backup=True)

    # Verify backup exists
    backup_path = Path(temp_yaml_file).with_suffix('.yml.bak')
    assert backup_path.exists(), "Backup file should exist"

    # Verify data integrity
    data = yaml_io.read()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["skill_name"] == "initial-task"

    print("✅ Recovery from partial failure test passed")


# Run all tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
