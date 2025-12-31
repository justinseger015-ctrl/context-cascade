/**
 * MCP Health Monitoring System
 * Phase 6.4 Health Monitoring
 *
 * Automatic health checks, failure detection, and alerting for MCP servers.
 * Inspired by Docker Gateway health probes and Kubernetes liveness checks.
 *
 * @module dependencies/health/health-monitor
 */

const { EventEmitter } = require('events');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Project paths
const PROJECT_ROOT = path.join(__dirname, '..', '..');

/**
 * Health check configuration
 */
const HEALTH_CONFIG = {
  checkInterval: 30000,      // 30 seconds between checks
  timeout: 10000,            // 10 second timeout per check
  failureThreshold: 3,       // Failures before unhealthy
  successThreshold: 1,       // Successes to restore healthy
  autoRestart: true,         // Auto-restart unhealthy servers
  maxRestarts: 3,            // Max restarts before giving up
  restartCooldown: 60000     // 1 minute between restarts
};

/**
 * Health status enum
 */
const HealthStatus = {
  UNKNOWN: 'unknown',
  HEALTHY: 'healthy',
  UNHEALTHY: 'unhealthy',
  DEGRADED: 'degraded',
  STARTING: 'starting',
  STOPPED: 'stopped'
};

/**
 * Server health state
 */
class ServerHealthState {
  constructor(serverId) {
    this.serverId = serverId;
    this.status = HealthStatus.UNKNOWN;
    this.consecutiveFailures = 0;
    this.consecutiveSuccesses = 0;
    this.lastCheck = null;
    this.lastSuccess = null;
    this.lastFailure = null;
    this.lastError = null;
    this.restartCount = 0;
    this.lastRestart = null;
    this.responseTime = null;
    this.history = [];
  }

  /**
   * Record a successful health check
   * @param {number} responseTime - Response time in ms
   */
  recordSuccess(responseTime) {
    this.consecutiveSuccesses++;
    this.consecutiveFailures = 0;
    this.lastCheck = Date.now();
    this.lastSuccess = Date.now();
    this.responseTime = responseTime;
    this.lastError = null;

    this.addToHistory({
      timestamp: Date.now(),
      success: true,
      responseTime
    });

    if (this.consecutiveSuccesses >= HEALTH_CONFIG.successThreshold) {
      this.status = HealthStatus.HEALTHY;
    }
  }

  /**
   * Record a failed health check
   * @param {string} error - Error message
   */
  recordFailure(error) {
    this.consecutiveFailures++;
    this.consecutiveSuccesses = 0;
    this.lastCheck = Date.now();
    this.lastFailure = Date.now();
    this.lastError = error;

    this.addToHistory({
      timestamp: Date.now(),
      success: false,
      error
    });

    if (this.consecutiveFailures >= HEALTH_CONFIG.failureThreshold) {
      this.status = HealthStatus.UNHEALTHY;
    } else if (this.consecutiveFailures > 0) {
      this.status = HealthStatus.DEGRADED;
    }
  }

  /**
   * Record a restart attempt
   */
  recordRestart() {
    this.restartCount++;
    this.lastRestart = Date.now();
    this.status = HealthStatus.STARTING;
    this.consecutiveFailures = 0;
    this.consecutiveSuccesses = 0;
  }

  /**
   * Add entry to history (keep last 100)
   * @param {Object} entry - History entry
   */
  addToHistory(entry) {
    this.history.push(entry);
    if (this.history.length > 100) {
      this.history.shift();
    }
  }

  /**
   * Check if server can be restarted
   * @returns {boolean} Can restart
   */
  canRestart() {
    if (this.restartCount >= HEALTH_CONFIG.maxRestarts) {
      return false;
    }
    if (this.lastRestart) {
      const elapsed = Date.now() - this.lastRestart;
      if (elapsed < HEALTH_CONFIG.restartCooldown) {
        return false;
      }
    }
    return true;
  }

  /**
   * Get health summary
   * @returns {Object} Health summary
   */
  toJSON() {
    return {
      serverId: this.serverId,
      status: this.status,
      consecutiveFailures: this.consecutiveFailures,
      consecutiveSuccesses: this.consecutiveSuccesses,
      lastCheck: this.lastCheck,
      lastSuccess: this.lastSuccess,
      lastFailure: this.lastFailure,
      lastError: this.lastError,
      responseTime: this.responseTime,
      restartCount: this.restartCount,
      lastRestart: this.lastRestart,
      historyLength: this.history.length
    };
  }
}

