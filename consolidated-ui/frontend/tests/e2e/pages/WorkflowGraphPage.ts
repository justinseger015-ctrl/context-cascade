/**
 * Workflow Graph Page Object for E2E Testing
 */

import { Page, Locator } from '@playwright/test';

export class WorkflowGraphPage {
  readonly page: Page;
  readonly graphContainer: Locator;
  readonly zoomInButton: Locator;
  readonly zoomOutButton: Locator;
  readonly resetViewButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.graphContainer = page.locator('[data-testid="workflow-graph-container"]');
    this.zoomInButton = page.locator('[data-testid="graph-zoom-in"]');
    this.zoomOutButton = page.locator('[data-testid="graph-zoom-out"]');
    this.resetViewButton = page.locator('[data-testid="graph-reset-view"]');
  }

  async goto(): Promise<void> {
    await this.page.goto('/workflow/graph');
    await this.page.waitForLoadState('networkidle');
  }

  async getNode(nodeId: string): Promise<Locator> {
    return this.page.locator(`[data-graph-node-id="${nodeId}"]`);
  }

  async getEdge(fromId: string, toId: string): Promise<Locator> {
    return this.page.locator(`[data-edge-from="${fromId}"][data-edge-to="${toId}"]`);
  }

  async clickNode(nodeId: string): Promise<void> {
    const node = await this.getNode(nodeId);
    await node.click();
  }

  async zoomIn(): Promise<void> {
    await this.zoomInButton.click();
    await this.page.waitForTimeout(300);
  }

  async zoomOut(): Promise<void> {
    await this.zoomOutButton.click();
    await this.page.waitForTimeout(300);
  }

  async resetView(): Promise<void> {
    await this.resetViewButton.click();
    await this.page.waitForTimeout(300);
  }
}
