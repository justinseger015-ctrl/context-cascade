/**
 * Budget Tracker v3.0
 * Tracks token/cost budgets for agent operations
 * Performance: <5ms per operation
 *
 * BLOCKER-2 FIX: Added Memory MCP persistence for cross-session continuity
 * v3.0: Uses x- prefixed custom fields for Anthropic-compliant format
 */

const fs = require('fs');
const path = require('path');

const BUDGET_STORE = path.join(__dirname, '.budget-store.json');

// BLOCKER-2: Import Memory MCP tagging protocol
let taggedMemoryStore, memoryMcpAvailable;
try {
  const taggingProtocol = require('./memory-mcp-tagging-protocol.js');
  taggedMemoryStore = taggingProtocol.taggedMemoryStore;
  memoryMcpAvailable = true;
  // Use stderr to avoid contaminating JSON stdout
  console.error('[BudgetTracker] Memory MCP tagging protocol loaded');
} catch (err) {
  memoryMcpAvailable = false;
  // Use stderr to avoid contaminating JSON stdout
  console.error('[BudgetTracker] Memory MCP not available - using file-only persistence');
}

class BudgetTracker {
  constructor() {
    this.budgets = this.loadBudgets();
  }

  loadBudgets() {
    // BLOCKER-2: Try Memory MCP first (if available), fall back to file
    // NOTE: Synchronous for constructor, async version added below

    try {
      if (fs.existsSync(BUDGET_STORE)) {
        // ISSUE #6 FIX: Verify file permissions and ownership on load
        const stats = fs.statSync(BUDGET_STORE);

        // Check if file is readable only by owner (mode 0o600)
        const mode = stats.mode & 0o777;
        if (mode !== 0o600 && process.platform !== 'win32') {
          // Windows doesn't support POSIX permissions, so skip check
          console.warn(`[BudgetTracker] WARNING: Insecure file permissions ${mode.toString(8)}. Fixing to 0o600...`);
          fs.chmodSync(BUDGET_STORE, 0o600);
        }

        const budgets = JSON.parse(fs.readFileSync(BUDGET_STORE, 'utf8'));
        // Use stderr to avoid contaminating JSON stdout
        console.error(`[BudgetTracker] Loaded budgets from file (${Object.keys(budgets.agents || {}).length} agents)`);
        return budgets;
      }
    } catch (error) {
      console.error('[BudgetTracker] Failed to load budgets from file:', error.message);
    }

    return {
      agents: {},
      globalBudget: {
        tokensPerDay: 1000000,
        tokensUsed: 0,
        resetAt: this.getNextResetTime()
      }
    };
  }

  /**
   * BLOCKER-2: Async initialization to load from Memory MCP
   */
  async initializeFromMemoryMCP() {
    if (!memoryMcpAvailable) {
      // Use stderr to avoid contaminating JSON stdout
      console.error('[BudgetTracker] Memory MCP unavailable, using file-only mode');
      return;
    }

    // Use stderr to avoid contaminating JSON stdout
    console.error('[BudgetTracker] Initializing from Memory MCP...');

    // Try to restore budget for known agents
    const knownAgents = ['coder', 'backend-dev', 'tester', 'reviewer', 'planner'];

    for (const agentId of knownAgents) {
      const budgetState = await this.loadBudgetStateFromMemoryMCP(agentId);
      if (budgetState && budgetState.usage) {
        this.budgets.agents[agentId] = {
          limits: budgetState.limits,
          usage: budgetState.usage
        };
        // Use stderr to avoid contaminating JSON stdout
        console.error(`[BudgetTracker] Restored ${agentId} from Memory MCP: ${budgetState.usage.tokensUsed} tokens used`);
      }
    }

    // Use stderr to avoid contaminating JSON stdout
    console.error('[BudgetTracker] Memory MCP initialization complete');
  }

  saveBudgets() {
    try {
      // Primary: File persistence (synchronous backup)
      // ISSUE #6 FIX: Enforce restrictive file permissions (owner read/write only)
      fs.writeFileSync(
        BUDGET_STORE,
        JSON.stringify(this.budgets, null, 2),
        { mode: 0o600 }  // Read/write for owner only (no group/world access)
      );

      // BLOCKER-2: Also persist to Memory MCP (asynchronous)
      if (memoryMcpAvailable) {
        this.saveBudgetsToMemoryMCP().catch(err => {
          console.error('[BudgetTracker] Memory MCP persistence failed:', err.message);
        });
      }
    } catch (error) {
      console.error('[BudgetTracker] Failed to save budgets:', error.message);
    }
  }

