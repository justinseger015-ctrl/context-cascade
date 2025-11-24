import { useEffect, useRef } from 'react';
import { useTerminalsStore, TerminalMessage } from '../store/terminalsStore';

/**
 * WebSocket Terminal Stream Hook
 *
 * Connects to backend WebSocket endpoint for real-time terminal output
 * Endpoint: ws://localhost:8000/ws/terminals/{terminalId}
 */

interface UseTerminalStreamOptions {
  terminalId: string;
  autoConnect?: boolean;
  reconnectDelay?: number;
  maxReconnectAttempts?: number;
  onMessage?: (message: TerminalMessage) => void;
  onConnect?: () => void;
  onDisconnect?: () => void;
  onError?: (error: Event) => void;
}

export const useTerminalStream = ({
  terminalId,
  autoConnect = true,
  reconnectDelay = 3000,
  maxReconnectAttempts = 5,
  onMessage,
  onConnect,
  onDisconnect,
  onError,
}: UseTerminalStreamOptions) => {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const { addMessage, setConnectionStatus } = useTerminalsStore();

  const connect = () => {
    // Prevent duplicate connections
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    setConnectionStatus(terminalId, 'connecting');

    const wsUrl = `ws://localhost:8000/ws/terminals/${terminalId}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log(`[useTerminalStream] Connected to terminal ${terminalId}`);
      setConnectionStatus(terminalId, 'connected');
      reconnectAttemptsRef.current = 0;

      if (onConnect) {
        onConnect();
      }
    };

    ws.onmessage = (event) => {
      try {
        const message: TerminalMessage = JSON.parse(event.data);

        // Store message in Zustand store
        addMessage(terminalId, message);

        // Call custom handler if provided
        if (onMessage) {
          onMessage(message);
        }
      } catch (error) {
        console.error('[useTerminalStream] Failed to parse message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error(`[useTerminalStream] WebSocket error for terminal ${terminalId}:`, error);
      setConnectionStatus(terminalId, 'error');

      if (onError) {
        onError(error);
      }
    };

    ws.onclose = () => {
      console.log(`[useTerminalStream] Disconnected from terminal ${terminalId}`);
      setConnectionStatus(terminalId, 'disconnected');

      if (onDisconnect) {
        onDisconnect();
      }

      // Auto-reconnect logic
      if (reconnectAttemptsRef.current < maxReconnectAttempts) {
        reconnectAttemptsRef.current += 1;
        console.log(`[useTerminalStream] Reconnecting... (attempt ${reconnectAttemptsRef.current}/${maxReconnectAttempts})`);

        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, reconnectDelay);
      } else {
        console.warn(`[useTerminalStream] Max reconnect attempts reached for terminal ${terminalId}`);
      }
    };

    wsRef.current = ws;
  };

  const disconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  };

  // Auto-connect on mount
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, [terminalId, autoConnect]);

  return {
    connect,
    disconnect,
    isConnected: wsRef.current?.readyState === WebSocket.OPEN,
  };
};
