/**
 * Phase 6 Audit Test Suite
 * MCP Dependency Hardening Verification
 *
 * Tests all Phase 6 components:
 * - 6.1 Version Lockfile
 * - 6.2 Gateway Proxy
 * - 6.3 Observability Stack
 * - 6.4 Health Monitoring
 * - 6.5 Admin Interface
 *
 * @module dependencies/tests/phase6-audit
 */

const fs = require('fs');
const path = require('path');

// Test utilities
let passed = 0;
let failed = 0;
const results = [];

function test(name, fn) {
  try {
    fn();
    passed++;
    results.push({ name, status: 'PASS' });
    console.log(`  [PASS] ${name}`);
  } catch (err) {
    failed++;
    results.push({ name, status: 'FAIL', error: err.message });
    console.log(`  [FAIL] ${name}: ${err.message}`);
  }
}

function assertEqual(actual, expected, msg) {
  if (actual !== expected) {
    throw new Error(`${msg}: expected ${expected}, got ${actual}`);
  }
}

function assertTrue(value, msg) {
  if (!value) {
    throw new Error(msg || 'Expected true');
  }
}

function assertExists(obj, msg) {
  if (obj === undefined || obj === null) {
    throw new Error(msg || 'Expected value to exist');
  }
}

function assertType(obj, type, msg) {
  const actual = typeof obj;
  if (actual !== type) {
    throw new Error(`${msg}: expected type ${type}, got ${actual}`);
  }
}

// ============================================================
// Phase 6.1: Version Lockfile Tests
// ============================================================

console.log('\n=== Phase 6.1: Version Lockfile ===\n');

const lockfile = require('../version-lock/mcp-lockfile.cjs');

test('6.1.1 loadLockfile returns object', () => {
  const result = lockfile.loadLockfile();
  assertType(result, 'object', 'loadLockfile return type');
  assertExists(result.servers, 'servers property');
});

test('6.1.2 loadMCPConfig returns object', () => {
  const result = lockfile.loadMCPConfig();
  assertType(result, 'object', 'loadMCPConfig return type');
});

test('6.1.3 calculateConfigChecksum returns string', () => {
  const result = lockfile.calculateConfigChecksum({ command: 'npx', args: ['-y', 'test'] });
  assertType(result, 'string', 'checksum type');
  assertEqual(result.length, 16, 'checksum length');
});

test('6.1.4 verifyLockfile returns verification result', () => {
  const result = lockfile.verifyLockfile();
  assertType(result, 'object', 'verifyLockfile return type');
  assertExists(result.valid, 'valid property');
  assertExists(result.mismatches, 'mismatches property');
  assertExists(result.missing, 'missing property');
  assertExists(result.extra, 'extra property');
});

test('6.1.5 getUnpinnedPackages returns array', () => {
  const result = lockfile.getUnpinnedPackages();
  assertTrue(Array.isArray(result), 'getUnpinnedPackages should return array');
});

test('6.1.6 generatePinnedConfig returns config object', () => {
  const result = lockfile.generatePinnedConfig();
  assertType(result, 'object', 'generatePinnedConfig return type');
});

test('6.1.7 generateLockfileReport returns markdown', () => {
  const result = lockfile.generateLockfileReport();
  assertType(result, 'string', 'generateLockfileReport return type');
  assertTrue(result.includes('# MCP Lockfile Report'), 'Report should have header');
});

test('6.1.8 LOCKFILE_PATH is exported', () => {
  assertExists(lockfile.LOCKFILE_PATH, 'LOCKFILE_PATH should be exported');
  assertTrue(lockfile.LOCKFILE_PATH.includes('mcp-lock.json'), 'Should point to mcp-lock.json');
});

// ============================================================
// Phase 6.2: Gateway Proxy Tests
// ============================================================

console.log('\n=== Phase 6.2: Gateway Proxy ===\n');

const gateway = require('../gateway/mcp-gateway.cjs');

