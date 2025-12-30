# Saturation Detection Algorithm v1.0

## Executive Summary

This document specifies the algorithm for detecting when the eval harness has been **consistently saturated**, triggering controlled expansion to maintain discriminative power.

**Key Insight**: A frozen eval harness that is too easy provides false confidence. When the system consistently hits ceiling, the harness must become MORE rigorous (one-way ratchet).

---

## PART 1: SATURATION METRICS

### 1.1 Primary Saturation Signals

| Signal | Description | Threshold | Weight |
|--------|-------------|-----------|--------|
| `benchmark_ceiling_rate` | % of benchmarks scoring >95% | >= 80% | 0.30 |
| `regression_pass_rate` | % of regression tests passing | = 100% | 0.25 |
| `improvement_delta_trend` | Trend of improvement magnitudes | Declining 5+ cycles | 0.20 |
| `proposal_pass_rate` | % of proposals passing eval | >= 85% | 0.15 |
| `auditor_unanimous_rate` | % of cycles with all auditors agreeing | >= 90% | 0.10 |

### 1.2 Saturation Score Calculation

```python
def compute_saturation_score(metrics: dict) -> float:
    """
    Compute overall saturation score [0.0, 1.0].
    Higher = more saturated = harness may need expansion.
    """
    weights = {
        'benchmark_ceiling_rate': 0.30,
        'regression_pass_rate': 0.25,
        'improvement_delta_trend': 0.20,
        'proposal_pass_rate': 0.15,
        'auditor_unanimous_rate': 0.10
    }

    # Normalize each metric to [0, 1]
    normalized = {
        'benchmark_ceiling_rate': min(1.0, metrics['benchmark_ceiling_rate'] / 0.80),
        'regression_pass_rate': 1.0 if metrics['regression_pass_rate'] == 1.0 else 0.5,
        'improvement_delta_trend': compute_trend_score(metrics['delta_history']),
        'proposal_pass_rate': min(1.0, metrics['proposal_pass_rate'] / 0.85),
        'auditor_unanimous_rate': min(1.0, metrics['auditor_unanimous_rate'] / 0.90)
    }

    # Weighted sum
    score = sum(normalized[k] * weights[k] for k in weights)
    return score

def compute_trend_score(delta_history: list) -> float:
    """
    Returns 1.0 if deltas are consistently declining (saturated).
    Returns 0.0 if deltas are stable or increasing.
    """
    if len(delta_history) < 5:
        return 0.0

    # Linear regression slope
    x = list(range(len(delta_history)))
    slope = compute_slope(x, delta_history)

    # Negative slope = declining deltas = saturation
    if slope < -0.01:  # Statistically significant decline
        return min(1.0, abs(slope) * 10)
    return 0.0
```

### 1.3 Saturation Thresholds

| Level | Score Range | Interpretation | Action |
|-------|-------------|----------------|--------|
| `NORMAL` | 0.0 - 0.5 | Harness providing good discrimination | Continue |
| `ELEVATED` | 0.5 - 0.7 | Early saturation signs | Monitor closely |
| `HIGH` | 0.7 - 0.85 | Significant saturation | Flag for review |
| `CRITICAL` | 0.85 - 1.0 | Consistent saturation | Trigger expansion research |

---

## PART 2: CONSISTENCY TRACKING (Memory MCP)

### 2.1 Storage Schema

