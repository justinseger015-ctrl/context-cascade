/**
 * Unit Tests for Tasks Slice (Zustand Store)
 * Tests state updates, persistence, optimistic updates, and rollback logic
 */

import { describe, it, expect, beforeEach, afterEach, vi } from '@jest/globals';
import { create } from 'zustand';
import { createTasksSlice, TasksSlice } from '../../../src/store/tasksSlice';
import { Task } from '../../../src/types';

// Mock fetch globally
global.fetch = vi.fn();

// Helper to create a test store
const createTestStore = () => {
  return create<TasksSlice>()((...a) => createTasksSlice(...a));
};

// Mock task data
const mockTask: Task = {
  id: 'task-1',
  projectId: 'project-1',
  title: 'Test Task',
  description: 'Test Description',
  status: 'pending',
  priority: 'medium',
  skill_name: 'testing',
  createdAt: '2024-01-01T00:00:00.000Z',
  updatedAt: '2024-01-01T00:00:00.000Z',
};

describe('TasksSlice - State Management', () => {
  let store: ReturnType<typeof createTestStore>;

  beforeEach(() => {
    store = createTestStore();
    vi.clearAllMocks();
    (fetch as jest.Mock).mockClear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = store.getState();

      expect(state.tasks).toEqual([]);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.optimisticUpdates.size).toBe(0);
    });
  });

  describe('Helper Methods', () => {
    beforeEach(() => {
      store.setState({ tasks: [mockTask] });
    });

    it('getTaskById should return task when found', () => {
      const task = store.getState().getTaskById('task-1');
      expect(task).toEqual(mockTask);
    });

    it('getTaskById should return undefined when not found', () => {
      const task = store.getState().getTaskById('non-existent');
      expect(task).toBeUndefined();
    });

    it('getTasksByProject should filter tasks by project', () => {
      store.setState({
        tasks: [
          mockTask,
          { ...mockTask, id: 'task-2', projectId: 'project-2' },
        ],
      });

      const tasks = store.getState().getTasksByProject('project-1');
      expect(tasks).toHaveLength(1);
      expect(tasks[0].id).toBe('task-1');
    });

    it('getTasksByStatus should filter tasks by status', () => {
      store.setState({
        tasks: [
          mockTask,
          { ...mockTask, id: 'task-2', status: 'completed' },
        ],
      });

      const tasks = store.getState().getTasksByStatus('pending');
      expect(tasks).toHaveLength(1);
      expect(tasks[0].status).toBe('pending');
    });
  });

  describe('Optimistic Updates - addTask', () => {
    it('should add task optimistically before API call', async () => {
      const taskData = {
        projectId: 'project-1',
        title: 'New Task',
        description: 'New Description',
        status: 'pending' as const,
        priority: 'high' as const,
        skill_name: 'testing',
      };

      // Setup fetch mock to hang (never resolve) so we can test optimistic state
      let resolvePromise: (value: Response) => void;
      (fetch as jest.Mock).mockReturnValue(
        new Promise<Response>((resolve) => {
          resolvePromise = resolve;
        })
      );

      // Start async task creation
      const promise = store.getState().addTask(taskData);

      // Verify optimistic update applied immediately
      await new Promise((resolve) => setTimeout(resolve, 0)); // Let state update
      const state = store.getState();

      expect(state.tasks).toHaveLength(1);
      expect(state.tasks[0].title).toBe('New Task');
      expect(state.tasks[0].id).toMatch(/^temp-/);
      expect(state.optimisticUpdates.size).toBe(1);

      // Cleanup: resolve the promise
      resolvePromise!(
        new Response(
          JSON.stringify({
            success: true,
            data: { ...taskData, id: 'real-1', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
          }),
          { status: 200 }
        )
      );
      await promise.catch(() => {}); // Avoid unhandled promise rejection
    });

    it('should replace optimistic task with real task on success', async () => {
      const taskData = {
        projectId: 'project-1',
        title: 'New Task',
        description: 'New Description',
        status: 'pending' as const,
        priority: 'high' as const,
        skill_name: 'testing',
      };

      const realTask = {
        ...taskData,
        id: 'real-task-id',
        createdAt: '2024-01-01T00:00:00.000Z',
        updatedAt: '2024-01-01T00:00:00.000Z',
      };

      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: true, data: realTask }),
          { status: 200 }
        )
      );

      await store.getState().addTask(taskData);

      const state = store.getState();
      expect(state.tasks).toHaveLength(1);
      expect(state.tasks[0].id).toBe('real-task-id');
      expect(state.optimisticUpdates.size).toBe(0);
      expect(state.error).toBeNull();
    });

    it('should rollback optimistic update on API failure', async () => {
      const taskData = {
        projectId: 'project-1',
        title: 'New Task',
        description: 'New Description',
        status: 'pending' as const,
        priority: 'high' as const,
        skill_name: 'testing',
      };

      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: false, error: 'Server error' }),
          { status: 500 }
        )
      );

      await expect(store.getState().addTask(taskData)).rejects.toThrow();

      const state = store.getState();
      expect(state.tasks).toHaveLength(0);
      expect(state.optimisticUpdates.size).toBe(0);
      expect(state.error).toBe('Server error');
    });
  });

  describe('Optimistic Updates - updateTask', () => {
    beforeEach(() => {
      store.setState({ tasks: [mockTask] });
    });

    it('should update task optimistically', async () => {
      const updates = { title: 'Updated Title', priority: 'high' as const };

      let resolvePromise: (value: Response) => void;
      (fetch as jest.Mock).mockReturnValue(
        new Promise<Response>((resolve) => {
          resolvePromise = resolve;
        })
      );

      const promise = store.getState().updateTask('task-1', updates);

      await new Promise((resolve) => setTimeout(resolve, 0));
      const state = store.getState();

      expect(state.tasks[0].title).toBe('Updated Title');
      expect(state.tasks[0].priority).toBe('high');
      expect(state.optimisticUpdates.size).toBe(1);

      // Cleanup
      resolvePromise!(
        new Response(
          JSON.stringify({ success: true, data: { ...mockTask, ...updates } }),
          { status: 200 }
        )
      );
      await promise.catch(() => {});
    });

    it('should rollback update on failure', async () => {
      const updates = { title: 'Updated Title' };

      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: false, error: 'Update failed' }),
          { status: 500 }
        )
      );

      await expect(store.getState().updateTask('task-1', updates)).rejects.toThrow();

      const state = store.getState();
      expect(state.tasks[0].title).toBe('Test Task'); // Original title
      expect(state.optimisticUpdates.size).toBe(0);
    });

    it('should throw error if task not found', async () => {
      await expect(
        store.getState().updateTask('non-existent', { title: 'New' })
      ).rejects.toThrow('Task non-existent not found');
    });
  });

  describe('Optimistic Updates - deleteTask', () => {
    beforeEach(() => {
      store.setState({ tasks: [mockTask] });
    });

    it('should remove task optimistically', async () => {
      let resolvePromise: (value: Response) => void;
      (fetch as jest.Mock).mockReturnValue(
        new Promise<Response>((resolve) => {
          resolvePromise = resolve;
        })
      );

      const promise = store.getState().deleteTask('task-1');

      await new Promise((resolve) => setTimeout(resolve, 0));
      const state = store.getState();

      expect(state.tasks).toHaveLength(0);
      expect(state.optimisticUpdates.size).toBe(1);

      // Cleanup
      resolvePromise!(
        new Response(
          JSON.stringify({ success: true }),
          { status: 200 }
        )
      );
      await promise.catch(() => {});
    });

    it('should restore task on delete failure', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: false, error: 'Delete failed' }),
          { status: 500 }
        )
      );

      await expect(store.getState().deleteTask('task-1')).rejects.toThrow();

      const state = store.getState();
      expect(state.tasks).toHaveLength(1);
      expect(state.tasks[0].id).toBe('task-1');
    });
  });

  describe('fetchTasks', () => {
    it('should fetch all tasks successfully', async () => {
      const tasks = [mockTask, { ...mockTask, id: 'task-2' }];

      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: true, data: tasks }),
          { status: 200 }
        )
      );

      await store.getState().fetchTasks();

      const state = store.getState();
      expect(state.tasks).toEqual(tasks);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
    });

    it('should fetch tasks by project', async () => {
      const tasks = [mockTask];

      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: true, data: tasks }),
          { status: 200 }
        )
      );

      await store.getState().fetchTasks('project-1');

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('projectId=project-1')
      );
    });

    it('should handle fetch error', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: false, error: 'Fetch failed' }),
          { status: 500 }
        )
      );

      await store.getState().fetchTasks();

      const state = store.getState();
      expect(state.error).toBe('Fetch failed');
      expect(state.isLoading).toBe(false);
    });

    it('should set loading state during fetch', async () => {
      let resolvePromise: (value: Response) => void;
      (fetch as jest.Mock).mockReturnValue(
        new Promise<Response>((resolve) => {
          resolvePromise = resolve;
        })
      );

      const promise = store.getState().fetchTasks();

      expect(store.getState().isLoading).toBe(true);

      resolvePromise!(
        new Response(
          JSON.stringify({ success: true, data: [] }),
          { status: 200 }
        )
      );
      await promise;

      expect(store.getState().isLoading).toBe(false);
    });
  });

  describe('Optimistic Update Management', () => {
    it('should clear all optimistic updates', () => {
      store.setState({
        optimisticUpdates: new Map([
          ['id-1', { id: 'id-1', type: 'create', data: mockTask, timestamp: Date.now() }],
          ['id-2', { id: 'id-2', type: 'update', data: mockTask, timestamp: Date.now() }],
        ]),
      });

      store.getState().clearOptimisticUpdates();

      expect(store.getState().optimisticUpdates.size).toBe(0);
    });
  });
});
