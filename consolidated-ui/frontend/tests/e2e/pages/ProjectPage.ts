/**
 * Project Page Object for E2E Testing
 */

import { Page, Locator } from '@playwright/test';

export class ProjectPage {
  readonly page: Page;
  readonly createProjectButton: Locator;
  readonly projectList: Locator;

  constructor(page: Page) {
    this.page = page;
    this.createProjectButton = page.locator('[data-testid="create-project-button"]');
    this.projectList = page.locator('[data-testid="project-list"]');
  }

  async goto(): Promise<void> {
    await this.page.goto('/projects');
    await this.page.waitForLoadState('networkidle');
  }

  async clickCreateProject(): Promise<void> {
    await this.createProjectButton.click();
  }

  async openProject(projectId: string): Promise<void> {
    const projectCard = this.page.locator(`[data-project-id="${projectId}"]`);
    await projectCard.click();
    await this.page.waitForLoadState('networkidle');
  }

  async deleteProject(projectId: string): Promise<void> {
    const projectCard = this.page.locator(`[data-project-id="${projectId}"]`);
    const deleteButton = projectCard.locator('[data-testid="delete-project"]');
    await deleteButton.click();

    const confirmDialog = this.page.locator('[data-testid="confirm-delete-dialog"]');
    const confirmButton = confirmDialog.locator('[data-testid="confirm-delete"]');
    await confirmButton.click();

    await this.page.waitForTimeout(500);
  }
}
