/**
 * Pre-Permission-Check Hook
 * Enforces RBAC path permissions and API access
 * Priority: 2 (after identity verification)
 * Blocking: true (stops execution on permission denial)
 */

const fs = require('fs');
const path = require('path');

const RBAC_RULES_PATH = path.join(__dirname, '..', '..', '..', 'agents', 'identity', 'agent-rbac-rules.json');

function isPathAllowed(filePath, allowedPaths) {
  if (allowedPaths.includes('**')) return true;
  const normalizedPath = filePath.replace(/\\/g, '/');  // Normalize path separators
  return allowedPaths.some(pattern => {
    const regexPattern = pattern.replace(/\*\*/g, '.*').replace(/\*/g, '[^/]*').replace(/\//g, '[\\/]');
    const regex = new RegExp(`^${regexPattern}$`);
    return regex.test(normalizedPath);
  });
}

function hasApiAccess(apiName, allowedApis) {
  if (allowedApis.includes('*')) return true;
  return allowedApis.includes(apiName);
}

async function execute(context) {
  const startTime = Date.now();

  try {
    const agentRole = context.agentRole || context.agent_role || context.metadata?.agentRole || 'unknown';
    const toolName = context.toolName;

    let rbacRules;
    try {
      const rbacData = fs.readFileSync(RBAC_RULES_PATH, 'utf8');
      rbacRules = JSON.parse(rbacData);
    } catch (error) {
      console.error('[pre-permission-check] Failed to load RBAC rules:', error.message);
      return { success: false, reason: 'RBAC rules unavailable', allowed: false, blocking: true, error: error.message };
    }

    const roleConfig = rbacRules.roles[agentRole];
    if (!roleConfig) {
      console.error(`[pre-permission-check] BLOCKED: Unknown role: ${agentRole}`);
      return { success: false, reason: `Unknown agent role: ${agentRole}`, allowed: false, blocking: true };
    }

    // Check file path permissions
    if (toolName === 'Read' || toolName === 'Write' || toolName === 'Edit') {
      const filePath = context.file_path || context.filePath || '';
      const allowedPaths = roleConfig.permissions.paths || [];

      if (!isPathAllowed(filePath, allowedPaths)) {
        console.error(`[pre-permission-check] BLOCKED: Path not allowed for ${agentRole}: ${filePath}`);
        return { success: false, reason: `Path access denied: ${filePath} (role: ${agentRole})`, allowed: false, blocking: true };
      }
    }

    // Check API access
    if (toolName.startsWith('mcp__')) {
      const apiMatch = toolName.match(/mcp__([^_]+)__/);
      const apiName = apiMatch ? apiMatch[1] : 'unknown';
      const allowedApis = roleConfig.permissions.api_access || [];

      if (!hasApiAccess(apiName, allowedApis)) {
        console.error(`[pre-permission-check] BLOCKED: API access denied for ${agentRole}: ${apiName}`);
        return { success: false, reason: `API access denied: ${apiName} (role: ${agentRole})`, allowed: false, blocking: true };
      }
    }

    // Check agent spawning
    if (toolName === 'Task' && !roleConfig.permissions.can_spawn_agents) {
      console.error(`[pre-permission-check] BLOCKED: Agent spawning not allowed for ${agentRole}`);
      return { success: false, reason: `Agent spawning denied (role: ${agentRole})`, allowed: false, blocking: true };
    }

    console.log(`[pre-permission-check] ALLOWED: Permissions verified for ${agentRole}`);
    return { success: true, reason: `Permissions verified for ${agentRole}`, allowed: true, agent_role: agentRole, level: roleConfig.level, execution_time: Date.now() - startTime };

  } catch (error) {
    console.error('[pre-permission-check] Error:', error.message);
    return { success: false, reason: `Permission check error: ${error.message}`, allowed: false, blocking: true, error: error.message };
  }
}

module.exports = { execute };
