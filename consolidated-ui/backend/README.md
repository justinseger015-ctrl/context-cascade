# RUV SPARC UI Dashboard - FastAPI Backend

Production-ready FastAPI backend with security, performance, and monitoring built-in.

## 🚀 Features

### Security
- ✅ **CVE-2024-47874 Mitigation**: FastAPI 0.121.0+
- ✅ **OWASP API1:2023 Protection**: Broken Object Level Authorization checks
- ✅ **JWT Authentication**: Secure token-based authentication
- ✅ **Rate Limiting**: slowapi with 100 req/min per IP
- ✅ **CORS Middleware**: Configured for localhost:3000 (dev)
- ✅ **Security Headers**: XSS, CSRF, Content-Type protection

### Performance
- ✅ **Multi-worker**: Gunicorn + Uvicorn (2*CPU+1 workers)
- ✅ **Async Database**: AsyncPG + SQLAlchemy 2.0
- ✅ **Connection Pooling**: Optimized for production
- ✅ **GZip Compression**: Automatic response compression

### Monitoring
- ✅ **Health Checks**: Database + Memory MCP status
- ✅ **Kubernetes Probes**: Readiness/Liveness endpoints
- ✅ **Request Tracing**: Unique request IDs
- ✅ **Structured Logging**: Production-ready logs

## 📋 API Endpoints

### Health & Monitoring
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health with metrics
- `GET /api/v1/readiness` - Kubernetes readiness probe
- `GET /api/v1/liveness` - Kubernetes liveness probe

### Tasks
- `GET /api/v1/tasks` - List all tasks (with BOLA protection)
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{task_id}` - Get task by ID
- `PUT /api/v1/tasks/{task_id}` - Update task
- `DELETE /api/v1/tasks/{task_id}` - Delete task

### Projects
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create new project
- `GET /api/v1/projects/{project_id}` - Get project by ID
- `PUT /api/v1/projects/{project_id}` - Update project
- `DELETE /api/v1/projects/{project_id}` - Delete project

### Agents
- `GET /api/v1/agents` - List all agents
- `POST /api/v1/agents` - Create new agent
- `GET /api/v1/agents/{agent_id}` - Get agent by ID
- `PUT /api/v1/agents/{agent_id}` - Update agent
- `DELETE /api/v1/agents/{agent_id}` - Delete agent

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Setup

1. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Initialize database**:
```bash
# Database schema from P1_T2 should already be created
# Run migrations if needed
alembic upgrade head
```

## 🚀 Running the Server

### Development (with auto-reload)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production (multi-worker)
```bash
gunicorn app.main:app -c gunicorn_config.py
```

### Docker (from Phase 1)
```bash
cd ..
docker-compose up backend
```

## 📊 Health Check Example

```bash
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-08T22:45:00.000Z",
  "database": "connected",
  "memory_mcp": "available",
  "version": "1.0.0"
}
```

## 🔒 Security Features

### JWT Authentication
All protected endpoints require JWT token in Authorization header:

```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/tasks
```

### BOLA Protection
Each endpoint verifies resource ownership:
```python
# Automatic check in all endpoints
verify_resource_ownership(user.id, resource.user_id)
```

### Rate Limiting
- Default: 100 requests/minute per IP
- Configurable via `RATE_LIMIT_PER_MINUTE`
- Returns `429 Too Many Requests` when exceeded

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database connection
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Pydantic settings
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py             # JWT authentication
│   └── routers/
│       ├── __init__.py
│       ├── health.py           # Health checks
│       ├── tasks.py            # Task endpoints
│       ├── projects.py         # Project endpoints
│       └── agents.py           # Agent endpoints
├── gunicorn_config.py          # Gunicorn configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### API Documentation
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI JSON: http://localhost:8000/api/openapi.json

**Note**: API docs disabled in production for security

## 🔧 Configuration

### Environment Variables

All settings in `app/config/settings.py` can be overridden via environment variables:

```bash
# Example: Change worker count
WORKERS=17

# Example: Change database URL
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/mydb

# Example: Add CORS origin
CORS_ORIGINS='["http://localhost:3000","https://app.example.com"]'
```

### Gunicorn Workers

Default formula: `2 * CPU_COUNT + 1`

For 12-core system: `2 * 12 + 1 = 25 workers`

Adjust in `.env`:
```bash
WORKERS=25
```

## 📝 Next Steps

1. **P2_T2**: Connect to PostgreSQL database with SQLAlchemy models
2. **P2_T3**: Implement JWT authentication endpoints
3. **P2_T4**: Add business logic and validation
4. **P2_T5**: Integration testing

## 🐛 Known Issues

- Task/Project/Agent endpoints return 501 (not implemented) - requires database models from P2_T2
- Memory MCP health check requires Memory MCP server running

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
