# Security Audit Quick Reference
## One-Page Cheat Sheet

---

## 🚨 Current Status

| Audit | Status | Action Required |
|-------|--------|-----------------|
| **OWASP API** | ⚠️ Tests Ready | Run tests (backend must be running) |
| **WCAG 2.1 AA** | ⚠️ Tests Ready | Run automated + manual tests |
| **CVE Frontend** | ✅ PASS | Upgrade Vite to 6.4.1 (optional) |
| **CVE Backend** | ✅ PASS | None |
| **Licenses** | ✅ PASS | None |
| **Docker** | ⏳ Pending | Install Trivy |

---

## ⚡ Quick Commands

### Run All Security Tests
```bash
cd /c/Users/17175/ruv-sparc-ui-dashboard/docs/security
bash run-security-audit.sh
```

### OWASP API Testing
```bash
# 1. Start backend
cd backend && docker-compose up -d

# 2. Run OWASP tests
cd ../docs/security
node owasp-api-tests.js
```

### WCAG Accessibility Testing
```bash
# 1. Start frontend
cd frontend && npm run dev

# 2. Run axe-core tests
cd ../docs/security
node wcag-axe-tests.js
```

### CVE Dependency Scans
```bash
# Frontend
cd frontend && npm audit

# Backend
cd backend && pip-audit -r requirements.txt

# Docker (requires Trivy)
trivy image ruv-sparc-backend:latest
```

### Fix Moderate CVE (Vite)
```bash
cd frontend
npm install vite@6.4.1 --save-dev
npm audit fix
```

---

## 📋 OWASP API Top 10 2023 Coverage

| API | Test | Expected |
|-----|------|----------|
| **API1** | Access other user's tasks | 403 Forbidden ✅ |
| **API2** | Expired JWT token | 401 Unauthorized ✅ |
| **API3** | Mass assignment (is_admin=true) | Rejected ✅ |
| **API8** | Rate limiting | HTTP 429 after 100 requests ✅ |
| **API10** | XSS payload `<script>alert("XSS")</script>` | Sanitized ✅ |

**Script**: `/docs/security/owasp-api-tests.js` (478 lines)

---

## ♿ WCAG 2.1 AA Quick Test (30 min)

### 1. Keyboard Navigation (10 min)
- [ ] Tab through entire app (no mouse!)
- [ ] Focus visible on all elements
- [ ] Escape closes modals

### 2. Screen Reader (10 min)
- [ ] Install NVDA: https://www.nvaccess.org/
- [ ] Launch with `Ctrl + Alt + N`
- [ ] Navigate with arrow keys
- [ ] Verify all content is announced

### 3. Color Contrast (5 min)
- [ ] Open Chrome DevTools (F12)
- [ ] Select text element
- [ ] Check contrast ratio ≥ 4.5:1

### 4. Calendar Keyboard (3 min)
- [ ] Tab to calendar
- [ ] Arrow keys navigate dates
- [ ] Space/Enter selects date

### 5. Zoom (2 min)
- [ ] Zoom to 200% (Ctrl +)
- [ ] Verify no horizontal scrolling

**Full Guide**: `/docs/security/WCAG_MANUAL_TESTING_GUIDE.md`

---

## 🛡️ CVE Findings

### Frontend (npm audit)
- ✅ 0 CRITICAL
- ✅ 0 HIGH
- 🟡 2 MODERATE (esbuild/vite - dev only)

**Fix**: `npm install vite@6.4.1 --save-dev`

### Backend (pip-audit)
- ✅ 0 vulnerabilities
- ✅ All packages secure

### Docker (Trivy)
- ⏳ Not scanned (Trivy not installed)

**Install**: `choco install trivy`

---

## 📊 License Compliance

✅ **ALL COMPLIANT**

- ✅ MIT: 494 packages
- ✅ ISC: 50 packages
- ✅ Apache-2.0: 25 packages
- ✅ BSD-3-Clause: 17 packages
- ✅ No GPL/AGPL

**Full Report**: `/docs/security/licenses.json`

---

## 🚀 Production Checklist

### Must Complete Before Deploy

**Security**:
- [ ] OWASP tests PASS (0 CRITICAL/HIGH)
- [ ] Vite upgraded to 6.4.1+
- [ ] Trivy scan PASS (0 CRITICAL/HIGH)
- [ ] Security headers enabled

**Accessibility**:
- [ ] axe-core tests PASS
- [ ] Keyboard navigation works
- [ ] NVDA screen reader tested
- [ ] Color contrast ≥ 4.5:1
- [ ] 200% zoom functional

**Compliance**:
- [ ] Licenses verified
- [ ] Security audit reviewed

---

## 📞 Quick Links

| Resource | Link |
|----------|------|
| **Comprehensive Report** | `/docs/SECURITY_AUDIT_REPORT.md` |
| **OWASP Tests** | `/docs/security/owasp-api-tests.js` |
| **WCAG Tests** | `/docs/security/wcag-axe-tests.js` |
| **Manual Testing Guide** | `/docs/security/WCAG_MANUAL_TESTING_GUIDE.md` |
| **CVE Summary** | `/docs/security/CVE_SCAN_SUMMARY.txt` |
| **Full Audit Script** | `/docs/security/run-security-audit.sh` |

---

## 🔥 Emergency Contacts

- **Report Security Issue**: security@example.com
- **OWASP API Top 10**: https://owasp.org/API-Security/
- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **npm Security**: https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities

---

## 🎯 Priority Matrix

| Issue | Severity | Timeline | Effort |
|-------|----------|----------|--------|
| **OWASP API Testing** | 🔴 HIGH | Before production | 30 min |
| **WCAG Manual Tests** | 🔴 HIGH | Before production | 2-3 hours |
| **Vite Upgrade** | 🟡 MEDIUM | 7 days | 5 min |
| **Trivy Install + Scan** | 🟡 MEDIUM | Before production | 15 min |

---

## 💡 Pro Tips

1. **Automate in CI/CD**:
   ```yaml
   - run: npm audit --audit-level=high
   - run: pip-audit -r requirements.txt
   - run: trivy image ruv-sparc-backend:latest
   ```

2. **Weekly Scans**:
   ```bash
   # Add to cron
   0 9 * * 1 cd /path/to/project && bash docs/security/run-security-audit.sh
   ```

3. **Pre-commit Hook**:
   ```bash
   # .git/hooks/pre-commit
   npm audit --audit-level=high || exit 1
   ```

---

**Last Updated**: November 8, 2024
**Next Audit**: Before production deployment

---

**Quick Reference Card** - Keep this handy! 🚀
