# WebSocket Client Implementation - P3_T4

## Overview

This document describes the WebSocket client implementation for the Ruv-Sparc UI Dashboard, providing real-time updates for tasks, agents, and calendar events.

## Architecture

### Components

1. **useWebSocket Hook** (`src/hooks/useWebSocket.ts`)
   - Custom React hook managing WebSocket lifecycle
   - Automatic connection/disconnection
   - Exponential backoff reconnection strategy
   - Heartbeat mechanism for connection health
   - Event handling and message dispatching

2. **WebSocket Slice** (`src/store/websocketSlice.ts`)
   - Zustand store slice for connection state
   - Tracks: connection status, heartbeat, reconnect attempts, errors

3. **UI Components**
   - `WebSocketIndicator`: Full status indicator with error tooltips
   - `WebSocketBadge`: Compact status badge
   - `WebSocketProvider`: Convenience wrapper component

4. **Type Definitions** (`src/types/websocket.ts`)
   - TypeScript interfaces for messages and configuration
   - Connection status types

## Features

### 1. Automatic Connection Management

```typescript
// Hook automatically connects on mount
const { send, disconnect, reconnect } = useWebSocket();

// Or use the provider wrapper
<WebSocketProvider>
  <App />
</WebSocketProvider>
```

### 2. Exponential Backoff Reconnection

The client implements exponential backoff with configurable parameters:

- **Initial delay**: 1 second
- **Backoff multiplier**: 2x
- **Maximum delay**: 30 seconds

**Reconnection sequence**:
1. First attempt: 1s delay
2. Second attempt: 2s delay
3. Third attempt: 4s delay
4. Fourth attempt: 8s delay
5. Fifth attempt: 16s delay
6. Sixth+ attempts: 30s delay (capped)

### 3. Heartbeat Mechanism

- **Ping interval**: 30 seconds
- **Format**: `{ type: 'ping', timestamp: '...' }`
- **Expected response**: `{ type: 'pong' }`
- Updates `lastHeartbeat` timestamp in store

### 4. Event Handling

The client listens for and handles these message types:

#### Task Status Update
```typescript
{
  type: 'task_status_update',
  payload: {
    taskId: string,
    status: 'todo' | 'in_progress' | 'review' | 'done',
    assignee?: string,
    updatedAt: string (ISO 8601)
  }
}
```
**Action**: Updates task in Zustand tasksSlice, triggers UI re-render

#### Agent Activity Update
```typescript
{
  type: 'agent_activity_update',
  payload: {
    agentId: string,
    status: 'idle' | 'busy' | 'error',
    currentTask?: string,
    timestamp: string (ISO 8601)
  }
}
```
**Action**: Updates agent in Zustand agentsSlice, reflects in UI

#### Calendar Event Created
```typescript
{
  type: 'calendar_event_created',
  payload: {
    id: string,
    title: string,
    start: string (ISO 8601),
    end: string (ISO 8601),
    resource?: string,
    color?: string,
    data?: Record<string, unknown>
  }
}
```
**Action**: Logged (calendar slice integration pending)

#### Pong
```typescript
{
  type: 'pong'
}
```
**Action**: Updates `lastHeartbeat` timestamp

### 5. Connection Status Tracking

The WebSocket slice tracks four connection states:

- **`connecting`**: Initial connection attempt
- **`connected`**: Successfully connected and ready
- **`reconnecting`**: Connection lost, attempting to reconnect
- **`disconnected`**: Intentionally closed or failed

## Usage

### Basic Setup

1. **Configure environment variables**:
```bash
# .env
VITE_WS_URL=ws://localhost:8080/ws
```

2. **Add WebSocketProvider to your app**:
```tsx
import { WebSocketProvider } from './components/WebSocketProvider';

function App() {
  return (
    <WebSocketProvider>
      {/* Your app components */}
    </WebSocketProvider>
  );
}
```

3. **Add status indicator to UI**:
```tsx
import { WebSocketIndicator } from './components/WebSocketIndicator';

function Header() {
  return (
    <header>
      <h1>Dashboard</h1>
      <WebSocketIndicator />
    </header>
  );
}
```

