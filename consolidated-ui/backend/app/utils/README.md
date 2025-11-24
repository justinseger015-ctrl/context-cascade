# Memory MCP Integration with Circuit Breaker

Production-ready Memory MCP integration for RUV SPARC UI Dashboard implementing P2_T4 requirements.

## Overview

This implementation provides:
- **WHO/WHEN/PROJECT/WHY tagging protocol** - Mandatory metadata for all memory operations
- **Vector search** - Semantic similarity search for task history
- **Circuit breaker pattern** - Prevents cascade failures (from P1_T5)
- **Fallback mechanisms** - PostgreSQL + Redis cache when Memory MCP is unavailable
- **Health monitoring** - Degraded mode detection for UI warning banners

## Components

### 1. Tagging Protocol (`tagging_protocol.py`)

Implements mandatory WHO/WHEN/PROJECT/WHY metadata tagging:

```python
from app.utils import create_backend_dev_tagger, Intent

# Create tagger for your agent
tagger = create_backend_dev_tagger(
    project_id="ruv-sparc-ui-dashboard",
    project_name="RUV SPARC UI Dashboard"
)

# Generate tagged payload
payload = tagger.create_memory_store_payload(
    content="Implemented authentication feature",
    intent=Intent.IMPLEMENTATION,
    task_id="P2_T4",
    additional_metadata={"feature": "auth", "tests_passing": True}
)

# Payload includes:
# - WHO: agent_id, user_id, agent_category, capabilities
# - WHEN: ISO timestamp, Unix timestamp, readable format
# - PROJECT: project_id, project_name, task_id
# - WHY: intent (implementation/bugfix/refactor/testing/documentation/analysis)
```

### 2. Memory MCP Client (`memory_mcp_client.py`)

Main client with circuit breaker and fallback:

```python
from app.utils import create_memory_mcp_client, Intent

# Create client
client = create_memory_mcp_client(
    postgres_client=postgres,
    redis_client=redis
)

# Store with automatic tagging
result = await client.store(
    content="Implemented circuit breaker for Memory MCP",
    intent=Intent.IMPLEMENTATION,
    task_id="P2_T4"
)

# Vector search with semantic similarity
results = await client.vector_search(
    query="circuit breaker implementation",
    project_id="ruv-sparc-ui-dashboard",
    limit=10
)

# Get task history with related tasks
history = await client.get_task_history(
    task_id="P2_T4",
    include_related=True
)

# Health check
health = await client.health_check()
if health["degraded_mode"]:
    print("WARNING: Memory MCP unavailable, using fallback")
```

### 3. Vector Search API (`vector_search_api.py`)

FastAPI endpoints for memory operations:

```python
from app.utils import memory_router

# Add to FastAPI app
app.include_router(memory_router)

# Available endpoints:
# POST /api/v1/memory/search - Vector search
# POST /api/v1/memory/store - Store data
# GET /api/v1/memory/task/{task_id} - Get task history
# GET /api/v1/memory/health - Health check
# GET /api/v1/memory/projects/{project_id}/summary - Project summary
```

### 4. Fallback Mode Tests (`fallback_mode_tests.py`)

Comprehensive test suite for circuit breaker and fallback:

```bash
# Run tests
pytest backend/app/utils/fallback_mode_tests.py -v

# Run with coverage
pytest backend/app/utils/fallback_mode_tests.py --cov=app.utils --cov-report=html
```

## Architecture

```
Memory MCP Integration
├─ Tagging Protocol
│  ├─ WHO: Agent + User identification
│  ├─ WHEN: Temporal metadata
│  ├─ PROJECT: Context information
│  └─ WHY: Intent classification
├─ Memory MCP Client
│  ├─ Circuit Breaker (from P1_T5)
│  ├─ Vector Search (semantic similarity)
│  ├─ Fallback: PostgreSQL + Redis
│  └─ Health Monitoring
└─ Vector Search API
   ├─ POST /search - Semantic search
   ├─ POST /store - Tagged storage
   ├─ GET /task/{id} - History retrieval
   └─ GET /health - Status monitoring
```

## Circuit Breaker States

```
CLOSED (Normal Operation)
  ↓ (3 consecutive failures)
OPEN (Immediate Fallback)
  ↓ (60s timeout)
HALF_OPEN (Recovery Testing)
  ↓ (2 successful calls)
CLOSED (Recovered)
```

## Fallback Mechanisms

### When Memory MCP is Unavailable:

1. **Storage Operations**:
   - Primary: Memory MCP vector storage
   - Fallback: PostgreSQL relational storage + Redis cache

2. **Search Operations**:
   - Primary: Memory MCP vector search (semantic similarity)
   - Fallback: PostgreSQL text search (no semantic ranking)

3. **Task Retrieval**:
   - Primary: Memory MCP with vector-based related tasks
   - Fallback 1: Redis cache (stale data, 24h TTL)
   - Fallback 2: PostgreSQL (no related tasks)

## Usage Examples

### Store Implementation Work

```python
from app.utils import create_memory_mcp_client, Intent

client = create_memory_mcp_client(postgres, redis)

await client.store(
    content="Implemented REST API endpoints for task management",
    intent=Intent.IMPLEMENTATION,
    user_id="dev-123",
    task_id="API-001",
    additional_metadata={
        "endpoints": ["/tasks", "/tasks/{id}"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "tests_added": True
    }
)
```

### Store Bug Fix

```python
await client.store(
    content="Fixed race condition in concurrent task updates",
    intent=Intent.BUGFIX,
    task_id="BUG-042",
    additional_metadata={
        "issue_id": "BUG-042",
        "severity": "high",
        "affected_versions": ["1.0.0", "1.1.0"],
        "fix_verified": True
    }
)
```

