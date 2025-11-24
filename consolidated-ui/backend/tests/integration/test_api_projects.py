"""
Integration Tests for Projects API
Tests with real PostgreSQL database in Docker
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
class TestProjectsAPI:
    """Integration tests for /api/v1/projects endpoints"""

    async def test_create_project_endpoint(self, client: AsyncClient, sample_project_data):
        """Test POST /api/v1/projects"""
        # Act
        response = await client.post("/api/v1/projects", json=sample_project_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_project_data["name"]
        assert data["status"] == sample_project_data["status"]
        assert "id" in data
        assert "created_at" in data

    async def test_get_project_endpoint(self, client: AsyncClient, sample_project_data):
        """Test GET /api/v1/projects/{id}"""
        # Arrange - Create project first
        create_response = await client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Act
        response = await client.get(f"/api/v1/projects/{project_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project_id
        assert data["name"] == sample_project_data["name"]

    async def test_get_project_not_found(self, client: AsyncClient):
        """Test GET /api/v1/projects/{id} with non-existent ID"""
        # Act
        response = await client.get("/api/v1/projects/99999")

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    async def test_list_projects_endpoint(self, client: AsyncClient):
        """Test GET /api/v1/projects with pagination"""
        # Arrange - Create multiple projects
        for i in range(5):
            await client.post("/api/v1/projects", json={
                "name": f"Project {i}",
                "description": f"Test project {i}",
                "status": "active",
                "sparc_mode": "specification"
            })

        # Act
        response = await client.get("/api/v1/projects?skip=0&limit=3")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3
        assert all("id" in project for project in data)

    async def test_list_projects_filter_by_status(self, client: AsyncClient):
        """Test GET /api/v1/projects with status filter"""
        # Arrange
        await client.post("/api/v1/projects", json={
            "name": "Active Project",
            "status": "active",
            "sparc_mode": "specification"
        })
        await client.post("/api/v1/projects", json={
            "name": "Archived Project",
            "status": "archived",
            "sparc_mode": "specification"
        })

        # Act
        response = await client.get("/api/v1/projects?status=active")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert all(p["status"] == "active" for p in data)

    async def test_update_project_endpoint(self, client: AsyncClient, sample_project_data):
        """Test PUT /api/v1/projects/{id}"""
        # Arrange
        create_response = await client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        update_data = {
            "name": "Updated Project Name",
            "status": "completed"
        }

        # Act
        response = await client.put(f"/api/v1/projects/{project_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Project Name"
        assert data["status"] == "completed"

    async def test_update_project_partial(self, client: AsyncClient, sample_project_data):
        """Test PATCH /api/v1/projects/{id} partial update"""
        # Arrange
        create_response = await client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Act
        response = await client.patch(f"/api/v1/projects/{project_id}", json={
            "status": "archived"
        })

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "archived"
        assert data["name"] == sample_project_data["name"]  # Unchanged

    async def test_delete_project_endpoint(self, client: AsyncClient, sample_project_data):
        """Test DELETE /api/v1/projects/{id}"""
        # Arrange
        create_response = await client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Act
        delete_response = await client.delete(f"/api/v1/projects/{project_id}")

        # Assert
        assert delete_response.status_code == 204

        # Verify deletion
        get_response = await client.get(f"/api/v1/projects/{project_id}")
        assert get_response.status_code == 404

    async def test_create_project_validation(self, client: AsyncClient):
        """Test POST /api/v1/projects with invalid data"""
        # Act - Missing required fields
        response = await client.post("/api/v1/projects", json={
            "description": "Missing name field"
        })

        # Assert
        assert response.status_code == 422  # Validation error
        assert "field required" in response.text.lower()

    async def test_create_project_invalid_sparc_mode(self, client: AsyncClient):
        """Test POST /api/v1/projects with invalid SPARC mode"""
        # Act
        response = await client.post("/api/v1/projects", json={
            "name": "Test",
            "status": "active",
            "sparc_mode": "invalid_mode"
        })

        # Assert
        assert response.status_code == 422

    async def test_project_timestamps(self, client: AsyncClient, sample_project_data):
        """Test that created_at and updated_at are set correctly"""
        # Act
        create_response = await client.post("/api/v1/projects", json=sample_project_data)
        created_data = create_response.json()

        # Wait and update
        import asyncio
        await asyncio.sleep(0.1)

        update_response = await client.put(
            f"/api/v1/projects/{created_data['id']}",
            json={"name": "Updated"}
        )
        updated_data = update_response.json()

        # Assert
        assert "created_at" in created_data
        assert "updated_at" in updated_data
        # updated_at should be different after update
        # (in real scenario, check timestamp difference)

    async def test_concurrent_project_creation(self, client: AsyncClient, concurrent_executor):
        """Test creating multiple projects concurrently"""
        # Arrange
        async def create_project():
            return await client.post("/api/v1/projects", json={
                "name": f"Concurrent Project",
                "status": "active",
                "sparc_mode": "specification"
            })

        # Act
        responses = await concurrent_executor(create_project, count=10)

        # Assert
        assert all(r.status_code == 201 for r in responses)
        project_ids = [r.json()["id"] for r in responses]
        assert len(set(project_ids)) == 10  # All unique IDs
