/**
 * Permission Checker Stub - For Budget Tracker Integration
 *
 * This is a stub that shows how permission-checker.js will integrate
 * with budget-tracker.js once implemented by Security Manager.
 *
 * @module permission-checker-stub
 * @version 1.0.0
 */

'use strict';

const budgetTracker = require('./budget-tracker');

/**
 * Check if agent has permission to perform operation
 * with budget enforcement
 *
 * @param {string} agentId - Agent identifier
 * @param {string} operation - Operation to perform
 * @param {Object} context - Operation context
 * @param {number} context.estimatedTokens - Estimated tokens for operation
 * @returns {Object} {allowed: boolean, reason: string|null}
 */
async function checkPermission(agentId, operation, context = {}) {
  // Step 1: Check RBAC permissions (to be implemented by Security Manager)
  // const rbacCheck = await checkRBAC(agentId, operation);
  // if (!rbacCheck.allowed) {
  //   return rbacCheck;
  // }

  // Step 2: Check budget limits
  const estimatedTokens = context.estimatedTokens || 1000;
  const budgetCheck = budgetTracker.checkBudget(agentId, estimatedTokens);

  if (!budgetCheck.allowed) {
    return {
      allowed: false,
      reason: `Budget exceeded: ${budgetCheck.reason}`
    };
  }

  // Step 3: All checks passed
  return {
    allowed: true,
    reason: null
  };
}

/**
 * Record operation completion and deduct budget
 *
 * @param {string} agentId - Agent identifier
 * @param {string} operation - Operation performed
 * @param {Object} usage - Token usage
 * @param {number} usage.inputTokens - Input tokens used
 * @param {number} usage.outputTokens - Output tokens used
 * @returns {Object} Updated budget status
 */
async function recordOperation(agentId, operation, usage) {
  const { inputTokens = 0, outputTokens = 0 } = usage;

  // Deduct from budget
  const status = budgetTracker.deductBudget(agentId, inputTokens, outputTokens);

  // Log operation (to be implemented by Security Manager)
  // await auditLog.record({
  //   agent_id: agentId,
  //   operation,
  //   input_tokens: inputTokens,
  //   output_tokens: outputTokens,
  //   cost: status.daily.cost_used,
  //   timestamp: Date.now()
  // });

  return status;
}

/**
 * Example integration pattern
 *
 * Usage:
 *
 * // Before operation
 * const check = await checkPermission('agent-123', 'read_file', {
 *   estimatedTokens: 5000
 * });
 *
 * if (!check.allowed) {
 *   throw new Error(`Permission denied: ${check.reason}`);
 * }
 *
 * // Perform operation
 * const result = await performOperation();
 *
 * // After operation
 * await recordOperation('agent-123', 'read_file', {
 *   inputTokens: 4800,
 *   outputTokens: 15200
 * });
 */

module.exports = {
  checkPermission,
  recordOperation
};
