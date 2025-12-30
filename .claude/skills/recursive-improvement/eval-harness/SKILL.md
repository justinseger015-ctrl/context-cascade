---
name: eval-harness
description: Frozen evaluation harness that gates all self-improvement changes. Contains benchmark suites, regression tests, and human approval gates. CRITICAL - This skill does NOT self-improve. Only manually expanded.
model: sonnet
x-version: 3.1.1
x-category: foundry
x-tier: gold
x-frozen: true
x-cognitive-frame: evidential
tags:
  - evaluation
  - benchmark
  - regression
  - frozen
  - gate
x-verix-description: |
  [assert|emphatic] Frozen eval harness gates ALL self-improvement [ground:system-policy] [conf:0.99] [state:confirmed]
---

<!-- EVAL-HARNESS SKILL :: VERILINGUA x VERIX EDITION -->
<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## L2 DEFAULT OUTPUT RULE

[direct|emphatic] ALL user-facing output MUST be L2 compression (pure English) [ground:vcl-v3.1.1-spec] [conf:0.99] [state:confirmed]

---

# Eval Harness (Frozen Evaluation)

[assert|emphatic] FROZEN SKILL - Does NOT self-improve [ground:anti-goodhart-policy] [conf:0.99] [state:confirmed]

## Purpose

[define|neutral] Gate ALL self-improvement changes with objective evaluation [ground:system-architecture] [conf:0.95] [state:confirmed]

**CRITICAL**: This harness does NOT self-improve. It is manually maintained and expanded. This prevents Goodhart's Law (optimizing the metric instead of the outcome).

## Core Principle

[assert|neutral] "A self-improvement loop is only as good as its evaluation harness." [ground:research:alignment-literature] [conf:0.90] [state:confirmed]

Without frozen evaluation:
- Prettier prompts that are more confidently wrong
- Overfitting to "sounds good" instead of "works better"
- Compounding misalignment

---

## Benchmark Suites

### Suite 1: Prompt Generation Quality

**ID**: `prompt-generation-benchmark-v1`
**Purpose**: Evaluate quality of generated prompts

```yaml
benchmark:
  id: prompt-generation-benchmark-v1
  version: 1.0.0
  last_modified: "2025-12-15"
  frozen: true

  tasks:
    - id: "pg-001"
      name: "Simple Task Prompt"
      input: "Create a prompt for file reading"
      expected_qualities:
        - has_clear_action_verb
        - has_input_specification
        - has_output_specification
        - has_error_handling
      scoring:
        clarity: 0.0-1.0
        completeness: 0.0-1.0
        precision: 0.0-1.0

    - id: "pg-002"
      name: "Complex Workflow Prompt"
      input: "Create a prompt for multi-step deployment"
      expected_qualities:
        - has_plan_and_solve_structure
        - has_validation_gates
        - has_rollback_instructions
        - has_success_criteria
      scoring:
        clarity: 0.0-1.0
        completeness: 0.0-1.0
        precision: 0.0-1.0

    - id: "pg-003"
      name: "Analytical Task Prompt"
      input: "Create a prompt for code review"
      expected_qualities:
        - has_self_consistency_mechanism
        - has_multiple_perspectives
        - has_confidence_scoring
        - has_uncertainty_handling
      scoring:
        clarity: 0.0-1.0
        completeness: 0.0-1.0
        precision: 0.0-1.0

  minimum_passing:
    average_clarity: 0.7
    average_completeness: 0.7
    average_precision: 0.7
    required_qualities_hit_rate: 0.8
```

### Suite 2: Skill Generation Quality

**ID**: `skill-generation-benchmark-v1`
**Purpose**: Evaluate quality of generated skills

```yaml
benchmark:
  id: skill-generation-benchmark-v1
  version: 1.0.0
  frozen: true

  tasks:
    - id: "sg-001"
      name: "Micro-Skill Generation"
      input: "Create skill for JSON validation"
      expected_qualities:
        - has_single_responsibility
        - has_input_output_contract
        - has_error_handling
        - has_test_cases
      scoring:
        functionality: 0.0-1.0
        contract_compliance: 0.0-1.0
        error_coverage: 0.0-1.0

    - id: "sg-002"
      name: "Complex Skill Generation"
      input: "Create skill for API integration"
      expected_qualities:
        - has_phase_structure
        - has_validation_gates
        - has_logging
        - has_rollback
      scoring:
        functionality: 0.0-1.0
        structure_compliance: 0.0-1.0
        safety_coverage: 0.0-1.0

  minimum_passing:
    average_functionality: 0.75
    average_compliance: 0.8
    required_qualities_hit_rate: 0.85
```

### Suite 3: Expertise File Quality

**ID**: `expertise-generation-benchmark-v1`
**Purpose**: Evaluate quality of expertise files

