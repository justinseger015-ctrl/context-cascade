import React from 'react';
import { useStore } from '../store';
import type { ConnectionStatus } from '../types/websocket';

/**
 * WebSocket Connection Status Indicator
 *
 * Displays real-time connection status in the UI with visual feedback
 *
 * Status colors:
 * - Connected: Green
 * - Connecting: Yellow (pulsing)
 * - Reconnecting: Orange (pulsing)
 * - Disconnected: Red
 */
export const WebSocketIndicator: React.FC = () => {
  const { connectionStatus, reconnectAttempts, error } = useStore((state) => ({
    connectionStatus: state.connectionStatus,
    reconnectAttempts: state.reconnectAttempts,
    error: state.error,
  }));

  const getStatusConfig = (
    status: ConnectionStatus
  ): {
    color: string;
    bgColor: string;
    text: string;
    pulse: boolean;
  } => {
    switch (status) {
      case 'connected':
        return {
          color: 'text-green-700',
          bgColor: 'bg-green-100',
          text: 'Connected',
          pulse: false,
        };
      case 'connecting':
        return {
          color: 'text-yellow-700',
          bgColor: 'bg-yellow-100',
          text: 'Connecting...',
          pulse: true,
        };
      case 'reconnecting':
        return {
          color: 'text-orange-700',
          bgColor: 'bg-orange-100',
          text: `Reconnecting... (${reconnectAttempts})`,
          pulse: true,
        };
      case 'disconnected':
        return {
          color: 'text-red-700',
          bgColor: 'bg-red-100',
          text: 'Disconnected',
          pulse: false,
        };
      default:
        return {
          color: 'text-gray-700',
          bgColor: 'bg-gray-100',
          text: 'Unknown',
          pulse: false,
        };
    }
  };

  const config = getStatusConfig(connectionStatus);

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-gray-200">
      {/* Status Indicator Dot */}
      <div className="relative">
        <div
          className={`w-2 h-2 rounded-full ${config.bgColor} ${
            config.pulse ? 'animate-pulse' : ''
          }`}
        />
        {config.pulse && (
          <div
            className={`absolute inset-0 w-2 h-2 rounded-full ${config.bgColor} animate-ping opacity-75`}
          />
        )}
      </div>

      {/* Status Text */}
      <span className={`text-xs font-medium ${config.color}`}>
        {config.text}
      </span>

      {/* Error Tooltip */}
      {error && (
        <div
          className="group relative"
          title={error}
        >
          <svg
            className="w-4 h-4 text-red-500 cursor-help"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>

          {/* Tooltip on hover */}
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block w-48 p-2 bg-gray-900 text-white text-xs rounded shadow-lg z-10">
            {error}
            <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900" />
          </div>
        </div>
      )}
    </div>
  );
};

/**
 * Compact WebSocket Status Badge (for smaller UI areas)
 */
export const WebSocketBadge: React.FC = () => {
  const connectionStatus = useStore((state) => state.connectionStatus);

  const getStatusColor = (status: ConnectionStatus): string => {
    switch (status) {
      case 'connected':
        return 'bg-green-500';
      case 'connecting':
        return 'bg-yellow-500 animate-pulse';
      case 'reconnecting':
        return 'bg-orange-500 animate-pulse';
      case 'disconnected':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div
      className={`w-2 h-2 rounded-full ${getStatusColor(connectionStatus)}`}
      title={connectionStatus}
    />
  );
};
