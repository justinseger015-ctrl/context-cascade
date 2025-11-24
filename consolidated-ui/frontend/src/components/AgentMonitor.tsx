import React, { useEffect, useState } from 'react';
import { AgentActivityFeed } from './AgentActivityFeed';
import { AgentWorkflowGraph } from './AgentWorkflowGraph';
import { useStore } from '../store';

/**
 * AgentMonitor Component
 *
 * Main agent monitoring dashboard combining:
 * 1. Real-time activity feed (recent agent activities)
 * 2. Workflow graph (agent dependencies visualization)
 * 3. Agent statistics (performance metrics)
 *
 * Features:
 * - Auto-updates via WebSocket
 * - Memory MCP integration for metadata
 * - Tab-based layout for feed vs graph
 * - Performance optimized for 100+ agents
 */
export const AgentMonitor: React.FC = () => {
  const { agents, fetchAgents, isLoading, error } = useStore();
  const [activeTab, setActiveTab] = useState<'feed' | 'graph'>('feed');

  // Fetch agents on mount
  useEffect(() => {
    void fetchAgents();
  }, [fetchAgents]);

  // Calculate summary stats
  const stats = React.useMemo(() => {
    const activeAgents = agents.filter(
      (a) => a.status === 'busy' || a.status === 'idle'
    ).length;
    const busyAgents = agents.filter((a) => a.status === 'busy').length;
    const errorAgents = agents.filter((a) => a.status === 'error').length;

    return {
      total: agents.length,
      active: activeAgents,
      busy: busyAgents,
      error: errorAgents,
    };
  }, [agents]);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Agent Monitor</h1>
          <p className="text-gray-600 mt-1">
            Real-time agent activity tracking and workflow visualization
          </p>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-500">Total Agents</div>
          <div className="text-2xl font-bold text-gray-900 mt-1">
            {stats.total}
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-500">Active Agents</div>
          <div className="text-2xl font-bold text-green-600 mt-1">
            {stats.active}
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-500">Busy Agents</div>
          <div className="text-2xl font-bold text-blue-600 mt-1">
            {stats.busy}
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-500">Error Agents</div>
          <div className="text-2xl font-bold text-red-600 mt-1">
            {stats.error}
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600">Error: {error}</p>
        </div>
      )}

      {/* Loading State */}
      {isLoading && agents.length === 0 && (
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading agents...</div>
        </div>
      )}

      {/* Tab Navigation */}
      {!isLoading && agents.length > 0 && (
        <>
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('feed')}
                className={`
                  py-4 px-1 border-b-2 font-medium text-sm
                  ${
                    activeTab === 'feed'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                Activity Feed
              </button>
              <button
                onClick={() => setActiveTab('graph')}
                className={`
                  py-4 px-1 border-b-2 font-medium text-sm
                  ${
                    activeTab === 'graph'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                Workflow Graph
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            {activeTab === 'feed' && <AgentActivityFeed />}
            {activeTab === 'graph' && <AgentWorkflowGraph />}
          </div>
        </>
      )}

      {/* Empty State */}
      {!isLoading && agents.length === 0 && !error && (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="text-gray-500 mb-2">No agents found</div>
            <p className="text-sm text-gray-400">
              Agents will appear here once they start executing tasks
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
