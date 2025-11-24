# P2_T3 WebSocket Integration Checklist

## ✅ Pre-Integration Verification

### Files Created (11 files)
- [x] `app/websocket/__init__.py` - Module exports
- [x] `app/websocket/message_types.py` - Message schemas
- [x] `app/websocket/connection_manager.py` - Connection management
- [x] `app/websocket/redis_pubsub.py` - Redis pub/sub
- [x] `app/websocket/heartbeat.py` - Heartbeat management
- [x] `app/websocket/router.py` - FastAPI router
- [x] `app/websocket/client_example.html` - Client example
- [x] `app/websocket/README.md` - Documentation
- [x] `tests/test_websocket.py` - Test suite
- [x] `app/main_websocket_integration.py` - Integration example
- [x] `scripts/test_websocket_load.py` - Load testing script

### Dependencies Required
- [x] fastapi
- [x] websockets
- [x] redis (aioredis)
- [x] python-jose[cryptography] (JWT)
- [x] pydantic

---

## 🔧 Integration Steps

### Step 1: Install Dependencies

```bash
cd C:\Users\17175\ruv-sparc-ui-dashboard\backend

pip install redis[hiredis] python-jose[cryptography]
# or add to requirements.txt:
# redis[hiredis]==5.0.1
# python-jose[cryptography]==3.3.0
```

### Step 2: Update Main Application

Option A: Use the provided integration example:
```bash
# Copy integration example to main.py
cp app/main_websocket_integration.py app/main.py
```

Option B: Add WebSocket router to existing main.py:
```python
from app.websocket.router import router as websocket_router, on_startup, on_shutdown

# Include router
app.include_router(websocket_router, tags=["WebSocket"])

# Add startup/shutdown handlers
@app.on_event("startup")
async def startup():
    await on_startup()

@app.on_event("shutdown")
async def shutdown():
    await on_shutdown()
```

### Step 3: Update Configuration

Add to `app/core/config.py`:
```python
class Settings(BaseSettings):
    # Existing settings...

    # WebSocket settings
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT settings (if not already present)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
```

Add to `.env`:
```bash
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

### Step 4: Start Redis

```bash
# Using Docker
docker run -d -p 6379:6379 --name redis redis:7-alpine

# Or using local Redis
redis-server
```

### Step 5: Run Application

```bash
# Development (single worker)
uvicorn app.main:app --reload --port 8000

# Production (multiple workers)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🧪 Testing Steps

### Step 1: Unit Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/test_websocket.py -v

# With coverage
pytest tests/test_websocket.py -v --cov=app.websocket --cov-report=html
```

### Step 2: Manual Testing

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Get a JWT token:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'
```

3. Open client example:
```bash
# Open in browser
start app/websocket/client_example.html
# Or use a WebSocket client like Postman
```

4. Test connection:
   - Enter JWT token
   - Click "Connect"
   - Verify connection established
   - Check ping/pong messages

### Step 3: Health Check

```bash
curl http://localhost:8000/ws/health
```

Expected response:
```json
{
  "status": "healthy",
  "connections": {
    "total": 1,
    "local": 1,
    "alive": 1,
    "dead": 0
  },
  "redis": {
    "connected": true,
    "pubsub_connected": true
  }
}
```

### Step 4: Load Testing

```bash
# Small load (1k connections)
python scripts/test_websocket_load.py

# Edit script to test specific loads:
# - 1k connections (warm-up)
# - 10k connections (medium load)
# - 50k connections (target load)
```

---

## 🔐 Production Checklist

