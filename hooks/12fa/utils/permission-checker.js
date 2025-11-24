/**
 * Permission Checker for Agent RBAC Enforcement
 *
 * Enforces Role-Based Access Control across 3 dimensions:
 * 1. Tool Whitelist - Does agent's role allow this tool?
 * 2. Path Scopes - Is file path within agent's allowed paths?
 * 3. API Access - Does role permit this MCP call?
 *
 * Features:
 * - Loads RBAC rules from agents/identity/agent-rbac-rules.json
 * - Checks tool permissions, path scopes, and API access
 * - Returns budget impact for cost tracking
 * - Performance: <50ms per check (cached)
 * - Windows compatible (no Unicode)
 *
 * @module hooks/12fa/utils/permission-checker
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const minimatch = require('minimatch');

// Cache for RBAC rules
let rbacRulesCache = null;
let rbacRulesCacheTime = 0;
const RBAC_CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

/**
 * Load RBAC rules from JSON file
 * @param {string} rulesPath - Path to agent-rbac-rules.json (default: auto-detect)
 * @returns {Object} RBAC rules object
 */
function loadRBACRules(rulesPath = null) {
  // Check cache first
  const now = Date.now();
  if (rbacRulesCache && (now - rbacRulesCacheTime) < RBAC_CACHE_TTL_MS) {
    return rbacRulesCache;
  }

  // Auto-detect rules path
  if (!rulesPath) {
    rulesPath = path.join(__dirname, '..', '..', '..', 'agents', 'identity', 'agent-rbac-rules.json');
  }

  try {
    const rulesContent = fs.readFileSync(rulesPath, 'utf8');
    rbacRulesCache = JSON.parse(rulesContent);
    rbacRulesCacheTime = now;
    return rbacRulesCache;
  } catch (error) {
    console.error(`Error loading RBAC rules from ${rulesPath}:`, error.message);
    throw new Error('Failed to load RBAC rules');
  }
}

/**
 * Check if agent's role allows a specific tool
 * @param {string} role - Agent's RBAC role
 * @param {string} toolName - Tool name (e.g., "Read", "Write", "Bash")
 * @returns {Object} {allowed: boolean, reason: string}
 */
function checkToolPermission(role, toolName) {
  const rules = loadRBACRules();

  if (!rules.roles[role]) {
    return {
      allowed: false,
      reason: `Unknown role: ${role}`
    };
  }

  const rolePermissions = rules.roles[role].permissions;

  // Check for wildcard permission
  if (rolePermissions.tools.includes('*')) {
    return {
      allowed: true,
      reason: 'Role has wildcard tool access'
    };
  }

  // Check if tool is in allowed list
  if (rolePermissions.tools.includes(toolName)) {
    return {
      allowed: true,
      reason: `Tool ${toolName} is in role's allowed tools`
    };
  }

  // Check permission matrix as fallback
  if (rules.permission_matrix && rules.permission_matrix.tools) {
    const allowedRoles = rules.permission_matrix.tools[toolName];
    if (allowedRoles && allowedRoles.includes(role)) {
      return {
        allowed: true,
        reason: `Tool ${toolName} allowed via permission matrix`
      };
    }
  }

  return {
    allowed: false,
    reason: `Tool ${toolName} not in role's allowed tools`
  };
}

/**
 * Check if file path is within agent's allowed path scopes
 * @param {string} role - Agent's RBAC role
 * @param {string} filePath - File path to check
 * @returns {Object} {allowed: boolean, reason: string}
 */
function checkPathPermission(role, filePath) {
  const rules = loadRBACRules();

  if (!rules.roles[role]) {
    return {
      allowed: false,
      reason: `Unknown role: ${role}`
    };
  }

  const rolePermissions = rules.roles[role].permissions;

  // Check for wildcard path access
  if (rolePermissions.paths.includes('**')) {
    return {
      allowed: true,
      reason: 'Role has wildcard path access'
    };
  }

  // Normalize path (convert Windows paths to forward slashes)
  const normalizedPath = filePath.replace(/\\/g, '/');

  // Check if path matches any allowed pattern
  for (const pattern of rolePermissions.paths) {
    if (minimatch(normalizedPath, pattern)) {
      return {
        allowed: true,
        reason: `Path matches pattern: ${pattern}`
      };
    }
  }

  return {
    allowed: false,
    reason: `Path ${filePath} not in role's allowed scopes`
  };
}

