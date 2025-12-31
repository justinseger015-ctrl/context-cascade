/**
 * RBAC Enforcement Layer
 * Phase 1.1 Security Hardening
 *
 * This module provides ACTUAL enforcement of RBAC rules, not just semantic definitions.
 * It intercepts tool calls and validates permissions before execution.
 *
 * @module security/rbac/enforcer
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Load RBAC rules from JSON
const RBAC_RULES_PATH = path.join(__dirname, '../../agents/identity/agent-rbac-rules.json');
let RBAC_RULES = null;

/**
 * Load RBAC rules from disk (cached)
 */
function loadRBACRules() {
  if (RBAC_RULES === null) {
    try {
      const content = fs.readFileSync(RBAC_RULES_PATH, 'utf8');
      RBAC_RULES = JSON.parse(content);
    } catch (err) {
      console.error(`RBAC: Failed to load rules from ${RBAC_RULES_PATH}:`, err.message);
      // Fail closed - deny all if rules can't be loaded
      RBAC_RULES = { roles: {}, permission_matrix: { tools: {}, api_access: {}, path_access: {} } };
    }
  }
  return RBAC_RULES;
}

/**
 * Agent identity registry - maps agent IDs to their roles
 * In production, this would be loaded from a secure store
 */
const AGENT_REGISTRY = new Map();

/**
 * Register an agent with a role and token
 * @param {string} agentId - Unique agent identifier
 * @param {string} role - RBAC role name
 * @param {string} token - Authentication token
 */
function registerAgent(agentId, role, token) {
  const rules = loadRBACRules();

  if (!rules.roles[role]) {
    throw new Error(`RBAC: Invalid role '${role}' for agent ${agentId}`);
  }

  // Hash the token for storage
  const tokenHash = crypto.createHash('sha256').update(token).digest('hex');

  AGENT_REGISTRY.set(agentId, {
    role,
    tokenHash,
    registeredAt: new Date().toISOString(),
    permissions: rules.roles[role].permissions
  });

  return true;
}

/**
 * Validate agent token
 * @param {string} agentId - Agent identifier
 * @param {string} token - Token to validate
 * @returns {boolean} True if token is valid
 */
function validateToken(agentId, token) {
  const agent = AGENT_REGISTRY.get(agentId);
  if (!agent) {
    return false;
  }

  const tokenHash = crypto.createHash('sha256').update(token).digest('hex');
  return agent.tokenHash === tokenHash;
}

/**
 * Get agent's role
 * @param {string} agentId - Agent identifier
 * @returns {string|null} Role name or null if not found
 */
function getAgentRole(agentId) {
  const agent = AGENT_REGISTRY.get(agentId);
  return agent ? agent.role : null;
}

/**
 * Check if a path matches any of the allowed patterns
 * @param {string} targetPath - Path to check
 * @param {string[]} allowedPatterns - Array of glob patterns
 * @returns {boolean} True if path matches any pattern
 */
