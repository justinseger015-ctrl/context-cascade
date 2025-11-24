# Memory MCP Integration Guide

## Overview

The Budget Tracker now integrates with Memory MCP for persistent state across restarts. This guide covers setup, usage, troubleshooting, and migration from in-memory to persistent storage.

**Version**: 2.0.0
**Last Updated**: 2025-11-17
**Memory MCP Namespace**: `agent-reality-map/budgets`

---

## Features

- **Persistent Budget State**: Budget data survives Claude Code restarts
- **Auto-Sync**: Automatic background sync every 5 minutes
- **Graceful Degradation**: Works without Memory MCP (falls back to in-memory)
- **Historical Analytics**: Query budget history and trends over time
- **Low Overhead**: <5ms Memory MCP overhead per operation

---

## Setup

### 1. Verify Memory MCP Installation

Check if Memory MCP is configured:

```bash
claude mcp list
```

Expected output:
```
memory-mcp: npx @modelcontextprotocol/server-memory
```

### 2. Add Memory MCP (if not installed)

```bash
claude mcp add memory-mcp npx @modelcontextprotocol/server-memory
```

### 3. Verify Budget Tracker Configuration

The budget tracker will automatically detect Memory MCP availability:

```javascript
const budgetTracker = require('./hooks/12fa/utils/budget-tracker.js');

// Check if Memory MCP is available
console.log('Memory MCP Available:', budgetTracker._internal.memoryMCPAvailable);
```

### 4. Start Auto-Sync (Optional)

Auto-sync is recommended for production environments:

```javascript
const budgetTracker = require('./hooks/12fa/utils/budget-tracker.js');

// Start auto-sync (every 5 minutes)
budgetTracker.startAutoSync();
```

---

## Memory MCP Tagging Protocol

All Memory MCP writes follow the required tagging protocol with WHO/WHEN/PROJECT/WHY metadata.

### Budget State Schema

```json
{
  "text": "{\"agent_id\":\"coder\",\"role\":\"code-quality\",\"session_tokens_used\":1500,...}",
  "metadata": {
    "agent": {
      "name": "backend-dev",
      "category": "code-quality",
      "capabilities": ["memory-mcp", "claude-flow"]
    },
    "timestamp": {
      "iso": "2025-11-17T12:00:00.000Z",
      "unix": 1700222400,
      "readable": "11/17/2025, 12:00:00 PM"
    },
    "project": "agent-reality-map",
    "intent": {
      "primary": "budget-persistence",
      "description": "Auto-detected from content",
      "task_id": "BUDGET-SAVE-coder"
    },
    "namespace": "agent-reality-map/budgets",
    "key": "coder",
    "_tagged_at": "2025-11-17T12:00:00.000Z",
    "_agent": "backend-dev",
    "_project": "agent-reality-map",
    "_intent": "budget-persistence"
  }
}
```

### Tagging Example

```javascript
const { taggedMemoryStore } = require('./hooks/12fa/memory-mcp-tagging-protocol.js');

// Prepare budget data
const budgetData = {
  agent_id: 'coder',
  role: 'code-quality',
  session_tokens_used: 1500,
  session_token_limit: 10000,
  daily_cost_used: 0.15,
  daily_cost_limit: 5.00,
  last_reset: Date.now(),
  operations_blocked: 0,
  created_at: Date.now(),
  updated_at: Date.now()
};

// Tag for Memory MCP
const tagged = taggedMemoryStore('backend-dev', JSON.stringify(budgetData), {
  project: 'agent-reality-map',
  intent: 'budget-persistence',
  namespace: 'agent-reality-map/budgets',
  key: 'coder',
  task_id: 'BUDGET-SAVE-coder'
});

// Store in Memory MCP (in production)
// await memoryStore(tagged.text, tagged.metadata);
```

---

## Usage

### Initialize Budget with Persistence

```javascript
const budgetTracker = require('./hooks/12fa/utils/budget-tracker.js');

// Initialize budget - automatically loads from Memory MCP if available
const budget = await budgetTracker.initializeBudget(
  'coder',           // agentId
  'code-quality',    // role
  10000,             // sessionTokenLimit
  5.00               // dailyCostLimit (USD)
);

console.log('Budget initialized:', budget);
// If found in Memory MCP: "Restored budget for coder from Memory MCP"
```

### Manual Save/Load