test('6.2.1 MCPGateway class exists', () => {
  assertExists(gateway.MCPGateway, 'MCPGateway class');
  const gw = new gateway.MCPGateway();
  assertType(gw, 'object', 'MCPGateway instance');
});

test('6.2.2 MCPServerConnection class exists', () => {
  assertExists(gateway.MCPServerConnection, 'MCPServerConnection class');
  const conn = new gateway.MCPServerConnection('test', { command: 'node' });
  assertType(conn, 'object', 'MCPServerConnection instance');
});

test('6.2.3 ConnectionState enum has all states', () => {
  const states = gateway.ConnectionState;
  assertEqual(states.DISCONNECTED, 'disconnected', 'DISCONNECTED state');
  assertEqual(states.CONNECTING, 'connecting', 'CONNECTING state');
  assertEqual(states.CONNECTED, 'connected', 'CONNECTED state');
  assertEqual(states.ERROR, 'error', 'ERROR state');
});

test('6.2.4 createGateway factory function works', () => {
  const gw = gateway.createGateway();
  assertExists(gw, 'createGateway result');
  assertTrue(gw instanceof gateway.MCPGateway, 'Should be MCPGateway instance');
});

test('6.2.5 Gateway registerServer method', () => {
  const gw = gateway.createGateway();
  gw.registerServer('test-server', { command: 'node', args: ['test.js'] });
  const status = gw.getStatus();
  assertEqual(status.serverCount, 1, 'Server count after registration');
});

test('6.2.6 Gateway unregisterServer method', () => {
  const gw = gateway.createGateway();
  gw.registerServer('test-server', { command: 'node' });
  gw.unregisterServer('test-server');
  const status = gw.getStatus();
  assertEqual(status.serverCount, 0, 'Server count after unregistration');
});

test('6.2.7 Gateway getStatus returns full status', () => {
  const gw = gateway.createGateway();
  const status = gw.getStatus();
  assertExists(status.serverCount, 'serverCount property');
  assertExists(status.connectedCount, 'connectedCount property');
  assertExists(status.pendingRequests, 'pendingRequests property');
  assertExists(status.servers, 'servers property');
});

test('6.2.8 GATEWAY_CONFIG has required settings', () => {
  const config = gateway.GATEWAY_CONFIG;
  assertExists(config.maxConnections, 'maxConnections');
  assertExists(config.connectionTimeout, 'connectionTimeout');
  assertExists(config.healthCheckInterval, 'healthCheckInterval');
  assertExists(config.retryAttempts, 'retryAttempts');
});

// ============================================================
// Phase 6.3: Observability Stack Tests
// ============================================================

console.log('\n=== Phase 6.3: Observability Stack ===\n');

const telemetry = require('../observability/telemetry.cjs');

test('6.3.1 Span class exists', () => {
  assertExists(telemetry.Span, 'Span class');
  const span = new telemetry.Span('test-span');
  assertExists(span.traceId, 'span.traceId');
  assertExists(span.spanId, 'span.spanId');
  assertEqual(span.name, 'test-span', 'span.name');
});

test('6.3.2 SpanStatus enum has all statuses', () => {
  assertEqual(telemetry.SpanStatus.UNSET, 'UNSET', 'UNSET status');
  assertEqual(telemetry.SpanStatus.OK, 'OK', 'OK status');
  assertEqual(telemetry.SpanStatus.ERROR, 'ERROR', 'ERROR status');
});

test('6.3.3 Tracer class creates spans', () => {
  const tracer = new telemetry.Tracer('test-service');
  const span = tracer.startSpan('test-operation');
  assertExists(span, 'span created');
  assertEqual(span.attributes['service.name'], 'test-service', 'service.name attribute');
});

test('6.3.4 MetricsCollector tracks counters', () => {
  const metrics = new telemetry.MetricsCollector('test');
  metrics.incrementCounter('test_counter', 1);
  metrics.incrementCounter('test_counter', 5);
  const all = metrics.getMetrics();
  assertExists(all.counters, 'counters property');
});

