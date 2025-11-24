# API Documentation

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

FastAPI auto-generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Health Check

#### GET /health
Check API and database health

**Response** (200 OK):
```json
{
  "status": "healthy",
  "database": "connected",
  "api": "operational"
}
```

---

### Agents

#### GET /api/v1/agents/
List all agents

**Query Parameters**:
- `skip` (int): Offset for pagination (default: 0)
- `limit` (int): Max results (default: 100, max: 500)
- `role` (string): Filter by role

**Response** (200 OK):
```json
[
  {
    "agent_id": "uuid",
    "name": "coder-001",
    "role": "developer",
    "capabilities": ["coding", "testing"],
    "rbac": {
      "allowed_tools": ["Read", "Write"],
      "path_scopes": ["src/**"],
      "api_access": ["github"]
    },
    "budget": {
      "max_tokens_per_session": 100000,
      "max_cost_per_day": 30.0
    },
    "metadata": {
      "category": "delivery",
      "specialist": true,
      "tags": ["development"]
    },
    "performance": {
      "tasks_completed": 42,
      "success_rate": 0.95,
      "avg_execution_time": 1.2
    },
    "timestamps": {
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-15T12:00:00Z"
    }
  }
]
```

---

#### GET /api/v1/registry/agents
Alias for /api/v1/agents/ (frontend compatibility)

---

### Events

#### GET /api/v1/events/
List audit events

**Query Parameters**:
- `skip` (int): Offset (default: 0)
- `limit` (int): Max results (default: 100)

**Response** (200 OK):
```json
[
  {
    "audit_id": "uuid",
    "agent": "coder-001",
    "operation": "Read",
    "target": "src/app.js",
    "rbac": {"allowed": true},
    "cost": {"tokens": 500, "usd": 0.015},
    "context": {},
    "timestamp": "2025-01-15T12:00:00Z"
  }
]
```

---

#### POST /api/v1/events/ingest
Ingest new audit event

**Request Body**:
```json
{
  "agent": "coder-001",
  "operation": "Write",
  "target": "src/feature.js",
  "rbac": {"allowed": true, "role": "developer"},
  "cost": {"tokens": 1000, "usd": 0.03},
  "context": {"task_id": "TASK-123"}
}
```

**Response** (201 Created):
```json
{
  "audit_id": "uuid",
  "agent": "coder-001",
  ...
}
```

---

### Activity Feed

#### GET /api/v1/agent-activity
Get agent activity feed

**Response** (200 OK):
```json
[
  {
    "activity_id": "uuid",
    "agent": "coder-001",
    "action": "completed_task",
    "details": {},
    "timestamp": "2025-01-15T12:00:00Z"
  }
]
```

---

### WebSocket

#### WS /ws
Real-time event stream

**Connection**:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Event:', data);
};
```

**Message Format**:
```json
{
  "type": "connection|event|echo",
  "data": {...},
  "timestamp": "2025-01-15T12:00:00Z"
}
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Not Found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "detail": "Error message",
  "path": "/api/v1/endpoint"
}
```

---

## Rate Limits

- No rate limits in development
- Production: 1000 requests/minute per IP

## Authentication

- Development: No authentication required
- Production: JWT tokens (coming soon)

## CORS

Allowed origins:
- http://localhost:3000 (Next.js dev)
- http://localhost:5173 (Vite dev)