```yaml
# Memory MCP Namespace: eval-harness/saturation

# Per-cycle snapshot
key: "eval-harness/saturation/cycles/{cycle_id}"
value:
  cycle_id: "cycle-1735600000000"
  timestamp: "2025-12-30T15:00:00Z"
  metrics:
    benchmark_ceiling_rate: 0.82
    regression_pass_rate: 1.0
    improvement_delta: 0.03
    proposal_pass_rate: 0.88
    auditor_unanimous_rate: 0.92
  saturation_score: 0.78
  saturation_level: "HIGH"
  x-schema-version: "1.0"

# Rolling window aggregate
key: "eval-harness/saturation/aggregate"
value:
  window_size: 20
  cycles_tracked: 20
  oldest_cycle: "cycle-1735400000000"
  newest_cycle: "cycle-1735600000000"

  rolling_metrics:
    avg_saturation_score: 0.72
    saturation_trend: "increasing"
    consecutive_high_count: 8
    consecutive_critical_count: 0

  history:
    - { cycle_id: "...", score: 0.65, level: "ELEVATED" }
    - { cycle_id: "...", score: 0.71, level: "HIGH" }
    # ... last 20 cycles

  last_updated: "2025-12-30T15:00:00Z"
  x-schema-version: "1.0"

# Expansion event log
key: "eval-harness/saturation/expansions/{expansion_id}"
value:
  expansion_id: "exp-1735600000000"
  triggered_at: "2025-12-30T15:00:00Z"
  trigger_reason: "consecutive_high >= 10"
  saturation_score_at_trigger: 0.86

  research_spawned:
    task_id: "research-exp-1735600000000"
    status: "in_progress"
    findings: null

  proposed_expansions: []
  human_approved: null
  applied_at: null

  x-schema-version: "1.0"
```

### 2.2 Consistency Detection Logic

```python
CONSISTENCY_THRESHOLDS = {
    'consecutive_high_for_research': 10,      # 10 consecutive HIGH triggers research
    'consecutive_critical_for_urgent': 5,     # 5 consecutive CRITICAL = urgent
    'rolling_avg_high_threshold': 0.70,       # Rolling avg > 0.70 = sustained saturation
    'minimum_cycles_for_detection': 10,       # Need at least 10 cycles
}

def check_consistency(aggregate: dict) -> dict:
    """
    Check if saturation is consistent enough to warrant action.
    Returns action recommendation.
    """
    result = {
        'is_consistent': False,
        'action': 'CONTINUE',
        'reason': None,
        'urgency': 'LOW'
    }

    # Not enough data
    if aggregate['cycles_tracked'] < CONSISTENCY_THRESHOLDS['minimum_cycles_for_detection']:
        result['reason'] = f"Insufficient data: {aggregate['cycles_tracked']} cycles"
        return result

    # Check consecutive CRITICAL (urgent)
    if aggregate['rolling_metrics']['consecutive_critical_count'] >= \
       CONSISTENCY_THRESHOLDS['consecutive_critical_for_urgent']:
        result['is_consistent'] = True
        result['action'] = 'TRIGGER_EXPANSION_RESEARCH'
        result['reason'] = f"URGENT: {aggregate['rolling_metrics']['consecutive_critical_count']} consecutive CRITICAL"
        result['urgency'] = 'CRITICAL'
        return result

    # Check consecutive HIGH
    if aggregate['rolling_metrics']['consecutive_high_count'] >= \
       CONSISTENCY_THRESHOLDS['consecutive_high_for_research']:
        result['is_consistent'] = True
        result['action'] = 'TRIGGER_EXPANSION_RESEARCH'
        result['reason'] = f"{aggregate['rolling_metrics']['consecutive_high_count']} consecutive HIGH"
        result['urgency'] = 'HIGH'
        return result

    # Check rolling average
    if aggregate['rolling_metrics']['avg_saturation_score'] >= \
       CONSISTENCY_THRESHOLDS['rolling_avg_high_threshold']:
        if aggregate['rolling_metrics']['saturation_trend'] == 'increasing':
            result['is_consistent'] = True
            result['action'] = 'FLAG_FOR_REVIEW'
            result['reason'] = f"Rolling avg {aggregate['rolling_metrics']['avg_saturation_score']:.2f} with increasing trend"
            result['urgency'] = 'MEDIUM'
            return result

    return result
```

### 2.3 Memory MCP Integration Points

