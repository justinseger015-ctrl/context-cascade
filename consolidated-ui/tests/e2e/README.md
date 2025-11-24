# End-to-End Integration Testing Suite

## Overview

Comprehensive E2E testing for ruv-SPARC UI Dashboard using Playwright and Docker Compose.

**Task**: P4_T7 - Integration Testing (End-to-End Workflows)
**Target**: <5% failure rate across all workflows
**Technology**: Playwright v1.56.1 + Docker Compose + PostgreSQL + Redis + Memory MCP

---

## Test Workflows

### Workflow 1: Task → Calendar → Execute → Result

**Location**: `tests/e2e/workflows/workflow-1-task-execution.spec.ts`

**Flow**:
1. Fill task form (skill, cron schedule, params)
2. Submit and verify calendar display at correct date/time
3. Trigger task execution ('Run now' button)
4. Wait for WebSocket status updates (pending → running → completed)
5. Verify execution result in dashboard (output, duration)
6. Query Memory MCP for WHO/WHEN/PROJECT/WHY tagging

**Features Tested**:
- ✅ Task creation with validation
- ✅ Calendar navigation and display
- ✅ Real-time WebSocket status updates
- ✅ Task execution and result verification
- ✅ Memory MCP tagging protocol compliance
- ✅ Keyboard accessibility
- ✅ Error handling for failed tasks

---

### Workflow 2: Project → Tasks → Reorder → Delete

**Location**: `tests/e2e/workflows/workflow-2-project-management.spec.ts`

**Flow**:
1. Create project with name/description
2. Add 5 tasks to project
3. Drag-and-drop to reorder tasks
4. Test keyboard reordering (Space + Arrow keys + Enter)
5. Verify order persisted in API
6. Delete project and verify cascade delete to tasks

**Features Tested**:
- ✅ Project CRUD operations
- ✅ Task association with projects
- ✅ Drag-and-drop reordering (mouse)
- ✅ Keyboard reordering (accessibility)
- ✅ API persistence verification
- ✅ Cascade deletion
- ✅ Concurrent reordering conflict resolution

---

### Workflow 3: Agent Activity → Real-time Feed → Workflow Graph

**Location**: `tests/e2e/workflows/workflow-3-agent-activity.spec.ts`

**Flow**:
1. Spawn 3 agents via hooks (researcher, coder, reviewer)
2. Verify real-time activity feed updates
3. Verify workflow graph shows agent dependencies
4. Test interactive graph features (zoom, pan, node selection)
5. Verify agent status transitions (idle → busy → completed)

**Features Tested**:
- ✅ Agent spawning with capabilities and dependencies
- ✅ Real-time activity feed with WebSocket events
- ✅ Workflow graph visualization (ReactFlow)
- ✅ Agent dependency graph layout
- ✅ Interactive graph controls (zoom, pan, select)
- ✅ Agent status transitions and updates
- ✅ Error handling for agent failures
- ✅ Keyboard navigation accessibility

---

## Architecture

### Docker Compose Test Environment

**File**: `docker-compose.test.yml`

**Services**:
- **postgres-e2e**: PostgreSQL 15 test database (port 5434)
- **redis-e2e**: Redis 7 caching and real-time (port 6381)
- **memory-mcp-e2e**: Memory MCP server with tagging (port 9001)
- **backend-e2e**: FastAPI backend (port 8001)
- **frontend-e2e**: React + Vite frontend (port 3000)
- **playwright-e2e**: Playwright test runner (optional)

**Network**: `e2e-network` (subnet: 172.29.0.0/16)

### Test Helpers

**WebSocket Helper** (`helpers/websocket-helper.ts`):
- Connect to WebSocket server
- Listen for specific message types
- Wait for messages with matching criteria
- Send messages through WebSocket
- Message log and replay

**Memory MCP Helper** (`helpers/memory-mcp-helper.ts`):
- Query task executions from Memory MCP
- Verify WHO/WHEN/PROJECT/WHY tagging protocol
- Store test execution data
- Clear test entries
- Health check

**API Helper** (`helpers/api-helper.ts`):
- Type-safe API interactions
- GET/POST/PATCH/DELETE requests
- Response validation
- Wait for API readiness

### Page Objects

**Page Object Pattern** (`pages/*.ts`):
- `ProjectPage`: Project CRUD operations
- `TaskListPage`: Task management
- `CalendarPage`: Calendar navigation and interactions
- `DashboardPage`: Execution results and metrics
- `AgentActivityPage`: Agent monitoring and activity feed
- `WorkflowGraphPage`: Interactive workflow graph

