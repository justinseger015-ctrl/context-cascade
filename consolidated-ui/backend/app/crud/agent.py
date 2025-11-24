"""
CRUD operations for Agent model.

All operations include audit logging for NFR2.6 compliance.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.agent import Agent
from app.core.audit_logging import AuditLogger


class AgentCRUD:
    """
    CRUD service for Agent with audit logging.

    Usage:
        crud = AgentCRUD(db_session)
        agent = await crud.create(name="coder-01", type="coder", capabilities=["python", "fastapi"])
        agents = await crud.get_all(status="active")
        await crud.update(agent_id=1, data={"status": "busy"})
        await crud.delete(agent_id=1)
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.audit_logger = AuditLogger(session)

    async def create(
        self,
        name: str,
        type: str,
        capabilities_json: Optional[list] = None,
        status: str = "idle",
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Agent:
        """
        Create a new agent with audit logging.

        Args:
            name: Agent name/identifier
            type: Agent type (coder, reviewer, etc.)
            capabilities_json: List of capabilities
            status: Agent status (default: idle)
            user_id: User creating the agent
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Created Agent instance
        """
        agent = Agent(
            name=name,
            type=type,
            capabilities_json=capabilities_json or [],
            status=status,
        )
        self.session.add(agent)
        await self.session.flush()

        # Audit log
        await self.audit_logger.log_create(
            table_name="agents",
            record_id=agent.id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return agent

    async def get_by_id(self, agent_id: int) -> Optional[Agent]:
        """Get agent by ID."""
        result = await self.session.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Agent]:
        """Get agent by name."""
        result = await self.session.execute(
            select(Agent).where(Agent.name == name)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Agent]:
        """
        Get all agents with optional filters.

        Args:
            type: Filter by agent type
            status: Filter by status
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of Agent instances
        """
        query = select(Agent)

        if type:
            query = query.where(Agent.type == type)
        if status:
            query = query.where(Agent.status == status)

        query = query.order_by(Agent.last_active_at.desc().nulls_last())
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(
        self,
        agent_id: int,
        data: dict,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[Agent]:
        """
        Update agent with audit logging.

        Args:
            agent_id: Agent ID to update
            data: Fields to update (dict)
            user_id: User making the update
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Updated Agent instance or None if not found
        """
        # Get existing agent for audit diff
        agent = await self.get_by_id(agent_id)
        if not agent:
            return None

        old_data = agent.to_dict()

        # Update fields
        for key, value in data.items():
            if hasattr(agent, key):
                setattr(agent, key, value)

        await self.session.flush()

        # Audit log with field diff
        new_data = agent.to_dict()
        await self.audit_logger.log_update(
            table_name="agents",
            record_id=agent_id,
            old_data=old_data,
            new_data=new_data,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return agent

    async def update_activity(self, agent_id: int, status: str = "active") -> bool:
        """
        Update agent last_active_at timestamp and status.

        Args:
            agent_id: Agent ID
            status: New status (default: active)

        Returns:
            True if updated, False if not found
        """
        agent = await self.get_by_id(agent_id)
        if not agent:
            return False

        agent.last_active_at = datetime.utcnow()
        agent.status = status
        await self.session.flush()
        return True

    async def delete(
        self,
        agent_id: int,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """
        Delete agent with audit logging.

        Args:
            agent_id: Agent ID to delete
            user_id: User making the deletion
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            True if deleted, False if not found
        """
        # Check if exists
        agent = await self.get_by_id(agent_id)
        if not agent:
            return False

        # Delete
        await self.session.execute(
            delete(Agent).where(Agent.id == agent_id)
        )

        # Audit log
        await self.audit_logger.log_delete(
            table_name="agents",
            record_id=agent_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return True

    async def count(
        self,
        type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> int:
        """
        Count agents with optional filters.

        Args:
            type: Filter by agent type
            status: Filter by status

        Returns:
            Count of matching agents
        """
        from sqlalchemy import func

        query = select(func.count(Agent.id))

        if type:
            query = query.where(Agent.type == type)
        if status:
            query = query.where(Agent.status == status)

        result = await self.session.execute(query)
        return result.scalar_one()
