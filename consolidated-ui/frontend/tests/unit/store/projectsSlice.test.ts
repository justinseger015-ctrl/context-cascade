/**
 * Unit Tests for Projects Slice (Zustand Store)
 * Tests state updates, persistence, optimistic updates, and selection logic
 */

import { describe, it, expect, beforeEach, afterEach, vi } from '@jest/globals';
import { create } from 'zustand';
import { createProjectsSlice, ProjectsSlice } from '../../../src/store/projectsSlice';
import { Project } from '../../../src/types';

global.fetch = vi.fn();

const createTestStore = () => {
  return create<ProjectsSlice>()((...a) => createProjectsSlice(...a));
};

const mockProject: Project = {
  id: 'project-1',
  name: 'Test Project',
  description: 'Test Description',
  status: 'active',
  taskCount: 5,
  agentCount: 3,
  createdAt: '2024-01-01T00:00:00.000Z',
  updatedAt: '2024-01-01T00:00:00.000Z',
};

describe('ProjectsSlice - State Management', () => {
  let store: ReturnType<typeof createTestStore>;

  beforeEach(() => {
    store = createTestStore();
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = store.getState();

      expect(state.projects).toEqual([]);
      expect(state.selectedProject).toBeNull();
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
      expect(state.optimisticUpdates.size).toBe(0);
    });
  });

  describe('Project Selection', () => {
    it('should select a project', () => {
      store.getState().selectProject('project-1');
      expect(store.getState().selectedProject).toBe('project-1');
    });

    it('should deselect a project', () => {
      store.setState({ selectedProject: 'project-1' });
      store.getState().selectProject(null);
      expect(store.getState().selectedProject).toBeNull();
    });
  });

  describe('Helper Methods', () => {
    beforeEach(() => {
      store.setState({ projects: [mockProject] });
    });

    it('getProjectById should return project when found', () => {
      const project = store.getState().getProjectById('project-1');
      expect(project).toEqual(mockProject);
    });

    it('getProjectById should return undefined when not found', () => {
      const project = store.getState().getProjectById('non-existent');
      expect(project).toBeUndefined();
    });

    it('getActiveProjects should filter active projects', () => {
      store.setState({
        projects: [
          mockProject,
          { ...mockProject, id: 'project-2', status: 'completed' as const },
        ],
      });

      const activeProjects = store.getState().getActiveProjects();
      expect(activeProjects).toHaveLength(1);
      expect(activeProjects[0].status).toBe('active');
    });
  });

  describe('Optimistic Updates - addProject', () => {
    it('should add project optimistically', async () => {
      const projectData = {
        name: 'New Project',
        description: 'New Description',
        status: 'active' as const,
      };

      let resolvePromise: (value: Response) => void;
      (fetch as jest.Mock).mockReturnValue(
        new Promise<Response>((resolve) => {
          resolvePromise = resolve;
        })
      );

      const promise = store.getState().addProject(projectData);
      await new Promise((resolve) => setTimeout(resolve, 0));

      const state = store.getState();
      expect(state.projects).toHaveLength(1);
      expect(state.projects[0].name).toBe('New Project');
      expect(state.projects[0].id).toMatch(/^temp-/);
      expect(state.optimisticUpdates.size).toBe(1);

      // Cleanup
      resolvePromise!(
        new Response(
          JSON.stringify({
            success: true,
            data: { ...projectData, id: 'real-1', taskCount: 0, agentCount: 0, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
          }),
          { status: 200 }
        )
      );
      await promise.catch(() => {});
    });

    it('should replace optimistic project with real one on success', async () => {
      const projectData = {
        name: 'New Project',
        description: 'New Description',
        status: 'active' as const,
      };

      const realProject = {
        ...mockProject,
        ...projectData,
        id: 'real-project',
      };

      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: true, data: realProject }),
          { status: 200 }
        )
      );

      await store.getState().addProject(projectData);

      const state = store.getState();
      expect(state.projects[0].id).toBe('real-project');
      expect(state.optimisticUpdates.size).toBe(0);
    });

    it('should rollback on API failure', async () => {
      const projectData = {
        name: 'New Project',
        description: 'New Description',
        status: 'active' as const,
      };

      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: false, error: 'Creation failed' }),
          { status: 500 }
        )
      );

      await expect(store.getState().addProject(projectData)).rejects.toThrow();

      const state = store.getState();
      expect(state.projects).toHaveLength(0);
      expect(state.error).toBe('Creation failed');
    });
  });

  describe('Optimistic Updates - updateProject', () => {
    beforeEach(() => {
      store.setState({ projects: [mockProject] });
    });

    it('should update project optimistically', async () => {
      const updates = { name: 'Updated Name' };

      let resolvePromise: (value: Response) => void;
      (fetch as jest.Mock).mockReturnValue(
        new Promise<Response>((resolve) => {
          resolvePromise = resolve;
        })
      );

      const promise = store.getState().updateProject('project-1', updates);
      await new Promise((resolve) => setTimeout(resolve, 0));

      const state = store.getState();
      expect(state.projects[0].name).toBe('Updated Name');
      expect(state.optimisticUpdates.size).toBe(1);

      // Cleanup
      resolvePromise!(
        new Response(
          JSON.stringify({ success: true, data: { ...mockProject, ...updates } }),
          { status: 200 }
        )
      );
      await promise.catch(() => {});
    });

    it('should rollback update on failure', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: false, error: 'Update failed' }),
          { status: 500 }
        )
      );

      await expect(
        store.getState().updateProject('project-1', { name: 'Updated' })
      ).rejects.toThrow();

      const state = store.getState();
      expect(state.projects[0].name).toBe('Test Project');
    });
  });

  describe('Optimistic Updates - deleteProject', () => {
    beforeEach(() => {
      store.setState({ projects: [mockProject], selectedProject: 'project-1' });
    });

    it('should remove project optimistically and deselect it', async () => {
      let resolvePromise: (value: Response) => void;
      (fetch as jest.Mock).mockReturnValue(
        new Promise<Response>((resolve) => {
          resolvePromise = resolve;
        })
      );

      const promise = store.getState().deleteProject('project-1');
      await new Promise((resolve) => setTimeout(resolve, 0));

      const state = store.getState();
      expect(state.projects).toHaveLength(0);
      expect(state.selectedProject).toBeNull();
      expect(state.optimisticUpdates.size).toBe(1);

      // Cleanup
      resolvePromise!(
        new Response(JSON.stringify({ success: true }), { status: 200 })
      );
      await promise.catch(() => {});
    });

    it('should restore project on delete failure', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: false, error: 'Delete failed' }),
          { status: 500 }
        )
      );

      await expect(store.getState().deleteProject('project-1')).rejects.toThrow();

      const state = store.getState();
      expect(state.projects).toHaveLength(1);
      expect(state.projects[0].id).toBe('project-1');
    });
  });

  describe('fetchProjects', () => {
    it('should fetch projects successfully', async () => {
      const projects = [mockProject, { ...mockProject, id: 'project-2' }];

      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: true, data: projects }),
          { status: 200 }
        )
      );

      await store.getState().fetchProjects();

      const state = store.getState();
      expect(state.projects).toEqual(projects);
      expect(state.isLoading).toBe(false);
      expect(state.error).toBeNull();
    });

    it('should handle fetch error', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce(
        new Response(
          JSON.stringify({ success: false, error: 'Fetch failed' }),
          { status: 500 }
        )
      );

      await store.getState().fetchProjects();

      const state = store.getState();
      expect(state.error).toBe('Fetch failed');
      expect(state.isLoading).toBe(false);
    });
  });
});
