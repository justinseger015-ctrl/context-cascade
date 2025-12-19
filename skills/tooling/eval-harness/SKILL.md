---
name: eval-harness
description: Frozen evaluation harness that gates all self-improvement changes. Contains benchmark suites, regression tests, and human approval gates. Evaluates cognitive frame application and cross-lingual integration quality. CRITICAL - This skill does NOT self-improve. Only manually expanded.
version: 1.1.0
category: foundry
tags:
  - evaluation
  - benchmark
  - regression
  - frozen
  - gate
  - cognitive-frames
  - cross-lingual
---

# Eval Harness (Frozen Evaluation)

## Purpose

Gate ALL self-improvement changes with objective evaluation.

**CRITICAL**: This harness does NOT self-improve. It is manually maintained and expanded. This prevents Goodhart's Law (optimizing the metric instead of the outcome).

## Core Principle

> "A self-improvement loop is only as good as its evaluation harness."

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

### Suite 4: Cognitive Frame Quality

**ID**: `cognitive-frame-benchmark-v1`
**Purpose**: Evaluate quality of cognitive frame application

```yaml
benchmark:
  id: cognitive-frame-benchmark-v1
  version: 1.0.0
  last_modified: "2025-12-18"
  frozen: true

  tasks:
    - id: "cf-001"
      name: "Evidential Frame Application"
      input: "Apply evidential frame to code review task"
      expected_qualities:
        - has_source_markers
        - has_confidence_levels
        - has_multi_lingual_activation
        - markers_consistently_applied
      scoring:
        marker_coverage: 0.0-1.0
        activation_quality: 0.0-1.0
        output_improvement: 0.0-1.0

    - id: "cf-002"
      name: "Aspectual Frame Application"
      input: "Apply aspectual frame to deployment tracking"
      expected_qualities:
        - has_completion_markers
        - has_progress_states
        - has_multi_lingual_activation
        - states_accurately_tracked
      scoring:
        marker_coverage: 0.0-1.0
        activation_quality: 0.0-1.0
        tracking_accuracy: 0.0-1.0

    - id: "cf-003"
      name: "Frame Selection Accuracy"
      input: "Given task, select appropriate frame"
      expected_qualities:
        - goal_analysis_complete
        - checklist_followed
        - frame_matches_task_type
        - rationale_documented
      scoring:
        selection_accuracy: 0.0-1.0
        rationale_quality: 0.0-1.0

  minimum_passing:
    average_marker_coverage: 0.75
    average_activation_quality: 0.7
    selection_accuracy: 0.8
```

### Suite 5: Cross-Lingual Integration Quality

**ID**: `cross-lingual-benchmark-v1`
**Purpose**: Evaluate quality of cross-lingual cognitive integration

```yaml
benchmark:
  id: cross-lingual-benchmark-v1
  version: 1.0.0
  last_modified: "2025-12-18"
  frozen: true

  tasks:
    - id: "cl-001"
      name: "Turkish Evidential Integration"
      input: "Generate evidential markers with Turkish activation"
      expected_qualities:
        - turkish_text_grammatically_correct
        - markers_map_to_turkish_concepts
        - english_output_incorporates_markers
      scoring:
        linguistic_quality: 0.0-1.0
        integration_quality: 0.0-1.0

    - id: "cl-002"
      name: "Russian Aspectual Integration"
      input: "Generate aspectual markers with Russian activation"
      expected_qualities:
        - russian_text_grammatically_correct
        - sv_nsv_distinction_applied
        - english_output_tracks_completion
      scoring:
        linguistic_quality: 0.0-1.0
        integration_quality: 0.0-1.0

    - id: "cl-003"
      name: "Japanese Hierarchical Integration"
      input: "Generate audience-calibrated output with Japanese keigo activation"
      expected_qualities:
        - japanese_register_terms_correct
        - audience_calibration_applied
        - english_output_reflects_register
      scoring:
        linguistic_quality: 0.0-1.0
        integration_quality: 0.0-1.0

    - id: "cl-004"
      name: "Multi-Frame Composition"
      input: "Compose two frames for complex task"
      expected_qualities:
        - both_frames_activated
        - no_marker_conflicts
        - output_benefits_from_both
      scoring:
        composition_quality: 0.0-1.0
        coherence: 0.0-1.0

  minimum_passing:
    average_linguistic_quality: 0.7
    average_integration_quality: 0.75
    composition_quality: 0.7
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

### Regression Suite: Cognitive Lensing

**ID**: `cognitive-lensing-regression-v1`

```yaml
regression_suite:
  id: cognitive-lensing-regression-v1
  version: 1.0.0
  frozen: true

  tests:
    - id: "clr-001"
      name: "Goal analysis preserved"
      action: "Run frame selection on task"
      expected: "All three goal orders analyzed (1st, 2nd, 3rd)"
      must_pass: true

    - id: "clr-002"
      name: "Checklist followed"
      action: "Select frame for ambiguous task"
      expected: "Checklist completed before selection"
      must_pass: true

    - id: "clr-003"
      name: "Multi-lingual activation included"
      action: "Apply frame to prompt"
      expected: "Native language activation section present"
      must_pass: true

    - id: "clr-004"
      name: "English output maintained"
      action: "Generate frame-enhanced output"
      expected: "Final output is in English with markers"
      must_pass: true

    - id: "clr-005"
      name: "Frame selection logged"
      action: "Complete frame selection"
      expected: "Selection stored in memory-mcp with WHO/WHEN/PROJECT/WHY"
      must_pass: true

    - id: "clr-006"
      name: "Backward compatibility"
      action: "Run prompt without frame selection"
      expected: "Standard processing works when frame not selected"
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

