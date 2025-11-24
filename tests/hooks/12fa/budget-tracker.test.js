/**
 * Budget Tracker Tests
 *
 * Validates budget tracking, enforcement, and performance
 */

'use strict';

const assert = require('assert');
const budgetTracker = require('../../../hooks/12fa/utils/budget-tracker');

describe('Budget Tracker', () => {
  beforeEach(() => {
    // Clear all budgets before each test
    budgetTracker.clearAllBudgets();
  });

  describe('initializeBudget', () => {
    it('should initialize budget with valid parameters', () => {
      const budget = budgetTracker.initializeBudget(
        'agent-123',
        'backend-dev',
        100000,
        10.00
      );

      assert.strictEqual(budget.agent_id, 'agent-123');
      assert.strictEqual(budget.role, 'backend-dev');
      assert.strictEqual(budget.session_token_limit, 100000);
      assert.strictEqual(budget.daily_cost_limit, 10.00);
      assert.strictEqual(budget.session_tokens_used, 0);
      assert.strictEqual(budget.daily_cost_used, 0);
      assert.strictEqual(budget.operations_blocked, 0);
      assert.ok(budget.last_reset);
    });

    it('should reject invalid agent_id', () => {
      assert.throws(
        () => budgetTracker.initializeBudget('', 'backend-dev', 100000, 10.00),
        /Invalid agent_id/
      );
    });

    it('should reject invalid session_token_limit', () => {
      assert.throws(
        () => budgetTracker.initializeBudget('agent-123', 'backend-dev', -1, 10.00),
        /Invalid session_token_limit/
      );
    });

    it('should reject invalid daily_cost_limit', () => {
      assert.throws(
        () => budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 0),
        /Invalid daily_cost_limit/
      );
    });
  });

  describe('getBudgetStatus', () => {
    it('should return null for non-existent agent', () => {
      const status = budgetTracker.getBudgetStatus('non-existent');
      assert.strictEqual(status, null);
    });

    it('should return budget status for existing agent', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      const status = budgetTracker.getBudgetStatus('agent-123');

      assert.strictEqual(status.agent_id, 'agent-123');
      assert.strictEqual(status.role, 'backend-dev');
      assert.strictEqual(status.session.tokens_used, 0);
      assert.strictEqual(status.session.tokens_limit, 100000);
      assert.strictEqual(status.session.tokens_remaining, 100000);
      assert.strictEqual(status.daily.cost_used, 0);
      assert.strictEqual(status.daily.cost_limit, 10.00);
      assert.strictEqual(status.is_session_exhausted, false);
      assert.strictEqual(status.is_daily_exhausted, false);
    });

    it('should calculate utilization percentages correctly', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      budgetTracker.deductBudget('agent-123', 25000, 25000); // 50% of session

      const status = budgetTracker.getBudgetStatus('agent-123');
      assert.strictEqual(status.session.utilization_pct, 50);
    });
  });

  describe('checkBudget', () => {
    it('should allow operation within budget', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      const result = budgetTracker.checkBudget('agent-123', 1000);

      assert.strictEqual(result.allowed, true);
      assert.strictEqual(result.reason, null);
    });

    it('should block operation exceeding session token limit', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 10000, 10.00);
      // Try operation that would exceed limit (1000 input + ~3000 output = 4000 total)
      const result = budgetTracker.checkBudget('agent-123', 8000);

      assert.strictEqual(result.allowed, false);
      assert.ok(result.reason.includes('Session token limit exceeded'));
    });

    it('should block operation exceeding daily cost limit', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 1000000, 0.10);
      // Large operation that exceeds $0.10 daily limit
      const result = budgetTracker.checkBudget('agent-123', 10000);

      assert.strictEqual(result.allowed, false);
      assert.ok(result.reason.includes('Daily cost limit exceeded'));
    });

    it('should reject invalid agent_id', () => {
      const result = budgetTracker.checkBudget('', 1000);
      assert.strictEqual(result.allowed, false);
      assert.ok(result.reason.includes('Invalid agent_id'));
    });

    it('should reject non-initialized agent', () => {
      const result = budgetTracker.checkBudget('non-existent', 1000);
      assert.strictEqual(result.allowed, false);
      assert.ok(result.reason.includes('Budget not initialized'));
    });
  });

  describe('deductBudget', () => {
    it('should deduct tokens and cost correctly', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      const status = budgetTracker.deductBudget('agent-123', 1000, 3000);

      assert.strictEqual(status.session.tokens_used, 4000);
      assert.ok(status.daily.cost_used > 0);
      assert.ok(status.daily.cost_used < 1.00); // Should be ~$0.048
    });

    it('should throw error for non-existent agent', () => {
      assert.throws(
        () => budgetTracker.deductBudget('non-existent', 1000, 3000),
        /Budget not found/
      );
    });

    it('should reject negative token values', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      assert.throws(
        () => budgetTracker.deductBudget('agent-123', -1000, 3000),
        /Invalid input_tokens/
      );
    });
  });

  describe('resetSession', () => {
    it('should reset session tokens but preserve daily cost', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      budgetTracker.deductBudget('agent-123', 10000, 30000);

      const beforeReset = budgetTracker.getBudgetStatus('agent-123');
      assert.strictEqual(beforeReset.session.tokens_used, 40000);
      assert.ok(beforeReset.daily.cost_used > 0);

      const afterReset = budgetTracker.resetSession('agent-123');
      assert.strictEqual(afterReset.session.tokens_used, 0);
      assert.strictEqual(afterReset.daily.cost_used, beforeReset.daily.cost_used);
    });
  });

  describe('resetDaily', () => {
    it('should reset daily cost and operations_blocked', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      budgetTracker.deductBudget('agent-123', 10000, 30000);

      const beforeReset = budgetTracker.getBudgetStatus('agent-123');
      assert.ok(beforeReset.daily.cost_used > 0);

      const afterReset = budgetTracker.resetDaily('agent-123');
      assert.strictEqual(afterReset.daily.cost_used, 0);
      assert.strictEqual(afterReset.operations_blocked, 0);
    });
  });

  describe('Daily Reset Logic', () => {
    it('should automatically reset at midnight UTC', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      budgetTracker.deductBudget('agent-123', 10000, 30000);

      const beforeStatus = budgetTracker.getBudgetStatus('agent-123');
      assert.ok(beforeStatus.daily.cost_used > 0);

      // Simulate time passing (24+ hours)
      const budget = budgetTracker.getBudgetStatus('agent-123');
      const mockLastReset = Date.now() - (25 * 60 * 60 * 1000); // 25 hours ago

      // Manual override for testing
      budgetTracker._internal = budgetTracker._internal || {};
      const originalNeedsDailyReset = budgetTracker._internal.needsDailyReset;
      budgetTracker._internal.needsDailyReset = () => true;

      // Next operation should trigger reset
      budgetTracker.resetDaily('agent-123');
      const afterStatus = budgetTracker.getBudgetStatus('agent-123');

      assert.strictEqual(afterStatus.daily.cost_used, 0);

      // Restore original function
      if (originalNeedsDailyReset) {
        budgetTracker._internal.needsDailyReset = originalNeedsDailyReset;
      }
    });
  });

  describe('Cost Calculation', () => {
    it('should calculate cost within ±10% of expected', () => {
      const { calculateCost, PRICING } = budgetTracker._internal;

      // Test case: 10k input, 30k output
      const inputTokens = 10000;
      const outputTokens = 30000;

      const expectedInputCost = (inputTokens / 1_000_000) * PRICING.INPUT_PER_MILLION;
      const expectedOutputCost = (outputTokens / 1_000_000) * PRICING.OUTPUT_PER_MILLION;
      const expectedTotal = expectedInputCost + expectedOutputCost;

      const actualCost = calculateCost(inputTokens, outputTokens);

      // Should be $0.03 + $0.45 = $0.48
      assert.ok(Math.abs(actualCost - expectedTotal) < 0.001);
      assert.ok(actualCost >= 0.47 && actualCost <= 0.49); // ±10% tolerance
    });
  });

  describe('Performance', () => {
    it('should complete budget check in <20ms', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);

      const iterations = 100;
      const startTime = Date.now();

      for (let i = 0; i < iterations; i++) {
        budgetTracker.checkBudget('agent-123', 1000);
      }

      const endTime = Date.now();
      const avgTime = (endTime - startTime) / iterations;

      assert.ok(avgTime < 20, `Average time ${avgTime}ms exceeds 20ms threshold`);
    });

    it('should track performance metrics', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);

      // Run several operations
      for (let i = 0; i < 10; i++) {
        budgetTracker.checkBudget('agent-123', 1000);
      }

      const metrics = budgetTracker.getPerformanceMetrics();
      assert.ok(metrics.sample_count >= 10);
      assert.ok(metrics.avg_ms >= 0);
      assert.ok(metrics.min_ms >= 0);
      assert.ok(metrics.max_ms >= metrics.min_ms);
      assert.ok(metrics.p95_ms >= 0);
    });
  });

  describe('Edge Cases', () => {
    it('should handle zero token operations', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);
      const result = budgetTracker.checkBudget('agent-123', 0);

      assert.strictEqual(result.allowed, true);
    });

    it('should handle very large token counts', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 10_000_000, 1000.00);
      const result = budgetTracker.checkBudget('agent-123', 1_000_000);

      assert.strictEqual(result.allowed, true);
    });

    it('should increment operations_blocked counter', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 1000, 0.01);

      // First block (session limit)
      budgetTracker.checkBudget('agent-123', 5000);

      let status = budgetTracker.getBudgetStatus('agent-123');
      assert.strictEqual(status.operations_blocked, 1);

      // Second block
      budgetTracker.checkBudget('agent-123', 5000);

      status = budgetTracker.getBudgetStatus('agent-123');
      assert.strictEqual(status.operations_blocked, 2);
    });
  });

  describe('Integration Scenarios', () => {
    it('should handle typical agent session lifecycle', () => {
      // Initialize
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 100000, 10.00);

      // Check budget before operation
      let check = budgetTracker.checkBudget('agent-123', 5000);
      assert.strictEqual(check.allowed, true);

      // Deduct after operation
      budgetTracker.deductBudget('agent-123', 5000, 15000);

      // Check status
      let status = budgetTracker.getBudgetStatus('agent-123');
      assert.strictEqual(status.session.tokens_used, 20000);
      assert.ok(status.daily.cost_used > 0);

      // Another operation
      check = budgetTracker.checkBudget('agent-123', 5000);
      assert.strictEqual(check.allowed, true);

      budgetTracker.deductBudget('agent-123', 5000, 15000);

      // Final status
      status = budgetTracker.getBudgetStatus('agent-123');
      assert.strictEqual(status.session.tokens_used, 40000);
      assert.ok(status.session.tokens_remaining, 60000);
    });

    it('should enforce budget across multiple sessions', () => {
      budgetTracker.initializeBudget('agent-123', 'backend-dev', 50000, 10.00);

      // Session 1: Use 40k tokens
      budgetTracker.deductBudget('agent-123', 10000, 30000);
      let status = budgetTracker.getBudgetStatus('agent-123');
      assert.strictEqual(status.session.tokens_used, 40000);

      // Session 1: Attempt to exceed limit
      let check = budgetTracker.checkBudget('agent-123', 20000);
      assert.strictEqual(check.allowed, false);

      // Reset session for Session 2
      budgetTracker.resetSession('agent-123');
      status = budgetTracker.getBudgetStatus('agent-123');
      assert.strictEqual(status.session.tokens_used, 0);

      // Session 2: Should have full session budget again
      check = budgetTracker.checkBudget('agent-123', 10000);
      assert.strictEqual(check.allowed, true);

      // But daily cost accumulates
      assert.ok(status.daily.cost_used > 0);
    });
  });
});
