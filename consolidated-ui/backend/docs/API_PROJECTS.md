# Projects API Documentation

## Overview

The Projects API provides comprehensive CRUD operations for managing projects with:
- ✅ OWASP API1:2023 BOLA protection on all endpoints
- ✅ Memory MCP integration with automatic tagging
- ✅ Advanced search, pagination, and sorting
- ✅ Nested tasks display
- ✅ Soft delete with cascade to tasks
- ✅ Comprehensive input validation

## Base URL

```
/api/v1/projects
```

## Authentication

All endpoints require authentication. Include user credentials in request headers.

**Mock Authentication (Development)**:
Currently using mock user with `id=1`. Replace with JWT/OAuth in production.

## Endpoints

### 1. Create Project

**POST** `/api/v1/projects/`

Create a new project owned by the authenticated user.

**Request Body**:
```json
{
  "name": "My Awesome Project",
  "description": "Optional project description"
}
```

**Validation Rules**:
- `name`: Required, 1-255 characters, cannot be whitespace only
- `description`: Optional, max 2000 characters

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "My Awesome Project",
  "description": "Optional project description",
  "user_id": 1,
  "status": "active",
  "tasks_count": 0,
  "created_at": "2025-01-08T12:00:00Z",
  "updated_at": "2025-01-08T12:00:00Z"
}
```

**Memory MCP Storage**:
Project creation is automatically logged to Memory MCP with tags:
- `WHO`: backend-api-developer
- `WHEN`: ISO timestamp
- `PROJECT`: ruv-sparc-ui-dashboard
- `WHY`: implementation
- `entity_type`: project
- `user_id`: User ID
- `project_id`: Project ID

**Example**:
```bash
curl -X POST http://localhost:8000/api/v1/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Project",
    "description": "My new project"
  }'
```

---

### 2. List Projects

**GET** `/api/v1/projects/`

List all projects owned by the authenticated user with advanced filtering.

**Query Parameters**:
- `search` (optional): Search term for name or description (case-insensitive)
- `limit` (optional): Items per page (1-100, default: 20)
- `offset` (optional): Pagination offset (default: 0)
- `sort_by` (optional): Sort field and direction
  - `created_at` (default: descending)
  - `-created_at` (ascending)
  - `tasks_count` (descending)
  - `-tasks_count` (ascending)
  - `name` (descending)
  - `-name` (ascending)

**Response** (200 OK):
```json
{
  "total": 100,
  "limit": 20,
  "offset": 0,
  "projects": [
    {
      "id": 1,
      "name": "Project 1",
      "description": "Description 1",
      "user_id": 1,
      "status": "active",
      "tasks_count": 5,
      "created_at": "2025-01-08T12:00:00Z",
      "updated_at": "2025-01-08T12:00:00Z"
    }
  ]
}
```

**BOLA Protection**:
Only returns projects owned by the authenticated user.

**Examples**:
```bash
# List all projects (first page)
curl http://localhost:8000/api/v1/projects/

# Search for "API" in name or description
curl http://localhost:8000/api/v1/projects/?search=API

# Pagination: second page with 10 items
curl http://localhost:8000/api/v1/projects/?limit=10&offset=10

# Sort by tasks_count descending
curl http://localhost:8000/api/v1/projects/?sort_by=-tasks_count

# Combine: search + pagination + sort
curl "http://localhost:8000/api/v1/projects/?search=API&limit=20&offset=0&sort_by=-created_at"
```

---

### 3. Get Project Details

**GET** `/api/v1/projects/{project_id}`

Get detailed information about a specific project, including nested tasks.

**Path Parameters**:
- `project_id`: Project ID (integer)

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "My Project",
  "description": "Project description",
  "user_id": 1,
  "status": "active",
  "tasks_count": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Task 1",
      "status": "pending",
      "priority": "high",
      "created_at": "2025-01-08T12:00:00Z",
      "updated_at": "2025-01-08T12:00:00Z"
    },
    {
      "id": 2,
      "title": "Task 2",
      "status": "completed",
      "priority": "medium",
      "created_at": "2025-01-08T13:00:00Z",
      "updated_at": "2025-01-08T14:00:00Z"
    }
  ],
  "created_at": "2025-01-08T12:00:00Z",
  "updated_at": "2025-01-08T12:00:00Z"
}
```

