/**
 * WebSocket Helper for E2E Testing
 * Handles real-time WebSocket connections and message verification
 */

import { Page } from '@playwright/test';

export interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: string;
}

export class WebSocketHelper {
  private page: Page;
  private wsUrl: string;
  private connected: boolean = false;
  private messageHandlers: Map<string, ((data: any) => void)[]> = new Map();
  private messageLog: WebSocketMessage[] = [];

  constructor(page: Page, wsUrl?: string) {
    this.page = page;
    this.wsUrl = wsUrl || process.env.WS_URL || 'ws://localhost:8000/ws';
  }

  /**
   * Connect to WebSocket server
   */
  async connect(): Promise<void> {
    if (this.connected) {
      return;
    }

    await this.page.evaluate((url) => {
      // @ts-ignore - Injecting WebSocket into page context
      window.testWebSocket = new WebSocket(url);

      // @ts-ignore
      window.testWebSocket.addEventListener('open', () => {
        // @ts-ignore
        window.testWebSocketConnected = true;
      });

      // @ts-ignore
      window.testWebSocket.addEventListener('message', (event) => {
        const message = JSON.parse(event.data);
        // @ts-ignore
        if (!window.testWebSocketMessages) {
          // @ts-ignore
          window.testWebSocketMessages = [];
        }
        // @ts-ignore
        window.testWebSocketMessages.push({
          type: message.type,
          data: message.data || message,
          timestamp: new Date().toISOString(),
        });
      });

      // @ts-ignore
      window.testWebSocket.addEventListener('error', (error) => {
        console.error('WebSocket error:', error);
      });
    }, this.wsUrl);

    // Wait for connection
    await this.page.waitForFunction(() => {
      // @ts-ignore
      return window.testWebSocketConnected === true;
    }, { timeout: 10000 });

    this.connected = true;

    // Start polling for messages
    this.startMessagePolling();
  }

  /**
   * Disconnect from WebSocket
   */
  async disconnect(): Promise<void> {
    if (!this.connected) {
      return;
    }

    await this.page.evaluate(() => {
      // @ts-ignore
      if (window.testWebSocket) {
        // @ts-ignore
        window.testWebSocket.close();
        // @ts-ignore
        window.testWebSocketConnected = false;
      }
    });

    this.connected = false;
  }

  /**
   * Register message handler for specific message type
   */
  async onMessage(messageType: string, handler: (data: any) => void): Promise<void> {
    if (!this.messageHandlers.has(messageType)) {
      this.messageHandlers.set(messageType, []);
    }
    this.messageHandlers.get(messageType)!.push(handler);
  }

  /**
   * Wait for specific message with optional matching criteria
   */
  async waitForMessage(
    messageType: string,
    matchCriteria?: Partial<any>,
    timeout: number = 10000
  ): Promise<any> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      // Get messages from page context
      const messages = await this.page.evaluate(() => {
        // @ts-ignore
        return window.testWebSocketMessages || [];
      });

      // Find matching message
      const matchingMessage = messages.find((msg: WebSocketMessage) => {
        if (msg.type !== messageType) {
          return false;
        }

        if (!matchCriteria) {
          return true;
        }

        // Check if all criteria match
        return Object.keys(matchCriteria).every((key) => {
          return msg.data[key] === matchCriteria[key];
        });
      });

      if (matchingMessage) {
        return matchingMessage;
      }

      // Wait before next poll
      await this.page.waitForTimeout(100);
    }

    throw new Error(
      `Timeout waiting for message type "${messageType}" with criteria ${JSON.stringify(matchCriteria)}`
    );
  }

  /**
   * Get all messages of a specific type
   */
  async getMessages(messageType: string): Promise<WebSocketMessage[]> {
    const messages = await this.page.evaluate(() => {
      // @ts-ignore
      return window.testWebSocketMessages || [];
    });

    return messages.filter((msg: WebSocketMessage) => msg.type === messageType);
  }

  /**
   * Clear message log
   */
  async clearMessages(): Promise<void> {
    await this.page.evaluate(() => {
      // @ts-ignore
      window.testWebSocketMessages = [];
    });
  }

  /**
   * Send message through WebSocket
   */
  async sendMessage(type: string, data: any): Promise<void> {
    if (!this.connected) {
      throw new Error('WebSocket not connected');
    }

    await this.page.evaluate(
      ({ type, data }) => {
        // @ts-ignore
        window.testWebSocket.send(JSON.stringify({ type, data }));
      },
      { type, data }
    );
  }

  /**
   * Check if WebSocket is connected
   */
  async isConnected(): Promise<boolean> {
    if (!this.connected) {
      return false;
    }

    return await this.page.evaluate(() => {
      // @ts-ignore
      return window.testWebSocket?.readyState === WebSocket.OPEN;
    });
  }

  /**
   * Start polling for messages and trigger handlers
   */
  private startMessagePolling(): void {
    // This runs in the test context, polling page context for messages
    const poll = async () => {
      if (!this.connected) {
        return;
      }

      const messages = await this.page.evaluate(() => {
        // @ts-ignore
        const msgs = window.testWebSocketMessages || [];
        // @ts-ignore
        window.testWebSocketMessages = []; // Clear after reading
        return msgs;
      });

      // Trigger handlers for each message
      for (const message of messages) {
        this.messageLog.push(message);

        const handlers = this.messageHandlers.get(message.type);
        if (handlers) {
          handlers.forEach((handler) => handler(message.data));
        }
      }

      // Continue polling
      setTimeout(poll, 100);
    };

    poll();
  }

  /**
   * Get full message log
   */
  getMessageLog(): WebSocketMessage[] {
    return [...this.messageLog];
  }
}
