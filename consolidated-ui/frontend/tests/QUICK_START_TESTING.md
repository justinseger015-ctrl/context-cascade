# Frontend Testing Quick Start Guide

## 🚀 Quick Commands

### Run All Tests
```bash
# Unit + Integration tests with coverage
npm test -- --coverage

# E2E tests (requires dev server running)
npm run test:e2e

# Watch mode (auto-rerun on changes)
npm run test:watch
```

### View Coverage Report
```bash
# Generate coverage report
npm run test:coverage

# Open HTML report (Windows)
start coverage/index.html

# Open HTML report (macOS/Linux)
open coverage/index.html
```

### Debug Tests
```bash
# Jest debug mode
node --inspect-brk node_modules/.bin/jest --runInBand

# Playwright debug mode
npx playwright test --debug

# Playwright UI mode (interactive)
npx playwright test --ui
```

---

## 📊 What's Tested

### ✅ Unit Tests (47+ tests)
- **Zustand Store Slices**: Tasks, Projects, WebSocket state management
- **Optimistic Updates**: Create, update, delete with automatic rollback
- **Helper Functions**: Filtering, searching, state selectors

### ✅ Integration Tests (10+ tests)
- **Task Creation Workflow**: Form → API → State → Calendar
- **WebSocket Integration**: Real-time updates, reconnection, heartbeat

### ✅ E2E Tests (37+ tests)
- **Calendar Navigation**: Month/week/day views, date navigation
- **Drag & Drop**: Task repositioning with API verification
- **Task Creation**: Full workflow with validation and error handling
- **WebSocket**: Real-time status updates, connection management

**Total**: **70+ comprehensive tests**

---

## 🎯 Coverage Target

**≥90% coverage required**:
- Statements: 90%
- Branches: 90%
- Functions: 90%
- Lines: 90%

---

## 📁 Test File Locations

```
frontend/
├── tests/
│   ├── unit/store/          # Store unit tests
│   ├── integration/         # Workflow integration tests
│   ├── mocks/              # MSW API mocking
│   └── setup.ts            # Test configuration
└── e2e/
    ├── pages/              # Page Object Models
    ├── fixtures/           # Test data
    └── *.spec.ts          # E2E test specs
```

---

## 🛠️ Test Infrastructure

### Frameworks
- **Jest** - Unit & integration testing
- **React Testing Library** - Component testing
- **Playwright** - E2E testing
- **MSW** - API mocking

### Features
- ✅ Optimistic UI updates with rollback
- ✅ WebSocket connection mocking
- ✅ API request interception
- ✅ Cross-browser E2E testing (Chromium, Firefox, WebKit)
- ✅ Accessibility testing (keyboard navigation)

---

## 📝 Writing New Tests

### Unit Test Template
```typescript
import { describe, it, expect, beforeEach } from '@jest/globals';
import { create } from 'zustand';
import { createMySlice, MySlice } from '../../src/store/mySlice';

describe('MySlice', () => {
  let store: ReturnType<typeof create<MySlice>>;

  beforeEach(() => {
    store = create<MySlice>()((...a) => createMySlice(...a));
  });

  it('should have correct initial state', () => {
    const state = store.getState();
    expect(state.myProperty).toBe(expectedValue);
  });
});
```

### E2E Test Template
```typescript
import { test, expect } from '@playwright/test';
import { MyPage } from './pages/MyPage';

test.describe('My Feature', () => {
  let myPage: MyPage;

  test.beforeEach(async ({ page }) => {
    myPage = new MyPage(page);
    await myPage.goto();
  });

  test('should do something', async () => {
    await myPage.performAction();
    await expect(myPage.element).toBeVisible();
  });
});
```

---

## 🐛 Common Issues & Solutions

### Issue: Tests Failing with "Response is not defined"
**Solution**: `whatwg-fetch` polyfill already added to `tests/setup.ts`

### Issue: WebSocket mock not working
**Solution**: Check `tests/setup.ts` has MockWebSocket class setup

### Issue: MSW handlers not intercepting requests
**Solution**: Ensure `server.listen()` called in `beforeAll()` hook

### Issue: E2E tests timing out
**Solution**:
- Increase timeout in test: `test.setTimeout(60000)`
- Check dev server is running: `npm run dev`
- Use `page.waitForLoadState('networkidle')`

---

## 📚 Documentation

- **Full Test Summary**: `tests/TEST_SUMMARY.md`
- **Jest Config**: `jest.config.js`
- **Playwright Config**: `playwright.config.ts`
- **Test Setup**: `tests/setup.ts`

---

## ✨ Best Practices

### 1. Test Structure
- **Arrange**: Set up test data and state
- **Act**: Perform the action being tested
- **Assert**: Verify the expected outcome

### 2. Test Naming
```typescript
// ✅ Good
it('should create task when form submitted with valid data', ...)

// ❌ Bad
it('test task creation', ...)
```

### 3. Async Testing
```typescript
// ✅ Good - wait for API response
await waitFor(() => {
  expect(screen.getByText('Task created')).toBeInTheDocument();
});

// ❌ Bad - might fail due to timing
expect(screen.getByText('Task created')).toBeInTheDocument();
```

### 4. MSW Mocking
```typescript
// ✅ Good - use existing handlers
import { setMockTasks } from '../mocks/handlers';
setMockTasks([mockTask1, mockTask2]);

// ❌ Bad - manually mock fetch
global.fetch = jest.fn().mockResolvedValue(...);
```

---

## 🚨 Pre-Commit Checklist

Before committing code:

1. ✅ Run all tests: `npm test`
2. ✅ Check coverage: `npm run test:coverage`
3. ✅ Ensure ≥90% coverage on new code
4. ✅ Run E2E tests: `npm run test:e2e`
5. ✅ Fix any failing tests
6. ✅ Add tests for new features

---

## 📞 Need Help?

1. **Check test examples**: Look at existing tests in `tests/` and `e2e/`
2. **Read full documentation**: `tests/TEST_SUMMARY.md`
3. **Debug with UI**: `npx playwright test --ui`
4. **Check console output**: Tests show detailed error messages

---

**Status**: ✅ **READY FOR USE**

**Last Updated**: 2024-11-08
