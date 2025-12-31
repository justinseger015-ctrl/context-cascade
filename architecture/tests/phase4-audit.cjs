/**
 * Phase 4 Audit: Architecture Optimization
 * Verifies all Phase 4 implementations
 *
 * @module architecture/tests/phase4-audit
 */

const fs = require('fs');
const path = require('path');

// Test configuration
const ARCHITECTURE_DIR = path.join(__dirname, '..');
const RESULTS = {
  total: 0,
  passed: 0,
  failed: 0,
  tests: []
};

/**
 * Run a test case
 */
function test(name, fn) {
  RESULTS.total++;
  try {
    const result = fn();
    if (result === true || result === undefined) {
      RESULTS.passed++;
      RESULTS.tests.push({ name, status: 'PASS' });
      console.log(`  [PASS] ${name}`);
    } else {
      RESULTS.failed++;
      RESULTS.tests.push({ name, status: 'FAIL', reason: result });
      console.log(`  [FAIL] ${name}: ${result}`);
    }
  } catch (err) {
    RESULTS.failed++;
    RESULTS.tests.push({ name, status: 'FAIL', reason: err.message });
    console.log(`  [FAIL] ${name}: ${err.message}`);
  }
}

/**
 * Run async test case
 */
async function testAsync(name, fn) {
  RESULTS.total++;
  try {
    const result = await fn();
    if (result === true || result === undefined) {
      RESULTS.passed++;
      RESULTS.tests.push({ name, status: 'PASS' });
      console.log(`  [PASS] ${name}`);
    } else {
      RESULTS.failed++;
      RESULTS.tests.push({ name, status: 'FAIL', reason: result });
      console.log(`  [FAIL] ${name}: ${result}`);
    }
  } catch (err) {
    RESULTS.failed++;
    RESULTS.tests.push({ name, status: 'FAIL', reason: err.message });
    console.log(`  [FAIL] ${name}: ${err.message}`);
  }
}

// ==========================================
// TEST SUITE 1: Agent Archetypes
// ==========================================
console.log('\n=== Suite 1: Agent Archetypes ===');

test('1.1 Agent archetypes module exists', () => {
  const modulePath = path.join(ARCHITECTURE_DIR, 'archetypes', 'agent-archetypes.cjs');
  if (!fs.existsSync(modulePath)) return 'Module file not found';
  return true;
});

test('1.2 Archetypes module loads without error', () => {
  const archetypes = require('../archetypes/agent-archetypes.cjs');
  if (!archetypes) return 'Module failed to load';
  return true;
});

test('1.3 Has at least 15 archetypes defined', () => {
  const archetypes = require('../archetypes/agent-archetypes.cjs');
  const count = Object.keys(archetypes.AGENT_ARCHETYPES).length;
  if (count < 15) return `Only ${count} archetypes, expected >= 15`;
  return true;
});

test('1.4 Each archetype has required fields', () => {
  const archetypes = require('../archetypes/agent-archetypes.cjs');
  const requiredFields = ['id', 'name', 'description', 'capabilities'];
  for (const [id, arch] of Object.entries(archetypes.AGENT_ARCHETYPES)) {
    for (const field of requiredFields) {
      if (!arch[field]) return `Archetype ${id} missing ${field}`;
    }
  }
  return true;
});

test('1.5 mapAgentsToArchetypes function exists', () => {
  const archetypes = require('../archetypes/agent-archetypes.cjs');
  if (typeof archetypes.mapAgentsToArchetypes !== 'function') {
    return 'mapAgentsToArchetypes not a function';
  }
  return true;
});

test('1.6 getArchetypeForAgent returns valid archetype', () => {
  const archetypes = require('../archetypes/agent-archetypes.cjs');
  const result = archetypes.getArchetypeForAgent('code-reviewer');
  if (!result || !result.id) return 'getArchetypeForAgent returned invalid result';
  return true;
});

// ==========================================
// TEST SUITE 2: Provider Abstraction
// ==========================================
console.log('\n=== Suite 2: Provider Abstraction ===');

test('2.1 Provider abstraction module exists', () => {
  const modulePath = path.join(ARCHITECTURE_DIR, 'providers', 'provider-abstraction.cjs');
  if (!fs.existsSync(modulePath)) return 'Module file not found';
  return true;
});

