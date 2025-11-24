import React, { useEffect, useMemo } from 'react';
import { useStore } from '../store';
import type { AgentActivityExtended } from '../types/agent-monitor';

/**
 * AgentActivityFeed Component
 *
 * Real-time activity feed showing recent agent activities:
 * - Agent ID, task ID, skill name, status
 * - Started at, duration, output preview
 * - Auto-updates via WebSocket 'agent_activity_update' events
 * - Queries Memory MCP for agent metadata
 */
export const AgentActivityFeed: React.FC = () => {
  const {
    agentActivity,
    agents,
    fetchAgentActivity,
    isLoading,
    error,
  } = useStore();

  // Fetch initial activity on mount
  useEffect(() => {
    void fetchAgentActivity(undefined, 100); // Fetch last 100 activities
  }, [fetchAgentActivity]);

  // Enhance activities with agent metadata
  const enhancedActivities = useMemo((): AgentActivityExtended[] => {
    return agentActivity.map((activity) => {
      const agent = agents.find((a) => a.id === activity.agentId);

      // Calculate duration if we have completion time
      const durationMs = activity.details?.completedAt
        ? new Date(activity.details.completedAt as string).getTime() -
          new Date(activity.timestamp).getTime()
        : undefined;

      return {
        ...activity,
        agentName: agent?.name,
        agentType: agent?.type,
        taskId: activity.details?.taskId as string | undefined,
        taskTitle: activity.details?.taskTitle as string | undefined,
        skillName: activity.details?.skillName as string | undefined,
        status: (activity.details?.status as AgentActivityExtended['status']) || 'started',
        startedAt: new Date(activity.timestamp),
        completedAt: activity.details?.completedAt
          ? new Date(activity.details.completedAt as string)
          : undefined,
        durationMs,
        outputPreview: activity.details?.outputPreview as string | undefined,
        error: activity.details?.error as string | undefined,
      };
    });
  }, [agentActivity, agents]);

  // Sort by most recent first
  const sortedActivities = useMemo(() => {
    return [...enhancedActivities].sort(
      (a, b) => b.startedAt.getTime() - a.startedAt.getTime()
    );
  }, [enhancedActivities]);

  // Format duration
  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    return `${Math.floor(ms / 60000)}m ${Math.floor((ms % 60000) / 1000)}s`;
  };

  // Status color mapping
  const getStatusColor = (status: AgentActivityExtended['status']): string => {
    switch (status) {
      case 'started':
      case 'running':
        return 'text-blue-600 bg-blue-50';
      case 'completed':
        return 'text-green-600 bg-green-50';
      case 'failed':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  if (isLoading && sortedActivities.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading agent activities...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-600">Error loading activities: {error}</p>
      </div>
    );
  }

  if (sortedActivities.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">No agent activity yet</div>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">Agent Activity Feed</h3>
        <div className="text-sm text-gray-500">
          {sortedActivities.length} recent activities
        </div>
      </div>

      <div className="space-y-2 max-h-[600px] overflow-y-auto">
        {sortedActivities.map((activity) => (
          <div
            key={activity.id}
            className="p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between">
              {/* Left: Agent info and action */}
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-gray-900">
                    {activity.agentName || activity.agentId}
                  </span>
                  <span className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded">
                    {activity.agentType || 'unknown'}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${getStatusColor(activity.status)}`}
                  >
                    {activity.status}
                  </span>
                </div>

                <div className="text-sm text-gray-600 mb-2">
                  {activity.action}
                </div>

                {/* Task and skill info */}
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  {activity.taskId && (
                    <div>
                      Task: <span className="font-mono">{activity.taskId.slice(0, 8)}</span>
                      {activity.taskTitle && ` - ${activity.taskTitle}`}
                    </div>
                  )}
                  {activity.skillName && (
                    <div>
                      Skill: <span className="font-medium">{activity.skillName}</span>
                    </div>
                  )}
                </div>

                {/* Output preview */}
                {activity.outputPreview && (
                  <div className="mt-2 p-2 bg-gray-50 rounded text-xs font-mono text-gray-700 truncate">
                    {activity.outputPreview}
                  </div>
                )}

                {/* Error message */}
                {activity.error && (
                  <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-600">
                    Error: {activity.error}
                  </div>
                )}
              </div>

              {/* Right: Timing info */}
              <div className="text-right text-xs text-gray-500 ml-4">
                <div>{activity.startedAt.toLocaleTimeString()}</div>
                {activity.durationMs !== undefined && (
                  <div className="font-medium text-gray-700 mt-1">
                    {formatDuration(activity.durationMs)}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
