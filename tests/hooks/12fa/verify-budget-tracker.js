/**
 * Budget Tracker Verification Script
 * Runs basic tests without mocha/chai
 */

'use strict';

const budgetTracker = require('../../../hooks/12fa/utils/budget-tracker');

let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`  PASS: ${message}`);
    passed++;
  } else {
    console.error(`  FAIL: ${message}`);
    failed++;
  }
}

function test(description, fn) {
  console.log(`\nTest: ${description}`);
  try {
    fn();
  } catch (error) {
    console.error(`  ERROR: ${error.message}`);
    failed++;
  }
}

console.log('=== Budget Tracker Verification ===\n');

// Test 1: Initialization
test('Initialize budget with valid parameters', () => {
  budgetTracker.clearAllBudgets();
  const budget = budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);

  assert(budget.agent_id === 'agent-123', 'agent_id is correct');
  assert(budget.role === 'backend-dev', 'role is correct');
  assert(budget.session_token_limit === 100000, 'session_token_limit is correct');
  assert(budget.daily_cost_limit === 10.00, 'daily_cost_limit is correct');
  assert(budget.session_tokens_used === 0, 'session_tokens_used starts at 0');
  assert(budget.daily_cost_used === 0, 'daily_cost_used starts at 0');
});

// Test 2: Get Budget Status
test('Get budget status for existing agent', () => {
  budgetTracker.clearAllBudgets();
  budgetTracker.initializeBudget('agent-456', 'coder', 50000, 5.00);
  const status = budgetTracker.getBudgetStatus('agent-456');

  assert(status !== null, 'status is not null');
  assert(status.agent_id === 'agent-456', 'agent_id matches');
  assert(status.session.tokens_remaining === 50000, 'tokens_remaining is correct');
  assert(status.daily.cost_remaining === 5.00, 'cost_remaining is correct');
  assert(status.is_session_exhausted === false, 'session not exhausted');
  assert(status.is_daily_exhausted === false, 'daily not exhausted');
});

// Test 3: Check Budget (Allow)
test('Allow operation within budget', () => {
  budgetTracker.clearAllBudgets();
  budgetTracker.initializeBudget('agent-789', 'tester', 100000, 10.00);
  const result = budgetTracker.checkBudget('agent-789', 1000);

  assert(result.allowed === true, 'operation allowed');
  assert(result.reason === null, 'no rejection reason');
});

// Test 4: Check Budget (Block)
test('Block operation exceeding session limit', () => {
  budgetTracker.clearAllBudgets();
  budgetTracker.initializeBudget('agent-999', 'reviewer', 10000, 10.00);
  const result = budgetTracker.checkBudget('agent-999', 8000);

  assert(result.allowed === false, 'operation blocked');
  assert(result.reason.includes('Session token limit'), 'correct rejection reason');
});

// Test 5: Deduct Budget
test('Deduct tokens and cost correctly', () => {
  budgetTracker.clearAllBudgets();
  budgetTracker.initializeBudget('agent-111', 'backend-dev', 100000, 10.00);

  const beforeStatus = budgetTracker.getBudgetStatus('agent-111');
  assert(beforeStatus.session.tokens_used === 0, 'tokens start at 0');

  const afterStatus = budgetTracker.deductBudget('agent-111', 1000, 3000);
  assert(afterStatus.session.tokens_used === 4000, 'tokens deducted correctly (1000 + 3000)');
  assert(afterStatus.daily.cost_used > 0, 'cost was calculated');
  assert(afterStatus.daily.cost_used < 1.00, 'cost is reasonable (<$1)');
});