## Version History

### v1.1.0 (2025-12-18)
- Added Suite 4: Cognitive Frame Quality (cognitive-frame-benchmark-v1)
- Added Suite 5: Cross-Lingual Integration Quality (cross-lingual-benchmark-v1)
- Added Regression Suite: Cognitive Lensing (cognitive-lensing-regression-v1)
- Added cognitive-frames and cross-lingual tags
- Expanded scope to evaluate cross-lingual cognitive enhancement
- NOTE: Expansion approved per protocol - does not invalidate existing tests

### v1.0.0 (Initial Release)
- Core benchmark suites: Prompt Generation, Skill Generation, Expertise File Quality
- Regression suites: Prompt Forge, Skill Forge
- 5 human gates for risk management
- Evaluation protocol and expansion protocol
- Anti-patterns documentation

---

**Status**: Production-Ready (FROZEN)
**Version**: 1.1.0
**Key Constraint**: This skill does NOT self-improve
**Expansion**: Manual only, with human approval

---

## Core Principles

### 1. Frozen Evaluation Prevents Goodhart's Law
The eval harness must NOT self-improve to prevent optimizing for the metric instead of the outcome.

**In practice**:
- Benchmarks and regression tests are versioned and immutable once published
- New benchmarks are added through manual human approval process
- Thresholds can only increase, never decrease to "pass" failing changes
- Any expansion requires explicit justification and does not invalidate existing tests
- Treat the eval harness as a regulatory compliance artifact, not engineering code

### 2. Objective Measurement Before Subjective Judgment
All improvement proposals must pass quantitative evaluation before human review.

**In practice**:
- Run benchmarks first: if scores do not meet minimum thresholds, reject immediately
- Run regressions next: if ANY regression fails, reject without further review
- Only invoke human gates after objective criteria pass
- Log all metrics with timestamps for audit trail and trend analysis
- Measure improvement deltas against baseline to detect marginal gains or regressions

### 3. Human Gates for Uncertainty and Risk
Automated evaluation cannot capture all failure modes - human judgment is required for edge cases.

**In practice**:
- Trigger human review for breaking changes, security modifications, novel patterns
- Require multi-approver consensus for high-risk changes
- Set timeouts: no approval within deadline equals automatic rejection
- Document disagreements between auditors and escalate to human tiebreaker
- Track gate effectiveness: which gates catch real issues vs false positives

---

## Anti-Patterns (Enhanced)

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Self-Improving Eval** | Allowing the eval harness to modify itself creates a feedback loop where improvements optimize for passing tests, not real quality gains | Freeze the eval harness. Only expand through manual approval. Version all benchmarks. Prevent automated threshold adjustments. |
| **Lowering Thresholds to Pass** | When improvements fail to meet standards, lowering the bar instead of improving the work erodes quality over time | Thresholds can only increase. If a proposal fails, improve the proposal or reject it. Track threshold changes in audit log. |
| **Skipping Regressions for Small Changes** | Even minor changes can introduce unexpected side effects - skipping validation creates compounding risk | Run full regression suite on every change, no exceptions. Automate regression execution to remove friction. Treat any regression failure as a hard block. |
| **Ignoring Human Gate Timeouts** | Allowing proposals to proceed when human reviewers do not respond undermines the gate's purpose | Timeouts default to REJECT, not ACCEPT. If reviewers are unavailable, the change waits or is withdrawn. Log timeout events for capacity planning. |
| **Metric Manipulation** | Optimizing for specific benchmark tasks instead of general capability (e.g., memorizing test cases) | Use holdout test sets that are not visible during training. Rotate benchmarks periodically. Add adversarial examples. Measure transfer learning to unseen tasks. |
| **Approval Fatigue** | Over-triggering human gates for low-risk changes causes reviewers to rubber-stamp approvals | Calibrate gate triggers to balance false positives vs false negatives. Track approval rates and adjust thresholds. Provide reviewers with rich context to make informed decisions. |

---

## Conclusion

The eval harness is the foundation of trustworthy self-improvement systems. By freezing evaluation criteria, requiring objective measurement before subjective judgment, and invoking human gates for uncertainty, teams prevent the insidious drift toward superficial improvements that look good on paper but fail in practice.

Goodhart's Law warns us: "When a measure becomes a target, it ceases to be a good measure." The eval harness resists this by remaining immutable - improvements must adapt to the harness, not the other way around. This asymmetry is not a limitation but a feature: it forces rigorous engineering instead of metric gaming.

Remember: a self-improvement loop is only as good as its evaluation harness. Invest in comprehensive benchmarks, regression tests, and human oversight. Treat the harness as infrastructure - boring, reliable, and never exciting. When the harness is solid, you can innovate with confidence knowing that regressions will be caught before they reach production.
