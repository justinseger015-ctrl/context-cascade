/**
 * Page Object Model - Calendar Page
 * Encapsulates calendar interactions for E2E tests
 */

import { Page, Locator } from '@playwright/test';

export class CalendarPage {
  readonly page: Page;
  readonly calendarContainer: Locator;
  readonly monthViewButton: Locator;
  readonly weekViewButton: Locator;
  readonly dayViewButton: Locator;
  readonly prevButton: Locator;
  readonly nextButton: Locator;
  readonly todayButton: Locator;
  readonly currentDateDisplay: Locator;

  constructor(page: Page) {
    this.page = page;
    this.calendarContainer = page.locator('[data-testid="calendar-container"]');
    this.monthViewButton = page.locator('[data-testid="view-month"]');
    this.weekViewButton = page.locator('[data-testid="view-week"]');
    this.dayViewButton = page.locator('[data-testid="view-day"]');
    this.prevButton = page.locator('[data-testid="nav-prev"]');
    this.nextButton = page.locator('[data-testid="nav-next"]');
    this.todayButton = page.locator('[data-testid="nav-today"]');
    this.currentDateDisplay = page.locator('[data-testid="current-date"]');
  }

  async goto() {
    await this.page.goto('/calendar');
  }

  async switchToMonthView() {
    await this.monthViewButton.click();
  }

  async switchToWeekView() {
    await this.weekViewButton.click();
  }

  async switchToDayView() {
    await this.dayViewButton.click();
  }

  async navigateNext() {
    await this.nextButton.click();
  }

  async navigatePrevious() {
    await this.prevButton.click();
  }

  async navigateToToday() {
    await this.todayButton.click();
  }

  async getCurrentDate(): Promise<string> {
    return await this.currentDateDisplay.textContent() || '';
  }

  async getTaskEvent(taskId: string): Promise<Locator> {
    return this.page.locator(`[data-task-id="${taskId}"]`);
  }

  async clickTaskEvent(taskId: string) {
    const event = await this.getTaskEvent(taskId);
    await event.click();
  }

  async dragTaskToDate(taskId: string, targetDate: string) {
    const taskElement = await this.getTaskEvent(taskId);
    const targetCell = this.page.locator(`[data-date="${targetDate}"]`);

    await taskElement.hover();
    await this.page.mouse.down();
    await targetCell.hover();
    await this.page.mouse.up();
  }

  async verifyTaskOnDate(taskId: string, expectedDate: string): Promise<boolean> {
    const taskElement = await this.getTaskEvent(taskId);
    const dateCell = this.page.locator(`[data-date="${expectedDate}"]`);

    const taskBox = await taskElement.boundingBox();
    const cellBox = await dateCell.boundingBox();

    if (!taskBox || !cellBox) return false;

    // Check if task is within date cell boundaries
    return (
      taskBox.x >= cellBox.x &&
      taskBox.x + taskBox.width <= cellBox.x + cellBox.width &&
      taskBox.y >= cellBox.y &&
      taskBox.y + taskBox.height <= cellBox.y + cellBox.height
    );
  }
}
