"""
Unit Tests for Agent CRUD Operations
London School TDD: Tests with mocked database dependencies
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from app.crud.agent import (
    create_agent,
    get_agent,
    get_agents,
    update_agent,
    delete_agent,
    get_agents_by_type,
)
from app.models.agent import Agent


@pytest.mark.unit
@pytest.mark.asyncio
class TestAgentCRUD:
    """Test Agent CRUD operations with mocked database"""

    async def test_create_agent_success(self, mock_db_session, sample_agent_data):
        """Test successful agent creation"""
        # Arrange
        mock_db_session.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, 'id', 1))

        # Act
        result = await create_agent(mock_db_session, sample_agent_data)

        # Assert
        assert result.name == sample_agent_data["name"]
        assert result.agent_type == sample_agent_data["agent_type"]
        assert result.status == sample_agent_data["status"]
        assert result.capabilities == sample_agent_data["capabilities"]
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    async def test_create_agent_with_capabilities(self, mock_db_session):
        """Test agent creation with multiple capabilities"""
        # Arrange
        agent_data = {
            "name": "multi-capability-agent",
            "agent_type": "coder",
            "status": "active",
            "capabilities": ["python", "javascript", "testing", "debugging"],
            "metadata": {"skill_level": "expert"}
        }

        # Act
        result = await create_agent(mock_db_session, agent_data)

        # Assert
        assert len(result.capabilities) == 4
        assert "python" in result.capabilities
        assert "debugging" in result.capabilities

    async def test_get_agent_found(self, mock_db_session):
        """Test getting existing agent"""
        # Arrange
        agent_id = 1
        mock_agent = Agent(
            id=agent_id,
            name="test-agent",
            agent_type="researcher",
            status="active",
            capabilities=["research"]
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_agent
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await get_agent(mock_db_session, agent_id)

        # Assert
        assert result is not None
        assert result.id == agent_id
        assert result.name == "test-agent"

    async def test_get_agent_not_found(self, mock_db_session):
        """Test getting non-existent agent"""
        # Arrange
        agent_id = 999
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await get_agent(mock_db_session, agent_id)

        # Assert
        assert result is None

    async def test_get_agents_with_pagination(self, mock_db_session):
        """Test getting agents with skip and limit"""
        # Arrange
        mock_agents = [
            Agent(id=i, name=f"agent-{i}", agent_type="coder", status="active")
            for i in range(1, 11)
        ]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_agents[5:10]
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await get_agents(mock_db_session, skip=5, limit=5)

        # Assert
        assert len(result) == 5
        assert result[0].id == 6

    async def test_get_agents_by_type(self, mock_db_session):
        """Test filtering agents by type"""
        # Arrange
        researcher_agents = [
            Agent(id=i, name=f"researcher-{i}", agent_type="researcher", status="active")
            for i in range(1, 4)
        ]
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = researcher_agents
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await get_agents_by_type(mock_db_session, "researcher")

        # Assert
        assert len(result) == 3
        assert all(a.agent_type == "researcher" for a in result)

    async def test_update_agent_success(self, mock_db_session):
        """Test successful agent update"""
        # Arrange
        agent_id = 1
        existing_agent = Agent(
            id=agent_id,
            name="old-agent",
            agent_type="coder",
            status="active",
            capabilities=["python"]
        )
        update_data = {
            "name": "new-agent",
            "status": "inactive",
            "capabilities": ["python", "javascript", "typescript"]
        }
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_agent
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await update_agent(mock_db_session, agent_id, update_data)

        # Assert
        assert result.name == "new-agent"
        assert result.status == "inactive"
        assert len(result.capabilities) == 3
        mock_db_session.commit.assert_called_once()

    async def test_update_agent_add_capabilities(self, mock_db_session):
        """Test adding capabilities to existing agent"""
        # Arrange
        agent_id = 1
        existing_agent = Agent(
            id=agent_id,
            name="agent",
            agent_type="coder",
            status="active",
            capabilities=["python"]
        )
        update_data = {
            "capabilities": ["python", "rust", "go"]
        }
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_agent
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await update_agent(mock_db_session, agent_id, update_data)

        # Assert
        assert "rust" in result.capabilities
        assert "go" in result.capabilities
        assert len(result.capabilities) == 3

    async def test_delete_agent_success(self, mock_db_session):
        """Test successful agent deletion"""
        # Arrange
        agent_id = 1
        existing_agent = Agent(
            id=agent_id,
            name="to-delete",
            agent_type="coder",
            status="active"
        )
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_agent
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await delete_agent(mock_db_session, agent_id)

        # Assert
        assert result is True
        mock_db_session.delete.assert_called_once()
        mock_db_session.commit.assert_called_once()

    async def test_delete_agent_not_found(self, mock_db_session):
        """Test deleting non-existent agent"""
        # Arrange
        agent_id = 999
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await delete_agent(mock_db_session, agent_id)

        # Assert
        assert result is False
        mock_db_session.delete.assert_not_called()

    async def test_create_agent_all_types(self, mock_db_session):
        """Test creating agents of all valid types"""
        agent_types = ["coder", "researcher", "tester", "reviewer", "architect"]

        for agent_type in agent_types:
            # Arrange
            agent_data = {
                "name": f"{agent_type}-agent",
                "agent_type": agent_type,
                "status": "active",
                "capabilities": [agent_type]
            }

            # Act
            result = await create_agent(mock_db_session, agent_data)

            # Assert
            assert result.agent_type == agent_type
            assert agent_type in result.capabilities

    async def test_update_agent_metadata(self, mock_db_session):
        """Test updating agent metadata"""
        # Arrange
        agent_id = 1
        existing_agent = Agent(
            id=agent_id,
            name="agent",
            agent_type="coder",
            status="active",
            metadata={"version": "1.0"}
        )
        update_data = {
            "metadata": {
                "version": "2.0",
                "performance_score": 95,
                "last_task": "authentication"
            }
        }
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_agent
        mock_db_session.execute.return_value = mock_result

        # Act
        result = await update_agent(mock_db_session, agent_id, update_data)

        # Assert
        assert result.metadata["version"] == "2.0"
        assert result.metadata["performance_score"] == 95
        assert "last_task" in result.metadata
