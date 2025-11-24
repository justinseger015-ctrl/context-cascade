/**
 * Integration Tests - Task Creation Workflow
 * Tests complete task creation flow: form → API → state → calendar
 */

import { describe, it, expect, beforeEach } from '@jest/globals';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { create } from 'zustand';
import { createTasksSlice, TasksSlice } from '../../src/store/tasksSlice';
import { createProjectsSlice, ProjectsSlice } from '../../src/store/projectsSlice';
import { setMockProjects } from '../mocks/handlers';
import type { Project } from '../../src/types';

// Create a combined store for integration testing
type CombinedStore = TasksSlice & ProjectsSlice;

const createIntegrationStore = () => {
  return create<CombinedStore>()((...a) => ({
    ...createTasksSlice(...a),
    ...createProjectsSlice(...a),
  }));
};

// Mock TaskForm component for testing
const MockTaskForm: React.FC<{ store: ReturnType<typeof createIntegrationStore> }> = ({ store }) => {
  const [title, setTitle] = React.useState('');
  const [description, setDescription] = React.useState('');
  const { addTask, tasks } = store();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await addTask({
      projectId: 'project-1',
      title,
      description,
      status: 'pending',
      priority: 'medium',
      skill_name: 'test-skill',
    });
  };

  return (
    <div>
      <form onSubmit={handleSubmit} data-testid="task-form">
        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          data-testid="task-title-input"
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          data-testid="task-description-input"
        />
        <button type="submit" data-testid="submit-button">
          Create Task
        </button>
      </form>
      <div data-testid="task-list">
        {tasks.map((task) => (
          <div key={task.id} data-testid={`task-${task.id}`}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <span data-testid="task-status">{task.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

describe('Integration: Task Creation Workflow', () => {
  let store: ReturnType<typeof createIntegrationStore>;

  beforeEach(() => {
    store = createIntegrationStore();

    const mockProject: Project = {
      id: 'project-1',
      name: 'Test Project',
      description: 'Test',
      status: 'active',
      taskCount: 0,
      agentCount: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    setMockProjects([mockProject]);
  });

  it('should create task through form and display in list', async () => {
    const user = userEvent.setup();
    render(<MockTaskForm store={store} />);

    // Fill out form
    await user.type(screen.getByTestId('task-title-input'), 'New Integration Test Task');
    await user.type(screen.getByTestId('task-description-input'), 'This tests the full workflow');

    // Submit form
    await user.click(screen.getByTestId('submit-button'));

    // Wait for task to appear in list (after API call completes)
    await waitFor(() => {
      expect(screen.getByText('New Integration Test Task')).toBeInTheDocument();
    });

    // Verify task details
    expect(screen.getByText('This tests the full workflow')).toBeInTheDocument();
    expect(screen.getByTestId('task-status')).toHaveTextContent('pending');

    // Verify store state
    const tasks = store.getState().tasks;
    expect(tasks).toHaveLength(1);
    expect(tasks[0].title).toBe('New Integration Test Task');
    expect(tasks[0].projectId).toBe('project-1');
  });

  it('should handle optimistic updates during task creation', async () => {
    const user = userEvent.setup();
    render(<MockTaskForm store={store} />);

    await user.type(screen.getByTestId('task-title-input'), 'Optimistic Task');
    await user.type(screen.getByTestId('task-description-input'), 'Testing optimistic updates');

    // Submit - task should appear immediately (optimistic)
    const submitPromise = user.click(screen.getByTestId('submit-button'));

    // Task should appear optimistically (before API completes)
    await waitFor(() => {
      expect(screen.getByText('Optimistic Task')).toBeInTheDocument();
    });

    // Wait for API to complete
    await submitPromise;
    await waitFor(() => {
      const tasks = store.getState().tasks;
      expect(tasks[0].id).not.toMatch(/^temp-/); // Real ID from API
    });
  });

  it('should update task list when tasks are fetched', async () => {
    // Pre-populate some tasks via API
    await store.getState().addTask({
      projectId: 'project-1',
      title: 'Existing Task 1',
      description: 'Already exists',
      status: 'pending',
      priority: 'high',
      skill_name: 'test',
    });

    await store.getState().addTask({
      projectId: 'project-1',
      title: 'Existing Task 2',
      description: 'Also exists',
      status: 'completed',
      priority: 'low',
      skill_name: 'test',
    });

    render(<MockTaskForm store={store} />);

    // Verify both tasks are displayed
    await waitFor(() => {
      expect(screen.getByText('Existing Task 1')).toBeInTheDocument();
      expect(screen.getByText('Existing Task 2')).toBeInTheDocument();
    });
  });

  it('should filter tasks by project', async () => {
    const mockProject2: Project = {
      id: 'project-2',
      name: 'Another Project',
      description: 'Test',
      status: 'active',
      taskCount: 0,
      agentCount: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    setMockProjects([mockProject2]);

    await store.getState().addTask({
      projectId: 'project-1',
      title: 'Project 1 Task',
      description: 'For project 1',
      status: 'pending',
      priority: 'medium',
      skill_name: 'test',
    });

    await store.getState().addTask({
      projectId: 'project-2',
      title: 'Project 2 Task',
      description: 'For project 2',
      status: 'pending',
      priority: 'medium',
      skill_name: 'test',
    });

    // Fetch only project-1 tasks
    await store.getState().fetchTasks('project-1');

    const project1Tasks = store.getState().getTasksByProject('project-1');
    expect(project1Tasks).toHaveLength(1);
    expect(project1Tasks[0].title).toBe('Project 1 Task');
  });
});
