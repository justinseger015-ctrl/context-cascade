/**
 * Agent Activity Page Object for E2E Testing
 */

import { Page, Locator } from '@playwright/test';

export class AgentActivityPage {
  readonly page: Page;
  readonly spawnAgentButton: Locator;
  readonly activityFeed: Locator;

  constructor(page: Page) {
    this.page = page;
    this.spawnAgentButton = page.locator('[data-testid="spawn-agent-button"]');
    this.activityFeed = page.locator('[data-testid="activity-feed"]');
  }

  async goto(): Promise<void> {
    await this.page.goto('/agents/activity');
    await this.page.waitForLoadState('networkidle');
  }

  async clickSpawnAgent(): Promise<void> {
    await this.spawnAgentButton.click();
    await this.page.waitForTimeout(300);
  }

  async getActivityEvent(eventType: string, agentId?: string): Promise<Locator> {
    if (agentId) {
      return this.page.locator(
        `[data-event-type="${eventType}"][data-agent-id="${agentId}"]`
      );
    }
    return this.page.locator(`[data-event-type="${eventType}"]`);
  }
}