test('6.3.5 MetricsCollector tracks gauges', () => {
  const metrics = new telemetry.MetricsCollector('test');
  metrics.setGauge('test_gauge', 42);
  const all = metrics.getMetrics();
  assertExists(all.gauges, 'gauges property');
});

test('6.3.6 MetricsCollector tracks histograms', () => {
  const metrics = new telemetry.MetricsCollector('test');
  metrics.recordHistogram('test_histogram', 100);
  metrics.recordHistogram('test_histogram', 200);
  const all = metrics.getMetrics();
  assertExists(all.histograms, 'histograms property');
});

test('6.3.7 StructuredLogger logs messages', () => {
  const logger = new telemetry.StructuredLogger('test', { logLevel: 'error' });
  // Should not throw
  logger.info('test info');
  logger.error('test error');
  logger.stopFlushTimer();
  assertTrue(true, 'Logger works without errors');
});

test('6.3.8 createTelemetry factory returns complete object', () => {
  const t = telemetry.createTelemetry('test-service');
  assertExists(t.tracer, 'tracer');
  assertExists(t.metrics, 'metrics');
  assertExists(t.logger, 'logger');
  assertExists(t.startSpan, 'startSpan convenience method');
  assertExists(t.increment, 'increment convenience method');
  assertExists(t.gauge, 'gauge convenience method');
  t.shutdown();
});

test('6.3.9 generateTraceId returns valid format', () => {
  const traceId = telemetry.generateTraceId();
  assertEqual(traceId.length, 32, 'traceId should be 32 chars (16 bytes hex)');
  assertTrue(/^[0-9a-f]+$/.test(traceId), 'traceId should be hex');
});

test('6.3.10 generateSpanId returns valid format', () => {
  const spanId = telemetry.generateSpanId();
  assertEqual(spanId.length, 16, 'spanId should be 16 chars (8 bytes hex)');
  assertTrue(/^[0-9a-f]+$/.test(spanId), 'spanId should be hex');
});

// ============================================================
// Phase 6.4: Health Monitoring Tests
// ============================================================

console.log('\n=== Phase 6.4: Health Monitoring ===\n');

const health = require('../health/health-monitor.cjs');

test('6.4.1 HealthMonitor class exists', () => {
  assertExists(health.HealthMonitor, 'HealthMonitor class');
  const monitor = new health.HealthMonitor();
  assertType(monitor, 'object', 'HealthMonitor instance');
});

test('6.4.2 HealthStatus enum has all statuses', () => {
  const s = health.HealthStatus;
  assertEqual(s.UNKNOWN, 'unknown', 'UNKNOWN status');
  assertEqual(s.HEALTHY, 'healthy', 'HEALTHY status');
  assertEqual(s.UNHEALTHY, 'unhealthy', 'UNHEALTHY status');
  assertEqual(s.DEGRADED, 'degraded', 'DEGRADED status');
  assertEqual(s.STARTING, 'starting', 'STARTING status');
  assertEqual(s.STOPPED, 'stopped', 'STOPPED status');
});

test('6.4.3 ServerHealthState tracks state', () => {
  const state = new health.ServerHealthState('test');
  assertEqual(state.serverId, 'test', 'serverId');
  assertEqual(state.status, health.HealthStatus.UNKNOWN, 'initial status');
  state.recordSuccess(100);
  assertEqual(state.consecutiveSuccesses, 1, 'consecutiveSuccesses after success');
  assertEqual(state.responseTime, 100, 'responseTime');
});

test('6.4.4 ServerHealthState tracks failures', () => {
  const state = new health.ServerHealthState('test');
  state.recordFailure('Connection refused');
  assertEqual(state.consecutiveFailures, 1, 'consecutiveFailures after failure');
  assertEqual(state.lastError, 'Connection refused', 'lastError');
});

