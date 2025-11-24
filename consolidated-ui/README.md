# Ruv-Sparc UI Dashboard - Docker Infrastructure

**Phase 1, Task 1 (P1_T1)**: Docker Compose Infrastructure with Security Hardening

## Security Features

### CVE-2024-47874 Mitigation
- **FastAPI Version**: 0.121.0+ (CRITICAL DoS vulnerability patched)
- **CVSS Score**: 8.7 (HIGH severity)
- **Status**: ✅ PATCHED

### Container Security
- ✅ **Non-root users**: All containers run as non-root (postgres, redis, nginx, appuser)
- ✅ **Trivy scanning**: Automated security scanning with zero CRITICAL CVEs requirement
- ✅ **Secret management**: Docker secrets (NOT environment variables)
- ✅ **SSL/TLS**: PostgreSQL verify-full mode, Nginx HTTPS with TLS 1.2+

## Architecture

```
┌─────────────────────────────────────────────┐
│           Nginx Frontend (Port 80/443)      │
│         SSL/TLS, Rate Limiting, Gzip        │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│      FastAPI Backend (Port 8000)            │
│   Gunicorn + Uvicorn Workers (4)            │
│   FastAPI 0.121.0+ (CVE-2024-47874 fix)     │
└─────────┬───────────────────┬───────────────┘
          │                   │
          ▼                   ▼
┌─────────────────┐   ┌─────────────────┐
│  PostgreSQL 15  │   │    Redis 7      │
│  SSL verify-full│   │  AOF persistence│
│  Persistent Vol │   │  LRU eviction   │
└─────────────────┘   └─────────────────┘
```

## Quick Start

### 1. Setup Secrets
```bash
chmod +x scripts/setup-secrets.sh
./scripts/setup-secrets.sh
```

### 2. Build and Start Services
```bash
docker-compose build
docker-compose up -d
```

### 3. Verify FastAPI Version
```bash
chmod +x scripts/verify-fastapi-version.sh
./scripts/verify-fastapi-version.sh
```

### 4. Run Trivy Security Scan
```bash
chmod +x scripts/trivy-scan.sh
./scripts/trivy-scan.sh
```

### 5. Check Service Health
```bash
docker-compose ps
docker-compose logs -f
```

## Service Endpoints

- **Frontend**: http://localhost (redirects to HTTPS)
- **Backend API**: http://localhost/api
- **API Docs**: http://localhost/api/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Health Checks

All services include health checks:
- **PostgreSQL**: `pg_isready` (30s start period)
- **Redis**: `redis-cli ping` (10s start period)
- **Backend**: `curl http://localhost:8000/health` (30s start period)
- **Frontend**: `curl http://localhost/health` (10s start period)

## Security Configuration

### PostgreSQL
- SSL enabled with TLS 1.2+
- scram-sha-256 authentication
- Connection only allowed from Docker network (172.28.0.0/16)
- Persistent volume for data

### Redis
- Password authentication via Docker secret
- AOF persistence (appendonly yes)
- Memory limit: 256MB with LRU eviction

### FastAPI Backend
- Runs as non-root user (appuser)
- Secret-based configuration
- Gunicorn process manager (4 workers)
- Request/response logging

### Nginx Frontend
- Security headers (CSP, X-Frame-Options, etc.)
- Rate limiting (API: 10 req/s, General: 100 req/s)
- Gzip compression
- SSL/TLS with strong ciphers

## Docker Secrets

Located in `docker/secrets/` (auto-generated):
- `db_user.txt` - PostgreSQL username
- `db_password.txt` - PostgreSQL password
- `redis_password.txt` - Redis password
- `api_secret_key.txt` - API secret key

**⚠️ WARNING**: These files are gitignored and should NEVER be committed!

## Trivy Scan Reports

Reports saved to `docker/trivy-reports/`:
- `backend-scan.json` - Backend image vulnerabilities
- `frontend-scan.json` - Frontend image vulnerabilities
- `postgres-scan.json` - PostgreSQL image vulnerabilities
- `redis-scan.json` - Redis image vulnerabilities

**Requirement**: Zero CRITICAL CVEs for deployment approval

## Development

### Rebuild Specific Service
```bash
docker-compose build backend
docker-compose up -d backend
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Stop Services
```bash
docker-compose down
```

### Clean Up (including volumes)
```bash
docker-compose down -v
```

## Compliance

✅ **Loop 1 Security Requirements Met**:
- [x] CVE-2024-47874 patched (FastAPI 0.121.0+)
- [x] Trivy scanning enabled
- [x] Non-root containers
- [x] Secret management
- [x] SSL/TLS encryption
- [x] Health checks
- [x] Persistent volumes
- [x] Network isolation

## Next Steps (Phase 1)

- **P1_T2**: Initialize FastAPI project with config management
- **P1_T3**: Database schema design and migrations
- **P1_T4**: Redis session management setup
- **P1_T5**: Frontend framework initialization

---

**Task**: P1_T1 - Project Setup & Docker Compose Infrastructure
**Status**: ✅ COMPLETE
**Agent**: DevOps Engineer (CI/CD)
**Security**: CVE-2024-47874 PATCHED | Trivy Scans PASSING
