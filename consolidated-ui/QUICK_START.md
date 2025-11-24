# Quick Start Guide - Ruv-Sparc UI Dashboard

## 1-Minute Setup

```bash
# Navigate to project
cd /c/Users/17175/ruv-sparc-ui-dashboard

# Generate secrets
./scripts/setup-secrets.sh

# Build and start
docker-compose up -d

# Verify
./scripts/validate-deployment.sh
```

## What You Get

✅ **PostgreSQL 15** - Production database with SSL
✅ **Redis 7** - Session management with persistence
✅ **FastAPI 0.121.0+** - Backend API (CVE-2024-47874 patched)
✅ **Nginx** - Frontend reverse proxy with HTTPS

## Verify Everything Works

```bash
# Check services
docker-compose ps

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost/health

# View logs
docker-compose logs -f
```

## Security Check

```bash
# Verify CVE-2024-47874 is patched
./scripts/verify-fastapi-version.sh

# Run security scan (requires Trivy)
./scripts/trivy-scan.sh
```

## Access Points

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Troubleshooting

**Services won't start?**
```bash
# Check logs
docker-compose logs <service-name>

# Common fixes
./scripts/setup-secrets.sh  # Regenerate secrets
docker-compose down -v      # Clean restart
```

**Health checks failing?**
```bash
# Wait 30-60 seconds for startup
docker-compose ps

# Check individual service
docker-compose logs backend
```

## Next Steps

1. ✅ **P1_T1 Complete** - Docker infrastructure ready
2. ⏭️ **P1_T2** - Initialize FastAPI project with config management
3. ⏭️ **P1_T3** - Database schema design and migrations
4. ⏭️ **P1_T4** - Redis session management setup
5. ⏭️ **P1_T5** - Frontend framework initialization

## Documentation

- `README.md` - Full project overview
- `DEPLOYMENT.md` - Detailed deployment guide
- `docs/P1_T1_COMPLETION_REPORT.md` - Technical completion report

---

**Task**: P1_T1 - Docker Compose Infrastructure
**Status**: ✅ COMPLETE
**Security**: CVE-2024-47874 PATCHED
