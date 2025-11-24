/**
 * Integration Example - Budget Tracker + Permission Checker
 *
 * This example demonstrates how budget-tracker.js will integrate
 * with the full RBAC system once identity.js and permission-checker.js
 * are implemented by the Security Manager.
 *
 * @module integration-example
 * @version 1.0.0
 */

'use strict';

const budgetTracker = require('./budget-tracker');

// ============================================================================
// EXAMPLE 1: Agent Session Initialization
// ============================================================================

console.log('=== Example 1: Agent Session Initialization ===\n');

// Step 1: Initialize budget when agent starts session
const agentConfig = {
  agent_id: 'backend-dev-001',
  role: 'backend-dev',
  session_token_limit: 100000,  // 100k tokens per session
  daily_cost_limit: 10.00       // $10/day
};

const budget = budgetTracker.initializeBudget(
  agentConfig.agent_id,
  agentConfig.role,
  agentConfig.session_token_limit,
  agentConfig.daily_cost_limit
);

console.log('Agent initialized:', budget);
console.log('');

// ============================================================================
// EXAMPLE 2: Pre-Operation Budget Check
// ============================================================================

console.log('=== Example 2: Pre-Operation Budget Check ===\n');

// Before performing any operation, check budget
const operationRequest = {
  operation: 'read_file',
  file: 'src/large-file.js',
  estimatedTokens: 5000  // Conservative estimate
};

const budgetCheck = budgetTracker.checkBudget(
  agentConfig.agent_id,
  operationRequest.estimatedTokens
);

if (!budgetCheck.allowed) {
  console.error(`Operation blocked: ${budgetCheck.reason}`);
  process.exit(1);
}

console.log('Budget check passed:', budgetCheck);
console.log('');

// ============================================================================
// EXAMPLE 3: Post-Operation Budget Deduction
// ============================================================================

console.log('=== Example 3: Post-Operation Budget Deduction ===\n');

// After operation completes, deduct actual usage
const actualUsage = {
  inputTokens: 4800,   // Actual input tokens (slightly less than estimate)
  outputTokens: 15200  // Actual output tokens
};

const updatedStatus = budgetTracker.deductBudget(
  agentConfig.agent_id,
  actualUsage.inputTokens,
  actualUsage.outputTokens
);

console.log('Budget deducted:', {
  tokens_used: updatedStatus.session.tokens_used,
  tokens_remaining: updatedStatus.session.tokens_remaining,
  cost_used: `$${updatedStatus.daily.cost_used.toFixed(4)}`,
  cost_remaining: `$${updatedStatus.daily.cost_remaining.toFixed(4)}`
});
console.log('');

// ============================================================================
// EXAMPLE 4: Multiple Operations in Session
// ============================================================================

console.log('=== Example 4: Multiple Operations in Session ===\n');

const operations = [
  { name: 'write_file', estimatedTokens: 3000 },
  { name: 'run_tests', estimatedTokens: 8000 },
  { name: 'deploy', estimatedTokens: 2000 }
];

for (const op of operations) {
  // Check budget before each operation
  const check = budgetTracker.checkBudget(agentConfig.agent_id, op.estimatedTokens);

  if (!check.allowed) {
    console.error(`${op.name} blocked: ${check.reason}`);
    break;
  }

  console.log(`${op.name}: Budget check passed`);

  // Simulate operation (estimate output as 3x input)
  const outputTokens = op.estimatedTokens * 3;
  budgetTracker.deductBudget(agentConfig.agent_id, op.estimatedTokens, outputTokens);

  const status = budgetTracker.getBudgetStatus(agentConfig.agent_id);
  console.log(`  Tokens remaining: ${status.session.tokens_remaining}`);
  console.log(`  Cost remaining: $${status.daily.cost_remaining.toFixed(4)}`);
}

console.log('');

// ============================================================================
// EXAMPLE 5: Budget Exhaustion Handling
// ============================================================================

console.log('=== Example 5: Budget Exhaustion Handling ===\n');

// Try an operation that would exceed budget
const largeOperation = {
  name: 'analyze_entire_codebase',
  estimatedTokens: 80000  // This would exceed remaining budget
};

const exhaustionCheck = budgetTracker.checkBudget(
  agentConfig.agent_id,
  largeOperation.estimatedTokens
);

if (!exhaustionCheck.allowed) {
  console.log('Large operation blocked (as expected)');
  console.log(`Reason: ${exhaustionCheck.reason}`);

  const status = budgetTracker.getBudgetStatus(agentConfig.agent_id);
  console.log(`Current session usage: ${status.session.utilization_pct.toFixed(1)}%`);
  console.log(`Operations blocked: ${status.operations_blocked}`);
}

console.log('');

// ============================================================================
// EXAMPLE 6: Session Reset
// ============================================================================

console.log('=== Example 6: Session Reset ===\n');

