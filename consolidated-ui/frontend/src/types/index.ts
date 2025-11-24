// Core types for the Ruv-Sparc UI Dashboard

export interface Project {
  id: string;
  name: string;
  description: string;
  status: 'planning' | 'in_progress' | 'completed' | 'on_hold';
  tasks?: Task[];
  createdAt: Date;
  updatedAt: Date;
}

// Dashboard-specific types
export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed';
export type TaskSortField = 'createdAt' | 'next_run_at' | 'status';
export type SortDirection = 'asc' | 'desc';

export interface TaskFilters {
  status?: TaskStatus[];
  skill_name?: string[];
}

export interface TaskSort {
  field: TaskSortField;
  direction: SortDirection;
}

export interface Task {
  id: string;
  projectId: string;
  title: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  skill_name: string;
  schedule?: string; // Cron expression or schedule string
  next_run_at?: Date;
  last_run_at?: Date;
  assignee?: string;
  dueDate?: Date;
  order?: number; // For drag-and-drop ordering
  createdAt: Date;
  updatedAt: Date;
}

export interface Agent {
  id: string;
  name: string;
  type: string;
  status: 'idle' | 'busy' | 'error';
  capabilities: string[];
  currentTask?: string;
}

export interface AgentActivity {
  id: string;
  agentId: string;
  action: string;
  details?: Record<string, unknown>;
  timestamp: Date;
}

export interface WorkflowNode {
  id: string;
  type: 'task' | 'decision' | 'parallel' | 'end';
  data: {
    label: string;
    description?: string;
    agentType?: string;
  };
  position: { x: number; y: number };
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  type?: 'default' | 'conditional';
}

export interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  resource?: string;
  color?: string;
  data?: Record<string, unknown>;
}

// Export API types
export type { ApiResponse, OptimisticUpdate, WebSocketConnectionStatus, WebSocketMessage } from './api';

// Export task types
export type {
  ScheduledTask,
  TaskExecution,
  CreateTaskPayload,
  UpdateTaskPayload,
  TaskListResponse,
  TaskResponse,
  TaskApiError,
} from './task.types';

// Export form types
export type { TaskFormData } from '../validation/taskSchema';

// Export hook types
export type { Skill } from '../hooks/useSkills';

// Export agent monitor types
export type {
  AgentActivityExtended,
  AgentStats,
  AgentDependency,
  AgentFlowNode,
  AgentFlowEdge,
} from './agent-monitor';
export { AGENT_TYPE_COLORS, AGENT_STATUS_COLORS } from './agent-monitor';