**BOLA Protection**:
Verifies user owns the project before returning. Returns 403 if user doesn't own the project.

**Error Responses**:
- `404 Not Found`: Project doesn't exist or is deleted
- `403 Forbidden`: User doesn't own the project

**Example**:
```bash
curl http://localhost:8000/api/v1/projects/1
```

---

### 4. Update Project

**PUT** `/api/v1/projects/{project_id}`

Update project name and/or description.

**Path Parameters**:
- `project_id`: Project ID (integer)

**Request Body** (all fields optional):
```json
{
  "name": "Updated Project Name",
  "description": "Updated description"
}
```

**Validation Rules**:
- `name`: If provided, 1-255 characters, cannot be whitespace only
- `description`: If provided, max 2000 characters
- At least one field must be provided

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Updated Project Name",
  "description": "Updated description",
  "user_id": 1,
  "status": "active",
  "tasks_count": 5,
  "created_at": "2025-01-08T12:00:00Z",
  "updated_at": "2025-01-08T15:00:00Z"
}
```

**BOLA Protection**:
Verifies user owns the project before updating.

**Memory MCP Storage**:
Updates are logged to Memory MCP with updated fields and timestamp.

**Error Responses**:
- `400 Bad Request`: No fields to update
- `404 Not Found`: Project doesn't exist or is deleted
- `403 Forbidden`: User doesn't own the project
- `422 Unprocessable Entity`: Validation error

**Examples**:
```bash
# Update name only
curl -X PUT http://localhost:8000/api/v1/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name"}'

# Update both name and description
curl -X PUT http://localhost:8000/api/v1/projects/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "description": "Updated description"
  }'
```

---

### 5. Delete Project

**DELETE** `/api/v1/projects/{project_id}`

Soft delete a project and cascade to all associated tasks.

**Path Parameters**:
- `project_id`: Project ID (integer)

**Response** (204 No Content):
Empty response body.

**Behavior**:
- **Soft Delete**: Project is marked as `status=deleted`, not physically removed
- **Cascade**: All tasks in the project are also soft deleted
- **Reversible**: Deleted projects can be restored by admin if needed

**BOLA Protection**:
Verifies user owns the project before deleting.

**Memory MCP Storage**:
Deletion is logged to Memory MCP with count of cascaded tasks.

**Error Responses**:
- `404 Not Found`: Project doesn't exist or is already deleted
- `403 Forbidden`: User doesn't own the project

**Example**:
```bash
curl -X DELETE http://localhost:8000/api/v1/projects/1
```

---

## Security Features

### OWASP BOLA Protection (API1:2023)

All endpoints implement **Broken Object Level Authorization (BOLA)** protection:

1. **Automatic Ownership**: Projects are automatically owned by the authenticated user on creation
2. **Ownership Verification**: Before any read/update/delete operation, we verify `project.user_id == current_user.id`
3. **Detailed Logging**: All BOLA attempts are logged with user IDs for security monitoring

**Example BOLA Protection Code**:
```python
def verify_project_ownership(project: Project, user: User) -> None:
    if project.user_id != user.id:
        logger.warning(
            f"BOLA attempt: User {user.id} tried to access project {project.id} "
            f"owned by user {project.user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this project"
        )
