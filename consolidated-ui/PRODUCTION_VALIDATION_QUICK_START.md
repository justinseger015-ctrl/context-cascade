# Production Validation - Quick Start Guide

**Project**: Ruv-Sparc UI Dashboard
**Task**: P6_T3 - Production Deployment Testing
**Time Required**: 4-6 hours

---

## 📋 Prerequisites

- ✅ Docker Desktop installed and running
- ✅ Node.js 18+ and npm
- ✅ Python 3.11+
- ✅ Git Bash or WSL (for shell scripts)

---

## 🚀 Quick Start (6-Step Deployment)

### Step 1: Start Infrastructure (15 minutes)

```bash
cd C:/Users/17175/ruv-sparc-ui-dashboard

# Generate secrets
./scripts/setup-secrets.sh

# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# Validate deployment
./scripts/validate-deployment.sh
```

**Expected Output**:
```
✅ PostgreSQL: HEALTHY
✅ Redis: HEALTHY
✅ Backend: HEALTHY
✅ Frontend: HEALTHY
✅ CVE-2024-47874: PATCHED
```

---

### Step 2: Run Automated Tests (30 minutes)

**Backend Tests**:
```bash
cd backend
pytest --cov=app --cov-report=term-missing
```

**Expected**: ✅ Coverage ≥90%, All tests pass

**Frontend Tests**:
```bash
cd frontend
npm test -- --coverage
npx playwright test
```

**Expected**: ✅ All tests pass, No console errors

---

### Step 3: Execute Performance Benchmarks (15 minutes)

**k6 Load Tests**:
```bash
cd k6-load-test-scripts
./run-benchmarks.sh
```

**Expected**:
- API P99 latency: <200ms
- WebSocket latency: <100ms
- Error rate: <1%

**Lighthouse Audit**:
```bash
cd frontend
npx lighthouse http://localhost:3000 --output html --output-path ../lighthouse-reports/home.html
```

**Expected**:
- Performance: ≥90
- Accessibility: 100
- Best Practices: ≥90
- SEO: ≥90

---

### Step 4: Run Security Scans (20 minutes)

**Trivy Container Scan**:
```bash
./scripts/trivy-scan.sh
```

**Expected**: Zero CRITICAL CVEs

**OWASP ZAP Scan** (if installed):
```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:3000 -r zap-report.html
```

**Expected**: Zero HIGH/CRITICAL findings

**axe-core WCAG Scan**:
```bash
cd frontend
npx playwright test --grep "accessibility"
```

**Expected**: WCAG 2.1 AA compliant

---

### Step 5: Manual FR Validation (2 hours)

Open `docs/validation/functional-requirements-checklist.md` and test:

**FR1: Calendar UI (10 requirements)**
- [ ] FR1.1 - Interactive calendar views
- [ ] FR1.2 - Click time slot to schedule
- [ ] FR1.3 - Recurrence patterns
- [ ] FR1.4 - Agent dropdown (86 agents)
- [ ] FR1.5 - Visual status indicators
- [ ] FR1.6 - schedule_config.yml integration
- [ ] FR1.7 - Bi-directional YAML sync
- [ ] FR1.8 - Project tagging
- [ ] FR1.9 - Priority levels
- [ ] FR1.10 - Task execution history

**FR2: Project Dashboard (11 requirements)**
- [ ] FR2.1 - Kanban board drag-and-drop
- [ ] FR2.2 - Board columns (4 columns)
- [ ] FR2.3 - Memory MCP project display
- [ ] FR2.4 - Tasks with assigned agents
- [ ] FR2.5 - Task detail view
- [ ] FR2.6 - Three-Loop phase tracking
- [ ] FR2.7 - Quality Gate visualization
- [ ] FR2.8 - Test coverage progress bars
- [ ] FR2.9 - Duration tracking
- [ ] FR2.10 - Memory MCP integration
- [ ] FR2.11 - Project status indicators

