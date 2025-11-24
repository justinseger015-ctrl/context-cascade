import React from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

/**
 * WebSocket Provider Component
 *
 * Wraps the application to provide WebSocket functionality
 * Automatically connects on mount and disconnects on unmount
 *
 * Usage:
 * ```tsx
 * <WebSocketProvider>
 *   <App />
 * </WebSocketProvider>
 * ```
 */
export const WebSocketProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  // Initialize WebSocket connection
  useWebSocket();

  return <>{children}</>;
};
