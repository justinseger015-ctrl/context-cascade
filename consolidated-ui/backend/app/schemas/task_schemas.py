"""
Pydantic Schemas for Tasks API
Comprehensive input validation and output serialization

Security:
- Cron expression validation
- Input sanitization
- User ownership verification
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from croniter import croniter


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DISABLED = "disabled"
    DELETED = "deleted"  # Soft delete status


class TaskSortField(str, Enum):
    """Allowed sort fields for task listing"""
    CREATED_AT = "created_at"
    NEXT_RUN_AT = "next_run_at"
    UPDATED_AT = "updated_at"
    STATUS = "status"


class SortOrder(str, Enum):
    """Sort order direction"""
    ASC = "asc"
    DESC = "desc"


# Request Schemas

class TaskCreate(BaseModel):
    """
    Schema for creating a new scheduled task

    Validates:
    - Cron expression syntax
    - Skill name format
    - Parameters JSON structure
    """
    skill_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of skill to execute",
        examples=["pair-programming", "code-review-assistant"]
    )
    schedule_cron: str = Field(
        ...,
        min_length=9,  # Minimum valid cron: "* * * * *"
        max_length=100,
        description="Cron expression for scheduling (e.g., '0 0 * * *' for daily at midnight)",
        examples=["0 0 * * *", "*/15 * * * *", "0 9-17 * * 1-5"]
    )
    params: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Execution parameters for the skill",
        examples=[{"mode": "driver", "language": "python"}]
    )
    status: Optional[TaskStatus] = Field(
        default=TaskStatus.PENDING,
        description="Initial task status"
    )

    @field_validator("schedule_cron")
    @classmethod
    def validate_cron_expression(cls, v: str) -> str:
        """
        Validate cron expression syntax using croniter

        Raises:
            ValueError: If cron expression is invalid
        """
        try:
            # Test if croniter can parse the expression
            croniter(v, datetime.now())
            return v
        except (ValueError, KeyError) as e:
            raise ValueError(
                f"Invalid cron expression '{v}': {str(e)}. "
                f"Use format: 'minute hour day month weekday' "
                f"(e.g., '0 0 * * *' for daily at midnight)"
            )

    @field_validator("skill_name")
    @classmethod
    def validate_skill_name(cls, v: str) -> str:
        """
        Validate skill name format

        Raises:
            ValueError: If skill name contains invalid characters
        """
        # Allow alphanumeric, hyphens, underscores
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError(
                f"Skill name '{v}' contains invalid characters. "
                f"Only alphanumeric, hyphens, and underscores are allowed."
            )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "skill_name": "pair-programming",
                    "schedule_cron": "0 9 * * 1-5",
                    "params": {
                        "mode": "driver",
                        "language": "python",
                        "tdd_enabled": True
                    },
                    "status": "pending"
                }
            ]
        }
    }


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task
    All fields are optional for partial updates
    """
    schedule_cron: Optional[str] = Field(
        None,
        min_length=9,
        max_length=100,
        description="New cron expression"
    )
    params: Optional[Dict[str, Any]] = Field(
        None,
        description="Updated execution parameters"
    )
    status: Optional[TaskStatus] = Field(
        None,
        description="New task status"
    )

    @field_validator("schedule_cron")
    @classmethod
    def validate_cron_expression(cls, v: Optional[str]) -> Optional[str]:
        """Validate cron expression if provided"""
        if v is not None:
            try:
                croniter(v, datetime.now())
            except (ValueError, KeyError) as e:
                raise ValueError(f"Invalid cron expression '{v}': {str(e)}")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "schedule_cron": "0 */2 * * *",
                    "params": {"mode": "navigator"},
                    "status": "pending"
                }
            ]
        }
    }


# Response Schemas

class ExecutionResultResponse(BaseModel):
    """Execution result nested in task response"""
    id: int
    started_at: datetime
    ended_at: Optional[datetime]
    status: str
    duration_ms: Optional[int]
    output_text: Optional[str] = None
    error_text: Optional[str] = None

    model_config = {"from_attributes": True}


class TaskResponse(BaseModel):
    """
    Schema for task detail response
    Includes execution history when requested
    """
    id: int
    skill_name: str
    schedule_cron: str
    next_run_at: datetime
    params_json: Dict[str, Any] = Field(alias="params")
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    user_id: Optional[str]
    execution_results: Optional[List[ExecutionResultResponse]] = Field(
        default=None,
        description="Execution history (only included in detail view)"
    )

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 123,
                    "skill_name": "pair-programming",
                    "schedule_cron": "0 9 * * 1-5",
                    "next_run_at": "2025-11-09T09:00:00Z",
                    "params": {"mode": "driver", "language": "python"},
                    "status": "pending",
                    "created_at": "2025-11-08T10:30:00Z",
                    "updated_at": "2025-11-08T10:30:00Z",
                    "user_id": "user_12345",
                    "execution_results": []
                }
            ]
        }
    }


class TaskListResponse(BaseModel):
    """
    Schema for paginated task list response
    """
    tasks: List[TaskResponse]
    total: int = Field(..., description="Total number of tasks matching filters")
    limit: int = Field(..., description="Maximum results per page")
    offset: int = Field(..., description="Number of results skipped")
    has_more: bool = Field(..., description="Whether more results are available")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tasks": [
                        {
                            "id": 123,
                            "skill_name": "pair-programming",
                            "schedule_cron": "0 9 * * 1-5",
                            "next_run_at": "2025-11-09T09:00:00Z",
                            "params": {"mode": "driver"},
                            "status": "pending",
                            "created_at": "2025-11-08T10:30:00Z",
                            "updated_at": "2025-11-08T10:30:00Z",
                            "user_id": "user_12345"
                        }
                    ],
                    "total": 42,
                    "limit": 20,
                    "offset": 0,
                    "has_more": True
                }
            ]
        }
    }


class TaskDeleteResponse(BaseModel):
    """Response for task deletion"""
    message: str = Field(..., description="Success message")
    task_id: int = Field(..., description="ID of deleted task")
    status: str = Field(..., description="New status (deleted)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Task successfully deleted",
                    "task_id": 123,
                    "status": "deleted"
                }
            ]
        }
    }


# Query Parameters Schema

class TaskQueryParams(BaseModel):
    """
    Query parameters for task listing
    Used for OpenAPI documentation and validation
    """
    status: Optional[TaskStatus] = Field(
        None,
        description="Filter by task status"
    )
    skill_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Filter by skill name (exact match)"
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of results (1-100)"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of results to skip for pagination"
    )
    sort_by: TaskSortField = Field(
        default=TaskSortField.CREATED_AT,
        description="Field to sort by"
    )
    sort_order: SortOrder = Field(
        default=SortOrder.DESC,
        description="Sort order (ascending or descending)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "pending",
                    "skill_name": "pair-programming",
                    "limit": 20,
                    "offset": 0,
                    "sort_by": "created_at",
                    "sort_order": "desc"
                }
            ]
        }
    }