**FR3: Agent Monitor (12 requirements)**
- [ ] FR3.1 - Agent registry (86 agents)
- [ ] FR3.2 - Agent status badges
- [ ] FR3.3 - Filter by category
- [ ] FR3.4 - Search by name/capabilities
- [ ] FR3.5 - Workflow visualization (React Flow)
- [ ] FR3.6 - Three-Loop workflow progression
- [ ] FR3.7 - Byzantine/Raft consensus viz
- [ ] FR3.8 - Quality Gate checkpoints
- [ ] FR3.9 - Skills usage timeline
- [ ] FR3.10 - Real-time activity log (WebSocket)
- [ ] FR3.11 - Hooks system integration
- [ ] FR3.12 - Correlation ID tracking

**FR4: Automatic Startup (6 requirements)**
- [ ] FR4.1 - startup-master.ps1 script
- [ ] FR4.2 - Docker Compose orchestration
- [ ] FR4.3 - Health checks
- [ ] FR4.4 - Browser auto-launch
- [ ] FR4.5 - Data sync on startup
- [ ] FR4.6 - Cross-platform support

---

### Step 6: Smoke Tests (30 minutes)

**Smoke Test 1: Create Task → Execute → See Result**
```
1. Navigate to http://localhost:3000/calendar
2. Click Monday 9:00 AM time slot
3. Enter prompt: "Test task execution"
4. Select agent: "coder"
5. Save task
6. Verify task appears with 🟢 scheduled indicator
7. Manually trigger or wait for scheduled time
8. Verify status changes: 🔵 running → ✅ completed
9. View execution logs
```

**Expected**: ✅ Complete workflow succeeds

**Smoke Test 2: Create Project → Drag Tasks**
```
1. Navigate to http://localhost:3000/dashboard
2. Create project: "Smoke Test Project"
3. Add 3 tasks to Backlog
4. Drag task 1 to In Progress
5. Verify database updated
6. Drag task 2 to Done
7. Check project progress
```

**Expected**: ✅ Drag-and-drop works and persists

**Smoke Test 3: Monitor Agent Activity**
```
1. Navigate to http://localhost:3000/agents
2. Verify 86 agents displayed
3. Execute task with backend-dev agent
4. Verify backend-dev status: 🟢 Active
5. Verify real-time activity log updates
6. Filter by category "Core Development"
7. Verify only Core Development agents shown
```

**Expected**: ✅ Real-time updates work

---

## 🎯 GO/NO-GO Decision

### Automated Validation

Run comprehensive validation suite:
```bash
./scripts/production-validation-suite.sh
```

**Expected Output**:
```
Total Tests:    XX
Passed:        XX
Failed:         0
Pass Rate:     100%

✅ GO FOR PRODUCTION
```

### Decision Criteria

| Criterion | Target | Status |
|-----------|--------|--------|
| All 40 FRs PASS | 40/40 | Check |
| Test coverage | ≥90% | Check |
| Zero CRITICAL CVEs | 0 | Check |
| API P99 latency | <200ms | Check |
| WebSocket latency | <100ms | Check |
| Lighthouse score | ≥90 | Check |
| WCAG 2.1 AA | Compliant | Check |

**Final Decision**:
- ✅ **GO FOR PRODUCTION** if all criteria met
- ⚠️ **CONDITIONAL GO** if minor failures (75-90% pass rate)
- ❌ **NO-GO** if critical failures or <75% pass rate

---

## 📊 Performance Targets

| Metric | Target | Expected | Validation |
|--------|--------|----------|------------|
| API P99 latency | <200ms | ~180ms | k6 benchmark |
| WebSocket latency | <100ms | <50ms | P4_T3 validated |
| Calendar render | <500ms | ~350ms | React Profiler |
| Lighthouse Performance | ≥90 | TBD | Lighthouse CLI |
| Bundle size | <500KB | 180KB | P4_T8 achieved |
| Test coverage | ≥90% | TBD | pytest/Jest |

