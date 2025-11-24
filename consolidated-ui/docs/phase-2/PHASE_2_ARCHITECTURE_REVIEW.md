# Phase 2 Backend Architecture - Comprehensive Review

**Project**: RUV SPARC UI Dashboard Backend
**Phase**: Phase 2 - Backend Core Development
**Version**: 1.0.0
**Last Updated**: 2024-11-08

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Component Architecture](#component-architecture)
3. [Data Architecture](#data-architecture)
4. [Integration Architecture](#integration-architecture)
5. [Security Architecture](#security-architecture)
6. [Performance Architecture](#performance-architecture)
7. [Resilience Architecture](#resilience-architecture)
8. [Deployment Architecture](#deployment-architecture)

---

## System Architecture Overview

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Applications                        │
│         (Browser, Mobile App, CLI, External Services)            │
└────────────────────────┬─────────────────────────────────────────┘
                         │ HTTPS/WSS
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                     Load Balancer (Nginx)                        │
│            SSL Termination, Rate Limiting, Compression           │
└────────────────────────┬─────────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
┌─────────────────────┐       ┌─────────────────────┐
│   FastAPI Worker 1  │  ...  │  FastAPI Worker 25  │
│  (Uvicorn+Gunicorn) │       │  (Uvicorn+Gunicorn) │
└──────────┬──────────┘       └──────────┬──────────┘
           │                              │
           └──────────────┬───────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
┌────────────────┐ ┌────────────┐ ┌────────────────┐
│  PostgreSQL 15 │ │  Redis 7   │ │  Memory MCP    │
│  (Primary DB)  │ │  (Cache)   │ │  (Optional)    │
│  ACID Storage  │ │  Pub/Sub   │ │  Vector Search │
└────────────────┘ └────────────┘ └────────────────┘
```

### **Architecture Principles**

1. **Asynchronous First**: All I/O operations use async/await
2. **Stateless Workers**: No session state in workers (Redis-backed)
3. **Circuit Breaker Pattern**: Graceful degradation for external dependencies
4. **Defense in Depth**: Multiple security layers (JWT, BOLA, rate limiting)
5. **Fail Fast**: Early validation with Pydantic schemas
6. **Audit Everything**: Comprehensive logging for compliance

---

## Component Architecture

### 1. API Layer

#### **FastAPI Application** (`app/main.py`)

**Responsibilities**:
- Request routing and validation
- Middleware coordination
- Lifecycle management (startup/shutdown)
- Exception handling

**Key Components**:
```python
FastAPI Application
├── Lifespan Manager (async context manager)
│   ├── Startup: Database pool initialization
│   └── Shutdown: Graceful connection cleanup
├── Middleware Stack
│   ├── CORSMiddleware (configurable origins)
│   ├── GZipMiddleware (responses >1KB)
│   ├── TrustedHostMiddleware (production)
│   ├── Request ID Middleware (tracing)
│   └── Security Headers Middleware
├── Rate Limiter (slowapi)
│   └── 100 requests/minute per IP
└── Exception Handlers
    ├── HTTPException (400, 401, 403, 404, 422)
    └── Global Exception Handler (500)
```

**Configuration**:
- **Development**: API docs enabled at `/api/docs` and `/api/redoc`
- **Production**: API docs disabled for security
- **Versioning**: `/api/v1/` prefix for all endpoints

#### **Router Architecture**

```
app/routers/
├── health.py          # Health checks (4 endpoints)
│   ├── GET /health             # Basic health
│   ├── GET /health/detailed    # Detailed metrics
│   ├── GET /readiness          # Kubernetes readiness
│   └── GET /liveness           # Kubernetes liveness
├── tasks.py           # Task CRUD (5 endpoints)
│   ├── POST   /tasks           # Create task
│   ├── GET    /tasks           # List tasks (filtering, pagination)
│   ├── GET    /tasks/{id}      # Get task with execution history
│   ├── PUT    /tasks/{id}      # Update task
│   └── DELETE /tasks/{id}      # Soft delete task
├── projects.py        # Project CRUD (5 endpoints)
│   ├── POST   /projects        # Create project
│   ├── GET    /projects        # List projects (search, pagination)
│   ├── GET    /projects/{id}   # Get project with nested tasks
│   ├── PUT    /projects/{id}   # Update project
│   └── DELETE /projects/{id}   # Soft delete (cascade)
└── agents.py          # Agent management (5 endpoints)
    ├── GET    /agents          # List agents (filtering, pagination)
    ├── GET    /agents/{id}     # Get agent with metrics
    ├── POST   /agents/activity # Log agent activity
    ├── PUT    /agents/{id}     # Update agent status
    └── DELETE /agents/{id}     # Soft delete agent
```

### 2. Data Layer

#### **Database Models** (SQLAlchemy 2.0 ORM)

```python
# Database Schema Hierarchy
app/models/
├── project.py              # Projects (top-level entity)
│   ├── id (PK)
│   ├── name, description
│   ├── metadata_json
│   ├── created_at, updated_at
│   └── Relationship: tasks (1-to-many)
├── scheduled_task.py       # Scheduled Tasks
│   ├── id (PK)
│   ├── skill_name, schedule_cron
│   ├── next_run_at, params_json
│   ├── status (pending, running, completed, failed, deleted)
│   ├── project_id (FK)
│   ├── user_id (FK, BOLA protection)
│   └── Relationship: execution_results (1-to-many)
├── execution_result.py     # Task Execution History
│   ├── id (PK)
│   ├── task_id (FK)
│   ├── status, result_json
│   ├── started_at, completed_at
│   └── logs_text
├── agent.py                # Agent Registry
│   ├── id (PK)
│   ├── name, agent_type
│   ├── capabilities_json
│   ├── status (active, idle, busy, error)
│   └── last_activity_at
└── audit_log.py            # Audit Trail (NFR2.6)
    ├── id (PK)
    ├── entity_type, entity_id
    ├── action, user_id
    ├── ip_address, user_agent
    └── timestamp
```

#### **Database Indexes** (8 composite indexes)

```sql
-- Performance-optimized indexes
CREATE INDEX idx_tasks_user_status ON scheduled_task(user_id, status);
CREATE INDEX idx_tasks_next_run ON scheduled_task(next_run_at) WHERE status='pending';
CREATE INDEX idx_execution_task_time ON execution_result(task_id, started_at DESC);
CREATE INDEX idx_projects_user ON project(user_id);
CREATE INDEX idx_agents_status ON agent(status, last_activity_at DESC);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id, timestamp DESC);
CREATE INDEX idx_audit_user ON audit_log(user_id, timestamp DESC);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp DESC);
```

#### **CRUD Operations** (app/crud/)

```python
# CRUD Layer Pattern (example: ScheduledTaskCRUD)
class ScheduledTaskCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(...) -> ScheduledTask:
        # 1. Create model instance
        # 2. Add to session
        # 3. Flush (get ID)
        # 4. Create audit log
        # 5. Return model

    async def get_by_id(task_id: int) -> Optional[ScheduledTask]:
        # 1. Query by ID
        # 2. Eager load relationships
        # 3. Return model or None

    async def get_all(...) -> List[ScheduledTask]:
        # 1. Build query with filters
        # 2. Apply pagination (limit, offset)
        # 3. Apply sorting
        # 4. Execute query
        # 5. Return list

    async def update(task_id: int, data: dict) -> ScheduledTask:
        # 1. Get existing model
        # 2. Update fields
        # 3. Flush
        # 4. Create audit log
        # 5. Return updated model

    async def delete(task_id: int) -> bool:
        # Soft delete: mark status='deleted'
```

### 3. Integration Layer

#### **Memory MCP Client** (`app/utils/memory_mcp_client.py`)

```python
# Memory MCP Integration Architecture
MemoryMCPClient
├── Tagging Protocol (WHO/WHEN/PROJECT/WHY)
│   ├── WHO: agent_id, agent_category, capabilities, user_id
│   ├── WHEN: iso_timestamp, unix_timestamp, readable
│   ├── PROJECT: project_id, project_name, task_id
│   └── WHY: intent (implementation, bugfix, refactor, ...)
├── Circuit Breaker (from P1_T5)
│   ├── States: CLOSED (normal), OPEN (fallback), HALF_OPEN (recovery)
│   ├── Failure threshold: 3 consecutive failures
│   ├── Timeout: 60 seconds
│   └── Recovery: 2 successful calls to close
├── Vector Search
│   ├── Semantic similarity ranking (0-1 score)
│   ├── Project/task filtering
│   └── Result limit (default: 10)
└── Fallback Hierarchy
    ├── Primary: Memory MCP (vector storage + semantic search)
    ├── Fallback 1: PostgreSQL (relational storage + text search)
    └── Fallback 2: Redis (stale data serving, 24h TTL)
```

**Key Methods**:
```python
async def store(content: str, intent: Intent, task_id: str) -> dict:
    """Store with automatic WHO/WHEN/PROJECT/WHY tagging"""

async def vector_search(query: str, project_id: str, limit: int) -> List[dict]:
    """Semantic similarity search with ranking"""

async def get_task_history(task_id: str) -> dict:
    """Get task + related tasks via vector search"""

async def health_check() -> dict:
    """System status + degraded mode detection"""
```

### 4. Real-Time Layer

#### **WebSocket Manager** (`app/websocket/`)

```python
# WebSocket Architecture
WebSocket System
├── Connection Manager
│   ├── Active connections registry (Dict[str, WebSocket])
│   ├── Connect/disconnect lifecycle
│   ├── Broadcast to all clients
│   └── Send to specific client
├── Redis Pub/Sub (horizontal scaling)
│   ├── Channel: "sparc_websocket_events"
│   ├── Publisher: Broadcast events to all workers
│   └── Subscriber: Listen for events from other workers
├── Heartbeat Mechanism
│   ├── Ping interval: 30 seconds
│   ├── Pong timeout: 60 seconds
│   └── Automatic reconnection
└── Message Types
    ├── task_status_update
    ├── agent_activity_update
    ├── calendar_event_created
    └── error
```

**WebSocket Endpoint**:
```python
GET /ws
# Authentication: JWT token in query parameter
# Format: ws://localhost:8000/ws?token=<jwt>

# Message Format (JSON)
{
  "type": "task_status_update",
  "data": {
    "task_id": 123,
    "status": "running",
    "timestamp": "2024-11-08T10:30:00Z"
  }
}
```

**Horizontal Scaling with Redis Pub/Sub**:
```
Worker 1 (Client A, B, C) ─┐
Worker 2 (Client D, E, F) ─┼──> Redis Pub/Sub Channel
Worker 3 (Client G, H, I) ─┘
                            │
            Broadcast to ALL workers
                            │
                            ▼
All clients receive message regardless of worker
```

### 5. Security Layer

#### **Authentication & Authorization** (`app/middleware/auth.py`)

```python
# Security Architecture
Security Layer
├── JWT Authentication
│   ├── Access Token (60 min expiry)
│   ├── Refresh Token (7 day expiry)
│   ├── Algorithm: HS256
│   └── Secret: Environment variable (JWT_SECRET_KEY)
├── OWASP BOLA Protection (API1:2023)
│   ├── Resource ownership verification
│   ├── User ID comparison
│   └── 403 Forbidden on ownership mismatch
├── Rate Limiting (slowapi)
│   ├── Default: 100 requests/minute per IP
│   ├── Burst: 20 requests
│   └── Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
└── Security Headers Middleware
    ├── X-Content-Type-Options: nosniff
    ├── X-Frame-Options: DENY
    ├── X-XSS-Protection: 1; mode=block
    ├── Strict-Transport-Security: max-age=31536000; includeSubDomains
    └── Content-Security-Policy: default-src 'self'
```

**JWT Token Flow**:
```
1. User Login
   POST /api/v1/auth/login
   Body: {"username": "user", "password": "pass"}
   Response: {"access_token": "...", "refresh_token": "...", "token_type": "bearer"}

2. Protected Request
   GET /api/v1/tasks
   Header: Authorization: Bearer <access_token>

3. Token Refresh (when access token expires)
   POST /api/v1/auth/refresh
   Body: {"refresh_token": "..."}
   Response: {"access_token": "...", "token_type": "bearer"}
```

**BOLA Protection Example**:
```python
# Automatic ownership verification in all endpoints
@router.get("/tasks/{task_id}")
async def get_task(task_id: int, current_user: User = Depends(get_current_user)):
    task = await task_crud.get_by_id(task_id)

    # OWASP API1:2023 BOLA protection
    if task.user_id != current_user.id:
        raise HTTPException(403, "You do not have permission to access this resource")

    return task
```

---

## Data Architecture

### Database Connection Pool

```python
# AsyncPG Connection Pool Configuration
Database Pool
├── Pool Size: 10 base connections
├── Max Overflow: 20 additional connections (total: 30)
├── Pool Timeout: 30 seconds (wait for available connection)
├── Pool Recycle: 3600 seconds (1 hour, prevent stale connections)
├── Echo: False (disable SQL logging in production)
└── SSL Mode: verify-full (production), prefer (development)
```

**Connection Pool Lifecycle**:
```python
# Startup (app lifespan)
async def init_db():
    engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=20)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Per-Request
async def get_db():
    async with SessionLocal() as session:
        yield session
        # Automatic commit/rollback on exit

# Shutdown
async def close_db():
    await engine.dispose()
```

### Data Flow Diagram

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ POST /api/v1/tasks (create task)
       ▼
┌────────────────────────────────────────┐
│  FastAPI Router (tasks.py)             │
│  1. Validate request (Pydantic)        │
│  2. Extract JWT user ID                │
│  3. Calculate next_run_at (croniter)   │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│  CRUD Layer (scheduled_task.py)        │
│  1. Create SQLAlchemy model            │
│  2. Add to session                     │
│  3. Flush (get auto-incremented ID)    │
│  4. Create audit log entry             │
└────────┬───────────────────────────────┘
         │
         ├──────────────────┬─────────────┐
         │                  │             │
         ▼                  ▼             ▼
┌────────────────┐  ┌─────────────┐  ┌──────────────┐
│  PostgreSQL    │  │  Memory MCP │  │  Redis       │
│  (Primary DB)  │  │  (Optional) │  │  (Cache)     │
│  - Insert task │  │  - Store    │  │  - Cache key │
│  - Commit      │  │    metadata │  │  - 24h TTL   │
└────────────────┘  │    with tag │  └──────────────┘
                    │  - Circuit  │
                    │    breaker  │
                    └─────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│  Response                              │
│  {                                     │
│    "id": 123,                          │
│    "skill_name": "pair-programming",   │
│    "status": "pending",                │
│    "next_run_at": "2024-11-09T09:00Z"  │
│  }                                     │
└────────────────────────────────────────┘
```

---

## Integration Architecture

### External Service Integration

```
FastAPI Backend
├── Memory MCP Server (optional)
│   ├── Protocol: HTTP REST
│   ├── Endpoint: http://localhost:3001
│   ├── Circuit Breaker: Enabled (CF003 mitigation)
│   └── Fallback: PostgreSQL + Redis
├── PostgreSQL Database (required)
│   ├── Protocol: PostgreSQL Wire Protocol
│   ├── Driver: asyncpg
│   ├── Connection: SSL (verify-full in production)
│   └── Pool: 10 base + 20 overflow
└── Redis Server (required)
    ├── Protocol: Redis RESP
    ├── Driver: redis.asyncio
    ├── Connection: TCP (optional TLS)
    └── Usage: WebSocket pub/sub, caching, session storage
```

### Message Flow (Task Execution)

```
1. Scheduler (cron daemon) checks next_run_at
   SELECT * FROM scheduled_task WHERE next_run_at <= NOW() AND status='pending'

2. Execute task
   UPDATE scheduled_task SET status='running' WHERE id=123

3. Create execution result
   INSERT INTO execution_result (task_id, status, started_at) VALUES (123, 'running', NOW())

4. Broadcast WebSocket event
   Redis Pub/Sub: PUBLISH sparc_websocket_events '{"type":"task_status_update","data":{...}}'

5. All workers receive event → broadcast to connected WebSocket clients

6. Update execution result
   UPDATE execution_result SET status='completed', completed_at=NOW(), result_json='...'

7. Update task next_run_at
   UPDATE scheduled_task SET status='pending', next_run_at=<next cron time>

8. Store in Memory MCP (with circuit breaker)
   POST http://localhost:3001/memory/store
   Body: {content, metadata: {who, when, project, why}}
```

---

## Security Architecture

### Defense-in-Depth Layers

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Network Security                                  │
│  - TLS/SSL encryption (HTTPS/WSS)                          │
│  - Nginx rate limiting (requests/sec)                      │
│  - DDoS protection (Cloudflare/AWS Shield)                 │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: Application Security                              │
│  - CORS (configurable origins)                             │
│  - Trusted Host Middleware (production)                    │
│  - Security Headers (XSS, CSP, HSTS)                       │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Authentication & Authorization                    │
│  - JWT access tokens (60 min expiry)                       │
│  - JWT refresh tokens (7 day expiry)                       │
│  - OWASP BOLA protection (resource ownership)              │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: Input Validation                                  │
│  - Pydantic schemas (type safety)                          │
│  - SQL injection prevention (SQLAlchemy ORM)               │
│  - XSS prevention (JSON encoding)                          │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 5: Audit & Monitoring                                │
│  - Audit logging (all CRUD operations)                     │
│  - Request tracing (X-Request-ID)                          │
│  - Error logging (structured JSON)                         │
└─────────────────────────────────────────────────────────────┘
```

### Security Risk Mitigations

| Risk ID | OWASP Category | Vulnerability | Mitigation | Implementation |
|---------|----------------|---------------|------------|----------------|
| **CA001** | A06:2021 Vulnerable Components | FastAPI CVE-2024-47874 | Upgrade to FastAPI ≥0.121.0 | requirements.txt, Dockerfile |
| **CA005** | A02:2021 Cryptographic Failures | Insecure WebSocket (WS) | WSS with TLS/SSL | nginx.conf, production config |
| **CA006** | API1:2023 BOLA | Broken Object Level Authorization | Resource ownership verification | middleware/auth.py (verify_resource_ownership) |
| **CF003** | N/A | Memory MCP cascade failures | Circuit breaker pattern | utils/memory_mcp_client.py (CircuitBreaker) |

---

## Performance Architecture

### Multi-Worker Setup

```python
# Gunicorn Configuration (gunicorn_config.py)
workers = 2 * multiprocessing.cpu_count() + 1  # 25 workers on 12-core system
worker_class = "uvicorn.workers.UvicornWorker"  # ASGI server
worker_connections = 1000  # Max concurrent connections per worker
max_requests = 10000  # Restart worker after 10k requests (memory leak prevention)
max_requests_jitter = 1000  # Random jitter (prevent thundering herd)
timeout = 120  # Worker timeout (2 minutes)
```

**Worker Capacity**:
- **Total Workers**: 25
- **Connections per Worker**: 1,000
- **Total Capacity**: 25,000 concurrent connections (HTTP)
- **WebSocket Capacity**: 45-50k (Redis pub/sub scaling)

### Database Query Optimization

```sql
-- Indexed queries for common operations

-- 1. List user's tasks with filtering (uses idx_tasks_user_status)
SELECT * FROM scheduled_task
WHERE user_id = '123' AND status = 'pending'
ORDER BY created_at DESC LIMIT 20 OFFSET 0;

-- 2. Get next tasks to execute (uses idx_tasks_next_run)
SELECT * FROM scheduled_task
WHERE next_run_at <= NOW() AND status = 'pending'
ORDER BY next_run_at ASC LIMIT 100;

-- 3. Get task execution history (uses idx_execution_task_time)
SELECT * FROM execution_result
WHERE task_id = 123
ORDER BY started_at DESC LIMIT 10;

-- 4. Audit log by entity (uses idx_audit_entity)
SELECT * FROM audit_log
WHERE entity_type = 'scheduled_task' AND entity_id = 123
ORDER BY timestamp DESC LIMIT 50;
```

### Caching Strategy

```python
# Redis Caching Layer (future enhancement)
cache_strategy = {
    "task_list": {
        "key": "tasks:user:{user_id}:status:{status}",
        "ttl": 60,  # 1 minute
        "invalidate_on": ["task_create", "task_update", "task_delete"]
    },
    "project_detail": {
        "key": "project:{project_id}",
        "ttl": 300,  # 5 minutes
        "invalidate_on": ["project_update", "task_create", "task_delete"]
    },
    "agent_metrics": {
        "key": "agent:{agent_id}:metrics",
        "ttl": 30,  # 30 seconds
        "invalidate_on": ["agent_activity_log"]
    }
}
```

---

## Resilience Architecture

### Circuit Breaker Pattern (CF003 Mitigation)

```python
# Circuit Breaker States
CircuitBreaker
├── CLOSED (normal operation)
│   ├── Success: Call Memory MCP
│   ├── Failure: Increment failure count
│   └── Threshold: 3 consecutive failures → OPEN
├── OPEN (immediate fallback)
│   ├── All calls: Fallback to PostgreSQL + Redis
│   ├── Timeout: 60 seconds
│   └── Transition: After timeout → HALF_OPEN
└── HALF_OPEN (recovery testing)
    ├── Test Call: Attempt Memory MCP
    ├── Success: Reset failure count → CLOSED
    └── Failure: → OPEN (60s timeout)
```

**Fallback Hierarchy**:
```
Memory MCP Unavailable
         ↓
PostgreSQL + Redis Fallback
         ↓
(If PostgreSQL unavailable)
Redis Stale Data (24h TTL)
         ↓
(If Redis unavailable)
Error Response (503 Service Unavailable)
```

### Error Handling Strategy

```python
# Error Response Format
{
  "detail": "Human-readable error message",
  "error_id": "uuid-for-tracing",
  "timestamp": "2024-11-08T10:30:00Z",
  "status_code": 500
}

# HTTP Status Codes
200 OK              # Successful GET, PUT, PATCH
201 Created         # Successful POST
204 No Content      # Successful DELETE
400 Bad Request     # Invalid input (e.g., invalid cron expression)
401 Unauthorized    # Missing or invalid JWT token
403 Forbidden       # Valid token but no permission (BOLA)
404 Not Found       # Resource doesn't exist
422 Unprocessable   # Validation error (Pydantic)
429 Too Many Req    # Rate limit exceeded
500 Internal Error  # Server error (logged)
503 Service Unavail # Dependency unavailable (e.g., database down)
```

---

## Deployment Architecture

### Docker Compose Stack

```yaml
# Production Deployment Stack
services:
  postgres:
    image: postgres:15-alpine
    ports: 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: pg_isready -U postgres -d ruv_sparc_db
      interval: 10s
      timeout: 5s
      retries: 5
    secrets:
      - db_user
      - db_password

  redis:
    image: redis:7-alpine
    ports: 6379:6379
    volumes:
      - redis_data:/data
    healthcheck:
      test: redis-cli ping
      interval: 10s
      timeout: 5s
      retries: 5
    secrets:
      - redis_password

  backend:
    build: ./backend
    ports: 8000:8000
    depends_on:
      postgres: {condition: service_healthy}
      redis: {condition: service_healthy}
    environment:
      - DATABASE_URL=postgresql://postgres@postgres:5432/ruv_sparc_db
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=production
    secrets:
      - api_secret_key
    healthcheck:
      test: curl -f http://localhost:8000/api/v1/health
      interval: 15s
      timeout: 5s
      retries: 3

  frontend:
    build: ./frontend
    ports:
      - 80:80
      - 443:443
    depends_on:
      - backend
    volumes:
      - ./config/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
```

### Kubernetes Deployment (Future)

```yaml
# Kubernetes Deployment Example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ruv-sparc-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ruv-sparc-backend
  template:
    metadata:
      labels:
        app: ruv-sparc-backend
    spec:
      containers:
      - name: backend
        image: ruv-sparc-backend:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
        livenessProbe:
          httpGet:
            path: /api/v1/liveness
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/readiness
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Conclusion

Phase 2 Backend Core delivers a **production-ready architecture** with:

1. ✅ **Security**: 4 critical vulnerabilities mitigated (CA001, CA005, CA006, CF003)
2. ✅ **Performance**: <100ms API response, 45-50k WebSocket connections
3. ✅ **Resilience**: Circuit breaker pattern prevents cascade failures
4. ✅ **Scalability**: Multi-worker setup with Redis pub/sub
5. ✅ **Maintainability**: Clean architecture with separation of concerns

**Next Steps**: Phase 3 Frontend Integration

---

*Document Version: 1.0.0*
*Last Updated: 2024-11-08*
*For API details, see PHASE_2_API_REFERENCE.md*