### Security
- [ ] Replace default SECRET_KEY in production
- [ ] Use WSS (wss://) with TLS/SSL
- [ ] Configure CORS appropriately
- [ ] Add rate limiting
- [ ] Enable Redis authentication
- [ ] Use strong JWT signing algorithm (RS256 recommended)

### Configuration
- [ ] Set REDIS_URL for production Redis instance
- [ ] Configure Redis connection pool size
- [ ] Set appropriate heartbeat intervals
- [ ] Configure WebSocket timeout values
- [ ] Set up Redis persistence (AOF or RDB)

### Infrastructure
- [ ] Deploy Redis cluster for high availability
- [ ] Set up Redis Sentinel or Redis Cluster
- [ ] Configure load balancer for WebSocket (sticky sessions)
- [ ] Set up TLS termination (nginx/Caddy)
- [ ] Configure firewall rules

### Monitoring
- [ ] Set up health check monitoring
- [ ] Monitor Redis memory usage
- [ ] Track connection metrics
- [ ] Set up alerts for connection failures
- [ ] Monitor message latency
- [ ] Track error rates

### Performance
- [ ] Tune Redis configuration for 50k connections
- [ ] Adjust uvicorn worker count
- [ ] Configure OS limits (file descriptors)
- [ ] Enable connection pooling
- [ ] Test with production load

---

## 🚀 Multi-Worker Setup

### Why Multiple Workers?

- **Horizontal Scaling**: Handle more connections
- **High Availability**: Worker failure doesn't affect all connections
- **Load Distribution**: Connections distributed across workers
- **Performance**: Utilize multiple CPU cores

### Configuration

```python
# app/main.py
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # 4 workers for 4 CPU cores
        log_level="info",
    )
```

Or via command line:
```bash
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Load Balancing

Nginx configuration for WebSocket load balancing:
```nginx
upstream websocket_backend {
    ip_hash;  # Sticky sessions for WebSocket
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    location /ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 📊 Expected Performance

### Targets
- **Concurrent Connections**: 45-50k
- **Connection Time**: < 100ms
- **Message Latency**: < 50ms
- **Memory per Connection**: ~10KB
- **Total Memory (50k)**: ~500MB

### Redis Configuration for 50k Connections

```bash
redis-server \
    --maxmemory 2gb \
    --maxmemory-policy allkeys-lru \
    --maxclients 50000 \
    --tcp-backlog 511 \
    --timeout 0
```

### OS Limits (Linux)

```bash
# Increase file descriptor limit
ulimit -n 100000

# Add to /etc/security/limits.conf
* soft nofile 100000
* hard nofile 100000

# Increase TCP backlog
sysctl -w net.core.somaxconn=4096
sysctl -w net.ipv4.tcp_max_syn_backlog=4096
```

---

## 🐛 Troubleshooting

### Issue: Cannot connect to Redis

**Solution**:
```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# Check Redis URL in .env
REDIS_URL=redis://localhost:6379/0
```

### Issue: WebSocket connection fails

**Solution**:
1. Check JWT token is valid
2. Verify CORS settings
3. Check server logs for errors
4. Test with `/ws/health` endpoint

### Issue: High memory usage

**Solution**:
1. Check connection count: `/ws/health`
2. Verify Redis TTL is working
3. Monitor for connection leaks
4. Adjust heartbeat timeout

### Issue: Slow performance

**Solution**:
1. Increase Redis connection pool
2. Add more workers
3. Check network latency
4. Monitor Redis performance
5. Profile application code

---

## 📝 Usage Examples

### Broadcasting Task Updates

```python
from app.websocket.redis_pubsub import redis_pubsub
from app.websocket.message_types import TaskStatusUpdate
import uuid

@app.post("/tasks/{task_id}/update")
async def update_task(task_id: str, status: str, progress: int):
    # Update task in database
    # ...

    # Broadcast to all connected clients
    message = TaskStatusUpdate(
        event_id=str(uuid.uuid4()),
        data={
            "task_id": task_id,
            "status": status,
            "progress": progress,
        }
    )
    await redis_pubsub.publish_broadcast(message)

    return {"status": "updated"}
```

### Sending User Notifications

```python
from app.websocket.redis_pubsub import redis_pubsub
from app.websocket.message_types import WSMessage, MessageType
import uuid

@app.post("/users/{user_id}/notify")
async def notify_user(user_id: str, message: str):
    # Send to specific user
    ws_message = WSMessage(
        type=MessageType.AGENT_ACTIVITY_UPDATE,
        event_id=str(uuid.uuid4()),
        data={"message": message}
    )
    await redis_pubsub.publish_to_user(user_id, ws_message)

    return {"status": "sent"}
```

---

## ✅ Completion Checklist

### Development
- [x] All files created
- [x] Dependencies documented
- [x] Tests written
- [x] Documentation complete
- [x] Example client provided
- [x] Load testing script provided

### Integration
- [ ] Dependencies installed
- [ ] Redis running
- [ ] Configuration updated
- [ ] WebSocket router integrated
- [ ] Environment variables set

### Testing
- [ ] Unit tests passing
- [ ] Manual testing successful
- [ ] Health check working
- [ ] Load testing completed

### Production
- [ ] Security hardened
- [ ] TLS/SSL configured
- [ ] Monitoring set up
- [ ] Performance tuned
- [ ] Documentation reviewed

---

## 📚 Additional Resources

- [FastAPI WebSocket Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [Redis Pub/Sub Documentation](https://redis.io/topics/pubsub)
- [WebSocket RFC 6455](https://tools.ietf.org/html/rfc6455)
- [JWT Authentication](https://jwt.io/)
- [Load Testing Guide](https://github.com/websockets/websocket-bench)

---

**Status**: Ready for Integration
**Next**: Follow integration steps above
**Support**: See `app/websocket/README.md` for detailed documentation
