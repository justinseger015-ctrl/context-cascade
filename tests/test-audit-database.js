/**
 * Audit Database Test Suite
 * Tests all audit query functions and performance
 * Target: <10ms write, <50ms query
 * Windows compatible: No Unicode
 */

const path = require('path');
const fs = require('fs');

// Use sqlite3 from hooks/12fa/utils/node_modules
const sqlite3Module = path.join(__dirname, '..', 'hooks', '12fa', 'utils', 'node_modules', 'sqlite3');
const sqlite3 = require(sqlite3Module).verbose();

const auditQueries = require('../hooks/12fa/utils/audit-queries');

const DB_PATH = path.join(__dirname, '..', 'hooks', '12fa', 'agent-reality-map.db');
const PERFORMANCE_THRESHOLD_WRITE = 10; // ms
const PERFORMANCE_THRESHOLD_QUERY = 50; // ms

// Test results tracker
const results = {
  passed: 0,
  failed: 0,
  tests: []
};

/**
 * Assert helper
 */
function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

/**
 * Test runner
 */
async function runTest(name, testFn) {
  process.stdout.write(`[TEST] ${name}... `);

  const startTime = Date.now();
  try {
    await testFn();
    const duration = Date.now() - startTime;
    console.log(`PASS (${duration}ms)`);
    results.passed++;
    results.tests.push({ name, status: 'PASS', duration });
  } catch (error) {
    const duration = Date.now() - startTime;
    console.log(`FAIL (${duration}ms)`);
    console.error(`  Error: ${error.message}`);
    results.failed++;
    results.tests.push({ name, status: 'FAIL', duration, error: error.message });
  }
}

/**
 * Insert test data
 */