test('6.4.5 createHealthMonitor factory works', () => {
  const monitor = health.createHealthMonitor();
  assertExists(monitor, 'createHealthMonitor result');
  assertTrue(monitor instanceof health.HealthMonitor, 'Should be HealthMonitor instance');
});

test('6.4.6 HealthMonitor registerServer method', () => {
  const monitor = health.createHealthMonitor();
  monitor.registerServer('test', { command: 'node', args: ['test.js'] });
  const h = monitor.getServerHealth('test');
  assertExists(h, 'Server health should exist after registration');
  assertEqual(h.serverId, 'test', 'serverId in health');
});

test('6.4.7 HealthMonitor getSummary method', () => {
  const monitor = health.createHealthMonitor();
  monitor.registerServer('s1', { command: 'node' });
  monitor.registerServer('s2', { command: 'npx' });
  const summary = monitor.getSummary();
  assertEqual(summary.total, 2, 'total servers');
  assertExists(summary.healthy, 'healthy count');
  assertExists(summary.unhealthy, 'unhealthy count');
});

test('6.4.8 HealthMonitor generateReport returns markdown', () => {
  const monitor = health.createHealthMonitor();
  monitor.registerServer('test', { command: 'node' });
  const report = monitor.generateReport();
  assertTrue(report.includes('# MCP Health Report'), 'Report should have header');
  assertTrue(report.includes('test'), 'Report should include server name');
});

test('6.4.9 HEALTH_CONFIG has required settings', () => {
  const config = health.HEALTH_CONFIG;
  assertExists(config.checkInterval, 'checkInterval');
  assertExists(config.timeout, 'timeout');
  assertExists(config.failureThreshold, 'failureThreshold');
  assertExists(config.autoRestart, 'autoRestart');
});

// ============================================================
// Phase 6.5: Admin Interface Tests
// ============================================================

console.log('\n=== Phase 6.5: Admin Interface ===\n');

const admin = require('../admin/admin-dashboard.cjs');

test('6.5.1 AdminDashboard class exists', () => {
  assertExists(admin.AdminDashboard, 'AdminDashboard class');
  const dashboard = new admin.AdminDashboard();
  assertType(dashboard, 'object', 'AdminDashboard instance');
});

test('6.5.2 HTMLGenerator generates dashboard HTML', () => {
  const html = admin.HTMLGenerator.dashboard({
    summary: { total: 3, healthy: 2, unhealthy: 1, degraded: 0, unknown: 0 },
    gateway: { serverCount: 3, connectedCount: 2, pendingRequests: 0 },
    telemetry: { activeSpans: 5 },
    servers: [
      { id: 'test', status: 'healthy', responseTime: 100, failures: 0, lastCheck: 'now' }
    ],
    logs: [
      { timestamp: '2025-01-01', level: 'info', message: 'Test log' }
    ]
  });
  assertTrue(html.includes('<!DOCTYPE html>'), 'Should be valid HTML');
  assertTrue(html.includes('MCP Admin Dashboard'), 'Should have title');
  assertTrue(html.includes('test'), 'Should include server');
});

test('6.5.3 HTMLGenerator generates JSON', () => {
  const json = admin.HTMLGenerator.json({ test: true });
  assertEqual(json.includes('"test": true'), true, 'Should format JSON');
});

test('6.5.4 HTMLGenerator generates error page', () => {
  const html = admin.HTMLGenerator.error('Something went wrong');
  assertTrue(html.includes('Error'), 'Should have error title');
  assertTrue(html.includes('Something went wrong'), 'Should include message');
});

test('6.5.5 createAdminDashboard factory works', () => {
  const dashboard = admin.createAdminDashboard();
  assertExists(dashboard, 'createAdminDashboard result');
  assertTrue(dashboard instanceof admin.AdminDashboard, 'Should be AdminDashboard instance');
});

