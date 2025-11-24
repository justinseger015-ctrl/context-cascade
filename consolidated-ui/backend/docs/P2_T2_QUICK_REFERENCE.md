# P2_T2: SQLAlchemy ORM - Quick Reference

## Import Paths

```python
# Database session
from app.core.database import get_db, AsyncSessionLocal

# Models
from app.models import ScheduledTask, Project, Agent, ExecutionResult, AuditLog

# CRUD services
from app.crud import ScheduledTaskCRUD, ProjectCRUD, AgentCRUD, ExecutionResultCRUD

# Audit logging
from app.core.audit_logging import AuditLogger
```

## FastAPI Dependency Injection

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud import ScheduledTaskCRUD

router = APIRouter()

@router.post("/tasks")
async def create_task(
    skill_name: str,
    schedule_cron: str,
    db: AsyncSession = Depends(get_db)
):
    crud = ScheduledTaskCRUD(db)
    task = await crud.create(
        skill_name=skill_name,
        schedule_cron=schedule_cron,
        next_run_at=datetime.utcnow() + timedelta(days=1),
        user_id="user123"  # From JWT token in P2_T4
    )
    # No need to commit - get_db() handles it
    return task.to_dict()
```

## CRUD Operations Cheat Sheet

### ScheduledTask
```python
crud = ScheduledTaskCRUD(db)

# Create
task = await crud.create(skill_name="test", schedule_cron="* * * * *", next_run_at=...)

# Read
task = await crud.get_by_id(1)
tasks = await crud.get_all(user_id="user123", status="pending", limit=10)
pending = await crud.get_pending_tasks(limit=10)

# Update
task = await crud.update(1, {"status": "completed"}, user_id="user123")

# Delete
deleted = await crud.delete(1, user_id="user123")

# Count
count = await crud.count(user_id="user123", status="pending")
```

### Project
```python
crud = ProjectCRUD(db)

# Create
project = await crud.create(name="My Project", description="...", user_id="user123")

# Read
project = await crud.get_by_id(1)
projects = await crud.get_all(user_id="user123", limit=10)

# Update
project = await crud.update(1, {"description": "Updated"}, user_id="user123")
await crud.increment_task_count(1)

# Delete
deleted = await crud.delete(1, user_id="user123")

# Count
count = await crud.count(user_id="user123")
```

### Agent
```python
crud = AgentCRUD(db)

# Create
agent = await crud.create(name="coder-01", type="coder", capabilities_json=["python"])

# Read
agent = await crud.get_by_id(1)
agent = await crud.get_by_name("coder-01")
agents = await crud.get_all(type="coder", status="active", limit=10)

# Update
agent = await crud.update(1, {"status": "busy"})
updated = await crud.update_activity(1, status="active")

# Delete
deleted = await crud.delete(1)

# Count
count = await crud.count(type="coder", status="active")
```

### ExecutionResult
```python
crud = ExecutionResultCRUD(db)

# Create
result = await crud.create(task_id=1, started_at=datetime.utcnow(), status="running")

# Read
result = await crud.get_by_id(1)
results = await crud.get_by_task_id(1, limit=10)
results = await crud.get_all(status="success", limit=10)

# Update
result = await crud.update(1, {"ended_at": datetime.utcnow(), "status": "success"})
result = await crud.complete_execution(1, "success", datetime.utcnow(), output_text="Done")

# Delete
deleted = await crud.delete(1)

# Statistics
stats = await crud.get_statistics(task_id=1)
# Returns: {"total": 10, "success": 8, "failed": 2, "avg_duration_ms": 1234.5}
```

## Audit Logging

### Automatic Audit Logs
All CRUD CREATE/UPDATE/DELETE operations automatically create audit logs:

```python
# This automatically creates an audit log entry
task = await crud.create(
    skill_name="test",
    schedule_cron="* * * * *",
    next_run_at=...,
    user_id="user123",        # Required for audit
    ip_address="192.168.1.1", # Optional
    user_agent="Mozilla/5.0"  # Optional
)
```

### Manual Audit Logging
```python
from app.core.audit_logging import AuditLogger

logger = AuditLogger(db)

# Log CREATE
await logger.log_create("scheduled_tasks", task.id, user_id="user123")

# Log UPDATE with field diff
old_data = {"status": "pending", "name": "Old"}
new_data = {"status": "completed", "name": "New"}
await logger.log_update("scheduled_tasks", task.id, old_data, new_data, user_id="user123")

# Log DELETE
await logger.log_delete("scheduled_tasks", task.id, user_id="user123")

# Retrieve audit trail
entries = await logger.get_audit_trail(
    table_name="scheduled_tasks",
    record_id=1,
    user_id="user123",
    limit=50
)
```

## Model Methods

### All models have `.to_dict()` for API responses:

```python
task = await crud.get_by_id(1)
return task.to_dict()
# Returns:
# {
#   "id": 1,
#   "skill_name": "test",
#   "schedule_cron": "* * * * *",
#   "next_run_at": "2025-11-09T00:00:00",
#   "params_json": {},
#   "status": "pending",
#   "created_at": "2025-11-08T22:52:00",
#   "updated_at": "2025-11-08T22:52:00",
#   "user_id": "user123"
# }
```

## Database Initialization

```python
# In main.py
from app.core.database import init_db, close_db

@app.on_event("startup")
async def startup():
    await init_db()  # Create all tables

@app.on_event("shutdown")
async def shutdown():
    await close_db()  # Close connections
```

## Common Patterns

### Pagination
```python
# Get page 2 with 20 items per page
tasks = await crud.get_all(limit=20, offset=20)
```

### Filtering
```python
# Get user's pending tasks
tasks = await crud.get_all(user_id="user123", status="pending")

# Get active coder agents
agents = await crud.get_all(type="coder", status="active")
```

### Counting
```python
# Count user's tasks
total = await crud.count(user_id="user123")
pending = await crud.count(user_id="user123", status="pending")
```

### Relationships
```python
# Get task with execution results
task = await crud.get_by_id(1)
# SQLAlchemy will lazy load execution_results relationship
# Or use eager loading:
from sqlalchemy.orm import selectinload
stmt = select(ScheduledTask).options(selectinload(ScheduledTask.execution_results))
```

## Environment Variables

```bash
# .env file
DATABASE_URL=postgresql+asyncpg://sparc_user:sparc_password@localhost:5432/sparc_dashboard
```

## Performance Tips

1. **Use composite indexes** for common query patterns
2. **Batch operations** when possible
3. **Use pagination** for large result sets
4. **Eager load relationships** to avoid N+1 queries
5. **Connection pooling** is configured automatically

## Error Handling

```python
from sqlalchemy.exc import IntegrityError, NoResultFound

try:
    task = await crud.create(...)
except IntegrityError:
    # Unique constraint violation, duplicate key, etc.
    raise HTTPException(status_code=400, detail="Duplicate task")
except Exception as e:
    # Other database errors
    raise HTTPException(status_code=500, detail=str(e))
```

## Testing

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.database import Base, AsyncSessionLocal

@pytest.fixture
async def db_session():
    # Use test database
    engine = create_async_engine("postgresql+asyncpg://test_user:test_pass@localhost/test_db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_task(db_session: AsyncSession):
    crud = ScheduledTaskCRUD(db_session)
    task = await crud.create(
        skill_name="test",
        schedule_cron="* * * * *",
        next_run_at=datetime.utcnow()
    )
    assert task.id is not None
    assert task.skill_name == "test"
```

---

**Quick Start**: See `docs/P2_T2_ORM_IMPLEMENTATION.md` for full documentation.
