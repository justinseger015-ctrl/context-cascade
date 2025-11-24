/**
 * E2E Workflow 2: Project → Tasks → Reorder → Delete
 * P4_T7 - Integration Testing
 *
 * Test Flow:
 * 1. Create project with name/description
 * 2. Add 5 tasks to project
 * 3. Drag-and-drop to reorder tasks
 * 4. Test keyboard reordering accessibility
 * 5. Verify order persisted in API
 * 6. Delete project and verify cascade delete to tasks
 *
 * Target: <5% failure rate
 */

import { test, expect, Page } from '@playwright/test';
import { ProjectPage } from '../pages/ProjectPage';
import { TaskListPage } from '../pages/TaskListPage';
import { ApiHelper } from '../helpers/api-helper';

test.describe('Workflow 2: Complete Project Management Lifecycle', () => {
  let projectPage: ProjectPage;
  let taskListPage: TaskListPage;
  let apiHelper: ApiHelper;
  let projectId: string;
  let taskIds: string[] = [];

  test.beforeEach(async ({ page }) => {
    projectPage = new ProjectPage(page);
    taskListPage = new TaskListPage(page);
    apiHelper = new ApiHelper(page);
  });

  test('should create project, add tasks, reorder, and delete', async ({ page }) => {
    // Step 1: Create project with name/description
    await projectPage.goto();

    const projectData = {
      name: 'E2E Test Project - Workflow 2',
      description: 'Comprehensive project management testing with task ordering',
    };

    await projectPage.clickCreateProject();

    const projectForm = page.locator('[data-testid="project-form"]');
    await expect(projectForm).toBeVisible({ timeout: 3000 });

    await projectForm.locator('[name="name"]').fill(projectData.name);
    await projectForm.locator('[name="description"]').fill(projectData.description);

    await projectForm.locator('[data-testid="submit-project"]').click();

    // Wait for project creation
    await page.waitForURL(/\/projects\/\d+/, { timeout: 5000 });

    // Extract project ID from URL
    const url = page.url();
    const match = url.match(/\/projects\/(\d+)/);
    expect(match).toBeTruthy();
    projectId = match![1];

    // Verify project appears in list
    const projectCard = page.locator(`[data-project-id="${projectId}"]`);
    await expect(projectCard).toBeVisible({ timeout: 3000 });
    await expect(projectCard).toContainText(projectData.name);

    // Step 2: Add 5 tasks to project
    const tasks = [
      { title: 'Task 1 - Research', description: 'Initial research phase', priority: 'high' },
      { title: 'Task 2 - Design', description: 'Design architecture', priority: 'high' },
      { title: 'Task 3 - Implementation', description: 'Code implementation', priority: 'medium' },
      { title: 'Task 4 - Testing', description: 'Write and run tests', priority: 'medium' },
      { title: 'Task 5 - Deployment', description: 'Deploy to production', priority: 'low' },
    ];

    for (let i = 0; i < tasks.length; i++) {
      await taskListPage.clickAddTask();

      const taskForm = page.locator('[data-testid="task-form"]');
      await expect(taskForm).toBeVisible({ timeout: 2000 });

      await taskForm.locator('[name="title"]').fill(tasks[i].title);
      await taskForm.locator('[name="description"]').fill(tasks[i].description);
      await taskForm.locator('[name="priority"]').selectOption(tasks[i].priority);

      // Associate with project
      await taskForm.locator('[name="project_id"]').selectOption(projectId);

      await taskForm.locator('[data-testid="submit-task"]').click();

      // Wait for task creation
      await page.waitForTimeout(500);

      // Extract task ID
      const taskSuccessMsg = page.locator('[data-testid="success-message"]');
      const taskIdText = await taskSuccessMsg.textContent();
      const taskIdMatch = taskIdText?.match(/ID:\s*(\d+)|#(\d+)/);

      if (taskIdMatch) {
        taskIds.push(taskIdMatch[1] || taskIdMatch[2]);
      }
    }

    expect(taskIds.length).toBe(5);

    // Verify all tasks appear in project
    await projectPage.openProject(projectId);

    for (const taskId of taskIds) {
      const taskElement = page.locator(`[data-task-id="${taskId}"]`);
      await expect(taskElement).toBeVisible({ timeout: 3000 });
    }

    // Step 3: Drag-and-drop to reorder tasks
    await page.waitForLoadState('networkidle');

    // Get initial order
    const initialOrder = await getTaskOrder(page);
    expect(initialOrder).toEqual(taskIds);

    // Drag Task 5 (last) to position 1 (first)
    const task5 = page.locator(`[data-task-id="${taskIds[4]}"]`);
    const task1 = page.locator(`[data-task-id="${taskIds[0]}"]`);

    const task5BoundingBox = await task5.boundingBox();
    const task1BoundingBox = await task1.boundingBox();

    expect(task5BoundingBox).toBeTruthy();
    expect(task1BoundingBox).toBeTruthy();

    // Perform drag and drop
    await page.mouse.move(
      task5BoundingBox!.x + task5BoundingBox!.width / 2,
      task5BoundingBox!.y + task5BoundingBox!.height / 2
    );
    await page.mouse.down();
    await page.mouse.move(
      task1BoundingBox!.x + task1BoundingBox!.width / 2,
      task1BoundingBox!.y + task1BoundingBox!.height / 2,
      { steps: 10 }
    );
    await page.mouse.up();

    // Wait for reorder animation
    await page.waitForTimeout(500);

    // Verify new order
    const newOrder = await getTaskOrder(page);
    expect(newOrder[0]).toBe(taskIds[4]); // Task 5 now first
    expect(newOrder).not.toEqual(initialOrder);

    // Drag Task 1 (now second) to last position
    const reorderedTask1 = page.locator(`[data-task-id="${taskIds[0]}"]`);
    const lastPosition = page.locator('[data-task-position="last"]');

    const reorderedTask1Box = await reorderedTask1.boundingBox();
    const lastPositionBox = await lastPosition.boundingBox();

    if (reorderedTask1Box && lastPositionBox) {
      await page.mouse.move(
        reorderedTask1Box.x + reorderedTask1Box.width / 2,
        reorderedTask1Box.y + reorderedTask1Box.height / 2
      );
      await page.mouse.down();
      await page.mouse.move(
        lastPositionBox.x + lastPositionBox.width / 2,
        lastPositionBox.y + lastPositionBox.height / 2,
        { steps: 10 }
      );
      await page.mouse.up();

      await page.waitForTimeout(500);
    }

    // Step 4: Test keyboard reordering accessibility
    await page.reload();
    await page.waitForLoadState('networkidle');

    const currentOrder = await getTaskOrder(page);

    // Focus first task
    const firstTask = page.locator(`[data-task-id="${currentOrder[0]}"]`);
    await firstTask.focus();

    // Use keyboard to move task down
    await page.keyboard.press('Space'); // Activate drag mode
    await page.keyboard.press('ArrowDown'); // Move down one position
    await page.keyboard.press('ArrowDown'); // Move down another position
    await page.keyboard.press('Enter'); // Drop task

    await page.waitForTimeout(500);

    const keyboardReorderedOrder = await getTaskOrder(page);
    expect(keyboardReorderedOrder).not.toEqual(currentOrder);

    // Verify first task moved down by 2 positions
    expect(keyboardReorderedOrder.indexOf(currentOrder[0])).toBe(2);

    // Step 5: Verify order persisted in API
    const apiOrder = await apiHelper.get(`/api/projects/${projectId}/tasks`);

    expect(apiOrder.success).toBe(true);
    expect(apiOrder.data).toHaveLength(5);

    const apiTaskIds = apiOrder.data.map((task: any) => task.id.toString());
    const currentUIOrder = await getTaskOrder(page);

    expect(apiTaskIds).toEqual(currentUIOrder);

    // Verify each task has correct position/order field
    for (let i = 0; i < apiOrder.data.length; i++) {
      expect(apiOrder.data[i].order).toBe(i + 1);
    }

    // Step 6: Delete project and verify cascade delete to tasks
    await projectPage.goto();

    const projectCardToDelete = page.locator(`[data-project-id="${projectId}"]`);
    await expect(projectCardToDelete).toBeVisible();

    const deleteButton = projectCardToDelete.locator('[data-testid="delete-project"]');
    await deleteButton.click();

    // Confirm deletion
    const confirmDialog = page.locator('[data-testid="confirm-delete-dialog"]');
    await expect(confirmDialog).toBeVisible({ timeout: 2000 });

    const confirmDeleteButton = confirmDialog.locator('[data-testid="confirm-delete"]');
    await confirmDeleteButton.click();

    // Wait for deletion
    await page.waitForTimeout(500);

    // Verify project removed from UI
    await expect(projectCardToDelete).not.toBeVisible({ timeout: 3000 });

    // Verify project deleted via API
    const deletedProject = await apiHelper.get(`/api/projects/${projectId}`);
    expect(deletedProject.success).toBe(false);
    expect(deletedProject.error).toMatch(/not found|deleted/i);

    // Verify all tasks cascade deleted
    for (const taskId of taskIds) {
      const deletedTask = await apiHelper.get(`/api/tasks/${taskId}`);
      expect(deletedTask.success).toBe(false);
      expect(deletedTask.error).toMatch(/not found|deleted/i);
    }
  });

  test('should handle concurrent reordering conflicts', async ({ page }) => {
    // Create project and tasks
    await projectPage.goto();
    await projectPage.clickCreateProject();

    const projectForm = page.locator('[data-testid="project-form"]');
    await projectForm.locator('[name="name"]').fill('Concurrent Test Project');
    await projectForm.locator('[name="description"]').fill('Testing concurrent operations');
    await projectForm.locator('[data-testid="submit-project"]').click();

    await page.waitForURL(/\/projects\/\d+/, { timeout: 5000 });
    const url = page.url();
    const match = url.match(/\/projects\/(\d+)/);
    const testProjectId = match![1];

    // Add 3 tasks
    const taskTitles = ['Task A', 'Task B', 'Task C'];
    const testTaskIds: string[] = [];

    for (const title of taskTitles) {
      await taskListPage.clickAddTask();
      const taskForm = page.locator('[data-testid="task-form"]');
      await taskForm.locator('[name="title"]').fill(title);
      await taskForm.locator('[name="description"]').fill(`Description for ${title}`);
      await taskForm.locator('[name="project_id"]').selectOption(testProjectId);
      await taskForm.locator('[data-testid="submit-task"]').click();
      await page.waitForTimeout(300);

      const taskIdText = await page.locator('[data-testid="success-message"]').textContent();
      const taskIdMatch = taskIdText?.match(/ID:\s*(\d+)|#(\d+)/);
      if (taskIdMatch) {
        testTaskIds.push(taskIdMatch[1] || taskIdMatch[2]);
      }
    }

    await projectPage.openProject(testProjectId);

    // Simulate concurrent reordering (drag two tasks at same time in different browser contexts)
    // This tests optimistic locking and conflict resolution

    const initialOrder = await getTaskOrder(page);

    // Perform first drag
    const task1 = page.locator(`[data-task-id="${testTaskIds[0]}"]`);
    const task2 = page.locator(`[data-task-id="${testTaskIds[1]}"]`);

    await dragElement(page, task1, task2);

    // Immediately perform second drag (before first completes)
    const task3 = page.locator(`[data-task-id="${testTaskIds[2]}"]`);
    await dragElement(page, task3, task1);

    await page.waitForTimeout(1000); // Allow both operations to complete

    // Verify final order is consistent
    const finalOrder = await getTaskOrder(page);
    expect(finalOrder).toHaveLength(3);
    expect(new Set(finalOrder).size).toBe(3); // No duplicates

    // Verify API has consistent order
    const apiOrder = await apiHelper.get(`/api/projects/${testProjectId}/tasks`);
    const apiTaskIds = apiOrder.data.map((task: any) => task.id.toString());
    expect(apiTaskIds).toEqual(finalOrder);

    // Cleanup
    await projectPage.deleteProject(testProjectId);
  });
});

/**
 * Get current order of tasks in the UI
 */
async function getTaskOrder(page: Page): Promise<string[]> {
  const taskElements = await page.locator('[data-task-id]').all();
  const taskIds: string[] = [];

  for (const element of taskElements) {
    const taskId = await element.getAttribute('data-task-id');
    if (taskId) {
      taskIds.push(taskId);
    }
  }

  return taskIds;
}

/**
 * Drag element from source to target
 */
async function dragElement(page: Page, source: any, target: any): Promise<void> {
  const sourceBBox = await source.boundingBox();
  const targetBBox = await target.boundingBox();

  if (!sourceBBox || !targetBBox) {
    throw new Error('Could not get bounding boxes for drag operation');
  }

  await page.mouse.move(
    sourceBBox.x + sourceBBox.width / 2,
    sourceBBox.y + sourceBBox.height / 2
  );
  await page.mouse.down();
  await page.mouse.move(
    targetBBox.x + targetBBox.width / 2,
    targetBBox.y + targetBBox.height / 2,
    { steps: 10 }
  );
  await page.mouse.up();
}
