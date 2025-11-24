# Integration Guide for Security Manager

## Overview

The Budget Tracker module is **production ready** and waiting for integration with your RBAC components. This guide shows exactly how to integrate budget tracking into your permission checker.

## Your Components (To Implement)

### 1. identity.js

**What it should do:**
- Agent registration with unique IDs
- Role assignment and verification
- Session management
- Identity verification

**Example API:**
```javascript
// identity.js
module.exports = {
  async registerAgent(agentId, role, metadata) {
    // Store agent identity
    // Return agent record
  },

  async getAgent(agentId) {
    // Return: { agent_id, role, permissions, session_id, ... }
  },

  async verifyAgent(agentId) {
    // Return: { valid: true/false, reason: ... }
  },

  async createSession(agentId) {
    // Create new session
    // Return session_id
  }
};
```

## Integration Pattern

### Step 1: Initialize Budget on Agent Registration

When you register an agent in identity.js, also initialize their budget:

```javascript
// identity.js
const budgetTracker = require('./budget-tracker');

async function registerAgent(agentId, role, metadata) {
  // Your identity registration logic
  const agent = await createAgentRecord(agentId, role);

  // Initialize budget based on role
  const roleBudgets = {
    'backend-dev': { session: 100000, daily: 10.00 },
    'coder': { session: 80000, daily: 8.00 },
    'tester': { session: 60000, daily: 6.00 },
    'reviewer': { session: 40000, daily: 4.00 },
    'researcher': { session: 120000, daily: 15.00 }
  };

  const budget = roleBudgets[role] || { session: 50000, daily: 5.00 };

  budgetTracker.initializeBudget(
    agentId,
    role,
    budget.session,
    budget.daily
  );

  return agent;
}
```

### Step 2: Integrate into Permission Checker

```javascript
// permission-checker.js
const budgetTracker = require('./budget-tracker');
const identity = require('./identity');

/**
 * Check if agent has permission to perform operation
 */
async function checkPermission(agentId, operation, context = {}) {
  const startTime = Date.now();

  // STEP 1: Verify agent identity
  const agent = await identity.getAgent(agentId);
  if (!agent) {
    return {
      allowed: false,
      reason: 'Agent not found',
      error_code: 'AGENT_NOT_FOUND'
    };
  }

  // STEP 2: Check RBAC permissions (YOUR LOGIC)
  const rbacCheck = await checkRBAC(agent.role, operation, context);
  if (!rbacCheck.allowed) {
    return {
      allowed: false,
      reason: rbacCheck.reason,
      error_code: 'RBAC_DENIED'
    };
  }

  // STEP 3: Check budget (ALREADY IMPLEMENTED)
  const estimatedTokens = context.estimatedTokens || estimateTokensForOperation(operation);
  const budgetCheck = budgetTracker.checkBudget(agentId, estimatedTokens);

  if (!budgetCheck.allowed) {
    // Budget exceeded - increment blocked counter
    return {
      allowed: false,
      reason: budgetCheck.reason,
      error_code: 'BUDGET_EXCEEDED',
      budget_status: budgetTracker.getBudgetStatus(agentId)
    };
  }

  // STEP 4: All checks passed
  const checkDuration = Date.now() - startTime;

  return {
    allowed: true,
    reason: null,
    check_duration_ms: checkDuration
  };
}

/**
 * Record operation completion and deduct budget
 */
async function recordOperation(agentId, operation, usage, result = 'success') {
  const { inputTokens = 0, outputTokens = 0 } = usage;

  // STEP 1: Deduct from budget (ALREADY IMPLEMENTED)
  const budgetStatus = budgetTracker.deductBudget(agentId, inputTokens, outputTokens);

  // STEP 2: Log to audit trail (YOUR LOGIC)
  await auditLog.record({
    agent_id: agentId,
    operation: operation,
    result: result,
    input_tokens: inputTokens,
    output_tokens: outputTokens,
    total_tokens: inputTokens + outputTokens,
    cost: budgetStatus.daily.cost_used,
    session_utilization: budgetStatus.session.utilization_pct,
    daily_utilization: budgetStatus.daily.utilization_pct,
    timestamp: Date.now()
  });

  return {
    success: true,
    budget_status: budgetStatus
  };
}

/**
 * YOUR RBAC LOGIC
 */
async function checkRBAC(role, operation, context) {
  // Example RBAC matrix
  const permissions = {
    'backend-dev': ['read_file', 'write_file', 'run_tests', 'deploy'],
    'coder': ['read_file', 'write_file', 'run_tests'],
    'tester': ['read_file', 'run_tests'],
    'reviewer': ['read_file']
  };

  const allowedOps = permissions[role] || [];

  if (!allowedOps.includes(operation)) {
    return {
      allowed: false,
      reason: `Role ${role} not authorized for operation ${operation}`
    };
  }

  return { allowed: true, reason: null };
}

/**
 * Estimate tokens for operation (optional, can use fixed estimate)
 */
function estimateTokensForOperation(operation) {
  const estimates = {
    'read_file': 5000,
    'write_file': 3000,
    'run_tests': 8000,
    'deploy': 10000,
    'analyze_code': 15000
  };

  return estimates[operation] || 1000;
}

module.exports = {
  checkPermission,
  recordOperation,
  checkRBAC
};
```

