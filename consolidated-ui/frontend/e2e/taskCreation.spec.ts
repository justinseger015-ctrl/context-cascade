/**
 * E2E Tests - Task Creation End-to-End Flow
 * Tests complete task creation workflow from form to calendar display
 */

import { test, expect } from '@playwright/test';
import { TaskFormPage } from './pages/TaskFormPage';
import { CalendarPage } from './pages/CalendarPage';
import { createNewTask } from './fixtures/testData';

test.describe('Task Creation Workflow', () => {
  let taskFormPage: TaskFormPage;

  test.beforeEach(async ({ page }) => {
    taskFormPage = new TaskFormPage(page);
    await taskFormPage.goto();
  });

  test('should create a new task successfully', async ({ page }) => {
    const newTask = createNewTask({
      title: 'E2E Test Task',
      description: 'Created via Playwright E2E test',
      priority: 'high',
    });

    await taskFormPage.createTask(newTask);

    // Wait for redirect to task list or calendar
    await page.waitForURL(/\/(tasks|calendar)/, { timeout: 5000 });

    // Verify success message
    const successMessage = page.locator('[data-testid="success-message"]');
    await expect(successMessage).toBeVisible({ timeout: 3000 });
    await expect(successMessage).toContainText(/created successfully/i);
  });

  test('should validate required fields', async ({ page }) => {
    // Try to submit empty form
    await taskFormPage.submitForm();

    // Verify validation errors appear
    expect(await taskFormPage.hasValidationError('title')).toBe(true);
    expect(await taskFormPage.hasValidationError('description')).toBe(true);

    const titleError = await taskFormPage.getValidationError('title');
    expect(titleError).toContain('required');
  });

  test('should show validation error for too short title', async ({ page }) => {
    await taskFormPage.fillTaskForm({
      title: 'AB', // Too short (assuming min 3 chars)
      description: 'Valid description',
    });

    await taskFormPage.submitForm();

    const titleError = await taskFormPage.getValidationError('title');
    expect(titleError).toMatch(/minimum|at least|too short/i);
  });

  test('should allow canceling task creation', async ({ page }) => {
    await taskFormPage.fillTaskForm({
      title: 'Canceled Task',
      description: 'This will be canceled',
    });

    await taskFormPage.cancelForm();

    // Verify redirected away from form
    await page.waitForURL(/^((?!\/tasks\/new).)*$/, { timeout: 3000 });

    // Verify we're back at previous page
    expect(page.url()).not.toContain('/tasks/new');
  });

  test('should persist form data while typing', async ({ page }) => {
    const title = 'Persistent Task Title';
    const description = 'This description should persist';

    await taskFormPage.titleInput.fill(title);
    await taskFormPage.descriptionInput.fill(description);

    // Verify values are retained
    await expect(taskFormPage.titleInput).toHaveValue(title);
    await expect(taskFormPage.descriptionInput).toHaveValue(description);
  });

  test('should display created task in calendar', async ({ page }) => {
    const newTask = createNewTask({
      title: 'Calendar Visible Task',
      description: 'Should appear in calendar',
    });

    await taskFormPage.createTask(newTask);

    // Navigate to calendar
    const calendarPage = new CalendarPage(page);
    await calendarPage.goto();

    // Wait for calendar to load
    await page.waitForLoadState('networkidle');

    // Verify task appears in calendar
    const taskInCalendar = page.locator('text=Calendar Visible Task');
    await expect(taskInCalendar).toBeVisible({ timeout: 5000 });
  });

  test('should handle server error gracefully', async ({ page }) => {
    // Intercept API request and force error
    await page.route('**/api/tasks', (route) => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ success: false, error: 'Server error' }),
      });
    });

    const newTask = createNewTask();
    await taskFormPage.createTask(newTask);

    // Verify error message displayed
    const errorMessage = page.locator('[data-testid="error-message"]');
    await expect(errorMessage).toBeVisible({ timeout: 3000 });
    await expect(errorMessage).toContainText(/error|failed/i);

    // Verify form is still visible (not redirected)
    await expect(taskFormPage.formContainer).toBeVisible();
  });

  test('should sanitize user input to prevent XSS', async ({ page }) => {
    const xssAttempt = '<script>alert("XSS")</script>';

    await taskFormPage.fillTaskForm({
      title: `Task with ${xssAttempt}`,
      description: `Description with ${xssAttempt}`,
    });

    await taskFormPage.submitForm();
    await page.waitForTimeout(1000);

    // Verify script tags are escaped/removed
    const content = await page.content();
    expect(content).not.toContain('<script>alert("XSS")</script>');
    expect(content).toMatch(/&lt;script&gt;|&amp;lt;script&amp;gt;|Task with /);
  });
});

test.describe('Task Priority and Status Selection', () => {
  let taskFormPage: TaskFormPage;

  test.beforeEach(async ({ page }) => {
    taskFormPage = new TaskFormPage(page);
    await taskFormPage.goto();
  });

  test('should select different priority levels', async ({ page }) => {
    const priorities = ['low', 'medium', 'high', 'critical'];

    for (const priority of priorities) {
      await taskFormPage.prioritySelect.selectOption(priority);
      const selectedValue = await taskFormPage.prioritySelect.inputValue();
      expect(selectedValue).toBe(priority);
    }
  });

  test('should select different status values', async ({ page }) => {
    const statuses = ['pending', 'running', 'completed', 'failed'];

    for (const status of statuses) {
      await taskFormPage.statusSelect.selectOption(status);
      const selectedValue = await taskFormPage.statusSelect.inputValue();
      expect(selectedValue).toBe(status);
    }
  });

  test('should have default values for priority and status', async ({ page }) => {
    const defaultPriority = await taskFormPage.prioritySelect.inputValue();
    const defaultStatus = await taskFormPage.statusSelect.inputValue();

    expect(defaultPriority).toBeTruthy();
    expect(defaultStatus).toBeTruthy();
  });
});
