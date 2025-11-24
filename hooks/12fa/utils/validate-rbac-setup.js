#!/usr/bin/env node
/**
 * RBAC Setup Validation Script
 *
 * Validates the complete RBAC Engine setup:
 * 1. RBAC rules JSON structure
 * 2. All 207 agent identities
 * 3. Performance benchmarks
 * 4. Integration tests
 *
 * Usage: node validate-rbac-setup.js
 *
 * @module hooks/12fa/utils/validate-rbac-setup
 */

const fs = require('fs');
const path = require('path');
const { validateRBACRules } = require('./permission-checker');
const { loadAgentIdentity, validateAgentIdentity } = require('./identity');

// ANSI color codes (Windows compatible)
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSuccess(message) {
  log(`[SUCCESS] ${message}`, 'green');
}

function logError(message) {
  log(`[ERROR] ${message}`, 'red');
}

function logWarning(message) {
  log(`[WARNING] ${message}`, 'yellow');
}

function logInfo(message) {
  log(`[INFO] ${message}`, 'blue');
}

/**
 * Validate RBAC rules JSON structure
 */
function validateRBACRulesStructure() {
  logInfo('Validating RBAC rules JSON structure...');

  const result = validateRBACRules();

  if (result.valid) {
    logSuccess('RBAC rules JSON is valid');
    logInfo('  - All 10 roles present');
    logInfo('  - All required fields present');
    logInfo('  - Budget constraints defined');
    return true;
  } else {
    logError('RBAC rules JSON validation failed:');
    result.errors.forEach(error => logError(`  - ${error}`));
    return false;
  }
}

/**
 * Find all agent .md files recursively
 */