```javascript
// saturation-monitor.js

const { taggedMemoryStore } = require('./12fa/memory-mcp-tagging-protocol.js');

class SaturationMonitor {
  constructor() {
    this.namespace = 'eval-harness/saturation';
  }

  /**
   * Record cycle metrics after each eval harness run
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

    // Store to Memory MCP
    await taggedMemoryStore('saturation-monitor', JSON.stringify(snapshot), {
      project: 'context-cascade',
      'x-intent': 'saturation_tracking',
      'x-namespace': `${this.namespace}/cycles/${cycleId}`,
      'x-level': saturationLevel
    });

    // Update aggregate
    await this.updateAggregate(snapshot);

    // Check consistency and trigger if needed
    const aggregate = await this.loadAggregate();
    const consistency = this.checkConsistency(aggregate);

    if (consistency.action === 'TRIGGER_EXPANSION_RESEARCH') {
      await this.triggerExpansionResearch(consistency, aggregate);
    }

    return { snapshot, consistency };
  }

  /**
   * Update rolling aggregate with new cycle
   */
  async updateAggregate(snapshot) {
    let aggregate = await this.loadAggregate();

    if (!aggregate) {
      aggregate = this.createEmptyAggregate();
    }

    // Add to history (maintain window size)
    aggregate.history.push({
      cycle_id: snapshot.cycle_id,
      score: snapshot.saturation_score,
      level: snapshot.saturation_level
    });

    if (aggregate.history.length > aggregate.window_size) {
      aggregate.history.shift();
    }

    // Update rolling metrics
    aggregate.cycles_tracked = aggregate.history.length;
    aggregate.newest_cycle = snapshot.cycle_id;
    aggregate.oldest_cycle = aggregate.history[0].cycle_id;

    aggregate.rolling_metrics = this.computeRollingMetrics(aggregate.history);
    aggregate.last_updated = new Date().toISOString();

    // Store updated aggregate
    await taggedMemoryStore('saturation-monitor', JSON.stringify(aggregate), {
      project: 'context-cascade',
      'x-intent': 'saturation_aggregate',
      'x-namespace': `${this.namespace}/aggregate`
    });

    return aggregate;
  }

  /**
   * Compute rolling metrics from history
   */
  computeRollingMetrics(history) {
    const scores = history.map(h => h.score);
    const levels = history.map(h => h.level);

    // Average score
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;

    // Trend (linear regression slope)
    const trend = this.computeTrend(scores);

    // Consecutive counts (from end)
    let consecutiveHigh = 0;
    let consecutiveCritical = 0;

    for (let i = levels.length - 1; i >= 0; i--) {
      if (levels[i] === 'CRITICAL') {
        consecutiveCritical++;
        consecutiveHigh++;
      } else if (levels[i] === 'HIGH') {
        consecutiveHigh++;
        if (consecutiveCritical > 0) break; // Only count consecutive
      } else {
        break;
      }
    }

    return {
      avg_saturation_score: avgScore,
      saturation_trend: trend > 0.01 ? 'increasing' : (trend < -0.01 ? 'decreasing' : 'stable'),
      consecutive_high_count: consecutiveHigh,
      consecutive_critical_count: consecutiveCritical
    };
  }
}
```

---

## PART 3: RESEARCH TRIGGER PROTOCOL

### 3.1 Expansion Research Task

When saturation is consistently detected, spawn a research task to identify expansion candidates:

```yaml
expansion_research:
  trigger: "consistency check returns TRIGGER_EXPANSION_RESEARCH"

  research_objectives:
    1. "Identify benchmark ceiling cases"
    2. "Analyze proposal failure patterns (what DOES fail?)"
    3. "Survey external benchmarks for inspiration"
    4. "Identify edge cases not currently covered"
    5. "Propose threshold increases"

  research_outputs:
    - benchmark_gaps: "Areas where current benchmarks lack discrimination"
    - edge_cases: "Specific scenarios not tested"
    - threshold_proposals: "Specific threshold increases"
    - new_benchmark_proposals: "Entirely new benchmarks"

  human_gate: required
  one_way_ratchet: enforced
```

### 3.2 Research Task Template

```javascript
async function triggerExpansionResearch(consistency, aggregate) {
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

  // Store expansion event
  await taggedMemoryStore('saturation-monitor', JSON.stringify(expansionEvent), {
    project: 'context-cascade',
    'x-intent': 'expansion_trigger',
    'x-namespace': `eval-harness/saturation/expansions/${expansionId}`,
    'x-urgency': consistency.urgency
  });

  // Spawn research task
  const researchPrompt = `
## Eval Harness Expansion Research

### Context
The eval harness has been consistently saturated:
- Saturation Score: ${aggregate.rolling_metrics.avg_saturation_score.toFixed(2)}
- Consecutive HIGH cycles: ${aggregate.rolling_metrics.consecutive_high_count}
- Trigger Reason: ${consistency.reason}

