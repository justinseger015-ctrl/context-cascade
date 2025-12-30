/**
 * Saturation Monitor v1.0
 *
 * Tracks eval harness saturation and triggers expansion research
 * when the system consistently hits ceiling performance.
 *
 * Key Insight: A frozen eval harness that's too easy provides false confidence.
 * When saturation is consistent, the harness must become MORE rigorous (one-way ratchet).
 *
 * @version 1.0.0
 * @see docs/SATURATION-DETECTION-ALGORITHM.md
 */

const fs = require('fs');
const path = require('path');

// Import Memory MCP tagging protocol
let taggedMemoryStore, memoryMcpAvailable;
try {
  const taggingProtocol = require('./memory-mcp-tagging-protocol.js');
  taggedMemoryStore = taggingProtocol.taggedMemoryStore;
  memoryMcpAvailable = true;
} catch (err) {
  memoryMcpAvailable = false;
  console.error('[SaturationMonitor] Memory MCP not available - using file-only storage');
}

// Configuration
const STATE_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.claude', 'eval-harness');
const SATURATION_DIR = path.join(STATE_DIR, 'saturation');
const CYCLES_DIR = path.join(SATURATION_DIR, 'cycles');
const EXPANSIONS_DIR = path.join(SATURATION_DIR, 'expansions');
const AGGREGATE_FILE = path.join(SATURATION_DIR, 'aggregate.json');

// Saturation thresholds
const SATURATION_WEIGHTS = {
  benchmark_ceiling_rate: 0.30,
  regression_pass_rate: 0.25,
  improvement_delta_trend: 0.20,
  proposal_pass_rate: 0.15,
  auditor_unanimous_rate: 0.10
};

const SATURATION_LEVELS = {
  NORMAL: { min: 0.0, max: 0.5 },
  ELEVATED: { min: 0.5, max: 0.7 },
  HIGH: { min: 0.7, max: 0.85 },
  CRITICAL: { min: 0.85, max: 1.0 }
};

const CONSISTENCY_THRESHOLDS = {
  consecutive_high_for_research: 10,
  consecutive_critical_for_urgent: 5,
  rolling_avg_high_threshold: 0.70,
  minimum_cycles_for_detection: 10,
  window_size: 20
};

/**
 * Saturation Monitor Class
 */
class SaturationMonitor {
  constructor() {
    this.namespace = 'eval-harness/saturation';
    this.ensureDirectories();
  }