// Test 6: Cost Calculation Accuracy
test('Calculate cost within acceptable range', () => {
  const { calculateCost, PRICING } = budgetTracker._internal;

  const inputTokens = 10000;
  const outputTokens = 30000;

  const expectedInputCost = (inputTokens / 1_000_000) * PRICING.INPUT_PER_MILLION;
  const expectedOutputCost = (outputTokens / 1_000_000) * PRICING.OUTPUT_PER_MILLION;
  const expectedTotal = expectedInputCost + expectedOutputCost;

  const actualCost = calculateCost(inputTokens, outputTokens);

  // Expected: $0.03 (input) + $0.45 (output) = $0.48
  assert(Math.abs(actualCost - expectedTotal) < 0.001, 'cost calculation is accurate');
  assert(actualCost >= 0.43 && actualCost <= 0.53, 'cost within ±10% tolerance');
});

// Test 7: Reset Session
test('Reset session tokens but preserve daily cost', () => {
  budgetTracker.clearAllBudgets();
  budgetTracker.initializeBudget('agent-222', 'coder', 100000, 10.00);
  budgetTracker.deductBudget('agent-222', 10000, 30000);

  const beforeReset = budgetTracker.getBudgetStatus('agent-222');
  assert(beforeReset.session.tokens_used === 40000, 'tokens used before reset');

  const afterReset = budgetTracker.resetSession('agent-222');
  assert(afterReset.session.tokens_used === 0, 'session tokens reset to 0');
  assert(afterReset.daily.cost_used === beforeReset.daily.cost_used, 'daily cost preserved');
});

// Test 8: Reset Daily
test('Reset daily cost and operations_blocked', () => {
  budgetTracker.clearAllBudgets();
  budgetTracker.initializeBudget('agent-333', 'reviewer', 100000, 10.00);
  budgetTracker.deductBudget('agent-333', 10000, 30000);

  const beforeReset = budgetTracker.getBudgetStatus('agent-333');
  assert(beforeReset.daily.cost_used > 0, 'daily cost > 0 before reset');

  const afterReset = budgetTracker.resetDaily('agent-333');
  assert(afterReset.daily.cost_used === 0, 'daily cost reset to 0');
  assert(afterReset.operations_blocked === 0, 'operations_blocked reset to 0');
});

// Test 9: Performance
test('Budget checks complete in <20ms', () => {
  budgetTracker.clearAllBudgets();
  budgetTracker.initializeBudget('agent-444', 'tester', 100000, 10.00);

  const iterations = 100;
  const startTime = Date.now();

  for (let i = 0; i < iterations; i++) {
    budgetTracker.checkBudget('agent-444', 1000);
  }

  const endTime = Date.now();
  const avgTime = (endTime - startTime) / iterations;

  assert(avgTime < 20, `avg time ${avgTime.toFixed(2)}ms is <20ms`);

  const metrics = budgetTracker.getPerformanceMetrics();
  assert(metrics.sample_count > 0, 'performance metrics tracked');
  assert(metrics.avg_ms >= 0, 'avg_ms is valid');
});

// Test 10: Integration Scenario
test('Full agent session lifecycle', () => {
  budgetTracker.clearAllBudgets();
  budgetTracker.initializeBudget('agent-555', 'backend-dev', 100000, 10.00);

  // Operation 1
  let check = budgetTracker.checkBudget('agent-555', 5000);
  assert(check.allowed === true, 'operation 1 allowed');

  budgetTracker.deductBudget('agent-555', 5000, 15000);
  let status = budgetTracker.getBudgetStatus('agent-555');
  assert(status.session.tokens_used === 20000, 'tokens deducted after operation 1');

  // Operation 2
  check = budgetTracker.checkBudget('agent-555', 5000);
  assert(check.allowed === true, 'operation 2 allowed');

  budgetTracker.deductBudget('agent-555', 5000, 15000);
  status = budgetTracker.getBudgetStatus('agent-555');
  assert(status.session.tokens_used === 40000, 'tokens deducted after operation 2');
  assert(status.session.tokens_remaining === 60000, 'correct tokens remaining');
});

// Summary
console.log('\n=== Summary ===');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total: ${passed + failed}`);

if (failed > 0) {
  console.log('\nStatus: FAILED');
  process.exit(1);
} else {
  console.log('\nStatus: ALL TESTS PASSED');
  process.exit(0);
}
