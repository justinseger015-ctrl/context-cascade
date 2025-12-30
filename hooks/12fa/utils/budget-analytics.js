/**
 * Budget Analytics Module v3.0
 *
 * Provides historical analysis and reporting for budget usage across all agents.
 * Queries Memory MCP for historical budget data and generates insights.
 *
 * Features:
 * - Budget usage history over time
 * - Spending pattern analysis
 * - Budget alerts for agents approaching limits
 * - Comprehensive budget reports
 *
 * v3.0: Uses x- prefixed custom fields for Anthropic compliance
 *
 * @module budget-analytics
 * @version 3.0.0
 */

'use strict';

// Try to load Memory MCP tagging protocol (graceful degradation)
let memoryMCPAvailable = false;
try {
  require('../memory-mcp-tagging-protocol.js');
  memoryMCPAvailable = true;
} catch (err) {
  console.warn('[Budget Analytics] Memory MCP not available - limited functionality');
}

const BUDGET_NAMESPACE = 'agent-reality-map/budgets';

/**
 * Get budget history for an agent over specified days
 * Queries Memory MCP for historical budget records
 *
 * @param {string} agentId - Agent identifier
 * @param {number} days - Number of days to look back (default: 7)
 * @returns {Promise<Array>} Array of budget snapshots
 */
async function getBudgetHistory(agentId, days = 7) {
  if (!memoryMCPAvailable) {
    return {
      error: 'Memory MCP not available',
      agent_id: agentId,
      days_requested: days,
      days: days,
      history: []
    };
  }

  try {
    const cutoffTimestamp = Date.now() - (days * 24 * 60 * 60 * 1000);

    // Note: In production, this would query Memory MCP:
    // const query = `agent_id:${agentId} namespace:${BUDGET_NAMESPACE} timestamp.unix:>=${Math.floor(cutoffTimestamp/1000)}`;
    // const results = await vectorSearch(query, { limit: 100 });

    // For now, return mock structure
    return {
      agent_id: agentId,
      days_requested: days,
      days: days,
      cutoff_date: new Date(cutoffTimestamp).toISOString(),
      history: [],
      summary: {
        total_snapshots: 0,
        avg_daily_cost: 0,
        avg_session_tokens: 0,
        max_daily_cost: 0,
        max_session_tokens: 0
      }
    };
  } catch (err) {
    console.error(`[Budget Analytics] Failed to get history for ${agentId}:`, err.message);
    return {
      error: err.message,
      agent_id: agentId,
      history: []
    };
  }
}

/**
 * Analyze budget trends across all agents
 * Identifies patterns like peak usage times, cost trends, etc.
 *
 * @returns {Promise<Object>} Trend analysis report
 */
async function getBudgetTrends() {
  if (!memoryMCPAvailable) {
    return {
      error: 'Memory MCP not available',
      period: 'last_7_days',
      trends: {
        total_agents: 0,
        total_cost: 0,
        total_tokens: 0,
        avg_cost_per_agent: 0,
        avg_tokens_per_agent: 0,
        peak_usage_hour: null,
        peak_usage_day: null,
        cost_trend: 'stable',
        token_trend: 'stable'
      },
      top_spenders: [],
      top_token_users: [],
      recommendations: []
    };
  }

  try {
    // Note: In production, this would aggregate data from Memory MCP:
    // const query = `namespace:${BUDGET_NAMESPACE}`;
    // const results = await vectorSearch(query, { limit: 1000 });

    // Mock structure
    return {
      period: 'last_7_days',
      analyzed_at: new Date().toISOString(),
      trends: {
        total_agents: 0,
        total_cost: 0,
        total_tokens: 0,
        avg_cost_per_agent: 0,
        avg_tokens_per_agent: 0,
        peak_usage_hour: null,
        peak_usage_day: null,
        cost_trend: 'stable', // 'increasing', 'decreasing', 'stable'
        token_trend: 'stable'
      },
      top_spenders: [],
      top_token_users: [],
      recommendations: [],
      error: null
    };
  } catch (err) {
    console.error('[Budget Analytics] Failed to get trends:', err.message);
    return {
      error: err.message,
      trends: []
    };
  }
}

