/**
 * Identity & RBAC Pipeline Orchestrator
 * Coordinates all 6 security hooks in sequence
 * Provides unified API for RBAC enforcement
 * Performance: <100ms total for all 6 hooks
 */

const preIdentityVerify = require('./security-hooks/pre-identity-verify');
const prePermissionCheck = require('./security-hooks/pre-permission-check');
const preBudgetEnforce = require('./security-hooks/pre-budget-enforce');
const preApprovalGate = require('./security-hooks/pre-approval-gate');
const postAuditTrail = require('./security-hooks/post-audit-trail');
const postBudgetDeduct = require('./security-hooks/post-budget-deduct');

class IdentityRBACPipeline {
  constructor() {
    this.hooks = {
      pre: [
        { name: 'pre-identity-verify', handler: preIdentityVerify, priority: 1, blocking: true },
        { name: 'pre-permission-check', handler: prePermissionCheck, priority: 2, blocking: true },
        { name: 'pre-budget-enforce', handler: preBudgetEnforce, priority: 3, blocking: true },
        { name: 'pre-approval-gate', handler: preApprovalGate, priority: 4, blocking: true }
      ],
      post: [
        { name: 'post-audit-trail', handler: postAuditTrail, priority: 5, blocking: false },
        { name: 'post-budget-deduct', handler: postBudgetDeduct, priority: 6, blocking: false }
      ]
    };

    this.stats = {
      totalExecutions: 0,
      successfulExecutions: 0,
      blockedExecutions: 0,
      averageExecutionTime: 0,
      hookStats: {}
    };
  }

  /**
   * Execute pre-operation hooks (blocking)
   * All hooks must pass for operation to proceed
   * @param {string} agentId - Agent identifier
   * @param {string} operation - Operation name
   * @param {object} context - Operation context
   * @returns {object} Aggregated result
   */
  async executePreHooks(agentId, operation, context = {}) {
    const startTime = Date.now();
    const results = [];
    const enrichedContext = {
      ...context,
      agentId,
      operation,
      toolName: operation
    };

    // Execute all pre-hooks in sequence
    for (const hook of this.hooks.pre) {
      try {
        const hookStartTime = Date.now();
        const result = await hook.handler.execute(enrichedContext);
        const hookExecutionTime = Date.now() - hookStartTime;

        // Update stats
        this.updateHookStats(hook.name, hookExecutionTime, result.allowed);

        results.push({
          hook: hook.name,
          priority: hook.priority,
          ...result
        });

        // If blocking hook fails, stop pipeline
        if (hook.blocking && !result.allowed) {
          console.warn(`[RBAC Pipeline] Blocked by ${hook.name}: ${result.reason}`);

          return {
            allowed: false,
            blockedBy: hook.name,
            reason: result.reason,
            agentId,
            operation,
            hookResults: results,
            totalExecutionTime: Date.now() - startTime
          };
        }

      } catch (error) {
        console.error(`[RBAC Pipeline] Error in ${hook.name}:`, error.message);

        // Blocking hook errors block the operation
        if (hook.blocking) {
          results.push({
            hook: hook.name,
            priority: hook.priority,
            allowed: false,
            reason: `Hook error: ${error.message}`,
            error: error.message
          });

          return {
            allowed: false,
            blockedBy: hook.name,
            reason: `Hook error: ${error.message}`,
            agentId,
            operation,
            hookResults: results,
            totalExecutionTime: Date.now() - startTime,
            error: error.message
          };
        }
      }
    }

    // All pre-hooks passed
    const totalTime = Date.now() - startTime;

    return {
      allowed: true,
      reason: 'All pre-hooks passed',
      agentId,
      operation,
      hookResults: results,
      totalExecutionTime: totalTime
    };
  }

