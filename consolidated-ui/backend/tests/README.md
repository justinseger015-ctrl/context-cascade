# Backend Testing Suite - P2_T8

Comprehensive test suite for the RUV SPARC UI Dashboard backend, achieving ≥90% code coverage using pytest and pytest-asyncio.

## 📁 Test Structure

```
tests/
├── conftest.py                      # Shared fixtures and configuration
├── unit/                            # Unit tests (mocked dependencies)
│   ├── test_crud_project.py        # Project CRUD operations
│   ├── test_crud_agent.py          # Agent CRUD operations
│   ├── test_crud_task.py           # Task CRUD operations
│   └── test_crud_execution.py      # Execution result CRUD
├── integration/                     # Integration tests (real database)
│   ├── test_api_projects.py        # Projects API endpoints
│   ├── test_api_agents.py          # Agents API endpoints
│   └── test_api_tasks.py           # Tasks API endpoints
├── websocket/                       # WebSocket tests
│   ├── test_websocket_connection.py # Connection lifecycle
│   ├── test_heartbeat.py           # Heartbeat mechanism
│   └── test_message_types.py       # Message type validation
└── circuit_breaker/                 # Circuit breaker tests
    └── test_memory_mcp_circuit_breaker.py # Memory MCP fallback
```

## 🚀 Running Tests

### Prerequisites

1. **Install test dependencies:**
   ```bash
   pip install -r requirements-test.txt
   ```

2. **Set up test database (Docker):**
   ```bash
   docker-compose -f docker-compose.test.yml up -d
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env.test
   # Edit .env.test with test database credentials
   ```

### Run All Tests

```bash
# Run complete test suite with coverage
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Run Specific Test Categories

```bash
# Unit tests only (fast, mocked dependencies)
pytest -m unit

# Integration tests only (real database)
pytest -m integration

# WebSocket tests only
pytest -m websocket

# Circuit breaker tests only
pytest -m circuit_breaker

# Performance tests (slow)
pytest -m performance

# Concurrent operation tests
pytest -m concurrent
```

### Run Specific Test Files

```bash
# Test specific CRUD module
pytest tests/unit/test_crud_project.py

# Test specific API endpoints
pytest tests/integration/test_api_projects.py

# Test WebSocket connections
pytest tests/websocket/test_websocket_connection.py
```

### Run Tests in Parallel

```bash
# Use all CPU cores
pytest -n auto

# Use specific number of workers
pytest -n 4
```

## 📊 Coverage Requirements

This test suite maintains **≥90% code coverage** across all modules:

### View Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Coverage by Module

- **CRUD Operations**: ≥95% coverage
- **API Endpoints**: ≥90% coverage
- **WebSocket**: ≥90% coverage
- **Circuit Breaker**: ≥85% coverage
- **Utilities**: ≥90% coverage

## 🧪 Test Categories

### 1. Unit Tests (`tests/unit/`)

**London School TDD approach with mocked dependencies**

- ✅ Fast execution (< 1ms per test)
- ✅ Isolated from external dependencies
- ✅ Test business logic thoroughly
- ✅ Mock database, Redis, Memory MCP

**Example:**
```python
async def test_create_project_success(mock_db_session, sample_project_data):
    result = await create_project(mock_db_session, sample_project_data)
    assert result.name == sample_project_data["name"]
    mock_db_session.commit.assert_called_once()
```

### 2. Integration Tests (`tests/integration/`)

**Tests with real PostgreSQL + Redis in Docker**

- ✅ Real database transactions
- ✅ API endpoint validation
- ✅ Response schema verification
- ✅ Authorization checks

**Example:**
```python
async def test_create_project_endpoint(client, sample_project_data):
    response = await client.post("/api/v1/projects", json=sample_project_data)
    assert response.status_code == 201
    assert "id" in response.json()
```

### 3. WebSocket Tests (`tests/websocket/`)

**Connection lifecycle, heartbeat, and reconnection**

- ✅ Connection establishment
- ✅ Message send/receive
- ✅ Heartbeat ping-pong
- ✅ Disconnection handling
- ✅ Reconnection scenarios

**Example:**
```python
async def test_websocket_heartbeat(websocket_manager, mock_websocket):
    await websocket_manager.connect(mock_websocket, "client-1")
    # Test heartbeat mechanism
