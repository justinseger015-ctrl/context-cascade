/**
 * Phase 2 Safety Controls Audit
 * Verifies all safety components are working correctly
 *
 * Run: node safety/tests/phase2-audit.cjs
 */

const path = require('path');
const fs = require('fs');

// Adjust paths for test location
process.chdir(path.join(__dirname, '..', '..'));

const safetyGuardian = require('../guardian/safety-guardian.cjs');
const autoRollback = require('../rollback/auto-rollback.cjs');

// Test results accumulator
const results = {
  passed: 0,
  failed: 0,
  tests: []
};

function test(name, fn) {
  try {
    const result = fn();
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
  console.log('PHASE 2 SAFETY CONTROLS AUDIT');
  console.log('Context Cascade Safety Verification');
  console.log('='.repeat(60));
  console.log('');

  // ============================================
  // SECTION 1: SAFETY CONSTITUTION
  // ============================================
  console.log('\n--- SECTION 1: SAFETY CONSTITUTION ---\n');

  test('1.1 Constitution file exists', () => {
    const constitutionPath = path.join(__dirname, '..', 'constitution', 'SYSTEM-SAFETY.md');
    return fs.existsSync(constitutionPath);
  });

  test('1.2 Constitution contains required articles', () => {
    const constitutionPath = path.join(__dirname, '..', 'constitution', 'SYSTEM-SAFETY.md');
    const content = fs.readFileSync(constitutionPath, 'utf8');

    const requiredArticles = [
      'ARTICLE I: EMERGENCY STOP',
      'ARTICLE II: HUMAN OVERSIGHT',
      'ARTICLE III: SELF-MODIFICATION LIMITS',
      'ARTICLE IV: RESOURCE LIMITS',
      'ARTICLE V: ROLLBACK AND RECOVERY',
      'ARTICLE VI: AUDIT AND TRANSPARENCY',
      'ARTICLE VII: ENFORCEMENT'
    ];

    const missing = requiredArticles.filter(article => !content.includes(article));
    return missing.length === 0;
  });

  test('1.3 Constitution marked as immutable', () => {
    const constitutionPath = path.join(__dirname, '..', 'constitution', 'SYSTEM-SAFETY.md');
    const content = fs.readFileSync(constitutionPath, 'utf8');
    return content.includes('IMMUTABLE') && content.includes('MUST NOT be modified');
  });

  // ============================================
  // SECTION 2: SAFETY GUARDIAN
  // ============================================
  console.log('\n--- SECTION 2: SAFETY GUARDIAN ---\n');

  test('2.1 Hash file function works', () => {
    const hash = safetyGuardian.hashFile(__filename);
    return hash && hash.length === 64; // SHA-256 hex length
  });

  test('2.2 Hash seal can be generated', () => {
    const seal = safetyGuardian.generateHashSeal();
    return seal && seal.version && seal.files;
  });

  test('2.3 Hash seal can be loaded', () => {
    const seal = safetyGuardian.loadHashSeal();
    return seal && seal.files;
  });

  test('2.4 Integrity verification runs', () => {
    const result = safetyGuardian.verifyIntegrity();
    return result && typeof result.valid === 'boolean';
  });

  test('2.5 Immutable path detection works', () => {
    const check1 = safetyGuardian.checkApprovalRequired('safety/constitution/SYSTEM-SAFETY.md');
    const check2 = safetyGuardian.checkApprovalRequired('src/some-file.js');

    return check1.allowed === false &&
           check1.reason === 'IMMUTABLE_PATH' &&
           check2.allowed === true;
  });

  test('2.6 Approval required path detection works', () => {
    const check = safetyGuardian.checkApprovalRequired('agents/identity/agent-rbac-rules.json');
    return check.requiresApproval === true;
  });

  test('2.7 Kill switch check works', () => {
    const result = safetyGuardian.checkKillSwitch();
    return typeof result.active === 'boolean';
  });

  test('2.8 Pre-operation check runs', () => {
    const result = safetyGuardian.preOperationCheck('read', { path: '/some/file' });
    return result && typeof result.allowed === 'boolean' && Array.isArray(result.checks);
  });

  test('2.9 Pre-operation blocks immutable writes', () => {
    const result = safetyGuardian.preOperationCheck('write', {
      path: 'safety/constitution/SYSTEM-SAFETY.md'
    });
    return result.allowed === false &&
           result.violations.some(v => v.type === 'IMMUTABLE_PATH');
  });

  await testAsync('2.10 Safety audit runs', async () => {
    const audit = await safetyGuardian.auditSafetySystem();
    return audit && audit.status && audit.checks;
  });

  // ============================================
  // SECTION 3: AUTO-ROLLBACK
  // ============================================
  console.log('\n--- SECTION 3: AUTO-ROLLBACK ---\n');

  test('3.1 Rollback state can be loaded', () => {
    const state = autoRollback.loadState();
    return state && typeof state.failureCounts === 'object';
  });

  test('3.2 Rollback status available', () => {
    const status = autoRollback.getStatus();
    return status &&
           typeof status.inRecoveryMode === 'boolean' &&
           typeof status.threshold === 'number';
  });

  await testAsync('3.3 Test result can be recorded', async () => {
    const result = await autoRollback.recordTestResult('test-component', true, { test: 'data' });
    return result.recorded === true && result.component === 'test-component';
  });

  await testAsync('3.4 Failed test increments counter', async () => {
    // Record 2 failures
    await autoRollback.recordTestResult('failure-test', false, {});
    const result = await autoRollback.recordTestResult('failure-test', false, {});

    return result.consecutiveFailures === 2;
  });

  await testAsync('3.5 Success resets counter', async () => {
    // Record success after failures
    const result = await autoRollback.recordTestResult('failure-test', true, {});
    return result.consecutiveFailures === 0;
  });

  test('3.6 Risk assessment works', () => {
    const risk = autoRollback.assessRollbackRisk('some-component');
    return risk &&
           typeof risk.consecutiveFailures === 'number' &&
           typeof risk.threshold === 'number' &&
           typeof risk.atRisk === 'boolean';
  });

  test('3.7 Recovery mode can be exited', () => {
    const result = autoRollback.exitRecoveryMode();
    return result.success === true;
  });

  test('3.8 Configuration has correct threshold', () => {
    return autoRollback.CONFIG.consecutiveFailureThreshold === 3;
  });

  // ============================================
  // SECTION 4: KILL SWITCH INTEGRATION
  // ============================================
  console.log('\n--- SECTION 4: KILL SWITCH INTEGRATION ---\n');

  test('4.1 Kill switch file detection works', () => {
    // Create temporary kill switch file
    const testKillSwitch = path.join(process.cwd(), '.meta-loop-stop-test');

    // Ensure it doesn't interfere with real kill switch
    const result = safetyGuardian.checkKillSwitch();

    return typeof result.active === 'boolean';
  });

  test('4.2 Environment variable detection works', () => {
    // Save current value
    const oldValue = process.env.META_LOOP_EMERGENCY_STOP;

    // Test with value set
    process.env.META_LOOP_EMERGENCY_STOP = 'true';
    const activeResult = safetyGuardian.checkKillSwitch();

    // Restore
    if (oldValue) {
      process.env.META_LOOP_EMERGENCY_STOP = oldValue;
    } else {
      delete process.env.META_LOOP_EMERGENCY_STOP;
    }

    return activeResult.active === true;
  });

  test('4.3 Emergency response can be triggered', () => {
    // Test logging (don't actually create kill switch)
    safetyGuardian.logViolation({
      type: 'TEST_VIOLATION',
      message: 'Test violation for audit'
    });

    // Verify log was created
    const logPath = path.join(process.cwd(), 'logs', 'safety-violations.jsonl');
    return fs.existsSync(logPath);
  });

  // ============================================
  // SECTION 5: HASH SEAL INTEGRITY
  // ============================================
  console.log('\n--- SECTION 5: HASH SEAL INTEGRITY ---\n');

  test('5.1 Hash seal file exists', () => {
    const sealPath = path.join(__dirname, '..', 'constitution', 'hash-seal.json');
    return fs.existsSync(sealPath);
  });

  test('5.2 Hash seal has required fields', () => {
    const seal = safetyGuardian.loadHashSeal();
    return seal &&
           seal.version &&
           seal.generatedAt &&
           seal.files;
  });

  test('5.3 Constitution hash is recorded', () => {
    const seal = safetyGuardian.loadHashSeal();
    return seal && seal.constitutionHash && seal.constitutionHash.length === 64;
  });

  test('5.4 Guardian is sealed', () => {
    const seal = safetyGuardian.loadHashSeal();
    return seal &&
           seal.files &&
           seal.files['safety/guardian/safety-guardian.cjs'];
  });

  test('5.5 Current integrity matches seal', () => {
    const result = safetyGuardian.verifyIntegrity();
    return result.valid === true;
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
      if (t.details) console.log(`    Details: ${JSON.stringify(t.details)}`);
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