```javascript
// Save current budget state
const saved = await budgetTracker.saveBudgetState('coder');
console.log('Budget saved:', saved);

// Load budget from Memory MCP
const loaded = await budgetTracker.loadBudgetState('coder');
console.log('Budget loaded:', loaded);
```

### Sync All Budgets

```javascript
// Manually sync all active budgets to Memory MCP
const stats = await budgetTracker.syncBudgetState();
console.log('Sync stats:', stats);
// Output: { synced: 5, failed: 0, total: 5, duration_ms: 42 }
```

### Auto-Sync Management

```javascript
// Start auto-sync (every 5 minutes)
budgetTracker.startAutoSync();

// Stop auto-sync and save all budgets
await budgetTracker.stopAutoSync();
```

### Check Persistence Status

```javascript
const status = budgetTracker.getBudgetStatus('coder');
console.log('Persistence:', status.persistence);
// Output:
// {
//   memory_mcp_available: true,
//   auto_sync_enabled: true
// }
```

---

## Historical Analytics

### Get Budget History

```javascript
const analytics = require('./hooks/12fa/utils/budget-analytics.js');

// Get last 7 days of budget history for an agent
const history = await analytics.getBudgetHistory('coder', 7);
console.log('Budget history:', history);
```

### Budget Trends Analysis

```javascript
// Analyze spending patterns across all agents
const trends = await analytics.getBudgetTrends();
console.log('Trends:', trends);
// Output:
// {
//   period: 'last_7_days',
//   trends: {
//     total_cost: 15.42,
//     cost_trend: 'increasing',
//     peak_usage_hour: 14,
//     peak_usage_day: 'Wednesday'
//   },
//   top_spenders: [...],
//   recommendations: [...]
// }
```

### Budget Alerts

```javascript
// Get agents approaching budget limits (>80% utilization)
const alerts = await analytics.getBudgetAlerts(80);
console.log('Alerts:', alerts);
// Output:
// {
//   threshold_pct: 80,
//   alerts: [
//     { agent_id: 'coder', utilization: 95, alert_level: 'critical' },
//     { agent_id: 'tester', utilization: 82, alert_level: 'warning' }
//   ]
// }
```

### Comprehensive Report

```javascript
// Generate full budget report
const report = await analytics.generateBudgetReport({
  days: 7,
  includeAgentDetails: true,
  includeRecommendations: true
});

console.log('Budget Report:', report);
```

---

## Graceful Degradation

The budget tracker works seamlessly with or without Memory MCP:

### Without Memory MCP

```javascript
// Memory MCP not available - falls back to in-memory
const budget = await budgetTracker.initializeBudget('coder', 'code-quality', 10000, 5.00);

// Operations work normally
const check = budgetTracker.checkBudget('coder', 1000);
const status = budgetTracker.getBudgetStatus('coder');

// But state is lost on restart
console.log('Memory MCP Available:', budgetTracker._internal.memoryMCPAvailable);
// Output: false
```

### With Memory MCP

```javascript
// Memory MCP available - full persistence
const budget = await budgetTracker.initializeBudget('coder', 'code-quality', 10000, 5.00);

// State persists across restarts
// Auto-sync keeps Memory MCP updated every 5 minutes
budgetTracker.startAutoSync();
```

---

## Migration Guide

### From In-Memory to Persistent

**Step 1**: Verify Memory MCP is installed

```bash
claude mcp list
```

**Step 2**: Update budget tracker initialization

```javascript
// OLD: In-memory only
const budget = budgetTracker.initializeBudget('coder', 'code-quality', 10000, 5.00);

// NEW: With persistence (async)
const budget = await budgetTracker.initializeBudget('coder', 'code-quality', 10000, 5.00);
```

**Step 3**: Start auto-sync

```javascript
budgetTracker.startAutoSync();
```

**Step 4**: Verify persistence

```bash
# Restart Claude Code
# Check if budgets restored:
const status = budgetTracker.getBudgetStatus('coder');
console.log('Session tokens used:', status.session.tokens_used);
# Should show previous values (not 0)
```

---

## Troubleshooting

### Memory MCP Not Available

**Symptom**: `Memory MCP not available - using in-memory mode only`

**Solution**:
```bash
# Check if Memory MCP is installed
claude mcp list

# If not listed, add it
claude mcp add memory-mcp npx @modelcontextprotocol/server-memory

# Verify configuration
cat ~/.claude/claude_desktop_config.json
```

### Auto-Sync Not Running

