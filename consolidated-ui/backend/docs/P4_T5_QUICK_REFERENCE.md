# P4_T5 - API Documentation Quick Reference

**Status**: ✅ COMPLETE | **Date**: 2025-11-08

---

## 📚 Documentation Files

| File | Purpose | Location |
|------|---------|----------|
| **Swagger UI** | Interactive API explorer | http://localhost:8000/api/docs |
| **ReDoc** | Alternative docs | http://localhost:8000/api/redoc |
| **OpenAPI JSON** | Raw schema | http://localhost:8000/api/openapi.json |
| **API Reference** | Complete guide | `docs/API_DOCS.md` |
| **Customization Guide** | How to maintain | `docs/OPENAPI_CUSTOMIZATION.md` |
| **Usage Examples** | Request/response | `docs/api-examples/*.json` |
| **Export Script** | Static HTML | `scripts/export_openapi_html.py` |

---

## 🚀 Quick Start

### Start Server
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Access Swagger UI
1. Navigate to http://localhost:8000/api/docs
2. Click **Authorize** button
3. Enter: `Bearer <your-jwt-token>`
4. Click **Authorize**
5. Try any endpoint with "Try it out"

### Export Static HTML
```bash
cd backend
python scripts/export_openapi_html.py
# Output: docs/api-static/swagger-ui.html, redoc.html, openapi.json
```

---

## 📋 Endpoints (15 Total)

### Health Check (1)
- `GET /api/v1/health` - System status

### Tasks API (5)
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks` - List tasks (filter, paginate, sort)
- `GET /api/v1/tasks/{id}` - Get task + execution history
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Soft delete task

### Projects API (5)
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects (search, paginate, sort)
- `GET /api/v1/projects/{id}` - Get project + nested tasks
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Soft delete project + cascade tasks

### Agents API (4)
- `GET /api/v1/agents` - List agents (filter by type, status, capabilities)
- `GET /api/v1/agents/{id}` - Get agent + execution history + metrics
- `POST /api/v1/agents/activity` - Log activity (PostgreSQL + Memory MCP + WebSocket)
- `POST /api/v1/agents` - Register new agent

---

## 🔐 Authentication

**Format**: `Authorization: Bearer <jwt-token>`

**Swagger UI**:
1. Click "Authorize" button (lock icon)
2. Enter: `Bearer <token>`
3. Click "Authorize"

**curl**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/v1/tasks
```

---

## ⏱️ Rate Limits

| Endpoint Type | Limit | Headers |
|--------------|-------|---------|
| Standard API | 100/min | `X-RateLimit-Limit: 100` |
| Activity Logging | 1000/min | `X-RateLimit-Remaining: 999` |
| Agent Creation | 60/min | `X-RateLimit-Reset: 1699999999` |

---

## ❌ Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| **400** | Bad Request | Invalid cron expression |
| **401** | Unauthorized | Missing JWT token |
| **403** | Forbidden | BOLA protection (not your resource) |
| **404** | Not Found | Resource doesn't exist |
| **422** | Validation Error | Pydantic schema failed |
| **429** | Rate Limit | Exceeded 100/min |
| **500** | Server Error | Unexpected error (has `X-Request-ID`) |

---

## 📦 Usage Examples

### Create Task
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "pair-programming",
    "schedule_cron": "0 9 * * 1-5",
    "params": {"mode": "driver"}
  }'
```

### List Tasks (Filtered)
```bash
curl "http://localhost:8000/api/v1/tasks?status=pending&limit=10" \
  -H "Authorization: Bearer TOKEN"
```

### Create Project
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Backend Refactoring",
    "description": "Modernize API endpoints"
  }'
```

### Log Agent Activity
```bash
curl -X POST http://localhost:8000/api/v1/agents/activity \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": 1,
    "task_id": 123,
    "status": "running",
    "output": "Processing task..."
  }'
```

---

## 🎨 Swagger UI Features

- **Theme**: Monokai syntax highlighting
- **Layout**: Models expanded (depth 3)
- **Display**: Request duration shown
- **Filter**: Search endpoints
- **Authorization**: Persistent (JWT stored in browser)

---

## 📄 File Locations

```
backend/
├── app/
│   ├── main.py                     # Enhanced OpenAPI metadata
│   ├── schemas/
│   │   ├── task_schemas.py         # Task models + examples
│   │   ├── project_schemas.py      # Project models + examples
│   │   └── agent_schemas.py        # Agent models + examples
│   └── routers/
│       ├── tasks.py                # Task endpoints + docs
│       ├── projects.py             # Project endpoints + docs
│       └── agents.py               # Agent endpoints + docs
├── docs/
│   ├── API_DOCS.md                 # Complete API reference
│   ├── OPENAPI_CUSTOMIZATION.md    # Maintenance guide
│   ├── P4_T5_API_DOCUMENTATION_COMPLETE.md  # Completion report
│   ├── api-examples/
│   │   ├── tasks-create.json       # Task creation example
│   │   ├── tasks-list.json         # Task listing example
│   │   ├── projects-create.json    # Project creation example
│   │   ├── agents-activity.json    # Activity logging example
│   │   ├── error-responses.json    # All error codes
│   │   └── README.md               # Usage guide
│   └── api-static/                 # Generated by export script
│       ├── openapi.json            # Raw OpenAPI schema
│       ├── swagger-ui.html         # Interactive docs (offline)
│       └── redoc.html              # Alternative docs (offline)
└── scripts/
    └── export_openapi_html.py      # Static HTML generator
```

---

## 🔧 Maintenance

### Update Endpoint Documentation
1. Edit docstring in `app/routers/*.py`
2. Update `description`, `summary`, `responses`
3. Restart server
4. Verify in Swagger UI

### Add New Example
1. Create JSON file in `docs/api-examples/`
2. Include request + response
3. Add to `api-examples/README.md`

### Update OpenAPI Metadata
1. Edit `app/main.py` FastAPI initialization
2. Modify `description`, `contact`, `license_info`, `openapi_tags`
3. Restart server

### Export Updated HTML
```bash
python scripts/export_openapi_html.py
```

---

## 📊 Coverage

- **Endpoints**: 15/15 (100%)
- **Error Codes**: 7/7 (100%)
- **Pydantic Models**: 12 schemas with examples
- **Usage Examples**: 6 JSON files
- **Documentation Files**: 10 files

---

## 🔗 Links

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json
- **FastAPI Docs**: https://fastapi.tiangolo.com/tutorial/metadata/
- **OpenAPI Spec**: https://spec.openapis.org/oas/v3.1.0

---

**Status**: ✅ Production Ready | **Version**: 1.0.0
