# API Documentation Index

**RUV SPARC UI Dashboard API**
**Version**: 1.0.0
**Last Updated**: 2025-11-08

---

## 🎯 Quick Links

| Resource | URL | Description |
|----------|-----|-------------|
| **Swagger UI** | http://localhost:8000/api/docs | Interactive API explorer |
| **ReDoc** | http://localhost:8000/api/redoc | Alternative documentation |
| **OpenAPI Schema** | http://localhost:8000/api/openapi.json | Machine-readable spec |

---

## 📚 Documentation Files

### Primary Documentation

1. **[API_DOCS.md](./API_DOCS.md)** - Complete API Reference
   - Overview and features
   - Authentication (JWT Bearer)
   - Rate limiting
   - Error handling
   - All 15 endpoints documented
   - Request/response examples
   - Security best practices

2. **[P4_T5_QUICK_REFERENCE.md](./P4_T5_QUICK_REFERENCE.md)** - Quick Start Guide
   - Start server
   - Access Swagger UI
   - Export static HTML
   - Endpoint summary
   - Authentication
   - Rate limits
   - Error codes
   - curl examples

3. **[OPENAPI_CUSTOMIZATION.md](./OPENAPI_CUSTOMIZATION.md)** - Developer Guide
   - FastAPI configuration
   - Pydantic schema customization
   - Endpoint documentation patterns
   - Authentication setup
   - Swagger UI theming
   - Static HTML export

---

### Completion Reports

1. **[P4_T5_API_DOCUMENTATION_COMPLETE.md](./P4_T5_API_DOCUMENTATION_COMPLETE.md)**
   - Task completion summary
   - All deliverables listed
   - Testing instructions
   - Metrics and coverage
   - Dependencies met
   - Next steps

2. **[DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md)**
   - Deliverables overview
   - Key features
   - Implementation details
   - Verification checklist
   - Resources

---

### Usage Examples

**Location**: `docs/api-examples/`

1. **[tasks-create.json](./api-examples/tasks-create.json)**
   - Create scheduled task
   - Cron expression examples
   - Parameter structure
   - Response format

2. **[tasks-list.json](./api-examples/tasks-list.json)**
   - List tasks with filtering
   - Pagination example
   - Sorting parameters
   - Query parameters

3. **[projects-create.json](./api-examples/projects-create.json)**
   - Create new project
   - Validation rules
   - Field examples

4. **[agents-activity.json](./api-examples/agents-activity.json)**
   - Log agent activity
   - Activity statuses
   - Integration details (PostgreSQL, Memory MCP, WebSocket)

5. **[error-responses.json](./api-examples/error-responses.json)**
   - All error codes (400-500)
   - Example error responses
   - Cause and fix for each

6. **[README.md](./api-examples/README.md)**
   - curl examples
   - Swagger UI walkthrough
   - JWT token generation
   - Common issues and fixes

---

### Scripts

1. **[export_openapi_html.py](../scripts/export_openapi_html.py)**
   - Export OpenAPI schema to static HTML
   - Generates: `openapi.json`, `swagger-ui.html`, `redoc.html`
   - Output: `docs/api-static/`

---

## 🚀 Getting Started

### 1. Start Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 2. Access Swagger UI

1. Navigate to http://localhost:8000/api/docs
2. Click **Authorize** button
3. Enter JWT token: `Bearer <your-token>`
4. Click **Authorize**

### 3. Try API Calls

1. Navigate to any endpoint
2. Click **Try it out**
3. Paste example JSON from `docs/api-examples/`
4. Click **Execute**
5. View response

### 4. Export Static HTML (Optional)

```bash
cd backend
python scripts/export_openapi_html.py
```

Output: `docs/api-static/swagger-ui.html`, `redoc.html`, `openapi.json`

---

## 📋 Endpoint Summary

### Health Check (1)
- `GET /api/v1/health` - System status

### Tasks API (5)
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks` - List tasks
- `GET /api/v1/tasks/{id}` - Get task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

### Projects API (5)
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Agents API (4)
- `GET /api/v1/agents` - List agents
- `GET /api/v1/agents/{id}` - Get agent
- `POST /api/v1/agents/activity` - Log activity
- `POST /api/v1/agents` - Register agent

**Total**: 15 endpoints

---

## 🔐 Authentication

All endpoints (except `/api/v1/health` and docs) require JWT authentication.

**Header Format**:
```
Authorization: Bearer <jwt-token>
```

**Swagger UI**:
1. Click "Authorize" button
2. Enter: `Bearer <token>`
3. Click "Authorize"

---

## ⏱️ Rate Limits

| Endpoint Type | Limit | Period |
|--------------|-------|--------|
| Standard API | 100 req | 1 min |
| Activity Logging | 1000 req | 1 min |
| Agent Creation | 60 req | 1 min |

**Headers**:
- `X-RateLimit-Limit`: Maximum allowed
- `X-RateLimit-Remaining`: Requests left
- `X-RateLimit-Reset`: Reset timestamp

---

## ❌ Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| **400** | Bad Request | Invalid cron expression |
| **401** | Unauthorized | Missing JWT token |
| **403** | Forbidden | BOLA protection |
| **404** | Not Found | Resource not found |
| **422** | Validation Error | Pydantic schema failed |
| **429** | Rate Limit | Exceeded limit |
| **500** | Server Error | Unexpected error |

See [error-responses.json](./api-examples/error-responses.json) for examples.

---

## 📦 Technology Stack

- **Framework**: FastAPI 0.121.0+
- **OpenAPI**: 3.1.0
- **Swagger UI**: 5.x
- **ReDoc**: Latest
- **Validation**: Pydantic 2.x

---

## 🔗 External Resources

- **FastAPI OpenAPI**: https://fastapi.tiangolo.com/tutorial/metadata/
- **Pydantic JSON Schema**: https://docs.pydantic.dev/latest/usage/json_schema/
- **OpenAPI Specification**: https://spec.openapis.org/oas/v3.1.0
- **Swagger UI**: https://swagger.io/tools/swagger-ui/
- **ReDoc**: https://redocly.com/redoc/

---

## 📊 Documentation Coverage

- **Endpoints**: 15/15 (100%)
- **Error Codes**: 7/7 (100%)
- **Pydantic Models**: 12 schemas with examples
- **Usage Examples**: 6 JSON files
- **Documentation Files**: 10+ files

---

## 📞 Support

- **GitHub Issues**: https://github.com/ruvnet/ruv-sparc-ui-dashboard/issues
- **Email**: support@ruv-sparc.io

---

**Version**: 1.0.0
**Status**: ✅ Production Ready
**Last Updated**: 2025-11-08
