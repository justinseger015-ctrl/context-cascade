# Projects API - Quick Reference

## 🚀 5 Endpoints Overview

```
POST   /api/v1/projects/           Create project
GET    /api/v1/projects/           List projects (search, pagination, sort)
GET    /api/v1/projects/{id}       Get project with tasks
PUT    /api/v1/projects/{id}       Update project
DELETE /api/v1/projects/{id}       Delete project (soft delete + cascade)
```

---

## 📝 Quick Examples

### Create Project
```bash
curl -X POST http://localhost:8000/api/v1/projects/ \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project", "description": "Optional"}'

# Response:
{
  "id": 1,
  "name": "My Project",
  "user_id": 1,
  "status": "active",
  "tasks_count": 0,
  "created_at": "2025-01-08T12:00:00Z",
  "updated_at": "2025-01-08T12:00:00Z"
}
```

### List Projects (with search, pagination, sort)
```bash
# All projects
curl http://localhost:8000/api/v1/projects/

# Search
curl "http://localhost:8000/api/v1/projects/?search=API"

# Pagination
curl "http://localhost:8000/api/v1/projects/?limit=10&offset=20"

# Sort by tasks_count descending
curl "http://localhost:8000/api/v1/projects/?sort_by=-tasks_count"

# Combine all
curl "http://localhost:8000/api/v1/projects/?search=API&limit=20&offset=0&sort_by=-created_at"
```

### Get Project (with nested tasks)
```bash
curl http://localhost:8000/api/v1/projects/1

# Response includes tasks array:
{
  "id": 1,
  "name": "My Project",
  "tasks_count": 2,
  "tasks": [
    {"id": 1, "title": "Task 1", "status": "pending", ...},
    {"id": 2, "title": "Task 2", "status": "completed", ...}
  ]
}
```

### Update Project
```bash
# Update name only
curl -X PUT http://localhost:8000/api/v1/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name"}'

# Update both
curl -X PUT http://localhost:8000/api/v1/projects/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name", "description": "New desc"}'
```

### Delete Project (soft delete + cascade)
```bash
curl -X DELETE http://localhost:8000/api/v1/projects/1

# Returns 204 No Content
# Project and all tasks marked as deleted
```

---

## 🔒 Security Features

### OWASP BOLA Protection
- ✅ All endpoints verify user owns resource
- ✅ Returns 403 if unauthorized access attempt
- ✅ Detailed logging of BOLA attempts

### Validation
- Name: 1-255 characters, not whitespace only
- Description: Max 2000 characters
- Unknown fields rejected in updates

---

## 🎯 Search & Filter Options

### Search
- Case-insensitive
- Searches name AND description
- Example: `?search=API` matches "API Project", "building an API"

### Pagination
- `limit`: 1-100 (default: 20)
- `offset`: Starting position (default: 0)
- Returns `total` count for UI

### Sorting
```
?sort_by=created_at     # Most recent first (default)
?sort_by=-created_at    # Oldest first
?sort_by=tasks_count    # Most tasks first
?sort_by=-tasks_count   # Least tasks first
?sort_by=name           # Z-A
?sort_by=-name          # A-Z
```

---

## 📊 Response Schemas

### ProjectResponse (List, Create, Update)
```json
{
  "id": int,
  "name": string,
  "description": string?,
  "user_id": int,
  "status": "active" | "deleted" | "archived",
  "tasks_count": int,
  "created_at": datetime,
  "updated_at": datetime
}
```

### ProjectDetailResponse (Get by ID)
```json
{
  ...ProjectResponse,
  "tasks": [
    {
      "id": int,
      "title": string,
      "status": string,
      "priority": string,
      "created_at": datetime,
      "updated_at": datetime
    }
  ]
}
```

### ProjectListResponse
```json
{
  "total": int,
  "limit": int,
  "offset": int,
  "projects": [ProjectResponse]
}
```

---

## ⚠️ Error Codes

| Code | Description |
|------|-------------|
| 200 | Success (GET, PUT) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (no fields to update) |
| 403 | Forbidden (BOLA violation) |
| 404 | Not Found (project doesn't exist) |
| 422 | Validation Error (invalid input) |
| 500 | Internal Server Error |

---

## 🧪 Testing

```bash
cd backend
pytest app/tests/test_projects.py -v
```

**Coverage**: 40+ tests
- CRUD operations
- Validation
- Search, pagination, sorting
- BOLA protection
- Soft delete cascade

---

## 📚 Full Documentation

- **API Docs**: `docs/API_PROJECTS.md`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Completion Summary**: `docs/P2_T6_COMPLETION_SUMMARY.md`

---

## 🔗 Files Reference

```
backend/
├── app/
│   ├── routers/
│   │   └── projects.py           # 5 CRUD endpoints
│   ├── schemas/
│   │   └── project_schemas.py    # 9 Pydantic models
│   └── tests/
│       └── test_projects.py      # 40+ tests
└── docs/
    ├── API_PROJECTS.md           # Full API documentation
    ├── P2_T6_COMPLETION_SUMMARY.md
    └── QUICK_REFERENCE_PROJECTS.md (this file)
```

---

**Last Updated**: 2025-01-08
**Status**: ✅ Production Ready
