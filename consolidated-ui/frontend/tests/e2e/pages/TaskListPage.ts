/**
 * Task List Page Object for E2E Testing
 */

import { Page, Locator } from '@playwright/test';

export class TaskListPage {
  readonly page: Page;
  readonly addTaskButton: Locator;
  readonly taskList: Locator;

  constructor(page: Page) {
    this.page = page;
    this.addTaskButton = page.locator('[data-testid="add-task-button"]');
    this.taskList = page.locator('[data-testid="task-list"]');
  }

  async goto(): Promise<void> {
    await this.page.goto('/tasks');
    await this.page.waitForLoadState('networkidle');
  }

  async clickAddTask(): Promise<void> {
    await this.addTaskButton.click();
    await this.page.waitForTimeout(300);
  }

  async getTaskElement(taskId: string): Promise<Locator> {
    return this.page.locator(`[data-task-id="${taskId}"]`);
  }

  async deleteTask(taskId: string): Promise<void> {
    const taskElement = await this.getTaskElement(taskId);
    const deleteButton = taskElement.locator('[data-testid="delete-task"]');
    await deleteButton.click();

    const confirmDialog = this.page.locator('[data-testid="confirm-delete-dialog"]');
    const confirmButton = confirmDialog.locator('[data-testid="confirm-delete"]');
    await confirmButton.click();

    await this.page.waitForTimeout(300);
  }
}
