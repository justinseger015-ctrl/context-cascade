/**
 * RBAC Engine Usage Examples
 *
 * Demonstrates how to use the Identity Verification and Permission Checker
 * systems in real-world scenarios.
 *
 * @module hooks/12fa/utils/example-usage
 */

const { loadAgentIdentityByName, validateAgentIdentity, generateJWT, validateJWT } = require('./identity');
const { checkPermission, checkBudgetThreshold, validateRBACRules } = require('./permission-checker');

console.log('========================================');
console.log('RBAC Engine Usage Examples');
console.log('========================================\n');

// Example 1: Validate RBAC Rules
console.log('[Example 1] Validate RBAC Rules');
console.log('--------------------------------');
const rulesValidation = validateRBACRules();
if (rulesValidation.valid) {
  console.log('Success: RBAC rules are valid');
  console.log('  10 roles defined with complete permissions\n');
} else {
  console.error('Error: RBAC rules validation failed');
  rulesValidation.errors.forEach(err => console.error(`  - ${err}`));
}

// Example 2: Load and Validate Agent Identity
console.log('[Example 2] Load Agent Identity');
console.log('--------------------------------');
const agentIdentity = loadAgentIdentityByName('system-architect');

if (agentIdentity) {
  console.log(`Loaded agent: ${agentIdentity.name}`);
  console.log(`  Agent ID: ${agentIdentity.agent_id}`);
  console.log(`  Role: ${agentIdentity.role}`);

  const validation = validateAgentIdentity(agentIdentity);
  if (validation.valid) {
    console.log('  Status: Valid identity\n');
  } else {
    console.error('  Errors:', validation.errors);
  }
} else {
  console.log('Agent not found (this is expected if file structure differs)\n');
}

// Example 3: Generate and Validate JWT Token
console.log('[Example 3] JWT Authentication');
console.log('-------------------------------');
const testIdentity = {
  agent_id: '550e8400-e29b-41d4-a716-446655440000',
  name: 'backend-dev',
  role: 'developer'
};

const token = generateJWT(testIdentity, 3600); // 1 hour expiry
console.log(`Generated JWT token (first 50 chars): ${token.substring(0, 50)}...`);

const payload = validateJWT(token);
if (payload) {
  console.log('Token validation: Success');
  console.log(`  Agent: ${payload.name}`);
  console.log(`  Role: ${payload.role}`);
  console.log(`  Expires: ${new Date(payload.exp * 1000).toISOString()}\n`);
} else {
  console.error('Token validation: Failed\n');
}

// Example 4: Check Tool Permission
console.log('[Example 4] Check Tool Permission');
console.log('----------------------------------');
const toolCheck1 = checkPermission({
  role: 'developer',
  toolName: 'Read'
});
console.log(`Developer can use Read: ${toolCheck1.allowed}`);
console.log(`  Reason: ${toolCheck1.reason}`);

const toolCheck2 = checkPermission({
  role: 'analyst',
  toolName: 'Write'
});
console.log(`Analyst can use Write: ${toolCheck2.allowed}`);
console.log(`  Reason: ${toolCheck2.reason}\n`);

// Example 5: Check Path Permission
console.log('[Example 5] Check Path Permission');
console.log('----------------------------------');
const pathCheck1 = checkPermission({
  role: 'developer',
  toolName: 'Write',
  filePath: 'src/api/users.js'
});
console.log(`Developer can write to src/api/users.js: ${pathCheck1.allowed}`);
console.log(`  Reason: ${pathCheck1.reason}`);

const pathCheck2 = checkPermission({
  role: 'frontend',
  toolName: 'Write',
  filePath: 'backend/api/users.js'
});
console.log(`Frontend can write to backend/api/users.js: ${pathCheck2.allowed}`);
console.log(`  Reason: ${pathCheck2.reason}\n`);

// Example 6: Check API Permission
console.log('[Example 6] Check API Permission');
console.log('---------------------------------');
const apiCheck1 = checkPermission({
  role: 'developer',
  toolName: 'Read',
  apiName: 'github'
});
console.log(`Developer can access GitHub API: ${apiCheck1.allowed}`);
console.log(`  Reason: ${apiCheck1.reason}`);

const apiCheck2 = checkPermission({
  role: 'frontend',
  toolName: 'Read',
  apiName: 'flow-nexus'
});
console.log(`Frontend can access Flow-Nexus API: ${apiCheck2.allowed}`);
console.log(`  Reason: ${apiCheck2.reason}\n`);

// Example 7: Comprehensive Permission Check with Budget
console.log('[Example 7] Comprehensive Permission Check');
console.log('-------------------------------------------');
const fullCheck = checkPermission({
  role: 'developer',
  toolName: 'Write',
  filePath: 'src/api/users.js',
  apiName: 'github',
  estimatedTokens: 5000
});

if (fullCheck.allowed) {
  console.log('Permission: Granted');
  console.log(`  Budget impact: $${fullCheck.budgetImpact.toFixed(4)}`);
  console.log(`  Requires approval: ${fullCheck.requiresApproval}`);
  console.log(`  Check time: ${fullCheck.checkTimeMs}ms\n`);
} else {
  console.log('Permission: Denied');
  console.log(`  Reason: ${fullCheck.reason}\n`);
}

// Example 8: Budget Threshold Check
console.log('[Example 8] Budget Threshold Check');
console.log('-----------------------------------');
const budgetCheck1 = checkBudgetThreshold('developer', 15.0);
console.log('Developer daily budget check:');
console.log(`  Current spend: $15.00`);
console.log(`  Threshold: $${budgetCheck1.threshold.toFixed(2)}`);
console.log(`  Remaining: $${budgetCheck1.remaining.toFixed(2)}`);
console.log(`  Exceeded: ${budgetCheck1.exceeded}`);

const budgetCheck2 = checkBudgetThreshold('developer', 35.0);
console.log('\nDeveloper daily budget check (over budget):');
console.log(`  Current spend: $35.00`);
console.log(`  Threshold: $${budgetCheck2.threshold.toFixed(2)}`);
console.log(`  Remaining: $${budgetCheck2.remaining.toFixed(2)}`);
console.log(`  Exceeded: ${budgetCheck2.exceeded}\n`);

// Example 9: High-Risk Operation Requiring Approval
console.log('[Example 9] High-Risk Operation');
console.log('--------------------------------');
const adminCheck = checkPermission({
  role: 'admin',
  toolName: 'KillShell',
  estimatedTokens: 1000
});

if (adminCheck.allowed) {
  console.log('Permission: Granted (with conditions)');
  console.log(`  Requires approval: ${adminCheck.requiresApproval}`);
  console.log(`  Approvers: ${adminCheck.approvers.join(', ')}`);
  console.log('  Action: Request human approval before proceeding\n');
}

// Example 10: Performance Benchmark
console.log('[Example 10] Performance Benchmark');
console.log('-----------------------------------');
const iterations = 1000;
const startTime = Date.now();

for (let i = 0; i < iterations; i++) {
  checkPermission({
    role: 'developer',
    toolName: 'Read',
    filePath: 'src/api/users.js',
    apiName: 'github',
    estimatedTokens: 1000
  });
}

const totalTime = Date.now() - startTime;
const avgTime = totalTime / iterations;

console.log(`Performed ${iterations} permission checks`);
console.log(`  Total time: ${totalTime}ms`);
console.log(`  Average time: ${avgTime.toFixed(2)}ms`);
console.log(`  Target: <50ms per check`);
console.log(`  Status: ${avgTime < 50 ? 'PASS' : 'FAIL'}\n`);

console.log('========================================');
console.log('Examples Complete');
console.log('========================================\n');