---

## Running Tests

### Prerequisites

```bash
# Install dependencies
cd frontend
npm install

# Install Playwright browsers
npx playwright install
```

### Quick Start (Docker Compose)

```bash
# Start Docker Compose test environment
docker-compose -f docker-compose.test.yml up -d

# Run E2E tests
cd frontend
npm run test:e2e:workflows

# Stop Docker Compose
docker-compose -f docker-compose.test.yml down -v
```

### One-Command (with auto-cleanup)

```bash
cd frontend
npm run test:e2e:docker
```

### Test Commands

```bash
# Run all E2E workflow tests
npm run test:e2e:workflows

# Run with UI mode (interactive)
npm run test:e2e:ui

# Run in debug mode (step through)
npm run test:e2e:debug

# Run headed (see browser)
npm run test:e2e:headed

# Run specific browser
npm run test:e2e:chromium
npm run test:e2e:firefox
npm run test:e2e:webkit

# View test report
npm run test:e2e:report
```

### Running Specific Tests

```bash
# Single workflow
npx playwright test workflow-1-task-execution

# Single test
npx playwright test -g "should create task, display in calendar"

# Update snapshots
npx playwright test --update-snapshots
```

---

## Configuration

### Playwright Config

**File**: `playwright.config.e2e.ts`

**Key Settings**:
- **testDir**: `./tests/e2e/workflows`
- **timeout**: 60 seconds per test
- **retries**: 1 locally, 2 in CI
- **workers**: 4 locally, 2 in CI
- **browsers**: Chromium, Firefox, WebKit, Mobile Chrome, Mobile Safari
- **reporters**: HTML, JSON, JUnit, List

### Environment Variables

```bash
# Backend API URL
E2E_BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000

# WebSocket URL
WS_URL=ws://localhost:8000/ws

# Memory MCP URL
MEMORY_MCP_URL=http://localhost:9001

# Database
DATABASE_URL=postgresql://e2e_test_user:e2e_test_pass@localhost:5434/e2e_test_db

# Redis
REDIS_URL=redis://localhost:6381
```

---

## Global Setup & Teardown

### Global Setup (`global-setup.ts`)

**Runs before all tests**:
1. Wait for services (Backend, Frontend, Memory MCP)
2. Run database migrations
3. Seed test data
4. Clear Memory MCP short-term layer

### Global Teardown (`global-teardown.ts`)

**Runs after all tests**:
1. Clean test data from database
2. Clear Memory MCP test entries
3. Generate test summary

---

## Test Data

### Fixtures (`fixtures/test-data.ts`)

**Pre-defined test data**:
- `testProjects`: Sample project data
- `testTasks`: Sample task data
- `testAgents`: Sample agent configurations

**Dynamic generation**:
```typescript
import { generateUniqueTestData } from './fixtures/test-data';

const { project, task, agent } = generateUniqueTestData('E2E');
```

---

## Quality Metrics

### Target: <5% Failure Rate

**Achieved through**:
- ✅ Explicit waits (no arbitrary timeouts)
- ✅ Proper WebSocket event handling
- ✅ Retries for flaky tests
- ✅ Isolated test data (no shared state)
- ✅ Health checks before tests
- ✅ Global setup/teardown
- ✅ Error recovery and cleanup

### Test Reliability Features

**Stability improvements**:
- `waitForLoadState('networkidle')` before interactions
- `waitForSelector` with explicit timeouts
- WebSocket message polling (100ms intervals)
- API readiness checks (30s timeout)
- Service health checks with retries

**Isolation**:
- Unique test data per test run
- Short-term Memory MCP layer (auto-cleanup)
- Docker Compose network isolation
- Separate test database (port 5434)

---

## Debugging

### Debug Mode

```bash
# Run with Playwright Inspector
npm run test:e2e:debug
```

**Features**:
- Step through test execution
- Inspect DOM and selectors
- View browser console logs
- Take screenshots at any step

### Headed Mode

```bash
# See browser while tests run
npm run test:e2e:headed
```

### Trace Viewer

```bash
# Run test with trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

### Screenshots and Videos

**Automatically captured**:
- Screenshots on failure
- Videos on first retry
- Traces on first retry

**Location**: `test-results/`

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Start Docker Compose
        run: docker-compose -f docker-compose.test.yml up -d

      - name: Install dependencies
        run: cd frontend && npm ci

      - name: Run E2E tests
        run: cd frontend && npm run test:e2e:workflows

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: frontend/playwright-report/

      - name: Stop Docker Compose
        if: always()
        run: docker-compose -f docker-compose.test.yml down -v
```

