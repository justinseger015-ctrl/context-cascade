/**
 * Unit Tests for WebSocket Slice (Zustand Store)
 * Tests connection state management and heartbeat tracking
 */

import { describe, it, expect, beforeEach, vi } from '@jest/globals';
import { create } from 'zustand';
import { createWebSocketSlice, WebSocketSlice } from '../../../src/store/websocketSlice';

const createTestStore = () => {
  return create<WebSocketSlice>()((...a) => createWebSocketSlice(...a));
};

describe('WebSocketSlice - Connection State Management', () => {
  let store: ReturnType<typeof createTestStore>;

  beforeEach(() => {
    store = createTestStore();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = store.getState();

      expect(state.isConnected).toBe(false);
      expect(state.connectionStatus).toBe('disconnected');
      expect(state.lastHeartbeat).toBeNull();
      expect(state.reconnectAttempts).toBe(0);
    });
  });

  describe('Connection Status Management', () => {
    it('should update connection status and isConnected flag', () => {
      store.getState().setConnectionStatus('connecting');
      expect(store.getState().connectionStatus).toBe('connecting');
      expect(store.getState().isConnected).toBe(false);

      store.getState().setConnectionStatus('connected');
      expect(store.getState().connectionStatus).toBe('connected');
      expect(store.getState().isConnected).toBe(true);

      store.getState().setConnectionStatus('reconnecting');
      expect(store.getState().connectionStatus).toBe('reconnecting');
      expect(store.getState().isConnected).toBe(false);

      store.getState().setConnectionStatus('disconnected');
      expect(store.getState().connectionStatus).toBe('disconnected');
      expect(store.getState().isConnected).toBe(false);
    });

    it('should set connected status directly', () => {
      store.getState().setConnected(true);
      expect(store.getState().isConnected).toBe(true);
      expect(store.getState().connectionStatus).toBe('connected');

      store.getState().setConnected(false);
      expect(store.getState().isConnected).toBe(false);
      expect(store.getState().connectionStatus).toBe('disconnected');
    });
  });

  describe('Heartbeat Management', () => {
    it('should update heartbeat timestamp', () => {
      const beforeUpdate = store.getState().lastHeartbeat;
      expect(beforeUpdate).toBeNull();

      const now = new Date('2024-01-01T12:00:00.000Z');
      vi.setSystemTime(now);

      store.getState().updateHeartbeat();

      const afterUpdate = store.getState().lastHeartbeat;
      expect(afterUpdate).toBeInstanceOf(Date);
      expect(afterUpdate?.getTime()).toBe(now.getTime());
    });

    it('should update heartbeat multiple times', () => {
      const time1 = new Date('2024-01-01T12:00:00.000Z');
      vi.setSystemTime(time1);
      store.getState().updateHeartbeat();
      const heartbeat1 = store.getState().lastHeartbeat;

      const time2 = new Date('2024-01-01T12:01:00.000Z');
      vi.setSystemTime(time2);
      store.getState().updateHeartbeat();
      const heartbeat2 = store.getState().lastHeartbeat;

      expect(heartbeat2!.getTime()).toBeGreaterThan(heartbeat1!.getTime());
    });
  });

  describe('Reconnection Attempts Management', () => {
    it('should increment reconnect attempts', () => {
      expect(store.getState().reconnectAttempts).toBe(0);

      store.getState().incrementReconnectAttempts();
      expect(store.getState().reconnectAttempts).toBe(1);

      store.getState().incrementReconnectAttempts();
      expect(store.getState().reconnectAttempts).toBe(2);

      store.getState().incrementReconnectAttempts();
      expect(store.getState().reconnectAttempts).toBe(3);
    });

    it('should reset reconnect attempts', () => {
      store.setState({ reconnectAttempts: 5 });
      expect(store.getState().reconnectAttempts).toBe(5);

      store.getState().resetReconnectAttempts();
      expect(store.getState().reconnectAttempts).toBe(0);
    });

    it('should simulate reconnection flow', () => {
      // Initial connection fails
      store.getState().setConnectionStatus('connecting');
      store.getState().incrementReconnectAttempts();
      expect(store.getState().reconnectAttempts).toBe(1);

      // Second attempt fails
      store.getState().setConnectionStatus('reconnecting');
      store.getState().incrementReconnectAttempts();
      expect(store.getState().reconnectAttempts).toBe(2);

      // Third attempt succeeds
      store.getState().setConnectionStatus('connected');
      store.getState().resetReconnectAttempts();
      expect(store.getState().reconnectAttempts).toBe(0);
      expect(store.getState().isConnected).toBe(true);
    });
  });

  describe('Integration - Connection Lifecycle', () => {
    it('should handle complete connection lifecycle', () => {
      // Start connecting
      store.getState().setConnectionStatus('connecting');
      expect(store.getState().connectionStatus).toBe('connecting');
      expect(store.getState().isConnected).toBe(false);

      // Connection established
      store.getState().setConnectionStatus('connected');
      store.getState().updateHeartbeat();
      expect(store.getState().isConnected).toBe(true);
      expect(store.getState().lastHeartbeat).not.toBeNull();

      // Connection lost
      store.getState().setConnectionStatus('disconnected');
      store.getState().incrementReconnectAttempts();
      expect(store.getState().isConnected).toBe(false);
      expect(store.getState().reconnectAttempts).toBe(1);

      // Reconnecting
      store.getState().setConnectionStatus('reconnecting');
      store.getState().incrementReconnectAttempts();
      expect(store.getState().reconnectAttempts).toBe(2);

      // Reconnected
      store.getState().setConnectionStatus('connected');
      store.getState().resetReconnectAttempts();
      store.getState().updateHeartbeat();
      expect(store.getState().isConnected).toBe(true);
      expect(store.getState().reconnectAttempts).toBe(0);
    });
  });
});