test('6.5.6 Dashboard setHealthMonitor method', () => {
  const dashboard = admin.createAdminDashboard();
  const mockMonitor = { getSummary: () => ({ total: 0 }) };
  dashboard.setHealthMonitor(mockMonitor);
  assertEqual(dashboard.healthMonitor, mockMonitor, 'healthMonitor should be set');
});

test('6.5.7 Dashboard setGateway method', () => {
  const dashboard = admin.createAdminDashboard();
  const mockGateway = { getStatus: () => ({}) };
  dashboard.setGateway(mockGateway);
  assertEqual(dashboard.gateway, mockGateway, 'gateway should be set');
});

test('6.5.8 Dashboard getURL method', () => {
  const dashboard = admin.createAdminDashboard({ port: 9999 });
  const url = dashboard.getURL();
  assertTrue(url.includes('9999'), 'URL should include port');
  assertTrue(url.includes('localhost'), 'URL should include host');
});

test('6.5.9 DASHBOARD_CONFIG has required settings', () => {
  const config = admin.DASHBOARD_CONFIG;
  assertExists(config.port, 'port');
  assertExists(config.host, 'host');
  assertExists(config.refreshInterval, 'refreshInterval');
  assertExists(config.maxLogLines, 'maxLogLines');
});

// ============================================================
// Integration Tests
// ============================================================

console.log('\n=== Integration Tests ===\n');

test('6.I.1 All modules have consistent exports', () => {
  // Each module should export a create* factory function
  assertExists(gateway.createGateway, 'gateway.createGateway');
  assertExists(telemetry.createTelemetry, 'telemetry.createTelemetry');
  assertExists(health.createHealthMonitor, 'health.createHealthMonitor');
  assertExists(admin.createAdminDashboard, 'admin.createAdminDashboard');
});

test('6.I.2 Dashboard can integrate with health monitor', () => {
  const monitor = health.createHealthMonitor();
  const dashboard = admin.createAdminDashboard();
  dashboard.setHealthMonitor(monitor);

  // Simulate server registration
  monitor.registerServer('integration-test', { command: 'node' });

  // Dashboard should see the server
  const data = dashboard.collectData();
  assertTrue(data.servers.length > 0, 'Dashboard should see servers from monitor');
});

test('6.I.3 Gateway and health monitor can share config', () => {
  const gw = gateway.createGateway();
  const monitor = health.createHealthMonitor();

  // Register same server in both
  const serverConfig = { command: 'node', args: ['test.js'] };
  gw.registerServer('shared-server', serverConfig);
  monitor.registerServer('shared-server', serverConfig);

  // Both should track it
  assertEqual(gw.getStatus().serverCount, 1, 'Gateway server count');
  assertEqual(monitor.getSummary().total, 1, 'Monitor server count');
});

test('6.I.4 Telemetry can trace gateway operations', () => {
  const t = telemetry.createTelemetry('integration-test');
  const gw = gateway.createGateway();

  // Start a trace for gateway operation
  const span = t.startSpan('gateway.register');
  span.setAttribute('server.id', 'traced-server');

  gw.registerServer('traced-server', { command: 'node' });

  span.setStatus(telemetry.SpanStatus.OK);
  t.endSpan(span);

  // Verify span was recorded
  const completed = t.tracer.getCompletedSpans();
  assertTrue(completed.length > 0, 'Should have completed span');
  assertEqual(completed[0].name, 'gateway.register', 'Span name');

  t.shutdown();
});

// ============================================================
// Final Summary
// ============================================================

console.log('\n========================================');
console.log(`Phase 6 Audit: ${passed} passed, ${failed} failed`);
console.log('========================================\n');

// Write results to file
const resultPath = path.join(__dirname, 'phase6-audit-results.json');
fs.writeFileSync(resultPath, JSON.stringify({
  timestamp: new Date().toISOString(),
  passed,
  failed,
  total: passed + failed,
  results
}, null, 2));

console.log(`Results written to: ${resultPath}`);

// Exit with appropriate code
process.exit(failed > 0 ? 1 : 0);
