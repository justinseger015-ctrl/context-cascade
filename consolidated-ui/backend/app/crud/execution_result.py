"""
CRUD operations for ExecutionResult model.

All operations include audit logging for NFR2.6 compliance.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.execution_result import ExecutionResult
from app.core.audit_logging import AuditLogger


class ExecutionResultCRUD:
    """
    CRUD service for ExecutionResult with audit logging.

    Usage:
        crud = ExecutionResultCRUD(db_session)
        result = await crud.create(task_id=1, started_at=datetime.utcnow())
        results = await crud.get_by_task_id(task_id=1)
        await crud.update(result_id=1, data={"status": "success", "ended_at": datetime.utcnow()})
        await crud.delete(result_id=1)
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.audit_logger = AuditLogger(session)

    async def create(
        self,
        task_id: int,
        started_at: datetime,
        status: str = "running",
        output_text: Optional[str] = None,
        error_text: Optional[str] = None,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> ExecutionResult:
        """
        Create a new execution result with audit logging.

        Args:
            task_id: Foreign key to scheduled_tasks
            started_at: Execution start time
            status: Execution status
            output_text: Execution output
            error_text: Error messages
            user_id: User triggering execution
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Created ExecutionResult instance
        """
        result = ExecutionResult(
            task_id=task_id,
            started_at=started_at,
            status=status,
            output_text=output_text,
            error_text=error_text,
        )
        self.session.add(result)
        await self.session.flush()

        # Audit log
        await self.audit_logger.log_create(
            table_name="execution_results",
            record_id=result.id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return result

    async def get_by_id(self, result_id: int) -> Optional[ExecutionResult]:
        """Get execution result by ID."""
        result = await self.session.execute(
            select(ExecutionResult).where(ExecutionResult.id == result_id)
        )
        return result.scalar_one_or_none()

    async def get_by_task_id(
        self,
        task_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ExecutionResult]:
        """
        Get all execution results for a task.

        Args:
            task_id: Task ID to filter by
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of ExecutionResult instances
        """
        query = (
            select(ExecutionResult)
            .where(ExecutionResult.task_id == task_id)
            .order_by(ExecutionResult.started_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all(
        self,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ExecutionResult]:
        """
        Get all execution results with optional filters.

        Args:
            status: Filter by status
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of ExecutionResult instances
        """
        query = select(ExecutionResult)

        if status:
            query = query.where(ExecutionResult.status == status)

        query = query.order_by(ExecutionResult.started_at.desc())
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(
        self,
        result_id: int,
        data: dict,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[ExecutionResult]:
        """
        Update execution result with audit logging.

        Args:
            result_id: Result ID to update
            data: Fields to update (dict)
            user_id: User making the update
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            Updated ExecutionResult instance or None if not found
        """
        # Get existing result for audit diff
        result = await self.get_by_id(result_id)
        if not result:
            return None

        old_data = result.to_dict()

        # Update fields
        for key, value in data.items():
            if hasattr(result, key):
                setattr(result, key, value)

        # Calculate duration if ended_at is provided
        if "ended_at" in data and result.ended_at:
            delta = result.ended_at - result.started_at
            result.duration_ms = int(delta.total_seconds() * 1000)

        await self.session.flush()

        # Audit log with field diff
        new_data = result.to_dict()
        await self.audit_logger.log_update(
            table_name="execution_results",
            record_id=result_id,
            old_data=old_data,
            new_data=new_data,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return result

    async def complete_execution(
        self,
        result_id: int,
        status: str,
        ended_at: datetime,
        output_text: Optional[str] = None,
        error_text: Optional[str] = None,
    ) -> Optional[ExecutionResult]:
        """
        Mark execution as complete with final status.

        Args:
            result_id: Result ID to complete
            status: Final status (success, failed, timeout)
            ended_at: Execution end time
            output_text: Final output
            error_text: Error messages if failed

        Returns:
            Updated ExecutionResult instance or None if not found
        """
        data = {
            "status": status,
            "ended_at": ended_at,
        }
        if output_text is not None:
            data["output_text"] = output_text
        if error_text is not None:
            data["error_text"] = error_text

        return await self.update(result_id, data)

    async def delete(
        self,
        result_id: int,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> bool:
        """
        Delete execution result with audit logging.

        Args:
            result_id: Result ID to delete
            user_id: User making the deletion
            ip_address: Client IP address
            user_agent: Client user agent

        Returns:
            True if deleted, False if not found
        """
        # Check if exists
        result = await self.get_by_id(result_id)
        if not result:
            return False

        # Delete
        await self.session.execute(
            delete(ExecutionResult).where(ExecutionResult.id == result_id)
        )

        # Audit log
        await self.audit_logger.log_delete(
            table_name="execution_results",
            record_id=result_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return True

    async def get_statistics(self, task_id: Optional[int] = None) -> dict:
        """
        Get execution statistics.

        Args:
            task_id: Optional task ID to filter by

        Returns:
            Dictionary with statistics (total, success, failed, avg_duration_ms)
        """
        from sqlalchemy import func

        query = select(
            func.count(ExecutionResult.id).label("total"),
            func.sum(
                func.case((ExecutionResult.status == "success", 1), else_=0)
            ).label("success"),
            func.sum(
                func.case((ExecutionResult.status == "failed", 1), else_=0)
            ).label("failed"),
            func.avg(ExecutionResult.duration_ms).label("avg_duration_ms"),
        )

        if task_id:
            query = query.where(ExecutionResult.task_id == task_id)

        result = await self.session.execute(query)
        row = result.one()

        return {
            "total": row.total or 0,
            "success": row.success or 0,
            "failed": row.failed or 0,
            "avg_duration_ms": float(row.avg_duration_ms) if row.avg_duration_ms else 0,
        }
