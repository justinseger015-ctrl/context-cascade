/**
 * Phase 3 Terminology Cleanup Audit
 * Verifies terminology clarifications are in place
 *
 * Run: node terminology/tests/phase3-audit.cjs
 */

const path = require('path');
const fs = require('fs');

// Adjust paths for test location
process.chdir(path.join(__dirname, '..', '..'));

const registrySync = require('../registry-sync.cjs');

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
      console.log(`[FAIL] ${name}:`, typeof result === 'object' ? JSON.stringify(result) : result);
    }
  } catch (err) {
    results.failed++;
    results.tests.push({ name, status: 'ERROR', error: err.message });
    console.log(`[ERROR] ${name}:`, err.message);
  }
}

function runAudit() {
  console.log('='.repeat(60));
  console.log('PHASE 3 TERMINOLOGY CLEANUP AUDIT');
  console.log('Context Cascade Terminology Verification');
  console.log('='.repeat(60));
  console.log('');

  // ============================================
  // SECTION 1: TERMINOLOGY DOCUMENTATION
  // ============================================
  console.log('\n--- SECTION 1: TERMINOLOGY DOCUMENTATION ---\n');

  test('1.1 Terminology clarifications doc exists', () => {
    return fs.existsSync(path.join(process.cwd(), 'docs', 'TERMINOLOGY-CLARIFICATIONS.md'));
  });

  test('1.2 Terminology doc covers VeriX', () => {
    const content = fs.readFileSync(
      path.join(process.cwd(), 'docs', 'TERMINOLOGY-CLARIFICATIONS.md'),
      'utf8'
    );
    return content.includes('VeriX') && content.includes('epistemic notation');
  });

  test('1.3 Terminology doc covers Byzantine', () => {
    const content = fs.readFileSync(
      path.join(process.cwd(), 'docs', 'TERMINOLOGY-CLARIFICATIONS.md'),
      'utf8'
    );
    return content.includes('Byzantine') && content.includes('CONCEPTUAL');
  });

  test('1.4 Terminology doc covers Raft', () => {
    const content = fs.readFileSync(
      path.join(process.cwd(), 'docs', 'TERMINOLOGY-CLARIFICATIONS.md'),
      'utf8'
    );
    return content.includes('Raft') && content.includes('hierarchical');
  });

  test('1.5 Terminology doc covers frozen terminology', () => {
    const content = fs.readFileSync(
      path.join(process.cwd(), 'docs', 'TERMINOLOGY-CLARIFICATIONS.md'),
      'utf8'
    );
    return content.includes('Frozen') && content.includes('hash-verified');
  });

  // ============================================
  // SECTION 2: PROTOCOL DISCLAIMERS
  // ============================================
  console.log('\n--- SECTION 2: PROTOCOL DISCLAIMERS ---\n');

  test('2.1 Byzantine coordinator has disclaimer', () => {
    const filePath = path.join(
      process.cwd(),
      'agents', 'orchestration', 'consensus', 'byzantine-coordinator.md'
    );
    if (!fs.existsSync(filePath)) return { error: 'File not found' };

    const content = fs.readFileSync(filePath, 'utf8');
    return content.includes('x-terminology-disclaimer') ||
           content.includes('CONCEPTUAL');
  });

  test('2.2 Advanced coordination skill has disclaimer', () => {
    const filePath = path.join(
      process.cwd(),
      'skills', 'orchestration', 'advanced-coordination', 'SKILL.md'
    );
    if (!fs.existsSync(filePath)) return { error: 'File not found' };

    const content = fs.readFileSync(filePath, 'utf8');
    return content.includes('x-terminology-disclaimer') ||
           content.includes('CONCEPTUAL') ||
           content.includes('CLARIFICATION');
  });

  test('2.3 VeriX has disclaimer header', () => {
    const filePath = path.join(
      process.cwd(),
      'cognitive-architecture', 'core', 'verix.py'
    );
    if (!fs.existsSync(filePath)) return { error: 'File not found' };

    const content = fs.readFileSync(filePath, 'utf8');
    return content.includes('DISCLAIMER') ||
           content.includes('NOT formal verification') ||
           content.includes('structured epistemic notation');
  });

  test('2.4 VeriLingua has clarification header', () => {
    const filePath = path.join(
      process.cwd(),
      'cognitive-architecture', 'core', 'verilingua.py'
    );
    if (!fs.existsSync(filePath)) return { error: 'File not found' };

    const content = fs.readFileSync(filePath, 'utf8');
    return content.includes('CLARIFICATION') ||
           content.includes('prompting framework') ||
           content.includes('cognitive frames');
  });

  // ============================================
  // SECTION 3: REGISTRY SYNC
  // ============================================
  console.log('\n--- SECTION 3: REGISTRY SYNC ---\n');

  test('3.1 Registry sync tool exists', () => {
    return fs.existsSync(path.join(process.cwd(), 'terminology', 'registry-sync.cjs'));
  });

  test('3.2 Can count agents', () => {
    const result = registrySync.countAgents();
    return result.total > 0 && Array.isArray(result.files);
  });

  test('3.3 Can count skills', () => {
    const result = registrySync.countSkills();
    return result.total > 0 && Array.isArray(result.files);
  });

  test('3.4 Can count commands', () => {
    const result = registrySync.countCommands();
    return result.count >= 0;
  });

  test('3.5 Sync check runs without error', () => {
    const result = registrySync.syncCheck();
    return result.timestamp && result.actual;
  });

  test('3.6 Can detect documented counts', () => {
    const result = registrySync.getDocumentedCounts();
    return !result.error;
  });

  test('3.7 Can find duplicates', () => {
    const result = registrySync.findDuplicates();
    return result.agents !== undefined && result.skills !== undefined;
  });

  test('3.8 Can generate sync report', () => {
    const report = registrySync.generateSyncReport();
    return report.includes('Registry Sync Report') && report.includes('Agents');
  });

  // ============================================
  // SECTION 4: TERMINOLOGY CONSISTENCY
  // ============================================
  console.log('\n--- SECTION 4: TERMINOLOGY CONSISTENCY ---\n');

  test('4.1 No claims of SMT solver in VeriX', () => {
    const filePath = path.join(
      process.cwd(),
      'cognitive-architecture', 'core', 'verix.py'
    );
    if (!fs.existsSync(filePath)) return true; // Skip if file doesn't exist

    const content = fs.readFileSync(filePath, 'utf8');
    // Should NOT claim to be an SMT solver without disclaimer
    const claimsSMT = content.includes('SMT') && !content.includes('NOT');
    const claimsZ3 = content.includes('Z3 solver') && !content.includes('NOT');
    return !claimsSMT && !claimsZ3;
  });

  test('4.2 No claims of formal verification without disclaimer', () => {
    const filePath = path.join(
      process.cwd(),
      'cognitive-architecture', 'core', 'verix.py'
    );
    if (!fs.existsSync(filePath)) return true;

    const content = fs.readFileSync(filePath, 'utf8');
    // If it claims formal verification, must have disclaimer
    if (content.includes('formal verification')) {
      return content.includes('NOT formal verification') ||
             content.includes('DISCLAIMER');
    }
    return true;
  });

  test('4.3 Frozen terminology clarified in safety docs', () => {
    const safetyPath = path.join(
      process.cwd(),
      'safety', 'constitution', 'SYSTEM-SAFETY.md'
    );
    if (!fs.existsSync(safetyPath)) return { error: 'Safety constitution not found' };

    const content = fs.readFileSync(safetyPath, 'utf8');
    // Should clarify what immutable means
    return content.includes('IMMUTABLE') && content.includes('human');
  });

  // ============================================
  // SECTION 5: COUNTS VERIFICATION
  // ============================================
  console.log('\n--- SECTION 5: COUNTS VERIFICATION ---\n');

  test('5.1 Agent count reasonable (50-300)', () => {
    const result = registrySync.countAgents();
    return result.total >= 50 && result.total <= 300;
  });

  test('5.2 Skill count reasonable (50-300)', () => {
    const result = registrySync.countSkills();
    return result.total >= 50 && result.total <= 300;
  });

  test('5.3 Multiple agent categories exist', () => {
    const result = registrySync.countAgents();
    return Object.keys(result.categories).length >= 5;
  });

  test('5.4 Multiple skill categories exist', () => {
    const result = registrySync.countSkills();
    return Object.keys(result.categories).length >= 5;
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

  // Print registry summary
  const sync = registrySync.syncCheck();
  console.log('\n--- REGISTRY COUNTS ---');
  console.log(`Agents: ${sync.actual.agents}`);
  console.log(`Skills: ${sync.actual.skills}`);
  console.log(`Commands: ${sync.actual.commands}`);
  console.log(`Playbooks: ${sync.actual.playbooks}`);
  console.log(`Hooks: ${sync.actual.hooks}`);

  console.log('\n' + '='.repeat(60));

  // Exit with appropriate code
  process.exit(results.failed > 0 ? 1 : 0);
}

// Run the audit
runAudit();