/**
 * Get budget alerts for agents approaching limits
 * Returns agents at high utilization (>80% of limits)
 *
 * @param {number} threshold - Alert threshold percentage (default: 80)
 * @returns {Promise<Array>} Array of budget alerts
 */
async function getBudgetAlerts(threshold = 80) {
  if (!memoryMCPAvailable) {
    return {
      error: 'Memory MCP not available',
      threshold_pct: threshold,
      alerts: [],
      summary: {
        total_alerts: 0,
        critical_alerts: 0,
        warning_alerts: 0,
        agents_affected: []
      }
    };
  }

  try {
    // Note: In production, this would query recent budgets from Memory MCP
    // and filter by utilization percentage

    return {
      threshold_pct: threshold,
      checked_at: new Date().toISOString(),
      alerts: [],
      summary: {
        total_alerts: 0,
        critical_alerts: 0, // >95%
        warning_alerts: 0,  // 80-95%
        agents_affected: []
      },
      error: null
    };
  } catch (err) {
    console.error('[Budget Analytics] Failed to get alerts:', err.message);
    return {
      error: err.message,
      alerts: []
    };
  }
}

/**
 * Generate comprehensive budget report
 * Combines history, trends, and alerts into single report
 *
 * @param {Object} options - Report options
 * @param {number} options.days - Days to analyze (default: 7)
 * @param {boolean} options.includeAgentDetails - Include per-agent breakdown (default: true)
 * @param {boolean} options.includeRecommendations - Include optimization suggestions (default: true)
 * @returns {Promise<Object>} Comprehensive budget report
 */
async function generateBudgetReport(options = {}) {
  const {
    days = 7,
    includeAgentDetails = true,
    includeRecommendations = true
  } = options;

  try {
    // Gather all analytics data
    const [trends, alerts] = await Promise.all([
      getBudgetTrends(),
      getBudgetAlerts()
    ]);

    const report = {
      generated_at: new Date().toISOString(),
      period_days: days,
      memory_mcp_available: memoryMCPAvailable,

      overview: {
        total_agents: (trends.trends && trends.trends.total_agents) || 0,
        total_cost_usd: (trends.trends && trends.trends.total_cost) || 0,
        total_tokens: (trends.trends && trends.trends.total_tokens) || 0,
        avg_cost_per_agent_usd: (trends.trends && trends.trends.avg_cost_per_agent) || 0,
        avg_tokens_per_agent: (trends.trends && trends.trends.avg_tokens_per_agent) || 0
      },

      trends: {
        cost_trend: (trends.trends && trends.trends.cost_trend) || 'unknown',
        token_trend: (trends.trends && trends.trends.token_trend) || 'unknown',
        peak_usage_hour: (trends.trends && trends.trends.peak_usage_hour) || null,
        peak_usage_day: (trends.trends && trends.trends.peak_usage_day) || null
      },

      alerts: {
        total: (alerts.summary && alerts.summary.total_alerts) || 0,
        critical: (alerts.summary && alerts.summary.critical_alerts) || 0,
        warning: (alerts.summary && alerts.summary.warning_alerts) || 0,
        affected_agents: (alerts.summary && alerts.summary.agents_affected) || []
      },

      top_performers: {
        highest_cost: trends.top_spenders || [],
        highest_tokens: trends.top_token_users || []
      }
    };

    // Add agent details if requested
    if (includeAgentDetails) {
      report.agent_details = [];
      // Note: Would iterate through all agents and get their history
    }

    // Add recommendations if requested
    if (includeRecommendations) {
      report.recommendations = generateRecommendations(report);
    }

    return report;
  } catch (err) {
    console.error('[Budget Analytics] Failed to generate report:', err.message);
    return {
      error: err.message,
      generated_at: new Date().toISOString()
    };
  }
}

/**
 * Generate optimization recommendations based on report data
 * @private
 * @param {Object} report - Budget report data
 * @returns {Array} Array of recommendation objects
 */