### Advanced Usage

#### Custom Configuration
```tsx
const { send, disconnect, reconnect } = useWebSocket({
  url: 'wss://custom-server.com/ws',
  reconnectInterval: 2000,         // Start at 2s
  maxReconnectInterval: 60000,     // Max 60s
  heartbeatInterval: 15000,        // Ping every 15s
  reconnectBackoffMultiplier: 1.5, // 1.5x backoff
});
```

#### Manual Message Sending
```tsx
const { send } = useWebSocket();

// Send custom message
send({
  type: 'subscribe',
  channels: ['tasks', 'agents'],
});
```

#### Manual Reconnection
```tsx
const { reconnect, disconnect } = useWebSocket();

// Disconnect
disconnect();

// Reconnect later
reconnect();
```

### Accessing Connection State

```tsx
import { useStore } from './store';

function MyComponent() {
  const { isConnected, connectionStatus, error } = useStore((state) => ({
    isConnected: state.isConnected,
    connectionStatus: state.connectionStatus,
    error: state.error,
  }));

  if (!isConnected) {
    return <div>Connecting to server...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return <div>Connected! Status: {connectionStatus}</div>;
}
```

## UI Components

### WebSocketIndicator

Full status indicator with visual feedback:

```tsx
import { WebSocketIndicator } from './components/WebSocketIndicator';

<WebSocketIndicator />
```

**Features**:
- Color-coded status (green/yellow/orange/red)
- Pulsing animation for transitional states
- Reconnection attempt counter
- Error tooltip on hover
- Responsive design

### WebSocketBadge

Compact status badge for minimal UI:

```tsx
import { WebSocketBadge } from './components/WebSocketIndicator';

<WebSocketBadge />
```

**Features**:
- 2px circular indicator
- Color-coded status
- Pulsing animation
- Title attribute for accessibility

## Real-Time UI Updates

### Task Updates

When a `task_status_update` message is received:

1. Hook parses the message payload
2. Calls `updateTask(taskId, updates)` on Zustand store
3. Components subscribed to tasks automatically re-render
4. Calendar and project dashboard reflect new status

**Example flow**:
```
Server → WebSocket → useWebSocket hook → tasksSlice.updateTask() → UI re-render
```

### Agent Updates

When an `agent_activity_update` message is received:

1. Hook parses the message payload
2. Calls `updateAgent(agentId, updates)` on Zustand store
3. Agent status indicators update in real-time
4. Agent activity feeds refresh

**Example flow**:
```
Server → WebSocket → useWebSocket hook → agentsSlice.updateAgent() → UI re-render
```

## Testing

### Unit Tests

Run the comprehensive test suite:

```bash
npm test useWebSocket.test.ts
npm test WebSocketIndicator.test.tsx
```

**Test coverage**:
- Connection lifecycle (mount/unmount)
- Message handling (task, agent, calendar, pong)
- Reconnection with exponential backoff
- Heartbeat mechanism
- Error handling
- Manual send/disconnect/reconnect
- UI component rendering for all states

### Manual Testing

1. **Start the WebSocket server**:
```bash
# Ensure backend is running on ws://localhost:8080/ws
```

2. **Start the frontend**:
```bash
npm run dev
```

3. **Test scenarios**:
   - ✅ Connection indicator turns green when connected
   - ✅ Send task update from server → UI updates immediately
   - ✅ Send agent update from server → UI updates immediately
   - ✅ Stop server → Indicator shows "reconnecting" with attempt count
   - ✅ Restart server → Indicator reconnects automatically
   - ✅ Check console for heartbeat pings every 30s

## Performance Considerations

### 1. Optimized Re-renders

The hook uses Zustand selectors to minimize re-renders:

```tsx
// Only re-renders when connectionStatus changes
const connectionStatus = useStore((state) => state.connectionStatus);
```

### 2. Ref-based WebSocket Instance

WebSocket instance stored in `useRef` to prevent recreation on every render:

```typescript
const wsRef = useRef<WebSocket | null>(null);
```

