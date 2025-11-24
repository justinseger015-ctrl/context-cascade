/**
 * API Response and Optimistic Update Types
 */

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Optimistic update types
export interface OptimisticUpdate<T> {
  id: string;
  type: 'create' | 'update' | 'delete';
  data: T;
  previousData?: T;
  timestamp: number;
}

export type WebSocketConnectionStatus = 'connected' | 'disconnected' | 'connecting' | 'error';

export interface WebSocketMessage {
  type: string;
  payload: unknown;
  timestamp: string;
}
