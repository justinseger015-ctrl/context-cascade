import { useEffect, useRef, useCallback } from 'react';
import { useStore } from '../store';
import type {
  WebSocketMessage,
  TaskStatusUpdate,
  AgentActivityUpdate,
  CalendarEventCreated,
  WebSocketConfig,
} from '../types/websocket';

/**
 * Custom WebSocket Hook with Auto-Reconnection
 *
 * Features:
 * - Automatic connection on mount, disconnection on unmount
 * - Exponential backoff reconnection (1s, 2s, 4s, 8s, max 30s)
 * - Heartbeat mechanism (ping every 30s)
 * - Event handling for task updates, agent activity, calendar events
 * - Connection status tracking in Zustand store
 * - TypeScript strict mode support
 *
 * @param config - WebSocket configuration
 */
export function useWebSocket(config?: Partial<WebSocketConfig>) {
  // Default configuration with exponential backoff
  const defaultConfig: WebSocketConfig = {
    url: import.meta.env.VITE_WS_URL || 'ws://localhost:8080/ws',
    reconnectInterval: 1000, // Start at 1 second
    maxReconnectInterval: 30000, // Max 30 seconds
    heartbeatInterval: 30000, // Ping every 30 seconds
    reconnectBackoffMultiplier: 2, // Exponential backoff multiplier
  };

  const wsConfig = { ...defaultConfig, ...config };

  // Zustand store selectors and actions
  const {
    setConnectionStatus,
    updateHeartbeat,
    incrementReconnectAttempts,
    resetReconnectAttempts,
    setError,
    reconnectAttempts,
  } = useStore();

  const { updateTask } = useStore();
  const { updateAgent } = useStore();

  // Refs to persist across renders without causing re-renders
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const heartbeatIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const isIntentionalClose = useRef(false);

  /**
   * Calculate reconnect delay with exponential backoff
   * Formula: min(initialDelay * (multiplier ^ attempts), maxDelay)
   */
  const calculateReconnectDelay = useCallback((): number => {
    const delay = Math.min(
      wsConfig.reconnectInterval * Math.pow(wsConfig.reconnectBackoffMultiplier, reconnectAttempts),
      wsConfig.maxReconnectInterval
    );
    return delay;
  }, [wsConfig, reconnectAttempts]);

  /**
   * Start heartbeat mechanism - send ping every 30s
   */
  const startHeartbeat = useCallback(() => {
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
    }

    heartbeatIntervalRef.current = setInterval(() => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(
          JSON.stringify({
            type: 'ping',
            timestamp: new Date().toISOString(),
          })
        );
        console.log('[WebSocket] Heartbeat ping sent');
      }
    }, wsConfig.heartbeatInterval);
  }, [wsConfig.heartbeatInterval]);

  /**
   * Stop heartbeat mechanism
   */
  const stopHeartbeat = useCallback(() => {
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
      heartbeatIntervalRef.current = null;
    }
  }, []);

  /**
   * Handle incoming WebSocket messages
   */
  const handleMessage = useCallback(
    (event: MessageEvent) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);

        console.log('[WebSocket] Message received:', message.type);

        switch (message.type) {
          case 'task_status_update': {
            const payload = message.payload as TaskStatusUpdate;
            // P4_T3: Enhanced task status update with output/error
            updateTask(payload.taskId, {
              status: payload.status,
              assignee: payload.assignee,
              updatedAt: new Date(payload.updatedAt),
              // Additional fields from backend
              ...(payload.output && { output: payload.output }),
              ...(payload.error && { error: payload.error }),
              ...(payload.projectId && { projectId: payload.projectId }),
            });
            console.log('[WebSocket] Task status updated:', {
              taskId: payload.taskId,
              status: payload.status,
              hasOutput: !!payload.output,
              hasError: !!payload.error,
            });
            break;
          }

          case 'agent_activity_update': {
            const payload = message.payload as AgentActivityUpdate;
            updateAgent(payload.agentId, {
              status: payload.status,
              currentTask: payload.currentTask,
            });
            console.log('[WebSocket] Agent updated:', payload.agentId);
            break;
          }

          case 'calendar_event_created': {
            const payload = message.payload as CalendarEventCreated;
            // For calendar events, you might want to add them to a calendar slice
            // For now, just log them
            console.log('[WebSocket] Calendar event created:', payload);
            // TODO: Implement calendar slice integration when ready
            break;
          }

          case 'pong': {
            updateHeartbeat();
            console.log('[WebSocket] Pong received - connection alive');
            break;
          }

          default:
            console.warn('[WebSocket] Unknown message type:', message.type);
        }
      } catch (error) {
        console.error('[WebSocket] Failed to parse message:', error);
        setError(error instanceof Error ? error.message : 'Failed to parse message');
      }
    },
    [updateTask, updateAgent, updateHeartbeat, setError]
  );

  /**
   * Connect to WebSocket server
   */
  const connect = useCallback(() => {
    // Prevent duplicate connections
    if (wsRef.current?.readyState === WebSocket.OPEN || wsRef.current?.readyState === WebSocket.CONNECTING) {
      console.log('[WebSocket] Already connected or connecting');
      return;
    }

    console.log(`[WebSocket] Connecting to ${wsConfig.url}...`);
    setConnectionStatus('connecting');
    setError(null);

    try {
      const ws = new WebSocket(wsConfig.url);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('[WebSocket] Connected successfully');
        setConnectionStatus('connected');
        resetReconnectAttempts();
        startHeartbeat();
        setError(null);
      };

      ws.onmessage = handleMessage;

      ws.onerror = (error) => {
        console.error('[WebSocket] Error:', error);
        setError('WebSocket connection error');
      };

      ws.onclose = (event) => {
        console.log('[WebSocket] Connection closed', {
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean,
        });

        stopHeartbeat();

        // Only attempt reconnection if not intentionally closed
        if (!isIntentionalClose.current) {
          setConnectionStatus('reconnecting');
          incrementReconnectAttempts();

          const delay = calculateReconnectDelay();
          console.log(`[WebSocket] Reconnecting in ${delay}ms (attempt ${reconnectAttempts + 1})`);

          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, delay);
        } else {
          setConnectionStatus('disconnected');
          isIntentionalClose.current = false;
        }
      };
    } catch (error) {
      console.error('[WebSocket] Failed to create WebSocket:', error);
      setError(error instanceof Error ? error.message : 'Failed to create WebSocket');
      setConnectionStatus('disconnected');
    }
  }, [
    wsConfig.url,
    setConnectionStatus,
    setError,
    resetReconnectAttempts,
    incrementReconnectAttempts,
    startHeartbeat,
    stopHeartbeat,
    handleMessage,
    calculateReconnectDelay,
    reconnectAttempts,
  ]);

  /**
   * Disconnect from WebSocket server
   */
  const disconnect = useCallback(() => {
    console.log('[WebSocket] Disconnecting...');
    isIntentionalClose.current = true;

    // Clear reconnection timeout
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    // Stop heartbeat
    stopHeartbeat();

    // Close WebSocket connection
    if (wsRef.current) {
      wsRef.current.close(1000, 'Client initiated disconnect');
      wsRef.current = null;
    }

    setConnectionStatus('disconnected');
    resetReconnectAttempts();
  }, [setConnectionStatus, resetReconnectAttempts, stopHeartbeat]);

  /**
   * Send message through WebSocket
   */
  const send = useCallback((data: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
      console.log('[WebSocket] Message sent:', data);
    } else {
      console.warn('[WebSocket] Cannot send message - not connected');
      throw new Error('WebSocket is not connected');
    }
  }, []);

  // Effect: Connect on mount, disconnect on unmount
  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty deps - only run on mount/unmount

  return {
    send,
    disconnect,
    reconnect: connect,
  };
}
