"""
Integration tests for Tasks CRUD API
Tests all endpoints with various scenarios and edge cases

Security Testing:
- OWASP BOLA protection verification
- JWT authentication requirements
- User ownership validation

Functionality Testing:
- CRUD operations
- Cron validation
- Pagination and filtering
- Error handling
"""

import pytest
from datetime import datetime
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.middleware.auth import create_access_token
from app.models.scheduled_task import ScheduledTask
from app.models.execution_result import ExecutionResult


# Fixtures

@pytest.fixture
async def auth_headers():
    """Create authentication headers with JWT token"""
    token = create_access_token(user_id=1, email="test@example.com")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def other_user_headers():
    """Create authentication headers for different user (BOLA testing)"""
    token = create_access_token(user_id=2, email="other@example.com")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def sample_task_data():
    """Sample task creation data"""
    return {
        "skill_name": "pair-programming",
        "schedule_cron": "0 9 * * 1-5",  # Weekdays at 9 AM
        "params": {
            "mode": "driver",
            "language": "python",
            "tdd_enabled": True
        },
        "status": "pending"
    }


# POST /api/v1/tasks Tests

@pytest.mark.asyncio
async def test_create_task_success(auth_headers, sample_task_data):
    """Test successful task creation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/tasks",
            json=sample_task_data,
            headers=auth_headers
        )

    assert response.status_code == 201
    data = response.json()
    assert data["skill_name"] == sample_task_data["skill_name"]
    assert data["schedule_cron"] == sample_task_data["schedule_cron"]
    assert data["params"] == sample_task_data["params"]
    assert data["status"] == "pending"
    assert "id" in data
    assert "next_run_at" in data
    assert "created_at" in data
    assert data["user_id"] == "1"


@pytest.mark.asyncio
async def test_create_task_invalid_cron(auth_headers):
    """Test task creation with invalid cron expression"""
    invalid_data = {
        "skill_name": "test-skill",
        "schedule_cron": "invalid cron",  # Invalid
        "params": {}
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/tasks",
            json=invalid_data,
            headers=auth_headers
        )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_create_task_invalid_skill_name(auth_headers):
    """Test task creation with invalid skill name characters"""
    invalid_data = {
        "skill_name": "skill with spaces!",  # Invalid characters
        "schedule_cron": "0 0 * * *",
        "params": {}
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/tasks",
            json=invalid_data,
            headers=auth_headers
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_no_auth():
    """Test task creation without authentication"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/tasks",
            json={"skill_name": "test", "schedule_cron": "0 0 * * *"}
        )

    assert response.status_code == 401


# GET /api/v1/tasks Tests

@pytest.mark.asyncio
async def test_list_tasks_success(auth_headers, db_session):
    """Test successful task listing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/tasks",
            headers=auth_headers
        )

    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert "has_more" in data
    assert isinstance(data["tasks"], list)


@pytest.mark.asyncio
async def test_list_tasks_with_filters(auth_headers):
    """Test task listing with status filter"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/tasks",
            params={"status": "pending", "limit": 10, "offset": 0},
            headers=auth_headers
        )

    assert response.status_code == 200
    data = response.json()
    assert data["limit"] == 10
    assert data["offset"] == 0


@pytest.mark.asyncio
async def test_list_tasks_pagination(auth_headers):
    """Test task listing pagination"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First page
        response1 = await client.get(
            "/api/v1/tasks",
            params={"limit": 5, "offset": 0},
            headers=auth_headers
        )

        # Second page
        response2 = await client.get(
            "/api/v1/tasks",
            params={"limit": 5, "offset": 5},
            headers=auth_headers
        )

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    # Verify pagination metadata
    assert data1["limit"] == 5
    assert data1["offset"] == 0
    assert data2["offset"] == 5


@pytest.mark.asyncio
async def test_list_tasks_bola_protection(auth_headers, other_user_headers, db_session):
    """Test that users only see their own tasks (BOLA protection)"""
    # User 1 creates a task
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {}
            },
            headers=auth_headers
        )

        # User 1 lists tasks
        response1 = await client.get("/api/v1/tasks", headers=auth_headers)

        # User 2 lists tasks (should not see User 1's task)
        response2 = await client.get("/api/v1/tasks", headers=other_user_headers)

    data1 = response1.json()
    data2 = response2.json()

    # User 1 should see their task
    assert len(data1["tasks"]) > 0

    # User 2 should not see User 1's task
    user1_task_ids = [task["id"] for task in data1["tasks"]]
    user2_task_ids = [task["id"] for task in data2["tasks"]]
    assert not any(tid in user2_task_ids for tid in user1_task_ids)


# GET /api/v1/tasks/{id} Tests

@pytest.mark.asyncio
async def test_get_task_success(auth_headers, db_session):
    """Test successful task retrieval by ID"""
    # Create a task first
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_response = await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {"key": "value"}
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Get the task
        response = await client.get(
            f"/api/v1/tasks/{task_id}",
            headers=auth_headers
        )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert "execution_results" in data


@pytest.mark.asyncio
async def test_get_task_not_found(auth_headers):
    """Test getting non-existent task"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/tasks/99999",
            headers=auth_headers
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_task_bola_protection(auth_headers, other_user_headers, db_session):
    """Test that users cannot access other users' tasks (BOLA)"""
    # User 1 creates a task
    async with AsyncClient(app=app, base_url="http://test") as client:
        create_response = await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {}
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # User 2 tries to access User 1's task
        response = await client.get(
            f"/api/v1/tasks/{task_id}",
            headers=other_user_headers
        )

    assert response.status_code == 403  # Forbidden


