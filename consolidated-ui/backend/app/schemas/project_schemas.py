"""
Project API Schemas

Pydantic models for Projects CRUD API with comprehensive validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, validator
from enum import Enum


class ProjectStatus(str, Enum):
    """Project status enumeration"""
    ACTIVE = "active"
    DELETED = "deleted"
    ARCHIVED = "archived"


class ProjectBase(BaseModel):
    """Base project schema with common fields"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Project name (required, 1-255 characters)",
        examples=["My Awesome Project"]
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Project description (optional, max 2000 characters)",
        examples=["A project to build an amazing application"]
    )

    @validator('name')
    def validate_name(cls, v):
        """Validate name is not empty after stripping whitespace"""
        if not v or not v.strip():
            raise ValueError("Project name cannot be empty or whitespace only")
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        """Strip whitespace from description"""
        if v:
            return v.strip()
        return v


class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project (all fields optional)"""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated project name",
        examples=["Updated Project Name"]
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Updated project description",
        examples=["Updated description"]
    )

    @validator('name')
    def validate_name(cls, v):
        """Validate name if provided"""
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Project name cannot be empty or whitespace only")
            return v.strip()
        return v

    @validator('description')
    def validate_description(cls, v):
        """Strip whitespace from description if provided"""
        if v is not None:
            return v.strip() if v else None
        return v

    model_config = ConfigDict(
        extra="forbid",  # Reject unknown fields
        json_schema_extra={
            "example": {
                "name": "Updated Project",
                "description": "Updated project description"
            }
        }
    )


class TaskSummary(BaseModel):
    """Minimal task information for nested display"""
    id: int
    title: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectResponse(ProjectBase):
    """Schema for project response (single project)"""
    id: int
    user_id: int
    status: ProjectStatus
    tasks_count: int = Field(
        0,
        description="Number of tasks in this project"
    )
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "My Project",
                "description": "Project description",
                "user_id": 123,
                "status": "active",
                "tasks_count": 5,
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:00:00Z"
            }
        }
    )


class ProjectDetailResponse(ProjectResponse):
    """Schema for detailed project response with nested tasks"""
    tasks: List[TaskSummary] = Field(
        default_factory=list,
        description="List of tasks in this project"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "My Project",
                "description": "Project description",
                "user_id": 123,
                "status": "active",
                "tasks_count": 2,
                "tasks": [
                    {
                        "id": 1,
                        "title": "Task 1",
                        "status": "pending",
                        "priority": "high",
                        "created_at": "2025-01-01T12:00:00Z",
                        "updated_at": "2025-01-01T12:00:00Z"
                    }
                ],
                "created_at": "2025-01-01T12:00:00Z",
                "updated_at": "2025-01-01T12:00:00Z"
            }
        }
    )


class ProjectListResponse(BaseModel):
    """Schema for paginated project list response"""
    total: int = Field(..., description="Total number of projects matching the query")
    limit: int = Field(..., description="Number of items per page")
    offset: int = Field(..., description="Current offset")
    projects: List[ProjectResponse] = Field(
        ...,
        description="List of projects"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 100,
                "limit": 20,
                "offset": 0,
                "projects": [
                    {
                        "id": 1,
                        "name": "Project 1",
                        "description": "Description 1",
                        "user_id": 123,
                        "status": "active",
                        "tasks_count": 5,
                        "created_at": "2025-01-01T12:00:00Z",
                        "updated_at": "2025-01-01T12:00:00Z"
                    }
                ]
            }
        }
    )


class SortBy(str, Enum):
    """Valid sort fields for project listing"""
    CREATED_AT_ASC = "created_at"
    CREATED_AT_DESC = "-created_at"
    TASKS_COUNT_ASC = "tasks_count"
    TASKS_COUNT_DESC = "-tasks_count"
    NAME_ASC = "name"
    NAME_DESC = "-name"
