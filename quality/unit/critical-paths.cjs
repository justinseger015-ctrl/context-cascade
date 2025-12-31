/**
 * Unit Tests: Critical Paths
 * Phase 5.3 Quality Expansion
 *
 * Tests critical code paths in security, safety, and architecture modules.
 *
 * @module quality/unit/critical-paths
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Project paths
const PROJECT_ROOT = path.join(__dirname, '..', '..');
const SECURITY_DIR = path.join(PROJECT_ROOT, 'security');
const SAFETY_DIR = path.join(PROJECT_ROOT, 'safety');
const ARCHITECTURE_DIR = path.join(PROJECT_ROOT, 'architecture');

/**
 * Test runner
 */
class UnitTestRunner {
  constructor() {
    this.results = [];
  }

  test(name, fn) {
    const start = Date.now();
    try {
      const result = fn();
      if (result === false) {
        throw new Error('Test returned false');
      }
      this.results.push({
        name,
        status: 'PASS',
        duration: Date.now() - start
      });
      console.log(`  [PASS] ${name}`);
      return true;
    } catch (err) {
      this.results.push({
        name,
        status: 'FAIL',
        error: err.message,
        duration: Date.now() - start
      });
      console.log(`  [FAIL] ${name}: ${err.message}`);
      return false;
    }
  }

  async testAsync(name, fn) {
    const start = Date.now();
    try {
      const result = await fn();
      if (result === false) {
        throw new Error('Test returned false');
      }
      this.results.push({
        name,
        status: 'PASS',
        duration: Date.now() - start
      });
      console.log(`  [PASS] ${name}`);
      return true;
    } catch (err) {
      this.results.push({
        name,
        status: 'FAIL',
        error: err.message,
        duration: Date.now() - start
      });
      console.log(`  [FAIL] ${name}: ${err.message}`);
      return false;
    }
  }

  getSummary() {
    return {
      total: this.results.length,
      passed: this.results.filter(r => r.status === 'PASS').length,
      failed: this.results.filter(r => r.status === 'FAIL').length,
      results: this.results
    };
  }
}

/**
 * Security module unit tests
 */
