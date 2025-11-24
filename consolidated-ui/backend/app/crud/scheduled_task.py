"""
CRUD operations for ScheduledTask model.

All operations include audit logging for NFR2.6 compliance.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scheduled_task import ScheduledTask
from app.core.audit_logging import AuditLogger


class ScheduledTaskCRUD:
    """
    CRUD service for ScheduledTask with audit logging.

    Usage:
        crud = ScheduledTaskCRUD(db_session)
        task = await crud.create(skill_name="test", schedule_cron="* * * * *", user_id="user123")
        tasks = await crud.get_all(user_id="user123", status="pending")
        await crud.update(task_id=1, data={"status": "completed"}, user_id="user123")
        await crud.delete(task_id=1, user_id="user123")
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.audit_logger = AuditLogger(session)

    async def create(
        self,
        skill_name: str,
        schedule_cron: str,
        next_run_at: datetime,
        params_json: Optional[dict] = None,
        status: str = "pending",
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> ScheduledTask:
        """
        Create a new scheduled task with audit logging.

        Args:
            skill_name: Name of skill to execute
            schedule_cron: Cron expression
            next_run_at: Next execution time
            params_json: Execution parameters
            status: Task status (default: pending)
            user_id: User creating the task
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Created ScheduledTask instance
        """
        task = ScheduledTask(
            skill_name=skill_name,
            schedule_cron=schedule_cron,
            next_run_at=next_run_at,
            params_json=params_json or {},
            status=status,
            user_id=user_id,
        )
        self.session.add(task)
        await self.session.flush()

        # Audit log
        await self.audit_logger.log_create(
            table_name="scheduled_tasks",
            record_id=task.id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return task

    async def get_by_id(self, task_id: int) -> Optional[ScheduledTask]:
        """Get task by ID."""
        result = await self.session.execute(
            select(ScheduledTask).where(ScheduledTask.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ScheduledTask]:
        """
        Get all tasks with optional filters.

        Args:
            user_id: Filter by user ID
            status: Filter by status
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of ScheduledTask instances
        """
        query = select(ScheduledTask)

        if user_id:
            query = query.where(ScheduledTask.user_id == user_id)
        if status:
            query = query.where(ScheduledTask.status == status)

        query = query.order_by(ScheduledTask.created_at.desc())
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_pending_tasks(self, limit: int = 10) -> List[ScheduledTask]:
        """
        Get pending tasks ready for execution.

        Returns tasks with status='pending' and next_run_at <= now.
        """
        query = (
            select(ScheduledTask)
            .where(ScheduledTask.status == "pending")
            .where(ScheduledTask.next_run_at <= datetime.utcnow())
            .order_by(ScheduledTask.next_run_at)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(
        self,
        task_id: int,
        data: dict,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[ScheduledTask]:
        """
        Update task with audit logging.

        Args:
            task_id: Task ID to update
            data: Fields to update (dict)
            user_id: User making the update
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Updated ScheduledTask instance or None if not found
        """
        # Get existing task for audit diff
        task = await self.get_by_id(task_id)
        if not task:
            return None

        old_data = task.to_dict()

        # Update fields
        for key, value in data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        task.updated_at = datetime.utcnow()

        await self.session.flush()

        # Audit log with field diff
        new_data = task.to_dict()
        await self.audit_logger.log_update(
            table_name="scheduled_tasks",
            record_id=task_id,
            old_data=old_data,
            new_data=new_data,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return task

    async def delete(
        self,
        task_id: int,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """
        Delete task with audit logging.

        Args:
            task_id: Task ID to delete
            user_id: User making the deletion
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            True if deleted, False if not found
        """
        # Check if exists
        task = await self.get_by_id(task_id)
        if not task:
            return False

        # Delete
        await self.session.execute(
            delete(ScheduledTask).where(ScheduledTask.id == task_id)
        )

        # Audit log
        await self.audit_logger.log_delete(
            table_name="scheduled_tasks",
            record_id=task_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return True

    async def count(
        self,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> int:
        """
        Count tasks with optional filters.

        Args:
            user_id: Filter by user ID
            status: Filter by status

        Returns:
            Count of matching tasks
        """
        from sqlalchemy import func

        query = select(func.count(ScheduledTask.id))

        if user_id:
            query = query.where(ScheduledTask.user_id == user_id)
        if status:
            query = query.where(ScheduledTask.status == status)

        result = await self.session.execute(query)
        return result.scalar_one()