/**
 * Check if agent's role allows API access
 * @param {string} role - Agent's RBAC role
 * @param {string} apiName - API name (e.g., "github", "memory-mcp")
 * @returns {Object} {allowed: boolean, reason: string}
 */
function checkAPIPermission(role, apiName) {
  const rules = loadRBACRules();

  if (!rules.roles[role]) {
    return {
      allowed: false,
      reason: `Unknown role: ${role}`
    };
  }

  const rolePermissions = rules.roles[role].permissions;

  // Check for wildcard API access
  if (rolePermissions.api_access.includes('*')) {
    return {
      allowed: true,
      reason: 'Role has wildcard API access'
    };
  }

  // Check if API is in allowed list
  if (rolePermissions.api_access.includes(apiName)) {
    return {
      allowed: true,
      reason: `API ${apiName} is in role's allowed APIs`
    };
  }

  // Check permission matrix as fallback
  if (rules.permission_matrix && rules.permission_matrix.api_access) {
    const allowedRoles = rules.permission_matrix.api_access[apiName];
    if (allowedRoles && allowedRoles.includes(role)) {
      return {
        allowed: true,
        reason: `API ${apiName} allowed via permission matrix`
      };
    }
  }

  return {
    allowed: false,
    reason: `API ${apiName} not in role's allowed APIs`
  };
}

/**
 * Check if operation requires approval
 * @param {string} role - Agent's RBAC role
 * @param {string} operation - Operation name (e.g., "production_deploy", "KillShell")
 * @returns {Object} {requiresApproval: boolean, approvers: string[]}
 */
function checkApprovalRequired(role, operation) {
  const rules = loadRBACRules();

  if (!rules.roles[role]) {
    return {
      requiresApproval: false,
      approvers: []
    };
  }

  const rolePermissions = rules.roles[role].permissions;

  // Check role-specific approval requirements
  if (rolePermissions.requires_approval_for && rolePermissions.requires_approval_for.includes(operation)) {
    // Look up approvers from escalation rules
    if (rules.escalation_rules && rules.escalation_rules.high_risk_operations) {
      const escalationRule = rules.escalation_rules.high_risk_operations.find(
        rule => rule.operation === operation
      );
      if (escalationRule) {
        return {
          requiresApproval: true,
          approvers: escalationRule.approvers
        };
      }
    }

    return {
      requiresApproval: true,
      approvers: ['human', 'admin']
    };
  }

  return {
    requiresApproval: false,
    approvers: []
  };
}

/**
 * Get budget impact for an operation
 * @param {string} role - Agent's RBAC role
 * @param {string} toolName - Tool being used
 * @param {number} estimatedTokens - Estimated tokens for operation (default: 1000)
 * @returns {number} Estimated cost impact in USD
 */
function getBudgetImpact(role, toolName, estimatedTokens = 1000) {
  // Token cost estimates (based on Claude Sonnet 3.5 pricing)
  const costPerMillionTokens = 3.0; // $3 per million tokens (avg input/output)
  const tokenCost = (estimatedTokens / 1000000) * costPerMillionTokens;

  // Tool-specific multipliers
  const toolMultipliers = {
    'Read': 0.5,
    'Write': 1.0,
    'Edit': 0.8,
    'MultiEdit': 1.5,
    'Bash': 1.2,
    'Grep': 0.3,
    'Glob': 0.3,
    'Task': 2.0,
    'TodoWrite': 0.5,
    'WebSearch': 1.5,
    'WebFetch': 1.0
  };

  const multiplier = toolMultipliers[toolName] || 1.0;

  return tokenCost * multiplier;
}

/**
 * Check if budget threshold is exceeded
 * @param {string} role - Agent's RBAC role
 * @param {number} currentDailyCost - Current daily cost spent
 * @returns {Object} {exceeded: boolean, threshold: number, remaining: number}
 */
function checkBudgetThreshold(role, currentDailyCost) {
  const rules = loadRBACRules();

  if (!rules.roles[role]) {
    return {
      exceeded: false,
      threshold: 0,
      remaining: 0
    };
  }

  const budget = rules.roles[role].budget;
  const maxCostPerDay = budget.max_cost_per_day;

  return {
    exceeded: currentDailyCost >= maxCostPerDay,
    threshold: maxCostPerDay,
    remaining: Math.max(0, maxCostPerDay - currentDailyCost)
  };
}

