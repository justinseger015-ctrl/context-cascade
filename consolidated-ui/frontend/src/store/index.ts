import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { createTasksSlice, TasksSlice } from './tasksSlice';
import { createProjectsSlice, ProjectsSlice } from './projectsSlice';
import { createAgentsSlice, AgentsSlice } from './agentsSlice';
import { createWebSocketSlice, WebSocketSlice } from './websocketSlice';

// Combined store type
export type StoreState = TasksSlice & ProjectsSlice & AgentsSlice & WebSocketSlice;

/**
 * Main Zustand store combining all slices
 *
 * Features:
 * - Persistence: All slices except WebSocket are persisted to localStorage
 * - Optimistic updates: Tasks and Projects support optimistic UI updates
 * - Type safety: Full TypeScript strict mode support
 * - Modularity: Each slice is independently testable
 */
export const useStore = create<StoreState>()(
  persist(
    (...args) => ({
      ...createTasksSlice(...args),
      ...createProjectsSlice(...args),
      ...createAgentsSlice(...args),
      ...createWebSocketSlice(...args),
    }),
    {
      name: 'ruv-sparc-storage', // localStorage key
      storage: createJSONStorage(() => localStorage),

      // Partition: only persist non-WebSocket state
      partialize: (state) => ({
        // Tasks slice
        tasks: state.tasks,
        // Projects slice
        projects: state.projects,
        selectedProject: state.selectedProject,
        // Agents slice
        agents: state.agents,
        agentActivity: state.agentActivity,

        // Exclude WebSocket slice entirely
        // Exclude loading/error states (ephemeral)
        // Exclude optimistic updates (should not persist)
      }),

      // Version for migration compatibility
      version: 1,

      // Migration function for future schema changes
      migrate: (persistedState: unknown, version: number) => {
        if (version === 0) {
          // Example migration for v0 -> v1
          // Add any schema transformations here
        }
        return persistedState as StoreState;
      },
    }
  )
);

// Selectors for common use cases
export const selectTasks = (state: StoreState) => state.tasks;
export const selectProjects = (state: StoreState) => state.projects;
export const selectSelectedProject = (state: StoreState) => state.selectedProject;
export const selectAgents = (state: StoreState) => state.agents;
export const selectAgentActivity = (state: StoreState) => state.agentActivity;
export const selectWebSocketStatus = (state: StoreState) => ({
  isConnected: state.isConnected,
  connectionStatus: state.connectionStatus,
  error: state.error,
});

// Compound selectors
export const selectTasksByProject = (projectId: string) => (state: StoreState) =>
  state.getTasksByProject(projectId);

export const selectActiveProjects = (state: StoreState) =>
  state.getActiveProjects();

export const selectActiveAgents = (state: StoreState) =>
  state.getActiveAgents();

export const selectRecentActivity = (limit?: number) => (state: StoreState) =>
  state.getRecentActivity(limit);
