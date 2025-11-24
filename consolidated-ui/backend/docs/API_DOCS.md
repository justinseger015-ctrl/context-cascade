# RUV SPARC UI Dashboard API Documentation

**Version**: 1.0.0
**Base URL**: `http://localhost:8000` (development)
**Interactive Docs**: http://localhost:8000/api/docs
**ReDoc**: http://localhost:8000/api/redoc

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Rate Limiting](#rate-limiting)
4. [Error Handling](#error-handling)
5. [Endpoints](#endpoints)
   - [Health Check](#health-check)
   - [Tasks API](#tasks-api)
   - [Projects API](#projects-api)
   - [Agents API](#agents-api)
6. [Request Examples](#request-examples)
7. [Response Examples](#response-examples)
8. [Security Best Practices](#security-best-practices)

---

## 🚀 Overview

The RUV SPARC UI Dashboard API is a production-ready FastAPI backend providing:

- **Task Scheduling**: Automated skill/agent execution with cron expressions
- **Project Management**: Organize tasks with search, pagination, sorting
- **Agent Registry**: Track agent performance, execution history, metrics
- **Real-time Updates**: WebSocket support for live agent activity
- **Security**: JWT auth, rate limiting, OWASP BOLA protection
- **Performance**: Connection pooling, GZip compression, indexed queries
- **Observability**: Structured logging, request tracing, Memory MCP

---

## 🔐 Authentication

All API endpoints (except `/api/v1/health` and documentation) require JWT authentication.

### How to Authenticate

Include JWT token in the `Authorization` header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Using Swagger UI

1. Navigate to http://localhost:8000/api/docs
2. Click the **Authorize** button (top-right, lock icon)
3. Enter your JWT token: `Bearer <your-token>`
4. Click **Authorize**
5. All subsequent requests will include the token

### Token Format

```json
{
  "sub": "user_12345",
  "exp": 1699999999,
  "iat": 1699900000
}
```

### Error Response (401 Unauthorized)

```json
{
  "detail": "Not authenticated"
}
```

---

## ⏱️ Rate Limiting

Rate limits prevent API abuse and ensure fair usage.

### Limits by Endpoint

| Endpoint Type | Limit | Window | Header |
|--------------|-------|--------|--------|
| Standard API | 100 requests | 1 minute | `X-RateLimit-Limit: 100` |
| Activity Logging (`/agents/activity`) | 1000 requests | 1 minute | `X-RateLimit-Limit: 1000` |
| Agent Creation | 60 requests | 1 minute | `X-RateLimit-Limit: 60` |

### Rate Limit Headers

Every response includes rate limit information:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699999999
```

### Error Response (429 Too Many Requests)

```json
{
  "detail": "Rate limit exceeded: 100 per 1 minute"
}
```

**Retry After**: Check the `Retry-After` header (in seconds).

---

## ❌ Error Handling

### Standard Error Response Format

```json
{
  "detail": "Error message describing what went wrong",
  "error_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| **200** | OK | Request succeeded |
| **201** | Created | Resource created successfully |
| **204** | No Content | Deletion succeeded (no response body) |
| **400** | Bad Request | Invalid input, malformed cron, validation error |
| **401** | Unauthorized | Missing or invalid JWT token |
| **403** | Forbidden | User does not own the resource (BOLA protection) |
| **404** | Not Found | Resource not found or soft deleted |
| **422** | Unprocessable Entity | Pydantic validation error |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Internal Server Error | Unexpected error (includes `error_id`) |

### Validation Error Example (422)

```json
{
  "detail": [
    {
      "loc": ["body", "schedule_cron"],
      "msg": "Invalid cron expression '0 0 0 * *': Invalid day-of-month value",
      "type": "value_error"
    }
  ]
}
```

---

## 📚 Endpoints

### Health Check

#### `GET /api/v1/health`

Check API health and database connectivity.

**Authentication**: Not required
**Rate Limit**: Not enforced

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-08T10:30:00Z",
  "database": "connected",
  "version": "1.0.0"
}
```

---

### Tasks API

Manage scheduled tasks for automated skill/agent execution.

#### `POST /api/v1/tasks`

Create a new scheduled task.

**Authentication**: Required
**Rate Limit**: 100/min

**Request Body**:
```json
{
  "skill_name": "pair-programming",
  "schedule_cron": "0 9 * * 1-5",
  "params": {
    "mode": "driver",
    "language": "python",
    "tdd_enabled": true
  },
  "status": "pending"
}
```

**Response (201)**:
```json
{
  "id": 123,
  "skill_name": "pair-programming",
  "schedule_cron": "0 9 * * 1-5",
  "next_run_at": "2025-11-09T09:00:00Z",
  "params": {
    "mode": "driver",
    "language": "python",
    "tdd_enabled": true
  },
  "status": "pending",
  "created_at": "2025-11-08T10:30:00Z",
  "updated_at": "2025-11-08T10:30:00Z",
  "user_id": "user_12345"
}
```

**Validation Rules**:
- `skill_name`: Alphanumeric, hyphens, underscores only
- `schedule_cron`: Valid cron expression (e.g., `0 0 * * *`)
- `params`: Optional JSON object

---

#### `GET /api/v1/tasks`

List scheduled tasks with filtering, pagination, sorting.

**Authentication**: Required
**Rate Limit**: 100/min

**Query Parameters**:
- `status` (optional): Filter by status (`pending`, `running`, `completed`, `failed`, `disabled`)
- `skill_name` (optional): Filter by exact skill name
- `limit` (default: 20, max: 100): Results per page
- `offset` (default: 0): Pagination offset
- `sort_by` (default: `created_at`): Sort field (`created_at`, `next_run_at`, `updated_at`)
- `sort_order` (default: `desc`): Sort direction (`asc`, `desc`)

**Example**:
```http
GET /api/v1/tasks?status=pending&limit=10&offset=0&sort_by=created_at&sort_order=desc
```

**Response (200)**:
```json
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
  "has_more": true
}
```

---

#### `GET /api/v1/tasks/{task_id}`

Get task by ID with execution history.

**Authentication**: Required
**Rate Limit**: 100/min
**BOLA Protection**: User must own the task

**Response (200)**:
```json
{
  "id": 123,
  "skill_name": "pair-programming",
  "schedule_cron": "0 9 * * 1-5",
  "next_run_at": "2025-11-09T09:00:00Z",
  "params": {"mode": "driver"},
  "status": "pending",
  "created_at": "2025-11-08T10:30:00Z",
  "updated_at": "2025-11-08T10:30:00Z",
  "user_id": "user_12345",
  "execution_results": [
    {
      "id": 456,
      "started_at": "2025-11-08T09:00:00Z",
      "ended_at": "2025-11-08T09:05:30Z",
      "status": "success",
      "duration_ms": 330000,
      "output_text": "Task completed successfully",
      "error_text": null
    }
  ]
}
```

---

#### `PUT /api/v1/tasks/{task_id}`

Update an existing task (partial updates supported).

**Authentication**: Required
**Rate Limit**: 100/min
**BOLA Protection**: User must own the task

**Request Body** (all fields optional):
```json
{
  "schedule_cron": "0 */2 * * *",
  "params": {"mode": "navigator"},
  "status": "pending"
}
```

**Response (200)**: Updated task object

---

#### `DELETE /api/v1/tasks/{task_id}`

Soft delete a task (marks as `deleted`, preserves history).

**Authentication**: Required
**Rate Limit**: 100/min
**BOLA Protection**: User must own the task

**Response (200)**:
```json
{
  "message": "Task successfully deleted",
  "task_id": 123,
  "status": "deleted"
}
```

---

### Projects API

Organize tasks into projects with search, pagination, and nested display.

#### `POST /api/v1/projects`

Create a new project.

**Authentication**: Required
**Rate Limit**: 100/min

**Request Body**:
```json
{
  "name": "My Awesome Project",
  "description": "A project to build an amazing application"
}
```

**Response (201)**:
```json
{
  "id": 1,
  "name": "My Awesome Project",
  "description": "A project to build an amazing application",
  "user_id": 123,
  "status": "active",
  "tasks_count": 0,
  "created_at": "2025-11-08T10:30:00Z",
  "updated_at": "2025-11-08T10:30:00Z"
}
```

---

#### `GET /api/v1/projects`

List projects with search, pagination, sorting.

**Authentication**: Required
**Rate Limit**: 100/min

**Query Parameters**:
- `search` (optional): Search name/description (case-insensitive)
- `limit` (default: 20, max: 100): Results per page
- `offset` (default: 0): Pagination offset
- `sort_by` (default: `-created_at`): Sort field (`created_at`, `-created_at`, `tasks_count`, `-tasks_count`, `name`, `-name`)

**Example**:
```http
GET /api/v1/projects?search=awesome&limit=10&offset=0&sort_by=-created_at
```

**Response (200)**:
```json
{
  "total": 100,
  "limit": 20,
  "offset": 0,
  "projects": [
    {
      "id": 1,
      "name": "My Awesome Project",
      "description": "Description",
      "user_id": 123,
      "status": "active",
      "tasks_count": 5,
      "created_at": "2025-11-08T10:30:00Z",
      "updated_at": "2025-11-08T10:30:00Z"
    }
  ]
}
```

---

#### `GET /api/v1/projects/{project_id}`

Get project details with nested tasks.

**Authentication**: Required
**Rate Limit**: 100/min
**BOLA Protection**: User must own the project

**Response (200)**:
```json
{
  "id": 1,
  "name": "My Awesome Project",
  "description": "Description",
  "user_id": 123,
  "status": "active",
  "tasks_count": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Task 1",
      "status": "pending",
      "priority": "high",
      "created_at": "2025-11-08T10:30:00Z",
      "updated_at": "2025-11-08T10:30:00Z"
    }
  ],
  "created_at": "2025-11-08T10:30:00Z",
  "updated_at": "2025-11-08T10:30:00Z"
}
```

---

#### `PUT /api/v1/projects/{project_id}`

Update a project (partial updates supported).

**Authentication**: Required
**Rate Limit**: 100/min
**BOLA Protection**: User must own the project

**Request Body**:
```json
{
  "name": "Updated Project Name",
  "description": "Updated description"
}
```

**Response (200)**: Updated project object

---

#### `DELETE /api/v1/projects/{project_id}`

Soft delete a project (cascades to all tasks).

**Authentication**: Required
**Rate Limit**: 100/min
**BOLA Protection**: User must own the project

**Response (204 No Content)**

**Note**: All tasks in the project are also soft deleted.

---

### Agents API

Track agent activity, performance metrics, and execution history.

#### `GET /api/v1/agents`

List agents with filtering and pagination.

**Authentication**: Required
**Rate Limit**: 100/min

**Query Parameters**:
- `type` (optional): Filter by agent type (`coder`, `reviewer`, `tester`, etc.)
- `status` (optional): Filter by status (`active`, `idle`, `busy`, `offline`, `error`)
- `capabilities` (optional): Filter by capabilities (comma-separated)
- `limit` (default: 100, max: 1000): Results per page
- `offset` (default: 0): Pagination offset

**Example**:
```http
GET /api/v1/agents?type=coder&status=active&limit=50&offset=0
```

**Response (200)**:
```json
{
  "agents": [
    {
      "id": 1,
      "name": "coder-agent-01",
      "type": "coder",
      "capabilities": ["python", "javascript", "testing"],
      "status": "active",
      "last_active_at": "2025-11-08T10:30:00Z"
    }
  ],
  "total": 42,
  "limit": 100,
  "offset": 0
}
```

---

#### `GET /api/v1/agents/{agent_id}`

Get agent by ID with execution history and metrics.

**Authentication**: Required
**Rate Limit**: 100/min

**Query Parameters**:
- `history_limit` (default: 50, max: 500): Max execution history items

**Response (200)**:
```json
{
  "id": 1,
  "name": "coder-agent-01",
  "type": "coder",
  "capabilities": ["python", "javascript"],
  "status": "active",
  "last_active_at": "2025-11-08T10:30:00Z",
  "execution_history": [
    {
      "task_id": 123,
      "started_at": "2025-11-08T09:00:00Z",
      "ended_at": "2025-11-08T09:05:30Z",
      "status": "success",
      "duration_ms": 330000,
      "output_text": "Task completed",
      "error_text": null
    }
  ],
  "success_rate": 0.95,
  "avg_duration_ms": 280000
}
```

---

#### `POST /api/v1/agents/activity`

Log agent activity (stores in PostgreSQL + Memory MCP, broadcasts via WebSocket).

**Authentication**: Required
**Rate Limit**: 1000/min (higher limit for activity logging)

**Request Body**:
```json
{
  "agent_id": 1,
  "task_id": 123,
  "status": "running",
  "output": "Processing task...",
  "error": null,
  "duration_ms": 5000
}
```

**Response (201)**:
```json
{
  "status": "success",
  "message": "Agent activity logged successfully",
  "agent_id": 1,
  "task_id": 123,
  "stored_in_memory_mcp": true,
  "broadcasted_via_websocket": true
}
```

---

#### `POST /api/v1/agents`

Register a new agent in the system.

**Authentication**: Required
**Rate Limit**: 60/min

**Request Body**:
```json
{
  "name": "coder-agent-02",
  "type": "coder",
  "capabilities": ["python", "rust"],
  "status": "idle"
}
```

**Response (201)**:
```json
{
  "id": 2,
  "name": "coder-agent-02",
  "type": "coder",
  "capabilities": ["python", "rust"],
  "status": "idle",
  "last_active_at": null
}
```

---

## 📦 Request Examples

See `docs/api-examples/` for complete request/response examples:

- `tasks-create.json` - Create task
- `tasks-list.json` - List tasks
- `tasks-update.json` - Update task
- `projects-create.json` - Create project
- `projects-search.json` - Search projects
- `agents-activity.json` - Log agent activity

---

## 🔒 Security Best Practices

1. **Never hardcode JWT tokens** - Use environment variables
2. **Rotate tokens regularly** - Implement token refresh
3. **Validate all inputs** - Pydantic handles this automatically
4. **Monitor rate limits** - Check `X-RateLimit-*` headers
5. **Handle errors gracefully** - Always check status codes
6. **Use HTTPS in production** - Never send tokens over HTTP
7. **Log security events** - Monitor 401/403 responses
8. **Implement CORS properly** - Configure allowed origins

---

## 🚀 Getting Started

1. **Start the server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

2. **Access Swagger UI**: http://localhost:8000/api/docs

3. **Get a JWT token** (implementation-specific)

4. **Authorize in Swagger**:
   - Click "Authorize" button
   - Enter: `Bearer <your-token>`

5. **Try API calls**:
   - Use "Try it out" buttons
   - Execute requests
   - View responses

---

## 📞 Support

- **GitHub Issues**: https://github.com/ruvnet/ruv-sparc-ui-dashboard/issues
- **Email**: support@ruv-sparc.io
- **Documentation**: https://docs.ruv-sparc.io

---

**Version**: 1.0.0
**Last Updated**: 2025-11-08
**License**: MIT
