/**
 * Page Object Model - Task Form Page
 * Encapsulates task form interactions for E2E tests
 */

import { Page, Locator } from '@playwright/test';

export class TaskFormPage {
  readonly page: Page;
  readonly titleInput: Locator;
  readonly descriptionInput: Locator;
  readonly statusSelect: Locator;
  readonly prioritySelect: Locator;
  readonly skillNameInput: Locator;
  readonly projectSelect: Locator;
  readonly submitButton: Locator;
  readonly cancelButton: Locator;
  readonly formContainer: Locator;

  constructor(page: Page) {
    this.page = page;
    this.formContainer = page.locator('[data-testid="task-form"]');
    this.titleInput = page.locator('[data-testid="task-title"]');
    this.descriptionInput = page.locator('[data-testid="task-description"]');
    this.statusSelect = page.locator('[data-testid="task-status"]');
    this.prioritySelect = page.locator('[data-testid="task-priority"]');
    this.skillNameInput = page.locator('[data-testid="task-skill"]');
    this.projectSelect = page.locator('[data-testid="task-project"]');
    this.submitButton = page.locator('[data-testid="submit-task"]');
    this.cancelButton = page.locator('[data-testid="cancel-task"]');
  }

  async goto() {
    await this.page.goto('/tasks/new');
  }

  async fillTaskForm(taskData: {
    title: string;
    description: string;
    status?: string;
    priority?: string;
    skillName?: string;
    projectId?: string;
  }) {
    await this.titleInput.fill(taskData.title);
    await this.descriptionInput.fill(taskData.description);

    if (taskData.status) {
      await this.statusSelect.selectOption(taskData.status);
    }

    if (taskData.priority) {
      await this.prioritySelect.selectOption(taskData.priority);
    }

    if (taskData.skillName) {
      await this.skillNameInput.fill(taskData.skillName);
    }

    if (taskData.projectId) {
      await this.projectSelect.selectOption(taskData.projectId);
    }
  }

  async submitForm() {
    await this.submitButton.click();
  }

  async cancelForm() {
    await this.cancelButton.click();
  }

  async createTask(taskData: {
    title: string;
    description: string;
    status?: string;
    priority?: string;
    skillName?: string;
    projectId?: string;
  }) {
    await this.fillTaskForm(taskData);
    await this.submitForm();
  }

  async getValidationError(field: string): Promise<string | null> {
    const errorLocator = this.page.locator(`[data-testid="${field}-error"]`);
    return await errorLocator.textContent();
  }

  async hasValidationError(field: string): Promise<boolean> {
    const errorLocator = this.page.locator(`[data-testid="${field}-error"]`);
    return await errorLocator.isVisible();
  }
}
