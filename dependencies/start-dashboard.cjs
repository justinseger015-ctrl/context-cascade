/**
 * Full Dashboard Starter with Session Manager
 * Starts admin dashboard with health monitor, gateway, and MCP session management
 */

const http = require('http');
const { createAdminDashboard, HTMLGenerator } = require('./admin/admin-dashboard.cjs');
const { createHealthMonitor } = require('./health/health-monitor.cjs');
const { createGateway } = require('./gateway/mcp-gateway.cjs');
const { createTelemetry } = require('./observability/telemetry.cjs');
const { MCPSessionManager, generateSessionManagerHTML } = require('./admin/mcp-session-manager.cjs');

async function main() {
  console.log('[Startup] Initializing MCP Admin System with Session Manager...\n');

  // Create session manager
  const sessionManager = new MCPSessionManager();
  sessionManager.on('catalog:loaded', (d) => console.log(`[Session] Catalog: ${d.count} MCPs available`));
  sessionManager.on('active:loaded', (d) => console.log(`[Session] Active: ${d.count} MCPs enabled`));
  sessionManager.on('profile:applied', (d) => console.log(`[Session] Profile applied: ${d.mcpCount} MCPs`));
  sessionManager.on('config:saved', (d) => console.log(`[Session] Config saved: ${d.count} MCPs`));
  sessionManager.loadCatalog();
  sessionManager.loadActive();

  // Create telemetry
  const telemetry = createTelemetry('mcp-admin');
  console.log('[Startup] Telemetry initialized');

  // Create gateway
  const gateway = createGateway();
  gateway.on('server:registered', (data) => {
    console.log(`[Gateway] Registered: ${data.serverId}`);
  });
  gateway.initialize();
  console.log(`[Startup] Gateway initialized (${gateway.getStatus().serverCount} servers from .mcp.json)`);

  // Create health monitor
  const monitor = createHealthMonitor();
  monitor.on('server:registered', (data) => {
    console.log(`[Health] Registered: ${data.serverId}`);
  });
  monitor.loadServers();
  console.log(`[Startup] Health monitor initialized (${monitor.getSummary().total} servers)`);

  // Create custom server with session routes
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const pathname = url.pathname;

    console.log(`[Request] ${req.method} ${pathname}`);

    // Session Manager routes
    if (pathname === '/session') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(generateSessionManagerHTML(sessionManager));
      return;
    }

    if (pathname.startsWith('/api/session/')) {
      res.setHeader('Content-Type', 'application/json');

      // GET /api/session/status
      if (pathname === '/api/session/status' && req.method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify(sessionManager.getStatus()));
        return;
      }

      // GET /api/session/catalog
      if (pathname === '/api/session/catalog' && req.method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify(sessionManager.getAllMCPs()));
        return;
      }

      // POST /api/session/profile/:id
      const profileMatch = pathname.match(/^\/api\/session\/profile\/(.+)$/);
      if (profileMatch && req.method === 'POST') {
        const profileId = profileMatch[1];
        sessionManager.applyProfile(profileId);
        res.writeHead(200);
        res.end(JSON.stringify({
          success: true,
          profileId,
          activeMCPs: Object.keys(sessionManager.active)
        }));
        return;
      }

      // POST /api/session/save
      if (pathname === '/api/session/save' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
          try {
            const { mcps } = JSON.parse(body);
            // Clear and set new active MCPs
            sessionManager.active = {};
            for (const mcpId of mcps) {
              if (sessionManager.catalog[mcpId]) {
                sessionManager.active[mcpId] = sessionManager.catalog[mcpId];
              }
            }
            sessionManager.save();
            res.writeHead(200);
            res.end(JSON.stringify({
              success: true,
              count: Object.keys(sessionManager.active).length
            }));
          } catch (err) {
            res.writeHead(400);
            res.end(JSON.stringify({ error: err.message }));
          }
        });
        return;
      }

      // POST /api/session/enable/:id
      const enableMatch = pathname.match(/^\/api\/session\/enable\/(.+)$/);
      if (enableMatch && req.method === 'POST') {
        sessionManager.enable(enableMatch[1]);
        res.writeHead(200);
        res.end(JSON.stringify({ success: true }));
        return;
      }

      // POST /api/session/disable/:id
      const disableMatch = pathname.match(/^\/api\/session\/disable\/(.+)$/);
      if (disableMatch && req.method === 'POST') {
        sessionManager.disable(disableMatch[1]);
        res.writeHead(200);
        res.end(JSON.stringify({ success: true }));
        return;
      }
    }

    // Admin dashboard routes
    if (pathname === '/' || pathname === '/dashboard') {
      const data = collectDashboardData(monitor, gateway, telemetry, sessionManager);
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(HTMLGenerator.dashboard(data));
      return;
    }

    if (pathname === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(monitor.getSummary()));
      return;
    }

    if (pathname === '/api/status') {
      const data = collectDashboardData(monitor, gateway, telemetry, sessionManager);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(data));
      return;
    }

    if (pathname === '/api/servers') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(monitor.getAllHealth()));
      return;
    }

    // 404
    res.writeHead(404, { 'Content-Type': 'text/html' });
    res.end(HTMLGenerator.error('Page not found'));
  });

  function collectDashboardData(monitor, gateway, telemetry, sessionManager) {
    const summary = monitor.getSummary();
    const health = monitor.getAllHealth();
    const servers = [];

    for (const [id, h] of Object.entries(health)) {
      servers.push({
        id,
        status: h.status,
        responseTime: h.responseTime,
        failures: h.consecutiveFailures,
        lastCheck: h.lastCheck ? new Date(h.lastCheck).toISOString().split('T')[1].split('.')[0] : 'Never'
      });
    }

    return {
      summary,
      gateway: {
        serverCount: gateway.getStatus().serverCount,
        connectedCount: gateway.getStatus().connectedCount,
        pendingRequests: gateway.getStatus().pendingRequests
      },
      telemetry: { activeSpans: 0 },
      session: sessionManager.getStatus(),
      servers,
      logs: []
    };
  }

  // Start server
  const PORT = 8765;
  server.listen(PORT, 'localhost', () => {
    console.log(`\n[Dashboard] Started at http://localhost:${PORT}`);
    console.log(`[Session]   MCP Session Manager at http://localhost:${PORT}/session`);
    console.log('\n[Startup] All systems ready!\n');
    console.log('Quick Links:');
    console.log(`  Dashboard:       http://localhost:${PORT}/`);
    console.log(`  Session Manager: http://localhost:${PORT}/session`);
    console.log(`  Health Check:    http://localhost:${PORT}/health`);
    console.log('\nPress Ctrl+C to stop\n');
  });

  // Handle shutdown
  process.on('SIGINT', () => {
    console.log('\n[Shutdown] Stopping services...');
    server.close();
    monitor.stop();
    gateway.shutdown();
    telemetry.shutdown();
    console.log('[Shutdown] Complete');
    process.exit(0);
  });
}

main();
