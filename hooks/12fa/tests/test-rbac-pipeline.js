/**
 * Integration Tests for RBAC Pipeline
 * Tests all 6 security hooks and pipeline orchestrator
 */

const pipeline = require('../identity-rbac-pipeline');
const identity = require('../identity');
const permissionChecker = require('../permission-checker');
const budgetTracker = require('../budget-tracker');

// Test utilities
function assert(condition, message) {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`);
  }
}

function log(message) {
  console.log(`[Test] ${message}`);
}

async function runTests() {
  log('Starting RBAC Pipeline Integration Tests...\n');

  try {
    // Test 1: Identity Verification
    log('Test 1: Identity Verification');
    identity.register('test-agent-1', 'public-key-123', { category: 'coder' });
    const verifyResult = identity.verify('test-agent-1');
    assert(verifyResult.verified, 'Agent should be verified after registration');
    log('PASS: Identity verification works\n');

    // Test 2: Permission Checking
    log('Test 2: Permission Checking');
    permissionChecker.assignRole('test-agent-1', 'developer');
    const permResult = permissionChecker.checkPermission('test-agent-1', 'Edit');
    assert(permResult.allowed, 'Developer should have Edit permission');
    log('PASS: Permission checking works\n');

    // Test 3: Budget Tracking
    log('Test 3: Budget Tracking');
    budgetTracker.initBudget('test-agent-1', { tokensPerDay: 10000 });
    const budgetCheck = budgetTracker.checkBudget('test-agent-1', { estimatedTokens: 500 });
    assert(budgetCheck.allowed, 'Budget check should pass for reasonable usage');
    log('PASS: Budget tracking works\n');

    // Test 4: Pre-Hooks Pipeline (Allowed Operation)
    log('Test 4: Pre-Hooks Pipeline - Allowed Operation');
    const allowedResult = await pipeline.enforceRBAC('test-agent-1', 'Read', {
      filePath: 'src/test.js'
    });
    assert(allowedResult.allowed, 'Read operation should be allowed');
    assert(allowedResult.reasons.length === 4, 'Should have 4 pre-hook results');
    assert(allowedResult.metadata.hooksPassed === 4, 'All 4 hooks should pass');
    log(`PASS: Pre-hooks pipeline allowed operation (${allowedResult.metadata.executionTime}ms)\n`);

    // Test 5: Pre-Hooks Pipeline (Blocked by Permission)
    log('Test 5: Pre-Hooks Pipeline - Blocked by Permission');
    permissionChecker.assignRole('test-agent-2', 'reviewer'); // Read-only role
    const blockedResult = await pipeline.enforceRBAC('test-agent-2', 'Write', {
      filePath: 'src/important.js'
    });
    assert(!blockedResult.allowed, 'Write operation should be blocked for reviewer');
    assert(blockedResult.blockedBy === 'pre-permission-check', 'Should be blocked by permission check');
    log('PASS: Pre-hooks pipeline blocked unauthorized operation\n');

    // Test 6: Pre-Hooks Pipeline (Blocked by Budget)
    log('Test 6: Pre-Hooks Pipeline - Blocked by Budget');
    budgetTracker.initBudget('test-agent-3', { tokensPerDay: 100 }); // Very low budget
    const budgetBlockedResult = await pipeline.enforceRBAC('test-agent-3', 'Task', {
      description: 'Spawn expensive task'
    });
    assert(!budgetBlockedResult.allowed, 'Expensive operation should be blocked by budget');
    assert(budgetBlockedResult.blockedBy === 'pre-budget-enforce', 'Should be blocked by budget');
    log('PASS: Pre-hooks pipeline blocked over-budget operation\n');

    // Test 7: Post-Hooks Pipeline
    log('Test 7: Post-Hooks Pipeline');
    const postResult = await pipeline.executePostHooks('test-agent-1', 'Edit', {
      filePath: 'src/test.js',
      fileSize: 5000
    }, {
      success: true,
      executionTime: 123
    });
    assert(postResult.success, 'Post-hooks should complete successfully');
    assert(postResult.hookResults.length === 2, 'Should have 2 post-hook results');
    log('PASS: Post-hooks pipeline completed\n');

    // Test 8: Performance (All Hooks < 100ms)
    log('Test 8: Performance Test');
    const perfStart = Date.now();
    await pipeline.enforceRBAC('test-agent-1', 'Edit', { filePath: 'test.js' });
    const perfTime = Date.now() - perfStart;
    assert(perfTime < 100, `Total execution time should be < 100ms (was ${perfTime}ms)`);
    log(`PASS: Performance test (${perfTime}ms < 100ms)\n`);

    // Test 9: Pipeline Statistics
    log('Test 9: Pipeline Statistics');
    const stats = pipeline.getStats();
    assert(stats.totalExecutions > 0, 'Should have execution statistics');
    assert(stats.successRate !== 'N/A', 'Should have success rate');
    log(`PASS: Statistics tracking works (${stats.totalExecutions} executions, ${stats.successRate} success rate)\n`);

    // Test 10: Budget Deduction
    log('Test 10: Budget Deduction After Operation');
    budgetTracker.initBudget('test-agent-fresh', { tokensPerDay: 10000 });
    const beforeBudget = budgetTracker.getStatus('test-agent-fresh');
    const beforeTokens = beforeBudget.usage.tokensUsed;
    budgetTracker.deduct('test-agent-fresh', { tokensUsed: 1000, cost: 0.002 });
    const afterBudget = budgetTracker.getStatus('test-agent-fresh');
    const afterTokens = afterBudget.usage.tokensUsed;
    assert(afterTokens === beforeTokens + 1000,
           `Budget should be deducted correctly (before: ${beforeTokens}, after: ${afterTokens})`);
    log('PASS: Budget deduction works\n');

    // Test 11: High-Risk Operation (Auto-Approve in Dev Mode)
    log('Test 11: High-Risk Operation Approval');
    process.env.AUTO_APPROVE_HIGH_RISK = 'true';
    const highRiskResult = await pipeline.enforceRBAC('test-agent-1', 'Bash', {
      command: 'rm -rf test'
    });
    assert(highRiskResult.allowed, 'High-risk operation should be auto-approved in dev mode');
    const approvalHook = highRiskResult.metadata;
    log('PASS: High-risk operation approval works\n');

    // Summary
    log('='.repeat(50));
    log('ALL TESTS PASSED!');
    log('='.repeat(50));

    const finalStats = pipeline.getStats();
    console.log('\nFinal Pipeline Statistics:');
    console.log(JSON.stringify(finalStats, null, 2));

  } catch (error) {
    console.error('\nTEST FAILED:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// Run tests
runTests().then(() => {
  console.log('\nTest suite completed successfully!');
  process.exit(0);
}).catch(error => {
  console.error('\nTest suite failed:', error);
  process.exit(1);
});