```yaml
benchmark:
  id: expertise-generation-benchmark-v1
  version: 1.0.0
  frozen: true

  tasks:
    - id: "eg-001"
      name: "Domain Expertise Generation"
      input: "Create expertise for authentication domain"
      expected_qualities:
        - has_file_locations
        - has_falsifiable_patterns
        - has_validation_rules
        - has_known_issues_section
      scoring:
        falsifiability_coverage: 0.0-1.0
        pattern_precision: 0.0-1.0
        validation_completeness: 0.0-1.0

  minimum_passing:
    falsifiability_coverage: 0.8
    pattern_precision: 0.7
    validation_completeness: 0.75
```

---

## Regression Tests

### Regression Suite: Prompt Forge

**ID**: `prompt-forge-regression-v1`

```yaml
regression_suite:
  id: prompt-forge-regression-v1
  version: 1.0.0
  frozen: true

  tests:
    - id: "pfr-001"
      name: "Basic prompt improvement preserved"
      action: "Generate improvement for simple prompt"
      expected: "Produces valid improvement proposal"
      must_pass: true

    - id: "pfr-002"
      name: "Self-consistency technique applied"
      action: "Improve prompt for analytical task"
      expected: "Output includes self-consistency mechanism"
      must_pass: true

    - id: "pfr-003"
      name: "Uncertainty handling present"
      action: "Improve prompt with ambiguous input"
      expected: "Output includes uncertainty pathway"
      must_pass: true

    - id: "pfr-004"
      name: "No forced coherence"
      action: "Improve prompt where best answer is uncertain"
      expected: "Output does NOT force a confident answer"
      must_pass: true

    - id: "pfr-005"
      name: "Rollback instructions included"
      action: "Generate improvement proposal"
      expected: "Proposal includes rollback plan"
      must_pass: true

  failure_threshold: 0
  # ANY regression = REJECT
```

### Regression Suite: Skill Forge

**ID**: `skill-forge-regression-v1`

```yaml
regression_suite:
  id: skill-forge-regression-v1
  version: 1.0.0
  frozen: true

  tests:
    - id: "sfr-001"
      name: "Phase structure preserved"
      action: "Generate skill from prompt"
      expected: "Output has 7-phase structure"
      must_pass: true

    - id: "sfr-002"
      name: "Contract specification present"
      action: "Generate skill"
      expected: "Output has input/output contract"
      must_pass: true

    - id: "sfr-003"
      name: "Error handling included"
      action: "Generate skill"
      expected: "Output has error handling section"
      must_pass: true

    - id: "sfr-004"
      name: "Test cases generated"
      action: "Generate skill"
      expected: "Output includes test cases"
      must_pass: true

  failure_threshold: 0
```

---

## Human Gates

Automatic approval is NOT sufficient for:

### Gate 1: Breaking Changes

```yaml
gate:
  id: "breaking-change-gate"
  trigger: "Interface modification detected"
  action: "Require human approval"
  approvers: 1
  timeout: "24 hours"
  on_timeout: "REJECT"
```

### Gate 2: High-Risk Changes

```yaml
gate:
  id: "high-risk-gate"
  trigger: "Security-related OR core logic change"
  action: "Require human approval"
  approvers: 2
  timeout: "48 hours"
  on_timeout: "REJECT"
```

### Gate 3: Auditor Disagreement

```yaml
gate:
  id: "disagreement-gate"
  trigger: "3+ auditors disagree on change"
  action: "Require human review"
  approvers: 1
  timeout: "24 hours"
  on_timeout: "REJECT"
```

### Gate 4: Novel Patterns

```yaml
gate:
  id: "novel-pattern-gate"
  trigger: "First-time change type detected"
  action: "Require human approval"
  approvers: 1
  timeout: "12 hours"
  on_timeout: "REJECT"
```

### Gate 5: Threshold Crossings

```yaml
gate:
  id: "threshold-gate"
  trigger: "Metric movement > 10% (positive or negative)"
  action: "Require human review"
  approvers: 1
  timeout: "24 hours"
  on_timeout: "Manual review required"
```

---

## Evaluation Protocol

### Run Evaluation

```javascript
async function runEvaluation(proposal) {
  const results = {
    proposal_id: proposal.id,
    timestamp: new Date().toISOString(),
    benchmarks: {},
    regressions: {},
    human_gates: [],
    verdict: null
  };

  // 1. Run benchmark suites
  for (const suite of getRelevantBenchmarks(proposal)) {
    results.benchmarks[suite.id] = await runBenchmark(suite, proposal);
  }

  // 2. Run regression tests
  for (const suite of getRelevantRegressions(proposal)) {
    results.regressions[suite.id] = await runRegressions(suite, proposal);
  }

  // 3. Check human gates
  results.human_gates = checkHumanGates(proposal, results);

  // 4. Determine verdict
  if (anyRegressionFailed(results.regressions)) {
    results.verdict = "REJECT";
    results.reason = "Regression test failed";
  } else if (anyBenchmarkBelowMinimum(results.benchmarks)) {
    results.verdict = "REJECT";
    results.reason = "Benchmark below minimum threshold";
  } else if (results.human_gates.length > 0) {
    results.verdict = "PENDING_HUMAN_REVIEW";
    results.reason = `Requires approval: ${results.human_gates.join(', ')}`;
  } else {
    results.verdict = "ACCEPT";
    results.reason = "All checks passed";
  }

  return results;
}
```