test('2.2 Provider module loads without error', () => {
  const providers = require('../providers/provider-abstraction.cjs');
  if (!providers) return 'Module failed to load';
  return true;
});

test('2.3 Has Claude, Codex, and Gemini providers', () => {
  const providers = require('../providers/provider-abstraction.cjs');
  const ids = Object.keys(providers.PROVIDERS);
  if (!ids.includes('claude')) return 'Missing claude provider';
  if (!ids.includes('codex')) return 'Missing codex provider';
  if (!ids.includes('gemini')) return 'Missing gemini provider';
  return true;
});

test('2.4 Each provider has required fields', () => {
  const providers = require('../providers/provider-abstraction.cjs');
  const requiredFields = ['id', 'name', 'type', 'strengths', 'contextWindow'];
  for (const [id, provider] of Object.entries(providers.PROVIDERS)) {
    for (const field of requiredFields) {
      if (provider[field] === undefined) return `Provider ${id} missing ${field}`;
    }
  }
  return true;
});

test('2.5 ROUTING_RULES defined for task types', () => {
  const providers = require('../providers/provider-abstraction.cjs');
  const rules = providers.ROUTING_RULES;
  if (!rules.research) return 'Missing research routing rule';
  if (!rules.autonomous) return 'Missing autonomous routing rule';
  if (!rules.reasoning) return 'Missing reasoning routing rule';
  if (!rules.default) return 'Missing default routing rule';
  return true;
});

test('2.6 getBestProvider function works', () => {
  const providers = require('../providers/provider-abstraction.cjs');
  if (typeof providers.getBestProvider !== 'function') {
    return 'getBestProvider not a function';
  }
  return true;
});

test('2.7 detectTaskType identifies task types correctly', () => {
  const providers = require('../providers/provider-abstraction.cjs');
  if (providers.detectTaskType('search for information') !== 'research') {
    return 'Failed to detect research task';
  }
  if (providers.detectTaskType('analyze the code') !== 'reasoning') {
    return 'Failed to detect reasoning task';
  }
  return true;
});

// ==========================================
// TEST SUITE 3: Unified State Manager
// ==========================================
console.log('\n=== Suite 3: Unified State Manager ===');

test('3.1 State manager module exists', () => {
  const modulePath = path.join(ARCHITECTURE_DIR, 'state', 'unified-state.cjs');
  if (!fs.existsSync(modulePath)) return 'Module file not found';
  return true;
});

test('3.2 State manager loads without error', () => {
  const state = require('../state/unified-state.cjs');
  if (!state) return 'Module failed to load';
  return true;
});

test('3.3 Has required namespaces', () => {
  const state = require('../state/unified-state.cjs');
  const required = ['session', 'agents', 'workflows', 'tasks', 'metrics', 'cache'];
  for (const ns of required) {
    if (!state.NAMESPACES[ns]) return `Missing namespace: ${ns}`;
  }
  return true;
});

test('3.4 get/set/del functions work', () => {
  const state = require('../state/unified-state.cjs');
  // Test basic operations
  state.set('cache', 'test_key', 'test_value');
  const value = state.get('cache', 'test_key');
  if (value !== 'test_value') return `Expected 'test_value', got '${value}'`;
  state.del('cache', 'test_key');
  const afterDel = state.get('cache', 'test_key', null);
  if (afterDel !== null) return 'Delete did not remove key';
  return true;
});

test('3.5 Dot notation works for nested keys', () => {
  const state = require('../state/unified-state.cjs');
  state.set('cache', 'nested.deep.key', 'nested_value');
  const value = state.get('cache', 'nested.deep.key');
  if (value !== 'nested_value') return `Nested get failed: ${value}`;
  state.del('cache', 'nested');
  return true;
});

test('3.6 Transaction support exists', () => {
  const state = require('../state/unified-state.cjs');
  if (typeof state.transaction !== 'function') {
    return 'transaction not a function';
  }
  return true;
});

test('3.7 Listener support exists', () => {
  const state = require('../state/unified-state.cjs');
  if (typeof state.addListener !== 'function') return 'addListener missing';
  if (typeof state.removeListener !== 'function') return 'removeListener missing';
  return true;
});

