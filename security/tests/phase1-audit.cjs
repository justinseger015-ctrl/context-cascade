/**
 * Phase 1 Security Audit
 * Verifies all security components are working correctly
 *
 * Run: node security/tests/phase1-audit.js
 */

const path = require('path');

// Adjust paths for test location
process.chdir(path.join(__dirname, '..', '..'));

const security = require('../index.cjs');
const rbacEnforcer = require('../rbac/enforcer.cjs');
const tokenManager = require('../tokens/token-manager.cjs');
const checksumValidator = require('../mcp-integrity/checksum-validator.cjs');
const sandboxRouter = require('../sandbox/sandbox-router.cjs');

// Test results accumulator
const results = {
  passed: 0,
  failed: 0,
  tests: []
};

function test(name, fn) {
  try {
    const result = fn();
    if (result === true || (result && result.success !== false)) {
      results.passed++;
      results.tests.push({ name, status: 'PASS', details: result });
      console.log(`[PASS] ${name}`);
    } else {
      results.failed++;
      results.tests.push({ name, status: 'FAIL', details: result });
      console.log(`[FAIL] ${name}:`, result);
    }
  } catch (err) {
    results.failed++;
    results.tests.push({ name, status: 'ERROR', error: err.message });
    console.log(`[ERROR] ${name}:`, err.message);
  }
}

async function testAsync(name, fn) {
  try {
    const result = await fn();
    if (result === true || (result && result.success !== false && result.valid !== false)) {
      results.passed++;
      results.tests.push({ name, status: 'PASS', details: result });
      console.log(`[PASS] ${name}`);
    } else {
      results.failed++;
      results.tests.push({ name, status: 'FAIL', details: result });
      console.log(`[FAIL] ${name}:`, JSON.stringify(result, null, 2));
    }
  } catch (err) {
    results.failed++;
    results.tests.push({ name, status: 'ERROR', error: err.message });
    console.log(`[ERROR] ${name}:`, err.message);
  }
}

