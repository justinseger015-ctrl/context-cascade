/**
 * Context Cascade Security Module
 * Phase 1 Security Hardening - Integration Layer
 *
 * Provides unified access to all security components:
 * - RBAC enforcement
 * - Token management
 * - MCP integrity validation
 * - Sandbox execution routing
 *
 * @module security
 */

// Load security components
const rbacEnforcer = require('./rbac/enforcer.cjs');
const tokenManager = require('./tokens/token-manager.cjs');
const checksumValidator = require('./mcp-integrity/checksum-validator.cjs');
const sandboxRouter = require('./sandbox/sandbox-router.cjs');

/**
 * Initialize security subsystem
 * @param {Object} options - Configuration options
 * @returns {Object} Initialization result
 */
async function initialize(options = {}) {
  const results = {
    timestamp: new Date().toISOString(),
    components: {},
    ready: false
  };

  // Initialize RBAC
  try {
    rbacEnforcer.loadRBACRules();
    results.components.rbac = { status: 'ready', message: 'RBAC rules loaded' };
  } catch (err) {
    results.components.rbac = { status: 'error', message: err.message };
  }

  // Initialize token manager (keys are lazy-loaded)
  results.components.tokens = { status: 'ready', message: 'Token manager available' };

  // Initialize MCP integrity
  try {
    checksumValidator.initializeBuiltinServers();
    results.components.mcpIntegrity = { status: 'ready', message: 'Checksum registry loaded' };
  } catch (err) {
    results.components.mcpIntegrity = { status: 'error', message: err.message };
  }

  // Initialize sandbox router
  if (options.validateSandbox) {
    const sandboxValidation = await sandboxRouter.validateSandbox();
    results.components.sandbox = {
      status: sandboxValidation.valid ? 'ready' : 'degraded',
      message: sandboxValidation.valid
        ? 'Codex sandbox available'
        : 'Sandbox not available - will use direct execution',
      details: sandboxValidation
    };
  } else {
    results.components.sandbox = { status: 'ready', message: 'Sandbox router available' };
  }

  // Overall readiness
  const allReady = Object.values(results.components)
    .every(c => c.status === 'ready' || c.status === 'degraded');
  results.ready = allReady;

  return results;
}

/**
 * Secure agent registration with token generation
 * @param {string} agentId - Agent identifier
 * @param {string} role - RBAC role
 * @returns {Object} Registration result with token
 */
function registerSecureAgent(agentId, role) {
  // Generate cryptographic token
  const tokenResult = tokenManager.generateToken(agentId, role);

  // Register with RBAC enforcer
  rbacEnforcer.registerAgent(agentId, role, tokenResult.token);

  // Store token for session
  tokenManager.storeToken(agentId, tokenResult.token);

  return {
    agentId,
    role,
    token: tokenResult.token,
    expiresAt: tokenResult.expiresAt,
    registered: true
  };
}

/**
 * Enforce security for a tool call
 * @param {string} agentId - Agent making the call
 * @param {string} toolName - Tool being called
 * @param {Object} params - Tool parameters
 * @returns {Object} Enforcement result
 */
function enforceToolCall(agentId, toolName, params = {}) {
  // Get stored token
  const token = tokenManager.getStoredToken(agentId);

  if (!token) {
    return {
      allowed: false,
      reason: `SECURITY_DENIED: No active session for agent '${agentId}'`
    };
  }

  // Validate token is not expired or revoked
  const tokenValidation = tokenManager.fullValidation(token);
  if (!tokenValidation.valid) {
    return {
      allowed: false,
      reason: `SECURITY_DENIED: ${tokenValidation.reason}`
    };
  }

  // Enforce RBAC
  return rbacEnforcer.enforceRBAC(agentId, token, toolName, params);
}

/**
 * Validate MCP server before loading
 * @param {string} serverName - MCP server name
 * @param {string} serverPath - Path to server entry
 * @returns {Object} Validation result
 */
function validateMCPServer(serverName, serverPath) {
  return checksumValidator.validateServer(serverName, serverPath);
}

/**
 * Execute command in sandbox
 * @param {string} command - Command to execute
 * @param {Object} options - Execution options
 * @returns {Promise<Object>} Execution result
 */
async function executeSecure(command, options = {}) {
  // Route through sandbox if available
  return sandboxRouter.executeInSandbox(command, options);
}

/**
 * Run tests in isolated sandbox
 * @param {string} testCommand - Test command
 * @param {Object} options - Options
 * @returns {Promise<Object>} Test results
 */
async function runTestsSecure(testCommand, options = {}) {
  return sandboxRouter.runTestsInSandbox(testCommand, options);
}

/**
 * Audit all security components
 * @returns {Object} Audit results
 */
async function auditSecurity() {
  const results = {
    timestamp: new Date().toISOString(),
    checks: {}
  };

  // Check RBAC rules are loaded
  const rules = rbacEnforcer.loadRBACRules();
  results.checks.rbacRules = {
    loaded: !!rules.roles,
    roleCount: Object.keys(rules.roles || {}).length
  };

  // Check token manager
  results.checks.tokenManager = {
    configValid: !!tokenManager.TOKEN_CONFIG.algorithm
  };

  // Check MCP registry
  const servers = checksumValidator.listServers();
  results.checks.mcpRegistry = {
    serverCount: servers.length,
    trustedCount: servers.filter(s => s.trusted).length
  };

  // Check sandbox availability
  const sandboxCheck = await sandboxRouter.checkCodexAvailable();
  results.checks.sandbox = {
    codexAvailable: sandboxCheck.available,
    version: sandboxCheck.version || 'N/A'
  };

  // Validate all registered MCP servers
  const mcpValidation = checksumValidator.validateAllServers();
  results.checks.mcpIntegrity = mcpValidation;

  return results;
}

/**
 * Security middleware factory
 * @param {Function} handler - Original handler
 * @param {Object} options - Middleware options
 * @returns {Function} Secured handler
 */
function securityMiddleware(handler, options = {}) {
  return rbacEnforcer.createRBACMiddleware(handler);
}

// Export unified security API
module.exports = {
  // Initialization
  initialize,

  // Agent management
  registerSecureAgent,

  // Enforcement
  enforceToolCall,
  securityMiddleware,

  // MCP integrity
  validateMCPServer,
  registerMCPServer: checksumValidator.registerServer,
  listMCPServers: checksumValidator.listServers,

  // Sandboxed execution
  executeSecure,
  runTestsSecure,
  createSandboxContext: sandboxRouter.createSandboxContext,

  // Token management
  generateToken: tokenManager.generateToken,
  validateToken: tokenManager.fullValidation,
  revokeToken: tokenManager.revokeToken,

  // Auditing
  auditSecurity,
  auditLog: rbacEnforcer.auditLog,

  // Direct access to components (for advanced use)
  rbac: rbacEnforcer,
  tokens: tokenManager,
  mcpIntegrity: checksumValidator,
  sandbox: sandboxRouter,

  // Constants
  SANDBOX_MODES: sandboxRouter.SANDBOX_MODES
};