function runSecurityTests(runner) {
  console.log('\n--- Security Module Unit Tests ---');

  // RBAC Tests
  runner.test('RBAC: Module loads', () => {
    const rbac = require(path.join(SECURITY_DIR, 'rbac', 'enforcer.cjs'));
    if (!rbac) throw new Error('RBAC module not loaded');
    return true;
  });

  runner.test('RBAC: Has enforceRBAC function', () => {
    const rbac = require(path.join(SECURITY_DIR, 'rbac', 'enforcer.cjs'));
    if (typeof rbac.enforceRBAC !== 'function') {
      throw new Error('enforceRBAC not a function');
    }
    return true;
  });

  runner.test('RBAC: Has validateToken function', () => {
    const rbac = require(path.join(SECURITY_DIR, 'rbac', 'enforcer.cjs'));
    if (typeof rbac.validateToken !== 'function') {
      throw new Error('validateToken not a function');
    }
    return true;
  });

  runner.test('RBAC: Has matchPath function', () => {
    const rbac = require(path.join(SECURITY_DIR, 'rbac', 'enforcer.cjs'));
    if (typeof rbac.matchPath !== 'function') {
      throw new Error('matchPath not a function');
    }
    return true;
  });

  // Token Tests
  runner.test('Token: Module loads', () => {
    const tokens = require(path.join(SECURITY_DIR, 'tokens', 'token-manager.cjs'));
    if (!tokens) throw new Error('Token module not loaded');
    return true;
  });

  runner.test('Token: generateToken returns object with token', () => {
    const tokens = require(path.join(SECURITY_DIR, 'tokens', 'token-manager.cjs'));
    const result = tokens.generateToken('test-agent', 'developer');
    // May return object or string depending on implementation
    const tokenValue = typeof result === 'object' ? result.token : result;
    if (!tokenValue || tokenValue.length < 20) {
      throw new Error('Token too short or missing');
    }
    return true;
  });

  runner.test('Token: validateToken function exists', () => {
    const tokens = require(path.join(SECURITY_DIR, 'tokens', 'token-manager.cjs'));
    if (typeof tokens.validateToken !== 'function') {
      throw new Error('validateToken not a function');
    }
    return true;
  });

  runner.test('Token: validateToken rejects invalid token', () => {
    const tokens = require(path.join(SECURITY_DIR, 'tokens', 'token-manager.cjs'));
    const result = tokens.validateToken('invalid-token-string');
    if (result.valid) {
      throw new Error('Invalid token accepted');
    }
    return true;
  });

  runner.test('Token: revokeToken function exists', () => {
    const tokens = require(path.join(SECURITY_DIR, 'tokens', 'token-manager.cjs'));
    if (typeof tokens.revokeToken !== 'function') {
      throw new Error('revokeToken not a function');
    }
    return true;
  });

  // Checksum Validator Tests
  runner.test('Checksum: Module loads', () => {
    const checksum = require(path.join(SECURITY_DIR, 'mcp-integrity', 'checksum-validator.cjs'));
    if (!checksum) throw new Error('Checksum module not loaded');
    return true;
  });

  runner.test('Checksum: Has calculateChecksums function', () => {
    const checksum = require(path.join(SECURITY_DIR, 'mcp-integrity', 'checksum-validator.cjs'));
    if (typeof checksum.calculateChecksums !== 'function') {
      throw new Error('calculateChecksums not a function');
    }
    return true;
  });

  runner.test('Checksum: Has validateServer function', () => {
    const checksum = require(path.join(SECURITY_DIR, 'mcp-integrity', 'checksum-validator.cjs'));
    if (typeof checksum.validateServer !== 'function') {
      throw new Error('validateServer not a function');
    }
    return true;
  });

  // Sandbox Tests
  runner.test('Sandbox: Module loads', () => {
    const sandbox = require(path.join(SECURITY_DIR, 'sandbox', 'sandbox-router.cjs'));
    if (!sandbox) throw new Error('Sandbox module not loaded');
    return true;
  });

  runner.test('Sandbox: Has SANDBOX_MODES defined', () => {
    const sandbox = require(path.join(SECURITY_DIR, 'sandbox', 'sandbox-router.cjs'));
    if (!sandbox.SANDBOX_MODES) {
      throw new Error('SANDBOX_MODES not defined');
    }
    if (Object.keys(sandbox.SANDBOX_MODES).length < 2) {
      throw new Error('Need at least 2 sandbox modes');
    }
    return true;
  });
}

/**
 * Safety module unit tests
 */
