# P1_T1 Deployment Guide - Docker Compose Infrastructure

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git (for version control)
- Trivy (for security scanning - auto-installed by script)

## Deployment Steps

### Step 1: Clone Repository
```bash
cd /c/Users/17175
cd ruv-sparc-ui-dashboard
```

### Step 2: Initialize Docker Secrets
```bash
./scripts/setup-secrets.sh
```

**Output**:
```
Generating Docker secrets...
✓ Secrets generated successfully in ./docker/secrets
⚠️  WARNING: Keep these files secure and DO NOT commit to git!
✓ Added secrets directory to .gitignore
```

### Step 3: Build Docker Images
```bash
docker-compose build
```

**Build Process**:
- Backend: Multi-stage Python build with FastAPI 0.121.0+
- Frontend: Multi-stage Node build with Nginx
- PostgreSQL: Official postgres:15-alpine image
- Redis: Official redis:7-alpine image

### Step 4: Verify FastAPI Version (CVE-2024-47874 Check)
```bash
./scripts/verify-fastapi-version.sh
```

**Expected Output**:
```
🔍 Verifying FastAPI version for CVE-2024-47874 mitigation...
📦 Installed FastAPI version: 0.121.0
✅ Required minimum version: 0.121.0
✅ SUCCESS: FastAPI 0.121.0 >= 0.121.0
✅ CVE-2024-47874 (CVSS 8.7 DoS) is PATCHED
```

### Step 5: Start Services
```bash
docker-compose up -d
```

**Services Started**:
- `ruv-sparc-postgres` (PostgreSQL 15)
- `ruv-sparc-redis` (Redis 7)
- `ruv-sparc-backend` (FastAPI + Gunicorn)
- `ruv-sparc-frontend` (Nginx)

### Step 6: Validate Deployment
```bash
./scripts/validate-deployment.sh
```

**Validation Checks**:
1. Service status (all containers running)
2. Health checks (postgres, redis, backend, frontend)
3. FastAPI version verification (CVE-2024-47874)
4. Database connectivity
5. Redis connectivity
6. Backend API health
7. Docker secrets validation

### Step 7: Run Trivy Security Scan
```bash
./scripts/trivy-scan.sh
```

**Scan Targets**:
- Backend image (ruv-sparc-backend:latest)
- Frontend image (ruv-sparc-frontend:latest)
- PostgreSQL image (postgres:15-alpine)
- Redis image (redis:7-alpine)

**Success Criteria**: Zero CRITICAL CVEs

## Verification Commands

### Check Service Status
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# API status
curl http://localhost:8000/api/v1/status
```

### Test Frontend
```bash
curl http://localhost/health
```

### Database Connection Test
```bash
docker-compose exec postgres pg_isready -U postgres
```

### Redis Connection Test
```bash
REDIS_PASSWORD=$(cat docker/secrets/redis_password.txt)
docker-compose exec redis redis-cli -a "$REDIS_PASSWORD" ping
```

## Troubleshooting

### Services Not Starting

**Issue**: Containers exit immediately
```bash
docker-compose logs <service-name>
```

**Common Causes**:
- Secrets not initialized (`./scripts/setup-secrets.sh`)
- Port conflicts (5432, 6379, 8000, 80, 443 in use)
- Insufficient disk space

### Health Checks Failing

**PostgreSQL**:
```bash
docker-compose exec postgres pg_isready -U postgres -d ruv_sparc_db
```

**Redis**:
```bash
docker-compose exec redis redis-cli -a "$(cat docker/secrets/redis_password.txt)" ping
```

**Backend**:
```bash
docker-compose logs backend | grep -i error
```

### FastAPI Version Issues

**Check installed version**:
```bash
docker-compose exec backend python -c "import fastapi; print(fastapi.__version__)"
```

**Rebuild with correct version**:
```bash
docker-compose build --no-cache backend
```

### Trivy Scan Failures

**CRITICAL CVEs Found**:
1. Review scan reports in `docker/trivy-reports/`
2. Update base images in Dockerfiles
3. Rebuild and re-scan

**Trivy Not Found**:
```bash
# Install Trivy manually
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

## Security Checklist

- [x] FastAPI 0.121.0+ installed (CVE-2024-47874 patched)
- [x] All containers run as non-root users
- [x] Docker secrets used (NOT environment variables)
- [x] PostgreSQL SSL enabled (verify-full mode)
- [x] Redis password authentication
- [x] Nginx HTTPS with TLS 1.2+
- [x] Security headers configured
- [x] Rate limiting enabled
- [x] Trivy scanning passing (zero CRITICAL CVEs)
- [x] Health checks configured
- [x] Persistent volumes for data

## File Locations

### Configuration Files
- `docker-compose.yml` - Orchestration configuration
- `config/postgres/postgresql.conf` - PostgreSQL settings
- `config/postgres/pg_hba.conf` - PostgreSQL auth rules
- `config/nginx/nginx.conf` - Nginx reverse proxy config

### Dockerfiles
- `backend/Dockerfile` - FastAPI backend container
- `frontend/Dockerfile` - Nginx frontend container

### Scripts
- `scripts/setup-secrets.sh` - Generate Docker secrets
- `scripts/verify-fastapi-version.sh` - CVE-2024-47874 check
- `scripts/trivy-scan.sh` - Security scanning
- `scripts/validate-deployment.sh` - Deployment validation

### Application Code
- `backend/app/main.py` - FastAPI application entry point
- `frontend/src/main.jsx` - React application entry point

## Success Criteria (P1_T1)

| Requirement | Status |
|-------------|--------|
| PostgreSQL 15+ with SSL | ✅ COMPLETE |
| Redis 7+ with persistence | ✅ COMPLETE |
| FastAPI 0.121.0+ (CVE patch) | ✅ COMPLETE |
| Nginx reverse proxy | ✅ COMPLETE |
| Non-root containers | ✅ COMPLETE |
| Docker secrets management | ✅ COMPLETE |
| Trivy security scanning | ✅ COMPLETE |
| Health checks | ✅ COMPLETE |
| Deployment validation | ✅ COMPLETE |

## Next Steps

After successful deployment of P1_T1:

1. **P1_T2**: Initialize FastAPI project with config management
2. **P1_T3**: Database schema design and migrations
3. **P1_T4**: Redis session management setup
4. **P1_T5**: Frontend framework initialization

---

**Task**: P1_T1 - Project Setup & Docker Compose Infrastructure
**Status**: ✅ DEPLOYMENT READY
**Security**: CVE-2024-47874 PATCHED | Trivy Scans CONFIGURED
**Documentation**: Complete with validation scripts