```

### Input Validation

Comprehensive validation using Pydantic:
- **Length constraints**: Name (1-255), description (0-2000)
- **Whitespace handling**: Names cannot be whitespace only
- **Type safety**: All fields have strict type definitions
- **Unknown fields**: Rejected in update requests

### Error Handling

Consistent error responses across all endpoints:
- Database errors are caught and return 500
- Validation errors return 422 with details
- Authorization errors return 403
- Not found errors return 404

---

## Data Models

### ProjectCreate
```python
{
  "name": str,           # Required, 1-255 chars
  "description": str?    # Optional, max 2000 chars
}
```

### ProjectUpdate
```python
{
  "name": str?,          # Optional, 1-255 chars
  "description": str?    # Optional, max 2000 chars
}
```

### ProjectResponse
```python
{
  "id": int,
  "name": str,
  "description": str?,
  "user_id": int,
  "status": "active" | "deleted" | "archived",
  "tasks_count": int,
  "created_at": datetime,
  "updated_at": datetime
}
```

### ProjectDetailResponse
```python
{
  ...ProjectResponse,
  "tasks": [
    {
      "id": int,
      "title": str,
      "status": str,
      "priority": str,
      "created_at": datetime,
      "updated_at": datetime
    }
  ]
}
```

### ProjectListResponse
```python
{
  "total": int,
  "limit": int,
  "offset": int,
  "projects": [ProjectResponse]
}
```

---

## OpenAPI/Swagger

Access interactive API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

All endpoints are automatically documented with:
- Request/response schemas
- Validation rules
- Example requests/responses
- Error codes and descriptions
- Security requirements

---

## Testing

Comprehensive test suite in `backend/app/tests/test_projects.py`:

**Test Coverage**:
- ✅ CRUD operations (create, list, get, update, delete)
- ✅ Input validation (empty names, length limits, unknown fields)
- ✅ Search functionality (name, description)
- ✅ Pagination (limit, offset, edge cases)
- ✅ Sorting (all fields, ascending/descending)
- ✅ BOLA protection (ownership verification)
- ✅ Soft delete cascade (tasks marked as deleted)
- ✅ Nested tasks display
- ✅ Error handling (404, 403, 422, 500)
- ✅ Full CRUD lifecycle integration

**Run Tests**:
```bash
cd backend
pytest app/tests/test_projects.py -v
```

---

## Performance Considerations

### Database Queries

1. **Eager Loading**: Tasks are eager loaded with `selectinload()` to avoid N+1 queries
2. **Indexes**: Ensure indexes on `user_id`, `status`, `created_at` for fast filtering
3. **Soft Delete Filtering**: Always filter `status != 'deleted'` in WHERE clause

### Pagination

- Default limit: 20 items
- Max limit: 100 items
- Use offset-based pagination for consistency

### Search

- Case-insensitive ILIKE pattern matching
- Searches both name and description fields
- Recommended: Add full-text search index for large datasets

---

## Memory MCP Integration

All project operations are logged to Memory MCP with consistent tagging:

**Create Event**:
```json
{
  "key": "projects/{user_id}/{project_id}",
  "value": {
    "project_id": 1,
    "name": "Project Name",
    "description": "Description",
    "user_id": 1,
    "created_at": "2025-01-08T12:00:00Z",
    "action": "created"
  },
  "tags": {
    "WHO": "backend-api-developer",
    "WHEN": "2025-01-08T12:00:00Z",
    "PROJECT": "ruv-sparc-ui-dashboard",
    "WHY": "implementation",
    "entity_type": "project",
    "user_id": "1",
    "project_id": "1"
  }
}
```

**Benefits**:
- Cross-session memory persistence
- Audit trail for all operations
- Analytics and reporting data
- Debugging and troubleshooting

---

## Migration from Placeholder

This implementation replaces the placeholder in `routers/projects.py`:

**Before** (P2_T1):
```python
@router.post("")
async def create_project(...):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Project creation not yet implemented"
    )
```

**After** (P2_T6):
```python
@router.post("/")
async def create_project(...) -> ProjectResponse:
    new_project = Project(...)
    db.add(new_project)
    db.commit()
    # Memory MCP integration
    # BOLA protection
    # Comprehensive validation
    return ProjectResponse.model_validate(new_project)
```

---

## Production Checklist

Before deploying to production:

- [ ] Replace mock authentication with JWT/OAuth
- [ ] Add database indexes on `user_id`, `status`, `created_at`
- [ ] Configure rate limiting (e.g., 100 req/min per user)
- [ ] Enable CORS for frontend domain
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Add request ID tracking for debugging
- [ ] Configure Memory MCP production endpoint
- [ ] Set up database backups
- [ ] Add health check endpoint
- [ ] Configure logging aggregation

---

## Future Enhancements

Potential improvements:

1. **Archiving**: Add archive/unarchive functionality
2. **Sharing**: Share projects between users
3. **Webhooks**: Notify on project events
4. **Activity Log**: Detailed audit trail per project
5. **Bulk Operations**: Create/update/delete multiple projects
6. **Advanced Search**: Full-text search, filters by date range
7. **Project Templates**: Create projects from templates
8. **Export**: Export project data to CSV/JSON

---

## Support

For issues or questions:
- Repository: https://github.com/your-org/ruv-sparc-ui-dashboard
- Documentation: `/docs`
- API Reference: `http://localhost:8000/docs`
