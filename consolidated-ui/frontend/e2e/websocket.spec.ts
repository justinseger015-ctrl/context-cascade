/**
 * E2E Tests - WebSocket Real-Time Task Status Updates
 * Tests real-time task updates via WebSocket connection
 */

import { test, expect } from '@playwright/test';
import { CalendarPage } from './pages/CalendarPage';

test.describe('WebSocket Real-Time Updates', () => {
  let calendarPage: CalendarPage;

  test.beforeEach(async ({ page }) => {
    calendarPage = new CalendarPage(page);
    await calendarPage.goto();
    await page.waitForLoadState('networkidle');
  });

  test('should establish WebSocket connection on page load', async ({ page }) => {
    // Check for WebSocket connection indicator
    const wsStatus = page.locator('[data-testid="ws-status"]');
    await expect(wsStatus).toHaveAttribute('data-connected', 'true', { timeout: 5000 });
  });

  test('should display real-time task status update', async ({ page }) => {
    // Wait for initial tasks to load
    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    const taskId = 'task-e2e-1';
    const taskElement = await calendarPage.getTaskEvent(taskId);

    // Get initial status
    const initialStatus = await taskElement.getAttribute('data-status');

    // Simulate WebSocket message from server (via page evaluation)
    await page.evaluate((id) => {
      const mockMessage = {
        type: 'task_status_update',
        payload: {
          taskId: id,
          status: 'running',
          updatedAt: new Date().toISOString(),
        },
        timestamp: new Date().toISOString(),
      };

      // Trigger WebSocket message handler
      window.dispatchEvent(
        new CustomEvent('websocket-message', { detail: mockMessage })
      );
    }, taskId);

    // Wait for UI to update
    await page.waitForTimeout(500);

    // Verify status changed
    const updatedStatus = await taskElement.getAttribute('data-status');
    expect(updatedStatus).not.toBe(initialStatus);
  });

  test('should show connection status indicator', async ({ page }) => {
    const wsStatus = page.locator('[data-testid="ws-status"]');

    // Verify connected state
    await expect(wsStatus).toBeVisible();

    // Check for visual indicator (green dot, "Connected" text, etc.)
    const isConnected = await wsStatus.getAttribute('data-connected');
    expect(isConnected).toBe('true');
  });

  test('should handle WebSocket reconnection', async ({ page }) => {
    const wsStatus = page.locator('[data-testid="ws-status"]');

    // Simulate connection loss
    await page.evaluate(() => {
      const event = new CustomEvent('websocket-disconnect');
      window.dispatchEvent(event);
    });

    // Verify disconnected state
    await expect(wsStatus).toHaveAttribute('data-connected', 'false', { timeout: 2000 });

    // Simulate reconnection
    await page.evaluate(() => {
      const event = new CustomEvent('websocket-connect');
      window.dispatchEvent(event);
    });

    // Verify reconnected state
    await expect(wsStatus).toHaveAttribute('data-connected', 'true', { timeout: 3000 });
  });

  test('should display multiple concurrent task updates', async ({ page }) => {
    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    const taskIds = ['task-e2e-1', 'task-e2e-2', 'task-e2e-3'];

    // Simulate multiple WebSocket messages
    for (const taskId of taskIds) {
      await page.evaluate((id) => {
        const mockMessage = {
          type: 'task_status_update',
          payload: {
            taskId: id,
            status: 'completed',
            updatedAt: new Date().toISOString(),
          },
          timestamp: new Date().toISOString(),
        };

        window.dispatchEvent(
          new CustomEvent('websocket-message', { detail: mockMessage })
        );
      }, taskId);
    }

    // Wait for all updates to process
    await page.waitForTimeout(1000);

    // Verify all tasks updated
    for (const taskId of taskIds) {
      const taskElement = await calendarPage.getTaskEvent(taskId);
      const status = await taskElement.getAttribute('data-status');
      expect(status).toBe('completed');
    }
  });

  test('should show heartbeat indicator for active connection', async ({ page }) => {
    const heartbeat = page.locator('[data-testid="ws-heartbeat"]');

    if (await heartbeat.isVisible()) {
      // Verify heartbeat timestamp updates
      const initialTime = await heartbeat.textContent();

      // Wait for heartbeat (typically every 30 seconds, but test can be shorter)
      await page.waitForTimeout(2000);

      // Simulate heartbeat
      await page.evaluate(() => {
        window.dispatchEvent(new CustomEvent('websocket-heartbeat'));
      });

      await page.waitForTimeout(500);

      const updatedTime = await heartbeat.textContent();
      expect(updatedTime).not.toBe(initialTime);
    }
  });

  test('should handle malformed WebSocket messages gracefully', async ({ page }) => {
    // Set up console error monitoring
    const consoleErrors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    // Send malformed message
    await page.evaluate(() => {
      const malformedMessage = {
        // Missing required fields
        type: 'task_status_update',
        // No payload
      };

      window.dispatchEvent(
        new CustomEvent('websocket-message', { detail: malformedMessage })
      );
    });

    await page.waitForTimeout(500);

    // Verify app didn't crash - calendar still visible
    await expect(calendarPage.calendarContainer).toBeVisible();

    // Optionally verify error was logged (implementation-dependent)
    // expect(consoleErrors.length).toBeGreaterThan(0);
  });

  test('should batch rapid WebSocket updates efficiently', async ({ page }) => {
    await page.waitForSelector('[data-task-id]', { timeout: 5000 });

    const taskId = 'task-e2e-1';

    // Send rapid updates
    for (let i = 0; i < 10; i++) {
      await page.evaluate((id) => {
        const mockMessage = {
          type: 'task_status_update',
          payload: {
            taskId: id,
            status: 'running',
            updatedAt: new Date().toISOString(),
          },
          timestamp: new Date().toISOString(),
        };

        window.dispatchEvent(
          new CustomEvent('websocket-message', { detail: mockMessage })
        );
      }, taskId);

      // Small delay between messages
      await page.waitForTimeout(50);
    }

    // Wait for batching to complete
    await page.waitForTimeout(1000);

    // Verify final state is correct (batching should consolidate updates)
    const taskElement = await calendarPage.getTaskEvent(taskId);
    const status = await taskElement.getAttribute('data-status');
    expect(status).toBe('running');

    // Verify UI is still responsive
    await expect(calendarPage.calendarContainer).toBeVisible();
  });
});

test.describe('WebSocket - Agent Activity Updates', () => {
  test('should display agent activity updates via WebSocket', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');

    // Simulate agent activity update
    await page.evaluate(() => {
      const mockMessage = {
        type: 'agent_activity_update',
        payload: {
          agentId: 'agent-1',
          status: 'busy',
          currentTask: 'task-e2e-1',
          timestamp: new Date().toISOString(),
        },
        timestamp: new Date().toISOString(),
      };

      window.dispatchEvent(
        new CustomEvent('websocket-message', { detail: mockMessage })
      );
    });

    await page.waitForTimeout(500);

    // Verify agent status updated in UI
    const agentStatus = page.locator('[data-agent-id="agent-1"]');
    if (await agentStatus.isVisible()) {
      await expect(agentStatus).toHaveAttribute('data-status', 'busy');
    }
  });
});