---

## Memory MCP Tagging Protocol

### Required Tags (WHO/WHEN/PROJECT/WHY)

**All Memory MCP writes must include**:
```typescript
{
  who: "agent-name or user-id",
  when: "2025-11-08T19:00:00Z", // ISO 8601 timestamp
  project: "ruv-sparc-ui-dashboard",
  why: "implementation | testing | bugfix | refactor | analysis"
}
```

### Verification

```typescript
import { MemoryMCPHelper } from './helpers/memory-mcp-helper';

const mcpHelper = new MemoryMCPHelper();
const tags = await mcpHelper.queryTaskExecution(taskId);

// Verify WHO tag
expect(tags.who).toBeTruthy();

// Verify WHEN tag
expect(new Date(tags.when).getTime()).toBeGreaterThan(0);

// Verify PROJECT tag
expect(tags.project).toBe('ruv-sparc-ui-dashboard');

// Verify WHY tag
expect(tags.why).toMatch(/implementation|testing|execution/i);
```

---

## Troubleshooting

### Services not ready

**Error**: "Backend API did not become ready within 60000ms"

**Fix**:
```bash
# Check Docker Compose status
docker-compose -f docker-compose.test.yml ps

# Check service logs
docker-compose -f docker-compose.test.yml logs backend-e2e

# Restart services
docker-compose -f docker-compose.test.yml restart
```

### WebSocket connection failed

**Error**: "WebSocket connection failed"

**Fix**:
```bash
# Verify backend WebSocket endpoint
curl http://localhost:8000/ws

# Check firewall rules
# Ensure port 8000 is accessible
```

### Memory MCP not found

**Error**: "Memory MCP health check failed"

**Fix**:
```bash
# Check Memory MCP logs
docker-compose -f docker-compose.test.yml logs memory-mcp-e2e

# Verify Memory MCP is running
curl http://localhost:9001/health
```

### Database connection issues

**Error**: "Database connection refused"

**Fix**:
```bash
# Check PostgreSQL status
docker-compose -f docker-compose.test.yml logs postgres-e2e

# Verify port 5434 is available
netstat -an | grep 5434
```

---

## Best Practices

### ✅ DO

- Use explicit waits with `waitForSelector`, `waitForLoadState`
- Use page objects for complex interactions
- Use unique test data with timestamps
- Clean up test data after each test
- Use WebSocket helpers for real-time events
- Verify API persistence for critical operations
- Test keyboard accessibility
- Handle errors gracefully

### ❌ DON'T

- Use arbitrary `waitForTimeout` (flaky)
- Share test data between tests (race conditions)
- Use hardcoded IDs or indexes
- Rely on implicit waits
- Skip cleanup in `afterEach`
- Test without Docker Compose (missing services)
- Assume services are ready (use health checks)

---

## File Structure

```
tests/e2e/
├── workflows/
│   ├── workflow-1-task-execution.spec.ts     # Workflow 1 tests
│   ├── workflow-2-project-management.spec.ts # Workflow 2 tests
│   └── workflow-3-agent-activity.spec.ts     # Workflow 3 tests
├── helpers/
│   ├── websocket-helper.ts                   # WebSocket utilities
│   ├── memory-mcp-helper.ts                  # Memory MCP integration
│   └── api-helper.ts                         # API client
├── pages/
│   ├── ProjectPage.ts                        # Project page object
│   ├── TaskListPage.ts                       # Task list page object
│   ├── CalendarPage.ts                       # Calendar page object
│   ├── DashboardPage.ts                      # Dashboard page object
│   ├── AgentActivityPage.ts                  # Agent activity page object
│   └── WorkflowGraphPage.ts                  # Workflow graph page object
├── fixtures/
│   └── test-data.ts                          # Test data generators
├── global-setup.ts                           # Global setup
├── global-teardown.ts                        # Global teardown
└── README.md                                 # This file
```

---

## Support

**Issues**: Create issue in repository with:
- Test failure screenshot
- Test output log
- Docker Compose logs
- Browser console errors

**Contact**: See main README for project maintainers

---

**Last Updated**: 2025-11-08
**Version**: 1.0.0
**Task**: P4_T7 - Integration Testing (End-to-End Workflows)
