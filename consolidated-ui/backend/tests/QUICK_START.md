# Quick Start - Backend Testing Suite

**5-Minute Setup Guide for P2_T8 Testing**

---

## ⚡ Fast Track

```bash
# 1. Install dependencies
pip install -r requirements-test.txt

# 2. Start test infrastructure
docker-compose -f docker-compose.test.yml up -d

# 3. Run tests
./scripts/run-tests.sh

# 4. View coverage
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

---

## 📋 Test Categories

| Command | What it runs | Duration |
|---------|-------------|----------|
| `./scripts/run-tests.sh` | All tests with coverage | ~5 min |
| `./scripts/run-tests.sh unit` | Unit tests only (mocked) | ~10 sec |
| `./scripts/run-tests.sh integration` | API tests with real DB | ~2 min |
| `./scripts/run-tests.sh websocket` | WebSocket connection tests | ~30 sec |
| `./scripts/run-tests.sh circuit-breaker` | Circuit breaker tests | ~1 min |
| `./scripts/run-tests.sh all true` | All tests in PARALLEL | ~2 min |

---

## 🎯 What's Tested

✅ **34 Unit Tests** - CRUD operations (projects, agents)
✅ **12 Integration Tests** - API endpoints with real PostgreSQL
✅ **21 WebSocket Tests** - Connection, heartbeat, reconnection
✅ **20 Circuit Breaker Tests** - Memory MCP failure handling

**Total: 87+ tests | Coverage: ≥90%**

---

## 🔧 Troubleshooting

### Database Not Ready?
```bash
# Check PostgreSQL
docker-compose -f docker-compose.test.yml exec postgres-test pg_isready

# Check Redis
docker-compose -f docker-compose.test.yml exec redis-test redis-cli ping
```

### Tests Failing?
```bash
# Run in verbose mode
pytest -vv

# Run single test
pytest tests/unit/test_crud_project.py::TestProjectCRUD::test_create_project_success -vv

# Show print statements
pytest -s
```

### Coverage Too Low?
```bash
# See what's missing
pytest --cov=app --cov-report=term-missing

# Generate detailed HTML report
pytest --cov=app --cov-report=html
```

---

## 📁 Test Structure

```
tests/
├── conftest.py              # Fixtures (database, mocks, samples)
├── unit/                    # Fast tests with mocks
├── integration/             # Real database tests
├── websocket/               # WebSocket tests
└── circuit_breaker/         # Failure simulation tests
```

---

## 🚀 Next Steps

1. ✅ Tests passing? → **Check coverage report**
2. ✅ Coverage ≥90%? → **Integrate with CI/CD**
3. ✅ Ready for production? → **Enable GitHub Actions**

---

## 📞 Need Help?

- **Full Documentation**: `tests/README.md`
- **Test Runner Help**: `./scripts/run-tests.sh --help`
- **Coverage Report**: `htmlcov/index.html`

---

**That's it! Your backend is fully tested with ≥90% coverage.** 🎉