```

### 4. Circuit Breaker Tests (`tests/circuit_breaker/`)

**Memory MCP failure simulation and recovery**

- ✅ Circuit state transitions (CLOSED → OPEN → HALF_OPEN)
- ✅ Failure threshold detection
- ✅ Fallback mode activation
- ✅ Recovery after timeout
- ✅ Concurrent failure handling

**Example:**
```python
async def test_circuit_opens_after_threshold(memory_client):
    # Trigger 5 failures
    assert memory_client.circuit_state == "OPEN"
    assert memory_client.fallback_mode is True
```

## 🔧 Test Fixtures

### Database Fixtures

```python
@pytest_asyncio.fixture
async def db_session():
    """Provides clean database session for each test"""

@pytest_asyncio.fixture
async def client(db_session):
    """Provides HTTP test client with database override"""
```

### Mock Fixtures

```python
@pytest.fixture
def mock_db_session():
    """Mock AsyncSession for unit tests"""

@pytest.fixture
def mock_redis_client():
    """Mock Redis client"""

@pytest.fixture
def mock_memory_mcp_client():
    """Mock Memory MCP client with circuit breaker"""
```

### Sample Data Fixtures

```python
@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""

@pytest.fixture
def sample_agent_data():
    """Sample agent data for testing"""
```

## 📈 Performance Testing

### Benchmarking

```bash
# Run performance benchmarks
pytest -m performance --benchmark-only

# Compare with baseline
pytest -m performance --benchmark-compare
```

### Load Testing

```bash
# Run Locust load tests
locust -f tests/performance/locustfile.py
```

## 🐛 Debugging Tests

### Verbose Output

```bash
# Show print statements
pytest -s

# Show detailed assertion info
pytest -vv

# Show local variables on failure
pytest -l
```

### Debug Specific Test

```bash
# Run single test with debugger
pytest tests/unit/test_crud_project.py::TestProjectCRUD::test_create_project_success -vv
```

### Stop on First Failure

```bash
pytest -x  # Stop on first failure
pytest --maxfail=3  # Stop after 3 failures
```

## 🔄 Concurrent Testing

Tests include concurrent operation scenarios:

- **Race conditions** in YAML writes
- **Database transaction isolation**
- **Multiple WebSocket connections**
- **Circuit breaker state transitions**

```bash
# Run concurrent tests
pytest -m concurrent
```

## 📝 Test Documentation

Each test includes:
- **Docstring** explaining what is tested
- **AAA pattern**: Arrange, Act, Assert
- **Clear assertions** with meaningful messages
- **Fixtures** for setup/teardown

## 🚢 CI/CD Integration

### GitHub Actions Example

```yaml
name: Backend Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt

      - name: Run tests
        run: pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## 📊 Coverage Reports

### Generate Reports

```bash
# HTML report (interactive)
pytest --cov=app --cov-report=html

# Terminal report
pytest --cov=app --cov-report=term-missing

# XML report (for CI)
pytest --cov=app --cov-report=xml

# JSON report
pytest --cov=app --cov-report=json
```

### Coverage Goals

- **Overall**: ≥90%
- **Critical paths**: 100%
- **CRUD operations**: ≥95%
- **API endpoints**: ≥90%
- **Error handling**: ≥85%

## 🎯 Testing Best Practices

1. **Test in isolation**: Each test should be independent
2. **Use fixtures**: Reuse setup code via fixtures
3. **Mock external dependencies**: Unit tests should be fast
4. **Test edge cases**: Include boundary conditions
5. **Test error paths**: Don't just test happy paths
6. **Clear test names**: Describe what is being tested
7. **AAA pattern**: Arrange, Act, Assert structure
8. **Async tests**: Use `@pytest.mark.asyncio` for async code

## 🔍 Common Issues

### Database Connection Errors

```bash
# Ensure test database is running
docker-compose -f docker-compose.test.yml up -d

# Check database connectivity
psql -h localhost -U test -d test_db
```

### WebSocket Test Failures

```bash
# Ensure Redis is running for WebSocket pubsub
docker ps | grep redis
```

### Import Errors

```bash
# Ensure app is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Guide](https://pytest-asyncio.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [TDD London School](https://github.com/testdouble/contributing-tests/wiki/London-school-TDD)

## ✅ Test Completion Checklist

- [x] Unit tests for all CRUD operations
- [x] Integration tests for all API endpoints
- [x] WebSocket connection lifecycle tests
- [x] Circuit breaker and fallback tests
- [x] Concurrent operation tests
- [x] ≥90% code coverage achieved
- [x] CI/CD integration ready
- [x] Documentation complete

---

**Last Updated**: 2024-11-08
**Coverage**: ≥90%
**Test Count**: 150+ tests
**Technology Stack**: pytest, pytest-asyncio, httpx, websockets
