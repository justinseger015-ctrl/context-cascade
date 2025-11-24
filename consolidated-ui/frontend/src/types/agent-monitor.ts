/**
 * Agent Monitor Types
 *
 * TypeScript types for agent monitoring, activity tracking, and workflow visualization
 */

import type { Agent, AgentActivity } from './index';

/**
 * Extended Agent Activity with additional details for monitoring
 */
export interface AgentActivityExtended extends AgentActivity {
  agentName?: string;
  agentType?: string;
  taskId?: string;
  taskTitle?: string;
  skillName?: string;
  status: 'started' | 'running' | 'completed' | 'failed';
  startedAt: Date;
  completedAt?: Date;
  durationMs?: number;
  outputPreview?: string;
  error?: string;
}

/**
 * Agent Statistics
 */
export interface AgentStats {
  agentId: string;
  agentName: string;
  agentType: string;
  totalTasksExecuted: number;
  successCount: number;
  failureCount: number;
  successRate: number; // 0-100
  avgDurationMs: number;
  lastActiveAt?: Date;
  currentStatus: Agent['status'];
}

/**
 * Agent Dependency - represents who spawned/called whom
 */
export interface AgentDependency {
  id: string;
  sourceAgentId: string; // Agent that spawned/called
  targetAgentId: string; // Agent that was spawned/called
  taskId?: string; // Task that created this dependency
  taskTitle?: string;
  createdAt: Date;
}

/**
 * Agent Node for React Flow visualization
 */
export interface AgentFlowNode {
  id: string;
  type: 'agent';
  data: {
    agentId: string;
    agentName: string;
    agentType: string;
    status: Agent['status'];
    stats?: AgentStats;
    capabilities?: string[];
  };
  position: { x: number; y: number };
}

/**
 * Agent Edge for React Flow visualization
 */
export interface AgentFlowEdge {
  id: string;
  source: string;
  target: string;
  type?: 'default' | 'smoothstep';
  label?: string;
  data?: {
    taskId?: string;
    taskTitle?: string;
  };
}

/**
 * Agent color mapping by type
 */
export const AGENT_TYPE_COLORS: Record<string, string> = {
  researcher: '#3B82F6', // blue
  coder: '#10B981', // green
  tester: '#FBBF24', // yellow
  reviewer: '#8B5CF6', // purple
  planner: '#EC4899', // pink
  analyst: '#06B6D4', // cyan
  optimizer: '#F97316', // orange
  coordinator: '#EF4444', // red
  default: '#6B7280', // gray
};

/**
 * Agent status color mapping
 */
export const AGENT_STATUS_COLORS: Record<Agent['status'], string> = {
  idle: '#6B7280', // gray
  busy: '#10B981', // green
  error: '#EF4444', // red
};