# PUT /api/v1/tasks/{id} Tests

@pytest.mark.asyncio
async def test_update_task_success(auth_headers, db_session):
    """Test successful task update"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create task
        create_response = await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {"old": "value"}
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Update task
        update_data = {
            "schedule_cron": "0 12 * * *",  # Change to noon
            "params": {"new": "value"},
            "status": "disabled"
        }

        response = await client.put(
            f"/api/v1/tasks/{task_id}",
            json=update_data,
            headers=auth_headers
        )

    assert response.status_code == 200
    data = response.json()
    assert data["schedule_cron"] == "0 12 * * *"
    assert data["params"] == {"new": "value"}
    assert data["status"] == "disabled"


@pytest.mark.asyncio
async def test_update_task_partial(auth_headers, db_session):
    """Test partial task update (only some fields)"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create task
        create_response = await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {"key": "value"}
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]
        original_cron = create_response.json()["schedule_cron"]

        # Update only params
        response = await client.put(
            f"/api/v1/tasks/{task_id}",
            json={"params": {"updated": "params"}},
            headers=auth_headers
        )

    assert response.status_code == 200
    data = response.json()
    assert data["params"] == {"updated": "params"}
    assert data["schedule_cron"] == original_cron  # Unchanged


@pytest.mark.asyncio
async def test_update_task_bola_protection(auth_headers, other_user_headers, db_session):
    """Test that users cannot update other users' tasks"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # User 1 creates task
        create_response = await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {}
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # User 2 tries to update User 1's task
        response = await client.put(
            f"/api/v1/tasks/{task_id}",
            json={"status": "disabled"},
            headers=other_user_headers
        )

    assert response.status_code == 403


# DELETE /api/v1/tasks/{id} Tests

@pytest.mark.asyncio
async def test_delete_task_success(auth_headers, db_session):
    """Test successful task deletion (soft delete)"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create task
        create_response = await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {}
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # Delete task
        response = await client.delete(
            f"/api/v1/tasks/{task_id}",
            headers=auth_headers
        )

    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "deleted"
    assert "successfully deleted" in data["message"].lower()


@pytest.mark.asyncio
async def test_delete_task_soft_delete_verification(auth_headers, db_session):
    """Test that deletion is soft delete (task still exists with status=deleted)"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create and delete task
        create_response = await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {}
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)

        # Verify task still exists in database with deleted status
        # (This would require direct database access in real test)
        response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)

        # Task should still be retrievable but with deleted status
        assert response.status_code == 200
        assert response.json()["status"] == "deleted"


@pytest.mark.asyncio
async def test_delete_task_bola_protection(auth_headers, other_user_headers, db_session):
    """Test that users cannot delete other users' tasks"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # User 1 creates task
        create_response = await client.post(
            "/api/v1/tasks",
            json={
                "skill_name": "test-skill",
                "schedule_cron": "0 0 * * *",
                "params": {}
            },
            headers=auth_headers
        )
        task_id = create_response.json()["id"]

        # User 2 tries to delete User 1's task
        response = await client.delete(
            f"/api/v1/tasks/{task_id}",
            headers=other_user_headers
        )

    assert response.status_code == 403


# Edge Cases and Validation Tests

@pytest.mark.asyncio
async def test_cron_validation_edge_cases(auth_headers):
    """Test various cron expression formats"""
    test_cases = [
        ("* * * * *", True),          # Every minute - valid
        ("0 0 * * *", True),          # Daily at midnight - valid
        ("0 */2 * * *", True),        # Every 2 hours - valid
        ("0 9-17 * * 1-5", True),     # Weekdays 9-5 - valid
        ("invalid", False),            # Invalid format
        ("60 0 * * *", False),        # Invalid minute (60)
        ("0 25 * * *", False),        # Invalid hour (25)
        ("", False),                   # Empty
    ]

    async with AsyncClient(app=app, base_url="http://test") as client:
        for cron_expr, should_succeed in test_cases:
            response = await client.post(
                "/api/v1/tasks",
                json={
                    "skill_name": "test-skill",
                    "schedule_cron": cron_expr,
                    "params": {}
                },
                headers=auth_headers
            )

            if should_succeed:
                assert response.status_code == 201, f"Failed for valid cron: {cron_expr}"
            else:
                assert response.status_code in [400, 422], f"Accepted invalid cron: {cron_expr}"


@pytest.mark.asyncio
async def test_pagination_limits(auth_headers):
    """Test pagination limit validation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Valid limits
        response = await client.get(
            "/api/v1/tasks",
            params={"limit": 1, "offset": 0},
            headers=auth_headers
        )
        assert response.status_code == 200

        response = await client.get(
            "/api/v1/tasks",
            params={"limit": 100, "offset": 0},
            headers=auth_headers
        )
        assert response.status_code == 200

        # Invalid limits
        response = await client.get(
            "/api/v1/tasks",
            params={"limit": 0},  # Too small
            headers=auth_headers
        )
        assert response.status_code == 422

        response = await client.get(
            "/api/v1/tasks",
            params={"limit": 101},  # Too large
            headers=auth_headers
        )
        assert response.status_code == 422
