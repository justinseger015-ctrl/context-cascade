/**
 * Test Script for Visibility Pipeline
 * Verifies database logging and WebSocket broadcasting
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');
const http = require('http');

const DB_PATH = path.join(__dirname, '..', 'agent-reality-map.db');
const VISIBILITY_LOG = path.join(__dirname, '..', '.visibility-pipeline.log');

/**
 * Test 1: Verify database connection and schema
 */
function testDatabaseConnection() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE, (err) => {
      if (err) {
        console.log('[TEST FAIL] Database connection failed:', err.message);
        reject(err);
        return;
      }
      console.log('[TEST PASS] Database connection successful');

      // Verify agent_audit_log table exists
      db.get("SELECT name FROM sqlite_master WHERE type='table' AND name='agent_audit_log'", (err, row) => {
        if (err || !row) {
          console.log('[TEST FAIL] agent_audit_log table not found');
          reject(new Error('Table not found'));
          return;
        }
        console.log('[TEST PASS] agent_audit_log table exists');
        db.close();
        resolve();
      });
    });
  });
}

/**
 * Test 2: Simulate visibility event logging
 */
function testEventLogging() {
  return new Promise((resolve, reject) => {
    const { execute } = require('./visibility-pipeline.js');

    const mockContext = {
      agentId: 'test-agent-visibility',
      toolName: 'Write',
      file_path: 'test/visibility-test.js',
      description: 'Test visibility pipeline',
      sessionId: 'test-session-123',
      agentRole: 'tester',
      result: {
        success: true,
        executionTime: 50
      }
    };

    execute(mockContext)
      .then(result => {
        if (result.success) {
          console.log('[TEST PASS] Visibility event logged successfully');
          console.log('  Agent ID:', result.agent_id);
          console.log('  Tool Name:', result.tool_name);
          console.log('  Execution Time:', result.execution_time, 'ms');
          resolve();
        } else {
          console.log('[TEST FAIL] Event logging failed');
          reject(new Error('Logging failed'));
        }
      })
      .catch(err => {
        console.log('[TEST FAIL] Event logging error:', err.message);
        reject(err);
      });
  });
}

/**
 * Test 3: Verify database entry
 */
function testDatabaseEntry() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READONLY);

    const query = `
      SELECT * FROM agent_audit_log
      WHERE agent_id = 'test-agent-visibility'
      ORDER BY timestamp DESC
      LIMIT 1
    `;

    db.get(query, (err, row) => {
      if (err) {
        console.log('[TEST FAIL] Database query failed:', err.message);
        db.close();
        reject(err);
        return;
      }

      if (!row) {
        console.log('[TEST FAIL] No database entry found for test agent');
        db.close();
        reject(new Error('Entry not found'));
        return;
      }

      console.log('[TEST PASS] Database entry verified');
      console.log('  Timestamp:', row.timestamp);
      console.log('  Agent ID:', row.agent_id);
      console.log('  Tool Name:', row.tool_name);
      console.log('  Operation:', row.operation);
      console.log('  Allowed:', row.allowed === 1 ? 'true' : 'false');

      db.close();
      resolve();
    });
  });
}

/**
 * Test 4: Verify log file
 */
function testLogFile() {
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(VISIBILITY_LOG)) {
      console.log('[TEST WARN] Visibility log file not found (may use database only)');
      resolve();
      return;
    }

    const logContent = fs.readFileSync(VISIBILITY_LOG, 'utf8');
    const lines = logContent.trim().split('\n');

    if (lines.length === 0) {
      console.log('[TEST WARN] Visibility log file is empty');
      resolve();
      return;
    }

    console.log('[TEST PASS] Visibility log file verified');
    console.log('  Total entries:', lines.length);
    console.log('  Latest entry:', lines[lines.length - 1].substring(0, 100) + '...');

    resolve();
  });
}

/**
 * Test 5: Verify backend API health
 */
function testBackendHealth() {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8000,
      path: '/health',
      method: 'GET',
      timeout: 3000
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          console.log('[TEST PASS] Backend API is healthy');
          console.log('  Response:', data);
          resolve();
        } else {
          console.log('[TEST FAIL] Backend API returned status', res.statusCode);
          reject(new Error(`HTTP ${res.statusCode}`));
        }
      });
    });

    req.on('error', err => {
      console.log('[TEST FAIL] Backend API connection failed:', err.message);
      reject(err);
    });

    req.on('timeout', () => {
      console.log('[TEST FAIL] Backend API timeout');
      req.destroy();
      reject(new Error('Timeout'));
    });

    req.end();
  });
}

/**
 * Run all tests
 */
async function runTests() {
  console.log('================================');
  console.log('VISIBILITY PIPELINE TESTS');
  console.log('================================\n');

  const tests = [
    { name: 'Database Connection', fn: testDatabaseConnection },
    { name: 'Event Logging', fn: testEventLogging },
    { name: 'Database Entry', fn: testDatabaseEntry },
    { name: 'Log File', fn: testLogFile },
    { name: 'Backend Health', fn: testBackendHealth }
  ];

  let passed = 0;
  let failed = 0;

  for (const test of tests) {
    console.log(`\nRunning: ${test.name}`);
    console.log('--------------------------------');
    try {
      await test.fn();
      passed++;
    } catch (err) {
      failed++;
      console.log('Error:', err.message);
    }
  }

  console.log('\n================================');
  console.log('TEST RESULTS');
  console.log('================================');
  console.log(`PASSED: ${passed}/${tests.length}`);
  console.log(`FAILED: ${failed}/${tests.length}`);
  console.log('================================\n');

  process.exit(failed > 0 ? 1 : 0);
}

// Run tests
runTests().catch(err => {
  console.error('Test suite failed:', err);
  process.exit(1);
});
