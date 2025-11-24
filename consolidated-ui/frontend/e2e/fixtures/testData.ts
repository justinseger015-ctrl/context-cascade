/**
 * E2E Test Data Fixtures
 * Reusable test data for Playwright tests
 */

import type { Task, Project } from '../../src/types';

export const mockProjects: Project[] = [
  {
    id: 'project-e2e-1',
    name: 'E2E Test Project',
    description: 'Project for end-to-end testing',
    status: 'active',
    taskCount: 0,
    agentCount: 0,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'project-e2e-2',
    name: 'Secondary Project',
    description: 'Another test project',
    status: 'in_progress',
    taskCount: 0,
    agentCount: 0,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
];

export const mockTasks: Task[] = [
  {
    id: 'task-e2e-1',
    projectId: 'project-e2e-1',
    title: 'Test Task 1',
    description: 'First test task',
    status: 'pending',
    priority: 'high',
    skill_name: 'testing',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'task-e2e-2',
    projectId: 'project-e2e-1',
    title: 'Test Task 2',
    description: 'Second test task',
    status: 'running',
    priority: 'medium',
    skill_name: 'development',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'task-e2e-3',
    projectId: 'project-e2e-1',
    title: 'Test Task 3',
    description: 'Third test task',
    status: 'completed',
    priority: 'low',
    skill_name: 'review',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
];

export const createNewTask = (overrides: Partial<Task> = {}): Omit<Task, 'id' | 'createdAt' | 'updatedAt'> => ({
  projectId: 'project-e2e-1',
  title: 'New E2E Task',
  description: 'Created via E2E test',
  status: 'pending',
  priority: 'medium',
  skill_name: 'e2e-testing',
  ...overrides,
});