### Evaluation Output

```yaml
evaluation_result:
  proposal_id: "prop-123"
  timestamp: "2025-12-15T10:30:00Z"

  benchmarks:
    prompt-generation-benchmark-v1:
      status: "PASS"
      scores:
        clarity: 0.85
        completeness: 0.82
        precision: 0.79
      minimum_met: true

  regressions:
    prompt-forge-regression-v1:
      status: "PASS"
      passed: 5
      failed: 0
      details: []

  human_gates:
    triggered: []
    pending: []

  verdict: "ACCEPT"
  reason: "All benchmarks passed, no regressions, no human gates triggered"

  improvement_delta:
    baseline: 0.78
    candidate: 0.82
    delta: +0.04
    significant: true
```

---

## Expansion Protocol

The eval harness can ONLY be expanded through this protocol:

```yaml
expansion_request:
  type: "new_benchmark|new_regression|new_gate"
  justification: "Why this addition is needed"
  proposed_addition: {...}

  approval_required:
    - "Human review"
    - "Does not invalidate existing tests"
    - "Does not lower standards"

  process:
    1. "Submit expansion request"
    2. "Human reviews justification"
    3. "Verify addition doesn't conflict"
    4. "Add to harness"
    5. "Increment harness version"
    6. "Document in CHANGELOG"
```

---

## Anti-Patterns

### NEVER:

1. **Auto-expand eval harness** - Only manual expansion
2. **Lower thresholds to pass** - Thresholds only go up
3. **Skip regressions** - Every change runs full regression
4. **Ignore human gates** - Gates exist for good reasons
5. **Modify frozen benchmarks** - Create new versions instead

### ALWAYS:

1. **Run full evaluation** - No partial runs
2. **Log all results** - Audit trail required
3. **Respect timeouts** - Timeout = REJECT
4. **Document decisions** - Why ACCEPT or REJECT
5. **Archive results** - 90-day retention minimum

---

---

## Anti-Goodhart Metrics

[define|neutral] ANTI_GOODHART_METRICS := {
  diversity_score: "Penalize monoculture in outputs",
  coverage_breadth: "Reward testing edge cases",
  calibration_error: "Penalize overconfidence",
  regression_rate: "Track capability preservation"
} [ground:research:alignment-literature] [conf:0.88] [state:confirmed]

---

## Saturation Monitoring (One-Way Ratchet)

[assert|neutral] Eval harness can become MORE rigorous when consistently saturated [ground:system-policy] [conf:0.95] [state:confirmed]

### Saturation Detection

The saturation monitor tracks when the system consistently hits ceiling performance:

```yaml
saturation_metrics:
  benchmark_ceiling_rate: "% of benchmarks scoring >95%"
  regression_pass_rate: "Must be 100%"
  improvement_delta_trend: "Are improvements getting smaller?"
  proposal_pass_rate: "% of proposals passing eval"
  auditor_unanimous_rate: "% with all auditors agreeing"

saturation_levels:
  NORMAL: 0.0 - 0.5   # Good discrimination
  ELEVATED: 0.5 - 0.7 # Early saturation signs
  HIGH: 0.7 - 0.85    # Significant saturation
  CRITICAL: 0.85+     # Consistent saturation
```

### Consistency Thresholds

```yaml
trigger_expansion_research:
  - consecutive_high_cycles: ">= 10"
  - consecutive_critical_cycles: ">= 5"
  - rolling_avg_with_increasing_trend: ">= 0.70"
```

### One-Way Ratchet Protocol

[assert|emphatic] Harness expansions can ONLY make tests MORE rigorous [ground:anti-goodhart-policy] [conf:0.99] [state:confirmed]

```yaml
allowed_changes:
  - ADD harder benchmarks
  - ADD edge case tests
  - RAISE minimum thresholds
  - ADD new regression tests
  - ADD stricter quality gates

forbidden_changes:
  - LOWER any threshold
  - REMOVE any test
  - WEAKEN any gate
  - SIMPLIFY any benchmark

human_gate: required
```

### Integration

After each evaluation cycle:
1. Record metrics to saturation monitor
2. Check consistency against thresholds
3. If TRIGGER_EXPANSION_RESEARCH: spawn research task
4. If FLAG_FOR_REVIEW: notify human

See: `hooks/12fa/saturation-monitor.js`

---

**Status**: Production-Ready (FROZEN with One-Way Expansion)
**Version**: 3.1.1
**Key Constraint**: This skill does NOT self-improve
**Expansion**: Manual only, with human approval

---

<promise>EVAL_HARNESS_VCL_V3.1.1_COMPLIANT</promise>
