"""
Projects CRUD API Router

Implements comprehensive Projects CRUD with:
- OWASP BOLA protection (verify user owns resource)
- Memory MCP integration with tagging
- Search, pagination, sorting
- Nested tasks display
- Soft delete with cascade
- OpenAPI documentation
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import or_, func, case

from app.database import get_db
from app.models import Project, Task, User
from app.schemas.project_schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    ProjectListResponse,
    SortBy,
    ProjectStatus,
    TaskSummary
)
from app.utils.memory_mcp import memory_mcp_client
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/projects",
    tags=["projects"],
    responses={
        401: {"description": "Unauthorized - Missing or invalid authentication"},
        403: {"description": "Forbidden - User does not own this resource"},
        404: {"description": "Not Found - Project does not exist"},
    }
)


# Dependency: Get current user (mock for now, replace with actual auth)
async def get_current_user() -> User:
    """
    Get current authenticated user.

    TODO: Replace with actual authentication (JWT, OAuth, etc.)
    For now, returns a mock user.

    Raises:
        HTTPException: 401 if authentication fails
    """
    # Mock user for development - REPLACE WITH REAL AUTH
    mock_user = User(id=1, email="user@example.com", username="testuser")
    return mock_user


def verify_project_ownership(
    project: Project,
    user: User
) -> None:
    """
    Verify that the user owns the project (OWASP BOLA protection).

    Args:
        project: Project to verify
        user: Current authenticated user

    Raises:
        HTTPException: 403 if user does not own the project
    """
    if project.user_id != user.id:
        logger.warning(
            f"BOLA attempt: User {user.id} tried to access project {project.id} "
            f"owned by user {project.user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this project"
        )


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="""
    Create a new project with name and optional description.

    **Security**: Requires authentication. Project will be owned by authenticated user.

    **Memory MCP**: Project creation is logged to Memory MCP with tagging.
    """
)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ProjectResponse:
    """
    Create a new project.

    Args:
        project_data: Project creation data
        db: Database session
        current_user: Authenticated user

    Returns:
        Created project with ID
    """
    try:
        # Create project
        new_project = Project(
            name=project_data.name,
            description=project_data.description,
            user_id=current_user.id,
            status=ProjectStatus.ACTIVE
        )

        db.add(new_project)
        db.commit()
        db.refresh(new_project)

        # Calculate tasks count (will be 0 for new project)
        new_project.tasks_count = 0

        # Store in Memory MCP with tagging
        try:
            memory_key = f"projects/{current_user.id}/{new_project.id}"
            memory_value = {
                "project_id": new_project.id,
                "name": new_project.name,
                "description": new_project.description,
                "user_id": current_user.id,
                "created_at": new_project.created_at.isoformat(),
                "action": "created"
            }

            await memory_mcp_client.store(
                key=memory_key,
                value=memory_value,
                tags={
                    "WHO": "backend-api-developer",
                    "WHEN": datetime.utcnow().isoformat(),
                    "PROJECT": "ruv-sparc-ui-dashboard",
                    "WHY": "implementation",
                    "entity_type": "project",
                    "user_id": str(current_user.id),
                    "project_id": str(new_project.id)
                }
            )
            logger.info(f"Stored project {new_project.id} in Memory MCP")
        except Exception as e:
            # Log but don't fail the request if memory storage fails
            logger.error(f"Failed to store in Memory MCP: {e}")

        logger.info(
            f"User {current_user.id} created project {new_project.id}: {new_project.name}"
        )

        return ProjectResponse.model_validate(new_project)

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )


@router.get(
    "/",
    response_model=ProjectListResponse,
    summary="List projects with search, pagination, and sorting",
    description="""
    List all projects owned by the authenticated user.

    **Features**:
    - Search by name or description (case-insensitive)
    - Pagination with limit and offset
    - Sorting by created_at, tasks_count, or name (ascending/descending)

    **Security**: Only returns projects owned by the authenticated user.
    """
)
async def list_projects(
    search: Optional[str] = Query(
        None,
        description="Search term for name or description (case-insensitive)",
        examples=["project"]
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Number of projects per page (1-100)"
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of projects to skip"
    ),
    sort_by: SortBy = Query(
        SortBy.CREATED_AT_DESC,
        description="Sort field and direction"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ProjectListResponse:
    """
    List projects with filtering, pagination, and sorting.

    Args:
        search: Optional search term
        limit: Page size
        offset: Pagination offset
        sort_by: Sort field and direction
        db: Database session
        current_user: Authenticated user

    Returns:
        Paginated list of projects
    """
    try:
        # Base query - only user's projects, exclude deleted
        query = db.query(
            Project,
            func.count(Task.id).label('tasks_count')
        ).outerjoin(
            Task,
            (Task.project_id == Project.id) & (Task.status != "deleted")
        ).filter(
            Project.user_id == current_user.id,
            Project.status != ProjectStatus.DELETED
        ).group_by(Project.id)

        # Apply search filter
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Project.name.ilike(search_pattern),
                    Project.description.ilike(search_pattern)
                )
            )

        # Count total before pagination
        total = query.count()

        # Apply sorting
        if sort_by == SortBy.CREATED_AT_ASC:
            query = query.order_by(Project.created_at.asc())
        elif sort_by == SortBy.CREATED_AT_DESC:
            query = query.order_by(Project.created_at.desc())
        elif sort_by == SortBy.TASKS_COUNT_ASC:
            query = query.order_by(func.count(Task.id).asc())
        elif sort_by == SortBy.TASKS_COUNT_DESC:
            query = query.order_by(func.count(Task.id).desc())
        elif sort_by == SortBy.NAME_ASC:
            query = query.order_by(Project.name.asc())
        elif sort_by == SortBy.NAME_DESC:
            query = query.order_by(Project.name.desc())

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute query
        results = query.all()

        # Build response with tasks_count
        projects = []
        for project, tasks_count in results:
            project_dict = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "user_id": project.user_id,
                "status": project.status,
                "tasks_count": tasks_count or 0,
                "created_at": project.created_at,
                "updated_at": project.updated_at
            }
            projects.append(ProjectResponse(**project_dict))

        logger.info(
            f"User {current_user.id} listed projects: {len(projects)} of {total} "
            f"(search={search}, limit={limit}, offset={offset}, sort={sort_by})"
        )

        return ProjectListResponse(
            total=total,
            limit=limit,
            offset=offset,
            projects=projects
        )

    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list projects"
        )


@router.get(
    "/{project_id}",
    response_model=ProjectDetailResponse,
    summary="Get project details with nested tasks",
    description="""
    Get detailed information about a specific project, including all associated tasks.

    **Security**: User must own the project (OWASP BOLA protection).

    **Returns**: Project with nested list of tasks, tasks_count, timestamps.
    """
)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ProjectDetailResponse:
    """
    Get project by ID with nested tasks.

    Args:
        project_id: Project ID
        db: Database session
        current_user: Authenticated user

    Returns:
        Project with nested tasks list

    Raises:
        HTTPException: 404 if project not found, 403 if user doesn't own project
    """
    try:
        # Query project with eager loading of tasks
        project = db.query(Project).options(
            selectinload(Project.tasks)
        ).filter(
            Project.id == project_id,
            Project.status != ProjectStatus.DELETED
        ).first()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        # OWASP BOLA protection
        verify_project_ownership(project, current_user)

        # Filter out deleted tasks
        active_tasks = [t for t in project.tasks if t.status != "deleted"]

        # Build response
        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "user_id": project.user_id,
            "status": project.status,
            "tasks_count": len(active_tasks),
            "tasks": [TaskSummary.model_validate(task) for task in active_tasks],
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }

        logger.info(
            f"User {current_user.id} retrieved project {project_id} with {len(active_tasks)} tasks"
        )

        return ProjectDetailResponse(**project_dict)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get project"
        )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
    description="""
    Update project name and/or description.

    **Security**: User must own the project (OWASP BOLA protection).

    All fields are optional - only provided fields will be updated.
    """
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ProjectResponse:
    """
    Update project.

    Args:
        project_id: Project ID
        project_data: Fields to update
        db: Database session
        current_user: Authenticated user

    Returns:
        Updated project

    Raises:
        HTTPException: 404 if project not found, 403 if user doesn't own project
    """
    try:
        # Get project
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.status != ProjectStatus.DELETED
        ).first()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        # OWASP BOLA protection
        verify_project_ownership(project, current_user)

        # Update fields
        update_data = project_data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        for field, value in update_data.items():
            setattr(project, field, value)

        project.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(project)

        # Calculate tasks count
        tasks_count = db.query(func.count(Task.id)).filter(
            Task.project_id == project_id,
            Task.status != "deleted"
        ).scalar() or 0

        # Store update in Memory MCP
        try:
            memory_key = f"projects/{current_user.id}/{project_id}/updates"
            memory_value = {
                "project_id": project_id,
                "updated_fields": list(update_data.keys()),
                "updated_at": project.updated_at.isoformat(),
                "action": "updated"
            }

            await memory_mcp_client.store(
                key=memory_key,
                value=memory_value,
                tags={
                    "WHO": "backend-api-developer",
                    "WHEN": datetime.utcnow().isoformat(),
                    "PROJECT": "ruv-sparc-ui-dashboard",
                    "WHY": "implementation",
                    "entity_type": "project_update",
                    "user_id": str(current_user.id),
                    "project_id": str(project_id)
                }
            )
        except Exception as e:
            logger.error(f"Failed to store update in Memory MCP: {e}")

        logger.info(
            f"User {current_user.id} updated project {project_id}: {update_data}"
        )

        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "user_id": project.user_id,
            "status": project.status,
            "tasks_count": tasks_count,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }

        return ProjectResponse(**project_dict)

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project"
        )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project (soft delete with cascade)",
    description="""
    Soft delete a project by marking it as deleted.

    **Security**: User must own the project (OWASP BOLA protection).

    **Cascade**: All tasks in the project will also be soft deleted.

    **Note**: This is a soft delete - data is not physically removed from database.
    """
)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Soft delete project and cascade to tasks.

    Args:
        project_id: Project ID
        db: Database session
        current_user: Authenticated user

    Raises:
        HTTPException: 404 if project not found, 403 if user doesn't own project
    """
    try:
        # Get project
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.status != ProjectStatus.DELETED
        ).first()

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )

        # OWASP BOLA protection
        verify_project_ownership(project, current_user)

        # Soft delete project
        project.status = ProjectStatus.DELETED
        project.updated_at = datetime.utcnow()

        # Cascade soft delete to all tasks
        tasks_deleted = db.query(Task).filter(
            Task.project_id == project_id,
            Task.status != "deleted"
        ).update(
            {
                "status": "deleted",
                "updated_at": datetime.utcnow()
            },
            synchronize_session=False
        )

        db.commit()

        # Store deletion in Memory MCP
        try:
            memory_key = f"projects/{current_user.id}/{project_id}/deletion"
            memory_value = {
                "project_id": project_id,
                "tasks_deleted": tasks_deleted,
                "deleted_at": project.updated_at.isoformat(),
                "action": "deleted"
            }

            await memory_mcp_client.store(
                key=memory_key,
                value=memory_value,
                tags={
                    "WHO": "backend-api-developer",
                    "WHEN": datetime.utcnow().isoformat(),
                    "PROJECT": "ruv-sparc-ui-dashboard",
                    "WHY": "implementation",
                    "entity_type": "project_deletion",
                    "user_id": str(current_user.id),
                    "project_id": str(project_id)
                }
            )
        except Exception as e:
            logger.error(f"Failed to store deletion in Memory MCP: {e}")

        logger.info(
            f"User {current_user.id} deleted project {project_id} "
            f"and cascaded to {tasks_deleted} tasks"
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project"
        )
