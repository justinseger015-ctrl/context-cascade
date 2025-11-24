"""
Unit Tests for Project CRUD Operations
London School TDD: Tests with mocked database dependencies
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import (
    create_project,
    get_project,
    get_projects,
    update_project,
    delete_project,
)
from app.models.project import Project


@pytest.mark.unit
@pytest.mark.asyncio
class TestProjectCRUD:
    """Test Project CRUD operations with mocked database"""

    async def test_create_project_success(self, mock_db_session, sample_project_data):
        """Test successful project creation"""
        # Arrange
        mock_project = Project(
            id=1,
            **sample_project_data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        mock_db_session.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, 'id', 1))

        # Act
        result = await create_project(mock_db_session, sample_project_data)

        # Assert
        assert result.name == sample_project_data["name"]
        assert result.description == sample_project_data["description"]
        assert result.status == sample_project_data["status"]
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    async def test_create_project_with_metadata(self, mock_db_session):
        """Test project creation with metadata"""
        # Arrange
        project_data = {
            "name": "Metadata Project",
            "description": "Project with metadata",
            "status": "active",
            "sparc_mode": "architecture",
            "metadata": {
                "owner": "admin",
                "priority": "high",
                "tags": ["important", "urgent"]
            }
        }

        # Act
        result = await create_project(mock_db_session, project_data)

        # Assert
        assert result.metadata == project_data["metadata"]
        assert "owner" in result.metadata
        assert result.metadata["priority"] == "high"

    async def test_get_project_found(self, mock_db_session):
        """Test getting existing project"""
        # Arrange
        project_id = 1
        mock_project = Project(
            id=project_id,
            name="Test Project",
            description="Test",
            status="active",
            sparc_mode="specification"
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_project
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await get_project(mock_db_session, project_id)

        # Assert
        assert result is not None
        assert result.id == project_id
        assert result.name == "Test Project"
        mock_db_session.execute.assert_called_once()

    async def test_get_project_not_found(self, mock_db_session):
        """Test getting non-existent project"""
        # Arrange
        project_id = 999
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await get_project(mock_db_session, project_id)

        # Assert
        assert result is None

    async def test_get_projects_with_pagination(self, mock_db_session):
        """Test getting projects with skip and limit"""
        # Arrange
        mock_projects = [
            Project(id=i, name=f"Project {i}", status="active", sparc_mode="specification")
            for i in range(1, 6)
        ]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_projects[2:4]  # Skip 2, limit 2
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await get_projects(mock_db_session, skip=2, limit=2)

        # Assert
        assert len(result) == 2
        assert result[0].id == 3
        assert result[1].id == 4

    async def test_get_projects_filter_by_status(self, mock_db_session):
        """Test filtering projects by status"""
        # Arrange
        active_projects = [
            Project(id=i, name=f"Active {i}", status="active", sparc_mode="specification")
            for i in range(1, 4)
        ]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = active_projects
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await get_projects(mock_db_session, status="active")

        # Assert
        assert len(result) == 3
        assert all(p.status == "active" for p in result)

    async def test_update_project_success(self, mock_db_session):
        """Test successful project update"""
        # Arrange
        project_id = 1
        existing_project = Project(
            id=project_id,
            name="Old Name",
            description="Old Description",
            status="active",
            sparc_mode="specification"
        )
        update_data = {
            "name": "New Name",
            "description": "New Description",
            "status": "completed"
        }
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_project
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await update_project(mock_db_session, project_id, update_data)

        # Assert
        assert result.name == "New Name"
        assert result.description == "New Description"
        assert result.status == "completed"
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    async def test_update_project_partial(self, mock_db_session):
        """Test partial project update (only some fields)"""
        # Arrange
        project_id = 1
        existing_project = Project(
            id=project_id,
            name="Original Name",
            description="Original Description",
            status="active",
            sparc_mode="specification"
        )
        update_data = {"status": "archived"}
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_project
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await update_project(mock_db_session, project_id, update_data)

        # Assert
        assert result.name == "Original Name"  # Unchanged
        assert result.description == "Original Description"  # Unchanged
        assert result.status == "archived"  # Updated

    async def test_update_project_not_found(self, mock_db_session):
        """Test updating non-existent project"""
        # Arrange
        project_id = 999
        update_data = {"name": "New Name"}
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await update_project(mock_db_session, project_id, update_data)

        # Assert
        assert result is None
        mock_db_session.commit.assert_not_called()

    async def test_delete_project_success(self, mock_db_session):
        """Test successful project deletion"""
        # Arrange
        project_id = 1
        existing_project = Project(
            id=project_id,
            name="To Delete",
            status="active",
            sparc_mode="specification"
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_project
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await delete_project(mock_db_session, project_id)

        # Assert
        assert result is True
        mock_db_session.delete.assert_called_once_with(existing_project)
        mock_db_session.commit.assert_called_once()

    async def test_delete_project_not_found(self, mock_db_session):
        """Test deleting non-existent project"""
        # Arrange
        project_id = 999
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await delete_project(mock_db_session, project_id)

        # Assert
        assert result is False
        mock_db_session.delete.assert_not_called()
        mock_db_session.commit.assert_not_called()

    async def test_create_project_with_sparc_modes(self, mock_db_session):
        """Test creating projects with different SPARC modes"""
        sparc_modes = ["specification", "pseudocode", "architecture", "refinement", "completion"]

        for mode in sparc_modes:
            # Arrange
            project_data = {
                "name": f"SPARC {mode}",
                "description": f"Testing {mode} mode",
                "status": "active",
                "sparc_mode": mode
            }

            # Act
            result = await create_project(mock_db_session, project_data)

            # Assert
            assert result.sparc_mode == mode
            assert mode in result.name

    async def test_update_project_metadata(self, mock_db_session):
        """Test updating project metadata"""
        # Arrange
        project_id = 1
        existing_project = Project(
            id=project_id,
            name="Test",
            status="active",
            sparc_mode="specification",
            metadata={"version": "1.0", "tags": ["old"]}
        )
        update_data = {
            "metadata": {
                "version": "2.0",
                "tags": ["new", "updated"],
                "priority": "high"
            }
        }
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_project
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await update_project(mock_db_session, project_id, update_data)

        # Assert
        assert result.metadata["version"] == "2.0"
        assert "priority" in result.metadata
        assert "new" in result.metadata["tags"]