console.log('Before reset:');
let status = budgetTracker.getBudgetStatus(agentConfig.agent_id);
console.log(`  Session tokens used: ${status.session.tokens_used}`);
console.log(`  Daily cost used: $${status.daily.cost_used.toFixed(4)}`);

// Reset session (new session, but daily cost persists)
budgetTracker.resetSession(agentConfig.agent_id);

console.log('\nAfter session reset:');
status = budgetTracker.getBudgetStatus(agentConfig.agent_id);
console.log(`  Session tokens used: ${status.session.tokens_used}`);
console.log(`  Daily cost used: $${status.daily.cost_used.toFixed(4)} (persists)`);

console.log('');

// ============================================================================
// EXAMPLE 7: Daily Budget Tracking Across Sessions
// ============================================================================

console.log('=== Example 7: Daily Budget Tracking Across Sessions ===\n');

// Session 1: Use 40k tokens
budgetTracker.deductBudget(agentConfig.agent_id, 10000, 30000);
console.log('Session 1 completed');

status = budgetTracker.getBudgetStatus(agentConfig.agent_id);
console.log(`Daily cost after session 1: $${status.daily.cost_used.toFixed(4)}`);

// Reset for session 2
budgetTracker.resetSession(agentConfig.agent_id);

// Session 2: Use another 40k tokens
budgetTracker.deductBudget(agentConfig.agent_id, 10000, 30000);
console.log('Session 2 completed');

status = budgetTracker.getBudgetStatus(agentConfig.agent_id);
console.log(`Daily cost after session 2: $${status.daily.cost_used.toFixed(4)}`);
console.log(`Daily utilization: ${status.daily.utilization_pct.toFixed(1)}%`);

console.log('');

// ============================================================================
// EXAMPLE 8: Performance Monitoring
// ============================================================================

console.log('=== Example 8: Performance Monitoring ===\n');

// Run many operations to collect performance data
for (let i = 0; i < 50; i++) {
  budgetTracker.checkBudget(agentConfig.agent_id, 1000);
}

const metrics = budgetTracker.getPerformanceMetrics();
console.log('Performance metrics:');
console.log(`  Sample count: ${metrics.sample_count}`);
console.log(`  Average time: ${metrics.avg_ms.toFixed(3)}ms`);
console.log(`  Min time: ${metrics.min_ms.toFixed(3)}ms`);
console.log(`  Max time: ${metrics.max_ms.toFixed(3)}ms`);
console.log(`  P95 time: ${metrics.p95_ms.toFixed(3)}ms`);

console.log('');

// ============================================================================
// EXAMPLE 9: Integration with Permission Checker (Future)
// ============================================================================

console.log('=== Example 9: Future Integration Pattern ===\n');

console.log('When Security Manager completes permission-checker.js:');
console.log('');
console.log('async function executeOperation(agentId, operation, context) {');
console.log('  // Step 1: Check RBAC permissions');
console.log('  const rbacCheck = await permissionChecker.checkRBAC(agentId, operation);');
console.log('  if (!rbacCheck.allowed) {');
console.log('    throw new Error(`RBAC denied: ${rbacCheck.reason}`);');
console.log('  }');
console.log('');
console.log('  // Step 2: Check budget (ALREADY IMPLEMENTED)');
console.log('  const budgetCheck = budgetTracker.checkBudget(agentId, context.estimatedTokens);');
console.log('  if (!budgetCheck.allowed) {');
console.log('    throw new Error(`Budget exceeded: ${budgetCheck.reason}`);');
console.log('  }');
console.log('');
console.log('  // Step 3: Execute operation');
console.log('  const result = await performOperation(operation, context);');
console.log('');
console.log('  // Step 4: Record usage (ALREADY IMPLEMENTED)');
console.log('  budgetTracker.deductBudget(agentId, result.inputTokens, result.outputTokens);');
console.log('');
console.log('  return result;');
console.log('}');

console.log('');

// ============================================================================
// FINAL STATUS
// ============================================================================

console.log('=== Final Status ===\n');

status = budgetTracker.getBudgetStatus(agentConfig.agent_id);
console.log('Agent:', status.agent_id);
console.log('Role:', status.role);
console.log('');
console.log('Session Budget:');
console.log(`  Used: ${status.session.tokens_used.toLocaleString()} tokens`);
console.log(`  Remaining: ${status.session.tokens_remaining.toLocaleString()} tokens`);
console.log(`  Utilization: ${status.session.utilization_pct.toFixed(1)}%`);
console.log('');
console.log('Daily Budget:');
console.log(`  Used: $${status.daily.cost_used.toFixed(4)}`);
console.log(`  Remaining: $${status.daily.cost_remaining.toFixed(4)}`);
console.log(`  Utilization: ${status.daily.utilization_pct.toFixed(1)}%`);
console.log('');
console.log('Operations blocked:', status.operations_blocked);
console.log('Session exhausted:', status.is_session_exhausted);
console.log('Daily exhausted:', status.is_daily_exhausted);

console.log('\n=== Integration Example Complete ===');
