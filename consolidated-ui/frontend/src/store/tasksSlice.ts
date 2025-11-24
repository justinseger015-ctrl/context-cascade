import { StateCreator } from 'zustand';
import { Task, ApiResponse, OptimisticUpdate } from '../types';

export interface TasksSlice {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  optimisticUpdates: Map<string, OptimisticUpdate<Task>>;

  // CRUD operations
  addTask: (task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => Promise<void>;
  updateTask: (id: string, updates: Partial<Task>) => Promise<void>;
  deleteTask: (id: string) => Promise<void>;
  fetchTasks: (projectId?: string) => Promise<void>;

  // Helper methods
  getTaskById: (id: string) => Task | undefined;
  getTasksByProject: (projectId: string) => Task[];
  getTasksByStatus: (status: Task['status']) => Task[];

  // Optimistic update handlers
  rollbackOptimisticUpdate: (updateId: string) => void;
  clearOptimisticUpdates: () => void;
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

export const createTasksSlice: StateCreator<TasksSlice> = (set, get) => ({
  tasks: [],
  isLoading: false,
  error: null,
  optimisticUpdates: new Map(),

  addTask: async (taskData) => {
    const tempId = `temp-${Date.now()}`;
    const optimisticTask: Task = {
      ...taskData,
      id: tempId,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    // Optimistic update
    set((state) => ({
      tasks: [...state.tasks, optimisticTask],
      optimisticUpdates: new Map(state.optimisticUpdates).set(tempId, {
        id: tempId,
        type: 'create',
        data: optimisticTask,
        timestamp: Date.now(),
      }),
    }));

    try {
      const response = await fetch(`${API_BASE}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData),
      });

      const result: ApiResponse<Task> = await response.json();

      if (!response.ok || !result.success || !result.data) {
        throw new Error(result.error || 'Failed to create task');
      }

      // Replace optimistic task with real one
      set((state) => {
        const updates = new Map(state.optimisticUpdates);
        updates.delete(tempId);

        return {
          tasks: state.tasks.map((t) => (t.id === tempId ? result.data! : t)),
          optimisticUpdates: updates,
          error: null,
        };
      });
    } catch (error) {
      // Rollback on error
      get().rollbackOptimisticUpdate(tempId);
      set({ error: error instanceof Error ? error.message : 'Unknown error' });
      throw error;
    }
  },

  updateTask: async (id, updates) => {
    const previousTask = get().getTaskById(id);
    if (!previousTask) {
      throw new Error(`Task ${id} not found`);
    }

    const optimisticTask: Task = {
      ...previousTask,
      ...updates,
      updatedAt: new Date(),
    };

    // Optimistic update
    set((state) => ({
      tasks: state.tasks.map((t) => (t.id === id ? optimisticTask : t)),
      optimisticUpdates: new Map(state.optimisticUpdates).set(id, {
        id,
        type: 'update',
        data: optimisticTask,
        previousData: previousTask,
        timestamp: Date.now(),
      }),
    }));

    try {
      const response = await fetch(`${API_BASE}/tasks/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      });

      const result: ApiResponse<Task> = await response.json();

      if (!response.ok || !result.success || !result.data) {
        throw new Error(result.error || 'Failed to update task');
      }

      // Confirm update with server data
      set((state) => {
        const optimisticUpdates = new Map(state.optimisticUpdates);
        optimisticUpdates.delete(id);

        return {
          tasks: state.tasks.map((t) => (t.id === id ? result.data! : t)),
          optimisticUpdates,
          error: null,
        };
      });
    } catch (error) {
      // Rollback on error
      get().rollbackOptimisticUpdate(id);
      set({ error: error instanceof Error ? error.message : 'Unknown error' });
      throw error;
    }
  },

  deleteTask: async (id) => {
    const previousTask = get().getTaskById(id);
    if (!previousTask) {
      throw new Error(`Task ${id} not found`);
    }

    // Optimistic update
    set((state) => ({
      tasks: state.tasks.filter((t) => t.id !== id),
      optimisticUpdates: new Map(state.optimisticUpdates).set(id, {
        id,
        type: 'delete',
        data: previousTask,
        previousData: previousTask,
        timestamp: Date.now(),
      }),
    }));

    try {
      const response = await fetch(`${API_BASE}/tasks/${id}`, {
        method: 'DELETE',
      });

      const result: ApiResponse<void> = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.error || 'Failed to delete task');
      }

      // Confirm deletion
      set((state) => {
        const optimisticUpdates = new Map(state.optimisticUpdates);
        optimisticUpdates.delete(id);

        return {
          optimisticUpdates,
          error: null,
        };
      });
    } catch (error) {
      // Rollback on error
      get().rollbackOptimisticUpdate(id);
      set({ error: error instanceof Error ? error.message : 'Unknown error' });
      throw error;
    }
  },

  fetchTasks: async (projectId) => {
    set({ isLoading: true, error: null });

    try {
      const url = projectId
        ? `${API_BASE}/tasks?projectId=${projectId}`
        : `${API_BASE}/tasks`;

      const response = await fetch(url);
      const result: ApiResponse<Task[]> = await response.json();

      if (!response.ok || !result.success || !result.data) {
        throw new Error(result.error || 'Failed to fetch tasks');
      }

      set({ tasks: result.data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      });
    }
  },

  getTaskById: (id) => {
    return get().tasks.find((t) => t.id === id);
  },

  getTasksByProject: (projectId) => {
    return get().tasks.filter((t) => t.projectId === projectId);
  },

  getTasksByStatus: (status) => {
    return get().tasks.filter((t) => t.status === status);
  },

  rollbackOptimisticUpdate: (updateId) => {
    const update = get().optimisticUpdates.get(updateId);
    if (!update) return;

    set((state) => {
      const optimisticUpdates = new Map(state.optimisticUpdates);
      optimisticUpdates.delete(updateId);

      let tasks = [...state.tasks];

      if (update.type === 'create') {
        // Remove the optimistic task
        tasks = tasks.filter((t) => t.id !== updateId);
      } else if (update.type === 'update' && update.previousData) {
        // Restore previous data
        tasks = tasks.map((t) => (t.id === updateId ? update.previousData as Task : t));
      } else if (update.type === 'delete' && update.previousData) {
        // Restore deleted task
        tasks.push(update.previousData as Task);
      }

      return { tasks, optimisticUpdates };
    });
  },

  clearOptimisticUpdates: () => {
    set({ optimisticUpdates: new Map() });
  },
});

// Re-export Task for calendar types
export type { Task }