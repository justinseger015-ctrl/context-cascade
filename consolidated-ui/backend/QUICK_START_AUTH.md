# 🚀 Quick Start: Multi-User Authentication

## ⚡ 3-Minute Integration

### Step 1: Update main.py (2 changes)
```python
# Line 26: Add auth import
from app.routers import tasks, projects, agents, health, auth

# After line 294 (after health.router), add:
app.include_router(
    auth.router,
    tags=["Authentication"]
)
```

### Step 2: Run Database Migration
```bash
cd backend
alembic upgrade head
```

### Step 3: Test Authentication
```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"SecurePass123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"SecurePass123"}'
```

---

## 📚 Full Documentation
- **Integration Guide**: `INTEGRATION_GUIDE.md`
- **Implementation Summary**: `P5_T1_IMPLEMENTATION_SUMMARY.md`
- **API Docs**: http://localhost:8000/api/docs (after integration)

---

## 🔒 Security Features Enabled
✅ Bcrypt password hashing
✅ JWT access tokens (1h expiration)
✅ JWT refresh tokens (7d expiration)
✅ Session management with revocation
✅ Role-based access control (admin/user)
✅ Password strength validation
✅ Device/session tracking

---

## 📋 Available Endpoints
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login with username/password
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout (revoke token)
- `GET /api/v1/auth/me` - Get current user
- `PUT /api/v1/auth/me` - Update profile
- `POST /api/v1/auth/change-password` - Change password
- `GET /api/v1/auth/sessions` - List active sessions
- `DELETE /api/v1/auth/sessions/{id}` - Revoke session

---

## 🎯 Next Steps (Optional)
1. Add `user_id` to existing tables (scheduled_tasks, projects, agents)
2. Update existing routers to use `get_current_user` dependency
3. Generate production JWT secret: `openssl rand -hex 32`
4. Set environment variables for production
