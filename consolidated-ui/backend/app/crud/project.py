"""
CRUD operations for Project model.

All operations include audit logging for NFR2.6 compliance.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project
from app.core.audit_logging import AuditLogger


class ProjectCRUD:
    """
    CRUD service for Project with audit logging.

    Usage:
        crud = ProjectCRUD(db_session)
        project = await crud.create(name="My Project", user_id="user123")
        projects = await crud.get_all(user_id="user123")
        await crud.update(project_id=1, data={"description": "Updated"}, user_id="user123")
        await crud.delete(project_id=1, user_id="user123")
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.audit_logger = AuditLogger(session)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Project:
        """
        Create a new project with audit logging.

        Args:
            name: Project name
            description: Project description
            user_id: User creating the project
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Created Project instance
        """
        project = Project(
            name=name,
            description=description,
            user_id=user_id,
            tasks_count=0,
        )
        self.session.add(project)
        await self.session.flush()

        # Audit log
        await self.audit_logger.log_create(
            table_name="projects",
            record_id=project.id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return project

    async def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        result = await self.session.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        user_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Project]:
        """
        Get all projects with optional filters.

        Args:
            user_id: Filter by user ID
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of Project instances
        """
        query = select(Project)

        if user_id:
            query = query.where(Project.user_id == user_id)

        query = query.order_by(Project.created_at.desc())
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(
        self,
        project_id: int,
        data: dict,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[Project]:
        """
        Update project with audit logging.

        Args:
            project_id: Project ID to update
            data: Fields to update (dict)
            user_id: User making the update
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Updated Project instance or None if not found
        """
        # Get existing project for audit diff
        project = await self.get_by_id(project_id)
        if not project:
            return None

        old_data = project.to_dict()

        # Update fields
        for key, value in data.items():
            if hasattr(project, key):
                setattr(project, key, value)
        project.updated_at = datetime.utcnow()

        await self.session.flush()

        # Audit log with field diff
        new_data = project.to_dict()
        await self.audit_logger.log_update(
            table_name="projects",
            record_id=project_id,
            old_data=old_data,
            new_data=new_data,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return project

    async def delete(
        self,
        project_id: int,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """
        Delete project with audit logging.

        Args:
            project_id: Project ID to delete
            user_id: User making the deletion
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            True if deleted, False if not found
        """
        # Check if exists
        project = await self.get_by_id(project_id)
        if not project:
            return False

        # Delete
        await self.session.execute(
            delete(Project).where(Project.id == project_id)
        )

        # Audit log
        await self.audit_logger.log_delete(
            table_name="projects",
            record_id=project_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return True

    async def increment_task_count(self, project_id: int) -> bool:
        """
        Increment tasks_count for a project.

        Args:
            project_id: Project ID

        Returns:
            True if updated, False if not found
        """
        project = await self.get_by_id(project_id)
        if not project:
            return False

        project.tasks_count += 1
        await self.session.flush()
        return True

    async def count(self, user_id: Optional[str] = None) -> int:
        """
        Count projects with optional filters.

        Args:
            user_id: Filter by user ID

        Returns:
            Count of matching projects
        """
        from sqlalchemy import func

        query = select(func.count(Project.id))

        if user_id:
            query = query.where(Project.user_id == user_id)

        result = await self.session.execute(query)
        return result.scalar_one()
