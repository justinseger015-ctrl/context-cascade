import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { Project, Task } from '../types';

interface ProjectState {
  projects: Project[];
  selectedProjectId: string | null;
  addProject: (project: Omit<Project, 'id' | 'createdAt' | 'updatedAt'>) => void;
  updateProject: (id: string, updates: Partial<Project>) => void;
  deleteProject: (id: string) => void;
  selectProject: (id: string | null) => void;

  // Task management
  addTask: (projectId: string, task: Omit<Task, 'id' | 'projectId' | 'createdAt' | 'updatedAt'>) => void;
  updateTask: (projectId: string, taskId: string, updates: Partial<Task>) => void;
  deleteTask: (projectId: string, taskId: string) => void;
  reorderTasks: (projectId: string, tasks: Task[]) => void;
  runTaskNow: (projectId: string, taskId: string) => void;

  // Computed values
  getSelectedProject: () => Project | null;
  getProjectTasks: (projectId: string) => Task[];
}

export const useProjectStore = create<ProjectState>()(
  devtools(
    persist(
      (set) => ({
        projects: [],
        selectedProjectId: null,

        addProject: (projectData) =>
          set((state) => ({
            projects: [
              ...state.projects,
              {
                ...projectData,
                id: crypto.randomUUID(),
                createdAt: new Date(),
                updatedAt: new Date(),
              },
            ],
          })),

        updateProject: (id, updates) =>
          set((state) => ({
            projects: state.projects.map((p) =>
              p.id === id ? { ...p, ...updates, updatedAt: new Date() } : p
            ),
          })),

        deleteProject: (id) =>
          set((state) => ({
            projects: state.projects.filter((p) => p.id !== id),
            selectedProjectId: state.selectedProjectId === id ? null : state.selectedProjectId,
          })),

        selectProject: (id) =>
          set(() => ({
            selectedProjectId: id,
          })),

        // Task management
        addTask: (projectId, taskData) =>
          set((state) => ({
            projects: state.projects.map((p) =>
              p.id === projectId
                ? {
                    ...p,
                    tasks: [
                      ...(p.tasks || []),
                      {
                        ...taskData,
                        id: crypto.randomUUID(),
                        projectId,
                        order: (p.tasks || []).length,
                        createdAt: new Date(),
                        updatedAt: new Date(),
                      },
                    ],
                    updatedAt: new Date(),
                  }
                : p
            ),
          })),

        updateTask: (projectId, taskId, updates) =>
          set((state) => ({
            projects: state.projects.map((p) =>
              p.id === projectId
                ? {
                    ...p,
                    tasks: (p.tasks || []).map((t) =>
                      t.id === taskId ? { ...t, ...updates, updatedAt: new Date() } : t
                    ),
                    updatedAt: new Date(),
                  }
                : p
            ),
          })),

        deleteTask: (projectId, taskId) =>
          set((state) => ({
            projects: state.projects.map((p) =>
              p.id === projectId
                ? {
                    ...p,
                    tasks: (p.tasks || []).filter((t) => t.id !== taskId),
                    updatedAt: new Date(),
                  }
                : p
            ),
          })),

        reorderTasks: (projectId, reorderedTasks) =>
          set((state) => ({
            projects: state.projects.map((p) =>
              p.id === projectId
                ? {
                    ...p,
                    tasks: reorderedTasks.map((t, index) => ({ ...t, order: index })),
                    updatedAt: new Date(),
                  }
                : p
            ),
          })),

        runTaskNow: (projectId, taskId) =>
          set((state) => ({
            projects: state.projects.map((p) =>
              p.id === projectId
                ? {
                    ...p,
                    tasks: (p.tasks || []).map((t) =>
                      t.id === taskId
                        ? {
                            ...t,
                            status: 'running' as const,
                            last_run_at: new Date(),
                            updatedAt: new Date(),
                          }
                        : t
                    ),
                    updatedAt: new Date(),
                  }
                : p
            ),
          })),

        // Computed values
        getSelectedProject: (): Project | null => {
          const state = useProjectStore.getState();
          return state.projects.find((p: Project) => p.id === state.selectedProjectId) || null;
        },

        getProjectTasks: (projectId: string): Task[] => {
          const state = useProjectStore.getState();
          const project = state.projects.find((p: Project) => p.id === projectId);
          return project?.tasks || [];
        },
      }),
      {
        name: 'project-storage',
      }
    )
  )
);