/**
 * Health check probe
 */
class HealthProbe {
  constructor(serverId, serverConfig) {
    this.serverId = serverId;
    this.config = serverConfig;
    this.probeType = this.detectProbeType();
  }

  /**
   * Detect probe type based on server configuration
   * @returns {string} Probe type
   */
  detectProbeType() {
    const { command, args } = this.config;

    // Check for HTTP health endpoint
    if (args && args.some(a => a.includes('--health-port'))) {
      return 'http';
    }

    // Default to process check
    return 'process';
  }

  /**
   * Run health check
   * @returns {Promise<Object>} Check result
   */
  async check() {
    const startTime = Date.now();

    try {
      let result;

      switch (this.probeType) {
        case 'http':
          result = await this.httpCheck();
          break;
        case 'process':
        default:
          result = await this.processCheck();
          break;
      }

      const responseTime = Date.now() - startTime;
      return {
        success: result.success,
        responseTime,
        details: result.details
      };

    } catch (err) {
      return {
        success: false,
        responseTime: Date.now() - startTime,
        error: err.message
      };
    }
  }

  /**
   * Process-based health check (verify server responds to JSON-RPC)
   * @returns {Promise<Object>} Check result
   */
  async processCheck() {
    return new Promise((resolve) => {
      const { command, args, env, cwd } = this.config;

      // Spawn a quick test process
      const proc = spawn(command, args || [], {
        cwd: cwd || process.cwd(),
        env: { ...process.env, ...env },
        stdio: ['pipe', 'pipe', 'pipe'],
        timeout: HEALTH_CONFIG.timeout
      });

      let stdout = '';
      let stderr = '';
      let responded = false;

      // Send initialize request
      const initRequest = JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'initialize',
        params: {
          protocolVersion: '2024-11-05',
          clientInfo: { name: 'health-check', version: '1.0.0' },
          capabilities: {}
        }
      }) + '\n';

      const timeout = setTimeout(() => {
        if (!responded) {
          proc.kill('SIGTERM');
          resolve({
            success: false,
            details: 'Health check timeout'
          });
        }
      }, HEALTH_CONFIG.timeout);

      proc.stdout.on('data', (data) => {
        stdout += data.toString();
        // Check for valid JSON-RPC response
        try {
          const response = JSON.parse(stdout.trim().split('\n').pop());
          if (response.result && response.result.protocolVersion) {
            responded = true;
            clearTimeout(timeout);
            proc.kill('SIGTERM');
            resolve({
              success: true,
              details: {
                protocolVersion: response.result.protocolVersion,
                serverInfo: response.result.serverInfo
              }
            });
          }
        } catch (e) {
          // Not complete JSON yet
        }
      });

      proc.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      proc.on('error', (err) => {
        responded = true;
        clearTimeout(timeout);
        resolve({
          success: false,
          details: `Process error: ${err.message}`
        });
      });

      proc.on('exit', (code) => {
        if (!responded) {
          responded = true;
          clearTimeout(timeout);
          resolve({
            success: false,
            details: `Process exited with code ${code}`
          });
        }
      });

      // Send the init request
      try {
        proc.stdin.write(initRequest);
      } catch (e) {
        responded = true;
        clearTimeout(timeout);
        resolve({
          success: false,
          details: `Failed to write to stdin: ${e.message}`
        });
      }
    });
  }

  /**
   * HTTP-based health check
   * @returns {Promise<Object>} Check result
   */
  async httpCheck() {
    // Extract health port from args
    const portArg = this.config.args.find(a => a.includes('--health-port'));
    const port = portArg ? portArg.split('=')[1] : 8080;

    return new Promise((resolve) => {
      const http = require('http');
      const req = http.get(`http://localhost:${port}/health`, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          resolve({
            success: res.statusCode === 200,
            details: {
              statusCode: res.statusCode,
              body: data
            }
          });
        });
      });

      req.on('error', (err) => {
        resolve({
          success: false,
          details: `HTTP error: ${err.message}`
        });
      });

      req.setTimeout(HEALTH_CONFIG.timeout, () => {
        req.destroy();
        resolve({
          success: false,
          details: 'HTTP timeout'
        });
      });
    });
  }
}

