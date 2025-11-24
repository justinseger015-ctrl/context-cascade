const http = require('http');
const TOOL_TOKEN_COSTS = {'Task': 5000, 'Write': 500, 'Edit': 1000, 'Read': 100, 'Bash': 500};
function sendBudgetDeduction(deduction) {
  return new Promise((resolve) => {
    const postData = JSON.stringify(deduction);
    const options = {hostname: 'localhost', port: 8000, path: '/api/v1/budget/deduct', method: 'POST', headers: {'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(postData)}, timeout: 2000};
    const req = http.request(options, (res) => {
      if (res.statusCode === 200 || res.statusCode === 201) { resolve(true); } else { resolve(false); }
    });
    req.on('error', () => resolve(false));
    req.on('timeout', () => { req.destroy(); resolve(false); });
    req.write(postData);
    req.end();
  });
}
async function execute(context) {
  try {
    const agentId = context.agentId || context.agent_id;
    const agentRole = context.agentRole || context.agent_role || 'unknown';
    const toolName = context.toolName;
    const tokensUsed = TOOL_TOKEN_COSTS[toolName] || 500;
    const costUSD = (tokensUsed / 1000000) * 3.0;
    const deduction = {agent_id: agentId, agent_role: agentRole, tool_name: toolName, tokens_used: tokensUsed, cost_usd: costUSD, timestamp: new Date().toISOString()};
    const sent = await sendBudgetDeduction(deduction);
    return { success: true, reason: sent ? 'Budget deduction recorded' : 'Backend unavailable', tokens_used: tokensUsed, cost_usd: costUSD };
  } catch (error) {
    return { success: true, reason: 'Budget deduction error (non-blocking)', error: error.message };
  }
}
module.exports = { execute };
