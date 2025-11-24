/**
 * WebSocket Types and Message Interfaces
 */

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'reconnecting';

export interface WebSocketMessage {
  type: 'task_status_update' | 'agent_activity_update' | 'calendar_event_created' | 'pong';
  payload?: unknown;
  timestamp?: string;
}

export interface TaskStatusUpdate {
  taskId: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'disabled';
  assignee?: string;
  updatedAt: string;
  output?: string;
  error?: string;
  projectId?: string;
}

export interface AgentActivityUpdate {
  agentId: string;
  status: 'idle' | 'busy' | 'error';
  currentTask?: string;
  timestamp: string;
}

export interface CalendarEventCreated {
  id: string;
  title: string;
  start: string;
  end: string;
  resource?: string;
  color?: string;
  data?: Record<string, unknown>;
}

export interface WebSocketConfig {
  url: string;
  reconnectInterval?: number;
  maxReconnectInterval?: number;
  heartbeatInterval?: number;
  reconnectBackoffMultiplier?: number;
}
