const HIGH_RISK = {'Bash': {patterns: [{regex: /git\s+push\s+.*origin\s+(main|master)/, desc: 'Push to main/master'}]}, 'Write': {paths: ['package.json', '.github/workflows/']}};
function requiresApproval(context) {
  const toolName = context.toolName;
  if (HIGH_RISK[toolName]) {
    if (toolName === 'Bash') {
      const command = context.command || '';
      const riskPattern = HIGH_RISK.Bash.patterns.find(p => p.regex.test(command));
      if (riskPattern) return { required: true, reason: riskPattern.desc };
    }
    if (toolName === 'Write') {
      const filePath = context.file_path || context.filePath || '';
      if (HIGH_RISK.Write.paths.find(p => filePath.includes(p))) return { required: true, reason: 'Critical file' };
    }
  }
  return { required: false };
}
async function execute(context) {
  try {
    const check = requiresApproval(context);
    if (!check.required) {
      return { success: true, reason: 'No approval required', allowed: true };
    }
    console.log('[pre-approval-gate] High-risk: ' + check.reason + ' (auto-approved for now)');
    return { success: true, reason: 'Auto-approved', allowed: true };
  } catch (error) {
    return { success: false, reason: 'Approval gate error', allowed: false, blocking: true };
  }
}
module.exports = { execute };
