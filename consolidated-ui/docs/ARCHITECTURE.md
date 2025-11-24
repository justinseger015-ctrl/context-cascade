# RUV SPARC UI Dashboard - System Architecture

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [API Architecture](#api-architecture)
- [Real-Time Communication](#real-time-communication)
- [Memory MCP Integration](#memory-mcp-integration)
- [Security Architecture](#security-architecture)
- [Performance Optimization](#performance-optimization)

---

## Overview

The RUV SPARC UI Dashboard is a production-ready web application for managing scheduled tasks, agent orchestration, and real-time monitoring. It implements a modern three-tier architecture with comprehensive security, performance optimization, and observability features.

### Key Features

- **Task Scheduling**: Automated skill/agent execution with cron expressions
- **Project Management**: Hierarchical organization with nested task tracking
- **Agent Registry**: Real-time activity monitoring and performance metrics
- **WebSocket Updates**: Live task status broadcasting via Redis pub/sub
- **Memory MCP Integration**: Persistent context with tagging protocol and circuit breaker
- **Multi-User Support**: JWT-based authentication with role-based access control (RBAC)

---

## Technology Stack

### Frontend
- **Framework**: React 18.3.1
- **State Management**: Zustand 5.0.8 (atomic state), Jotai 2.15.1 (derived state)
- **UI Components**: Custom components with Tailwind CSS 4.1.17
- **Form Validation**: React Hook Form 7.66.0 + Zod 4.1.12
- **Workflow Visualization**: ReactFlow 11.11.4
- **Build Tool**: Vite 5.4.10 + TypeScript 5.6.2
- **Testing**: Jest 30.2.0, Playwright 1.56.1, Testing Library 16.3.0

### Backend
- **Framework**: FastAPI 0.121.0+ (CVE-2024-47874 patched)
- **ASGI Server**: Uvicorn 0.30.0+ with Gunicorn 22.0.0
- **ORM**: SQLAlchemy 2.0.30+ with async support
- **Database**: PostgreSQL 15+ with connection pooling
- **Cache/Memory**: Redis 7+ with aioredis 2.0.1
- **Security**: Python-JOSE (JWT), Passlib (bcrypt hashing)
- **Validation**: Pydantic 2.8.0+ with comprehensive schemas
- **Rate Limiting**: SlowAPI 0.1.9

### Infrastructure
- **Containerization**: Docker Compose 3.9
- **Database Migrations**: Alembic 1.13.0
- **Message Queue**: Redis Pub/Sub for WebSocket broadcasting
- **Memory System**: Memory MCP with ChromaDB vector storage

---

## System Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
        WS_Client[WebSocket Client]
    end

    subgraph "Frontend (React 18)"
        App[React Application]
        Zustand[Zustand Store]
        Jotai[Jotai Atoms]
        ReactFlow[ReactFlow Diagrams]
    end

    subgraph "Backend (FastAPI)"
        API[REST API Server]
        WS_Server[WebSocket Server]
        Auth[JWT Auth Middleware]
        RateLimit[Rate Limiter]
        BOLA[BOLA Protection]
    end

    subgraph "Data Layer"
        Postgres[(PostgreSQL 15)]
        Redis[(Redis 7)]
        MemoryMCP[Memory MCP + ChromaDB]
    end

    subgraph "External Services"
        Claude[Claude Code Agents]
        Skills[Skill Execution]
    end

    Browser -->|HTTP/HTTPS| App
    Browser -->|WebSocket| WS_Client
    App --> Zustand
    App --> Jotai
    App --> ReactFlow
    App -->|REST API| API
    WS_Client -->|WS Connection| WS_Server

    API --> Auth
    Auth --> RateLimit
    RateLimit --> BOLA
    BOLA --> Postgres
    API --> Redis
    WS_Server --> Redis
    API --> MemoryMCP

    API --> Claude
    API --> Skills

    style Browser fill:#e1f5ff
    style App fill:#b3e5fc
    style API fill:#81c784
    style Postgres fill:#ffb74d
    style Redis fill:#ff8a65
    style MemoryMCP fill:#ba68c8
```

### Request Flow

```mermaid
sequenceDiagram
    participant Client
    participant NGINX
    participant FastAPI
    participant Auth
    participant RateLimit
    participant Database
    participant Redis
    participant MemoryMCP

    Client->>NGINX: HTTPS Request
    NGINX->>FastAPI: Forward Request
    FastAPI->>Auth: Verify JWT Token
    Auth->>FastAPI: Token Valid
    FastAPI->>RateLimit: Check Rate Limit
    RateLimit->>FastAPI: Allowed
    FastAPI->>Database: Query Data
    Database->>FastAPI: Return Results
    FastAPI->>Redis: Cache Result
    FastAPI->>MemoryMCP: Store Context
    MemoryMCP->>FastAPI: Context Stored
    FastAPI->>NGINX: JSON Response
    NGINX->>Client: HTTPS Response
```

---

## Database Schema

### Entity-Relationship Diagram

```mermaid
erDiagram
    USERS ||--o{ PROJECTS : owns
    USERS ||--o{ SCHEDULED_TASKS : creates
    USERS ||--o{ REFRESH_TOKENS : has
    PROJECTS ||--o{ SCHEDULED_TASKS : contains
    SCHEDULED_TASKS ||--o{ EXECUTION_RESULTS : produces
    AGENTS ||--o{ AUDIT_LOGS : performs

    USERS {
        int id PK
        string username UK
        string email UK
        string hashed_password
        enum role "admin|user"
        boolean is_active
        boolean is_verified
        timestamp created_at
        timestamp updated_at
        timestamp last_login
        string full_name
        text bio
        string avatar_url
    }

    REFRESH_TOKENS {
        int id PK
        int user_id FK
        string token UK
        timestamp expires_at
        timestamp created_at
        boolean revoked
        timestamp revoked_at
        string user_agent
        string ip_address
    }

    PROJECTS {
        int id PK
        string name
        string description
        timestamp created_at
        timestamp updated_at
        int tasks_count
        string user_id FK
    }

    SCHEDULED_TASKS {
        int id PK
        string skill_name
        string schedule_cron
        timestamp next_run_at
        json params_json
        enum status "pending|running|completed|failed|disabled"
        timestamp created_at
        timestamp updated_at
        string user_id FK
    }

    EXECUTION_RESULTS {
        int id PK
        int task_id FK
        timestamp started_at
        timestamp ended_at
        enum status "success|failed|timeout|cancelled"
        text output_text
        text error_text
        int duration_ms
    }

    AGENTS {
        int id PK
        string name UK
        enum type "coder|reviewer|tester|..."
        json capabilities_json
        enum status "active|idle|busy|offline|error"
        timestamp last_active_at
    }

    AUDIT_LOGS {
        int id PK
        string entity_type
        int entity_id
        enum action "CREATE|UPDATE|DELETE"
        string user_id
        json old_values
        json new_values
        timestamp created_at
    }
```

### Key Relationships

1. **Users → Projects**: One-to-many (user can own multiple projects)
2. **Projects → Scheduled Tasks**: One-to-many (project contains multiple tasks)
3. **Scheduled Tasks → Execution Results**: One-to-many (task has execution history)
4. **Users → Refresh Tokens**: One-to-many (user can have multiple active sessions)

### Indexes and Constraints

#### Projects Table
- `ix_projects_user_created`: Composite index on `(user_id, created_at)`
- `ix_projects_name_user`: Composite index on `(name, user_id)`

#### Scheduled Tasks Table
- `ix_scheduled_tasks_user_status`: Composite index on `(user_id, status)`
- `ix_scheduled_tasks_status_next_run`: Composite index on `(status, next_run_at)`
- CHECK constraint: `status IN ('pending', 'running', 'completed', 'failed', 'disabled')`

#### Agents Table
- `ix_agents_type_status`: Composite index on `(type, status)`
- `ix_agents_status_active`: Composite index on `(status, last_active_at)`
- CHECK constraint: `status IN ('active', 'idle', 'busy', 'offline', 'error')`
- CHECK constraint: `type IN ('coder', 'reviewer', 'tester', ...)`

#### Execution Results Table
- `ix_execution_results_task_started`: Composite index on `(task_id, started_at)`
- `ix_execution_results_status_started`: Composite index on `(status, started_at)`
- CHECK constraint: `status IN ('success', 'failed', 'timeout', 'cancelled')`
- CHECK constraint: `duration_ms >= 0`

---

## API Architecture

### REST Endpoints

```mermaid
graph LR
    subgraph "Authentication (/api/v1/auth)"
        A1[POST /register]
        A2[POST /login]
        A3[POST /refresh]
        A4[POST /logout]
        A5[GET /me]
    end

    subgraph "Health (/api/v1/health)"
        H1[GET /]
    end

    subgraph "Projects (/api/v1/projects)"
        P1[GET /]
        P2[POST /]
        P3[GET /:id]
        P4[PUT /:id]
        P5[DELETE /:id]
    end

    subgraph "Tasks (/api/v1/tasks)"
        T1[GET /]
        T2[POST /]
        T3[GET /:id]
        T4[PUT /:id]
        T5[DELETE /:id]
        T6[GET /:id/history]
    end

    subgraph "Agents (/api/v1/agents)"
        AG1[GET /]
        AG2[POST /]
        AG3[GET /:id]
        AG4[PUT /:id/status]
        AG5[POST /activity]
    end

    style A1 fill:#ffcdd2
    style P1 fill:#c8e6c9
    style T1 fill:#bbdefb
    style AG1 fill:#fff9c4
```

### WebSocket Events

```mermaid
sequenceDiagram
    participant Client
    participant WebSocket
    participant Redis_PubSub
    participant Database

    Note over Client,Database: WebSocket Connection Flow

    Client->>WebSocket: Connect to /ws/tasks
    WebSocket->>Client: Connection Established

    Note over Client,Database: Task Status Update Flow

    Database->>Redis_PubSub: Publish task_status_changed
    Redis_PubSub->>WebSocket: Receive Event
    WebSocket->>Client: Broadcast task:status_changed
    Client->>Client: Update UI in Real-Time

    Note over Client,Database: Agent Activity Flow

    Database->>Redis_PubSub: Publish agent_activity
    Redis_PubSub->>WebSocket: Receive Event
    WebSocket->>Client: Broadcast agent:activity
    Client->>Client: Update Agent Dashboard

    Note over Client,Database: Heartbeat Flow

    loop Every 30 seconds
        Client->>WebSocket: Send ping
        WebSocket->>Client: Send pong
    end

    Client->>WebSocket: Disconnect
    WebSocket->>Client: Connection Closed
```

### API Rate Limits

| Endpoint Type | Limit | Period | Notes |
|--------------|-------|--------|-------|
| Standard API | 100 req | 1 min | General endpoints |
| Activity Logging | 1000 req | 1 min | High-frequency agent activity |
| Agent Creation | 60 req | 1 min | Resource-intensive operations |
| Authentication | 50 req | 1 min | Login, registration |
| WebSocket Connections | 10 connections | per IP | Concurrent limit |

---

## Real-Time Communication

### WebSocket Architecture

```mermaid
graph TB
    subgraph "Frontend"
        WSClient[WebSocket Client]
        UIComponent[React Component]
    end

    subgraph "Backend WebSocket Server"
        ConnectionMgr[Connection Manager]
        Heartbeat[Heartbeat Monitor]
        Broadcaster[Task Status Broadcaster]
    end

    subgraph "Redis Pub/Sub"
        Channel1[task_status_changed]
        Channel2[agent_activity]
        Channel3[execution_completed]
    end

    subgraph "Data Sources"
        TaskAPI[Task CRUD API]
        AgentAPI[Agent Activity API]
        Database[(PostgreSQL)]
    end

    WSClient <-->|WebSocket| ConnectionMgr
    ConnectionMgr --> Heartbeat
    ConnectionMgr --> Broadcaster

    Broadcaster --> Channel1
    Broadcaster --> Channel2
    Broadcaster --> Channel3

    TaskAPI -->|Publish| Channel1
    AgentAPI -->|Publish| Channel2
    Database -->|Trigger| Channel3

    Channel1 -->|Subscribe| Broadcaster
    Channel2 -->|Subscribe| Broadcaster
    Channel3 -->|Subscribe| Broadcaster

    Broadcaster -->|Broadcast| ConnectionMgr
    ConnectionMgr -->|Push| WSClient
    WSClient --> UIComponent

    style WSClient fill:#e1f5ff
    style ConnectionMgr fill:#81c784
    style Broadcaster fill:#ffb74d
    style Database fill:#ba68c8
```

### Message Types

1. **task:status_changed**: Task execution status updates
   ```json
   {
     "type": "task:status_changed",
     "task_id": 123,
     "status": "running",
     "timestamp": "2025-11-08T20:00:00Z"
   }
   ```

2. **agent:activity**: Agent activity logging
   ```json
   {
     "type": "agent:activity",
     "agent_id": 456,
     "action": "task_started",
     "details": {...}
   }
   ```

3. **execution:completed**: Task execution results
   ```json
   {
     "type": "execution:completed",
     "task_id": 123,
     "result_id": 789,
     "status": "success",
     "duration_ms": 1500
   }
   ```

---

## Memory MCP Integration

### Tagging Protocol Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        API[FastAPI Backend]
        TaskService[Task Service]
        AgentService[Agent Service]
    end

    subgraph "Memory MCP Client"
        TagProtocol[Tagging Protocol]
        CircuitBreaker[Circuit Breaker]
        FallbackMode[Fallback Mode]
        VectorSearch[Vector Search API]
    end

    subgraph "Memory MCP Server"
        ChromaDB[(ChromaDB)]
        Embeddings[384-dim Embeddings]
        HNSW[HNSW Indexing]
    end

    API --> TaskService
    API --> AgentService

    TaskService --> TagProtocol
    AgentService --> TagProtocol

    TagProtocol --> CircuitBreaker
    CircuitBreaker -->|Open| FallbackMode
    CircuitBreaker -->|Closed| VectorSearch
    CircuitBreaker -->|Half-Open| VectorSearch

    VectorSearch --> ChromaDB
    ChromaDB --> Embeddings
    Embeddings --> HNSW

    style API fill:#81c784
    style TagProtocol fill:#ffb74d
    style CircuitBreaker fill:#ff8a65
    style ChromaDB fill:#ba68c8
```

### Tagging Protocol Requirements

All Memory MCP writes **must** include metadata tags:

1. **WHO**: Agent name, category, capabilities
2. **WHEN**: ISO timestamp, Unix timestamp, readable format
3. **PROJECT**: `ruv-sparc-ui-dashboard`, `memory-mcp-triple-system`, etc.
4. **WHY**: Intent (implementation, bugfix, refactor, testing, documentation, analysis, planning, research)

Example:
```python
from app.utils.memory_mcp_client import memory_client

# Automatic tagging via protocol
await memory_client.store(
    content="Implemented task scheduling feature",
    metadata={
        "agent": "coder",
        "task_id": "TASK-123",
        "feature": "scheduling"
    }
)
# Auto-tagged with WHO/WHEN/PROJECT/WHY
```

### Circuit Breaker States

```mermaid
stateDiagram-v2
    [*] --> Closed
    Closed --> Open: 3 consecutive failures
    Open --> HalfOpen: 60s timeout
    HalfOpen --> Closed: Success
    HalfOpen --> Open: Failure

    note right of Closed
        Normal operation
        All requests pass through
    end note

    note right of Open
        Fallback mode active
        No Memory MCP calls
        Local logging only
    end note

    note right of HalfOpen
        Trial period
        Test with single request
    end note
```

**Configuration**:
- Failure threshold: 3 consecutive failures
- Timeout: 60 seconds
- Half-open max calls: 1
- Success threshold to close: 1

---

## Security Architecture

### Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Auth
    participant Database
    participant Redis

    Note over Client,Redis: Registration Flow

    Client->>API: POST /api/v1/auth/register
    API->>Auth: Hash Password (bcrypt)
    Auth->>Database: Create User
    Database->>API: User Created
    API->>Client: 201 Created

    Note over Client,Redis: Login Flow

    Client->>API: POST /api/v1/auth/login
    API->>Database: Query User
    Database->>API: User Found
    API->>Auth: Verify Password (bcrypt)
    Auth->>API: Password Valid
    API->>Auth: Generate JWT (access + refresh)
    Auth->>Database: Store Refresh Token
    API->>Redis: Cache User Session
    API->>Client: 200 OK + JWT Tokens

    Note over Client,Redis: Authenticated Request Flow

    Client->>API: GET /api/v1/tasks (Bearer Token)
    API->>Auth: Verify JWT Signature
    Auth->>Redis: Check Session Valid
    Redis->>Auth: Session Active
    Auth->>API: Token Valid + User Context
    API->>Database: Query with BOLA Check
    Database->>API: User's Tasks Only
    API->>Client: 200 OK + Tasks

    Note over Client,Redis: Refresh Token Flow

    Client->>API: POST /api/v1/auth/refresh
    API->>Database: Verify Refresh Token
    Database->>API: Token Valid
    API->>Auth: Generate New Access Token
    API->>Client: 200 OK + New Access Token

    Note over Client,Redis: Logout Flow

    Client->>API: POST /api/v1/auth/logout
    API->>Database: Revoke Refresh Token
    API->>Redis: Invalidate Session
    API->>Client: 200 OK
```

### OWASP API Security Implementation

| Risk | Mitigation | Implementation |
|------|-----------|----------------|
| **API1:2023 BOLA** | Resource ownership verification | All queries filter by `user_id` |
| **API2:2023 Broken Authentication** | JWT with bcrypt hashing | Python-JOSE + Passlib |
| **API3:2023 Broken Object Property** | Input validation | Pydantic schemas with strict typing |
| **API4:2023 Unrestricted Resource Access** | Rate limiting | SlowAPI with 100 req/min |
| **API5:2023 Broken Function Level Authorization** | RBAC with roles | Admin/User roles with middleware checks |
| **API7:2023 Server Side Request Forgery** | URL validation | Pydantic URL validators |
| **API8:2023 Security Misconfiguration** | Security headers | CSP, HSTS, X-Frame-Options |

### Security Headers

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

---

## Performance Optimization

### Database Connection Pooling

```python
# SQLAlchemy async engine configuration
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Max 20 connections
    max_overflow=10,       # Additional 10 overflow connections
    pool_timeout=30,       # 30s wait for connection
    pool_recycle=3600,     # Recycle connections every hour
    pool_pre_ping=True,    # Verify connection before use
    echo=False             # Disable SQL logging in production
)
```

### Redis Caching Strategy

```mermaid
graph LR
    Request[API Request] --> Cache{Redis Cache}
    Cache -->|HIT| Return[Return Cached Data]
    Cache -->|MISS| Database[(PostgreSQL)]
    Database --> Store[Store in Redis]
    Store --> Return

    style Cache fill:#ff8a65
    style Database fill:#ffb74d
```

**Cache TTL**:
- User sessions: 3600 seconds (1 hour)
- Task lists: 300 seconds (5 minutes)
- Agent status: 60 seconds (1 minute)
- Project metadata: 1800 seconds (30 minutes)

### Async Parallelism

```python
# Concurrent task execution
async def get_dashboard_data(user_id: str):
    # Execute queries in parallel
    tasks, projects, agents = await asyncio.gather(
        get_user_tasks(user_id),
        get_user_projects(user_id),
        get_active_agents()
    )
    return DashboardData(tasks, projects, agents)
```

### WebSocket Optimization

- **Heartbeat interval**: 30 seconds
- **Max message size**: 1 MB
- **Compression**: Enabled for messages > 1 KB
- **Connection timeout**: 300 seconds (5 minutes)
- **Reconnection strategy**: Exponential backoff (1s, 2s, 4s, 8s, 16s)

---

## Deployment Architecture

### Docker Compose Setup

```mermaid
graph TB
    subgraph "Docker Network: ruv-sparc-network (172.28.0.0/16)"
        Frontend[Frontend Container<br/>nginx:alpine<br/>Port 80, 443]
        Backend[Backend Container<br/>FastAPI + Uvicorn<br/>Port 8000]
        Postgres[PostgreSQL Container<br/>postgres:15-alpine<br/>Port 5432]
        Redis[Redis Container<br/>redis:7-alpine<br/>Port 6379]
    end

    subgraph "Volumes"
        PG_Data[(postgres_data)]
        Redis_Data[(redis_data)]
        Backend_Logs[(backend_logs)]
        Frontend_Logs[(frontend_logs)]
    end

    subgraph "Docker Secrets"
        DB_User[db_user.txt]
        DB_Pass[db_password.txt]
        Redis_Pass[redis_password.txt]
        API_Key[api_secret_key.txt]
    end

    Frontend --> Backend
    Backend --> Postgres
    Backend --> Redis

    Postgres --> PG_Data
    Redis --> Redis_Data
    Backend --> Backend_Logs
    Frontend --> Frontend_Logs

    Backend -.->|Read| DB_User
    Backend -.->|Read| DB_Pass
    Backend -.->|Read| Redis_Pass
    Backend -.->|Read| API_Key

    style Frontend fill:#b3e5fc
    style Backend fill:#81c784
    style Postgres fill:#ffb74d
    style Redis fill:#ff8a65
```

---

## Monitoring and Observability

### Logging Strategy

```python
# Structured logging with request tracing
logger.info(
    "Task created",
    extra={
        "request_id": request_id,
        "user_id": current_user.id,
        "task_id": task.id,
        "skill_name": task.skill_name,
        "timestamp": datetime.utcnow().isoformat()
    }
)
```

### Health Check Endpoint

```http
GET /api/v1/health

Response:
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "memory_mcp": "operational",
  "websocket": "active",
  "version": "1.0.0"
}
```

---

## Next Steps

- Implement distributed tracing with OpenTelemetry
- Add Prometheus metrics export
- Configure Grafana dashboards for real-time monitoring
- Set up ELK stack for centralized logging
- Implement A/B testing framework
- Add feature flags for gradual rollouts

---

**Last Updated**: 2025-11-08
**Maintainer**: RUV SPARC Team
**Version**: 1.0.0
