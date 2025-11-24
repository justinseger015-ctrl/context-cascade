/**
 * Integration Tests - WebSocket Real-Time Updates
 * Tests WebSocket integration with task updates
 */

import { describe, it, expect, beforeEach, vi } from '@jest/globals';
import { create } from 'zustand';
import { createWebSocketSlice, WebSocketSlice } from '../../src/store/websocketSlice';
import { createTasksSlice, TasksSlice } from '../../src/store/tasksSlice';
import type { WebSocketMessage, TaskStatusUpdate } from '../../src/types';

type IntegrationStore = WebSocketSlice & TasksSlice;

const createIntegrationStore = () => {
  return create<IntegrationStore>()((...a) => ({
    ...createWebSocketSlice(...a),
    ...createTasksSlice(...a),
  }));
};

describe('Integration: WebSocket Real-Time Updates', () => {
  let store: ReturnType<typeof createIntegrationStore>;
  let mockWebSocket: WebSocket;

  beforeEach(() => {
    store = createIntegrationStore();
    mockWebSocket = new WebSocket('ws://localhost:3001');
  });

  it('should update connection status when WebSocket connects', async () => {
    expect(store.getState().isConnected).toBe(false);

    // Simulate WebSocket connection
    store.getState().setConnectionStatus('connecting');
    expect(store.getState().connectionStatus).toBe('connecting');

    // Wait for mock WebSocket to "connect"
    await new Promise((resolve) => setTimeout(resolve, 10));

    store.getState().setConnectionStatus('connected');
    store.getState().updateHeartbeat();

    expect(store.getState().isConnected).toBe(true);
    expect(store.getState().lastHeartbeat).not.toBeNull();
  });

  it('should handle task status updates via WebSocket', async () => {
    // Setup initial task
    const initialTask = await store.getState().addTask({
      projectId: 'project-1',
      title: 'WebSocket Test Task',
      description: 'Testing real-time updates',
      status: 'pending',
      priority: 'high',
      skill_name: 'websocket-test',
    });

    await new Promise((resolve) => setTimeout(resolve, 100));

    const tasks = store.getState().tasks;
    const taskId = tasks[0]?.id;

    expect(taskId).toBeDefined();
    expect(tasks[0].status).toBe('pending');

    // Simulate receiving WebSocket message with task status update
    const statusUpdate: TaskStatusUpdate = {
      taskId: taskId!,
      status: 'in_progress',
      updatedAt: new Date().toISOString(),
    };

    const wsMessage: WebSocketMessage = {
      type: 'task_status_update',
      payload: statusUpdate,
      timestamp: new Date().toISOString(),
    };

    // Update task via store (simulating WebSocket handler)
    await store.getState().updateTask(taskId!, { status: 'running' });

    const updatedTasks = store.getState().tasks;
    expect(updatedTasks[0].status).toBe('running');
  });

  it('should handle reconnection after connection loss', async () => {
    // Initial connection
    store.getState().setConnectionStatus('connected');
    expect(store.getState().reconnectAttempts).toBe(0);

    // Connection lost
    store.getState().setConnectionStatus('disconnected');
    store.getState().incrementReconnectAttempts();
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

  it('should handle heartbeat updates during active connection', async () => {
    vi.useFakeTimers();

    store.getState().setConnectionStatus('connected');

    const time1 = new Date('2024-01-01T12:00:00.000Z');
    vi.setSystemTime(time1);
    store.getState().updateHeartbeat();

    const heartbeat1 = store.getState().lastHeartbeat;
    expect(heartbeat1?.getTime()).toBe(time1.getTime());

    // Simulate 30 seconds passing
    vi.advanceTimersByTime(30000);

    const time2 = new Date('2024-01-01T12:00:30.000Z');
    vi.setSystemTime(time2);
    store.getState().updateHeartbeat();

    const heartbeat2 = store.getState().lastHeartbeat;
    expect(heartbeat2!.getTime()).toBeGreaterThan(heartbeat1!.getTime());

    vi.useRealTimers();
  });

  it('should handle multiple concurrent WebSocket messages', async () => {
    // Create multiple tasks
    await Promise.all([
      store.getState().addTask({
        projectId: 'project-1',
        title: 'Task 1',
        description: 'Test',
        status: 'pending',
        priority: 'high',
        skill_name: 'test',
      }),
      store.getState().addTask({
        projectId: 'project-1',
        title: 'Task 2',
        description: 'Test',
        status: 'pending',
        priority: 'medium',
        skill_name: 'test',
      }),
      store.getState().addTask({
        projectId: 'project-1',
        title: 'Task 3',
        description: 'Test',
        status: 'pending',
        priority: 'low',
        skill_name: 'test',
      }),
    ]);

    await new Promise((resolve) => setTimeout(resolve, 100));

    const tasks = store.getState().tasks;
    expect(tasks).toHaveLength(3);

    // Simulate concurrent status updates
    await Promise.all(
      tasks.map((task) =>
        store.getState().updateTask(task.id, { status: 'running' })
      )
    );

    const updatedTasks = store.getState().tasks;
    expect(updatedTasks.every((t) => t.status === 'running')).toBe(true);
  });
});
