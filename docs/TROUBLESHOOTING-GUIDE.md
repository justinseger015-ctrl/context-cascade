# Troubleshooting Guide

## Backend Issues

### Backend Won't Start

**Symptom**: `uvicorn` command fails or crashes

**Solutions**:

1. Check Python version:
   ```bash
   python --version  # Should be 3.9+
   ```

2. Install dependencies:
   ```bash
   cd backend && pip install -r requirements.txt
   ```

3. Check port 8000 availability:
   ```bash
   lsof -i :8000  # Kill process if occupied
   ```

4. Check logs:
   ```bash
   cat /tmp/backend.log
   ```

### Database Connection Errors

**Symptom**: "Database disconnected" in /health

**Solutions**:

1. Check database file:
   ```bash
   ls agent-reality-map-backend.db
   ```

2. Recreate database:
   ```bash
   cd backend && python -c "from app.database import init_db; init_db()"
   ```

3. Check permissions:
   ```bash
   chmod 644 agent-reality-map-backend.db
   ```

### API Returns 500 Errors

**Symptom**: All endpoints return 500

**Solutions**:

1. Check backend logs:
   ```bash
   tail -f /tmp/backend.log
   ```

2. Check database integrity:
   ```bash
   sqlite3 agent-reality-map-backend.db "PRAGMA integrity_check;"
   ```

3. Restart backend with --reload:
   ```bash
   cd backend && uvicorn app.main:app --reload
   ```

---

## Frontend Issues

### Frontend Won't Load

**Symptom**: Blank page or build errors

**Solutions**:

1. Check Node version:
   ```bash
   node --version  # Should be 16+
   ```

2. Install dependencies:
   ```bash
   cd frontend && npm install
   ```

3. Clear Next.js cache:
   ```bash
   rm -rf .next && npm run dev
   ```

4. Check port 3000:
   ```bash
   lsof -i :3000  # Kill process if occupied
   ```

### Module Not Found Errors

**Symptom**: `Cannot find module '@/...'`

**Solutions**:

1. Check tsconfig/jsconfig path aliases:
   ```json
   {
     "compilerOptions": {
       "paths": {
         "@/*": ["./src/*"]
       }
     }
   }
   ```

2. Restart dev server:
   ```bash
   npm run dev
   ```

### WebSocket Connection Fails

**Symptom**: "WebSocket connection failed" in console

**Solutions**:

1. Check backend WebSocket endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

2. Test WebSocket manually:
   ```bash
   node -e "const ws=require('ws'); const c=new ws('ws://localhost:8000/ws'); c.on('open',()=>console.log('OK')); c.on('error',(e)=>console.log('FAIL:',e.message));"
   ```

3. Check CORS configuration (backend/app/main.py:36-42)

---

## RBAC Issues

### Agent Operations Blocked

**Symptom**: "Permission denied" in audit log

**Solutions**:

1. Check agent identity:
   ```bash
   cat hooks/12fa/.identity-store.json | jq '.agents["agent-name"]'
   ```

2. Check role permissions:
   ```bash
   cat agents/identity/agent-rbac-rules.json | jq '.roles["role-name"]'
   ```

3. Check allowed tools match operation

4. Review audit log:
   ```bash
   grep "agent-name" hooks/12fa/.audit-trail.log | tail
   ```

### Budget Exceeded

**Symptom**: "Agent daily budget exceeded"

**Solutions**:

1. Check current usage:
   ```bash
   grep "agent-name" hooks/12fa/.audit-trail.log | grep budget
   ```

2. Increase budget in `.identity-store.json`:
   ```json
   {
     "budget": {
       "max_tokens_per_session": 200000,
       "max_cost_per_day": 50.0
     }
   }
   ```

3. Wait for daily reset (midnight UTC)

---

## Performance Issues

### Slow API Responses

**Symptom**: Requests take >1 second

**Solutions**:

1. Enable caching (see Phase 5.2 docs):
   - Apply registry caching
   - Enable permission caching

2. Check database size:
   ```bash
   ls -lh agent-reality-map-backend.db
   ```

3. Add database indexes:
   ```sql
   CREATE INDEX idx_agent_role ON agents(role);
   CREATE INDEX idx_events_agent ON events(agent);
   ```

4. Monitor with `--log-level debug`:
   ```bash
   uvicorn app.main:app --log-level debug
   ```

### High Memory Usage

**Symptom**: Backend using >1GB RAM

**Solutions**:

1. Check cache size:
   ```bash
   node -e "const {cache} = require('./backend/app/cache.py'); console.log(cache.size())"
   ```

2. Clear cache:
   ```python
   from backend.app.cache import cache
   cache.clear()
   ```

3. Reduce cache TTL in cache.py

---

## Common Errors

### "Module 'backend.app' has no attribute 'main'"

**Fix**: Ensure running from correct directory:
```bash
cd /path/to/project && python -m uvicorn backend.app.main:app
```

### "WebSocket 403 Forbidden"

**Fix**: Add type annotation (already fixed in main.py:112)
```python
async def websocket_endpoint(websocket: WebSocket):
```

### "Cannot find file: /public/tree.json"

**Fix**: Use correct import path in frontend:
```javascript
import treeData from "/public/tree.json";
```

---

## Getting Help

1. **Check Logs**:
   - Backend: `/tmp/backend.log`
   - Frontend: Browser console
   - RBAC: `hooks/12fa/.audit-trail.log`

2. **Test Endpoints**:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/v1/agents/
   ```

3. **Run Tests**:
   ```bash
   node hooks/12fa/tests/test-rbac-pipeline.js
   ```

4. **Check Documentation**:
   - API Docs: http://localhost:8000/docs
   - User Guide: `docs/USER-GUIDE.md`
   - Admin Guide: `docs/ADMIN-GUIDE-RBAC.md`
   - Developer Guide: `docs/DEVELOPER-GUIDE.md`

5. **Review Phase 5 Reports**:
   - Integration Tests: `.claude/.artifacts/phase5-integration-test-report.md`
   - Performance: `.claude/.artifacts/phase52-caching-complete.md`
   - Completion Summary: `.claude/.artifacts/phase5-completion-summary.md`
