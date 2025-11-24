/**
 * Pre-Identity-Verify Hook
 * Blocks tool use if agent identity is invalid or command is dangerous
 * Priority: 1 (first in security chain)
 * Blocking: true (stops execution on failure)
 */

const fs = require('fs');
const path = require('path');

const RBAC_RULES_PATH = path.join(__dirname, '..', '..', '..', 'agents', 'identity', 'agent-rbac-rules.json');

// Dangerous command patterns
const DANGEROUS_COMMANDS = [
  /rm\s+-rf\s+\//,           // rm -rf /
  /rm\s+-rf\s+\*/,           // rm -rf *
  /del\s+\/s\s+\/q/i,        // del /s /q (Windows)
  /format\s+c:/i,            // format c:
  /dd\s+if=/,                // dd if=
  /:\(\)\{.*\};:/,           // Fork bomb
  /sudo\s+rm/,               // sudo rm
  /chmod\s+-R\s+777/,        // chmod -R 777
  /chown\s+-R/,              // chown -R
  /mkfs/,                    // mkfs (format disk)
  /fdisk/,                   // fdisk
  />\/dev\/sda/,               // Write to disk
  /shutdown/,                // shutdown
  /reboot/,                  // reboot
  /halt/,                    // halt
  /poweroff/                 // poweroff
];

// Environment/secret files
const SECRET_FILES = [
  '.env',
  '.env.local',
  '.env.production',
  'credentials.json',
  'secrets.yaml',
  'secrets.yml',
  'config/secrets',
  'id_rsa',
  'id_dsa',
  '.aws/credentials',
  '.ssh/',
  'database.yml'
];

function isDangerousCommand(context) {
  if (context.toolName !== 'Bash') return false;
  const command = context.command || '';
  return DANGEROUS_COMMANDS.some(pattern => pattern.test(command));
}

function isSecretFileAccess(context) {
  if (context.toolName !== 'Read' && context.toolName !== 'Edit' && context.toolName !== 'Write') return false;
  const filePath = context.file_path || context.filePath || '';
  return SECRET_FILES.some(file => filePath.includes(file));
}

function verifyAgentIdentity(context) {
  const agentId = context.agentId || context.agent_id || context.metadata?.agentId;

  if (!agentId) {
    return { allowed: true, reason: 'System operation (no agent identity required)', warning: true };
  }

  let rbacRules;
  try {
    const rbacData = fs.readFileSync(RBAC_RULES_PATH, 'utf8');
    rbacRules = JSON.parse(rbacData);
  } catch (error) {
    return { allowed: false, reason: 'RBAC rules unavailable', error: error.message };
  }

  const agentRole = context.agentRole || context.agent_role || context.metadata?.agentRole || 'unknown';
  const roleConfig = rbacRules.roles[agentRole];

  if (!roleConfig) {
    return { allowed: false, reason: `Unknown agent role: ${agentRole} (not in RBAC rules)` };
  }

  const toolName = context.toolName;
  const allowedTools = roleConfig.permissions.tools;

  if (allowedTools.includes('*') || allowedTools.includes(toolName)) {
    return { allowed: true, reason: `Agent identity verified: ${agentRole} (level ${roleConfig.level})`, agent_role: agentRole, level: roleConfig.level };
  }

  return { allowed: false, reason: `Agent role '${agentRole}' not authorized for tool: ${toolName}` };
}

async function execute(context) {
  const startTime = Date.now();

  try {
    if (isDangerousCommand(context)) {
      const command = context.command || '';
      console.error(`[pre-identity-verify] BLOCKED: Dangerous command: ${command.substring(0, 50)}...`);
      return { success: false, reason: `Command blocked: Dangerous operation detected`, allowed: false, blocking: true, security_event: { type: 'dangerous_command', command, blocked_at: new Date().toISOString() } };
    }

    if (isSecretFileAccess(context)) {
      const filePath = context.file_path || context.filePath || '';
      console.error(`[pre-identity-verify] BLOCKED: Secret file access: ${filePath}`);
      return { success: false, reason: `File access blocked: Secret/environment file`, allowed: false, blocking: true, security_event: { type: 'secret_file_access', file: filePath, blocked_at: new Date().toISOString() } };
    }

    const verification = verifyAgentIdentity(context);

    if (!verification.allowed) {
      console.error(`[pre-identity-verify] BLOCKED: ${verification.reason}`);
      return { success: false, reason: verification.reason, allowed: false, blocking: true, security_event: { type: 'identity_verification_failed', agent_id: context.agentId || context.agent_id, tool: context.toolName, blocked_at: new Date().toISOString() } };
    }

    console.log(`[pre-identity-verify] ALLOWED: ${verification.reason}`);
    return { success: true, reason: verification.reason, allowed: true, agent_role: verification.agent_role, level: verification.level, execution_time: Date.now() - startTime };

  } catch (error) {
    console.error('[pre-identity-verify] Error:', error.message);
    return { success: false, reason: `Security hook error: ${error.message}`, allowed: false, blocking: true, error: error.message };
  }
}

module.exports = { execute };