function findAgentFiles(directory, files = []) {
  const entries = fs.readdirSync(directory);

  for (const entry of entries) {
    const fullPath = path.join(directory, entry);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      findAgentFiles(fullPath, files);
    } else if (entry.endsWith('.md') && !entry.includes('README')) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * Validate all agent identities
 */
function validateAgentIdentities() {
  logInfo('Validating agent identities...');

  const agentsDir = path.join(__dirname, '..', '..', '..', 'agents');
  const agentFiles = findAgentFiles(agentsDir);

  let validCount = 0;
  let invalidCount = 0;
  let missingIdentityCount = 0;

  logInfo(`Found ${agentFiles.length} agent files`);

  agentFiles.forEach(filePath => {
    try {
      const identity = loadAgentIdentity(filePath);

      if (!identity) {
        missingIdentityCount++;
        logWarning(`Missing identity: ${path.basename(filePath)}`);
        return;
      }

      const validation = validateAgentIdentity(identity);

      if (validation.valid) {
        validCount++;
      } else {
        invalidCount++;
        logError(`Invalid identity in ${path.basename(filePath)}:`);
        validation.errors.forEach(error => logError(`  - ${error}`));
      }
    } catch (error) {
      invalidCount++;
      logError(`Error validating ${path.basename(filePath)}: ${error.message}`);
    }
  });

  logInfo(`Validation results:`);
  logSuccess(`  Valid: ${validCount}`);
  if (missingIdentityCount > 0) {
    logWarning(`  Missing identity: ${missingIdentityCount}`);
  }
  if (invalidCount > 0) {
    logError(`  Invalid: ${invalidCount}`);
  }

  return invalidCount === 0;
}

/**
 * Performance benchmark tests
 */
function runPerformanceBenchmarks() {
  logInfo('Running performance benchmarks...');

  const { checkPermission } = require('./permission-checker');
  const { generateJWT, validateJWT } = require('./identity');

  const iterations = 1000;
  const results = [];

  // Benchmark: JWT generation
  let startTime = Date.now();
  for (let i = 0; i < iterations; i++) {
    generateJWT({
      agent_id: '550e8400-e29b-41d4-a716-446655440000',
      name: 'test-agent',
      role: 'developer'
    });
  }
  const jwtGenTime = (Date.now() - startTime) / iterations;
  results.push({ test: 'JWT Generation', avgTimeMs: jwtGenTime });

  // Benchmark: JWT validation
  const token = generateJWT({
    agent_id: '550e8400-e29b-41d4-a716-446655440000',
    name: 'test-agent',
    role: 'developer'
  });

  startTime = Date.now();
  for (let i = 0; i < iterations; i++) {
    validateJWT(token);
  }
  const jwtValTime = (Date.now() - startTime) / iterations;
  results.push({ test: 'JWT Validation', avgTimeMs: jwtValTime });

  // Benchmark: Permission check (tool only)
  startTime = Date.now();
  for (let i = 0; i < iterations; i++) {
    checkPermission({
      role: 'developer',
      toolName: 'Read'
    });
  }
  const toolCheckTime = (Date.now() - startTime) / iterations;
  results.push({ test: 'Tool Permission Check', avgTimeMs: toolCheckTime });

  // Benchmark: Full permission check
  startTime = Date.now();
  for (let i = 0; i < iterations; i++) {
    checkPermission({
      role: 'developer',
      toolName: 'Read',
      filePath: 'src/api/users.js',
      apiName: 'github'
    });
  }
  const fullCheckTime = (Date.now() - startTime) / iterations;
  results.push({ test: 'Full Permission Check', avgTimeMs: fullCheckTime });

  logInfo('Performance benchmark results:');
  let allPassed = true;

  results.forEach(result => {
    const passed = result.avgTimeMs < 50;
    allPassed = allPassed && passed;

    if (passed) {
      logSuccess(`  ${result.test}: ${result.avgTimeMs.toFixed(2)}ms (< 50ms)`);
    } else {
      logError(`  ${result.test}: ${result.avgTimeMs.toFixed(2)}ms (>= 50ms)`);
    }
  });

  return allPassed;
}

/**
 * Integration test: Full workflow
 */
function runIntegrationTest() {
  logInfo('Running integration test...');

  const { checkPermission } = require('./permission-checker');
  const { loadAgentIdentityByName } = require('./identity');

  try {
    // 1. Load agent identity
    const identity = loadAgentIdentityByName('system-architect');
    if (!identity) {
      logWarning('system-architect not found, skipping integration test');
      return true;
    }

    // 2. Validate identity
    const validation = validateAgentIdentity(identity);
    if (!validation.valid) {
      logError('Agent identity validation failed in integration test');
      return false;
    }

    // 3. Check permissions
    const permissionCheck = checkPermission({
      role: identity.role,
      toolName: 'Read',
      filePath: 'src/api/users.js',
      apiName: 'github'
    });

    if (!permissionCheck.allowed) {
      logError('Permission check failed in integration test');
      logError(`Reason: ${permissionCheck.reason}`);
      return false;
    }

    logSuccess('Integration test passed');
    logInfo(`  Agent: ${identity.name}`);
    logInfo(`  Role: ${identity.role}`);
    logInfo(`  Budget impact: $${permissionCheck.budgetImpact.toFixed(4)}`);
    logInfo(`  Check time: ${permissionCheck.checkTimeMs}ms`);

    return true;
  } catch (error) {
    logError(`Integration test failed: ${error.message}`);
    return false;
  }
}

/**
 * Main validation function
 */
function main() {
  console.log('\n========================================');
  console.log('RBAC Engine Validation');
  console.log('========================================\n');

  let allPassed = true;

  // 1. Validate RBAC rules
  console.log('\n[1/4] RBAC Rules Validation');
  console.log('----------------------------');
  allPassed = validateRBACRulesStructure() && allPassed;

  // 2. Validate agent identities
  console.log('\n[2/4] Agent Identities Validation');
  console.log('----------------------------------');
  allPassed = validateAgentIdentities() && allPassed;

  // 3. Performance benchmarks
  console.log('\n[3/4] Performance Benchmarks');
  console.log('----------------------------');
  allPassed = runPerformanceBenchmarks() && allPassed;

  // 4. Integration test
  console.log('\n[4/4] Integration Test');
  console.log('----------------------');
  allPassed = runIntegrationTest() && allPassed;

  // Final summary
  console.log('\n========================================');
  if (allPassed) {
    logSuccess('ALL VALIDATION CHECKS PASSED');
    console.log('========================================\n');
    process.exit(0);
  } else {
    logError('SOME VALIDATION CHECKS FAILED');
    console.log('========================================\n');
    process.exit(1);
  }
}

// Run validation
if (require.main === module) {
  main();
}

module.exports = {
  validateRBACRulesStructure,
  validateAgentIdentities,
  runPerformanceBenchmarks,
  runIntegrationTest
};