---

## 🔒 Security Checklist

- [ ] Trivy scan: Zero CRITICAL CVEs
- [ ] OWASP ZAP: Zero HIGH/CRITICAL findings
- [ ] axe-core: WCAG 2.1 AA compliant
- [ ] FastAPI 0.121.0+ (CVE-2024-47874 patched)
- [ ] Docker secrets (no environment variables)
- [ ] Non-root containers
- [ ] PostgreSQL SSL enabled
- [ ] Redis password auth
- [ ] Nginx HTTPS/TLS 1.2+
- [ ] Input validation on all endpoints

---

## 📁 Key Files

**Validation Documentation**:
- `docs/validation/functional-requirements-checklist.md` (16 KB)
- `docs/validation/PRODUCTION_VALIDATION_REPORT.md` (52 KB)
- `P6_T3_PRODUCTION_VALIDATION_SUMMARY.txt` (15 KB)

**Validation Scripts**:
- `scripts/production-validation-suite.sh` (15 KB) - Automated validation
- `scripts/validate-deployment.sh` (4.7 KB) - Deployment validation
- `scripts/trivy-scan.sh` (2.6 KB) - Security scanning

**Test Suites**:
- `backend/pytest.ini` - Backend test configuration
- `frontend/e2e/` - Playwright e2e tests
- `k6-load-test-scripts/` - Performance benchmarks

**Logs and Reports**:
- `staging-deployment-logs/` - Validation logs
- `lighthouse-reports/` - Lighthouse audits
- `docker/trivy-reports/` - Security scans

---

## 🆘 Troubleshooting

### Services Not Starting

**Problem**: Docker services exit immediately

**Solution**:
```bash
# Check logs
docker-compose logs

# Verify secrets initialized
ls -la docker/secrets/

# Re-initialize if needed
./scripts/setup-secrets.sh
docker-compose down
docker-compose up -d
```

### Tests Failing

**Problem**: pytest or Jest tests fail

**Solution**:
```bash
# Backend: Check coverage threshold
cd backend
pytest --cov=app --cov-report=term

# Frontend: Check for console errors
cd frontend
npm test -- --verbose
```

### Performance Targets Not Met

**Problem**: k6 benchmarks show high latency

**Solution**:
```bash
# Apply performance optimizations
./scripts/apply-optimizations.sh

# Restart services
docker-compose restart backend
```

### Security Scans Find CVEs

**Problem**: Trivy reports CRITICAL CVEs

**Solution**:
1. Review Trivy report: `docker/trivy-reports/backend-scan.txt`
2. Update vulnerable dependencies
3. Rebuild images: `docker-compose build --no-cache`
4. Re-scan: `./scripts/trivy-scan.sh`

---

## 📞 Support

For detailed validation procedures, consult:
1. `PRODUCTION_VALIDATION_REPORT.md` - Comprehensive validation guide
2. `functional-requirements-checklist.md` - FR testing procedures
3. `P6_T3_PRODUCTION_VALIDATION_SUMMARY.txt` - Complete summary

---

## ✅ Completion Checklist

**Pre-Deployment**:
- [ ] Docker running
- [ ] Secrets generated
- [ ] Images built
- [ ] Services started
- [ ] Health checks passing

**Testing**:
- [ ] Backend tests passing (≥90% coverage)
- [ ] Frontend tests passing
- [ ] Playwright e2e tests passing
- [ ] Performance benchmarks passing
- [ ] Security scans passing

**Manual Validation**:
- [ ] All 40 FRs tested
- [ ] Smoke tests executed
- [ ] Error scenarios tested
- [ ] Accessibility verified

**Final Decision**:
- [ ] Validation suite executed
- [ ] GO/NO-GO decision made
- [ ] Production deployment approved

---

**Time Estimate**: 4-6 hours total
**Status**: Ready for deployment validation
**Next Step**: Start Docker → Execute Step 1
