# Development Setup Guide

This guide will help you set up your local development environment for the RUV SPARC UI Dashboard.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Local Development (Without Docker)](#local-development-without-docker)
- [Docker Development](#docker-development)
- [Database Migrations](#database-migrations)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Recommended Version | Installation |
|----------|----------------|---------------------|--------------|
| **Node.js** | 18.0.0 | 20.x or higher | [nodejs.org](https://nodejs.org/) |
| **Python** | 3.11.0 | 3.11.5 or higher | [python.org](https://www.python.org/) |
| **Docker** | 24.0.0 | Latest stable | [docker.com](https://www.docker.com/) |
| **Docker Compose** | 2.20.0 | Latest stable | Included with Docker Desktop |
| **Git** | 2.40.0 | Latest stable | [git-scm.com](https://git-scm.com/) |
| **PostgreSQL** | 15.0 | 15.x or higher | [postgresql.org](https://www.postgresql.org/) (optional for local dev) |
| **Redis** | 7.0 | 7.x or higher | [redis.io](https://redis.io/) (optional for local dev) |

### Verify Installation

```bash
# Check Node.js version
node --version
# Expected: v18.x.x or higher

# Check Python version
python --version
# Expected: Python 3.11.x

# Check Docker version
docker --version
# Expected: Docker version 24.x.x

# Check Docker Compose version
docker compose version
# Expected: Docker Compose version v2.x.x

# Check Git version
git --version
# Expected: git version 2.x.x
```

---

## Quick Start

### Option 1: Docker Setup (Recommended for Beginners)

```bash
# 1. Clone the repository
git clone https://github.com/ruvnet/ruv-sparc-ui-dashboard.git
cd ruv-sparc-ui-dashboard

# 2. Create Docker secrets
mkdir -p docker/secrets
echo "postgres_user" > docker/secrets/db_user.txt
echo "secure_password_123" > docker/secrets/db_password.txt
echo "redis_password_456" > docker/secrets/redis_password.txt
openssl rand -hex 32 > docker/secrets/api_secret_key.txt

# 3. Start all services with Docker Compose
docker compose up -d

# 4. Verify services are running
docker compose ps

# 5. Access the application
# Frontend: http://localhost:80
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Option 2: Local Development (Faster Iteration)

```bash
# 1. Clone the repository
git clone https://github.com/ruvnet/ruv-sparc-ui-dashboard.git
cd ruv-sparc-ui-dashboard

# 2. Install dependencies
cd frontend && npm install && cd ..
cd backend && pip install -r requirements.txt && cd ..

# 3. Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your local database credentials

# 4. Start PostgreSQL and Redis locally
# (See "Local Development Without Docker" section)

# 5. Run database migrations
cd backend
alembic upgrade head
cd ..

# 6. Start backend (Terminal 1)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. Start frontend (Terminal 2)
cd frontend
npm run dev
```

---

## Local Development (Without Docker)

Local development provides faster iteration cycles for frontend and backend changes.

### Step 1: Install PostgreSQL Locally

#### macOS (Homebrew)
```bash
brew install postgresql@15
brew services start postgresql@15

# Create database
createdb ruv_sparc_db
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE ruv_sparc_db;
CREATE USER ruv_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ruv_sparc_db TO ruv_user;
\q
```

#### Windows
1. Download PostgreSQL 15 installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer and follow the wizard
3. Use pgAdmin to create database `ruv_sparc_db`

### Step 2: Install Redis Locally

#### macOS (Homebrew)
```bash
brew install redis
brew services start redis
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

#### Windows
1. Download Redis from [redis.io/download](https://redis.io/download)
2. Extract and run `redis-server.exe`
3. Or use WSL2 with Ubuntu instructions

### Step 3: Configure Backend Environment

Create `backend/.env` file:

```bash
# Database Configuration
DATABASE_URL=postgresql://ruv_user:your_password@localhost:5432/ruv_sparc_db

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Environment
ENVIRONMENT=development
LOG_LEVEL=debug

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100

# Optional: Memory MCP Integration
MEMORY_MCP_ENABLED=true
MEMORY_MCP_HOST=localhost
MEMORY_MCP_PORT=8765
```

### Step 4: Install Backend Dependencies

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black ruff pytest pytest-cov httpx
```

### Step 5: Run Database Migrations

```bash
cd backend

# Initialize Alembic (if not already initialized)
# alembic init alembic

# Create initial migration (if not exists)
# alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Verify tables created
psql -U ruv_user -d ruv_sparc_db -c "\dt"
```

### Step 6: Start Backend Development Server

```bash
cd backend

# Start with hot-reload enabled
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Or use the shortcut (if defined in main.py)
python -m app.main
```

Backend will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Step 7: Install Frontend Dependencies

```bash
cd frontend

# Install dependencies
npm install

# Or use yarn
yarn install
```

### Step 8: Start Frontend Development Server

```bash
cd frontend

# Start Vite dev server with hot-reload
npm run dev

# Access at http://localhost:5173 (default Vite port)
```

Frontend will be available at:
- Development server: http://localhost:5173

### Step 9: Verify Setup

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/api/v1/health
   # Expected: {"status": "healthy", "database": "connected", ...}
   ```

2. **Frontend Access**:
   - Open http://localhost:5173 in your browser
   - You should see the RUV SPARC UI Dashboard

3. **WebSocket Connection** (optional):
   ```bash
   # Install wscat for testing
   npm install -g wscat

   # Connect to WebSocket endpoint
   wscat -c ws://localhost:8000/ws/tasks
   ```

---

## Docker Development

### Starting Services

```bash
# Start all services in detached mode
docker compose up -d

# Start specific service
docker compose up -d backend

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f backend
```

### Stopping Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v

# Stop and remove images
docker compose down --rmi all
```

### Rebuilding Containers

```bash
# Rebuild all services
docker compose build

# Rebuild specific service
docker compose build backend

# Rebuild and start
docker compose up -d --build
```

### Accessing Container Shells

```bash
# Backend container
docker compose exec backend bash

# Frontend container
docker compose exec frontend sh

# PostgreSQL container
docker compose exec postgres psql -U postgres -d ruv_sparc_db

# Redis container
docker compose exec redis redis-cli
```

### Docker Development Workflow

1. **Make code changes** in your editor (hot-reload enabled)
2. **Test changes** immediately (no rebuild needed for code changes)
3. **Add new dependencies**:
   ```bash
   # Backend: Add to requirements.txt, then rebuild
   docker compose build backend
   docker compose up -d backend

   # Frontend: Add with npm, then rebuild
   cd frontend && npm install new-package
   docker compose build frontend
   docker compose up -d frontend
   ```

---

## Database Migrations

### Creating a New Migration

```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new column to tasks table"

# Manually create empty migration
alembic revision -m "Custom migration"
```

### Editing Migration Files

Migrations are located in `backend/alembic/versions/`.

Example migration file:
```python
"""Add status column to tasks

Revision ID: abc123def456
Revises: previous_revision_id
Create Date: 2025-11-08 20:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abc123def456'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    # Add status column
    op.add_column(
        'scheduled_tasks',
        sa.Column('status', sa.String(20), nullable=False, server_default='pending')
    )
    # Create index
    op.create_index('ix_tasks_status', 'scheduled_tasks', ['status'])

def downgrade():
    # Remove index
    op.drop_index('ix_tasks_status', 'scheduled_tasks')
    # Remove column
    op.drop_column('scheduled_tasks', 'status')
```

### Applying Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade abc123def456

# Apply next migration only
alembic upgrade +1
```

### Rolling Back Migrations

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123def456

# Rollback all migrations
alembic downgrade base
```

### Migration Best Practices

1. **Always review auto-generated migrations** before applying
2. **Test migrations on development database** first
3. **Include both upgrade and downgrade** paths
4. **Use transactions** for data migrations
5. **Avoid destructive operations** without backups

---

## Testing

### Frontend Testing

#### Unit Tests (Jest + React Testing Library)

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test -- TaskCard.test.tsx

# Run tests matching pattern
npm test -- --testNamePattern="should render"
```

#### End-to-End Tests (Playwright)

```bash
cd frontend

# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui

# Run E2E tests in headed mode (see browser)
npm run test:e2e:headed

# Run E2E tests with debugging
npm run test:e2e:debug

# Run E2E tests for specific browser
npm run test:e2e:chromium
npm run test:e2e:firefox
npm run test:e2e:webkit

# View test report
npm run test:e2e:report
```

#### Frontend Test Configuration

- **Jest config**: `frontend/jest.config.js`
- **Playwright config**: `frontend/playwright.config.e2e.ts`
- **Test utilities**: `frontend/src/test-utils.tsx`

### Backend Testing

#### Unit and Integration Tests (pytest)

```bash
cd backend

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_tasks.py

# Run specific test function
pytest tests/test_tasks.py::test_create_task

# Run tests matching pattern
pytest -k "test_create"

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

#### Test Fixtures

Common fixtures are defined in `backend/tests/conftest.py`:

```python
# Example usage
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, auth_headers: dict):
    """Test task creation with authenticated user."""
    response = await client.post(
        "/api/v1/tasks",
        json={"name": "Test Task", "schedule_cron": "0 * * * *"},
        headers=auth_headers
    )
    assert response.status_code == 201
```

#### Backend Test Configuration

- **Pytest config**: `backend/pytest.ini` or `backend/pyproject.toml`
- **Test database**: Uses in-memory SQLite or dedicated test PostgreSQL database
- **Test fixtures**: `backend/tests/conftest.py`

### Running All Tests

```bash
# From project root
# Frontend tests
cd frontend && npm test && cd ..

# Backend tests
cd backend && pytest --cov=app && cd ..
```

### Test Coverage Requirements

| Component | Minimum Coverage |
|-----------|-----------------|
| Frontend | 90% |
| Backend | 90% |

---

## Troubleshooting

### Common Issues

#### Issue 1: Port Already in Use

**Error**:
```
Error starting userland proxy: listen tcp 0.0.0.0:8000: bind: address already in use
```

**Solution**:
```bash
# Find process using port
# macOS/Linux:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill process
# macOS/Linux:
kill -9 <PID>
# Windows:
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

#### Issue 2: Database Connection Failed

**Error**:
```
sqlalchemy.exc.OperationalError: connection to server at "localhost", port 5432 failed
```

**Solution**:
```bash
# Verify PostgreSQL is running
# macOS:
brew services list
# Ubuntu:
sudo systemctl status postgresql

# Check connection
psql -U postgres -c "SELECT version();"

# Verify .env file has correct DATABASE_URL
cat backend/.env | grep DATABASE_URL
```

#### Issue 3: Module Not Found (Python)

**Error**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**:
```bash
# Activate virtual environment
cd backend
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
```

#### Issue 4: TypeScript Errors (Frontend)

**Error**:
```
TS2307: Cannot find module '@/components/TaskCard' or its corresponding type declarations.
```

**Solution**:
```bash
cd frontend

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Restart TypeScript server in VSCode
# Ctrl+Shift+P → "TypeScript: Restart TS Server"

# Verify tsconfig.json paths
cat tsconfig.json | grep paths
```

#### Issue 5: Docker Build Fails

**Error**:
```
ERROR [backend 5/8] RUN pip install -r requirements.txt
```

**Solution**:
```bash
# Clear Docker build cache
docker builder prune -a

# Rebuild without cache
docker compose build --no-cache backend

# Check Dockerfile syntax
cat backend/Dockerfile

# Verify requirements.txt exists
ls backend/requirements.txt
```

#### Issue 6: Alembic Migration Fails

**Error**:
```
alembic.util.exc.CommandError: Target database is not up to date.
```

**Solution**:
```bash
cd backend

# Check current revision
alembic current

# Check pending migrations
alembic history

# Apply migrations one by one
alembic upgrade +1

# If stuck, reset to base and re-apply
alembic downgrade base
alembic upgrade head
```

### Getting Help

If you encounter issues not covered here:

1. **Check documentation**: Review `docs/ARCHITECTURE.md` and `docs/CONTRIBUTING.md`
2. **Search GitHub issues**: Look for similar problems and solutions
3. **Ask for help**: Create a new issue with detailed error logs
4. **Contact maintainers**: Email support@ruv-sparc.io

### Useful Commands

```bash
# Check all service statuses
docker compose ps

# View resource usage
docker stats

# Clean up Docker system
docker system prune -a --volumes

# Reset entire environment (WARNING: deletes all data)
docker compose down -v
rm -rf backend/venv
rm -rf frontend/node_modules
```

---

## Next Steps

- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
- Read [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines
- Explore [CI_CD.md](./CI_CD.md) for deployment pipelines

---

**Last Updated**: 2025-11-08
**Version**: 1.0.0
