# WebSocket Hook - useWebSocket

## Quick Start

```tsx
import { useWebSocket } from './hooks/useWebSocket';
import { WebSocketIndicator } from './components/WebSocketIndicator';

function App() {
  // Auto-connects on mount, disconnects on unmount
  useWebSocket();

  return (
    <div>
      <WebSocketIndicator />
      {/* Your app content */}
    </div>
  );
}
```

## Features

✅ **Automatic connection/disconnection** - Connects on mount, cleans up on unmount
✅ **Exponential backoff reconnection** - 1s → 2s → 4s → 8s → 16s → 30s (max)
✅ **Heartbeat mechanism** - Sends ping every 30s, expects pong response
✅ **Real-time event handling** - task_status_update, agent_activity_update, calendar_event_created
✅ **Connection status tracking** - connecting, connected, reconnecting, disconnected
✅ **Zustand integration** - Updates store automatically on message receipt
✅ **TypeScript strict mode** - Full type safety with discriminated unions
✅ **Comprehensive tests** - 90%+ code coverage

## Configuration

Create `.env` file:

```bash
VITE_WS_URL=ws://localhost:8080/ws
```

## Advanced Usage

### Custom Configuration

```tsx
useWebSocket({
  url: 'wss://production.com/ws',
  reconnectInterval: 2000,
  maxReconnectInterval: 60000,
  heartbeatInterval: 15000,
});
```

### Manual Control

```tsx
const { send, disconnect, reconnect } = useWebSocket();

// Send custom message
send({ type: 'subscribe', channels: ['tasks'] });

// Manual disconnect
disconnect();

// Manual reconnect
reconnect();
```

### Access Connection State

```tsx
import { useStore } from '../store';

const { isConnected, connectionStatus, error } = useStore();
```

## Message Types

### Task Status Update
```json
{
  "type": "task_status_update",
  "payload": {
    "taskId": "task-123",
    "status": "in_progress",
    "assignee": "agent-1",
    "updatedAt": "2025-11-08T12:00:00Z"
  }
}
```

### Agent Activity Update
```json
{
  "type": "agent_activity_update",
  "payload": {
    "agentId": "agent-123",
    "status": "busy",
    "currentTask": "task-456",
    "timestamp": "2025-11-08T12:00:00Z"
  }
}
```

### Calendar Event Created
```json
{
  "type": "calendar_event_created",
  "payload": {
    "id": "event-123",
    "title": "Team Meeting",
    "start": "2025-11-08T14:00:00Z",
    "end": "2025-11-08T15:00:00Z"
  }
}
```

## UI Components

### Full Indicator

```tsx
<WebSocketIndicator />
```

Shows: Status text, colored dot, reconnect count, error tooltip

### Compact Badge

```tsx
<WebSocketBadge />
```

Shows: 2px status dot only

## Testing

```bash
# Run tests
npm test useWebSocket.test.ts

# Run with coverage
npm test -- --coverage
```

## Documentation

See `docs/websocket-client-implementation.md` for complete documentation.

## Example

See `src/examples/WebSocketExample.tsx` for interactive demo.