### Search Similar Tasks

```python
# Find similar implementations
results = await client.vector_search(
    query="REST API authentication implementation",
    task_type="implementation",  # Filter by intent
    project_id="ruv-sparc-ui-dashboard",
    limit=10
)

# Results are ranked by semantic similarity
for result in results:
    print(f"Task: {result['task_id']}")
    print(f"Similarity: {result['similarity_score']:.2f}")
    print(f"Content: {result['content'][:100]}...")
```

### Get Task History with Context

```python
# Get task with related tasks via vector search
history = await client.get_task_history(
    task_id="P2_T4",
    include_related=True
)

print(f"Task: {history['task']['content']}")
print(f"Related tasks: {len(history['related_tasks'])}")

# If degraded mode:
if "warning" in history:
    print(f"Warning: {history['warning']}")
```

### Health Monitoring

```python
# Check system health
health = await client.health_check()

if health["degraded_mode"]:
    # Show warning banner in UI
    print("⚠️ Memory MCP unavailable - limited search capabilities")
    print(f"Circuit breaker: {health['circuit_breaker_state']}")
    print(f"Fallback available: {health['fallback_available']}")
else:
    print("✓ All systems operational")
```

## Testing Fallback Mode

### Simulate Memory MCP Failure

```python
# In production, this happens automatically via circuit breaker
# For testing, you can kill the Memory MCP server:

# 1. Store some data
await client.store(content="Test", intent=Intent.TESTING)

# 2. Kill Memory MCP server
# pkill -f "memory-mcp-server"

# 3. Attempt operations - should fallback
result = await client.store(content="Test 2", intent=Intent.TESTING)
assert result["status"] == "degraded"
assert result["storage"] == "postgresql_fallback"

# 4. Check health - should show degraded mode
health = await client.health_check()
assert health["degraded_mode"] is True

# 5. Restart Memory MCP server
# Circuit breaker will automatically recover after timeout
```

### Run Automated Tests

```bash
# Run all tests
pytest backend/app/utils/fallback_mode_tests.py -v

# Run specific test class
pytest backend/app/utils/fallback_mode_tests.py::TestFallbackMode -v

# Run with coverage
pytest backend/app/utils/fallback_mode_tests.py --cov=app.utils --cov-report=term-missing
```

## Integration with FastAPI

```python
# main.py
from fastapi import FastAPI
from app.utils import memory_router

app = FastAPI()

# Add Memory MCP routes
app.include_router(memory_router)

# Endpoints available:
# POST /api/v1/memory/search
# POST /api/v1/memory/store
# GET /api/v1/memory/task/{task_id}
# GET /api/v1/memory/health
# GET /api/v1/memory/projects/{project_id}/summary
```

## Configuration

### Environment Variables

```bash
# Memory MCP Configuration
MEMORY_MCP_ENDPOINT=http://localhost:3000
MEMORY_MCP_TIMEOUT=30

# Circuit Breaker Configuration
CIRCUIT_BREAKER_FAILURE_THRESHOLD=3
CIRCUIT_BREAKER_TIMEOUT_DURATION=60
CIRCUIT_BREAKER_HALF_OPEN_MAX_CALLS=2

# Fallback Configuration
REDIS_CACHE_TTL=86400  # 24 hours
POSTGRES_CONNECTION_POOL_SIZE=20
```

### Dependencies

```toml
# pyproject.toml
[tool.poetry.dependencies]
fastapi = "^0.104.0"
pydantic = "^2.5.0"
asyncpg = "^0.29.0"  # PostgreSQL async driver
redis = "^5.0.0"  # Redis client
httpx = "^0.25.0"  # For Memory MCP HTTP calls
```

## Monitoring

### Key Metrics to Track

1. **Circuit Breaker State**:
   - CLOSED: Normal operation
   - OPEN: Failures detected, using fallback
   - HALF_OPEN: Testing recovery

2. **Degraded Mode Time**:
   - Total time in degraded mode
   - Frequency of degradations

3. **Fallback Usage**:
   - PostgreSQL fallback calls
   - Redis cache hits/misses

4. **Vector Search Performance**:
   - Search latency (Memory MCP vs PostgreSQL)
   - Similarity score distribution

### Health Check Endpoint

```bash
# Check health status
curl http://localhost:8000/api/v1/memory/health

# Response:
{
  "status": "healthy",
  "degraded_mode": false,
  "circuit_breaker_state": "CLOSED",
  "mcp_available": true,
  "fallback_available": true,
  "last_check": "2025-11-08T22:00:00Z"
}
```

## Deliverables

✅ `tagging_protocol.py` - WHO/WHEN/PROJECT/WHY metadata generation
✅ `memory_mcp_client.py` - Client with circuit breaker and fallback
✅ `vector_search_api.py` - FastAPI endpoints for memory operations
✅ `fallback_mode_tests.py` - Comprehensive test suite
✅ `README.md` - Complete documentation

## Dependencies

- **P1_T5**: Circuit breaker implementation (✅ Complete)
- **P2_T1**: FastAPI core setup (✅ Complete)

## Risk Mitigations

- **CF003**: Memory MCP circuit breaker prevents cascade failures
- Fallback mechanisms ensure system continues operating
- Health monitoring enables proactive intervention
- Redis cache provides stale data when needed
- PostgreSQL fallback for critical operations

## Next Steps

1. Integrate with main FastAPI application
2. Add Prometheus metrics for monitoring
3. Configure alerting for degraded mode
4. Implement retry logic with exponential backoff
5. Add request tracing for debugging

## Contact

For issues or questions about Memory MCP integration, contact the backend development team.
