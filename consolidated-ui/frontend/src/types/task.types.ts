/**
 * Task-related TypeScript type definitions
 */

import { TaskFormData } from '../validation/taskSchema';

/**
 * Scheduled task entity from API
 */
export interface ScheduledTask extends TaskFormData {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'disabled';
  createdAt: string;
  updatedAt: string;
  lastRun?: string;
  nextRun?: string;
  runCount: number;
  errorCount: number;
}

/**
 * Task execution result
 */
export interface TaskExecution {
  id: string;
  taskId: string;
  status: 'running' | 'completed' | 'failed';
  startedAt: string;
  completedAt?: string;
  duration?: number;
  output?: string;
  error?: string;
}

/**
 * Task creation payload for API
 */
export interface CreateTaskPayload {
  skillName: string;
  cronSchedule: string;
  parameters: string; // JSON string
  projectId?: string;
  description?: string;
  enabled: boolean;
}

/**
 * Task update payload for API
 */
export interface UpdateTaskPayload extends Partial<CreateTaskPayload> {
  id: string;
}

/**
 * API response for task list
 */
export interface TaskListResponse {
  tasks: ScheduledTask[];
  total: number;
  page: number;
  pageSize: number;
}

/**
 * API response for single task
 */
export interface TaskResponse {
  task: ScheduledTask;
}

/**
 * API error response
 */
export interface TaskApiError {
  error: string;
  message: string;
  details?: Record<string, any>;
}