  /**
   * Execute post-operation hooks (non-blocking)
   * These run after the operation completes
   * @param {string} agentId - Agent identifier
   * @param {string} operation - Operation name
   * @param {object} context - Operation context
   * @param {object} operationResult - Result from the operation
   */
  async executePostHooks(agentId, operation, context = {}, operationResult = {}) {
    const startTime = Date.now();
    const results = [];
    const enrichedContext = {
      ...context,
      agentId,
      operation,
      toolName: operation,
      result: operationResult
    };

    // Execute all post-hooks (async, non-blocking)
    const promises = this.hooks.post.map(async (hook) => {
      try {
        const hookStartTime = Date.now();
        const result = await hook.handler.execute(enrichedContext);
        const hookExecutionTime = Date.now() - hookStartTime;

        // Update stats
        this.updateHookStats(hook.name, hookExecutionTime, result.success !== false);

        return {
          hook: hook.name,
          priority: hook.priority,
          ...result
        };

      } catch (error) {
        console.error(`[RBAC Pipeline] Error in ${hook.name}:`, error.message);

        return {
          hook: hook.name,
          priority: hook.priority,
          success: false,
          reason: `Hook error: ${error.message}`,
          error: error.message
        };
      }
    });

    // Wait for all post-hooks (but don't block operation)
    const hookResults = await Promise.allSettled(promises);

    hookResults.forEach((settled, idx) => {
      if (settled.status === 'fulfilled') {
        results.push(settled.value);
      } else {
        results.push({
          hook: this.hooks.post[idx].name,
          success: false,
          reason: `Promise rejected: ${settled.reason}`,
          error: settled.reason
        });
      }
    });

    return {
      success: true,
      reason: 'Post-hooks completed',
      agentId,
      operation,
      hookResults: results,
      totalExecutionTime: Date.now() - startTime
    };
  }

  /**
   * Unified RBAC enforcement API
   * Executes pre-hooks and returns authorization decision
   * @param {string} agentId - Agent identifier
   * @param {string} operation - Operation name
   * @param {object} context - Operation context
   * @returns {object} Authorization result with budget info
   */
  async enforceRBAC(agentId, operation, context = {}) {
    const startTime = Date.now();

    this.stats.totalExecutions++;

    try {
      const result = await this.executePreHooks(agentId, operation, context);

      if (result.allowed) {
        this.stats.successfulExecutions++;
      } else {
        this.stats.blockedExecutions++;
      }

      // Update average execution time
      this.stats.averageExecutionTime =
        (this.stats.averageExecutionTime * (this.stats.totalExecutions - 1) +
         result.totalExecutionTime) / this.stats.totalExecutions;

      // Extract budget info from results
      const budgetResult = result.hookResults?.find(r => r.hook === 'pre-budget-enforce');

      return {
        allowed: result.allowed,
        reasons: result.hookResults?.map(r => `${r.hook}: ${r.reason}`) || [],
        blockedBy: result.blockedBy,
        budgetRemaining: budgetResult?.remaining || null,
        metadata: {
          agentId,
          operation,
          executionTime: result.totalExecutionTime,
          hooksPassed: result.hookResults?.filter(r => r.allowed).length || 0,
          hooksTotal: this.hooks.pre.length
        }
      };

    } catch (error) {
      console.error('[RBAC Pipeline] Enforcement error:', error.message);

      this.stats.blockedExecutions++;

      return {
        allowed: false,
        reasons: [`Pipeline error: ${error.message}`],
        blockedBy: 'pipeline-error',
        budgetRemaining: null,
        metadata: {
          agentId,
          operation,
          executionTime: Date.now() - startTime,
          error: error.message
        }
      };
    }
  }

  /**
   * Update hook statistics
   * @param {string} hookName - Hook name
   * @param {number} executionTime - Execution time in ms
   * @param {boolean} success - Whether hook succeeded
   */
  updateHookStats(hookName, executionTime, success) {
    if (!this.stats.hookStats[hookName]) {
      this.stats.hookStats[hookName] = {
        executions: 0,
        successes: 0,
        failures: 0,
        averageTime: 0
      };
    }

    const stats = this.stats.hookStats[hookName];
    stats.executions++;

    if (success) {
      stats.successes++;
    } else {
      stats.failures++;
    }

    stats.averageTime =
      (stats.averageTime * (stats.executions - 1) + executionTime) / stats.executions;
  }

  /**
   * Get pipeline statistics
   */
  getStats() {
    return {
      ...this.stats,
      successRate: this.stats.totalExecutions > 0 ?
        (this.stats.successfulExecutions / this.stats.totalExecutions * 100).toFixed(2) + '%' :
        'N/A',
      blockRate: this.stats.totalExecutions > 0 ?
        (this.stats.blockedExecutions / this.stats.totalExecutions * 100).toFixed(2) + '%' :
        'N/A'
    };
  }

  /**
   * Reset statistics
   */
  resetStats() {
    this.stats = {
      totalExecutions: 0,
      successfulExecutions: 0,
      blockedExecutions: 0,
      averageExecutionTime: 0,
      hookStats: {}
    };
  }
}

// Export singleton instance
module.exports = new IdentityRBACPipeline();
