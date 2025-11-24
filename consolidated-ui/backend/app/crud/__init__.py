"""
CRUD operations for all models.

All operations include audit logging for NFR2.6 compliance.
"""

from app.crud.scheduled_task import ScheduledTaskCRUD
from app.crud.project import ProjectCRUD
from app.crud.agent import AgentCRUD
from app.crud.execution_result import ExecutionResultCRUD

__all__ = [
    "ScheduledTaskCRUD",
    "ProjectCRUD",
    "AgentCRUD",
    "ExecutionResultCRUD",
]
