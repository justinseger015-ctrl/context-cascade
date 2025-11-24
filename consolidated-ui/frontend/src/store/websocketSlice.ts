import { StateCreator } from 'zustand';
import type { ConnectionStatus } from '../types/websocket';

/**
 * WebSocket Slice for Zustand Store
 * Manages WebSocket connection state across the application
 */

export interface WebSocketSlice {
  isConnected: boolean;
  connectionStatus: ConnectionStatus;
  lastHeartbeat: Date | null;
  reconnectAttempts: number;
  error: string | null;

  setConnectionStatus: (status: ConnectionStatus) => void;
  setConnected: (connected: boolean) => void;
  updateHeartbeat: () => void;
  incrementReconnectAttempts: () => void;
  resetReconnectAttempts: () => void;
  setError: (error: string | null) => void;
}

export const createWebSocketSlice: StateCreator<
  WebSocketSlice,
  [],
  [],
  WebSocketSlice
> = (set) => ({
  isConnected: false,
  connectionStatus: 'disconnected',
  lastHeartbeat: null,
  reconnectAttempts: 0,
  error: null,

  setConnectionStatus: (status) =>
    set(() => ({
      connectionStatus: status,
      isConnected: status === 'connected',
    })),

  setConnected: (connected) =>
    set(() => ({
      isConnected: connected,
      connectionStatus: connected ? 'connected' : 'disconnected',
    })),

  updateHeartbeat: () =>
    set(() => ({
      lastHeartbeat: new Date(),
    })),

  incrementReconnectAttempts: () =>
    set((state) => ({
      reconnectAttempts: state.reconnectAttempts + 1,
    })),

  resetReconnectAttempts: () =>
    set(() => ({
      reconnectAttempts: 0,
    })),

  setError: (error) =>
    set(() => ({
      error,
    })),
});
