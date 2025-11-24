# P2_T4 Architecture - Memory MCP Integration

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                                 │
│                    http://localhost:3000                                 │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ HTTP/JSON
                                 │
┌────────────────────────────────▼────────────────────────────────────────┐
│                    FastAPI Backend (:8000)                               │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    Memory MCP Router                                │ │
│  │              /api/v1/memory/* endpoints                             │ │
│  └────────────────────────────┬───────────────────────────────────────┘ │
│                                │                                          │
│  ┌────────────────────────────▼───────────────────────────────────────┐ │
│  │                  Memory MCP Client                                  │ │
│  │                                                                      │ │
│  │  ┌────────────────────────────────────────────────────────────┐   │ │
│  │  │         Tagging Protocol (WHO/WHEN/PROJECT/WHY)            │   │ │
│  │  │  - Agent identification                                     │   │ │
│  │  │  - Timestamp generation                                     │   │ │
│  │  │  - Project context                                          │   │ │
│  │  │  - Intent classification                                    │   │ │
│  │  └────────────────────────────────────────────────────────────┘   │ │
│  │                                                                      │ │
│  │  ┌────────────────────────────────────────────────────────────┐   │ │
│  │  │         Circuit Breaker (from P1_T5)                        │   │ │
│  │  │  States: CLOSED → OPEN → HALF_OPEN                         │   │ │
│  │  │  Failure threshold: 3                                       │   │ │
│  │  │  Timeout: 60s                                               │   │ │
│  │  └────────────────────────────────────────────────────────────┘   │ │
│  │                                                                      │ │
│  │  ┌────────────────────────────────────────────────────────────┐   │ │
│  │  │         Operations                                          │   │ │
│  │  │  - store() - Tagged storage                                │   │ │
│  │  │  - vector_search() - Semantic search                       │   │ │
│  │  │  - get_task_history() - Task + related                     │   │ │
│  │  │  - health_check() - Status monitoring                      │   │ │
│  │  └────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────┬───────────────┬───────────────────────────┘ │
│                            │               │                              │
└────────────────────────────┼───────────────┼──────────────────────────────┘
                             │               │
                             │               │
        ┌────────────────────┼───────────────┼────────────────────┐
        │                    │               │                    │
        │                    │               │                    │
        ▼                    ▼               ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────┐    ┌──────────────┐
│ Memory MCP   │    │ PostgreSQL   │    │  Redis   │    │   Health     │
│ Server       │    │ Database     │    │  Cache   │    │  Monitoring  │
│ (:3000)      │    │ (:5432)      │    │  (:6379) │    │              │
│              │    │              │    │          │    │              │
│ Primary:     │    │ Fallback:    │    │ Fallback:│    │ Circuit      │
│ - Vector     │    │ - Relational │    │ - Stale  │    │ Breaker      │
│   storage    │    │   storage    │    │   data   │    │ State        │
│ - Semantic   │    │ - Text       │    │ - 24h    │    │ Tracking     │
│   search     │    │   search     │    │   TTL    │    │              │
│ - Similarity │    │ - No         │    │          │    │              │
│   ranking    │    │   semantic   │    │          │    │              │
└──────────────┘    └──────────────┘    └──────────┘    └──────────────┘
```

## Request Flow

### 1. Normal Operation (Memory MCP Available)

```
Client Request
    │
    ▼
FastAPI Endpoint (/api/v1/memory/search)
    │
    ▼
Memory MCP Client
    │
    ├─► Tagging Protocol (add WHO/WHEN/PROJECT/WHY)
    │
    ├─► Circuit Breaker (check state: CLOSED)
    │
    ▼
Memory MCP Server
    │
    ├─► Vector search with embeddings
    ├─► Semantic similarity ranking
    │
    ▼
Results (ranked by similarity_score)
    │
    ├─► Cache in Redis (for fallback)
    │
    ▼
Response to Client
```

### 2. Degraded Mode (Memory MCP Unavailable)

```
Client Request
    │
    ▼
FastAPI Endpoint
    │
    ▼
Memory MCP Client
    │
    ├─► Circuit Breaker (check state: OPEN)
    │   └─► State: OPEN → Skip Memory MCP
    │
    ├─► Try Redis Cache
    │   │
    │   ├─► Cache HIT → Return stale data (24h TTL)
    │   │                │
    │   │                └─► Response with warning:
    │   │                    "Serving stale data - Memory MCP unavailable"
    │   │
    │   └─► Cache MISS
    │       │
    │       ▼
    │   PostgreSQL Fallback
    │       │
    │       ├─► Text search (no semantic similarity)
    │       │
    │       ▼
    │   Results (no ranking)
    │       │
    │       └─► Response with warning:
    │           "Limited search - Memory MCP unavailable"
    │
    ▼
Response to Client
```

## Circuit Breaker State Machine

```
┌─────────────────┐
│     CLOSED      │  Normal operation
│  Memory MCP OK  │  All requests go to Memory MCP
└────────┬────────┘
         │
         │ 3 consecutive failures
         │
         ▼
┌─────────────────┐
│      OPEN       │  Degraded mode
│ Immediate       │  All requests use fallback
│ Fallback        │  (PostgreSQL + Redis)
└────────┬────────┘
         │
         │ After 60s timeout
         │
         ▼
┌─────────────────┐
│   HALF_OPEN     │  Recovery testing
│ Testing MCP     │  Allow 2 test requests
└────────┬────────┘
         │
         ├─► 2 successful requests
         │   └─► Back to CLOSED
         │
         └─► Any failure
             └─► Back to OPEN
```

## Data Flow - Store Operation

```
store(content, intent, task_id) request
    │
    ▼
┌─────────────────────────────────────────────┐
│  1. Tagging Protocol                         │
│     Generate WHO/WHEN/PROJECT/WHY metadata   │
│     {                                        │
│       who: { agent_id, user_id, ... }       │
│       when: { iso, unix, readable }         │
│       project: { id, name, task_id }        │
│       why: { intent, description }          │
│     }                                        │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  2. Circuit Breaker Check                    │
│     State: CLOSED/OPEN/HALF_OPEN             │
└────────────────────┬────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
    State: CLOSED          State: OPEN
         │                       │
         ▼                       │
┌─────────────────┐              │
│  3a. Memory MCP │              │
│      Store      │              │
│  - Vector       │              │
│    embedding    │              │
│  - Metadata     │              │
│    indexing     │              │
└────────┬────────┘              │
         │                       │
         │  Success              │  Skip MCP
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  4. PostgreSQL Store (always)                │
│     - Relational storage                     │
│     - Transaction safety                     │
│     - Fallback data source                   │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  5. Redis Cache (always)                     │
│     - Store with 24h TTL                     │
│     - Stale data fallback                    │
│     - Fast retrieval                         │
└────────────────────┬────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  6. Response                                 │
│     {                                        │
│       status: "success" | "degraded",       │
│       storage: "memory_mcp" | "postgresql", │
│       task_id: "...",                        │
│       warning: "..." (if degraded)          │
│     }                                        │
└─────────────────────────────────────────────┘
```

## Data Flow - Vector Search

```
vector_search(query, filters, limit) request
    │
    ▼
┌─────────────────────────────────────────────┐
│  1. Circuit Breaker Check                    │
└────────────────────┬────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
    State: CLOSED          State: OPEN
         │                       │
         ▼                       │
┌─────────────────┐              │
│  2a. Memory MCP │              │
│   Vector Search │              │
│  - Generate     │              │
│    query        │              │
│    embedding    │              │
│  - Semantic     │              │
│    similarity   │              │
│  - Rank by      │              │
│    score        │              │
└────────┬────────┘              │
         │                       │
         │  Success              │  Skip MCP
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │  2b. Redis      │
         │              │      Cache      │
         │              │  - Check for    │
         │              │    cached data  │
         │              └────────┬────────┘
         │                       │
         │                       │  Cache MISS
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │  2c. PostgreSQL │
         │              │   Text Search   │
         │              │  - No semantic  │
         │              │    similarity   │
         │              │  - No ranking   │
         │              └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│  3. Response                                 │
│     {                                        │
│       results: [                             │
│         {                                    │
│           task_id: "...",                    │
│           content: "...",                    │
│           similarity_score: 0.85,  // MCP   │
│           metadata: { ... }                  │
│         }                                    │
│       ],                                     │
│       source: "memory_mcp" | "postgresql",  │
│       warning: "..." (if degraded)          │
│     }                                        │
└─────────────────────────────────────────────┘
```

## Component Responsibilities

### Tagging Protocol (`tagging_protocol.py`)
- Generate WHO metadata (agent, user, capabilities)
- Generate WHEN metadata (timestamps)
- Generate PROJECT metadata (project, task context)
- Generate WHY metadata (intent classification)
- Provide factory functions for common agent types

### Memory MCP Client (`memory_mcp_client.py`)
- Manage circuit breaker state
- Coordinate storage across Memory MCP, PostgreSQL, Redis
- Handle vector search with semantic similarity
- Implement fallback logic
- Monitor health and degraded mode
- Provide unified API for memory operations

### Vector Search API (`vector_search_api.py`)
- Expose FastAPI endpoints
- Request/response validation with Pydantic
- Dependency injection
- Error handling
- Response formatting

### Circuit Breaker (from P1_T5)
- Track failure/success counts
- Manage state transitions (CLOSED → OPEN → HALF_OPEN)
- Automatic timeout and recovery
- Prevent cascade failures

## Error Handling Strategy

```
┌─────────────────────────────────────────┐
│  Request Processing                      │
└────────────────┬────────────────────────┘
                 │
                 ▼
         Try Memory MCP
                 │
         ┌───────┴────────┐
         │                │
         ▼                ▼
    Success          Exception
         │                │
         │                ├─► Log warning
         │                ├─► Increment failure count
         │                ├─► Update circuit breaker
         │                │
         │                ▼
         │        Try Redis Cache
         │                │
         │        ┌───────┴────────┐
         │        │                │
         │        ▼                ▼
         │   Cache HIT        Cache MISS
         │        │                │
         │        │                ▼
         │        │        Try PostgreSQL
         │        │                │
         │        │        ┌───────┴────────┐
         │        │        │                │
         │        │        ▼                ▼
         │        │    Success          Exception
         │        │        │                │
         │        │        │                └─► Return error
         │        │        │                    (500)
         └────────┴────────┴──────────┐
                                       │
                                       ▼
                              Return Response
                              (with degraded
                               warning if needed)
```

## Monitoring Points

### Metrics to Track
1. **Circuit Breaker State**: CLOSED/OPEN/HALF_OPEN distribution
2. **Failure Rate**: Memory MCP failure percentage
3. **Fallback Usage**: PostgreSQL fallback call count
4. **Cache Hit Rate**: Redis cache effectiveness
5. **Search Latency**: Memory MCP vs PostgreSQL latency
6. **Degraded Mode Time**: Total time in degraded mode

### Health Check Response
```json
{
  "status": "healthy" | "degraded",
  "degraded_mode": false,
  "circuit_breaker_state": "CLOSED",
  "mcp_available": true,
  "fallback_available": true,
  "last_check": "2025-11-08T22:00:00Z",
  "metrics": {
    "total_requests": 1000,
    "mcp_requests": 950,
    "fallback_requests": 50,
    "cache_hits": 200,
    "failure_rate": 0.05
  }
}
```

## Security Considerations

1. **Authentication**: FastAPI dependency injection for auth
2. **Rate Limiting**: Prevent abuse of vector search
3. **Input Validation**: Pydantic models for all requests
4. **SQL Injection**: Use parameterized queries in PostgreSQL
5. **Cache Poisoning**: Validate data before caching in Redis

## Performance Optimization

1. **Connection Pooling**: PostgreSQL connection pool (10-20 connections)
2. **Redis Pipeline**: Batch Redis operations
3. **Async I/O**: Full async/await for all operations
4. **Caching**: 24h TTL for stale data serving
5. **Circuit Breaker**: Fast-fail prevents timeout accumulation

## Future Enhancements

1. **Distributed Tracing**: OpenTelemetry integration
2. **Metrics Export**: Prometheus metrics endpoint
3. **Batch Operations**: Batch vector search for efficiency
4. **Retry Logic**: Exponential backoff for transient failures
5. **Memory Compaction**: Long-term storage optimization
6. **Multi-Region**: Geographic distribution for latency