### Step 3: Usage in Agent Execution

```javascript
// agent-executor.js (or wherever you execute agent operations)
const permissionChecker = require('./permission-checker');

async function executeAgentOperation(agentId, operation, context) {
  // STEP 1: Check permission (includes budget check)
  const permCheck = await permissionChecker.checkPermission(agentId, operation, context);

  if (!permCheck.allowed) {
    throw new Error(`Permission denied: ${permCheck.reason} (${permCheck.error_code})`);
  }

  // STEP 2: Execute operation
  const startTime = Date.now();
  let result, inputTokens, outputTokens;

  try {
    result = await performOperation(operation, context);
    inputTokens = result.inputTokens || 0;
    outputTokens = result.outputTokens || 0;
  } catch (error) {
    // Record failure (with estimated tokens)
    await permissionChecker.recordOperation(
      agentId,
      operation,
      { inputTokens: context.estimatedTokens || 1000, outputTokens: 0 },
      'failure'
    );
    throw error;
  }

  // STEP 3: Record success and deduct budget
  const recordResult = await permissionChecker.recordOperation(
    agentId,
    operation,
    { inputTokens, outputTokens },
    'success'
  );

  return {
    ...result,
    budget_status: recordResult.budget_status,
    execution_time_ms: Date.now() - startTime
  };
}
```

## Budget Configuration by Role

Recommended budget limits based on agent role:

```javascript
const ROLE_BUDGETS = {
  // High-usage agents
  'researcher': {
    session_token_limit: 200000,  // 200k tokens
    daily_cost_limit: 20.00       // $20/day
  },
  'ml-developer': {
    session_token_limit: 150000,
    daily_cost_limit: 15.00
  },

  // Medium-usage agents
  'backend-dev': {
    session_token_limit: 100000,
    daily_cost_limit: 10.00
  },
  'coder': {
    session_token_limit: 80000,
    daily_cost_limit: 8.00
  },
  'system-architect': {
    session_token_limit: 100000,
    daily_cost_limit: 10.00
  },

  // Lower-usage agents
  'tester': {
    session_token_limit: 60000,
    daily_cost_limit: 6.00
  },
  'reviewer': {
    session_token_limit: 40000,
    daily_cost_limit: 4.00
  },
  'code-analyzer': {
    session_token_limit: 50000,
    daily_cost_limit: 5.00
  },

  // Default for unknown roles
  'default': {
    session_token_limit: 50000,
    daily_cost_limit: 5.00
  }
};
```

## Error Handling

```javascript
// In your permission-checker.js
async function executeWithBudgetProtection(agentId, operation, context) {
  try {
    // Check permission
    const check = await checkPermission(agentId, operation, context);

    if (!check.allowed) {
      if (check.error_code === 'BUDGET_EXCEEDED') {
        // Special handling for budget exceeded
        const status = check.budget_status;

        if (status.is_session_exhausted) {
          return {
            error: 'SESSION_BUDGET_EXCEEDED',
            message: `Session token limit reached. Used: ${status.session.tokens_used}/${status.session.tokens_limit}`,
            suggestion: 'Start a new session or increase session limit'
          };
        }

        if (status.is_daily_exhausted) {
          return {
            error: 'DAILY_BUDGET_EXCEEDED',
            message: `Daily cost limit reached. Used: $${status.daily.cost_used.toFixed(2)}/$${status.daily.cost_limit.toFixed(2)}`,
            suggestion: 'Wait for daily reset at midnight UTC or increase daily limit'
          };
        }
      }

      // Other permission errors
      return {
        error: check.error_code,
        message: check.reason
      };
    }

    // Execute operation
    return await executeOperation(operation, context);

  } catch (error) {
    // Log error but don't expose budget details
    console.error('Operation failed:', error);
    throw error;
  }
}
```

