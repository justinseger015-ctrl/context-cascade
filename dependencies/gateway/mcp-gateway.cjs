/**
 * MCP Gateway Proxy
 * Phase 6.2 Gateway Architecture
 *
 * Centralized gateway for MCP server communication.
 * Inspired by Docker MCP Gateway and IBM Context Forge.
 *
 * @module dependencies/gateway/mcp-gateway
 */

const { spawn, exec } = require('child_process');
const { EventEmitter } = require('events');
const path = require('path');
const fs = require('fs');

// Project paths
const PROJECT_ROOT = path.join(__dirname, '..', '..');

/**
 * Gateway configuration
 */
const GATEWAY_CONFIG = {
  maxConnections: 10,
  connectionTimeout: 30000,
  healthCheckInterval: 60000,
  retryAttempts: 3,
  retryDelay: 1000
};

/**
 * MCP Server connection states
 */
const ConnectionState = {
  DISCONNECTED: 'disconnected',
  CONNECTING: 'connecting',
  CONNECTED: 'connected',
  ERROR: 'error'
};

/**
 * Individual MCP server connection
 */
class MCPServerConnection extends EventEmitter {
  constructor(serverId, config) {
    super();
    this.serverId = serverId;
    this.config = config;
    this.state = ConnectionState.DISCONNECTED;
    this.process = null;
    this.lastActivity = null;
    this.errorCount = 0;
    this.messageQueue = [];
  }

  /**
   * Start the MCP server process
   * @returns {Promise<boolean>} Success
   */
  async connect() {
    if (this.state === ConnectionState.CONNECTED) {
      return true;
    }

    this.state = ConnectionState.CONNECTING;
    this.emit('connecting', { serverId: this.serverId });

    try {
      const { command, args, cwd, env } = this.config;

      // Spawn the MCP server process
      this.process = spawn(command, args || [], {
        cwd: cwd || process.cwd(),
        env: { ...process.env, ...env },
        stdio: ['pipe', 'pipe', 'pipe']
      });

      // Handle stdout (MCP responses)
      this.process.stdout.on('data', (data) => {
        this.lastActivity = Date.now();
        this.emit('message', {
          serverId: this.serverId,
          data: data.toString()
        });
      });

      // Handle stderr (errors/logs)
      this.process.stderr.on('data', (data) => {
        this.emit('log', {
          serverId: this.serverId,
          level: 'error',
          message: data.toString()
        });
      });

      // Handle process exit
      this.process.on('exit', (code, signal) => {
        this.state = ConnectionState.DISCONNECTED;
        this.emit('disconnected', {
          serverId: this.serverId,
          code,
          signal
        });
      });

      // Handle process error
      this.process.on('error', (err) => {
        this.state = ConnectionState.ERROR;
        this.errorCount++;
        this.emit('error', {
          serverId: this.serverId,
          error: err.message
        });
      });

      this.state = ConnectionState.CONNECTED;
      this.lastActivity = Date.now();
      this.emit('connected', { serverId: this.serverId });
      return true;

    } catch (err) {
      this.state = ConnectionState.ERROR;
      this.errorCount++;
      this.emit('error', {
        serverId: this.serverId,
        error: err.message
      });
      return false;
    }
  }

  /**
   * Send message to MCP server
   * @param {Object} message - JSON-RPC message
   * @returns {boolean} Success
   */
  send(message) {
    if (this.state !== ConnectionState.CONNECTED || !this.process) {
      this.messageQueue.push(message);
      return false;
    }

    try {
      const data = JSON.stringify(message) + '\n';
      this.process.stdin.write(data);
      this.lastActivity = Date.now();
      return true;
    } catch (err) {
      this.emit('error', {
        serverId: this.serverId,
        error: `Send failed: ${err.message}`
      });
      return false;
    }
  }

  /**
   * Disconnect from MCP server
   */
  disconnect() {
    if (this.process) {
      this.process.kill('SIGTERM');
      this.process = null;
    }
    this.state = ConnectionState.DISCONNECTED;
    this.emit('disconnected', { serverId: this.serverId });
  }

  /**
   * Get connection status
   * @returns {Object} Status
   */
  getStatus() {
    return {
      serverId: this.serverId,
      state: this.state,
      lastActivity: this.lastActivity,
      errorCount: this.errorCount,
      queuedMessages: this.messageQueue.length
    };
  }
}

