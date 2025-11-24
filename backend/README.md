# Agent Reality Map Backend API

Production-ready FastAPI backend for Agent Reality Map integration with Phase 2 RBAC, real-time WebSocket streaming, and comprehensive agent management.

## Features

- **Agent Management**: CRUD operations for 207 agents with identity, RBAC, and budget controls
- **Metrics Aggregation**: Performance, cost, and quality tracking with analytics
- **Audit Trail**: Immutable security logs for compliance and incident investigation
- **WebSocket Streaming**: Real-time agent activity updates for dashboard
- **RBAC Integration**: Seamless integration with Phase 2 security hooks
- **SQLite Database**: Production-grade persistence with SQLAlchemy ORM

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python scripts/init_database.py
```

This will:
- Create all database tables (agent_identities, agent_metrics, agent_audit_log)
- Load 207 agents from Phase 1 identity files
- Verify database setup

### 3. Start API Server

```bash
python -m app.main
```

Server will start on `http://localhost:8000`

### 4. Explore API

- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **WebSocket**: ws://localhost:8000/api/v1/agents/activity/stream

## API Endpoints

### Agent Management (`/api/v1/agents`)

- `POST /` - Create new agent
- `GET /` - List agents (with filters: role, category, specialist)
- `GET /{agent_id}` - Get agent by ID
- `GET /name/{agent_name}` - Get agent by name
- `PUT /{agent_id}` - Update agent
- `DELETE /{agent_id}` - Delete agent
- `POST /{agent_id}/activate` - Mark agent as active
- `GET /stats/summary` - Aggregate agent statistics

### Metrics (`/api/v1/metrics`)

- `POST /` - Record new metric
- `GET /` - List metrics (with filters: agent_id, metric_type, date range)
- `GET /aggregate` - Aggregated analytics
- `GET /agent/{agent_id}/summary` - Agent-specific metrics summary

### Events (`/api/v1/events`)

- `POST /ingest` - Ingest hook event from Phase 2
- `GET /audit` - Query audit logs (with filters)
- `GET /audit/stats` - Aggregate audit statistics

### WebSocket (`/api/v1/agents/activity/stream`)

Real-time streaming for:
- Agent activation/completion events
- Budget updates
- RBAC decisions
- Metric recordings

## Database Schema

### agent_identities

Stores 207 agents with:
- UUID identity (`agent_id`)
- RBAC role and permissions
- Budget limits and current usage
- Performance metrics
- Metadata (category, specialist, version, tags)

### agent_metrics

Time-series performance tracking:
- Execution time
- Success rate
- Cost (tokens, API calls, USD)
- Quality scores (Connascence analysis)
- Task completion statistics

### agent_audit_log

Immutable audit trail:
- Agent identity and role
- Operation performed
- RBAC decision (allowed/denied/requires_approval)
- Target resources
- Timestamp (90-day retention)

## Integration with Phase 2

The backend integrates with Phase 2 RBAC Engine:

1. **Event Ingestion**: Phase 2 `post-audit-trail` hook calls `/api/v1/events/ingest`
2. **Metrics Recording**: Phase 2 hooks call `/api/v1/metrics/` for performance tracking
3. **Agent Activation**: Phase 2 calls `/api/v1/agents/{id}/activate` when agent starts task

## Performance

- **API Response Time**: <100ms (target)
- **WebSocket Broadcasting**: <50ms latency
- **Database**: SQLite with WAL mode for concurrent access
- **Connection Pooling**: Automatic with SQLAlchemy

## Testing

```bash
# Run tests
pytest backend/tests/

# Test specific endpoint
curl http://localhost:8000/api/v1/agents/

# Test WebSocket (requires wscat)
wscat -c ws://localhost:8000/api/v1/agents/activity/stream
```

## Security

- **RBAC Enforcement**: All endpoints secured with Phase 2 RBAC (when enabled)
- **Audit Logging**: All operations logged to immutable audit trail
- **CORS**: Configured for frontend origins (localhost:3000, localhost:5173)
- **Input Validation**: Pydantic schemas enforce strict validation

## Deployment

### Development

```bash
python -m app.main
```

### Production (with Gunicorn)

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Database locked error

If you see "database is locked", ensure:
1. Only one process is writing at a time
2. WAL mode is enabled (handled automatically)

### WebSocket connection refused

Ensure:
1. Server is running
2. Firewall allows port 8000
3. CORS allows frontend origin

### Agents not loading

Run initialization script again:
```bash
python scripts/init_database.py
```

## Next Steps

After Phase 3 completion:
- **Phase 4**: Build frontend dashboard components (Agent Registry UI, Activity Feed, Quality Metrics)
- **Phase 5**: Integration testing (end-to-end validation)
- **Phase 6**: Production deployment

## Architecture

```
backend/
├── app/
│   ├── main.py                    # FastAPI app + lifespan
│   ├── database.py                # SQLAlchemy config
│   ├── models/
│   │   ├── agent.py               # Agent ORM model
│   │   ├── metric.py              # Metric ORM model
│   │   └── audit.py               # AuditLog ORM model
│   ├── routers/
│   │   ├── agents.py              # Agent management endpoints
│   │   ├── metrics.py             # Metrics aggregation endpoints
│   │   └── events.py              # Event ingestion endpoints
│   └── websocket/
│       └── agent_activity.py      # WebSocket server
├── scripts/
│   └── init_database.py           # Database initialization
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Contributing

This backend is part of the Agent Reality Map Integration (Phase 3).

**Related Documentation**:
- Phase 1: Agent Identity System
- Phase 2: RBAC Engine & Security Hooks
- Phase 4: Frontend Dashboard
- Comprehensive Plan: `/docs/AGENT-REALITY-MAP-COMPREHENSIVE-PLAN.md`

## License

Part of ruv-sparc-three-loop-system plugin.
