-- Database Performance Optimization - Index Creation
-- Target: Reduce query latency, improve P99 performance
--
-- P4_T8: Database Optimization
--

-- ====================
-- 1. SCHEDULED_TASKS TABLE INDEXES
-- ====================

-- User-scoped queries (most common filter)
-- Used in: GET /api/v1/tasks?user_id=X
CREATE INDEX IF NOT EXISTS idx_tasks_user_id
ON scheduled_tasks(user_id);

-- Temporal queries (sorting, filtering by creation date)
-- Used in: GET /api/v1/tasks?sort=created_at DESC
CREATE INDEX IF NOT EXISTS idx_tasks_created_at
ON scheduled_tasks(created_at DESC);

-- Status filtering (active/inactive tasks)
-- Used in: GET /api/v1/tasks?status=enabled
CREATE INDEX IF NOT EXISTS idx_tasks_status
ON scheduled_tasks(status);

-- Composite index for common query pattern: user + status
-- Used in: GET /api/v1/tasks?user_id=X&status=enabled
-- This avoids index intersection, provides better performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_status
ON scheduled_tasks(user_id, status);

-- Composite index for user + temporal sorting
-- Used in: GET /api/v1/tasks?user_id=X ORDER BY created_at DESC
CREATE INDEX IF NOT EXISTS idx_tasks_user_created
ON scheduled_tasks(user_id, created_at DESC);

-- Next execution time (for scheduler queries)
-- Used in: Scheduler fetching due tasks
CREATE INDEX IF NOT EXISTS idx_tasks_next_execution
ON scheduled_tasks(next_execution_time)
WHERE enabled = true;  -- Partial index (only enabled tasks)


-- ====================
-- 2. PROJECTS TABLE INDEXES
-- ====================

-- User-scoped queries
CREATE INDEX IF NOT EXISTS idx_projects_user_id
ON projects(user_id);

-- Status filtering
CREATE INDEX IF NOT EXISTS idx_projects_status
ON projects(status);

-- Composite index for user + status
CREATE INDEX IF NOT EXISTS idx_projects_user_status
ON projects(user_id, status);

-- Temporal sorting
CREATE INDEX IF NOT EXISTS idx_projects_created_at
ON projects(created_at DESC);


-- ====================
-- 3. AGENTS TABLE INDEXES
-- ====================

-- Agent type filtering
CREATE INDEX IF NOT EXISTS idx_agents_type
ON agents(agent_type);

-- Status filtering
CREATE INDEX IF NOT EXISTS idx_agents_status
ON agents(status);

-- User-scoped queries
CREATE INDEX IF NOT EXISTS idx_agents_user_id
ON agents(user_id);

-- Composite index for type + status (common query)
CREATE INDEX IF NOT EXISTS idx_agents_type_status
ON agents(agent_type, status);


-- ====================
-- 4. EXECUTION_RESULTS TABLE INDEXES
-- ====================

-- Task relationship (foreign key)
CREATE INDEX IF NOT EXISTS idx_results_task_id
ON execution_results(task_id);

-- Status filtering
CREATE INDEX IF NOT EXISTS idx_results_status
ON execution_results(status);

-- Temporal queries (recent executions)
CREATE INDEX IF NOT EXISTS idx_results_started_at
ON execution_results(started_at DESC);

-- Composite index for task + temporal sorting
CREATE INDEX IF NOT EXISTS idx_results_task_started
ON execution_results(task_id, started_at DESC);


-- ====================
-- 5. AUDIT_LOGS TABLE INDEXES
-- ====================

-- User activity tracking
CREATE INDEX IF NOT EXISTS idx_audit_user_id
ON audit_logs(user_id);

-- Action filtering
CREATE INDEX IF NOT EXISTS idx_audit_action
ON audit_logs(action);

-- Temporal queries (recent activity)
CREATE INDEX IF NOT EXISTS idx_audit_timestamp
ON audit_logs(timestamp DESC);

-- Composite index for user + temporal
CREATE INDEX IF NOT EXISTS idx_audit_user_timestamp
ON audit_logs(user_id, timestamp DESC);

-- Resource-specific queries
CREATE INDEX IF NOT EXISTS idx_audit_resource_type
ON audit_logs(resource_type);


-- ====================
-- 6. ANALYZE TABLES
-- ====================
-- Update table statistics for query planner

ANALYZE scheduled_tasks;
ANALYZE projects;
ANALYZE agents;
ANALYZE execution_results;
ANALYZE audit_logs;


-- ====================
-- 7. INDEX USAGE MONITORING
-- ====================
-- Query to check index usage statistics

-- Run this query periodically to verify indexes are being used:
/*
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
*/

-- Identify unused indexes (candidates for removal):
/*
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
  AND indexrelname NOT LIKE 'pg_toast%';
*/


-- ====================
-- 8. QUERY PERFORMANCE ANALYSIS
-- ====================
-- Use EXPLAIN ANALYZE to verify indexes are used

-- Example: Verify user + status query uses composite index
/*
EXPLAIN ANALYZE
SELECT * FROM scheduled_tasks
WHERE user_id = 1 AND status = 'enabled'
ORDER BY created_at DESC
LIMIT 20;

Expected: "Index Scan using idx_tasks_user_status"
*/


-- ====================
-- 9. MAINTENANCE RECOMMENDATIONS
-- ====================

-- Run VACUUM ANALYZE weekly to maintain index health
-- Cron job: 0 2 * * 0 (Sundays at 2 AM)
/*
VACUUM ANALYZE scheduled_tasks;
VACUUM ANALYZE projects;
VACUUM ANALYZE agents;
VACUUM ANALYZE execution_results;
VACUUM ANALYZE audit_logs;
*/

-- Monitor bloat and rebuild indexes if necessary
-- Check index bloat:
/*
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
  pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename)) as index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
*/


-- ====================
-- 10. PERFORMANCE TARGETS
-- ====================
-- After index creation, query performance should meet:
--
-- - GET /tasks (user-scoped, filtered): P99 < 50ms
-- - GET /tasks (paginated, sorted): P99 < 80ms
-- - POST /tasks (with index updates): P99 < 100ms
-- - GET /projects: P99 < 40ms
-- - GET /agents: P99 < 40ms
--
-- Monitor using k6 load tests and PostgreSQL query logs.