function matchPath(targetPath, allowedPatterns) {
  if (!targetPath || !allowedPatterns) return false;

  // Normalize path separators
  const normalizedPath = targetPath.replace(/\\/g, '/');

  for (const pattern of allowedPatterns) {
    if (pattern === '**') return true;

    // Convert glob pattern to regex
    const regexPattern = pattern
      .replace(/\*\*/g, '<<GLOBSTAR>>')
      .replace(/\*/g, '[^/]*')
      .replace(/<<GLOBSTAR>>/g, '.*')
      .replace(/\//g, '\\/');

    const regex = new RegExp(`^${regexPattern}$`);
    if (regex.test(normalizedPath)) {
      return true;
    }
  }

  return false;
}

/**
 * RBAC Enforcement Result
 * @typedef {Object} RBACResult
 * @property {boolean} allowed - Whether the action is allowed
 * @property {string} reason - Explanation for the decision
 * @property {string} [requiredApproval] - If approval is needed, who can approve
 */

/**
 * Enforce RBAC for a tool call
 * @param {string} agentId - Agent making the request
 * @param {string} token - Agent's authentication token
 * @param {string} toolName - Name of the tool being called
 * @param {Object} params - Tool parameters (for path checking)
 * @returns {RBACResult} Enforcement result
 */
function enforceRBAC(agentId, token, toolName, params = {}) {
  const rules = loadRBACRules();

  // Step 1: Validate agent identity
  if (!validateToken(agentId, token)) {
    return {
      allowed: false,
      reason: `RBAC_DENIED: Invalid or missing token for agent '${agentId}'`
    };
  }

  // Step 2: Get agent's role and permissions
  const role = getAgentRole(agentId);
  const roleConfig = rules.roles[role];

  if (!roleConfig) {
    return {
      allowed: false,
      reason: `RBAC_DENIED: Unknown role '${role}' for agent '${agentId}'`
    };
  }

  const permissions = roleConfig.permissions;

  // Step 3: Check tool permission
  const allowedTools = permissions.tools || [];
  if (!allowedTools.includes(toolName) && !allowedTools.includes('*')) {
    return {
      allowed: false,
      reason: `RBAC_DENIED: Agent '${agentId}' (role: ${role}) cannot use tool '${toolName}'. Allowed tools: ${allowedTools.join(', ')}`
    };
  }

  // Step 4: Check path permission if applicable
  const targetPath = params.file_path || params.path || params.target;
  if (targetPath) {
    const allowedPaths = permissions.paths || [];
    if (!matchPath(targetPath, allowedPaths)) {
      return {
        allowed: false,
        reason: `RBAC_DENIED: Agent '${agentId}' (role: ${role}) cannot access path '${targetPath}'. Allowed paths: ${allowedPaths.join(', ')}`
      };
    }
  }

  // Step 5: Check if approval is required
  const requiresApproval = permissions.requires_approval_for || [];
  if (requiresApproval.includes(toolName)) {
    return {
      allowed: false,
      reason: `RBAC_APPROVAL_REQUIRED: Tool '${toolName}' requires approval`,
      requiredApproval: 'human or admin'
    };
  }

  // Step 6: Check budget limits
  const budget = roleConfig.budget || {};
  // Budget checking would integrate with a token counter service
  // For now, we just note the limits

  return {
    allowed: true,
    reason: `RBAC_ALLOWED: Agent '${agentId}' (role: ${role}) authorized for '${toolName}'`,
    budget: {
      maxTokensPerSession: budget.max_tokens_per_session,
      maxCostPerDay: budget.max_cost_per_day
    }
  };
}

/**
 * Create a middleware function for tool enforcement
 * @param {Function} toolHandler - Original tool handler
 * @returns {Function} Wrapped handler with RBAC enforcement
 */
function createRBACMiddleware(toolHandler) {
  return async function rbacEnforcedHandler(params, context = {}) {
    const agentId = context.agentId || process.env.AGENT_ID || 'unknown';
    const token = context.token || process.env.AGENT_TOKEN || '';
    const toolName = context.toolName || 'unknown';

    const result = enforceRBAC(agentId, token, toolName, params);

    if (!result.allowed) {
      // Log the denial
      console.error(`[RBAC] ${result.reason}`);

      // Return error instead of executing
      return {
        error: true,
        code: 'RBAC_DENIED',
        message: result.reason,
        requiredApproval: result.requiredApproval
      };
    }

    // Log the approval
    console.log(`[RBAC] ${result.reason}`);

    // Execute the original handler
    return toolHandler(params, context);
  };
}

/**
 * Audit log entry
 * @param {string} agentId - Agent identifier
 * @param {string} action - Action attempted
 * @param {boolean} allowed - Whether it was allowed
 * @param {string} reason - Explanation
 */
function auditLog(agentId, action, allowed, reason) {
  const entry = {
    timestamp: new Date().toISOString(),
    agentId,
    action,
    allowed,
    reason
  };

  const logPath = path.join(__dirname, '../../logs/rbac-audit.jsonl');

  try {
    // Ensure log directory exists
    const logDir = path.dirname(logPath);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }

    fs.appendFileSync(logPath, JSON.stringify(entry) + '\n');
  } catch (err) {
    console.error('[RBAC] Failed to write audit log:', err.message);
  }
}

// Export functions
module.exports = {
  loadRBACRules,
  registerAgent,
  validateToken,
  getAgentRole,
  enforceRBAC,
  createRBACMiddleware,
  matchPath,
  auditLog,
  AGENT_REGISTRY
};
