-- Agent Reality Map Audit Log Schema
-- Database: SQLite
-- Purpose: Track all agent operations for security and compliance
-- Retention: 90 days (auto-cleanup via scheduled task)

-- Drop existing table if exists (for clean reinstall)
DROP TABLE IF EXISTS agent_audit_log;

-- Main audit log table
CREATE TABLE agent_audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  agent_id TEXT NOT NULL,
  agent_role TEXT NOT NULL,
  operation TEXT NOT NULL,
  tool_name TEXT,
  file_path TEXT,
  api_name TEXT,
  allowed BOOLEAN NOT NULL,
  denied_reason TEXT,
  budget_impact REAL DEFAULT 0.0,
  session_id TEXT,
  metadata TEXT,  -- JSON stored as TEXT in SQLite
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Performance indexes
CREATE INDEX idx_agent_id ON agent_audit_log(agent_id);
CREATE INDEX idx_timestamp ON agent_audit_log(timestamp);
CREATE INDEX idx_operation ON agent_audit_log(operation);
CREATE INDEX idx_allowed ON agent_audit_log(allowed);
CREATE INDEX idx_session_id ON agent_audit_log(session_id);

-- Composite index for common queries
CREATE INDEX idx_agent_timestamp ON agent_audit_log(agent_id, timestamp DESC);

-- View for denied operations (security monitoring)
CREATE VIEW denied_operations AS
SELECT
  id,
  timestamp,
  agent_id,
  agent_role,
  operation,
  tool_name,
  file_path,
  denied_reason
FROM agent_audit_log
WHERE allowed = 0
ORDER BY timestamp DESC;

-- View for budget impact tracking
CREATE VIEW budget_impact_summary AS
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
ORDER BY total_budget_used DESC;

-- View for recent activity (last 24 hours)
CREATE VIEW recent_activity AS
SELECT
  id,
  timestamp,
  agent_id,
  agent_role,
  operation,
  tool_name,
  allowed,
  budget_impact
FROM agent_audit_log
WHERE timestamp >= datetime('now', '-1 day')
ORDER BY timestamp DESC;
