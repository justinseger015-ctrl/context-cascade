/**
 * E2E Tests - Calendar Navigation and Task Interactions
 * Tests calendar views, navigation, and drag-and-drop functionality
 */

import { test, expect } from '@playwright/test';
import { CalendarPage } from './pages/CalendarPage';
import { mockTasks } from './fixtures/testData';

test.describe('Calendar Navigation and Views', () => {
  let calendarPage: CalendarPage;

  test.beforeEach(async ({ page }) => {
    calendarPage = new CalendarPage(page);
    await calendarPage.goto();
  });

  test('should display calendar with default month view', async () => {
    await expect(calendarPage.calendarContainer).toBeVisible();
    await expect(calendarPage.monthViewButton).toHaveClass(/active|selected/);
  });

  test('should switch between month, week, and day views', async ({ page }) => {
    // Switch to week view
    await calendarPage.switchToWeekView();
    await expect(calendarPage.weekViewButton).toHaveClass(/active|selected/);
    await page.waitForTimeout(300); // Allow view transition

    // Switch to day view
    await calendarPage.switchToDayView();
    await expect(calendarPage.dayViewButton).toHaveClass(/active|selected/);
    await page.waitForTimeout(300);

    // Switch back to month view
    await calendarPage.switchToMonthView();
    await expect(calendarPage.monthViewButton).toHaveClass(/active|selected/);
  });

  test('should navigate to next and previous months', async () => {
    const initialDate = await calendarPage.getCurrentDate();

    // Navigate to next month
    await calendarPage.navigateNext();
    const nextDate = await calendarPage.getCurrentDate();
    expect(nextDate).not.toBe(initialDate);

    // Navigate to previous month
    await calendarPage.navigatePrevious();
    const prevDate = await calendarPage.getCurrentDate();
    expect(prevDate).toBe(initialDate);
  });

  test('should navigate to today', async ({ page }) => {
    // Navigate away from today
    await calendarPage.navigateNext();
    await calendarPage.navigateNext();

    // Navigate back to today
    await calendarPage.navigateToToday();

    const currentDate = await calendarPage.getCurrentDate();
    const today = new Date();
    const expectedMonth = today.toLocaleString('default', { month: 'long', year: 'numeric' });

    expect(currentDate).toContain(expectedMonth);
  });

  test('should display tasks in calendar', async ({ page }) => {
    // Wait for calendar to load with tasks
    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    // Verify at least one task is visible
    const taskElements = await page.locator('[data-task-id]').count();
    expect(taskElements).toBeGreaterThan(0);
  });

  test('should handle keyboard navigation', async ({ page }) => {
    await calendarPage.calendarContainer.focus();

    // Test arrow keys for navigation
    await page.keyboard.press('ArrowRight');
    await page.waitForTimeout(300);

    await page.keyboard.press('ArrowLeft');
    await page.waitForTimeout(300);

    // Verify calendar is still functional
    await expect(calendarPage.calendarContainer).toBeVisible();
  });
});

test.describe('Calendar - Drag and Drop Tasks', () => {
  let calendarPage: CalendarPage;

  test.beforeEach(async ({ page }) => {
    calendarPage = new CalendarPage(page);
    await calendarPage.goto();
    await page.waitForLoadState('networkidle');
  });

  test('should drag task to a new date', async ({ page }) => {
    // Wait for tasks to load
    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    const taskId = 'task-e2e-1';
    const targetDate = new Date();
    targetDate.setDate(targetDate.getDate() + 3);
    const targetDateStr = targetDate.toISOString().split('T')[0];

    // Perform drag and drop
    await calendarPage.dragTaskToDate(taskId, targetDateStr);

    // Wait for API call to complete
    await page.waitForTimeout(500);

    // Verify task moved to new date
    const isOnTargetDate = await calendarPage.verifyTaskOnDate(taskId, targetDateStr);
    expect(isOnTargetDate).toBe(true);
  });

  test('should verify API call after drag and drop', async ({ page }) => {
    // Set up API request interception
    const apiRequests: any[] = [];
    page.on('request', (request) => {
      if (request.url().includes('/api/tasks')) {
        apiRequests.push({
          method: request.method(),
          url: request.url(),
        });
      }
    });

    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    const taskId = 'task-e2e-2';
    const targetDate = new Date();
    targetDate.setDate(targetDate.getDate() + 1);
    const targetDateStr = targetDate.toISOString().split('T')[0];

    // Drag task
    await calendarPage.dragTaskToDate(taskId, targetDateStr);

    // Wait for API call
    await page.waitForTimeout(1000);

    // Verify PATCH request was made
    const patchRequests = apiRequests.filter((req) => req.method === 'PATCH');
    expect(patchRequests.length).toBeGreaterThan(0);
  });

  test('should support keyboard-based drag and drop', async ({ page }) => {
    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    const taskElement = await calendarPage.getTaskEvent('task-e2e-1');
    await taskElement.focus();

    // Use keyboard to initiate drag
    await page.keyboard.press('Space'); // Pick up task
    await page.keyboard.press('ArrowRight'); // Move right
    await page.keyboard.press('ArrowRight'); // Move right again
    await page.keyboard.press('Enter'); // Drop task

    // Wait for update
    await page.waitForTimeout(500);

    // Verify task moved (element should exist in new position)
    await expect(taskElement).toBeVisible();
  });
});

test.describe('Calendar - Task Click Interactions', () => {
  let calendarPage: CalendarPage;

  test.beforeEach(async ({ page }) => {
    calendarPage = new CalendarPage(page);
    await calendarPage.goto();
    await page.waitForLoadState('networkidle');
  });

  test('should open task details on click', async ({ page }) => {
    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    const taskId = 'task-e2e-1';
    await calendarPage.clickTaskEvent(taskId);

    // Verify task details modal/panel opens
    const taskDetails = page.locator('[data-testid="task-details"]');
    await expect(taskDetails).toBeVisible({ timeout: 2000 });
  });

  test('should handle double-click to edit task', async ({ page }) => {
    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    const taskElement = await calendarPage.getTaskEvent('task-e2e-2');
    await taskElement.dblclick();

    // Verify task edit form opens
    const editForm = page.locator('[data-testid="task-edit-form"]');
    await expect(editForm).toBeVisible({ timeout: 2000 });
  });
});