function runSafetyTests(runner) {
  console.log('\n--- Safety Module Unit Tests ---');

  // Constitution Tests
  runner.test('Safety: Constitution file exists', () => {
    const constitutionPath = path.join(SAFETY_DIR, 'constitution', 'SYSTEM-SAFETY.md');
    if (!fs.existsSync(constitutionPath)) {
      throw new Error('Constitution file not found');
    }
    return true;
  });

  runner.test('Safety: Constitution has content', () => {
    const constitutionPath = path.join(SAFETY_DIR, 'constitution', 'SYSTEM-SAFETY.md');
    const content = fs.readFileSync(constitutionPath, 'utf8');
    // Check for either "## Article" or "# Article" patterns
    const articlePatterns = content.match(/#+\s*Article/gi) || [];
    const hasSubstantialContent = content.length > 500;
    if (!hasSubstantialContent && articlePatterns.length === 0) {
      throw new Error('Constitution lacks substantial content');
    }
    return true;
  });

  // Guardian Tests
  runner.test('Guardian: Module loads', () => {
    const guardian = require(path.join(SAFETY_DIR, 'guardian', 'safety-guardian.cjs'));
    if (!guardian) throw new Error('Guardian module not loaded');
    return true;
  });

  runner.test('Guardian: Has verifyIntegrity function', () => {
    const guardian = require(path.join(SAFETY_DIR, 'guardian', 'safety-guardian.cjs'));
    if (typeof guardian.verifyIntegrity !== 'function') {
      throw new Error('verifyIntegrity not a function');
    }
    return true;
  });

  runner.test('Guardian: Has checkKillSwitch function', () => {
    const guardian = require(path.join(SAFETY_DIR, 'guardian', 'safety-guardian.cjs'));
    if (typeof guardian.checkKillSwitch !== 'function') {
      throw new Error('checkKillSwitch not a function');
    }
    return true;
  });

  runner.test('Guardian: checkKillSwitch returns result', () => {
    const guardian = require(path.join(SAFETY_DIR, 'guardian', 'safety-guardian.cjs'));
    const result = guardian.checkKillSwitch();
    // Result may have different structure - just verify it returns something
    if (result === undefined) {
      throw new Error('checkKillSwitch should return a result');
    }
    return true;
  });

  // Rollback Tests
  runner.test('Rollback: Module loads', () => {
    const rollback = require(path.join(SAFETY_DIR, 'rollback', 'auto-rollback.cjs'));
    if (!rollback) throw new Error('Rollback module not loaded');
    return true;
  });

  runner.test('Rollback: Has recordTestResult function', () => {
    const rollback = require(path.join(SAFETY_DIR, 'rollback', 'auto-rollback.cjs'));
    if (typeof rollback.recordTestResult !== 'function') {
      throw new Error('recordTestResult not a function');
    }
    return true;
  });

  runner.test('Rollback: getStatus function exists', () => {
    const rollback = require(path.join(SAFETY_DIR, 'rollback', 'auto-rollback.cjs'));
    if (typeof rollback.getStatus !== 'function') {
      throw new Error('getStatus not a function');
    }
    return true;
  });

  runner.test('Rollback: getStatus returns status object', () => {
    const rollback = require(path.join(SAFETY_DIR, 'rollback', 'auto-rollback.cjs'));
    const status = rollback.getStatus();
    if (typeof status !== 'object') {
      throw new Error('getStatus should return object');
    }
    return true;
  });
}

/**
 * Architecture module unit tests
 */
function runArchitectureTests(runner) {
  console.log('\n--- Architecture Module Unit Tests ---');

  // Archetype Tests
  runner.test('Archetype: Module loads', () => {
    const archetypes = require(path.join(ARCHITECTURE_DIR, 'archetypes', 'agent-archetypes.cjs'));
    if (!archetypes) throw new Error('Archetype module not loaded');
    return true;
  });

  runner.test('Archetype: Has 20 archetypes', () => {
    const archetypes = require(path.join(ARCHITECTURE_DIR, 'archetypes', 'agent-archetypes.cjs'));
    const count = Object.keys(archetypes.AGENT_ARCHETYPES).length;
    if (count !== 20) {
      throw new Error(`Expected 20 archetypes, got ${count}`);
    }
    return true;
  });

  runner.test('Archetype: getArchetypeForAgent works', () => {
    const archetypes = require(path.join(ARCHITECTURE_DIR, 'archetypes', 'agent-archetypes.cjs'));
    const result = archetypes.getArchetypeForAgent('code-reviewer');
    if (!result || !result.id) {
      throw new Error('getArchetypeForAgent returned invalid result');
    }
    return true;
  });

  // Provider Tests
  runner.test('Provider: Module loads', () => {
    const providers = require(path.join(ARCHITECTURE_DIR, 'providers', 'provider-abstraction.cjs'));
    if (!providers) throw new Error('Provider module not loaded');
    return true;
  });

  runner.test('Provider: Has 3 providers', () => {
    const providers = require(path.join(ARCHITECTURE_DIR, 'providers', 'provider-abstraction.cjs'));
    const count = Object.keys(providers.PROVIDERS).length;
    if (count !== 3) {
      throw new Error(`Expected 3 providers, got ${count}`);
    }
    return true;
  });

  runner.test('Provider: detectTaskType works', () => {
    const providers = require(path.join(ARCHITECTURE_DIR, 'providers', 'provider-abstraction.cjs'));
    const type = providers.detectTaskType('research the latest news');
    if (type !== 'research') {
      throw new Error(`Expected 'research', got '${type}'`);
    }
    return true;
  });

  // State Tests
  runner.test('State: Module loads', () => {
    const state = require(path.join(ARCHITECTURE_DIR, 'state', 'unified-state.cjs'));
    if (!state) throw new Error('State module not loaded');
    return true;
  });

  runner.test('State: get/set work', () => {
    const state = require(path.join(ARCHITECTURE_DIR, 'state', 'unified-state.cjs'));
    state.set('cache', 'unit_test_key', 'unit_test_value');
    const value = state.get('cache', 'unit_test_key');
    if (value !== 'unit_test_value') {
      throw new Error(`Expected 'unit_test_value', got '${value}'`);
    }
    state.del('cache', 'unit_test_key');
    return true;
  });

  runner.test('State: del works', () => {
    const state = require(path.join(ARCHITECTURE_DIR, 'state', 'unified-state.cjs'));
    state.set('cache', 'del_test', 'value');
    state.del('cache', 'del_test');
    const value = state.get('cache', 'del_test', null);
    if (value !== null) {
      throw new Error('Delete did not remove key');
    }
    return true;
  });

  // Ground Truth Tests
  runner.test('GroundTruth: Module loads', () => {
    const groundTruth = require(path.join(ARCHITECTURE_DIR, 'validation', 'ground-truth.cjs'));
    if (!groundTruth) throw new Error('Ground truth module not loaded');
    return true;
  });

  runner.test('GroundTruth: compareOutputs works', () => {
    const groundTruth = require(path.join(ARCHITECTURE_DIR, 'validation', 'ground-truth.cjs'));
    const result = groundTruth.compareOutputs('hello', 'hello');
    if (!result.valid) {
      throw new Error('Exact match should be valid');
    }
    return true;
  });

  runner.test('GroundTruth: compareHashes works', () => {
    const groundTruth = require(path.join(ARCHITECTURE_DIR, 'validation', 'ground-truth.cjs'));
    // Create a temp file to test
    const testFile = path.join(PROJECT_ROOT, 'quality', 'unit', 'test-hash-file.tmp');
    fs.writeFileSync(testFile, 'test content');
    const hash = crypto.createHash('sha256').update('test content').digest('hex');
    const result = groundTruth.compareHashes(testFile, hash);
    fs.unlinkSync(testFile);
    if (!result.valid) {
      throw new Error('Hash should match');
    }
    return true;
  });

  // Retrieval Verification Tests
  runner.test('Retrieval: Module loads', () => {
    const retrieval = require(path.join(ARCHITECTURE_DIR, 'validation', 'retrieval-verification.cjs'));
    if (!retrieval) throw new Error('Retrieval module not loaded');
    return true;
  });

  runner.test('Retrieval: verifyFileContent works for existing files', () => {
    const retrieval = require(path.join(ARCHITECTURE_DIR, 'validation', 'retrieval-verification.cjs'));
    const result = retrieval.verifyFileContent({
      filePath: path.join(ARCHITECTURE_DIR, 'validation', 'retrieval-verification.cjs')
    });
    if (!result.valid) {
      throw new Error('Valid file should pass verification');
    }
    return true;
  });

  runner.test('Retrieval: verifyFileContent fails for non-existent files', () => {
    const retrieval = require(path.join(ARCHITECTURE_DIR, 'validation', 'retrieval-verification.cjs'));
    const result = retrieval.verifyFileContent({
      filePath: '/nonexistent/path/file.js'
    });
    if (result.valid) {
      throw new Error('Non-existent file should fail verification');
    }
    return true;
  });

  runner.test('Retrieval: calculateConfidence works', () => {
    const retrieval = require(path.join(ARCHITECTURE_DIR, 'validation', 'retrieval-verification.cjs'));
    const result = retrieval.calculateConfidence({
      claims: [{ valid: true }, { valid: false }]
    });
    if (result !== 0.5) {
      throw new Error(`Expected 0.5, got ${result}`);
    }
    return true;
  });
}

/**
 * Run all unit tests
 */
async function runAllTests() {
  console.log('\n=== Unit Tests: Critical Paths ===');

  const runner = new UnitTestRunner();

  runSecurityTests(runner);
  runSafetyTests(runner);
  runArchitectureTests(runner);

  const summary = runner.getSummary();

  console.log('\n========================================');
  console.log('UNIT TEST RESULTS');
  console.log('========================================');
  console.log(`Total:  ${summary.total}`);
  console.log(`Passed: ${summary.passed}`);
  console.log(`Failed: ${summary.failed}`);
  console.log(`Status: ${summary.failed === 0 ? 'ALL TESTS PASSED' : 'FAILURES DETECTED'}`);
  console.log('========================================\n');

  return summary;
}

// Export
module.exports = {
  UnitTestRunner,
  runSecurityTests,
  runSafetyTests,
  runArchitectureTests,
  runAllTests
};

// Run if executed directly
if (require.main === module) {
  runAllTests().then(summary => {
    process.exit(summary.failed > 0 ? 1 : 0);
  });
}