async function insertTestData() {
  const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE);

  const testRecords = [
    {
      agent_id: 'test-agent-1',
      agent_role: 'coder',
      operation: 'file-write',
      tool_name: 'Write',
      file_path: '/test/file1.js',
      allowed: 1,
      budget_impact: 1.5,
      session_id: 'session-1'
    },
    {
      agent_id: 'test-agent-1',
      agent_role: 'coder',
      operation: 'file-read',
      tool_name: 'Read',
      file_path: '/test/file1.js',
      allowed: 1,
      budget_impact: 0.5,
      session_id: 'session-1'
    },
    {
      agent_id: 'test-agent-2',
      agent_role: 'reviewer',
      operation: 'api-call',
      tool_name: 'ApiCall',
      api_name: 'github',
      allowed: 0,
      denied_reason: 'Insufficient permissions',
      budget_impact: 0.0,
      session_id: 'session-2'
    },
    {
      agent_id: 'test-agent-3',
      agent_role: 'tester',
      operation: 'bash-execute',
      tool_name: 'Bash',
      allowed: 1,
      budget_impact: 2.0,
      session_id: 'session-3'
    }
  ];

  return new Promise((resolve, reject) => {
    const query = `
      INSERT INTO agent_audit_log (
        timestamp,
        agent_id,
        agent_role,
        operation,
        tool_name,
        file_path,
        api_name,
        allowed,
        denied_reason,
        budget_impact,
        session_id,
        metadata
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    let inserted = 0;

    testRecords.forEach(record => {
      const params = [
        new Date().toISOString(),
        record.agent_id,
        record.agent_role,
        record.operation,
        record.tool_name || null,
        record.file_path || null,
        record.api_name || null,
        record.allowed,
        record.denied_reason || null,
        record.budget_impact,
        record.session_id,
        JSON.stringify({ test: true })
      ];

      db.run(query, params, function(err) {
        if (err) {
          db.close();
          return reject(err);
        }

        inserted++;
        if (inserted === testRecords.length) {
          db.close();
          resolve(inserted);
        }
      });
    });
  });
}

/**
 * Test 1: Database exists
 */
async function testDatabaseExists() {
  assert(fs.existsSync(DB_PATH), 'Database file should exist');
}

/**
 * Test 2: Get audit log for agent
 */
async function testGetAuditLog() {
  const logs = await auditQueries.getAuditLog('test-agent-1', 10);
  assert(Array.isArray(logs), 'Should return array');
  assert(logs.length >= 2, 'Should have at least 2 records for test-agent-1');
  assert(logs[0].agent_id === 'test-agent-1', 'Should filter by agent_id');
  assert(typeof logs[0].allowed === 'boolean', 'allowed should be boolean');
}

/**
 * Test 3: Search audit log with filters
 */
async function testSearchAuditLog() {
  const logs = await auditQueries.searchAuditLog({
    operation: 'file-write',
    allowed: true,
    limit: 10
  });

  assert(Array.isArray(logs), 'Should return array');
  assert(logs.every(log => log.operation === 'file-write'), 'Should filter by operation');
  assert(logs.every(log => log.allowed === true), 'Should filter by allowed status');
}

/**
 * Test 4: Get audit stats
 */
async function testGetAuditStats() {
  const stats = await auditQueries.getAuditStats('test-agent-1');

  assert(stats.agentId === 'test-agent-1', 'Should return stats for correct agent');
  assert(stats.totalOperations >= 2, 'Should count total operations');
  assert(stats.allowedOperations >= 2, 'Should count allowed operations');
  assert(typeof stats.totalBudgetUsed === 'number', 'Should calculate total budget');
}

/**
 * Test 5: Get recent denials
 */
async function testGetRecentDenials() {
  const denials = await auditQueries.getRecentDenials(10);

  assert(Array.isArray(denials), 'Should return array');
  assert(denials.every(log => log.denied_reason), 'All should have denied_reason');
  assert(denials.some(log => log.agent_id === 'test-agent-2'), 'Should include test denial');
}

/**
 * Test 6: Get budget summary
 */
async function testGetBudgetSummary() {
  const summary = await auditQueries.getBudgetSummary();

  assert(Array.isArray(summary), 'Should return array');
  assert(summary.length >= 2, 'Should have at least 2 agents with budget');
  assert(summary.every(item => typeof item.totalBudgetUsed === 'number'), 'Should have budget totals');
}

/**
 * Test 7: Get operation frequency
 */
async function testGetOperationFrequency() {
  const freq = await auditQueries.getOperationFrequency('test-agent-1', 7);

  assert(Array.isArray(freq), 'Should return array');
  assert(freq.every(item => typeof item.frequency === 'number'), 'Should have frequency count');
}

/**
 * Test 8: Performance - Write speed
 */
async function testWritePerformance() {
  const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE);

  return new Promise((resolve, reject) => {
    const query = `
      INSERT INTO agent_audit_log (
        timestamp, agent_id, agent_role, operation, allowed, budget_impact, metadata
      ) VALUES (?, ?, ?, ?, ?, ?, ?)
    `;

    const startTime = Date.now();

    db.run(query, [
      new Date().toISOString(),
      'perf-test-agent',
      'perf-test',
      'performance-test',
      1,
      0.0,
      '{}'
    ], function(err) {
      db.close();

      const duration = Date.now() - startTime;

      if (err) {
        return reject(err);
      }

      assert(duration < PERFORMANCE_THRESHOLD_WRITE,
        `Write should complete in <${PERFORMANCE_THRESHOLD_WRITE}ms, took ${duration}ms`);

      resolve();
    });
  });
}

/**
 * Test 9: Performance - Query speed
 */
async function testQueryPerformance() {
  const startTime = Date.now();

  await auditQueries.getAuditLog('test-agent-1', 100);

  const duration = Date.now() - startTime;

  assert(duration < PERFORMANCE_THRESHOLD_QUERY,
    `Query should complete in <${PERFORMANCE_THRESHOLD_QUERY}ms, took ${duration}ms`);
}

/**
 * Test 10: 90-day retention cleanup
 */
async function testCleanupOldLogs() {
  // Insert old record (100 days ago)
  const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE);

  await new Promise((resolve, reject) => {
    const oldTimestamp = new Date();
    oldTimestamp.setDate(oldTimestamp.getDate() - 100);

    const query = `
      INSERT INTO agent_audit_log (
        timestamp, agent_id, agent_role, operation, allowed, budget_impact, metadata
      ) VALUES (?, ?, ?, ?, ?, ?, ?)
    `;

    db.run(query, [
      oldTimestamp.toISOString(),
      'old-agent',
      'old-role',
      'old-operation',
      1,
      0.0,
      '{}'
    ], function(err) {
      db.close();
      if (err) reject(err);
      else resolve(this.lastID);
    });
  });

  // Run cleanup
  const deleted = await auditQueries.cleanupOldLogs();

  assert(deleted >= 1, 'Should delete at least 1 old record');

  // Verify old record is gone
  const logs = await auditQueries.getAuditLog('old-agent', 10);
  assert(logs.length === 0, 'Old records should be deleted');
}

/**
 * Display test summary
 */
function displaySummary() {
  console.log('\n========================================');
  console.log('AUDIT DATABASE TEST SUMMARY');
  console.log('========================================');
  console.log(`Total Tests: ${results.passed + results.failed}`);
  console.log(`Passed: ${results.passed}`);
  console.log(`Failed: ${results.failed}`);
  console.log('\nTest Details:');

  results.tests.forEach(test => {
    const status = test.status === 'PASS' ? '✓' : '✗';
    console.log(`  ${status} ${test.name} (${test.duration}ms)`);
    if (test.error) {
      console.log(`    Error: ${test.error}`);
    }
  });

  console.log('\nPerformance Thresholds:');
  console.log(`  Write: <${PERFORMANCE_THRESHOLD_WRITE}ms`);
  console.log(`  Query: <${PERFORMANCE_THRESHOLD_QUERY}ms`);
  console.log('========================================\n');
}

/**
 * Main test runner
 */
async function main() {
  console.log('\n[TEST] Starting audit database test suite...\n');

  try {
    // Setup: Insert test data
    console.log('[SETUP] Inserting test data...');
    const inserted = await insertTestData();
    console.log(`[SETUP] Inserted ${inserted} test records\n`);

    // Run tests
    await runTest('Database exists', testDatabaseExists);
    await runTest('Get audit log for agent', testGetAuditLog);
    await runTest('Search audit log with filters', testSearchAuditLog);
    await runTest('Get audit stats', testGetAuditStats);
    await runTest('Get recent denials', testGetRecentDenials);
    await runTest('Get budget summary', testGetBudgetSummary);
    await runTest('Get operation frequency', testGetOperationFrequency);
    await runTest('Write performance (<10ms)', testWritePerformance);
    await runTest('Query performance (<50ms)', testQueryPerformance);
    await runTest('90-day retention cleanup', testCleanupOldLogs);

    // Display summary
    displaySummary();

    // Exit with appropriate code
    process.exit(results.failed > 0 ? 1 : 0);

  } catch (error) {
    console.error('\n[TEST] FATAL ERROR:', error.message);
    console.error('[TEST] Stack trace:', error.stack);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

module.exports = { main };
