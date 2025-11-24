import { StateCreator } from 'zustand';
import { Project, ApiResponse, OptimisticUpdate } from '../types';

export interface ProjectsSlice {
  projects: Project[];
  selectedProject: string | null;
  isLoading: boolean;
  error: string | null;
  optimisticUpdates: Map<string, OptimisticUpdate<Project>>;

  // CRUD operations
  addProject: (project: Omit<Project, 'id' | 'createdAt' | 'updatedAt' | 'taskCount' | 'agentCount'>) => Promise<void>;
  updateProject: (id: string, updates: Partial<Project>) => Promise<void>;
  deleteProject: (id: string) => Promise<void>;
  fetchProjects: () => Promise<void>;

  // Selection
  selectProject: (id: string | null) => void;

  // Helper methods
  getProjectById: (id: string) => Project | undefined;
  getActiveProjects: () => Project[];

  // Optimistic update handlers
  rollbackOptimisticUpdate: (updateId: string) => void;
  clearOptimisticUpdates: () => void;
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

export const createProjectsSlice: StateCreator<ProjectsSlice> = (set, get) => ({
  projects: [],
  selectedProject: null,
  isLoading: false,
  error: null,
  optimisticUpdates: new Map(),

  addProject: async (projectData) => {
    const tempId = `temp-${Date.now()}`;
    const optimisticProject: Project = {
      ...projectData,
      id: tempId,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      taskCount: 0,
      agentCount: 0,
    };

    // Optimistic update
    set((state) => ({
      projects: [...state.projects, optimisticProject],
      optimisticUpdates: new Map(state.optimisticUpdates).set(tempId, {
        id: tempId,
        type: 'create',
        data: optimisticProject,
        timestamp: Date.now(),
      }),
    }));

    try {
      const response = await fetch(`${API_BASE}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(projectData),
      });

      const result: ApiResponse<Project> = await response.json();

      if (!response.ok || !result.success || !result.data) {
        throw new Error(result.error || 'Failed to create project');
      }

      // Replace optimistic project with real one
      set((state) => {
        const updates = new Map(state.optimisticUpdates);
        updates.delete(tempId);

        return {
          projects: state.projects.map((p) => (p.id === tempId ? result.data! : p)),
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

  updateProject: async (id, updates) => {
    const previousProject = get().getProjectById(id);
    if (!previousProject) {
      throw new Error(`Project ${id} not found`);
    }

    const optimisticProject: Project = {
      ...previousProject,
      ...updates,
      updatedAt: new Date().toISOString(),
    };

    // Optimistic update
    set((state) => ({
      projects: state.projects.map((p) => (p.id === id ? optimisticProject : p)),
      optimisticUpdates: new Map(state.optimisticUpdates).set(id, {
        id,
        type: 'update',
        data: optimisticProject,
        previousData: previousProject,
        timestamp: Date.now(),
      }),
    }));

    try {
      const response = await fetch(`${API_BASE}/projects/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates),
      });

      const result: ApiResponse<Project> = await response.json();

      if (!response.ok || !result.success || !result.data) {
        throw new Error(result.error || 'Failed to update project');
      }

      // Confirm update with server data
      set((state) => {
        const optimisticUpdates = new Map(state.optimisticUpdates);
        optimisticUpdates.delete(id);

        return {
          projects: state.projects.map((p) => (p.id === id ? result.data! : p)),
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

  deleteProject: async (id) => {
    const previousProject = get().getProjectById(id);
    if (!previousProject) {
      throw new Error(`Project ${id} not found`);
    }

    // Optimistic update
    set((state) => ({
      projects: state.projects.filter((p) => p.id !== id),
      selectedProject: state.selectedProject === id ? null : state.selectedProject,
      optimisticUpdates: new Map(state.optimisticUpdates).set(id, {
        id,
        type: 'delete',
        data: previousProject,
        previousData: previousProject,
        timestamp: Date.now(),
      }),
    }));

    try {
      const response = await fetch(`${API_BASE}/projects/${id}`, {
        method: 'DELETE',
      });

      const result: ApiResponse<void> = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.error || 'Failed to delete project');
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

  fetchProjects: async () => {
    set({ isLoading: true, error: null });

    try {
      const response = await fetch(`${API_BASE}/projects`);
      const result: ApiResponse<Project[]> = await response.json();

      if (!response.ok || !result.success || !result.data) {
        throw new Error(result.error || 'Failed to fetch projects');
      }

      set({ projects: result.data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      });
    }
  },

  selectProject: (id) => {
    set({ selectedProject: id });
  },

  getProjectById: (id) => {
    return get().projects.find((p) => p.id === id);
  },

  getActiveProjects: () => {
    return get().projects.filter((p) => p.status === 'active');
  },

  rollbackOptimisticUpdate: (updateId) => {
    const update = get().optimisticUpdates.get(updateId);
    if (!update) return;

    set((state) => {
      const optimisticUpdates = new Map(state.optimisticUpdates);
      optimisticUpdates.delete(updateId);

      let projects = [...state.projects];

      if (update.type === 'create') {
        // Remove the optimistic project
        projects = projects.filter((p) => p.id !== updateId);
      } else if (update.type === 'update' && update.previousData) {
        // Restore previous data
        projects = projects.map((p) =>
          p.id === updateId ? (update.previousData as Project) : p
        );
      } else if (update.type === 'delete' && update.previousData) {
        // Restore deleted project
        projects.push(update.previousData as Project);
      }

      return { projects, optimisticUpdates };
    });
  },

  clearOptimisticUpdates: () => {
    set({ optimisticUpdates: new Map() });
  },
});