### Research Objectives
1. Analyze recent benchmark results - identify ceiling cases
2. Analyze proposal pass/fail patterns - what still fails and why?
3. Identify untested edge cases
4. Propose specific threshold increases
5. Propose new benchmarks (harder, more discriminative)

### Constraints
- ONE-WAY RATCHET: Only propose MORE rigorous changes
- FORBIDDEN: Lowering thresholds, removing tests, weakening gates
- REQUIRED: Human approval before any changes

### Output Format
Provide structured expansion proposals:
\`\`\`yaml
expansion_proposals:
  threshold_increases:
    - benchmark: "prompt-generation-benchmark-v1"
      current: 0.70
      proposed: 0.75
      rationale: "Consistently hitting >0.85"

  new_benchmarks:
    - id: "new-benchmark-id"
      name: "Description"
      purpose: "What it tests"
      expected_difficulty: "harder than existing"

  new_edge_cases:
    - category: "Category"
      description: "Edge case description"
      expected_failure_mode: "What should fail"
\`\`\`
`;

  // This would spawn a Task agent
  console.log(`[SaturationMonitor] Expansion research triggered: ${expansionId}`);
  console.log(`[SaturationMonitor] Research prompt ready for task spawn`);

  return { expansionId, researchPrompt };
}
```

### 3.3 Expansion Application Protocol

```yaml
expansion_application:
  prerequisites:
    - expansion_research: completed
    - human_review: approved
    - one_way_ratchet_verified: true

  process:
    1. "Archive current harness version"
    2. "Apply threshold increases"
    3. "Add new benchmarks (disabled initially)"
    4. "Add new edge case tests (disabled initially)"
    5. "Enable new tests one at a time"
    6. "Verify system still passes at baseline"
    7. "Commit new harness version"
    8. "Log expansion event"

  rollback:
    trigger: "System fails >50% of new tests immediately"
    action: "Restore previous harness, flag for review"
    rationale: "Expansion too aggressive, needs calibration"
```

---

## PART 4: INTEGRATION POINTS

### 4.1 Eval Harness Integration

Add to `eval-harness/SKILL.md`:

```yaml
## Saturation Monitoring

[assert|neutral] Eval harness tracks saturation for one-way expansion [ground:system-policy] [conf:0.95] [state:confirmed]

### After Each Evaluation

1. Record metrics to saturation monitor
2. Check consistency against thresholds
3. If TRIGGER_EXPANSION_RESEARCH: spawn research task
4. If FLAG_FOR_REVIEW: notify human

### Expansion Protocol

- Expansions require human approval
- Only MORE rigorous changes allowed
- All expansions logged to Memory MCP
```

### 4.2 Bootstrap Loop Integration

Update `bootstrap-loop/SKILL.md` to include saturation check:

```yaml
## Phase 4.5: Saturation Check (NEW)

After each eval harness run:
1. Record metrics to saturation monitor
2. Check if consistently saturated
3. If saturated: flag for harness expansion research
4. Continue with normal cycle
```

### 4.3 Memory MCP Namespace Summary

| Namespace | Purpose | Retention |
|-----------|---------|-----------|
| `eval-harness/saturation/cycles/{id}` | Per-cycle snapshots | 90 days |
| `eval-harness/saturation/aggregate` | Rolling window aggregate | Permanent |
| `eval-harness/saturation/expansions/{id}` | Expansion events | Permanent |

---

## PART 5: IMPLEMENTATION CHECKLIST

- [ ] Implement `saturation-monitor.js` in `hooks/12fa/`
- [ ] Add saturation metrics collection to eval harness
- [ ] Add Memory MCP storage for saturation tracking
- [ ] Add consistency detection logic
- [ ] Add research trigger mechanism
- [ ] Update eval-harness SKILL.md with saturation section
- [ ] Update bootstrap-loop with saturation check phase
- [ ] Add human gate for expansion approval
- [ ] Test one-way ratchet enforcement

---

## Document Metadata

- **Version**: 1.0
- **Created**: 2025-12-30
- **Status**: Design Complete
- **Owner**: Context Cascade Meta-Loop System
- **Dependencies**: Memory MCP, Eval Harness, Bootstrap Loop

---

<promise>SATURATION_DETECTION_ALGORITHM_V1.0_DESIGNED</promise>
