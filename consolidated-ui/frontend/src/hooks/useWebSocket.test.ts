import { renderHook, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import { useWebSocket } from './useWebSocket';
import { useStore } from '../store';

// Mock WebSocket
class MockWebSocket {
  static CONNECTING = 0;
  static OPEN = 1;
  static CLOSING = 2;
  static CLOSED = 3;

  readyState: number = MockWebSocket.CONNECTING;
  onopen: ((event: Event) => void) | null = null;
  onclose: ((event: CloseEvent) => void) | null = null;
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: ((event: Event) => void) | null = null;

  constructor(public url: string) {
    // Simulate async connection
    setTimeout(() => {
      this.readyState = MockWebSocket.OPEN;
      this.onopen?.(new Event('open'));
    }, 0);
  }

  send(data: string) {
    console.log('Mock WebSocket send:', data);
  }

  close(code?: number, reason?: string) {
    this.readyState = MockWebSocket.CLOSED;
    const closeEvent = new CloseEvent('close', {
      code: code || 1000,
      reason: reason || '',
      wasClean: true,
    });
    this.onclose?.(closeEvent);
  }

  // Helper to simulate receiving messages
  simulateMessage(data: unknown) {
    const messageEvent = new MessageEvent('message', {
      data: JSON.stringify(data),
    });
    this.onmessage?.(messageEvent);
  }

  // Helper to simulate errors
  simulateError() {
    this.onerror?.(new Event('error'));
  }
}

// Replace global WebSocket with mock
(global as any).WebSocket = MockWebSocket;

describe('useWebSocket', () => {
  beforeEach(() => {
    // Reset store before each test
    useStore.setState({
      isConnected: false,
      connectionStatus: 'disconnected',
      reconnectAttempts: 0,
      error: null,
    });

    // Clear all timers
    jest.clearAllTimers();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should connect to WebSocket on mount', async () => {
    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      const state = useStore.getState();
      expect(state.connectionStatus).toBe('connected');
      expect(state.isConnected).toBe(true);
    });
  });

  it('should disconnect on unmount', async () => {
    const { result, unmount } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    unmount();

    await waitFor(() => {
      const state = useStore.getState();
      expect(state.connectionStatus).toBe('disconnected');
      expect(state.isConnected).toBe(false);
    });
  });

  it('should handle task status updates', async () => {
    const mockUpdateTask = jest.fn();
    useStore.setState({ updateTask: mockUpdateTask });

    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    // Get the mock WebSocket instance
    const ws = (global as any).WebSocket.instances?.[0];

    act(() => {
      ws?.simulateMessage({
        type: 'task_status_update',
        payload: {
          taskId: 'task-123',
          status: 'in_progress',
          assignee: 'agent-1',
          updatedAt: new Date().toISOString(),
        },
      });
    });

    await waitFor(() => {
      expect(mockUpdateTask).toHaveBeenCalledWith(
        'task-123',
        expect.objectContaining({
          status: 'in_progress',
          assignee: 'agent-1',
        })
      );
    });
  });

  it('should handle agent activity updates', async () => {
    const mockUpdateAgent = jest.fn();
    useStore.setState({ updateAgent: mockUpdateAgent });

    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    const ws = (global as any).WebSocket.instances?.[0];

    act(() => {
      ws?.simulateMessage({
        type: 'agent_activity_update',
        payload: {
          agentId: 'agent-123',
          status: 'busy',
          currentTask: 'task-456',
          timestamp: new Date().toISOString(),
        },
      });
    });

    await waitFor(() => {
      expect(mockUpdateAgent).toHaveBeenCalledWith(
        'agent-123',
        expect.objectContaining({
          status: 'busy',
          currentTask: 'task-456',
        })
      );
    });
  });

  it('should send heartbeat pings every 30 seconds', async () => {
    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    const ws = (global as any).WebSocket.instances?.[0];
    const sendSpy = jest.spyOn(ws, 'send');

    // Fast-forward 30 seconds
    act(() => {
      jest.advanceTimersByTime(30000);
    });

    expect(sendSpy).toHaveBeenCalledWith(
      expect.stringContaining('"type":"ping"')
    );
  });

  it('should handle pong responses and update heartbeat', async () => {
    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    const ws = (global as any).WebSocket.instances?.[0];

    const initialHeartbeat = useStore.getState().lastHeartbeat;

    act(() => {
      ws?.simulateMessage({ type: 'pong' });
    });

    await waitFor(() => {
      const newHeartbeat = useStore.getState().lastHeartbeat;
      expect(newHeartbeat).not.toBe(initialHeartbeat);
      expect(newHeartbeat).toBeInstanceOf(Date);
    });
  });

  it('should attempt reconnection with exponential backoff', async () => {
    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    const ws = (global as any).WebSocket.instances?.[0];

    // Simulate connection close
    act(() => {
      ws?.close(1006, 'Abnormal closure');
    });

    await waitFor(() => {
      const state = useStore.getState();
      expect(state.connectionStatus).toBe('reconnecting');
    });

    // First reconnect attempt after 1s
    act(() => {
      jest.advanceTimersByTime(1000);
    });

    // Should increment reconnect attempts
    await waitFor(() => {
      expect(useStore.getState().reconnectAttempts).toBe(1);
    });
  });

  it('should reset reconnect attempts on successful connection', async () => {
    useStore.setState({ reconnectAttempts: 5 });

    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      const state = useStore.getState();
      expect(state.isConnected).toBe(true);
      expect(state.reconnectAttempts).toBe(0);
    });
  });

  it('should handle connection errors', async () => {
    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    const ws = (global as any).WebSocket.instances?.[0];

    act(() => {
      ws?.simulateError();
    });

    await waitFor(() => {
      const state = useStore.getState();
      expect(state.error).toBeTruthy();
    });
  });

  it('should allow manual send of messages', async () => {
    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    const ws = (global as any).WebSocket.instances?.[0];
    const sendSpy = jest.spyOn(ws, 'send');

    act(() => {
      result.current.send({ type: 'custom', data: 'test' });
    });

    expect(sendSpy).toHaveBeenCalledWith(
      JSON.stringify({ type: 'custom', data: 'test' })
    );
  });

  it('should allow manual reconnect', async () => {
    const { result } = renderHook(() => useWebSocket());

    await waitFor(() => {
      expect(useStore.getState().isConnected).toBe(true);
    });

    act(() => {
      result.current.disconnect();
    });

    await waitFor(() => {
      expect(useStore.getState().connectionStatus).toBe('disconnected');
    });

    act(() => {
      result.current.reconnect();
    });

    await waitFor(() => {
      expect(useStore.getState().connectionStatus).toBe('connected');
    });
  });
});
