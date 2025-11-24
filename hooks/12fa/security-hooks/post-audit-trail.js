/**
 * Post-Audit Trail Hook
 * Logs all operations to audit trail (database + file fallback)
 * Priority: 5 (runs after operation)
 * Blocking: false (non-blocking)
 */

const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

const AUDIT_LOG = path.join(__dirname, '..', '.audit-trail.log');
const DB_PATH = path.join(__dirname, '..', 'agent-reality-map.db');

/**
 * Get database connection (cached)
 */
let dbConnection = null;
function getDatabase() {
  if (!dbConnection) {
    dbConnection = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE, (err) => {
      if (err) {
        console.error('[post-audit-trail] Database connection failed:', err.message);
        dbConnection = null;
      }
    });
  }
  return dbConnection;
}

/**
 * Format audit entry
 * @param {string} agentId - Agent identifier
 * @param {string} operation - Operation name
 * @param {object} context - Operation context
 * @param {object} result - Operation result
 */
function formatAuditEntry(agentId, operation, context, result) {
  return {
    timestamp: new Date().toISOString(),
    agentId,
    operation,
    context: {
      toolName: context.toolName,
      filePath: context.filePath,
      command: context.command,
      metadata: context.metadata
    },
    result: {
      success: result?.success !== false,
      error: result?.error,
      executionTime: result?.executionTime
    }
  };
}

/**
 * Write audit entry to database (async, non-blocking)
 * @param {object} entry - Audit entry
 * @param {string} agentRole - Agent role
 * @param {boolean} allowed - Whether operation was allowed
 * @param {string} deniedReason - Reason if denied
 * @param {number} budgetImpact - Budget impact
 * @param {string} sessionId - Session identifier
 */
function writeAuditToDatabase(entry, agentRole, allowed, deniedReason, budgetImpact, sessionId) {
  const db = getDatabase();
  if (!db) {
    // Fallback to file logging
    writeAuditToFile(entry);
    return;
  }

  const query = `
    INSERT INTO agent_audit_log (
      timestamp,
      agent_id,
      agent_role,
      operation,
      tool_name,
      file_path,
      api_name,
      allowed,
      denied_reason,
      budget_impact,
      session_id,
      metadata
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `;

  const params = [
    entry.timestamp,
    entry.agentId,
    agentRole || 'unknown',
    entry.operation,
    entry.context.toolName || null,
    entry.context.filePath || null,
    entry.context.metadata?.apiName || null,
    allowed ? 1 : 0,
    deniedReason || null,
    budgetImpact || 0.0,
    sessionId || null,
    JSON.stringify(entry.context.metadata || {})
  ];

  // Async write, non-blocking
  db.run(query, params, function(err) {
    if (err) {
      console.error('[post-audit-trail] Database write failed:', err.message);
      // Fallback to file logging
      writeAuditToFile(entry);
    }
  });
}

/**
 * Write audit entry to file (fallback)
 * @param {object} entry - Audit entry
 */
function writeAuditToFile(entry) {
  try {
    const line = JSON.stringify(entry) + '\n';
    fs.appendFileSync(AUDIT_LOG, line);
  } catch (error) {
    console.error('[post-audit-trail] File write failed:', error.message);
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
         'system';
}

/**
 * Extract operation from context
 * @param {object} context - Hook execution context
 */
function extractOperation(context) {
  return context.toolName ||
         context.operation ||
         context.metadata?.operation ||
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
    const operation = extractOperation(context);

    // Extract additional metadata
    const agentRole = context.agentRole || context.metadata?.agentRole || 'unknown';
    const allowed = context.result?.allowed !== false;
    const deniedReason = context.result?.deniedReason || null;
    const budgetImpact = context.result?.budgetImpact || 0.0;
    const sessionId = context.sessionId || context.metadata?.sessionId || null;

    // Format audit entry
    const entry = formatAuditEntry(agentId, operation, context, context.result);

    // Write to database (async, non-blocking)
    writeAuditToDatabase(entry, agentRole, allowed, deniedReason, budgetImpact, sessionId);

    console.log(`[post-audit-trail] Logged operation: ${agentId} - ${operation} (allowed: ${allowed})`);

    return {
      success: true,
      reason: 'Operation logged to audit trail',
      agentId,
      operation,
      allowed,
      executionTime: Date.now() - startTime
    };

  } catch (error) {
    console.error('[post-audit-trail] Error:', error.message);

    // Non-blocking: always return success
    return {
      success: true,
      reason: `Audit logging failed (non-blocking): ${error.message}`,
      executionTime: Date.now() - startTime,
      error: error.message
    };
  }
}

module.exports = { execute };