## Session Management

```javascript
// When creating new agent session
async function startAgentSession(agentId) {
  // Create session in identity system
  const session = await identity.createSession(agentId);

  // Reset session budget
  budgetTracker.resetSession(agentId);

  return session;
}

// When ending agent session
async function endAgentSession(agentId, sessionId) {
  // Get final budget status
  const finalStatus = budgetTracker.getBudgetStatus(agentId);

  // Log session summary
  await sessionLog.record({
    agent_id: agentId,
    session_id: sessionId,
    tokens_used: finalStatus.session.tokens_used,
    cost_incurred: finalStatus.daily.cost_used,
    operations_blocked: finalStatus.operations_blocked,
    ended_at: Date.now()
  });

  // Close session in identity system
  await identity.endSession(sessionId);

  return finalStatus;
}
```

## Testing Integration

```javascript
// test-integration.js
const budgetTracker = require('./budget-tracker');
const permissionChecker = require('./permission-checker');

async function testIntegration() {
  console.log('Testing RBAC + Budget Integration...\n');

  // Setup
  const agentId = 'test-agent-001';
  const role = 'backend-dev';

  // Register agent (your identity.js)
  // await identity.registerAgent(agentId, role);

  // Initialize budget
  budgetTracker.initializeBudget(agentId, role, 100000, 10.00);

  // Test 1: Allowed operation
  console.log('Test 1: Allowed operation');
  const check1 = await permissionChecker.checkPermission(agentId, 'read_file', {
    estimatedTokens: 5000
  });
  console.log('Result:', check1);

  if (check1.allowed) {
    await permissionChecker.recordOperation(agentId, 'read_file', {
      inputTokens: 4800,
      outputTokens: 15200
    });
  }

  // Test 2: Budget exceeded
  console.log('\nTest 2: Budget exceeded');
  const check2 = await permissionChecker.checkPermission(agentId, 'read_file', {
    estimatedTokens: 100000  // Would exceed budget
  });
  console.log('Result:', check2);

  // Test 3: RBAC denied
  console.log('\nTest 3: RBAC denied');
  const check3 = await permissionChecker.checkPermission(agentId, 'unauthorized_op', {
    estimatedTokens: 1000
  });
  console.log('Result:', check3);

  // Final status
  console.log('\nFinal Budget Status:');
  const status = budgetTracker.getBudgetStatus(agentId);
  console.log(status);
}

testIntegration().catch(console.error);
```

## Monitoring Dashboard

```javascript
// Get budget overview for all agents
function getBudgetDashboard() {
  const allAgents = identity.getAllAgents();

  return allAgents.map(agent => {
    const status = budgetTracker.getBudgetStatus(agent.agent_id);

    return {
      agent_id: agent.agent_id,
      role: agent.role,
      session_utilization: status.session.utilization_pct.toFixed(1) + '%',
      daily_utilization: status.daily.utilization_pct.toFixed(1) + '%',
      cost_used: '$' + status.daily.cost_used.toFixed(4),
      operations_blocked: status.operations_blocked,
      status: status.is_daily_exhausted ? 'BLOCKED' : 'ACTIVE'
    };
  });
}
```

## Key Integration Points

1. **Agent Registration** → Initialize budget
2. **Permission Check** → Check RBAC + budget
3. **Operation Execution** → Deduct budget
4. **Session Start** → Reset session budget
5. **Session End** → Log final status
6. **Daily Reset** → Automatic at midnight UTC
7. **Monitoring** → Budget dashboard

## Files You Need

- ✅ budget-tracker.js (READY)
- ⏳ identity.js (YOUR IMPLEMENTATION)
- ⏳ permission-checker.js (YOUR IMPLEMENTATION + BUDGET INTEGRATION)

## Support

The budget tracker is production ready. Integration points are clearly marked with comments. All functions are documented with JSDoc.

For questions:
1. Check budget-tracker.js source code (fully commented)
2. Review integration-example.js for usage patterns
3. Run verify-budget-tracker.js to validate functionality

**Backend Developer**
Ready for Security Manager integration
