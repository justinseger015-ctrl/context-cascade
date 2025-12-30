/**
 * Example Usage: Identity & RBAC Pipeline v3.0
 * Demonstrates complete workflow for securing agent operations
 *
 * v3.0: Uses x- prefixed custom fields for Anthropic compliance
 */

const pipeline = require('./identity-rbac-pipeline');
const identity = require('./identity');
const permissionChecker = require('./permission-checker');
const budgetTracker = require('./budget-tracker');

async function demonstrateSecurityPipeline() {
  console.log('='.repeat(60));
  console.log('Identity & RBAC Pipeline - Example Usage (v3.0)');
  console.log('='.repeat(60));
  console.log();

  // Step 1: Register agents with identities (v3.0 x- prefixed fields)
  console.log('Step 1: Registering Agents (v3.0 format)');
  console.log('-'.repeat(60));

  // v3.0: Custom metadata fields use x- prefix
  identity.register('coder-001', 'public-key-coder', {
    'x-category': 'development',
    'x-team': 'backend'
  });

  identity.register('reviewer-001', 'public-key-reviewer', {
    'x-category': 'quality-assurance',
    'x-team': 'qa'
  });

  console.log('Registered agents:');
  identity.listAgents().forEach(agent => {
    // v3.0: Access x-prefixed field
    console.log(`  - ${agent.agentId} (${agent.metadata['x-category'] || agent.metadata.category})`);
  });
  console.log();

  // Step 2: Assign roles
  console.log('Step 2: Assigning RBAC Roles');
  console.log('-'.repeat(60));

  permissionChecker.assignRole('coder-001', 'developer');
  permissionChecker.assignRole('reviewer-001', 'reviewer');

  console.log('Role assignments:');
  console.log(`  - coder-001: developer`);
  console.log(`  - reviewer-001: reviewer`);
  console.log();

  // Step 3: Initialize budgets
  console.log('Step 3: Initializing Budgets');
  console.log('-'.repeat(60));

  budgetTracker.initBudget('coder-001', {
    tokensPerDay: 500000,
    maxCostPerOperation: 0.1
  });

  budgetTracker.initBudget('reviewer-001', {
    tokensPerDay: 100000, // Lower budget for read-only
    maxCostPerOperation: 0.05
  });

  console.log('Budget initialized:');
  console.log(`  - coder-001: 500,000 tokens/day`);
  console.log(`  - reviewer-001: 100,000 tokens/day`);
  console.log();

  // Step 4: Authorized Operation (Developer writes code)
  console.log('Step 4: Authorized Operation');
  console.log('-'.repeat(60));
  console.log('Agent: coder-001');
  console.log('Operation: Edit file src/app.js');
  console.log();

  const result1 = await pipeline.enforceRBAC('coder-001', 'Edit', {
    filePath: 'src/app.js',
    fileSize: 5000
  });

  if (result1.allowed) {
    console.log('ALLOWED');
    console.log('Reasons:', result1.reasons.join('\n        '));
    console.log('Budget Remaining:', result1.budgetRemaining);
    console.log('Execution Time:', result1.metadata.executionTime + 'ms');

    // Simulate operation completion
    await pipeline.executePostHooks('coder-001', 'Edit', {
      filePath: 'src/app.js'
    }, {
      success: true,
      executionTime: 50
    });

    console.log('Post-hooks completed (audit logged, budget deducted)');
  } else {
    console.log('DENIED');
    console.log('Blocked by:', result1.blockedBy);
    console.log('Reason:', result1.reasons.join(', '));
  }
  console.log();

  // Step 5: Unauthorized Operation (Reviewer tries to write)
  console.log('Step 5: Unauthorized Operation');
  console.log('-'.repeat(60));
  console.log('Agent: reviewer-001');
  console.log('Operation: Write file src/config.js');
  console.log();

  const result2 = await pipeline.enforceRBAC('reviewer-001', 'Write', {
    filePath: 'src/config.js'
  });

  if (result2.allowed) {
    console.log('ALLOWED');
  } else {
    console.log('DENIED');
    console.log('Blocked by:', result2.blockedBy);
    console.log('Reason:', result2.reasons.join('\n        '));
  }
  console.log();

  // Step 6: Over-Budget Operation
  console.log('Step 6: Over-Budget Operation');
  console.log('-'.repeat(60));

  // Exhaust reviewer budget
  budgetTracker.deduct('reviewer-001', { tokensUsed: 95000, cost: 0.19 });

  const reviewerStatus = budgetTracker.getStatus('reviewer-001');
  console.log('Reviewer budget status:');
  console.log(`  - Used: ${reviewerStatus.usage.tokensUsed} tokens`);
  console.log(`  - Remaining: ${reviewerStatus.remaining.tokens} tokens (${reviewerStatus.remaining.percentage}%)`);
  console.log();

  console.log('Agent: reviewer-001');
  console.log('Operation: Read large file (10,000 tokens)');
  console.log();

  const result3 = await pipeline.enforceRBAC('reviewer-001', 'Read', {
    filePath: 'src/large-file.js',
    fileSize: 100000 // Large file
  });

  if (result3.allowed) {
    console.log('ALLOWED');
  } else {
    console.log('DENIED');
    console.log('Blocked by:', result3.blockedBy);
    console.log('Reason:', result3.reasons.join('\n        '));
    console.log('Budget Remaining:', result3.budgetRemaining);
  }
  console.log();

  // Step 7: High-Risk Operation
  console.log('Step 7: High-Risk Operation');
  console.log('-'.repeat(60));
  console.log('Agent: coder-001');
  console.log('Operation: Execute shell command (rm -rf test/)');
  console.log();

  process.env.AUTO_APPROVE_HIGH_RISK = 'true'; // Dev mode

  const result4 = await pipeline.enforceRBAC('coder-001', 'Bash', {
    command: 'rm -rf test/'
  });

  if (result4.allowed) {
    console.log('ALLOWED (auto-approved in dev mode)');
    console.log('WARNING:', result4.reasons.find(r => r.includes('WARNING')) || 'High-risk operation');
  } else {
    console.log('DENIED (requires human approval)');
  }
  console.log();

  // Step 8: Statistics
  console.log('Step 8: Pipeline Statistics');
  console.log('-'.repeat(60));

  const stats = pipeline.getStats();
  console.log('Total Executions:', stats.totalExecutions);
  console.log('Successful:', stats.successfulExecutions);
  console.log('Blocked:', stats.blockedExecutions);
  console.log('Success Rate:', stats.successRate);
  console.log('Average Execution Time:', stats.averageExecutionTime.toFixed(2) + 'ms');
  console.log();

  console.log('Per-Hook Statistics:');
  Object.entries(stats.hookStats).forEach(([hook, hookStats]) => {
    console.log(`  ${hook}:`);
    console.log(`    - Executions: ${hookStats.executions}`);
    console.log(`    - Success Rate: ${(hookStats.successes / hookStats.executions * 100).toFixed(1)}%`);
    console.log(`    - Avg Time: ${hookStats.averageTime.toFixed(2)}ms`);
  });
  console.log();

  console.log('='.repeat(60));
  console.log('Demo Complete!');
  console.log('='.repeat(60));
}

// Run demo
if (require.main === module) {
  demonstrateSecurityPipeline().catch(error => {
    console.error('Demo failed:', error);
    process.exit(1);
  });
}

module.exports = { demonstrateSecurityPipeline };