### 3. Cleanup on Unmount

Proper cleanup prevents memory leaks:

```typescript
useEffect(() => {
  connect();
  return () => disconnect(); // Cleanup
}, []);
```

### 4. Debounced Reconnection

Exponential backoff prevents server overload during reconnection attempts.

## Security Considerations

### 1. WSS in Production

Always use secure WebSocket (WSS) in production:

```bash
# Production .env
VITE_WS_URL=wss://api.production.com/ws
```

### 2. Authentication

Add authentication to WebSocket messages:

```typescript
const { send } = useWebSocket();

// Send auth token on connection
useEffect(() => {
  if (isConnected) {
    send({
      type: 'authenticate',
      token: localStorage.getItem('authToken'),
    });
  }
}, [isConnected, send]);
```

### 3. Message Validation

The hook validates incoming messages:

```typescript
try {
  const message: WebSocketMessage = JSON.parse(event.data);
  // Process message
} catch (error) {
  console.error('Invalid message format');
  setError('Failed to parse message');
}
```

## Troubleshooting

### Connection Issues

**Problem**: WebSocket fails to connect

**Solutions**:
1. Check `VITE_WS_URL` in `.env`
2. Verify backend WebSocket server is running
3. Check browser console for errors
4. Verify firewall/proxy settings

### Reconnection Loop

**Problem**: Client reconnects infinitely

**Solutions**:
1. Check server-side connection handling
2. Verify server sends proper close codes
3. Check for server errors in backend logs
4. Increase `maxReconnectInterval` if needed

### Missing Updates

**Problem**: UI doesn't update when messages received

**Solutions**:
1. Check message format matches expected schema
2. Verify Zustand store methods are called
3. Check component is subscribed to correct store slice
4. Enable debug logging in hook

### Memory Leaks

**Problem**: Memory usage grows over time

**Solutions**:
1. Verify cleanup in `useEffect` return function
2. Check for proper interval/timeout clearing
3. Ensure WebSocket is closed on unmount
4. Use React DevTools Profiler to identify leaks

## Future Enhancements

### 1. Message Queuing

Queue messages when disconnected, send on reconnect:

```typescript
const messageQueue = useRef<unknown[]>([]);

const send = useCallback((data: unknown) => {
  if (isConnected) {
    wsRef.current?.send(JSON.stringify(data));
  } else {
    messageQueue.current.push(data);
  }
}, [isConnected]);
```

### 2. Binary Message Support

Support binary data (images, files):

```typescript
ws.onmessage = (event) => {
  if (event.data instanceof Blob) {
    // Handle binary data
  } else {
    // Handle text data
  }
};
```

### 3. Compression

Enable permessage-deflate extension:

```typescript
const ws = new WebSocket(url, {
  perMessageDeflate: true,
});
```

### 4. Metrics & Analytics

Track connection metrics:

```typescript
const metrics = {
  totalReconnects: 0,
  averageLatency: 0,
  messagesReceived: 0,
  messagesSent: 0,
};
```

## Integration Checklist

- [x] WebSocket slice added to Zustand store
- [x] useWebSocket hook implemented
- [x] Exponential backoff reconnection
- [x] Heartbeat mechanism (30s ping/pong)
- [x] Event handlers for task/agent/calendar updates
- [x] UI components (Indicator, Badge, Provider)
- [x] TypeScript types and interfaces
- [x] Comprehensive unit tests
- [x] Environment configuration
- [x] Documentation
- [ ] Backend WebSocket server implementation
- [ ] Integration testing with live server
- [ ] Production deployment with WSS

## Related Tasks

- **P1_T7**: Frontend scaffold (✅ Completed)
- **P3_T1**: Zustand state management (✅ Completed)
- **P3_T2**: Calendar component (Pending)
- **P3_T3**: Agent activity visualization (Pending)
- **P3_T5**: Backend WebSocket server (Pending)

## References

- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Zustand Documentation](https://docs.pmnd.rs/zustand/getting-started/introduction)
- [React Hooks Best Practices](https://react.dev/reference/react)
- [WebSocket Protocol RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)
