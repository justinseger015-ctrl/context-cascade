/**
 * MCP Admin Dashboard
 * Phase 6.5 Admin Interface
 *
 * Lightweight admin dashboard for MCP monitoring and configuration.
 * Inspired by IBM Context Forge HTMX-based admin UI.
 *
 * @module dependencies/admin/admin-dashboard
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { EventEmitter } = require('events');

// Project paths
const PROJECT_ROOT = path.join(__dirname, '..', '..');
const LOG_DIR = path.join(PROJECT_ROOT, 'logs');

/**
 * Dashboard configuration
 */
const DASHBOARD_CONFIG = {
  port: 8765,
  host: 'localhost',
  refreshInterval: 5000,
  maxLogLines: 500,
  logTailSize: 100
};

/**
 * HTML template generator
 */
class HTMLGenerator {
  /**
   * Generate main dashboard page
   * @param {Object} data - Dashboard data
   * @returns {string} HTML content
   */
  static dashboard(data) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MCP Admin Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #0a0a0a;
      color: #e0e0e0;
      line-height: 1.6;
    }
    .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 0;
      border-bottom: 1px solid #333;
      margin-bottom: 20px;
    }
    h1 { color: #4fc3f7; font-size: 1.5rem; }
    .status-badge {
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.85rem;
      font-weight: 500;
    }
    .status-healthy { background: #1b5e20; color: #a5d6a7; }
    .status-unhealthy { background: #b71c1c; color: #ef9a9a; }
    .status-degraded { background: #e65100; color: #ffcc80; }
    .status-unknown { background: #424242; color: #bdbdbd; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
    .card {
      background: #1a1a1a;
      border-radius: 8px;
      padding: 20px;
      border: 1px solid #333;
    }
    .card h2 {
      color: #81d4fa;
      font-size: 1rem;
      margin-bottom: 15px;
      padding-bottom: 10px;
      border-bottom: 1px solid #333;
    }
    .stat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .stat {
      background: #252525;
      padding: 12px;
      border-radius: 6px;
      text-align: center;
    }
    .stat-value { font-size: 1.5rem; font-weight: bold; color: #4fc3f7; }
    .stat-label { font-size: 0.75rem; color: #888; text-transform: uppercase; }
    table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #333; }
    th { color: #888; font-weight: 500; text-transform: uppercase; font-size: 0.75rem; }
    .log-viewer {
      background: #0d0d0d;
      border-radius: 6px;
      padding: 15px;
      max-height: 400px;
      overflow-y: auto;
      font-family: 'Monaco', 'Menlo', monospace;
      font-size: 0.8rem;
    }
    .log-line { padding: 2px 0; white-space: pre-wrap; word-break: break-all; }
    .log-error { color: #ef5350; }
    .log-warn { color: #ffb74d; }
    .log-info { color: #4fc3f7; }
    .log-debug { color: #888; }
    .refresh-btn {
      background: #1e88e5;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.9rem;
    }
    .refresh-btn:hover { background: #1565c0; }
    .actions { display: flex; gap: 10px; }
    .action-btn {
      background: #333;
      color: #e0e0e0;
      border: 1px solid #444;
      padding: 6px 12px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.8rem;
    }
    .action-btn:hover { background: #444; }
    .action-btn.danger { border-color: #b71c1c; color: #ef5350; }
    .action-btn.danger:hover { background: #b71c1c; color: white; }
    footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #333;
      text-align: center;
      color: #666;
      font-size: 0.8rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>MCP Admin Dashboard</h1>
      <div class="actions">
        <span class="status-badge ${data.summary.unhealthy > 0 ? 'status-unhealthy' : 'status-healthy'}">
          ${data.summary.unhealthy > 0 ? 'Issues Detected' : 'All Systems OK'}
        </span>
        <button class="refresh-btn" onclick="location.reload()">Refresh</button>
      </div>
    </header>

    <div class="grid">
      <div class="card">
        <h2>System Overview</h2>
        <div class="stat-grid">
          <div class="stat">
            <div class="stat-value">${data.summary.total}</div>
            <div class="stat-label">Total Servers</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="color: #66bb6a;">${data.summary.healthy}</div>
            <div class="stat-label">Healthy</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="color: #ef5350;">${data.summary.unhealthy}</div>
            <div class="stat-label">Unhealthy</div>
          </div>
          <div class="stat">
            <div class="stat-value" style="color: #ffb74d;">${data.summary.degraded}</div>
            <div class="stat-label">Degraded</div>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>Gateway Status</h2>
        <div class="stat-grid">
          <div class="stat">
            <div class="stat-value">${data.gateway.serverCount}</div>
            <div class="stat-label">Registered</div>
          </div>
          <div class="stat">
            <div class="stat-value">${data.gateway.connectedCount}</div>
            <div class="stat-label">Connected</div>
          </div>
          <div class="stat">
            <div class="stat-value">${data.gateway.pendingRequests}</div>
            <div class="stat-label">Pending Requests</div>
          </div>
          <div class="stat">
            <div class="stat-value">${data.telemetry.activeSpans}</div>
            <div class="stat-label">Active Spans</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card" style="margin-top: 20px;">
      <h2>Server Status</h2>
      <table>
        <thead>
          <tr>
            <th>Server</th>
            <th>Status</th>
            <th>Type</th>
            <th>Response Time</th>
            <th>Failures</th>
            <th>Last Check</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          ${data.servers.map(s => `
          <tr>
            <td><strong>${s.id}</strong></td>
            <td>
              <span class="status-badge status-${s.status}">${s.status}</span>
            </td>
            <td>${s.type || '-'}</td>
            <td>${s.responseTime ? s.responseTime + 'ms' : '-'}</td>
            <td>${s.failures}</td>
            <td>${s.lastCheck}</td>
            <td>
              <div class="actions">
                <button class="action-btn" onclick="restartServer('${s.id}')">Restart</button>
                <button class="action-btn danger" onclick="stopServer('${s.id}')">Stop</button>
              </div>
            </td>
          </tr>
          `).join('')}
        </tbody>
      </table>
    </div>

    <div class="card" style="margin-top: 20px;">
      <h2>Recent Logs</h2>
      <div class="log-viewer">
        ${data.logs.map(l => `
        <div class="log-line log-${l.level}">[${l.timestamp}] ${l.level.toUpperCase()} ${l.message}</div>
        `).join('')}
      </div>
    </div>

    <footer>
      Context Cascade MCP Admin | Last Updated: ${new Date().toISOString()}
    </footer>
  </div>

  <script>
    function restartServer(id) {
      if (confirm('Restart server ' + id + '?')) {
        fetch('/api/servers/' + id + '/restart', { method: 'POST' })
          .then(() => location.reload());
      }
    }
    function stopServer(id) {
      if (confirm('Stop server ' + id + '?')) {
        fetch('/api/servers/' + id + '/stop', { method: 'POST' })
          .then(() => location.reload());
      }
    }
    // Auto-refresh every ${DASHBOARD_CONFIG.refreshInterval / 1000} seconds
    setTimeout(() => location.reload(), ${DASHBOARD_CONFIG.refreshInterval});
  </script>
</body>
</html>`;
  }

  /**
   * Generate API JSON response
   * @param {Object} data - Response data
   * @returns {string} JSON string
   */
  static json(data) {
    return JSON.stringify(data, null, 2);
  }

  /**
   * Generate error page
   * @param {string} message - Error message
   * @returns {string} HTML content
   */
  static error(message) {
    return `<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body style="background:#0a0a0a;color:#ef5350;font-family:sans-serif;padding:40px;">
  <h1>Error</h1>
  <p>${message}</p>
  <a href="/" style="color:#4fc3f7;">Back to Dashboard</a>
</body>
</html>`;
  }
}

/**
 * Admin Dashboard Server
 */
class AdminDashboard extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = { ...DASHBOARD_CONFIG, ...config };
    this.server = null;
    this.healthMonitor = null;
    this.gateway = null;
    this.telemetry = null;
  }

  /**
   * Set health monitor reference
   * @param {Object} monitor - HealthMonitor instance
   */
  setHealthMonitor(monitor) {
    this.healthMonitor = monitor;
  }

  /**
   * Set gateway reference
   * @param {Object} gateway - MCPGateway instance
   */
  setGateway(gateway) {
    this.gateway = gateway;
  }

  /**
   * Set telemetry reference
   * @param {Object} telemetry - Telemetry instance
   */
  setTelemetry(telemetry) {
    this.telemetry = telemetry;
  }

  /**
   * Collect dashboard data
   * @returns {Object} Dashboard data
   */
  collectData() {
    const data = {
      summary: { total: 0, healthy: 0, unhealthy: 0, degraded: 0, unknown: 0 },
      gateway: { serverCount: 0, connectedCount: 0, pendingRequests: 0 },
      telemetry: { activeSpans: 0 },
      servers: [],
      logs: []
    };

    // Health monitor data
    if (this.healthMonitor) {
      const summary = this.healthMonitor.getSummary();
      data.summary = summary;

      const health = this.healthMonitor.getAllHealth();
      for (const [id, h] of Object.entries(health)) {
        data.servers.push({
          id,
          status: h.status,
          responseTime: h.responseTime,
          failures: h.consecutiveFailures,
          lastCheck: h.lastCheck ? this.formatTime(h.lastCheck) : 'Never'
        });
      }
    }

    // Gateway data
    if (this.gateway) {
      const status = this.gateway.getStatus();
      data.gateway = {
        serverCount: status.serverCount,
        connectedCount: status.connectedCount,
        pendingRequests: status.pendingRequests
      };

      // Add server types from gateway
      for (const [id, server] of Object.entries(status.servers || {})) {
        const existing = data.servers.find(s => s.id === id);
        if (existing) {
          existing.type = server.type || 'unknown';
        }
      }
    }

    // Telemetry data
    if (this.telemetry) {
      data.telemetry.activeSpans = this.telemetry.tracer?.activeSpans?.size || 0;
    }

    // Collect logs
    data.logs = this.collectLogs();

    return data;
  }

  /**
   * Collect recent logs from log files
   * @returns {Object[]} Log entries
   */
  collectLogs() {
    const logs = [];

    try {
      if (!fs.existsSync(LOG_DIR)) {
        return logs;
      }

      const files = fs.readdirSync(LOG_DIR)
        .filter(f => f.endsWith('.log'))
        .slice(0, 5);

      for (const file of files) {
        const content = fs.readFileSync(path.join(LOG_DIR, file), 'utf8');
        const lines = content.trim().split('\n').slice(-this.config.logTailSize);

        for (const line of lines) {
          try {
            const entry = JSON.parse(line);
            logs.push({
              timestamp: this.formatTime(new Date(entry.timestamp).getTime()),
              level: entry.level?.toLowerCase() || 'info',
              message: entry.message || line
            });
          } catch (e) {
            logs.push({
              timestamp: this.formatTime(Date.now()),
              level: 'info',
              message: line
            });
          }
        }
      }
    } catch (err) {
      logs.push({
        timestamp: this.formatTime(Date.now()),
        level: 'error',
        message: `Log collection failed: ${err.message}`
      });
    }

    return logs.slice(-this.config.maxLogLines).reverse();
  }

  /**
   * Format timestamp for display
   * @param {number} ts - Timestamp
   * @returns {string} Formatted time
   */
  formatTime(ts) {
    const d = new Date(ts);
    return d.toISOString().replace('T', ' ').split('.')[0];
  }

  /**
   * Handle HTTP request
   * @param {Object} req - HTTP request
   * @param {Object} res - HTTP response
   */
  handleRequest(req, res) {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const pathname = url.pathname;

    this.emit('request', { method: req.method, path: pathname });

    try {
      // API routes
      if (pathname.startsWith('/api/')) {
        return this.handleAPI(req, res, pathname);
      }

      // Dashboard route
      if (pathname === '/' || pathname === '/dashboard') {
        const data = this.collectData();
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(HTMLGenerator.dashboard(data));
        return;
      }

      // Health endpoint
      if (pathname === '/health') {
        const data = this.healthMonitor ? this.healthMonitor.getSummary() : { status: 'no monitor' };
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(HTMLGenerator.json(data));
        return;
      }

      // 404
      res.writeHead(404, { 'Content-Type': 'text/html' });
      res.end(HTMLGenerator.error('Page not found'));

    } catch (err) {
      this.emit('error', { error: err.message });
      res.writeHead(500, { 'Content-Type': 'text/html' });
      res.end(HTMLGenerator.error(err.message));
    }
  }

  /**
   * Handle API requests
   * @param {Object} req - HTTP request
   * @param {Object} res - HTTP response
   * @param {string} pathname - URL path
   */
  handleAPI(req, res, pathname) {
    res.setHeader('Content-Type', 'application/json');

    // GET /api/status
    if (pathname === '/api/status' && req.method === 'GET') {
      res.writeHead(200);
      res.end(HTMLGenerator.json(this.collectData()));
      return;
    }

    // GET /api/servers
    if (pathname === '/api/servers' && req.method === 'GET') {
      const data = this.healthMonitor ? this.healthMonitor.getAllHealth() : {};
      res.writeHead(200);
      res.end(HTMLGenerator.json(data));
      return;
    }

    // GET /api/logs
    if (pathname === '/api/logs' && req.method === 'GET') {
      res.writeHead(200);
      res.end(HTMLGenerator.json(this.collectLogs()));
      return;
    }

    // POST /api/servers/:id/restart
    const restartMatch = pathname.match(/^\/api\/servers\/([^/]+)\/restart$/);
    if (restartMatch && req.method === 'POST') {
      const serverId = restartMatch[1];
      this.emit('server:restart', { serverId });
      res.writeHead(200);
      res.end(HTMLGenerator.json({ success: true, action: 'restart', serverId }));
      return;
    }

    // POST /api/servers/:id/stop
    const stopMatch = pathname.match(/^\/api\/servers\/([^/]+)\/stop$/);
    if (stopMatch && req.method === 'POST') {
      const serverId = stopMatch[1];
      this.emit('server:stop', { serverId });
      res.writeHead(200);
      res.end(HTMLGenerator.json({ success: true, action: 'stop', serverId }));
      return;
    }

    // 404 for unknown API routes
    res.writeHead(404);
    res.end(HTMLGenerator.json({ error: 'API endpoint not found' }));
  }

  /**
   * Start the dashboard server
   * @returns {Promise<void>}
   */
  start() {
    return new Promise((resolve, reject) => {
      this.server = http.createServer((req, res) => {
        this.handleRequest(req, res);
      });

      this.server.on('error', (err) => {
        if (err.code === 'EADDRINUSE') {
          this.emit('error', { error: `Port ${this.config.port} already in use` });
          reject(err);
        } else {
          this.emit('error', { error: err.message });
          reject(err);
        }
      });

      this.server.listen(this.config.port, this.config.host, () => {
        this.emit('started', {
          url: `http://${this.config.host}:${this.config.port}`
        });
        resolve();
      });
    });
  }

  /**
   * Stop the dashboard server
   * @returns {Promise<void>}
   */
  stop() {
    return new Promise((resolve) => {
      if (this.server) {
        this.server.close(() => {
          this.emit('stopped');
          resolve();
        });
      } else {
        resolve();
      }
    });
  }

  /**
   * Get dashboard URL
   * @returns {string} Dashboard URL
   */
  getURL() {
    return `http://${this.config.host}:${this.config.port}`;
  }
}

/**
 * Create admin dashboard instance
 * @param {Object} config - Dashboard configuration
 * @returns {AdminDashboard} Dashboard instance
 */
function createAdminDashboard(config = {}) {
  return new AdminDashboard(config);
}

// Export
module.exports = {
  AdminDashboard,
  HTMLGenerator,
  DASHBOARD_CONFIG,
  createAdminDashboard
};

// Run if executed directly
if (require.main === module) {
  const dashboard = createAdminDashboard();

  dashboard.on('started', (data) => {
    console.log(`[Dashboard] Started at ${data.url}`);
  });

  dashboard.on('request', (data) => {
    console.log(`[Dashboard] ${data.method} ${data.path}`);
  });

  dashboard.on('error', (data) => {
    console.log(`[Dashboard] Error: ${data.error}`);
  });

  dashboard.start().then(() => {
    console.log('\n[Dashboard] Admin interface ready');
    console.log(`[Dashboard] Open http://localhost:${DASHBOARD_CONFIG.port} in browser`);
  }).catch(err => {
    console.error('[Dashboard] Failed to start:', err.message);
  });
}
