import React, { useEffect } from 'react';
import { useStore } from '../store';
import { useWebSocket } from '../hooks/useWebSocket';
import { WebSocketIndicator } from '../components/WebSocketIndicator';

/**
 * Example component demonstrating WebSocket integration
 *
 * This shows:
 * 1. How to use the useWebSocket hook
 * 2. How to access connection state from Zustand
 * 3. How to send custom messages
 * 4. How to display real-time task and agent updates
 */
export const WebSocketExample: React.FC = () => {
  // Initialize WebSocket connection
  const { send, disconnect, reconnect } = useWebSocket();

  // Access connection state from Zustand store
  const {
    isConnected,
    connectionStatus,
    error,
    lastHeartbeat,
    reconnectAttempts,
  } = useStore((state) => ({
    isConnected: state.isConnected,
    connectionStatus: state.connectionStatus,
    error: state.error,
    lastHeartbeat: state.lastHeartbeat,
    reconnectAttempts: state.reconnectAttempts,
  }));

  // Access tasks and agents from store
  const tasks = useStore((state) => state.tasks);
  const agents = useStore((state) => state.agents);

  // Subscribe to specific channels on connection
  useEffect(() => {
    if (isConnected) {
      send({
        type: 'subscribe',
        channels: ['tasks', 'agents', 'calendar'],
      });
    }
  }, [isConnected, send]);

  // Example: Send custom message
  const handleSendCustomMessage = () => {
    try {
      send({
        type: 'custom_action',
        action: 'request_status',
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">WebSocket Integration Example</h1>

      {/* Connection Status Card */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Connection Status</h2>
          <WebSocketIndicator />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-600">Status</p>
            <p className="font-medium">{connectionStatus}</p>
          </div>

          <div>
            <p className="text-sm text-gray-600">Connected</p>
            <p className="font-medium">{isConnected ? 'Yes' : 'No'}</p>
          </div>

          <div>
            <p className="text-sm text-gray-600">Reconnect Attempts</p>
            <p className="font-medium">{reconnectAttempts}</p>
          </div>

          <div>
            <p className="text-sm text-gray-600">Last Heartbeat</p>
            <p className="font-medium text-xs">
              {lastHeartbeat ? lastHeartbeat.toLocaleTimeString() : 'N/A'}
            </p>
          </div>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded">
            <p className="text-sm text-red-700">
              <strong>Error:</strong> {error}
            </p>
          </div>
        )}

        {/* Connection Controls */}
        <div className="mt-4 flex gap-2">
          <button
            onClick={() => disconnect()}
            disabled={!isConnected}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Disconnect
          </button>

          <button
            onClick={() => reconnect()}
            disabled={isConnected}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Reconnect
          </button>

          <button
            onClick={handleSendCustomMessage}
            disabled={!isConnected}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send Custom Message
          </button>
        </div>
      </div>

      {/* Real-time Tasks */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">
          Real-time Tasks ({tasks.length})
        </h2>

        {tasks.length === 0 ? (
          <p className="text-gray-500 italic">No tasks yet</p>
        ) : (
          <div className="space-y-2">
            {tasks.slice(0, 5).map((task) => (
              <div
                key={task.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded"
              >
                <div>
                  <p className="font-medium">{task.title}</p>
                  <p className="text-sm text-gray-600">
                    Assigned to: {task.assignee || 'Unassigned'}
                  </p>
                </div>
                <span
                  className={`px-2 py-1 text-xs rounded ${
                    task.status === 'done'
                      ? 'bg-green-100 text-green-700'
                      : task.status === 'in_progress'
                      ? 'bg-blue-100 text-blue-700'
                      : task.status === 'review'
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {task.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Real-time Agents */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">
          Real-time Agents ({agents.length})
        </h2>

        {agents.length === 0 ? (
          <p className="text-gray-500 italic">No agents yet</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {agents.map((agent) => (
              <div
                key={agent.id}
                className="p-4 bg-gray-50 rounded border border-gray-200"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium">{agent.name}</h3>
                  <span
                    className={`w-2 h-2 rounded-full ${
                      agent.status === 'busy'
                        ? 'bg-yellow-500'
                        : agent.status === 'idle'
                        ? 'bg-green-500'
                        : 'bg-red-500'
                    }`}
                  />
                </div>

                <p className="text-sm text-gray-600 mb-1">
                  Type: {agent.type}
                </p>

                {agent.currentTask && (
                  <p className="text-sm text-gray-600">
                    Current Task: {agent.currentTask}
                  </p>
                )}

                <div className="mt-2 flex flex-wrap gap-1">
                  {agent.capabilities.map((capability) => (
                    <span
                      key={capability}
                      className="px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded"
                    >
                      {capability}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded">
        <h3 className="font-semibold text-blue-900 mb-2">How to Test</h3>
        <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
          <li>Ensure WebSocket server is running on ws://localhost:8080/ws</li>
          <li>
            Watch the connection status indicator change as you connect/disconnect
          </li>
          <li>
            Use the buttons to manually disconnect and reconnect the WebSocket
          </li>
          <li>
            Send messages from the server to see real-time updates in tasks and
            agents
          </li>
          <li>
            Check the browser console for heartbeat pings and message logs
          </li>
        </ol>
      </div>
    </div>
  );
};

export default WebSocketExample;