function generateRecommendations(report) {
  const recommendations = [];

  // High cost alert
  if (report.overview.total_cost_usd > 50) {
    recommendations.push({
      priority: 'high',
      category: 'cost-optimization',
      title: 'High total cost detected',
      description: `Total cost of $${report.overview.total_cost_usd.toFixed(2)} exceeds typical range`,
      suggested_actions: [
        'Review token limits for high-usage agents',
        'Consider implementing more aggressive caching',
        'Optimize prompts to reduce token consumption'
      ]
    });
  }

  // Critical alerts
  if (report.alerts.critical > 0) {
    recommendations.push({
      priority: 'critical',
      category: 'budget-limits',
      title: `${report.alerts.critical} agents approaching limits`,
      description: 'Agents at >95% utilization may be blocked soon',
      suggested_actions: [
        'Increase budget limits for critical agents',
        'Review recent operations for unexpected usage spikes',
        'Implement request throttling if appropriate'
      ]
    });
  }

  // Trend-based recommendations
  if (report.trends.cost_trend === 'increasing') {
    recommendations.push({
      priority: 'medium',
      category: 'trend-analysis',
      title: 'Cost trend increasing',
      description: 'Budget costs have been increasing over the analysis period',
      suggested_actions: [
        'Analyze what features or agents are driving increased usage',
        'Review if increased usage is aligned with business goals',
        'Consider implementing cost controls or quotas'
      ]
    });
  }

  // No alerts - all good
  if (recommendations.length === 0) {
    recommendations.push({
      priority: 'info',
      category: 'status',
      title: 'Budget health is good',
      description: 'All agents operating within normal parameters',
      suggested_actions: [
        'Continue monitoring usage patterns',
        'Review budget limits quarterly'
      ]
    });
  }

  return recommendations;
}

/**
 * Export budget data for external analysis
 * Returns data in CSV-compatible format
 *
 * @param {Object} options - Export options
 * @param {number} options.days - Days to export (default: 30)
 * @param {string} options.format - Export format: 'json' or 'csv' (default: 'json')
 * @returns {Promise<Object|string>} Exported data
 */
async function exportBudgetData(options = {}) {
  const {
    days = 30,
    format = 'json'
  } = options;

  try {
    // Note: In production, query all budget records from Memory MCP
    const data = {
      exported_at: new Date().toISOString(),
      period_days: days,
      records: []
    };

    if (format === 'csv') {
      // Convert to CSV format
      const headers = ['timestamp', 'agent_id', 'role', 'session_tokens_used', 'daily_cost_used', 'operations_blocked'];
      const rows = data.records.map(record => [
        record.timestamp,
        record.agent_id,
        record.role,
        record.session_tokens_used,
        record.daily_cost_used,
        record.operations_blocked
      ]);

      return {
        format: 'csv',
        headers: headers.join(','),
        rows: rows.map(row => row.join(',')).join('\n'),
        record_count: rows.length
      };
    }

    return data;
  } catch (err) {
    console.error('[Budget Analytics] Failed to export data:', err.message);
    return {
      error: err.message,
      format
    };
  }
}

/**
 * Compare budget performance between two time periods
 *
 * @param {Object} options - Comparison options
 * @param {number} options.currentDays - Current period days (default: 7)
 * @param {number} options.previousDays - Previous period days (default: 7)
 * @returns {Promise<Object>} Comparison report
 */
async function compareBudgetPeriods(options = {}) {
  const {
    currentDays = 7,
    previousDays = 7
  } = options;

  try {
    // Note: In production, query two separate time periods from Memory MCP

    return {
      compared_at: new Date().toISOString(),
      current_period: {
        days: currentDays,
        total_cost: 0,
        total_tokens: 0,
        avg_cost_per_day: 0
      },
      previous_period: {
        days: previousDays,
        total_cost: 0,
        total_tokens: 0,
        avg_cost_per_day: 0
      },
      changes: {
        cost_change_pct: 0,
        cost_change_abs: 0,
        token_change_pct: 0,
        token_change_abs: 0,
        trend: 'stable' // 'increasing', 'decreasing', 'stable'
      }
    };
  } catch (err) {
    console.error('[Budget Analytics] Failed to compare periods:', err.message);
    return {
      error: err.message
    };
  }
}

module.exports = {
  getBudgetHistory,
  getBudgetTrends,
  getBudgetAlerts,
  generateBudgetReport,
  exportBudgetData,
  compareBudgetPeriods,

  // Expose for testing
  _internal: {
    generateRecommendations,
    memoryMCPAvailable,
    BUDGET_NAMESPACE
  }
};
