# API Examples

This directory contains realistic request/response examples for the RUV SPARC API.

## 📋 Available Examples

### Tasks API

- **`tasks-create.json`** - Create a scheduled task with cron expression
  - Example: Pair programming task running weekdays at 9 AM
  - Shows: Cron validation, parameter structure, response format

- **`tasks-list.json`** - List tasks with filtering and pagination
  - Example: Filter by status, sort by created_at
  - Shows: Pagination, filtering, sorting parameters

### Projects API

- **`projects-create.json`** - Create a new project
  - Example: Backend refactoring project
  - Shows: Name/description validation, response structure

### Agents API

- **`agents-activity.json`** - Log agent activity
  - Example: Agent executing pair programming task
  - Shows: Activity logging, Memory MCP storage, WebSocket broadcast

### Error Responses

- **`error-responses.json`** - Comprehensive error examples
  - 400 Bad Request (invalid cron)
  - 401 Unauthorized (missing token)
  - 403 Forbidden (BOLA protection)
  - 404 Not Found (resource missing)
  - 422 Validation Error (Pydantic)
  - 429 Rate Limit Exceeded
  - 500 Internal Server Error

## 🚀 Usage with curl

### Create Task

```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d @tasks-create.json
```

### List Tasks

```bash
curl -X GET "http://localhost:8000/api/v1/tasks?status=pending&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Create Project

```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d @projects-create.json
```

### Log Agent Activity

```bash
curl -X POST http://localhost:8000/api/v1/agents/activity \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d @agents-activity.json
```

## 🧪 Testing with Swagger UI

1. Start the server:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

2. Open Swagger UI: http://localhost:8000/api/docs

3. Click **Authorize** button and paste your JWT token

4. Try any endpoint:
   - Click **Try it out**
   - Paste example JSON from these files
   - Click **Execute**

## 📚 Related Documentation

- **API Docs**: `docs/API_DOCS.md` - Complete API reference
- **OpenAPI Customization**: `docs/OPENAPI_CUSTOMIZATION.md` - How docs are generated
- **Static HTML**: `docs/api-static/` - Offline documentation

## 🔑 JWT Token Format

Example JWT payload:

```json
{
  "sub": "user_12345",
  "exp": 1699999999,
  "iat": 1699900000
}
```

Generate test token (Python):

```python
import jwt
from datetime import datetime, timedelta

payload = {
    "sub": "user_12345",
    "exp": datetime.utcnow() + timedelta(hours=24),
    "iat": datetime.utcnow()
}

token = jwt.encode(payload, "your-secret-key", algorithm="HS256")
print(f"Bearer {token}")
```

## 💡 Tips

- **Validation**: All examples include valid data that passes Pydantic validation
- **Realistic**: Examples use realistic values (not "string", "0", etc.)
- **Complete**: All required fields included, optional fields shown
- **Headers**: Response headers demonstrate rate limiting, request tracing

## 🐛 Common Issues

### 401 Unauthorized
- **Cause**: Missing or invalid JWT token
- **Fix**: Include `Authorization: Bearer <token>` header

### 400 Bad Request (Invalid cron)
- **Cause**: Malformed cron expression
- **Fix**: Use valid format: `minute hour day month weekday`
  - Example: `0 9 * * 1-5` (weekdays at 9 AM)

### 403 Forbidden (BOLA)
- **Cause**: Trying to access another user's resource
- **Fix**: Ensure task/project belongs to authenticated user

### 422 Validation Error
- **Cause**: Pydantic schema validation failed
- **Fix**: Check field types, lengths, required fields

---

**Last Updated**: 2025-11-08