/**
 * Health Monitor - manages health checks for all MCP servers
 */
class HealthMonitor extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = { ...HEALTH_CONFIG, ...config };
    this.servers = new Map();      // serverId -> serverConfig
    this.states = new Map();       // serverId -> ServerHealthState
    this.probes = new Map();       // serverId -> HealthProbe
    this.checkTimer = null;
    this.isRunning = false;
  }

  /**
   * Load MCP server configurations
   * @param {string} configPath - Path to .mcp.json
   */
  loadServers(configPath) {
    const fullPath = configPath || path.join(PROJECT_ROOT, '.mcp.json');
    try {
      if (fs.existsSync(fullPath)) {
        const config = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
        for (const [serverId, serverConfig] of Object.entries(config.mcpServers || {})) {
          this.registerServer(serverId, serverConfig);
        }
      }
    } catch (err) {
      this.emit('error', { error: `Config load failed: ${err.message}` });
    }
  }

  /**
   * Register a server for monitoring
   * @param {string} serverId - Server identifier
   * @param {Object} serverConfig - Server configuration
   */
  registerServer(serverId, serverConfig) {
    this.servers.set(serverId, serverConfig);
    this.states.set(serverId, new ServerHealthState(serverId));
    this.probes.set(serverId, new HealthProbe(serverId, serverConfig));
    this.emit('server:registered', { serverId });
  }

  /**
   * Unregister a server
   * @param {string} serverId - Server identifier
   */
  unregisterServer(serverId) {
    this.servers.delete(serverId);
    this.states.delete(serverId);
    this.probes.delete(serverId);
    this.emit('server:unregistered', { serverId });
  }

  /**
   * Start health monitoring
   */
  start() {
    if (this.isRunning) return;

    this.isRunning = true;
    this.emit('started');

    // Run initial checks
    this.runAllChecks();

    // Start periodic checks
    this.checkTimer = setInterval(() => {
      this.runAllChecks();
    }, this.config.checkInterval);
  }

  /**
   * Stop health monitoring
   */
  stop() {
    if (!this.isRunning) return;

    this.isRunning = false;
    if (this.checkTimer) {
      clearInterval(this.checkTimer);
      this.checkTimer = null;
    }
    this.emit('stopped');
  }

  /**
   * Run health checks on all servers
   */
  async runAllChecks() {
    const results = {};

    for (const serverId of this.servers.keys()) {
      results[serverId] = await this.checkServer(serverId);
    }

    this.emit('checks:complete', results);
    return results;
  }

  /**
   * Run health check on a specific server
   * @param {string} serverId - Server identifier
   * @returns {Promise<Object>} Check result
   */
  async checkServer(serverId) {
    const probe = this.probes.get(serverId);
    const state = this.states.get(serverId);

    if (!probe || !state) {
      return { error: `Server ${serverId} not registered` };
    }

    this.emit('check:start', { serverId });

    const result = await probe.check();

    if (result.success) {
      state.recordSuccess(result.responseTime);
      this.emit('check:success', {
        serverId,
        responseTime: result.responseTime,
        details: result.details
      });
    } else {
      state.recordFailure(result.error || result.details);
      this.emit('check:failure', {
        serverId,
        error: result.error || result.details,
        consecutiveFailures: state.consecutiveFailures
      });

      // Check if auto-restart is needed
      if (this.config.autoRestart &&
          state.status === HealthStatus.UNHEALTHY &&
          state.canRestart()) {
        this.emit('restart:triggered', { serverId });
        state.recordRestart();
      }
    }

    return {
      serverId,
      ...result,
      status: state.status,
      consecutiveFailures: state.consecutiveFailures
    };
  }

  /**
   * Get health status of a specific server
   * @param {string} serverId - Server identifier
   * @returns {Object} Health status
   */
  getServerHealth(serverId) {
    const state = this.states.get(serverId);
    return state ? state.toJSON() : null;
  }

  /**
   * Get health status of all servers
   * @returns {Object} All health statuses
   */
  getAllHealth() {
    const health = {};
    for (const [serverId, state] of this.states) {
      health[serverId] = state.toJSON();
    }
    return health;
  }

  /**
   * Get summary statistics
   * @returns {Object} Summary stats
   */
  getSummary() {
    let healthy = 0;
    let unhealthy = 0;
    let degraded = 0;
    let unknown = 0;

    for (const state of this.states.values()) {
      switch (state.status) {
        case HealthStatus.HEALTHY:
          healthy++;
          break;
        case HealthStatus.UNHEALTHY:
          unhealthy++;
          break;
        case HealthStatus.DEGRADED:
          degraded++;
          break;
        default:
          unknown++;
      }
    }

    return {
      total: this.states.size,
      healthy,
      unhealthy,
      degraded,
      unknown,
      isRunning: this.isRunning
    };
  }

  /**
   * Get unhealthy servers
   * @returns {string[]} List of unhealthy server IDs
   */
  getUnhealthyServers() {
    const unhealthy = [];
    for (const [serverId, state] of this.states) {
      if (state.status === HealthStatus.UNHEALTHY) {
        unhealthy.push(serverId);
      }
    }
    return unhealthy;
  }

  /**
   * Generate health report
   * @returns {string} Markdown report
   */
  generateReport() {
    const summary = this.getSummary();
    const all = this.getAllHealth();

    let report = `# MCP Health Report

**Generated**: ${new Date().toISOString()}
**Monitoring Status**: ${this.isRunning ? 'Running' : 'Stopped'}

## Summary

| Metric | Value |
|--------|-------|
| Total Servers | ${summary.total} |
| Healthy | ${summary.healthy} |
| Unhealthy | ${summary.unhealthy} |
| Degraded | ${summary.degraded} |
| Unknown | ${summary.unknown} |

## Server Status

| Server | Status | Response Time | Failures | Last Check |
|--------|--------|---------------|----------|------------|
`;

    for (const [serverId, health] of Object.entries(all)) {
      const statusEmoji = health.status === HealthStatus.HEALTHY ? 'OK' :
                          health.status === HealthStatus.UNHEALTHY ? 'FAIL' :
                          health.status === HealthStatus.DEGRADED ? 'WARN' : '?';
      const lastCheck = health.lastCheck ?
        new Date(health.lastCheck).toISOString() : 'Never';
      const responseTime = health.responseTime ? `${health.responseTime}ms` : '-';

      report += `| ${serverId} | ${statusEmoji} | ${responseTime} | ${health.consecutiveFailures} | ${lastCheck} |\n`;
    }

    const unhealthy = this.getUnhealthyServers();
    if (unhealthy.length > 0) {
      report += `\n## Unhealthy Servers (Action Required)\n\n`;
      for (const serverId of unhealthy) {
        const health = all[serverId];
        report += `### ${serverId}\n\n`;
        report += `- **Status**: ${health.status}\n`;
        report += `- **Consecutive Failures**: ${health.consecutiveFailures}\n`;
        report += `- **Last Error**: ${health.lastError || 'Unknown'}\n`;
        report += `- **Restart Count**: ${health.restartCount}\n\n`;
      }
    }

    return report;
  }
}

/**
 * Create health monitor instance
 * @param {Object} config - Monitor configuration
 * @returns {HealthMonitor} Health monitor instance
 */
function createHealthMonitor(config = {}) {
  return new HealthMonitor(config);
}

// Export
module.exports = {
  HealthMonitor,
  HealthProbe,
  ServerHealthState,
  HealthStatus,
  HEALTH_CONFIG,
  createHealthMonitor
};

// Run if executed directly
if (require.main === module) {
  const monitor = createHealthMonitor();

  monitor.on('server:registered', (data) => {
    console.log(`[Health] Registered: ${data.serverId}`);
  });

  monitor.on('check:success', (data) => {
    console.log(`[Health] OK: ${data.serverId} (${data.responseTime}ms)`);
  });

  monitor.on('check:failure', (data) => {
    console.log(`[Health] FAIL: ${data.serverId} - ${data.error}`);
  });

  monitor.loadServers();
  console.log('\n[Health] Summary:', JSON.stringify(monitor.getSummary(), null, 2));
}