**Symptom**: Budgets not persisting after 5 minutes

**Solution**:
```javascript
// Check if auto-sync is running
const status = budgetTracker.getBudgetStatus('coder');
console.log('Auto-sync enabled:', status.persistence.auto_sync_enabled);

// Start auto-sync if not running
budgetTracker.startAutoSync();
```

### High Memory MCP Overhead

**Symptom**: Operations taking >20ms

**Solution**:
```javascript
// Check performance metrics
const metrics = budgetTracker.getPerformanceMetrics();
console.log('Avg operation time:', metrics.avg_ms);
console.log('P95 operation time:', metrics.p95_ms);

// If >20ms, verify Memory MCP is healthy
// Consider disabling auto-sync if needed
await budgetTracker.stopAutoSync();
```

### Budget Not Restored After Restart

**Symptom**: Budget resets to 0 after Claude Code restart

**Check**:
```javascript
// Verify Memory MCP availability
console.log('Memory MCP Available:', budgetTracker._internal.memoryMCPAvailable);

// Check if budget was saved
const saved = await budgetTracker.saveBudgetState('coder');
console.log('Save successful:', saved);

// Try manual load
const loaded = await budgetTracker.loadBudgetState('coder');
console.log('Loaded budget:', loaded);
```

---

## Performance Benchmarks

**Target**: <5ms Memory MCP overhead, <20ms total per operation

### Expected Performance

| Operation | Without Memory MCP | With Memory MCP | Overhead |
|-----------|-------------------|-----------------|----------|
| `initializeBudget()` | 2-5ms | 5-10ms | +3-5ms |
| `checkBudget()` | 1-3ms | 1-3ms | 0ms (read-only) |
| `deductBudget()` | 2-4ms | 5-8ms | +3-4ms |
| `getBudgetStatus()` | 1-2ms | 1-2ms | 0ms (read-only) |
| `saveBudgetState()` | N/A | 3-5ms | N/A |
| `syncBudgetState()` (all) | N/A | 15-30ms | N/A |

### Monitoring Performance

```javascript
const metrics = budgetTracker.getPerformanceMetrics();
console.log('Performance Metrics:', metrics);
// Output:
// {
//   sample_count: 100,
//   avg_ms: 3.2,
//   min_ms: 1.1,
//   max_ms: 8.4,
//   p95_ms: 6.7
// }
```

---

## Best Practices

1. **Always start auto-sync in production**
   ```javascript
   budgetTracker.startAutoSync();
   ```

2. **Use async/await for initialization**
   ```javascript
   const budget = await budgetTracker.initializeBudget(...);
   ```

3. **Monitor performance regularly**
   ```javascript
   const metrics = budgetTracker.getPerformanceMetrics();
   if (metrics.p95_ms > 20) {
     console.warn('Budget operations exceeding 20ms target');
   }
   ```

4. **Check Memory MCP availability before critical operations**
   ```javascript
   if (budgetTracker._internal.memoryMCPAvailable) {
     await budgetTracker.saveBudgetState(agentId);
   }
   ```

5. **Handle shutdown gracefully**
   ```javascript
   process.on('SIGTERM', async () => {
     await budgetTracker.stopAutoSync();
     process.exit(0);
   });
   ```

---

## API Reference

### Budget Tracker

- `initializeBudget(agentId, role, sessionTokenLimit, dailyCostLimit)` - Initialize with Memory MCP restore
- `saveBudgetState(agentId)` - Save to Memory MCP
- `loadBudgetState(agentId)` - Load from Memory MCP
- `syncBudgetState()` - Sync all budgets
- `startAutoSync()` - Enable auto-sync (5 min interval)
- `stopAutoSync()` - Disable auto-sync and save all

### Budget Analytics

- `getBudgetHistory(agentId, days)` - Get historical data
- `getBudgetTrends()` - Analyze spending patterns
- `getBudgetAlerts(threshold)` - Get agents near limits
- `generateBudgetReport(options)` - Comprehensive report
- `exportBudgetData(options)` - Export for analysis
- `compareBudgetPeriods(options)` - Period comparison

---

## Support

**Memory MCP Issues**: Check `~/.claude/claude_desktop_config.json`
**Budget Tracker Issues**: Check logs for `[Budget Tracker]` messages
**Analytics Issues**: Verify Memory MCP has historical data

**Contact**: Create issue at https://github.com/ruvnet/claude-flow/issues