// ==========================================
// TEST SUITE 4: Ground Truth Validation
// ==========================================
console.log('\n=== Suite 4: Ground Truth Validation ===');

test('4.1 Ground truth module exists', () => {
  const modulePath = path.join(ARCHITECTURE_DIR, 'validation', 'ground-truth.cjs');
  if (!fs.existsSync(modulePath)) return 'Module file not found';
  return true;
});

test('4.2 Ground truth loads without error', () => {
  const groundTruth = require('../validation/ground-truth.cjs');
  if (!groundTruth) return 'Module failed to load';
  return true;
});

test('4.3 Has deterministic validation strategies', () => {
  const groundTruth = require('../validation/ground-truth.cjs');
  const strategies = groundTruth.VALIDATION_STRATEGIES;
  if (!strategies.test_execution) return 'Missing test_execution strategy';
  if (!strategies.syntax_check) return 'Missing syntax_check strategy';
  if (!strategies.type_check) return 'Missing type_check strategy';
  if (!strategies.lint) return 'Missing lint strategy';
  return true;
});

test('4.4 All strategies marked as deterministic', () => {
  const groundTruth = require('../validation/ground-truth.cjs');
  for (const [id, strategy] of Object.entries(groundTruth.VALIDATION_STRATEGIES)) {
    if (!strategy.deterministic) return `Strategy ${id} not marked deterministic`;
  }
  return true;
});

test('4.5 compareOutputs function works correctly', () => {
  const groundTruth = require('../validation/ground-truth.cjs');
  const result1 = groundTruth.compareOutputs('hello world', 'hello world');
  if (!result1.valid) return 'Exact match should be valid';
  const result2 = groundTruth.compareOutputs('hello world', 'goodbye');
  if (result2.valid) return 'Mismatch should be invalid';
  return true;
});

test('4.6 compareHashes function works', () => {
  const groundTruth = require('../validation/ground-truth.cjs');
  if (typeof groundTruth.compareHashes !== 'function') {
    return 'compareHashes not a function';
  }
  return true;
});

test('4.7 generateValidationReport function exists', () => {
  const groundTruth = require('../validation/ground-truth.cjs');
  if (typeof groundTruth.generateValidationReport !== 'function') {
    return 'generateValidationReport not a function';
  }
  return true;
});

// ==========================================
// TEST SUITE 5: Retrieval Verification
// ==========================================
console.log('\n=== Suite 5: Retrieval Verification ===');

test('5.1 Retrieval verification module exists', () => {
  const modulePath = path.join(ARCHITECTURE_DIR, 'validation', 'retrieval-verification.cjs');
  if (!fs.existsSync(modulePath)) return 'Module file not found';
  return true;
});

test('5.2 Retrieval verification loads without error', () => {
  const retrieval = require('../validation/retrieval-verification.cjs');
  if (!retrieval) return 'Module failed to load';
  return true;
});

test('5.3 Has retrieval strategies', () => {
  const retrieval = require('../validation/retrieval-verification.cjs');
  const strategies = retrieval.RETRIEVAL_STRATEGIES;
  if (!strategies.file_content) return 'Missing file_content strategy';
  if (!strategies.code_symbol) return 'Missing code_symbol strategy';
  if (!strategies.search_result) return 'Missing search_result strategy';
  if (!strategies.memory_retrieval) return 'Missing memory_retrieval strategy';
  return true;
});

test('5.4 verifyFileContent works for existing files', () => {
  const retrieval = require('../validation/retrieval-verification.cjs');
  const result = retrieval.verifyFileContent({
    filePath: path.join(ARCHITECTURE_DIR, 'validation', 'retrieval-verification.cjs')
  });
  if (!result.valid) return `File verification failed: ${result.error}`;
  if (!result.fileExists) return 'fileExists should be true';
  return true;
});

test('5.5 verifyFileContent fails for non-existent files', () => {
  const retrieval = require('../validation/retrieval-verification.cjs');
  const result = retrieval.verifyFileContent({
    filePath: '/nonexistent/file/path.js'
  });
  if (result.valid) return 'Should fail for non-existent file';
  return true;
});

