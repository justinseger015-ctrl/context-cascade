/**
 * Dashboard Page Object for E2E Testing
 */

import { Page, Locator } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly executionResults: Locator;
  readonly agentActivity: Locator;

  constructor(page: Page) {
    this.page = page;
    this.executionResults = page.locator('[data-testid="execution-results"]');
    this.agentActivity = page.locator('[data-testid="agent-activity"]');
  }

  async goto(): Promise<void> {
    await this.page.goto('/dashboard');
    await this.page.waitForLoadState('networkidle');
  }

  async getExecutionResult(taskId: string): Promise<Locator> {
    return this.page.locator(`[data-execution-task-id="${taskId}"]`).first();
  }
}