  ensureDirectories() {
    [STATE_DIR, SATURATION_DIR, CYCLES_DIR, EXPANSIONS_DIR].forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      }
    });
  }

  log(message) {
    console.error(`[SaturationMonitor] ${message}`);
  }

  /**
   * Compute saturation score from metrics
   * @param {Object} metrics - Cycle metrics
   * @returns {number} Saturation score [0.0, 1.0]
   */
  computeSaturationScore(metrics) {
    const normalized = {
      benchmark_ceiling_rate: Math.min(1.0, (metrics.benchmark_ceiling_rate || 0) / 0.80),
      regression_pass_rate: metrics.regression_pass_rate === 1.0 ? 1.0 : 0.5,
      improvement_delta_trend: this.computeTrendScore(metrics.delta_history || []),
      proposal_pass_rate: Math.min(1.0, (metrics.proposal_pass_rate || 0) / 0.85),
      auditor_unanimous_rate: Math.min(1.0, (metrics.auditor_unanimous_rate || 0) / 0.90)
    };

    let score = 0;
    for (const [key, weight] of Object.entries(SATURATION_WEIGHTS)) {
      score += (normalized[key] || 0) * weight;
    }

    return Math.min(1.0, Math.max(0.0, score));
  }

  /**
   * Compute trend score from delta history
   * @param {Array} deltaHistory - Array of improvement deltas
   * @returns {number} Trend score [0.0, 1.0] where 1.0 = declining (saturated)
   */
  computeTrendScore(deltaHistory) {
    if (deltaHistory.length < 5) {
      return 0.0;
    }

    // Simple linear regression slope
    const n = deltaHistory.length;
    const x = Array.from({ length: n }, (_, i) => i);
    const y = deltaHistory;

    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((acc, xi, i) => acc + xi * y[i], 0);
    const sumX2 = x.reduce((acc, xi) => acc + xi * xi, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);

    // Negative slope = declining deltas = saturation
    if (slope < -0.01) {
      return Math.min(1.0, Math.abs(slope) * 10);
    }
    return 0.0;
  }

  /**
   * Get saturation level from score
   * @param {number} score - Saturation score
   * @returns {string} Level: NORMAL, ELEVATED, HIGH, CRITICAL
   */
  getLevel(score) {
    for (const [level, range] of Object.entries(SATURATION_LEVELS)) {
      if (score >= range.min && score < range.max) {
        return level;
      }
    }
    return 'CRITICAL'; // >= 0.85
  }

  /**
   * Record cycle metrics and check for saturation
   * @param {string} cycleId - Cycle identifier
   * @param {Object} metrics - Cycle metrics
   * @returns {Object} Snapshot and consistency check result
   */
  async recordCycle(cycleId, metrics) {
    const saturationScore = this.computeSaturationScore(metrics);
    const saturationLevel = this.getLevel(saturationScore);

    const snapshot = {
      cycle_id: cycleId,
      timestamp: new Date().toISOString(),
      metrics,
      saturation_score: saturationScore,
      saturation_level: saturationLevel,
      'x-schema-version': '1.0'
    };

    // Save to file
    const cycleFile = path.join(CYCLES_DIR, `${cycleId}.json`);
    fs.writeFileSync(cycleFile, JSON.stringify(snapshot, null, 2), { mode: 0o600 });

    // Save to Memory MCP if available
    if (memoryMcpAvailable) {
      try {
        await taggedMemoryStore('saturation-monitor', JSON.stringify(snapshot), {
          project: 'context-cascade',
          'x-intent': 'saturation_tracking',
          'x-namespace': `${this.namespace}/cycles/${cycleId}`,
          'x-level': saturationLevel
        });
      } catch (err) {
        this.log(`Memory MCP store failed: ${err.message}`);
      }
    }

    // Update aggregate
    const aggregate = await this.updateAggregate(snapshot);

    // Check consistency
    const consistency = this.checkConsistency(aggregate);

    this.log(`Cycle ${cycleId}: score=${saturationScore.toFixed(2)}, level=${saturationLevel}`);

    if (consistency.action === 'TRIGGER_EXPANSION_RESEARCH') {
      const { expansionId, researchPrompt } = await this.triggerExpansionResearch(consistency, aggregate);
      return { snapshot, consistency, expansionId, researchPrompt };
    }

    return { snapshot, consistency };
  }

  /**
   * Load aggregate from file
   * @returns {Object|null} Aggregate data
   */
  loadAggregate() {
    if (fs.existsSync(AGGREGATE_FILE)) {
      try {
        return JSON.parse(fs.readFileSync(AGGREGATE_FILE, 'utf8'));
      } catch (err) {
        this.log(`Error loading aggregate: ${err.message}`);
      }
    }
    return null;
  }

  /**
   * Create empty aggregate
   * @returns {Object} Empty aggregate structure
   */
  createEmptyAggregate() {
    return {
      window_size: CONSISTENCY_THRESHOLDS.window_size,
      cycles_tracked: 0,
      oldest_cycle: null,
      newest_cycle: null,
      rolling_metrics: {
        avg_saturation_score: 0,
        saturation_trend: 'stable',
        consecutive_high_count: 0,
        consecutive_critical_count: 0
      },
      history: [],
      last_updated: null,
      'x-schema-version': '1.0'
    };
  }

  /**
   * Update aggregate with new cycle snapshot
   * @param {Object} snapshot - Cycle snapshot
   * @returns {Object} Updated aggregate
   */
  async updateAggregate(snapshot) {
    let aggregate = this.loadAggregate() || this.createEmptyAggregate();

    // Add to history
    aggregate.history.push({
      cycle_id: snapshot.cycle_id,
      score: snapshot.saturation_score,
      level: snapshot.saturation_level
    });

    // Maintain window size
    while (aggregate.history.length > aggregate.window_size) {
      aggregate.history.shift();
    }

    // Update metadata
    aggregate.cycles_tracked = aggregate.history.length;
    aggregate.newest_cycle = snapshot.cycle_id;
    aggregate.oldest_cycle = aggregate.history[0].cycle_id;
    aggregate.last_updated = new Date().toISOString();

    // Compute rolling metrics
    aggregate.rolling_metrics = this.computeRollingMetrics(aggregate.history);

    // Save to file
    fs.writeFileSync(AGGREGATE_FILE, JSON.stringify(aggregate, null, 2), { mode: 0o600 });

    // Save to Memory MCP if available
    if (memoryMcpAvailable) {
      try {
        await taggedMemoryStore('saturation-monitor', JSON.stringify(aggregate), {
          project: 'context-cascade',
          'x-intent': 'saturation_aggregate',
          'x-namespace': `${this.namespace}/aggregate`
        });
      } catch (err) {
        this.log(`Memory MCP aggregate store failed: ${err.message}`);
      }
    }

    return aggregate;
  }

  /**
   * Compute rolling metrics from history
   * @param {Array} history - Array of {cycle_id, score, level}
   * @returns {Object} Rolling metrics
   */
  computeRollingMetrics(history) {
    if (history.length === 0) {
      return {
        avg_saturation_score: 0,
        saturation_trend: 'stable',
        consecutive_high_count: 0,
        consecutive_critical_count: 0
      };
    }

    const scores = history.map(h => h.score);
    const levels = history.map(h => h.level);

    // Average score
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;

    // Trend (linear regression slope)
    const trend = this.computeTrendScore(scores);
    const trendLabel = trend > 0.3 ? 'increasing' : (trend < -0.3 ? 'decreasing' : 'stable');

    // Consecutive counts (from end)
    let consecutiveHigh = 0;
    let consecutiveCritical = 0;

    for (let i = levels.length - 1; i >= 0; i--) {
      if (levels[i] === 'CRITICAL') {
        consecutiveCritical++;
        consecutiveHigh++;
      } else if (levels[i] === 'HIGH') {
        consecutiveHigh++;
        if (consecutiveCritical > 0 && levels[i] !== 'CRITICAL') {
          // Break critical streak but continue high streak
        }
      } else {
        break;
      }
    }

    return {
      avg_saturation_score: avgScore,
      saturation_trend: trendLabel,
      consecutive_high_count: consecutiveHigh,
      consecutive_critical_count: consecutiveCritical
    };
  }

  /**
   * Check consistency and determine action
   * @param {Object} aggregate - Aggregate data
   * @returns {Object} Consistency check result
   */
  checkConsistency(aggregate) {
    const result = {
      is_consistent: false,
      action: 'CONTINUE',
      reason: null,
      urgency: 'LOW'
    };

    // Not enough data
    if (aggregate.cycles_tracked < CONSISTENCY_THRESHOLDS.minimum_cycles_for_detection) {
      result.reason = `Insufficient data: ${aggregate.cycles_tracked} cycles`;
      return result;
    }

    const rm = aggregate.rolling_metrics;

    // Check consecutive CRITICAL (urgent)
    if (rm.consecutive_critical_count >= CONSISTENCY_THRESHOLDS.consecutive_critical_for_urgent) {
      result.is_consistent = true;
      result.action = 'TRIGGER_EXPANSION_RESEARCH';
      result.reason = `URGENT: ${rm.consecutive_critical_count} consecutive CRITICAL`;
      result.urgency = 'CRITICAL';
      return result;
    }

    // Check consecutive HIGH
    if (rm.consecutive_high_count >= CONSISTENCY_THRESHOLDS.consecutive_high_for_research) {
      result.is_consistent = true;
      result.action = 'TRIGGER_EXPANSION_RESEARCH';
      result.reason = `${rm.consecutive_high_count} consecutive HIGH`;
      result.urgency = 'HIGH';
      return result;
    }

    // Check rolling average with trend
    if (rm.avg_saturation_score >= CONSISTENCY_THRESHOLDS.rolling_avg_high_threshold) {
      if (rm.saturation_trend === 'increasing') {
        result.is_consistent = true;
        result.action = 'FLAG_FOR_REVIEW';
        result.reason = `Rolling avg ${rm.avg_saturation_score.toFixed(2)} with increasing trend`;
        result.urgency = 'MEDIUM';
        return result;
      }
    }

    return result;
  }

  /**
   * Trigger expansion research
   * @param {Object} consistency - Consistency check result
   * @param {Object} aggregate - Aggregate data
   * @returns {Object} Expansion event details
   */
  async triggerExpansionResearch(consistency, aggregate) {
    const expansionId = `exp-${Date.now()}`;

    const expansionEvent = {
      expansion_id: expansionId,
      triggered_at: new Date().toISOString(),
      trigger_reason: consistency.reason,
      saturation_score_at_trigger: aggregate.rolling_metrics.avg_saturation_score,
      research_spawned: {
        task_id: null,
        status: 'pending',
        findings: null
      },
      proposed_expansions: [],
      human_approved: null,
      applied_at: null,
      'x-schema-version': '1.0'
    };

    // Save to file
    const expansionFile = path.join(EXPANSIONS_DIR, `${expansionId}.json`);
    fs.writeFileSync(expansionFile, JSON.stringify(expansionEvent, null, 2), { mode: 0o600 });

    // Save to Memory MCP if available
    if (memoryMcpAvailable) {
      try {
        await taggedMemoryStore('saturation-monitor', JSON.stringify(expansionEvent), {
          project: 'context-cascade',
          'x-intent': 'expansion_trigger',
          'x-namespace': `${this.namespace}/expansions/${expansionId}`,
          'x-urgency': consistency.urgency
        });
      } catch (err) {
        this.log(`Memory MCP expansion store failed: ${err.message}`);
      }
    }

    // Generate research prompt
    const researchPrompt = this.generateResearchPrompt(consistency, aggregate);

    this.log(`EXPANSION RESEARCH TRIGGERED: ${expansionId}`);
    this.log(`Reason: ${consistency.reason}`);
    this.log(`Urgency: ${consistency.urgency}`);

    return { expansionId, researchPrompt, expansionEvent };
  }

  /**
   * Generate research prompt for expansion
   * @param {Object} consistency - Consistency check result
   * @param {Object} aggregate - Aggregate data
   * @returns {string} Research prompt
   */
  generateResearchPrompt(consistency, aggregate) {
    return `
## Eval Harness Expansion Research

### Context
The eval harness has been consistently saturated:
- Saturation Score: ${aggregate.rolling_metrics.avg_saturation_score.toFixed(2)}
- Consecutive HIGH cycles: ${aggregate.rolling_metrics.consecutive_high_count}
- Consecutive CRITICAL cycles: ${aggregate.rolling_metrics.consecutive_critical_count}
- Trigger Reason: ${consistency.reason}
- Urgency: ${consistency.urgency}

### Research Objectives
1. Analyze recent benchmark results - identify ceiling cases
2. Analyze proposal pass/fail patterns - what still fails and why?
3. Identify untested edge cases
4. Propose specific threshold increases
5. Propose new benchmarks (harder, more discriminative)

### Constraints (ONE-WAY RATCHET)
- ONLY propose MORE rigorous changes
- FORBIDDEN: Lowering thresholds, removing tests, weakening gates
- REQUIRED: Human approval before any changes

### Output Format
\`\`\`yaml
expansion_proposals:
  threshold_increases:
    - benchmark: "benchmark-id"
      metric: "metric-name"
      current: 0.70
      proposed: 0.75
      rationale: "Why this increase is justified"

  new_benchmarks:
    - id: "new-benchmark-id"
      name: "Benchmark Name"
      purpose: "What capability it tests"
      tasks: ["task descriptions"]
      expected_difficulty: "harder than existing"

  new_edge_cases:
    - category: "Category"
      description: "Edge case description"
      expected_failure_mode: "What should fail"

  new_regression_tests:
    - id: "new-regression-id"
      name: "Test Name"
      action: "What to test"
      expected: "What should happen"

human_review_required: true
one_way_ratchet_verified: true
\`\`\`
`;
  }

  /**
   * List all expansion events
   * @returns {Array} Expansion events
   */
  listExpansions() {
    const expansions = [];
    if (fs.existsSync(EXPANSIONS_DIR)) {
      const files = fs.readdirSync(EXPANSIONS_DIR);
      for (const file of files) {
        if (file.endsWith('.json')) {
          try {
            const data = JSON.parse(fs.readFileSync(path.join(EXPANSIONS_DIR, file), 'utf8'));
            expansions.push(data);
          } catch (err) {
            // Skip corrupted files
          }
        }
      }
    }
    return expansions.sort((a, b) => new Date(b.triggered_at) - new Date(a.triggered_at));
  }

  /**
   * Get current saturation status
   * @returns {Object} Current status
   */
  getStatus() {
    const aggregate = this.loadAggregate();
    if (!aggregate) {
      return {
        status: 'NO_DATA',
        message: 'No saturation data recorded yet'
      };
    }

    const consistency = this.checkConsistency(aggregate);

    return {
      status: consistency.action,
      cycles_tracked: aggregate.cycles_tracked,
      avg_saturation_score: aggregate.rolling_metrics.avg_saturation_score,
      saturation_trend: aggregate.rolling_metrics.saturation_trend,
      consecutive_high: aggregate.rolling_metrics.consecutive_high_count,
      consecutive_critical: aggregate.rolling_metrics.consecutive_critical_count,
      action_recommended: consistency.action,
      reason: consistency.reason,
      urgency: consistency.urgency,
      last_updated: aggregate.last_updated
    };
  }
}

// Singleton instance
const monitor = new SaturationMonitor();

// Export
module.exports = {
  SaturationMonitor,
  monitor,

  // Convenience functions
  recordCycle: (cycleId, metrics) => monitor.recordCycle(cycleId, metrics),
  getStatus: () => monitor.getStatus(),
  listExpansions: () => monitor.listExpansions(),

  // Constants
  SATURATION_LEVELS,
  CONSISTENCY_THRESHOLDS,
  SATURATION_WEIGHTS,

  // Directories
  SATURATION_DIR,
  CYCLES_DIR,
  EXPANSIONS_DIR
};