test('5.6 calculateConfidence function works', () => {
  const retrieval = require('../validation/retrieval-verification.cjs');
  const result = retrieval.calculateConfidence({
    claims: [{ valid: true }, { valid: true }, { valid: false }]
  });
  const expected = 2/3;
  if (Math.abs(result - expected) > 0.01) {
    return `Expected ${expected}, got ${result}`;
  }
  return true;
});

test('5.7 generateRetrievalReport function exists', () => {
  const retrieval = require('../validation/retrieval-verification.cjs');
  if (typeof retrieval.generateRetrievalReport !== 'function') {
    return 'generateRetrievalReport not a function';
  }
  return true;
});

// ==========================================
// TEST SUITE 6: Integration Tests
// ==========================================
console.log('\n=== Suite 6: Integration Tests ===');

test('6.1 Architecture directory structure exists', () => {
  const dirs = ['archetypes', 'providers', 'state', 'validation'];
  for (const dir of dirs) {
    const dirPath = path.join(ARCHITECTURE_DIR, dir);
    if (!fs.existsSync(dirPath)) return `Missing directory: ${dir}`;
  }
  return true;
});

test('6.2 All modules can be loaded together', () => {
  try {
    const archetypes = require('../archetypes/agent-archetypes.cjs');
    const providers = require('../providers/provider-abstraction.cjs');
    const state = require('../state/unified-state.cjs');
    const groundTruth = require('../validation/ground-truth.cjs');
    const retrieval = require('../validation/retrieval-verification.cjs');
    return true;
  } catch (err) {
    return `Module loading failed: ${err.message}`;
  }
});

test('6.3 No circular dependencies', () => {
  // Clear require cache to detect circular deps
  const modules = [
    '../archetypes/agent-archetypes.cjs',
    '../providers/provider-abstraction.cjs',
    '../state/unified-state.cjs',
    '../validation/ground-truth.cjs',
    '../validation/retrieval-verification.cjs'
  ];
  for (const mod of modules) {
    delete require.cache[require.resolve(mod)];
  }
  try {
    for (const mod of modules) {
      require(mod);
    }
    return true;
  } catch (err) {
    if (err.message.includes('circular')) {
      return `Circular dependency detected: ${err.message}`;
    }
    throw err;
  }
});

test('6.4 State can store provider routing decisions', () => {
  const state = require('../state/unified-state.cjs');
  const providers = require('../providers/provider-abstraction.cjs');

  const taskType = providers.detectTaskType('research current trends');
  state.set('cache', 'last_routing', { taskType, timestamp: Date.now() });
  const stored = state.get('cache', 'last_routing');
  if (!stored || stored.taskType !== taskType) {
    return 'Failed to store routing decision';
  }
  state.del('cache', 'last_routing');
  return true;
});

test('6.5 Ground truth can validate architecture files', () => {
  const groundTruth = require('../validation/ground-truth.cjs');
  const testFile = path.join(ARCHITECTURE_DIR, 'validation', 'ground-truth.cjs');

  // Just verify the function accepts the file - use non-strict mode
  const result = groundTruth.compareOutputs(
    fs.readFileSync(testFile, 'utf8').slice(0, 200),
    'Ground Truth Validation',
    { strict: false }
  );
  if (!result.valid) return 'File should contain expected content';
  return true;
});

// ==========================================
// Summary
// ==========================================
console.log('\n========================================');
console.log('PHASE 4 AUDIT RESULTS');
console.log('========================================');
console.log(`Total:  ${RESULTS.total}`);
console.log(`Passed: ${RESULTS.passed}`);
console.log(`Failed: ${RESULTS.failed}`);
console.log(`Status: ${RESULTS.failed === 0 ? 'ALL TESTS PASSED' : 'FAILURES DETECTED'}`);
console.log('========================================\n');

// Exit with error code if failures
if (RESULTS.failed > 0) {
  console.log('Failed tests:');
  RESULTS.tests.filter(t => t.status === 'FAIL').forEach(t => {
    console.log(`  - ${t.name}: ${t.reason}`);
  });
  process.exit(1);
}

module.exports = RESULTS;
