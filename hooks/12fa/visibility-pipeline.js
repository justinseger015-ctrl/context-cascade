/**
 * Visibility Pipeline Hook
 * Real-time agent action logging via backend API (database + WebSocket broadcasting)
 * Priority: 5 (runs after tool use)
 * Blocking: false (non-blocking)
 *
 * Architecture: Hook → Backend API → Database + WebSocket → Dashboard
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

const VISIBILITY_LOG = path.join(__dirname, '..', '.visibility-pipeline.log');
const BACKEND_HOST = 'localhost';
const BACKEND_PORT = 8000;

/**
 * Extract agent name from context
 * @param {object} context - Hook execution context
 */
function extractAgentName(context) {
  return context.agentName ||
         context.agent_name ||
         context.metadata?.agentName ||
         extractAgentId(context); // Fallback to agent ID
}

/**
 * Format visibility event for backend API
 * Maps to AuditLog model schema: agent_id, agent_name, agent_role, operation_type, operation_detail, etc.
 * @param {string} agentId - Agent identifier
 * @param {string} agentName - Agent name
 * @param {string} toolName - Tool name (Task, Edit, Write, Bash, etc.)
 * @param {object} context - Tool execution context
 * @param {object} result - Tool execution result
 */
function formatVisibilityEvent(agentId, agentName, toolName, context, result) {
  return {
    agent_id: agentId,
    agent_name: agentName,
    agent_role: context.agentRole || context.agent_role || 'unknown',
    operation_type: 'tool_use',
    operation_detail: `${toolName}: ${context.description || context.file_path || context.command || 'operation'}`,
    target_resource: context.file_path || context.filePath || context.command || null,
    target_type: getTargetType(toolName),
    rbac_decision: result?.success !== false ? 'allowed' : 'denied',
    rbac_reason: result?.error || null,
    cost_usd: result?.budgetImpact || result?.budget_impact || 0.0,
    tokens_used: result?.tokens || null,
    context: {
      session_id: context.sessionId || context.session_id || null,
      tool_name: toolName,
      execution_time_ms: result?.executionTime || result?.execution_time || 0,
      artifacts: extractArtifacts(toolName, context, result),
      metadata: context.metadata || {}
    }
  };
}

/**
 * Determine target type based on tool name
 * @param {string} toolName - Tool name
 */
function getTargetType(toolName) {
  const typeMap = {
    'Write': 'file',
    'Edit': 'file',
    'Read': 'file',
    'Bash': 'command',
    'Task': 'agent',
    'Grep': 'search',
    'Glob': 'search'
  };
  return typeMap[toolName] || 'unknown';
}

/**
 * Extract artifacts from tool execution
 * @param {string} toolName - Tool name
 * @param {object} context - Execution context
 * @param {object} result - Execution result
 */
function extractArtifacts(toolName, context, result) {
  const artifacts = [];

  if (toolName === 'Write' && context.file_path) {
    artifacts.push({ type: 'file_created', path: context.file_path });
  } else if (toolName === 'Edit' && context.file_path) {
    artifacts.push({ type: 'file_modified', path: context.file_path });
  } else if (toolName === 'Task' && result?.agentId) {
    artifacts.push({ type: 'agent_spawned', agent_id: result.agentId });
  } else if (toolName === 'Bash' && context.command) {
    artifacts.push({ type: 'command_executed', command: context.command });
  }

  return artifacts;
}

/**
 * Send visibility event to backend API
 * Backend handles database persistence + WebSocket broadcasting
 * @param {object} event - Visibility event
 * @returns {Promise<boolean>} Success status
 */
function sendEventToBackend(event) {
  return new Promise((resolve) => {
    // Send event directly (backend expects flat EventIngest schema)
    const postData = JSON.stringify(event);

    const options = {
      hostname: BACKEND_HOST,
      port: BACKEND_PORT,
      path: '/api/v1/events/ingest',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      },
      timeout: 2000 // 2 second timeout
    };

    const req = http.request(options, (res) => {
      let responseBody = '';
      res.on('data', (chunk) => {
        responseBody += chunk;
      });
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          console.log(`[visibility-pipeline] Event sent: ${event.agent_id} - ${event.operation_type}`);
          resolve(true);
        } else {
          console.error(`[visibility-pipeline] Backend API failed: HTTP ${res.statusCode}`);
          writeEventToFile(event);
          resolve(false);
        }
      });
    });

    req.on('error', (err) => {
      console.error('[visibility-pipeline] Backend API error:', err.message);
      writeEventToFile(event);
      resolve(false);
    });

    req.on('timeout', () => {
      console.error('[visibility-pipeline] Backend API timeout');
      req.destroy();
      writeEventToFile(event);
      resolve(false);
    });

    req.write(postData);
    req.end();
  });
}

/**
 * Write visibility event to file (fallback)
 * @param {object} event - Visibility event
 */
function writeEventToFile(event) {
  try {
    const line = JSON.stringify(event) + '\n';
    fs.appendFileSync(VISIBILITY_LOG, line);
  } catch (error) {
    console.error('[visibility-pipeline] File write failed:', error.message);
  }
}


/**
 * Extract agent ID from context
 * @param {object} context - Hook execution context
 */
function extractAgentId(context) {
  return context.agentId ||
         context.agent_id ||
         context.metadata?.agentId ||
         context.metadata?.agent_id ||
         'system';
}

/**
 * Extract tool name from context
 * @param {object} context - Hook execution context
 */
function extractToolName(context) {
  return context.toolName ||
         context.tool_name ||
         context.metadata?.toolName ||
         'unknown';
}

/**
 * Main hook execution
 * @param {object} context - Hook execution context
 */
async function execute(context) {
  const startTime = Date.now();

  try {
    const agentId = extractAgentId(context);
    const agentName = extractAgentName(context);
    const toolName = extractToolName(context);

    // Format visibility event for backend API
    const event = formatVisibilityEvent(agentId, agentName, toolName, context, context.result || {});

    // Send to backend API (handles database + WebSocket)
    const sent = await sendEventToBackend(event);

    console.log(`[visibility-pipeline] Event ${sent ? 'sent' : 'fallback'}: ${agentId} - ${toolName} (decision: ${event.rbac_decision})`);

    return {
      success: true,
      reason: sent ? 'Visibility event sent to backend' : 'Visibility event logged to file (backend unavailable)',
      agent_id: agentId,
      tool_name: toolName,
      execution_time: Date.now() - startTime
    };

  } catch (error) {
    console.error('[visibility-pipeline] Error:', error.message);

    // Non-blocking: always return success
    return {
      success: true,
      reason: `Visibility logging failed (non-blocking): ${error.message}`,
      execution_time: Date.now() - startTime,
      error: error.message
    };
  }
}

module.exports = { execute };
