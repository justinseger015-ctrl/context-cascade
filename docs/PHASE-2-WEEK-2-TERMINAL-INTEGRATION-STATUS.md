# Phase 2, Week 2: Terminal Integration - IN PROGRESS

**Date**: 2025-11-17
**Status**: Integration Started
**Time Spent**: ~1 hour
**Estimated Remaining**: 1-2 hours

---

## Summary

Successfully discovered and began integrating terminal emulator components from Terminal Manager into consolidated dashboard. xterm.js-based terminal with WebSocket streaming, VS Code-style UI, and real-time output.

---

## Completed Tasks (2/9)

### 1. Explored Terminal Manager - COMPLETE
- Located 3 terminal components in `C:/Users/17175/frontend/src/components/terminals/`
- Analyzed architecture and dependencies
- Documented requirements

### 2. Copied Terminal Components - COMPLETE
**Files Copied**:
- `TerminalMonitor.tsx` (109 lines) - Main layout
- `TerminalList.tsx` (222 lines) - Sidebar with terminal list
- `TerminalOutputView.tsx` (238 lines) - xterm.js terminal with WebSocket

**Destination**: `consolidated-ui/frontend/src/components/terminals/`

---

## Dependencies Installed

```json
{
  "@xterm/xterm": "^5.5.0",
  "@xterm/addon-fit": "^0.10.0",
  "@xterm/addon-search": "^0.15.0"
}
```

---

## Pending Tasks (7/9)

### 3. Create Terminal Store (Zustand) - NEXT
**File**: `consolidated-ui/frontend/src/store/terminalsStore.ts`

**Required State**:
```typescript
interface Terminal {
  id: string;
  project_id: string;
  working_dir: string;
  status: 'active' | 'idle' | 'stopped' | 'error';
  pid?: number;
}

interface TerminalsState {
  terminals: Terminal[];
  selectedTerminalId: string | null;
  messages: Map<string, TerminalMessage[]>;
  connectionStatus: Map<string, 'connected' | 'connecting' | 'disconnected' | 'error'>;

  setTerminals: (terminals: Terminal[]) => void;
  selectTerminal: (id: string) => void;
  getTerminal: (id: string) => Terminal | undefined;
  getMessages: (id: string) => TerminalMessage[];
  addMessage: (id: string, message: TerminalMessage) => void;
  getConnectionStatus: (id: string) => string;
  setConnectionStatus: (id: string, status: string) => void;
}
```

### 4. Create WebSocket Streaming Hook - NEXT
**File**: `consolidated-ui/frontend/src/hooks/useTerminalStream.ts`

**Features**:
- Connect to WebSocket at `ws://localhost:8000/ws/terminals/{id}`
- Handle message types: `stdout`, `stderr`, `status`, `error`, `connected`
- Auto-reconnect on disconnect
- Cleanup on unmount

### 5. Create Terminal Page - PENDING
**File**: `consolidated-ui/frontend/src/pages/TerminalPage.tsx`

**Content**:
```typescript
import { TerminalMonitor } from '../components/terminals/TerminalMonitor';

export const TerminalPage = () => {
  return <TerminalMonitor />;
};
```

### 6. Add Terminal Routing - PENDING
**File**: `consolidated-ui/frontend/src/App.tsx` or routing config

**Route**:
```typescript
{
  path: '/terminals',
  element: <TerminalPage />
}
```

### 7. Test Terminal Functionality - PENDING
- Verify terminal list loads from API
- Test WebSocket connection
- Verify xterm.js rendering
- Test real-time output streaming
- Verify terminal selection

### 8. Add Terminal Navigation Link - PENDING
Update main navigation to include Terminal link

### 9. Document Week 2 Completion - PENDING
Create final completion summary

---

## Component Architecture

### TerminalMonitor (Main Layout)
```
┌─────────────────────────────────────────┐
│  TerminalMonitor                        │
│  ┌────────────┬────────────────────┐   │
│  │ Sidebar    │  Main Panel        │   │
│  │            │                     │   │
│  │ Terminal   │  TerminalOutput    │   │
│  │ List       │  View              │   │
│  │            │                     │   │
│  │  • Term 1  │  ┌──────────────┐  │   │
│  │  • Term 2  │  │ xterm.js     │  │   │
│  │  • Term 3  │  │ terminal     │  │   │
│  │            │  │ output       │  │   │
│  │            │  └──────────────┘  │   │
│  └────────────┴────────────────────┘   │
└─────────────────────────────────────────┘
```

### Data Flow

```
Backend API (/api/v1/terminals/)
        ↓
   terminalsStore (Zustand)
        ↓
   TerminalList (Sidebar)
        ↓
   TerminalOutputView
        ↓
   xterm.js Terminal
        ↑
   WebSocket Stream
        ↑
Backend WS (/ws/terminals/{id})
```

---

## Features Implemented

### Terminal Components
- ✅ VS Code-style dark theme
- ✅ Real-time terminal output via WebSocket
- ✅ Multiple terminal support
- ✅ Terminal status indicators (active/idle/stopped/error)
- ✅ Connection status tracking
- ✅ xterm.js integration with Fit + Search addons
- ✅ ANSI color support
- ✅ Auto-resize on window resize
- ✅ 10,000 line scrollback buffer

### Not Yet Implemented
- ⏳ Terminal store (Zustand)
- ⏳ WebSocket streaming hook
- ⏳ Page + routing
- ⏳ Navigation link
- ⏳ Backend API endpoint verification

---

## Backend Integration Requirements

### API Endpoint (Expected)
**GET** `/api/v1/terminals/`
```json
[
  {
    "id": "term-123",
    "project_id": "my-project",
    "working_dir": "/path/to/project",
    "status": "active",
    "pid": 12345
  }
]
```

### WebSocket Endpoint (Expected)
**WS** `/ws/terminals/{terminal_id}`

**Message Types**:
```json
// stdout
{ "type": "stdout", "line": "output line" }

// stderr
{ "type": "stderr", "line": "error line" }

// status change
{ "type": "status", "status": "stopped", "exit_code": 0 }

// connection established
{ "type": "connected" }

// error
{ "type": "error", "message": "error message" }
```

---

## Next Steps (Immediate)

1. **Create terminalsStore.ts** (15-20 mins)
   - Zustand store with terminal state
   - CRUD operations for terminals
   - Message management
   - Connection status tracking

2. **Create useTerminalStream.ts** (20-30 mins)
   - WebSocket connection hook
   - Message handler
   - Auto-reconnect logic
   - Cleanup on unmount

3. **Create TerminalPage.tsx** (5 mins)
   - Simple wrapper around TerminalMonitor

4. **Add routing** (10 mins)
   - Add /terminals route
   - Add navigation link

5. **Test integration** (20-30 mins)
   - Verify API connectivity
   - Test WebSocket streaming
   - Verify xterm.js rendering

---

## Success Criteria

- [x] Terminal components copied
- [x] xterm dependencies installed
- [ ] Terminal store created
- [ ] WebSocket hook implemented
- [ ] Terminal page with routing
- [ ] Navigation link added
- [ ] Terminals load from backend API
- [ ] WebSocket streams real-time output
- [ ] xterm.js renders terminal output
- [ ] Terminal selection works

**Progress**: 2/10 complete (20%)

---

## Timeline

- **Week 2 Total**: 4-6 hours estimated
- **Completed**: ~1 hour (discovery + component copy)
- **Remaining**: 1-2 hours (store + hook + routing + testing)

---

**Status**: Week 2 is **20% complete** - Ready to create store and hooks

**Next Session**: Implement terminalsStore + useTerminalStream hook