  /**
   * BLOCKER-2: Save budget state to Memory MCP for cross-session persistence
   * v3.0: Uses x- prefixed custom fields for Anthropic compliance
   */
  async saveBudgetsToMemoryMCP() {
    if (!memoryMcpAvailable) return;

    for (const [agentId, budget] of Object.entries(this.budgets.agents)) {
      try {
        const budgetData = {
          agentId,
          limits: budget.limits,
          usage: budget.usage,
          timestamp: new Date().toISOString(),
          'x-schema-version': '3.0'
        };

        // Use tagging protocol for WHO/WHEN/PROJECT/WHY metadata (v3.0 x- prefixed)
        const tagged = taggedMemoryStore(agentId, JSON.stringify(budgetData), {
          project: 'context-cascade',
          'x-intent': 'budget_persistence',
          'x-agent-id': agentId,
          'x-namespace': 'agent-reality-map/budgets'
        });

        // BLOCKER-3 ACTIVATED: Memory MCP persistence now enabled
        // Use stderr to avoid contaminating JSON stdout
        console.error(`[BudgetTracker] Persisting ${agentId} budget to Memory MCP (${budget.usage.tokensUsed} tokens used)`);

        // Store in Memory MCP with WHO/WHEN/PROJECT/WHY metadata
        if (typeof mcp__memory_mcp__memory_store === 'function') {
          await mcp__memory_mcp__memory_store({
            text: tagged.text,
            metadata: tagged.metadata
          });
        } else {
          console.warn(`[BudgetTracker] Memory MCP not available - budget will persist to file only`);
        }

      } catch (error) {
        console.error(`[BudgetTracker] Failed to persist ${agentId} to Memory MCP:`, error.message);
      }
    }
  }

  /**
   * BLOCKER-2: Load budget state from Memory MCP
   * v3.0: Supports both old and new metadata formats for backward compatibility
   */
  async loadBudgetStateFromMemoryMCP(agentId) {
    if (!memoryMcpAvailable) return null;

    try {
      // BLOCKER-3 ACTIVATED: Query Memory MCP for budget state
      // Use stderr to avoid contaminating JSON stdout
      console.error(`[BudgetTracker] Querying Memory MCP for ${agentId} budget...`);

      if (typeof mcp__memory_mcp__vector_search === 'function') {
        // v3.0: Query with x- prefixed fields, fall back to old format
        const results = await mcp__memory_mcp__vector_search({
          query: `budget state for ${agentId}`,
          limit: 1,
          metadata: {
            _agent: agentId,
            // Support both old and new project names
            $or: [
              { _project: 'context-cascade' },
              { _project: 'ruv-sparc-three-loop-system' }
            ],
            // Support both old (_intent) and new (x-intent) formats
            $or: [
              { _intent: 'budget_persistence' },
              { 'x-intent': 'budget_persistence' }
            ]
          }
        });

        if (results && results.length > 0) {
          const budgetData = JSON.parse(results[0].text);
          // Use stderr to avoid contaminating JSON stdout
          console.error(`[BudgetTracker] Restored ${agentId} budget from Memory MCP: ${budgetData.usage.tokensUsed} tokens used`);
          return budgetData;
        }

        // Use stderr to avoid contaminating JSON stdout
        console.error(`[BudgetTracker] No stored budget found for ${agentId} in Memory MCP`);
        return null;
      } else {
        console.warn(`[BudgetTracker] Memory MCP not available - using file-only mode`);
        return null;
      }

    } catch (error) {
      console.error(`[BudgetTracker] Memory MCP query failed for ${agentId}:`, error.message);
      return null;
    }
  }

