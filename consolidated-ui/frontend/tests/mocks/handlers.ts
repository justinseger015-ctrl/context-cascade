/**
 * MSW (Mock Service Worker) Request Handlers
 * Provides API mocking for tests
 */

import { http, HttpResponse } from 'msw';
import type { Task, Project, ApiResponse } from '../../src/types';

const API_BASE = 'http://localhost:3001/api';

// In-memory storage for mocked data
let mockTasks: Task[] = [];
let mockProjects: Project[] = [];

// Helper to generate IDs
let taskIdCounter = 1;
let projectIdCounter = 1;

export const handlers = [
  // Tasks endpoints
  http.get(`${API_BASE}/tasks`, ({ request }) => {
    const url = new URL(request.url);
    const projectId = url.searchParams.get('projectId');

    const filteredTasks = projectId
      ? mockTasks.filter((t) => t.projectId === projectId)
      : mockTasks;

    const response: ApiResponse<Task[]> = {
      success: true,
      data: filteredTasks,
    };

    return HttpResponse.json(response);
  }),

  http.post(`${API_BASE}/tasks`, async ({ request }) => {
    const body = (await request.json()) as Omit<
      Task,
      'id' | 'createdAt' | 'updatedAt'
    >;

    const newTask: Task = {
      ...body,
      id: `task-${taskIdCounter++}`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    mockTasks.push(newTask);

    const response: ApiResponse<Task> = {
      success: true,
      data: newTask,
    };

    return HttpResponse.json(response, { status: 201 });
  }),

  http.patch(`${API_BASE}/tasks/:id`, async ({ params, request }) => {
    const { id } = params;
    const updates = (await request.json()) as Partial<Task>;

    const taskIndex = mockTasks.findIndex((t) => t.id === id);
    if (taskIndex === -1) {
      return HttpResponse.json(
        { success: false, error: 'Task not found' },
        { status: 404 }
      );
    }

    mockTasks[taskIndex] = {
      ...mockTasks[taskIndex],
      ...updates,
      updatedAt: new Date().toISOString(),
    };

    const response: ApiResponse<Task> = {
      success: true,
      data: mockTasks[taskIndex],
    };

    return HttpResponse.json(response);
  }),

  http.delete(`${API_BASE}/tasks/:id`, ({ params }) => {
    const { id } = params;
    const taskIndex = mockTasks.findIndex((t) => t.id === id);

    if (taskIndex === -1) {
      return HttpResponse.json(
        { success: false, error: 'Task not found' },
        { status: 404 }
      );
    }

    mockTasks.splice(taskIndex, 1);

    const response: ApiResponse<void> = {
      success: true,
    };

    return HttpResponse.json(response);
  }),

  // Projects endpoints
  http.get(`${API_BASE}/projects`, () => {
    const response: ApiResponse<Project[]> = {
      success: true,
      data: mockProjects,
    };

    return HttpResponse.json(response);
  }),

  http.post(`${API_BASE}/projects`, async ({ request }) => {
    const body = (await request.json()) as Omit<
      Project,
      'id' | 'createdAt' | 'updatedAt' | 'taskCount' | 'agentCount'
    >;

    const newProject: Project = {
      ...body,
      id: `project-${projectIdCounter++}`,
      taskCount: 0,
      agentCount: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    mockProjects.push(newProject);

    const response: ApiResponse<Project> = {
      success: true,
      data: newProject,
    };

    return HttpResponse.json(response, { status: 201 });
  }),

  http.patch(`${API_BASE}/projects/:id`, async ({ params, request }) => {
    const { id } = params;
    const updates = (await request.json()) as Partial<Project>;

    const projectIndex = mockProjects.findIndex((p) => p.id === id);
    if (projectIndex === -1) {
      return HttpResponse.json(
        { success: false, error: 'Project not found' },
        { status: 404 }
      );
    }

    mockProjects[projectIndex] = {
      ...mockProjects[projectIndex],
      ...updates,
      updatedAt: new Date().toISOString(),
    };

    const response: ApiResponse<Project> = {
      success: true,
      data: mockProjects[projectIndex],
    };

    return HttpResponse.json(response);
  }),

  http.delete(`${API_BASE}/projects/:id`, ({ params }) => {
    const { id } = params;
    const projectIndex = mockProjects.findIndex((p) => p.id === id);

    if (projectIndex === -1) {
      return HttpResponse.json(
        { success: false, error: 'Project not found' },
        { status: 404 }
      );
    }

    mockProjects.splice(projectIndex, 1);

    const response: ApiResponse<void> = {
      success: true,
    };

    return HttpResponse.json(response);
  }),
];

// Helper functions to manipulate mock data in tests
export const resetMockData = () => {
  mockTasks = [];
  mockProjects = [];
  taskIdCounter = 1;
  projectIdCounter = 1;
};

export const setMockTasks = (tasks: Task[]) => {
  mockTasks = [...tasks];
};

export const setMockProjects = (projects: Project[]) => {
  mockProjects = [...projects];
};

export const getMockTasks = () => [...mockTasks];
export const getMockProjects = () => [...mockProjects];
