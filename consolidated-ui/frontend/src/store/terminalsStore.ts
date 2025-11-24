import { create } from 'zustand';

/**
 * Terminal Interface
 * Matches backend API response from /api/v1/terminals/
 */
export interface Terminal {
  id: string;
  project_id: string;
  working_dir: string;
  status: 'active' | 'idle' | 'stopped' | 'error';
  pid?: number;
}

/**
 * Terminal Message Types
 * WebSocket message formats from /ws/terminals/{id}
 */
export interface TerminalMessage {
  type: 'stdout' | 'stderr' | 'status' | 'error' | 'connected';
  line?: string;
  status?: string;
  exit_code?: number;
  message?: string;
  timestamp?: number;
}

/**
 * Terminals Store State
 */
interface TerminalsState {
  // State
  terminals: Terminal[];
  selectedTerminalId: string | null;
  messages: Map<string, TerminalMessage[]>;
  connectionStatus: Map<string, 'connected' | 'connecting' | 'disconnected' | 'error'>;

  // Actions
  setTerminals: (terminals: Terminal[]) => void;
  selectTerminal: (id: string) => void;
  getTerminal: (id: string) => Terminal | undefined;
  getMessages: (id: string) => TerminalMessage[];
  addMessage: (id: string, message: TerminalMessage) => void;
  clearMessages: (id: string) => void;
  getConnectionStatus: (id: string) => string;
  setConnectionStatus: (id: string, status: 'connected' | 'connecting' | 'disconnected' | 'error') => void;
}

/**
 * Zustand Store for Terminal State Management
 */
export const useTerminalsStore = create<TerminalsState>((set, get) => ({
  // Initial state
  terminals: [],
  selectedTerminalId: null,
  messages: new Map(),
  connectionStatus: new Map(),

  // Set all terminals (from API fetch)
  setTerminals: (terminals: Terminal[]) => {
    set({ terminals });
  },

  // Select a terminal by ID
  selectTerminal: (id: string) => {
    const terminal = get().terminals.find((t) => t.id === id);
    if (terminal) {
      set({ selectedTerminalId: id });
    }
  },

  // Get terminal by ID
  getTerminal: (id: string) => {
    return get().terminals.find((t) => t.id === id);
  },

  // Get messages for a terminal
  getMessages: (id: string) => {
    return get().messages.get(id) || [];
  },

  // Add a message to a terminal
  addMessage: (id: string, message: TerminalMessage) => {
    set((state) => {
      const messages = new Map(state.messages);
      const terminalMessages = messages.get(id) || [];

      // Add timestamp if not present
      const timestampedMessage = {
        ...message,
        timestamp: message.timestamp || Date.now(),
      };

      // Append message
      messages.set(id, [...terminalMessages, timestampedMessage]);

      return { messages };
    });
  },

  // Clear messages for a terminal
  clearMessages: (id: string) => {
    set((state) => {
      const messages = new Map(state.messages);
      messages.delete(id);
      return { messages };
    });
  },

  // Get connection status for a terminal
  getConnectionStatus: (id: string) => {
    return get().connectionStatus.get(id) || 'disconnected';
  },

  // Set connection status for a terminal
  setConnectionStatus: (id: string, status: 'connected' | 'connecting' | 'disconnected' | 'error') => {
    set((state) => {
      const connectionStatus = new Map(state.connectionStatus);
      connectionStatus.set(id, status);
      return { connectionStatus };
    });
  },
}));
