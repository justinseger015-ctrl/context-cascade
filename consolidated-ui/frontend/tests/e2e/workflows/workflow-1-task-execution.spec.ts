/**
 * E2E Workflow 1: Task → Calendar → Execute → Result
 * P4_T7 - Integration Testing
 *
 * Test Flow:
 * 1. Fill task form (skill, cron schedule, params)
 * 2. Submit task and verify calendar display
 * 3. Trigger task execution (simulate cron or 'Run now')
 * 4. Wait for WebSocket 'task_status_update' (running → completed)
 * 5. Verify execution result in project dashboard
 * 6. Query Memory MCP for WHO/WHEN/PROJECT/WHY tagging
 *
 * Target: <5% failure rate
 */

import { test, expect, Page } from '@playwright/test';
import { WebSocketHelper } from '../helpers/websocket-helper';
import { MemoryMCPHelper } from '../helpers/memory-mcp-helper';
import { TaskFormPage } from '../pages/TaskFormPage';
import { CalendarPage } from '../pages/CalendarPage';
import { DashboardPage } from '../pages/DashboardPage';

test.describe('Workflow 1: Complete Task Execution Lifecycle', () => {
  let wsHelper: WebSocketHelper;
  let mcpHelper: MemoryMCPHelper;
  let taskFormPage: TaskFormPage;
  let calendarPage: CalendarPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    // Initialize helpers
    wsHelper = new WebSocketHelper(page);
    mcpHelper = new MemoryMCPHelper();
    taskFormPage = new TaskFormPage(page);
    calendarPage = new CalendarPage(page);
    dashboardPage = new DashboardPage(page);

    // Connect WebSocket before starting test
    await wsHelper.connect();
  });

  test.afterEach(async () => {
    // Cleanup
    await wsHelper.disconnect();
  });

  test('should create task, display in calendar, execute, and verify results', async ({ page }) => {
    // Step 1: Fill task form with skill, cron schedule, and params
    await taskFormPage.goto();

    const taskData = {
      skillName: 'test-skill-e2e',
      cronSchedule: '*/5 * * * *', // Every 5 minutes
      params: {
        testParam: 'e2e-test-value',
        retries: 3,
      },
      priority: 'high',
    };

    await taskFormPage.fillTaskForm({
      title: 'E2E Test Task - Workflow 1',
      description: 'Complete end-to-end task execution test',
      skillName: taskData.skillName,
      cronSchedule: taskData.cronSchedule,
      params: JSON.stringify(taskData.params, null, 2),
      priority: taskData.priority,
    });

    // Submit form
    await taskFormPage.submitForm();

    // Wait for redirect to calendar or success message
    await page.waitForURL(/\/(calendar|dashboard)/, { timeout: 5000 });

    const successMessage = page.locator('[data-testid="success-message"]');
    await expect(successMessage).toBeVisible({ timeout: 3000 });

    // Extract task ID from success message or URL
    const taskId = await extractTaskId(page);
    expect(taskId).toBeTruthy();

    // Step 2: Verify task appears in calendar at correct date/time
    await calendarPage.goto();
    await page.waitForLoadState('networkidle');

    // Calculate next run time based on cron (should be within next 5 minutes)
    const now = new Date();
    const expectedMinutes = Math.ceil(now.getMinutes() / 5) * 5;
    const nextRun = new Date(now);
    nextRun.setMinutes(expectedMinutes, 0, 0);

    const nextRunDate = nextRun.toISOString().split('T')[0];

    // Navigate to the date with the scheduled task
    await calendarPage.navigateToDate(nextRun);

    // Verify task is visible in calendar
    const taskInCalendar = page.locator(`[data-task-id="${taskId}"]`);
    await expect(taskInCalendar).toBeVisible({ timeout: 5000 });

    // Verify task details
    await expect(taskInCalendar).toContainText('E2E Test Task');
    await expect(taskInCalendar).toHaveAttribute('data-priority', 'high');

    // Step 3: Trigger task execution (click 'Run now' button)
    await taskInCalendar.click();

    const taskDetailsModal = page.locator('[data-testid="task-details-modal"]');
    await expect(taskDetailsModal).toBeVisible({ timeout: 2000 });

    const runNowButton = taskDetailsModal.locator('[data-testid="run-now-button"]');
    await expect(runNowButton).toBeEnabled();

    // Set up WebSocket listener before triggering execution
    const statusUpdates: any[] = [];
    await wsHelper.onMessage('task_status_update', (data) => {
      if (data.task_id === taskId) {
        statusUpdates.push(data);
      }
    });

    // Trigger execution
    await runNowButton.click();

    // Step 4: Wait for WebSocket status updates (pending → running → completed)
    await page.waitForTimeout(500); // Allow WebSocket to register

    // Verify initial status update (running)
    await wsHelper.waitForMessage('task_status_update', {
      task_id: taskId,
      status: 'running',
    }, 10000);

    expect(statusUpdates.some(u => u.status === 'running')).toBe(true);

    // Wait for completion status
    await wsHelper.waitForMessage('task_status_update', {
      task_id: taskId,
      status: 'completed',
    }, 30000); // Allow up to 30 seconds for task execution

    expect(statusUpdates.some(u => u.status === 'completed')).toBe(true);

    // Step 5: Verify execution result in project dashboard
    await dashboardPage.goto();
    await page.waitForLoadState('networkidle');

    // Find the task execution result
    const executionResult = page.locator(`[data-execution-task-id="${taskId}"]`).first();
    await expect(executionResult).toBeVisible({ timeout: 5000 });

    // Verify result details
    const resultStatus = await executionResult.getAttribute('data-status');
    expect(resultStatus).toBe('completed');

    const resultDuration = await executionResult.locator('[data-testid="execution-duration"]').textContent();
    expect(resultDuration).toBeTruthy();
    expect(parseFloat(resultDuration!)).toBeGreaterThan(0);

    // Verify output is present
    const resultOutput = await executionResult.locator('[data-testid="execution-output"]').textContent();
    expect(resultOutput).toBeTruthy();

    // Step 6: Query Memory MCP to verify WHO/WHEN/PROJECT/WHY tagging
    const memoryTags = await mcpHelper.queryTaskExecution(taskId);

    // Verify WHO tag
    expect(memoryTags.who).toBeTruthy();
    expect(memoryTags.who).toMatch(/agent|user|system/i);

    // Verify WHEN tag
    expect(memoryTags.when).toBeTruthy();
    const executionTime = new Date(memoryTags.when);
    expect(executionTime.getTime()).toBeGreaterThan(now.getTime());
    expect(executionTime.getTime()).toBeLessThan(Date.now());

    // Verify PROJECT tag
    expect(memoryTags.project).toBeTruthy();
    expect(memoryTags.project).toContain('ruv-sparc');

    // Verify WHY tag
    expect(memoryTags.why).toBeTruthy();
    expect(memoryTags.why).toMatch(/implementation|testing|execution/i);

    // Verify all required metadata
    expect(memoryTags).toHaveProperty('task_id', taskId);
    expect(memoryTags).toHaveProperty('skill_name', taskData.skillName);
    expect(memoryTags).toHaveProperty('status', 'completed');
  });

  test('should handle task execution failure gracefully', async ({ page }) => {
    // Create a task designed to fail
    await taskFormPage.goto();

    await taskFormPage.fillTaskForm({
      title: 'Failing Task Test',
      description: 'This task should fail',
      skillName: 'intentional-failure-skill',
      cronSchedule: '0 0 * * *',
      params: JSON.stringify({ shouldFail: true }),
    });

    await taskFormPage.submitForm();
    await page.waitForURL(/\/(calendar|dashboard)/, { timeout: 5000 });

    const taskId = await extractTaskId(page);

    // Navigate to calendar and trigger execution
    await calendarPage.goto();
    const taskElement = page.locator(`[data-task-id="${taskId}"]`);
    await taskElement.click();

    const runNowButton = page.locator('[data-testid="run-now-button"]');

    // Set up WebSocket listener
    await wsHelper.onMessage('task_status_update', (data) => {
      console.log('Status update:', data);
    });

    await runNowButton.click();

    // Wait for failure status
    await wsHelper.waitForMessage('task_status_update', {
      task_id: taskId,
      status: 'failed',
    }, 30000);

    // Verify error message in dashboard
    await dashboardPage.goto();
    const executionResult = page.locator(`[data-execution-task-id="${taskId}"]`).first();

    const errorMessage = await executionResult.locator('[data-testid="execution-error"]').textContent();
    expect(errorMessage).toBeTruthy();
    expect(errorMessage).toContain('failed');

    // Verify Memory MCP recorded the failure
    const memoryTags = await mcpHelper.queryTaskExecution(taskId);
    expect(memoryTags.status).toBe('failed');
    expect(memoryTags.error).toBeTruthy();
  });

  test('should support keyboard navigation for task execution', async ({ page }) => {
    // Create task via keyboard
    await taskFormPage.goto();

    // Tab through form fields
    await page.keyboard.press('Tab');
    await page.keyboard.type('Keyboard Nav Task');

    await page.keyboard.press('Tab');
    await page.keyboard.type('Testing keyboard accessibility');

    await page.keyboard.press('Tab');
    await page.keyboard.type('keyboard-test-skill');

    await page.keyboard.press('Tab');
    await page.keyboard.type('0 12 * * *');

    // Submit with Enter
    await page.keyboard.press('Tab'); // Focus submit button
    await page.keyboard.press('Enter');

    await page.waitForURL(/\/(calendar|dashboard)/, { timeout: 5000 });
    const taskId = await extractTaskId(page);

    // Navigate calendar with keyboard
    await calendarPage.goto();
    const taskElement = page.locator(`[data-task-id="${taskId}"]`);
    await taskElement.focus();

    // Open details with Enter
    await page.keyboard.press('Enter');

    const taskDetailsModal = page.locator('[data-testid="task-details-modal"]');
    await expect(taskDetailsModal).toBeVisible();

    // Navigate to run button with Tab
    const runNowButton = page.locator('[data-testid="run-now-button"]');
    await runNowButton.focus();

    // Execute with Space
    await page.keyboard.press('Space');

    // Verify execution started
    await wsHelper.waitForMessage('task_status_update', {
      task_id: taskId,
      status: 'running',
    }, 10000);
  });
});

/**
 * Extract task ID from page URL or success message
 */
async function extractTaskId(page: Page): Promise<string> {
  // Try URL first
  const url = page.url();
  const urlMatch = url.match(/task[s]?\/(\d+)/);
  if (urlMatch) {
    return urlMatch[1];
  }

  // Try success message
  const successMessage = page.locator('[data-testid="success-message"]');
  const messageText = await successMessage.textContent();
  const messageMatch = messageText?.match(/ID:\s*(\d+)|#(\d+)/);
  if (messageMatch) {
    return messageMatch[1] || messageMatch[2];
  }

  // Try data attribute
  const taskIdAttr = await page.getAttribute('[data-task-id]', 'data-task-id');
  if (taskIdAttr) {
    return taskIdAttr;
  }

  throw new Error('Could not extract task ID from page');
}