/**
 * MCP Gateway - manages multiple server connections
 */
class MCPGateway extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = { ...GATEWAY_CONFIG, ...config };
    this.connections = new Map();
    this.healthCheckTimer = null;
    this.requestId = 0;
    this.pendingRequests = new Map();
  }

  /**
   * Load MCP server configurations
   * @param {string} configPath - Path to .mcp.json
   * @returns {Object} Loaded config
   */
  loadConfig(configPath) {
    const fullPath = configPath || path.join(PROJECT_ROOT, '.mcp.json');
    try {
      if (fs.existsSync(fullPath)) {
        return JSON.parse(fs.readFileSync(fullPath, 'utf8'));
      }
    } catch (err) {
      this.emit('error', { error: `Config load failed: ${err.message}` });
    }
    return { mcpServers: {} };
  }

  /**
   * Initialize gateway with servers from config
   * @param {string} configPath - Optional config path
   */
  initialize(configPath) {
    const config = this.loadConfig(configPath);

    for (const [serverId, serverConfig] of Object.entries(config.mcpServers || {})) {
      this.registerServer(serverId, serverConfig);
    }

    // Start health checks
    this.startHealthChecks();

    this.emit('initialized', {
      serverCount: this.connections.size
    });
  }

  /**
   * Register an MCP server
   * @param {string} serverId - Server identifier
   * @param {Object} config - Server configuration
   */
  registerServer(serverId, config) {
    if (this.connections.has(serverId)) {
      this.emit('warning', { message: `Server ${serverId} already registered` });
      return;
    }

    const connection = new MCPServerConnection(serverId, config);

    // Forward events
    connection.on('connected', (data) => this.emit('server:connected', data));
    connection.on('disconnected', (data) => this.emit('server:disconnected', data));
    connection.on('message', (data) => this.handleMessage(data));
    connection.on('error', (data) => this.emit('server:error', data));
    connection.on('log', (data) => this.emit('server:log', data));

    this.connections.set(serverId, connection);
    this.emit('server:registered', { serverId });
  }

  /**
   * Unregister an MCP server
   * @param {string} serverId - Server identifier
   */
  unregisterServer(serverId) {
    const connection = this.connections.get(serverId);
    if (connection) {
      connection.disconnect();
      this.connections.delete(serverId);
      this.emit('server:unregistered', { serverId });
    }
  }

  /**
   * Connect to a specific server
   * @param {string} serverId - Server identifier
   * @returns {Promise<boolean>} Success
   */
  async connectServer(serverId) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      this.emit('error', { error: `Server ${serverId} not registered` });
      return false;
    }
    return connection.connect();
  }

  /**
   * Connect to all registered servers
   * @returns {Promise<Object>} Results
   */
  async connectAll() {
    const results = {};
    for (const [serverId, connection] of this.connections) {
      results[serverId] = await connection.connect();
    }
    return results;
  }

  /**
   * Disconnect from a specific server
   * @param {string} serverId - Server identifier
   */
  disconnectServer(serverId) {
    const connection = this.connections.get(serverId);
    if (connection) {
      connection.disconnect();
    }
  }

  /**
   * Disconnect from all servers
   */
  disconnectAll() {
    for (const connection of this.connections.values()) {
      connection.disconnect();
    }
  }

  /**
   * Send request to MCP server
   * @param {string} serverId - Target server
   * @param {string} method - JSON-RPC method
   * @param {Object} params - Method parameters
   * @returns {Promise<Object>} Response
   */
  async request(serverId, method, params = {}) {
    const connection = this.connections.get(serverId);
    if (!connection) {
      throw new Error(`Server ${serverId} not registered`);
    }

    if (connection.state !== ConnectionState.CONNECTED) {
      await this.connectServer(serverId);
    }

    const id = ++this.requestId;
    const message = {
      jsonrpc: '2.0',
      id,
      method,
      params
    };

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pendingRequests.delete(id);
        reject(new Error(`Request timeout: ${method}`));
      }, this.config.connectionTimeout);

      this.pendingRequests.set(id, { resolve, reject, timeout, serverId });
      connection.send(message);
    });
  }

  /**
   * Handle incoming message from server
   * @param {Object} data - Message data
   */
  handleMessage(data) {
    try {
      const message = JSON.parse(data.data);

      if (message.id && this.pendingRequests.has(message.id)) {
        const pending = this.pendingRequests.get(message.id);
        clearTimeout(pending.timeout);
        this.pendingRequests.delete(message.id);

        if (message.error) {
          pending.reject(new Error(message.error.message || 'Unknown error'));
        } else {
          pending.resolve(message.result);
        }
      } else {
        // Notification or event
        this.emit('notification', {
          serverId: data.serverId,
          message
        });
      }
    } catch (err) {
      // Non-JSON message (log output)
      this.emit('server:output', {
        serverId: data.serverId,
        raw: data.data
      });
    }
  }

  /**
   * Start health check timer
   */
  startHealthChecks() {
    if (this.healthCheckTimer) {
      clearInterval(this.healthCheckTimer);
    }

    this.healthCheckTimer = setInterval(() => {
      this.performHealthChecks();
    }, this.config.healthCheckInterval);
  }

  /**
   * Stop health check timer
   */
  stopHealthChecks() {
    if (this.healthCheckTimer) {
      clearInterval(this.healthCheckTimer);
      this.healthCheckTimer = null;
    }
  }

  /**
   * Perform health checks on all servers
   */
  async performHealthChecks() {
    const results = {};

    for (const [serverId, connection] of this.connections) {
      const status = connection.getStatus();
      results[serverId] = {
        ...status,
        healthy: status.state === ConnectionState.CONNECTED,
        lastCheck: Date.now()
      };

      // Auto-reconnect if disconnected
      if (status.state === ConnectionState.DISCONNECTED) {
        this.emit('health:reconnecting', { serverId });
        await this.connectServer(serverId);
      }
    }

    this.emit('health:check', results);
    return results;
  }

  /**
   * Get gateway status
   * @returns {Object} Status
   */
  getStatus() {
    const servers = {};
    for (const [serverId, connection] of this.connections) {
      servers[serverId] = connection.getStatus();
    }

    return {
      serverCount: this.connections.size,
      connectedCount: Array.from(this.connections.values())
        .filter(c => c.state === ConnectionState.CONNECTED).length,
      pendingRequests: this.pendingRequests.size,
      servers
    };
  }

  /**
   * List available tools across all servers
   * @returns {Promise<Object>} Tools by server
   */
  async listTools() {
    const tools = {};

    for (const serverId of this.connections.keys()) {
      try {
        const result = await this.request(serverId, 'tools/list');
        tools[serverId] = result.tools || [];
      } catch (err) {
        tools[serverId] = { error: err.message };
      }
    }

    return tools;
  }

  /**
   * Call a tool on a specific server
   * @param {string} serverId - Server identifier
   * @param {string} toolName - Tool name
   * @param {Object} args - Tool arguments
   * @returns {Promise<Object>} Tool result
   */
  async callTool(serverId, toolName, args = {}) {
    return this.request(serverId, 'tools/call', {
      name: toolName,
      arguments: args
    });
  }

  /**
   * Shutdown gateway
   */
  shutdown() {
    this.stopHealthChecks();
    this.disconnectAll();
    this.emit('shutdown');
  }
}

/**
 * Create gateway instance
 * @param {Object} config - Gateway config
 * @returns {MCPGateway} Gateway instance
 */
function createGateway(config = {}) {
  return new MCPGateway(config);
}

// Export
module.exports = {
  MCPGateway,
  MCPServerConnection,
  ConnectionState,
  GATEWAY_CONFIG,
  createGateway
};

// Run if executed directly
if (require.main === module) {
  const gateway = createGateway();

  gateway.on('initialized', (data) => {
    console.log(`[Gateway] Initialized with ${data.serverCount} servers`);
  });

  gateway.on('server:connected', (data) => {
    console.log(`[Gateway] Connected: ${data.serverId}`);
  });

  gateway.on('server:error', (data) => {
    console.log(`[Gateway] Error: ${data.serverId} - ${data.error}`);
  });

  gateway.initialize();
  console.log('\n[Gateway] Status:', JSON.stringify(gateway.getStatus(), null, 2));
}