/**
 * Comprehensive permission check for an operation
 * @param {Object} params - Check parameters
 * @param {string} params.role - Agent's RBAC role
 * @param {string} params.toolName - Tool being used
 * @param {string} params.filePath - File path (optional)
 * @param {string} params.apiName - API name (optional)
 * @param {number} params.estimatedTokens - Estimated tokens (default: 1000)
 * @returns {Object} {allowed: boolean, reason: string, budgetImpact: number, requiresApproval: boolean}
 */
function checkPermission(params) {
  const {
    role,
    toolName,
    filePath = null,
    apiName = null,
    estimatedTokens = 1000
  } = params;

  const startTime = Date.now();

  try {
    // 1. Check tool permission
    const toolCheck = checkToolPermission(role, toolName);
    if (!toolCheck.allowed) {
      return {
        allowed: false,
        reason: toolCheck.reason,
        budgetImpact: 0,
        requiresApproval: false,
        checkTimeMs: Date.now() - startTime
      };
    }

    // 2. Check path permission (if file path provided)
    if (filePath) {
      const pathCheck = checkPathPermission(role, filePath);
      if (!pathCheck.allowed) {
        return {
          allowed: false,
          reason: pathCheck.reason,
          budgetImpact: 0,
          requiresApproval: false,
          checkTimeMs: Date.now() - startTime
        };
      }
    }

    // 3. Check API permission (if API name provided)
    if (apiName) {
      const apiCheck = checkAPIPermission(role, apiName);
      if (!apiCheck.allowed) {
        return {
          allowed: false,
          reason: apiCheck.reason,
          budgetImpact: 0,
          requiresApproval: false,
          checkTimeMs: Date.now() - startTime
        };
      }
    }

    // 4. Check if approval required
    const approvalCheck = checkApprovalRequired(role, toolName);

    // 5. Calculate budget impact
    const budgetImpact = getBudgetImpact(role, toolName, estimatedTokens);

    return {
      allowed: true,
      reason: 'All permission checks passed',
      budgetImpact,
      requiresApproval: approvalCheck.requiresApproval,
      approvers: approvalCheck.approvers,
      checkTimeMs: Date.now() - startTime
    };
  } catch (error) {
    console.error('Permission check error:', error.message);
    return {
      allowed: false,
      reason: `Permission check failed: ${error.message}`,
      budgetImpact: 0,
      requiresApproval: false,
      checkTimeMs: Date.now() - startTime
    };
  }
}

/**
 * Validate RBAC rules JSON structure
 * @param {string} rulesPath - Path to agent-rbac-rules.json (default: auto-detect)
 * @returns {Object} {valid: boolean, errors: string[]}
 */
function validateRBACRules(rulesPath = null) {
  const errors = [];

  try {
    const rules = loadRBACRules(rulesPath);

    // Check required roles exist
    const requiredRoles = [
      'admin', 'developer', 'reviewer', 'security', 'database',
      'frontend', 'backend', 'tester', 'analyst', 'coordinator'
    ];

    for (const role of requiredRoles) {
      if (!rules.roles[role]) {
        errors.push(`Missing required role: ${role}`);
        continue;
      }

      const roleData = rules.roles[role];

      // Check required fields
      if (!roleData.permissions) {
        errors.push(`Role ${role} missing permissions object`);
        continue;
      }

      if (!roleData.permissions.tools) {
        errors.push(`Role ${role} missing permissions.tools`);
      }

      if (!roleData.permissions.paths) {
        errors.push(`Role ${role} missing permissions.paths`);
      }

      if (!roleData.permissions.api_access) {
        errors.push(`Role ${role} missing permissions.api_access`);
      }

      if (!roleData.budget) {
        errors.push(`Role ${role} missing budget object`);
      } else {
        if (typeof roleData.budget.max_tokens_per_session !== 'number') {
          errors.push(`Role ${role} budget.max_tokens_per_session must be number`);
        }

        if (typeof roleData.budget.max_cost_per_day !== 'number') {
          errors.push(`Role ${role} budget.max_cost_per_day must be number`);
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors
    };
  } catch (error) {
    errors.push(`Failed to load RBAC rules: ${error.message}`);
    return {
      valid: false,
      errors
    };
  }
}

/**
 * Clear RBAC rules cache
 */
function clearCache() {
  rbacRulesCache = null;
  rbacRulesCacheTime = 0;
}

module.exports = {
  loadRBACRules,
  checkToolPermission,
  checkPathPermission,
  checkAPIPermission,
  checkApprovalRequired,
  getBudgetImpact,
  checkBudgetThreshold,
  checkPermission,
  validateRBACRules,
  clearCache
};
