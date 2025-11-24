# Phase 2 Backend - 5-Minute Quick Start Guide

**Get the RUV SPARC UI Dashboard backend running in under 5 minutes!**

---

## Prerequisites

- **Python 3.11+**
- **Docker** & **Docker Compose**
- **Git**

---

## Step 1: Clone & Setup (1 minute)

```bash
# Clone repository
git clone <repository-url>
cd ruv-sparc-ui-dashboard

# Navigate to backend
cd backend

# Copy environment template
cp .env.example .env
```

---

## Step 2: Start Infrastructure (2 minutes)

```bash
# Start PostgreSQL + Redis with Docker Compose
docker-compose -f ../docker-compose.yml up -d postgres redis

# Wait for health checks (30 seconds)
docker-compose -f ../docker-compose.yml ps
```

**Expected output**:
```
NAME                  STATUS              PORTS
ruv-sparc-postgres    Up (healthy)        5432/tcp
ruv-sparc-redis       Up (healthy)        6379/tcp
```

---

## Step 3: Install Dependencies (1 minute)

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4: Run Backend (1 minute)

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
🚀 Starting RUV SPARC UI Dashboard API...
📦 FastAPI version: 0.121.0
🔒 Security: JWT + Rate Limiting + CORS enabled
✅ Database connection pool initialized
INFO:     Application startup complete.
```

---

## Step 5: Verify Installation (30 seconds)

Open browser to: **http://localhost:8000/api/docs**

You should see the **Swagger UI** with all API endpoints!

**Health Check**:
```bash
curl http://localhost:8000/api/v1/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-11-08T10:30:00.000Z",
  "database": "connected",
  "memory_mcp": "unavailable",
  "version": "1.0.0"
}
```

---

## 🎉 Success! You're Running!

### What's Next?

1. **Explore API**: http://localhost:8000/api/docs
2. **Create a Task**: POST /api/v1/tasks
3. **List Tasks**: GET /api/v1/tasks
4. **Run Tests**: `pytest tests/ -v`

---

## Common Issues

### Issue: Database connection failed

**Solution**:
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart PostgreSQL
docker-compose -f ../docker-compose.yml restart postgres
```

### Issue: Port 8000 already in use

**Solution**:
```bash
# Use different port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Issue: Module not found

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Production Deployment

For production deployment with **25 workers**:

```bash
# Use Gunicorn
gunicorn app.main:app -c gunicorn_config.py
```

---

## Stop Services

```bash
# Stop backend (Ctrl+C)

# Stop Docker services
docker-compose -f ../docker-compose.yml down
```

---

## Next Steps

- 📖 Read [PHASE_2_API_REFERENCE.md](./PHASE_2_API_REFERENCE.md) for API documentation
- 🏗️ Read [PHASE_2_ARCHITECTURE_REVIEW.md](./PHASE_2_ARCHITECTURE_REVIEW.md) for architecture details
- 🚀 Read [PHASE_2_DEPLOYMENT_GUIDE.md](./PHASE_2_DEPLOYMENT_GUIDE.md) for production deployment

---

**Total Time**: ~5 minutes ⏱️
**Difficulty**: Easy ✅
**Status**: Production Ready 🎉
