# Contributing to RUV SPARC UI Dashboard

Thank you for your interest in contributing to the RUV SPARC UI Dashboard! This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Commit Message Format](#commit-message-format)
- [Issue Reporting](#issue-reporting)
- [Code Review Guidelines](#code-review-guidelines)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. By participating in this project, you agree to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Reporting Issues

If you experience or witness unacceptable behavior, please contact the project maintainers at support@ruv-sparc.io.

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Node.js**: 18.x or higher
- **Python**: 3.11 or higher
- **Docker**: Latest stable version
- **Git**: Latest stable version
- **PostgreSQL**: 15+ (for local development without Docker)
- **Redis**: 7+ (for local development without Docker)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ruv-sparc-ui-dashboard.git
   cd ruv-sparc-ui-dashboard
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ruvnet/ruv-sparc-ui-dashboard.git
   ```

### Installation

See [DEV_SETUP.md](./DEV_SETUP.md) for detailed development environment setup instructions.

---

## Development Workflow

### Branching Strategy

We follow a **feature branch workflow**:

1. **Main branch** (`main`): Production-ready code
2. **Feature branches**: `feature/your-feature-name`
3. **Bug fix branches**: `fix/bug-description`
4. **Documentation branches**: `docs/documentation-update`

### Creating a Feature Branch

```bash
# Ensure main is up to date
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

### Keeping Your Branch Updated

```bash
# Fetch latest changes from upstream
git fetch upstream

# Rebase your branch on upstream/main
git rebase upstream/main

# Force push to your fork (if already pushed)
git push origin feature/your-feature-name --force-with-lease
```

---

## Code Style Guidelines

### Frontend (React + TypeScript)

We use **ESLint** and **Prettier** for code formatting and linting.

#### Configuration

- **ESLint**: `.eslintrc.cjs` with TypeScript, React, and React Hooks plugins
- **Prettier**: `.prettierrc` with consistent formatting rules

#### Running Linters

```bash
# Frontend directory
cd frontend

# Run ESLint
npm run lint

# Fix auto-fixable issues
npm run lint:fix

# Check Prettier formatting
npm run format:check

# Apply Prettier formatting
npm run format
```

#### TypeScript Style Guide

✅ **DO**:
```typescript
// Use explicit types for function parameters and return types
function createTask(name: string, cronSchedule: string): Task {
  return { name, cronSchedule };
}

// Use interfaces for object shapes
interface Task {
  id: number;
  name: string;
  cronSchedule: string;
}

// Use const assertions for literal types
const TASK_STATUS = {
  PENDING: 'pending',
  RUNNING: 'running',
  COMPLETED: 'completed',
} as const;

// Use strict null checks
function getTask(id: number): Task | null {
  return tasks.find(t => t.id === id) ?? null;
}
```

❌ **DON'T**:
```typescript
// Avoid 'any' type
function processData(data: any) { ... } // BAD

// Avoid non-null assertions unless absolutely necessary
const task = tasks.find(t => t.id === id)!; // BAD

// Avoid implicit 'any' in function parameters
function handleClick(event) { ... } // BAD
```

#### React Component Style

✅ **DO**:
```typescript
// Use functional components with TypeScript
interface TaskCardProps {
  task: Task;
  onDelete: (id: number) => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task, onDelete }) => {
  return (
    <div className="task-card">
      <h3>{task.name}</h3>
      <button onClick={() => onDelete(task.id)}>Delete</button>
    </div>
  );
};

// Use custom hooks for reusable logic
function useTaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTasks().then(setTasks);
  }, []);

  return { tasks, loading };
}
```

❌ **DON'T**:
```typescript
// Avoid class components (prefer functional components)
class TaskCard extends React.Component { ... } // BAD

// Avoid inline styles (use Tailwind CSS classes)
<div style={{ padding: '10px' }}>...</div> // BAD

// Avoid mutating state directly
tasks.push(newTask); // BAD
```

### Backend (Python + FastAPI)

We use **Black** for code formatting and **ruff** for linting.

#### Configuration

- **Black**: `pyproject.toml` with line length 88
- **Ruff**: `pyproject.toml` with comprehensive rule set

#### Running Linters

```bash
# Backend directory
cd backend

# Run Black formatter
black app/

# Check formatting without applying
black --check app/

# Run ruff linter
ruff check app/

# Fix auto-fixable issues
ruff check app/ --fix
```

#### Python Style Guide (PEP 8 + FastAPI Best Practices)

✅ **DO**:
```python
# Use type hints for all function signatures
from typing import List, Optional
from pydantic import BaseModel

async def get_tasks(user_id: str, limit: int = 10) -> List[Task]:
    """
    Retrieve tasks for a user.

    Args:
        user_id: User identifier
        limit: Maximum number of tasks to return

    Returns:
        List of Task objects
    """
    return await db.query(Task).filter_by(user_id=user_id).limit(limit).all()

# Use Pydantic models for request/response validation
class TaskCreate(BaseModel):
    name: str
    schedule_cron: str
    params_json: dict = {}

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Daily backup",
                "schedule_cron": "0 2 * * *",
                "params_json": {"backup_path": "/data"}
            }
        }

# Use dependency injection for database sessions
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ...
```

❌ **DON'T**:
```python
# Avoid missing type hints
def get_tasks(user_id, limit=10): # BAD
    ...

# Avoid direct database access without dependency injection
@router.get("/tasks")
async def get_tasks():
    db = SessionLocal() # BAD
    ...

# Avoid missing docstrings for public functions
async def process_task(task_id): # BAD (no docstring)
    ...

# Avoid bare except clauses
try:
    ...
except: # BAD
    pass
```

#### SQL and Database Best Practices

✅ **DO**:
```python
# Use parameterized queries to prevent SQL injection
from sqlalchemy import select

stmt = select(Task).where(Task.id == task_id)
result = await db.execute(stmt)

# Use proper indexing for performance
from sqlalchemy import Index

__table_args__ = (
    Index('ix_tasks_user_status', 'user_id', 'status'),
)

# Use transactions for atomic operations
async with db.begin():
    await db.execute(update(Task).where(Task.id == task_id).values(status='running'))
    await db.execute(insert(ExecutionResult).values(...))
```

---

## Testing Requirements

### Code Coverage Requirement

**All pull requests must maintain ≥90% test coverage.**

### Running Tests

#### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage

# Run E2E tests (Playwright)
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui
```

#### Backend Tests

```bash
cd backend

# Run all tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_tasks.py

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x
```

### Writing Tests

#### Frontend Testing (Jest + React Testing Library)

```typescript
// tests/TaskCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskCard } from './TaskCard';

describe('TaskCard', () => {
  it('renders task name correctly', () => {
    const task = { id: 1, name: 'Test Task', cronSchedule: '0 * * * *' };
    render(<TaskCard task={task} onDelete={jest.fn()} />);

    expect(screen.getByText('Test Task')).toBeInTheDocument();
  });

  it('calls onDelete when delete button is clicked', () => {
    const onDelete = jest.fn();
    const task = { id: 1, name: 'Test Task', cronSchedule: '0 * * * *' };
    render(<TaskCard task={task} onDelete={onDelete} />);

    fireEvent.click(screen.getByText('Delete'));
    expect(onDelete).toHaveBeenCalledWith(1);
  });
});
```

#### Backend Testing (pytest + httpx)

```python
# tests/test_tasks.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, auth_headers: dict):
    """Test task creation endpoint."""
    payload = {
        "name": "Test Task",
        "schedule_cron": "0 * * * *",
        "params_json": {}
    }

    response = await client.post(
        "/api/v1/tasks",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Task"
    assert data["schedule_cron"] == "0 * * * *"

@pytest.mark.asyncio
async def test_get_task_unauthorized(client: AsyncClient):
    """Test that unauthenticated requests are rejected."""
    response = await client.get("/api/v1/tasks/1")

    assert response.status_code == 401
```

### Test Coverage Thresholds

| Component | Minimum Coverage |
|-----------|-----------------|
| Frontend Components | 90% |
| Frontend Utilities | 95% |
| Backend API Routes | 90% |
| Backend CRUD Operations | 95% |
| Backend Models | 85% |

---

## Pull Request Process

### Before Submitting

1. ✅ **All tests pass** (`npm test` and `pytest`)
2. ✅ **Code coverage ≥90%** (check with `npm run test:coverage` and `pytest --cov`)
3. ✅ **Linting passes** (`npm run lint` and `black --check app/`)
4. ✅ **Type checking passes** (`npm run typecheck`)
5. ✅ **No merge conflicts** with `main` branch
6. ✅ **Commit messages follow convention** (see below)

### Submitting a Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request** on GitHub:
   - Navigate to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template (see below)

3. **PR Title Format**:
   ```
   <type>(<scope>): <short description>

   Examples:
   feat(tasks): Add bulk task deletion
   fix(auth): Resolve JWT token expiration bug
   docs(api): Update API documentation for new endpoints
   ```

### Pull Request Template

```markdown
## Description
<!-- Provide a brief description of the changes -->

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
<!-- Link to related issues: Closes #123, Fixes #456 -->

## Testing
<!-- Describe the tests you added or modified -->
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if applicable)
- [ ] Tests pass locally (`npm test` and `pytest`)
- [ ] Coverage ≥90% (`npm run test:coverage` and `pytest --cov`)
- [ ] No linting errors (`npm run lint` and `black --check app/`)
- [ ] Commit messages follow convention

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->
```

### Code Review Process

1. **Automated checks** must pass (GitHub Actions CI/CD)
2. **At least one approving review** from a maintainer
3. **All comments resolved** before merging
4. **Squash and merge** strategy (for clean commit history)

---

## Commit Message Format

We follow **Conventional Commits** specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, no logic change) |
| `refactor` | Code refactoring (no feature add or bug fix) |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `chore` | Build process or tooling changes |
| `ci` | CI/CD pipeline changes |

### Scopes

| Scope | Description |
|-------|-------------|
| `tasks` | Task scheduling features |
| `projects` | Project management features |
| `agents` | Agent registry features |
| `auth` | Authentication and authorization |
| `api` | API changes |
| `db` | Database schema or migrations |
| `ui` | User interface components |
| `websocket` | Real-time WebSocket features |
| `memory-mcp` | Memory MCP integration |

### Examples

```bash
# Feature commit
git commit -m "feat(tasks): Add bulk task deletion endpoint"

# Bug fix commit
git commit -m "fix(auth): Resolve JWT token expiration after 24 hours"

# Documentation commit
git commit -m "docs(api): Add OpenAPI examples for task endpoints"

# Refactoring commit
git commit -m "refactor(db): Optimize query performance with composite indexes"

# Multi-line commit with body and footer
git commit -m "feat(websocket): Add real-time task status updates

Implement Redis pub/sub for broadcasting task status changes to connected clients.
Includes heartbeat mechanism and automatic reconnection.

Closes #123
Refs #456"
```

### Commit Best Practices

✅ **DO**:
- Use imperative mood: "Add feature" not "Added feature"
- Keep subject line under 72 characters
- Capitalize subject line
- Don't end subject with a period
- Separate subject from body with blank line
- Use body to explain *what* and *why*, not *how*

❌ **DON'T**:
- Commit unrelated changes together
- Use vague messages like "Fix bug" or "Update code"
- Include work-in-progress commits (squash before PR)

---

## Issue Reporting

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check documentation** for common questions
3. **Reproduce the bug** with minimal steps

### Bug Report Template

```markdown
**Bug Description**
A clear and concise description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
A clear description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment**
- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- Browser: [e.g., Chrome 120, Firefox 121]
- Node.js version: [e.g., 18.19.0]
- Python version: [e.g., 3.11.5]

**Additional Context**
Add any other context about the problem here.
```

### Feature Request Template

```markdown
**Feature Description**
A clear and concise description of the feature you'd like.

**Problem to Solve**
Explain the problem this feature would solve.

**Proposed Solution**
Describe how you envision this feature working.

**Alternatives Considered**
Describe alternative solutions you've considered.

**Additional Context**
Add any other context, mockups, or screenshots about the feature request.
```

---

## Code Review Guidelines

### For Authors

- **Keep PRs small** (< 400 lines of code changes)
- **Write clear descriptions** explaining the "why" not just the "what"
- **Respond promptly** to review comments
- **Be open to feedback** and willing to make changes

### For Reviewers

- **Be respectful and constructive**
- **Focus on code quality**, not personal preferences
- **Explain the reasoning** behind suggestions
- **Approve quickly** if changes are minor
- **Test the changes** locally for complex features

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests cover new functionality
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is acceptable
- [ ] Documentation updated (if needed)
- [ ] Breaking changes are documented

---

## Questions?

If you have questions about contributing, please:

1. **Check the documentation** in the `docs/` directory
2. **Search existing issues** on GitHub
3. **Ask in discussions** on GitHub Discussions
4. **Contact maintainers** at support@ruv-sparc.io

---

Thank you for contributing to RUV SPARC UI Dashboard! 🚀

**Last Updated**: 2025-11-08
**Version**: 1.0.0
