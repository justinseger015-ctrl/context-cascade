import { StateCreator } from 'zustand';
import { Agent, AgentActivity, ApiResponse } from '../types';

export interface AgentsSlice {
  agents: Agent[];
  agentActivity: AgentActivity[];
  isLoading: boolean;
  error: string | null;

  // Fetch operations
  fetchAgents: (projectId?: string) => Promise<void>;
  fetchAgentActivity: (agentId?: string, limit?: number) => Promise<void>;

  // Update operations (for WebSocket real-time updates)
  updateAgent: (id: string, updates: Partial<Agent>) => void;

  // Helper methods
  getAgentById: (id: string) => Agent | undefined;
  getAgentsByProject: (projectId: string) => Agent[];
  getAgentsByStatus: (status: Agent['status']) => Agent[];
  getAgentsByType: (type: Agent['type']) => Agent[];
  getActiveAgents: () => Agent[];

  // Activity helpers
  getActivityByAgent: (agentId: string) => AgentActivity[];
  getRecentActivity: (limit?: number) => AgentActivity[];
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

export const createAgentsSlice: StateCreator<AgentsSlice> = (set, get) => ({
  agents: [],
  agentActivity: [],
  isLoading: false,
  error: null,

  fetchAgents: async (projectId) => {
    set({ isLoading: true, error: null });

    try {
      const url = projectId
        ? `${API_BASE}/agents?projectId=${projectId}`
        : `${API_BASE}/agents`;

      const response = await fetch(url);
      const result: ApiResponse<Agent[]> = await response.json();

      if (!response.ok || !result.success || !result.data) {
        throw new Error(result.error || 'Failed to fetch agents');
      }

      set({ agents: result.data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      });
    }
  },

  fetchAgentActivity: async (agentId, limit = 100) => {
    set({ isLoading: true, error: null });

    try {
      const params = new URLSearchParams();
      if (agentId) params.append('agentId', agentId);
      if (limit) params.append('limit', limit.toString());

      const url = `${API_BASE}/agent-activity?${params.toString()}`;
      const response = await fetch(url);
      const result: ApiResponse<AgentActivity[]> = await response.json();

      if (!response.ok || !result.success || !result.data) {
        throw new Error(result.error || 'Failed to fetch agent activity');
      }

      set({ agentActivity: result.data, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false,
      });
    }
  },

  updateAgent: (id, updates) => {
    set((state) => ({
      agents: state.agents.map((agent) =>
        agent.id === id ? { ...agent, ...updates } : agent
      ),
    }));
  },

  getAgentById: (id) => {
    return get().agents.find((a) => a.id === id);
  },

  getAgentsByProject: (projectId) => {
    return get().agents.filter((a) => a.projectId === projectId);
  },

  getAgentsByStatus: (status) => {
    return get().agents.filter((a) => a.status === status);
  },

  getAgentsByType: (type) => {
    return get().agents.filter((a) => a.type === type);
  },

  getActiveAgents: () => {
    return get().agents.filter((a) => a.status === 'busy' || a.status === 'idle');
  },

  getActivityByAgent: (agentId) => {
    return get().agentActivity.filter((activity) => activity.agentId === agentId);
  },

  getRecentActivity: (limit = 50) => {
    return get()
      .agentActivity.slice()
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, limit);
  },
});
