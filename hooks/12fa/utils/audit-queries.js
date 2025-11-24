/**
 * Audit Log Query Module
 * Provides query functions for agent_audit_log database
 * Performance target: <50ms per query
 * Windows compatible: No Unicode
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

// Database path (same as used by post-audit-trail hook)
const DB_PATH = path.join(__dirname, '..', 'agent-reality-map.db');

/**
 * Get database connection (reusable)
 * @returns {Promise<sqlite3.Database>}
 */
function getDatabase() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE, (err) => {
      if (err) {
        reject(new Error(`Database connection failed: ${err.message}`));
      } else {
        resolve(db);
      }
    });
  });
}

/**
 * Close database connection
 * @param {sqlite3.Database} db
 */
function closeDatabase(db) {
  return new Promise((resolve, reject) => {
    db.close((err) => {
      if (err) reject(err);
      else resolve();
    });
  });
}

/**
 * Get recent audit logs for a specific agent
 * @param {string} agentId - Agent identifier
 * @param {number} limit - Maximum number of records (default: 100)
 * @returns {Promise<Array>}
 */
async function getAuditLog(agentId, limit = 100) {
  const db = await getDatabase();

  return new Promise((resolve, reject) => {
    const query = `
      SELECT
        id,
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
      FROM agent_audit_log
      WHERE agent_id = ?
      ORDER BY timestamp DESC
      LIMIT ?
    `;

    db.all(query, [agentId, limit], (err, rows) => {
      closeDatabase(db);

      if (err) {
        reject(new Error(`Query failed: ${err.message}`));
      } else {
        // Parse JSON metadata
        const results = rows.map(row => ({
          ...row,
          metadata: row.metadata ? JSON.parse(row.metadata) : null,
          allowed: Boolean(row.allowed)
        }));
        resolve(results);
      }
    });
  });
}

/**
 * Search audit logs with flexible filters
 * @param {object} filters - Search filters
 * @param {string} filters.agentId - Agent ID (optional)
 * @param {string} filters.operation - Operation name (optional)
 * @param {boolean} filters.allowed - Allowed status (optional)
 * @param {string} filters.startDate - Start date ISO string (optional)
 * @param {string} filters.endDate - End date ISO string (optional)
 * @param {string} filters.sessionId - Session ID (optional)
 * @param {number} filters.limit - Max results (default: 100)
 * @returns {Promise<Array>}
 */
async function searchAuditLog(filters = {}) {
  const db = await getDatabase();

  return new Promise((resolve, reject) => {
    const conditions = [];
    const params = [];

    // Build WHERE clause dynamically
    if (filters.agentId) {
      conditions.push('agent_id = ?');
      params.push(filters.agentId);
    }

    if (filters.operation) {
      conditions.push('operation = ?');
      params.push(filters.operation);
    }

    if (typeof filters.allowed === 'boolean') {
      conditions.push('allowed = ?');
      params.push(filters.allowed ? 1 : 0);
    }

    if (filters.startDate) {
      conditions.push('timestamp >= ?');
      params.push(filters.startDate);
    }

    if (filters.endDate) {
      conditions.push('timestamp <= ?');
      params.push(filters.endDate);
    }

    if (filters.sessionId) {
      conditions.push('session_id = ?');
      params.push(filters.sessionId);
    }

    const whereClause = conditions.length > 0
      ? `WHERE ${conditions.join(' AND ')}`
      : '';

    const limit = filters.limit || 100;
    params.push(limit);

    const query = `
      SELECT
        id,
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
      FROM agent_audit_log
      ${whereClause}
      ORDER BY timestamp DESC
      LIMIT ?
    `;

    db.all(query, params, (err, rows) => {
      closeDatabase(db);

      if (err) {
        reject(new Error(`Search query failed: ${err.message}`));
      } else {
        const results = rows.map(row => ({
          ...row,
          metadata: row.metadata ? JSON.parse(row.metadata) : null,
          allowed: Boolean(row.allowed)
        }));
        resolve(results);
      }
    });
  });
}

/**
 * Get statistics for a specific agent
 * @param {string} agentId - Agent identifier
 * @returns {Promise<object>}
 */
