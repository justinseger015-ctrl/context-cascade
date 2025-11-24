"""
Audit logging system for NFR2.6 compliance.

Logs all CREATE/UPDATE/DELETE operations with:
- user_id: Who made the change
- timestamp: When the change occurred
- changed_fields: What was changed (JSON diff)
- operation: CREATE, UPDATE, DELETE
- table_name: Which table was affected
"""

from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Column, Integer, String, DateTime, JSON
from app.core.database import Base
import json


class AuditLog(Base):
    """
    Audit log table for tracking all database changes.

    Implements NFR2.6 compliance requirement for audit logging.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(255), index=True, nullable=True)  # User who made the change
    operation = Column(String(10), nullable=False, index=True)  # CREATE, UPDATE, DELETE
    table_name = Column(String(100), nullable=False, index=True)  # Affected table
    record_id = Column(Integer, nullable=False)  # ID of affected record
    changed_fields = Column(JSON, nullable=True)  # JSON diff of changes
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6 address
    user_agent = Column(String(500), nullable=True)  # Browser/client info

    def __repr__(self) -> str:
        return (
            f"<AuditLog(id={self.id}, user={self.user_id}, "
            f"op={self.operation}, table={self.table_name}, "
            f"record={self.record_id}, ts={self.timestamp})>"
        )


class AuditLogger:
    """
    Service for creating audit log entries.

    Usage:
        logger = AuditLogger(db_session)
        await logger.log_create("scheduled_tasks", task.id, user_id="user123")
        await logger.log_update("projects", project.id, old_data, new_data, user_id="user123")
        await logger.log_delete("agents", agent.id, user_id="user123")
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_create(
        self,
        table_name: str,
        record_id: int,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """
        Log a CREATE operation.

        Args:
            table_name: Name of the table
            record_id: ID of created record
            user_id: User who created the record
            ip_address: IP address of client
            user_agent: User agent string

        Returns:
            AuditLog: Created audit log entry
        """
        audit_entry = AuditLog(
            user_id=user_id,
            operation="CREATE",
            table_name=table_name,
            record_id=record_id,
            changed_fields=None,
            timestamp=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.add(audit_entry)
        await self.session.flush()
        return audit_entry

    async def log_update(
        self,
        table_name: str,
        record_id: int,
        old_data: Dict[str, Any],
        new_data: Dict[str, Any],
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """
        Log an UPDATE operation with field-level diff.

        Args:
            table_name: Name of the table
            record_id: ID of updated record
            old_data: Previous values
            new_data: New values
            user_id: User who updated the record
            ip_address: IP address of client
            user_agent: User agent string

        Returns:
            AuditLog: Created audit log entry
        """
        # Calculate diff of changed fields
        changed_fields = {}
        for key in new_data:
            if key in old_data and old_data[key] != new_data[key]:
                changed_fields[key] = {
                    "old": self._serialize_value(old_data[key]),
                    "new": self._serialize_value(new_data[key]),
                }

        audit_entry = AuditLog(
            user_id=user_id,
            operation="UPDATE",
            table_name=table_name,
            record_id=record_id,
            changed_fields=changed_fields,
            timestamp=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.add(audit_entry)
        await self.session.flush()
        return audit_entry

    async def log_delete(
        self,
        table_name: str,
        record_id: int,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """
        Log a DELETE operation.

        Args:
            table_name: Name of the table
            record_id: ID of deleted record
            user_id: User who deleted the record
            ip_address: IP address of client
            user_agent: User agent string

        Returns:
            AuditLog: Created audit log entry
        """
        audit_entry = AuditLog(
            user_id=user_id,
            operation="DELETE",
            table_name=table_name,
            record_id=record_id,
            changed_fields=None,
            timestamp=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.session.add(audit_entry)
        await self.session.flush()
        return audit_entry

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """
        Serialize value for JSON storage.

        Handles datetime, bytes, and other non-JSON types.
        """
        if isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, bytes):
            return value.decode('utf-8', errors='replace')
        elif hasattr(value, '__dict__'):
            return str(value)
        return value

    async def get_audit_trail(
        self,
        table_name: Optional[str] = None,
        record_id: Optional[int] = None,
        user_id: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditLog]:
        """
        Retrieve audit trail with optional filters.

        Args:
            table_name: Filter by table name
            record_id: Filter by record ID
            user_id: Filter by user ID
            limit: Maximum number of entries to return

        Returns:
            List of audit log entries
        """
        query = select(AuditLog).order_by(AuditLog.timestamp.desc())

        if table_name:
            query = query.where(AuditLog.table_name == table_name)
        if record_id:
            query = query.where(AuditLog.record_id == record_id)
        if user_id:
            query = query.where(AuditLog.user_id == user_id)

        query = query.limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()