async function runAudit() {
  console.log('='.repeat(60));
  console.log('PHASE 1 SECURITY AUDIT');
  console.log('Context Cascade Security Hardening Verification');
  console.log('='.repeat(60));
  console.log('');

  // ============================================
  // SECTION 1: RBAC ENFORCEMENT
  // ============================================
  console.log('\n--- SECTION 1: RBAC ENFORCEMENT ---\n');

  test('1.1 RBAC rules load successfully', () => {
    const rules = rbacEnforcer.loadRBACRules();
    return rules && rules.roles && Object.keys(rules.roles).length > 0;
  });

  test('1.2 Agent registration works', () => {
    const testToken = 'test-token-12345';
    try {
      rbacEnforcer.registerAgent('test-agent-001', 'developer', testToken);
      return true;
    } catch (err) {
      // developer role might not exist, try a different approach
      return { success: false, error: err.message };
    }
  });

  test('1.3 Token validation works', () => {
    const testToken = 'test-token-12345';
    // First register
    try {
      rbacEnforcer.registerAgent('test-agent-002', 'developer', testToken);
    } catch (e) {
      // Role might not exist in rules
    }
    // Then validate
    const valid = rbacEnforcer.validateToken('test-agent-002', testToken);
    const invalid = rbacEnforcer.validateToken('test-agent-002', 'wrong-token');
    return valid === true && invalid === false;
  });

  test('1.4 Path matching works correctly', () => {
    const match1 = rbacEnforcer.matchPath('/src/index.js', ['/src/**']);
    const match2 = rbacEnforcer.matchPath('/etc/passwd', ['/src/**']);
    const match3 = rbacEnforcer.matchPath('/any/path', ['**']);
    return match1 === true && match2 === false && match3 === true;
  });

  test('1.5 RBAC denies unauthorized agents', () => {
    const result = rbacEnforcer.enforceRBAC('unknown-agent', 'bad-token', 'Read', {});
    return result.allowed === false && result.reason.includes('RBAC_DENIED');
  });

  // ============================================
  // SECTION 2: TOKEN MANAGEMENT
  // ============================================
  console.log('\n--- SECTION 2: TOKEN MANAGEMENT ---\n');

  test('2.1 Token generation works', () => {
    const result = tokenManager.generateToken('agent-test-001', 'reader');
    return result.token && result.agentId === 'agent-test-001' && result.role === 'reader';
  });

  test('2.2 Token validation works', () => {
    const generated = tokenManager.generateToken('agent-test-002', 'developer');
    const validation = tokenManager.validateToken(generated.token);
    return validation.valid === true && validation.payload.agentId === 'agent-test-002';
  });

  test('2.3 Invalid token is rejected', () => {
    const validation = tokenManager.validateToken('invalid-token-garbage');
    return validation.valid === false;
  });

  test('2.4 Token expiry is enforced', () => {
    // Generate token that expired 1 hour ago
    const generated = tokenManager.generateToken('agent-test-003', 'reader', {
      expiryMs: -3600000 // Negative = already expired
    });
    const validation = tokenManager.validateToken(generated.token);
    return validation.valid === false && validation.reason.includes('expired');
  });

  test('2.5 Token revocation works', () => {
    const generated = tokenManager.generateToken('agent-test-004', 'reader');
    const revoked = tokenManager.revokeToken(generated.token);
    const isRevoked = tokenManager.isRevoked(generated.token);
    return revoked === true && isRevoked === true;
  });

  test('2.6 Token storage and retrieval works', () => {
    const generated = tokenManager.generateToken('agent-test-005', 'developer');
    tokenManager.storeToken('agent-test-005', generated.token);
    const retrieved = tokenManager.getStoredToken('agent-test-005');
    tokenManager.clearStoredToken('agent-test-005');
    const cleared = tokenManager.getStoredToken('agent-test-005');
    return retrieved === generated.token && cleared === null;
  });

  test('2.7 API key generation works', () => {
    const apiKey = tokenManager.generateApiKey('test-agent');
    return apiKey.startsWith('cc_test-agent_') && apiKey.length > 20;
  });

  // ============================================
  // SECTION 3: MCP INTEGRITY VALIDATION
  // ============================================
  console.log('\n--- SECTION 3: MCP INTEGRITY VALIDATION ---\n');

  test('3.1 Checksum registry loads', () => {
    const registry = checksumValidator.loadRegistry();
    return registry && registry.version && registry.servers;
  });

  test('3.2 Server listing works', () => {
    const servers = checksumValidator.listServers();
    return Array.isArray(servers);
  });

  test('3.3 Unknown server validation fails correctly', () => {
    const result = checksumValidator.validateServer('non-existent-server', '/fake/path');
    return result.valid === false && result.reason.includes('MCP_UNKNOWN');
  });

  test('3.4 Checksum calculation works', () => {
    // Calculate checksum of this test file itself
    const checksums = checksumValidator.calculateChecksums(__filename);
    return checksums.sha256 && checksums.sha256.length === 64 &&
           checksums.sha384 && checksums.sha384.length === 96;
  });

  test('3.5 Trust status checking works', () => {
    const trusted = checksumValidator.isTrusted('memory-mcp');
    const untrusted = checksumValidator.isTrusted('random-unknown-server');
    return trusted === true && untrusted === false;
  });

  // ============================================
  // SECTION 4: SANDBOX ROUTING
  // ============================================
  console.log('\n--- SECTION 4: SANDBOX ROUTING ---\n');

  test('4.1 Sandbox modes are defined', () => {
    const modes = sandboxRouter.SANDBOX_MODES;
    return modes.READ_ONLY && modes.WORKSPACE_WRITE && modes.FULL_AUTO && modes.YOLO;
  });

  test('4.2 Sandbox config is valid', () => {
    const config = sandboxRouter.SANDBOX_CONFIG;
    return config.defaultMode && config.maxExecutionTime > 0;
  });

  test('4.3 Sandbox mode determination works', () => {
    const readOnly = sandboxRouter.determineSandboxMode({ writesFiles: false });
    const writeMode = sandboxRouter.determineSandboxMode({ writesFiles: true });
    const autoMode = sandboxRouter.determineSandboxMode({ autonomous: true });
    const networkMode = sandboxRouter.determineSandboxMode({ requiresNetwork: true });

    return readOnly === 'read-only' &&
           writeMode === 'workspace-write' &&
           autoMode === 'full-auto' &&
           networkMode === 'yolo';
  });

  test('4.4 Sandbox context creation works', () => {
    const ctx = sandboxRouter.createSandboxContext({ mode: 'read-only' });
    return ctx.exec && ctx.runTests && ctx.lint && ctx.typeCheck && ctx.mode === 'read-only';
  });

  await testAsync('4.5 Codex availability check runs', async () => {
    const result = await sandboxRouter.checkCodexAvailable();
    // Either available or not, but should return valid structure
    return typeof result.available === 'boolean';
  });

  // ============================================
  // SECTION 5: INTEGRATED SECURITY
  // ============================================
  console.log('\n--- SECTION 5: INTEGRATED SECURITY ---\n');

  await testAsync('5.1 Security module initializes', async () => {
    const result = await security.initialize({ validateSandbox: false });
    return result.ready === true;
  });

  test('5.2 Secure agent registration works', () => {
    try {
      const result = security.registerSecureAgent('integrated-test-agent', 'developer');
      return result.registered === true && result.token;
    } catch (err) {
      // Role might not exist
      return { success: false, error: err.message };
    }
  });

  await testAsync('5.3 Security audit runs', async () => {
    const audit = await security.auditSecurity();
    return audit.timestamp && audit.checks;
  });

  // ============================================
  // SUMMARY
  // ============================================
  console.log('\n' + '='.repeat(60));
  console.log('AUDIT SUMMARY');
  console.log('='.repeat(60));
  console.log(`Total Tests: ${results.passed + results.failed}`);
  console.log(`Passed: ${results.passed}`);
  console.log(`Failed: ${results.failed}`);
  console.log(`Success Rate: ${((results.passed / (results.passed + results.failed)) * 100).toFixed(1)}%`);

  if (results.failed > 0) {
    console.log('\nFailed Tests:');
    results.tests.filter(t => t.status !== 'PASS').forEach(t => {
      console.log(`  - ${t.name}: ${t.status}`);
      if (t.error) console.log(`    Error: ${t.error}`);
    });
  }

  console.log('\n' + '='.repeat(60));

  // Exit with appropriate code
  process.exit(results.failed > 0 ? 1 : 0);
}

// Run the audit
runAudit().catch(err => {
  console.error('Audit failed to run:', err);
  process.exit(1);
});