async function getAuditStats(agentId) {
  const db = await getDatabase();

  return new Promise((resolve, reject) => {
    const query = `
      SELECT
        COUNT(*) as total_operations,
        SUM(CASE WHEN allowed = 1 THEN 1 ELSE 0 END) as allowed_operations,
        SUM(CASE WHEN allowed = 0 THEN 1 ELSE 0 END) as denied_operations,
        SUM(budget_impact) as total_budget_used,
        AVG(budget_impact) as avg_budget_per_op,
        MAX(budget_impact) as max_budget_operation,
        MIN(timestamp) as first_operation,
        MAX(timestamp) as last_operation,
        COUNT(DISTINCT session_id) as unique_sessions,
        COUNT(DISTINCT operation) as unique_operations
      FROM agent_audit_log
      WHERE agent_id = ?
    `;

    db.get(query, [agentId], (err, row) => {
      closeDatabase(db);

      if (err) {
        reject(new Error(`Stats query failed: ${err.message}`));
      } else {
        resolve({
          agentId,
          totalOperations: row.total_operations || 0,
          allowedOperations: row.allowed_operations || 0,
          deniedOperations: row.denied_operations || 0,
          totalBudgetUsed: row.total_budget_used || 0,
          avgBudgetPerOp: row.avg_budget_per_op || 0,
          maxBudgetOperation: row.max_budget_operation || 0,
          firstOperation: row.first_operation,
          lastOperation: row.last_operation,
          uniqueSessions: row.unique_sessions || 0,
          uniqueOperations: row.unique_operations || 0
        });
      }
    });
  });
}

/**
 * Get recent denied operations (security monitoring)
 * @param {number} limit - Maximum number of records (default: 50)
 * @returns {Promise<Array>}
 */
async function getRecentDenials(limit = 50) {
  const db = await getDatabase();

  return new Promise((resolve, reject) => {
    const query = `
      SELECT
        id,
        timestamp,
        agent_id,
        agent_role,
        operation,
        tool_name,
        file_path,
        api_name,
        denied_reason,
        session_id,
        metadata
      FROM agent_audit_log
      WHERE allowed = 0
      ORDER BY timestamp DESC
      LIMIT ?
    `;

    db.all(query, [limit], (err, rows) => {
      closeDatabase(db);

      if (err) {
        reject(new Error(`Denials query failed: ${err.message}`));
      } else {
        const results = rows.map(row => ({
          ...row,
          metadata: row.metadata ? JSON.parse(row.metadata) : null
        }));
        resolve(results);
      }
    });
  });
}

/**
 * Get budget impact summary for all agents
 * @returns {Promise<Array>}
 */
async function getBudgetSummary() {
  const db = await getDatabase();

  return new Promise((resolve, reject) => {
    const query = `
      SELECT
        agent_id,
        agent_role,
        COUNT(*) as total_operations,
        SUM(budget_impact) as total_budget_used,
        AVG(budget_impact) as avg_budget_per_op,
        MAX(budget_impact) as max_budget_op,
        MAX(timestamp) as last_operation
      FROM agent_audit_log
      WHERE allowed = 1
      GROUP BY agent_id, agent_role
      ORDER BY total_budget_used DESC
    `;

    db.all(query, [], (err, rows) => {
      closeDatabase(db);

      if (err) {
        reject(new Error(`Budget summary query failed: ${err.message}`));
      } else {
        resolve(rows.map(row => ({
          agentId: row.agent_id,
          agentRole: row.agent_role,
          totalOperations: row.total_operations,
          totalBudgetUsed: row.total_budget_used || 0,
          avgBudgetPerOp: row.avg_budget_per_op || 0,
          maxBudgetOp: row.max_budget_op || 0,
          lastOperation: row.last_operation
        })));
      }
    });
  });
}

/**
 * Clean up old audit logs (90-day retention)
 * @returns {Promise<number>} Number of deleted records
 */
async function cleanupOldLogs() {
  const db = await getDatabase();

  return new Promise((resolve, reject) => {
    const query = `
      DELETE FROM agent_audit_log
      WHERE timestamp < datetime('now', '-90 days')
    `;

    db.run(query, function(err) {
      closeDatabase(db);

      if (err) {
        reject(new Error(`Cleanup failed: ${err.message}`));
      } else {
        resolve(this.changes);
      }
    });
  });
}

/**
 * Get operation frequency distribution
 * @param {string} agentId - Agent ID (optional)
 * @param {number} days - Days to look back (default: 7)
 * @returns {Promise<Array>}
 */
async function getOperationFrequency(agentId = null, days = 7) {
  const db = await getDatabase();

  return new Promise((resolve, reject) => {
    const whereClause = agentId ? 'WHERE agent_id = ? AND' : 'WHERE';
    const params = agentId ? [agentId] : [];

    const query = `
      SELECT
        operation,
        COUNT(*) as frequency,
        SUM(CASE WHEN allowed = 1 THEN 1 ELSE 0 END) as allowed_count,
        SUM(CASE WHEN allowed = 0 THEN 1 ELSE 0 END) as denied_count
      FROM agent_audit_log
      ${whereClause} timestamp >= datetime('now', '-${days} days')
      GROUP BY operation
      ORDER BY frequency DESC
    `;

    db.all(query, params, (err, rows) => {
      closeDatabase(db);

      if (err) {
        reject(new Error(`Frequency query failed: ${err.message}`));
      } else {
        resolve(rows);
      }
    });
  });
}

module.exports = {
  getAuditLog,
  searchAuditLog,
  getAuditStats,
  getRecentDenials,
  getBudgetSummary,
  cleanupOldLogs,
  getOperationFrequency
};
