import React, { useMemo, useCallback, useState } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  ConnectionMode,
  NodeTypes,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { useStore } from '../store';
import type { Agent } from '../types';
import type {
  AgentFlowNode,
  AgentFlowEdge,
  AgentStats,
} from '../types/agent-monitor';
import {
  AGENT_TYPE_COLORS,
  AGENT_STATUS_COLORS,
} from '../types/agent-monitor';

/**
 * Custom Agent Node Component
 */
const AgentNode: React.FC<{ data: AgentFlowNode['data'] }> = ({ data }) => {
  const typeColor = AGENT_TYPE_COLORS[data.agentType] || AGENT_TYPE_COLORS.default;
  const statusColor = AGENT_STATUS_COLORS[data.status];

  return (
    <div
      className="px-4 py-3 rounded-lg border-2 bg-white shadow-md min-w-[180px]"
      style={{ borderColor: typeColor }}
    >
      {/* Agent name and status */}
      <div className="flex items-center justify-between mb-2">
        <div className="font-semibold text-sm text-gray-900 truncate">
          {data.agentName}
        </div>
        <div
          className="w-2 h-2 rounded-full"
          style={{ backgroundColor: statusColor }}
          title={data.status}
        />
      </div>

      {/* Agent type */}
      <div className="text-xs text-gray-600 mb-2">{data.agentType}</div>

      {/* Stats */}
      {data.stats && (
        <div className="text-xs space-y-1 pt-2 border-t border-gray-200">
          <div className="flex justify-between">
            <span className="text-gray-500">Tasks:</span>
            <span className="font-medium">{data.stats.totalTasksExecuted}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Success:</span>
            <span className="font-medium text-green-600">
              {data.stats.successRate.toFixed(0)}%
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Avg:</span>
            <span className="font-medium">
              {(data.stats.avgDurationMs / 1000).toFixed(1)}s
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

const nodeTypes: NodeTypes = {
  agent: AgentNode,
};

/**
 * AgentWorkflowGraph Component
 *
 * React Flow workflow visualization showing:
 * - Agent nodes (color-coded by type)
 * - Dependency edges (who spawned/called whom)
 * - Interactive: click node → show details
 * - Performance optimized for 100+ nodes (60 FPS)
 */
export const AgentWorkflowGraph: React.FC = () => {
  const { agents, agentActivity } = useStore();
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  // Calculate agent statistics
  const agentStats = useMemo((): Record<string, AgentStats> => {
    const stats: Record<string, AgentStats> = {};

    agents.forEach((agent) => {
      const activities = agentActivity.filter((a) => a.agentId === agent.id);

      const totalTasksExecuted = activities.length;
      const successCount = activities.filter(
        (a) => a.details?.status === 'completed'
      ).length;
      const failureCount = activities.filter(
        (a) => a.details?.status === 'failed'
      ).length;

      const durations = activities
        .map((a) => {
          if (a.details?.completedAt && a.timestamp) {
            return (
              new Date(a.details.completedAt as string).getTime() -
              new Date(a.timestamp).getTime()
            );
          }
          return 0;
        })
        .filter((d) => d > 0);

      const avgDurationMs =
        durations.length > 0
          ? durations.reduce((sum, d) => sum + d, 0) / durations.length
          : 0;

      const lastActivity = activities
        .sort(
          (a, b) =>
            new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        )[0];

      stats[agent.id] = {
        agentId: agent.id,
        agentName: agent.name,
        agentType: agent.type,
        totalTasksExecuted,
        successCount,
        failureCount,
        successRate:
          totalTasksExecuted > 0 ? (successCount / totalTasksExecuted) * 100 : 0,
        avgDurationMs,
        lastActiveAt: lastActivity
          ? new Date(lastActivity.timestamp)
          : undefined,
        currentStatus: agent.status,
      };
    });

    return stats;
  }, [agents, agentActivity]);

  // Extract agent dependencies from activity (simplified - in real app, would come from backend)
  const dependencies = useMemo((): AgentFlowEdge[] => {
    const deps: AgentFlowEdge[] = [];
    const addedEdges = new Set<string>();

    agentActivity.forEach((activity) => {
      // If activity has spawner info, create dependency
      const spawnerId = activity.details?.spawnedBy as string | undefined;
      if (spawnerId && spawnerId !== activity.agentId) {
        const edgeId = `${spawnerId}-${activity.agentId}`;
        if (!addedEdges.has(edgeId)) {
          deps.push({
            id: edgeId,
            source: spawnerId,
            target: activity.agentId,
            type: 'smoothstep',
            label: activity.details?.taskTitle as string | undefined,
            data: {
              taskId: activity.details?.taskId as string | undefined,
              taskTitle: activity.details?.taskTitle as string | undefined,
            },
          });
          addedEdges.add(edgeId);
        }
      }
    });

    return deps;
  }, [agentActivity]);

  // Create React Flow nodes
  const flowNodes = useMemo((): Node<AgentFlowNode['data']>[] => {
    // Simple layout: arrange in grid
    const nodesPerRow = Math.ceil(Math.sqrt(agents.length));

    return agents.map((agent, index) => {
      const row = Math.floor(index / nodesPerRow);
      const col = index % nodesPerRow;

      return {
        id: agent.id,
        type: 'agent',
        data: {
          agentId: agent.id,
          agentName: agent.name,
          agentType: agent.type,
          status: agent.status,
          stats: agentStats[agent.id],
          capabilities: agent.capabilities,
        },
        position: {
          x: col * 250,
          y: row * 200,
        },
      };
    });
  }, [agents, agentStats]);

  // Create React Flow edges
  const flowEdges = useMemo((): Edge[] => {
    return dependencies.map((dep) => ({
      id: dep.id,
      source: dep.source,
      target: dep.target,
      type: dep.type,
      label: dep.label,
      animated: true,
      style: { stroke: '#9CA3AF', strokeWidth: 2 },
    }));
  }, [dependencies]);

  // React Flow state
  const [nodes, setNodes, onNodesChange] = useNodesState(flowNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(flowEdges);

  // Update nodes/edges when data changes
  React.useEffect(() => {
    setNodes(flowNodes);
  }, [flowNodes, setNodes]);

  React.useEffect(() => {
    setEdges(flowEdges);
  }, [flowEdges, setEdges]);

  // Handle node click
  const onNodeClick = useCallback(
    (_event: React.MouseEvent, node: Node) => {
      const agent = agents.find((a) => a.id === node.id);
      if (agent) {
        setSelectedAgent(agent);
      }
    },
    [agents]
  );

  return (
    <div className="h-[600px] w-full border border-gray-200 rounded-lg overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        nodeTypes={nodeTypes}
        connectionMode={ConnectionMode.Loose}
        fitView
        minZoom={0.1}
        maxZoom={2}
      >
        <Background />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            const data = node.data as AgentFlowNode['data'];
            return (AGENT_TYPE_COLORS[data.agentType] || AGENT_TYPE_COLORS.default) ?? '#6B7280';
          }}
        />
        <Panel position="top-left" className="bg-white p-2 rounded shadow">
          <div className="text-sm font-medium">
            {agents.length} agents • {dependencies.length} dependencies
          </div>
        </Panel>
      </ReactFlow>

      {/* Selected agent details panel */}
      {selectedAgent && (
        <div className="absolute bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg border border-gray-200 max-w-md">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-semibold text-gray-900">
              {selectedAgent.name}
            </h4>
            <button
              onClick={() => setSelectedAgent(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
          <div className="space-y-2 text-sm">
            <div>
              <span className="text-gray-500">Type:</span>{' '}
              <span className="font-medium">{selectedAgent.type}</span>
            </div>
            <div>
              <span className="text-gray-500">Status:</span>{' '}
              <span className="font-medium">{selectedAgent.status}</span>
            </div>
            {selectedAgent.currentTask && (
              <div>
                <span className="text-gray-500">Current Task:</span>{' '}
                <span className="font-medium">{selectedAgent.currentTask}</span>
              </div>
            )}
            <div>
              <span className="text-gray-500">Capabilities:</span>
              <div className="flex flex-wrap gap-1 mt-1">
                {selectedAgent.capabilities.map((cap) => (
                  <span
                    key={cap}
                    className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-xs"
                  >
                    {cap}
                  </span>
                ))}
              </div>
            </div>
            {agentStats[selectedAgent.id] && (
              <div className="pt-2 border-t border-gray-200">
                <div className="text-gray-500 mb-1">Statistics:</div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    Total Tasks:{' '}
                    <span className="font-medium">
                      {agentStats[selectedAgent.id]?.totalTasksExecuted ?? 0}
                    </span>
                  </div>
                  <div>
                    Success Rate:{' '}
                    <span className="font-medium text-green-600">
                      {(agentStats[selectedAgent.id]?.successRate ?? 0).toFixed(0)}%
                    </span>
                  </div>
                  <div>
                    Avg Duration:{' '}
                    <span className="font-medium">
                      {((agentStats[selectedAgent.id]?.avgDurationMs ?? 0) / 1000).toFixed(1)}s
                    </span>
                  </div>
                  {agentStats[selectedAgent.id]?.lastActiveAt && (
                    <div>
                      Last Active:{' '}
                      <span className="font-medium">
                        {agentStats[selectedAgent.id]?.lastActiveAt?.toLocaleTimeString() ?? ''}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