  getNextResetTime() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(0, 0, 0, 0);
    return tomorrow.toISOString();
  }

  /**
   * Initialize budget for agent
   * @param {string} agentId - Agent identifier
   * @param {object} limits - Budget limits
   */
  initBudget(agentId, limits = {}) {
    const defaultLimits = {
      tokensPerHour: 100000,
      tokensPerDay: 500000,
      maxCostPerOperation: 0.1, // USD
      ...limits
    };

    this.budgets.agents[agentId] = {
      limits: defaultLimits,
      usage: {
        tokensUsed: 0,
        operationCount: 0,
        totalCost: 0,
        lastReset: new Date().toISOString()
      }
    };

    this.saveBudgets();
    return { success: true, agentId, limits: defaultLimits };
  }

  /**
   * Check if operation is within budget
   * @param {string} agentId - Agent identifier
   * @param {object} estimate - Estimated cost/tokens
   * @returns {object} Budget check result
   */
  checkBudget(agentId, estimate = {}) {
    const startTime = Date.now();

    // Initialize if not exists
    if (!this.budgets.agents[agentId]) {
      this.initBudget(agentId);
    }

    const budget = this.budgets.agents[agentId];
    const { estimatedTokens = 1000, estimatedCost = 0.01 } = estimate;

    // Check global budget
    if (Date.now() > new Date(this.budgets.globalBudget.resetAt).getTime()) {
      // Reset daily budget
      this.budgets.globalBudget.tokensUsed = 0;
      this.budgets.globalBudget.resetAt = this.getNextResetTime();
    }

    const globalRemaining = this.budgets.globalBudget.tokensPerDay -
                           this.budgets.globalBudget.tokensUsed;

    if (globalRemaining < estimatedTokens) {
      return {
        allowed: false,
        reason: 'Global daily budget exceeded',
        agentId,
        estimate,
        remaining: {
          global: globalRemaining,
          agent: budget.limits.tokensPerDay - budget.usage.tokensUsed
        },
        checkTime: Date.now() - startTime
      };
    }

    // Check agent budget
    const agentRemaining = budget.limits.tokensPerDay - budget.usage.tokensUsed;

    if (agentRemaining < estimatedTokens) {
      return {
        allowed: false,
        reason: 'Agent daily budget exceeded',
        agentId,
        estimate,
        remaining: {
          global: globalRemaining,
          agent: agentRemaining
        },
        checkTime: Date.now() - startTime
      };
    }

    // Check per-operation cost limit
    if (estimatedCost > budget.limits.maxCostPerOperation) {
      return {
        allowed: false,
        reason: `Operation cost ${estimatedCost} exceeds limit ${budget.limits.maxCostPerOperation}`,
        agentId,
        estimate,
        remaining: {
          global: globalRemaining,
          agent: agentRemaining
        },
        checkTime: Date.now() - startTime
      };
    }

    return {
      allowed: true,
      reason: 'Within budget',
      agentId,
      estimate,
      remaining: {
        global: globalRemaining,
        agent: agentRemaining
      },
      checkTime: Date.now() - startTime
    };
  }

  /**
   * Deduct tokens/cost after operation
   * @param {string} agentId - Agent identifier
   * @param {object} actual - Actual usage
   */
  deduct(agentId, actual = {}) {
    const startTime = Date.now();

    if (!this.budgets.agents[agentId]) {
      return { success: false, reason: 'Agent budget not initialized' };
    }

    const { tokensUsed = 0, cost = 0 } = actual;

    // Update agent budget
    this.budgets.agents[agentId].usage.tokensUsed += tokensUsed;
    this.budgets.agents[agentId].usage.operationCount += 1;
    this.budgets.agents[agentId].usage.totalCost += cost;

    // Update global budget
    this.budgets.globalBudget.tokensUsed += tokensUsed;

    this.saveBudgets();

    return {
      success: true,
      agentId,
      deducted: { tokensUsed, cost },
      remaining: {
        global: this.budgets.globalBudget.tokensPerDay - this.budgets.globalBudget.tokensUsed,
        agent: this.budgets.agents[agentId].limits.tokensPerDay -
               this.budgets.agents[agentId].usage.tokensUsed
      },
      deductTime: Date.now() - startTime
    };
  }

  /**
   * Get budget status
   * @param {string} agentId - Agent identifier
   */
  getStatus(agentId) {
    if (!this.budgets.agents[agentId]) {
      return { error: 'Agent budget not initialized' };
    }

    const budget = this.budgets.agents[agentId];
    return {
      agentId,
      limits: budget.limits,
      usage: budget.usage,
      remaining: {
        tokens: budget.limits.tokensPerDay - budget.usage.tokensUsed,
        percentage: ((budget.limits.tokensPerDay - budget.usage.tokensUsed) /
                    budget.limits.tokensPerDay * 100).toFixed(2)
      }
    };
  }

  /**
   * Reset agent budget
   * @param {string} agentId - Agent identifier
   */
  reset(agentId) {
    if (!this.budgets.agents[agentId]) {
      return { success: false, reason: 'Agent budget not initialized' };
    }

    this.budgets.agents[agentId].usage = {
      tokensUsed: 0,
      operationCount: 0,
      totalCost: 0,
      lastReset: new Date().toISOString()
    };

    this.saveBudgets();
    return { success: true, agentId };
  }
}

module.exports = new BudgetTracker();
