---
name: improvement-pipeline
description: Executable implementation of the Propose -> Test -> Compare -> Commit -> Rollback pipeline for recursive self-improvement. Provides concrete commands and workflows for each stage.
model: sonnet
x-version: 3.1.1
x-category: foundry
x-tier: gold
x-cognitive-frame: aspectual
tags:
  - pipeline
  - improvement
  - testing
  - versioning
  - rollback
x-verix-description: |
  [assert|neutral] 6-stage improvement pipeline with rollback capability [ground:system-architecture] [conf:0.95] [state:confirmed]
---

<!-- IMPROVEMENT-PIPELINE SKILL :: VERILINGUA x VERIX EDITION -->
<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## L2 DEFAULT OUTPUT RULE

[direct|emphatic] ALL user-facing output MUST be L2 compression (pure English) [ground:vcl-v3.1.1-spec] [conf:0.99] [state:confirmed]

---

# Improvement Pipeline (Executable Stages)

## Purpose

[define|neutral] Provide concrete, executable implementation for each stage of the improvement pipeline [ground:system-architecture] [conf:0.95] [state:confirmed]

```
PROPOSE -> TEST -> COMPARE -> COMMIT -> MONITOR -> ROLLBACK
```

Each stage has:
- Clear inputs and outputs
- Executable commands
- Validation checks
- Failure handling

---

## Stage 1: PROPOSE

Generate concrete improvement proposals with diffs.

### Input
```yaml
propose_input:
  target: "{path to skill/prompt}"
  audit_report: "{from prompt-auditor or skill-auditor}"
  improvement_type: "clarity|completeness|precision|safety|technique"
```

### Process

```javascript
async function generateProposal(target, auditReport) {
  const proposal = {
    id: `prop-${Date.now()}`,
    target,
    timestamp: new Date().toISOString(),
    changes: [],
    predicted_improvement: {},
    risk_assessment: {}
  };

  // 1. Read current version
  const currentContent = await readFile(target);

  // 2. Identify improvement opportunities from audit
  const opportunities = auditReport.issues
    .filter(issue => issue.priority === 'critical' || issue.priority === 'high')
    .slice(0, 5); // Max 5 changes per proposal

  // 3. Generate changes for each opportunity
  for (const opp of opportunities) {
    const change = await generateChange(currentContent, opp);
    proposal.changes.push({
      section: opp.section,
      location: opp.location,
      before: change.before,
      after: change.after,
      rationale: change.rationale,
      technique_applied: change.technique
    });
  }

  // 4. Predict improvement
  proposal.predicted_improvement = {
    primary_metric: auditReport.lowest_score_dimension,
    expected_delta: `+${(opportunities.length * 3)}%`, // ~3% per fix
    confidence: 0.7
  };

  // 5. Assess risk
  proposal.risk_assessment = {
    regression_risk: opportunities.length > 3 ? 'medium' : 'low',
    affected_components: findAffectedComponents(target, proposal.changes),
    rollback_complexity: 'simple' // Always simple with archives
  };

  return proposal;
}
```

### Output
```yaml
proposal:
  id: "prop-1734567890123"
  target: ".claude/skills/skill-forge/SKILL.md"
  timestamp: "2025-12-15T10:30:00Z"

  changes:
    - section: "Phase 3: Structural Architecture"
      location: "Lines 145-160"
      before: |
        Design the skill's structure based on progressive disclosure.
      after: |
        Design the skill's structure based on progressive disclosure.

        ### Failure Handling (REQUIRED)

        For each operation in the skill:
        1. Identify possible failure modes
        2. Define explicit error messages
        3. Specify recovery actions
        4. Include timeout handling

        ```yaml
        error_handling:
          timeout:
            threshold: 30s
            action: "Return partial results with warning"
          invalid_input:
            detection: "Validate against schema"
            action: "Return clear error message with fix suggestion"
        ```
      rationale: "Adds explicit failure handling missing from Phase 3"
      technique_applied: "completeness_enhancement"

  predicted_improvement:
    primary_metric: "failure_coverage"
    expected_delta: "+9%"
    confidence: 0.7

  risk_assessment:
    regression_risk: "low"
    affected_components: ["micro-skill-creator", "agent-creator"]
    rollback_complexity: "simple"
```

### Validation
```yaml
proposal_validation:
  required_fields:
    - id: "Must be unique"
    - target: "Must be valid file path"
    - changes: "At least 1 change"
    - predicted_improvement: "Must have primary_metric"
    - risk_assessment: "Must have regression_risk"

  change_validation:
    - before: "Must exist in current file"
    - after: "Must be different from before"
    - rationale: "Must not be empty"
```

---

## Stage 2: TEST

Run evaluation harness on proposed changes.

### Input
```yaml
test_input:
  proposal_id: "prop-1734567890123"
  candidate_content: "{content with changes applied}"
  benchmark_suite: "prompt-generation-benchmark-v1 | skill-generation-benchmark-v1"
  regression_suite: "prompt-forge-regression-v1 | skill-forge-regression-v1"
```

### Process

```javascript
async function runTests(proposal, candidateContent) {
  const results = {
    proposal_id: proposal.id,
    timestamp: new Date().toISOString(),
    benchmarks: {},
    regressions: {},
    human_gates: []
  };

  // 1. Determine which test suites to run
  const benchmarks = getBenchmarksForTarget(proposal.target);
  const regressions = getRegressionsForTarget(proposal.target);

  // 2. Run benchmark suite
  for (const benchmark of benchmarks) {
    const benchResult = await runBenchmark(benchmark, candidateContent);
    results.benchmarks[benchmark.id] = {
      status: benchResult.score >= benchmark.minimum ? 'PASS' : 'FAIL',
      score: benchResult.score,
      minimum: benchmark.minimum,
      tasks: benchResult.task_results
    };
  }

  // 3. Run regression tests
  for (const regression of regressions) {
    const regResult = await runRegressionSuite(regression, candidateContent);
    results.regressions[regression.id] = {
      status: regResult.failed === 0 ? 'PASS' : 'FAIL',
      passed: regResult.passed,
      failed: regResult.failed,
      failed_tests: regResult.failed_tests
    };
  }

  // 4. Check human gates
  results.human_gates = checkHumanGates(proposal);

  return results;
}

function getBenchmarksForTarget(target) {
  if (target.includes('prompt-forge')) {
    return [{ id: 'prompt-generation-benchmark-v1', minimum: 0.7 }];
  }
  if (target.includes('skill-forge') || target.includes('SKILL.md')) {
    return [{ id: 'skill-generation-benchmark-v1', minimum: 0.75 }];
  }
  if (target.includes('expertise')) {
    return [{ id: 'expertise-generation-benchmark-v1', minimum: 0.8 }];
  }
  return [];
}
```

### Output
```yaml
test_results:
  proposal_id: "prop-1734567890123"
  timestamp: "2025-12-15T10:35:00Z"

  benchmarks:
    skill-generation-benchmark-v1:
      status: "PASS"
      score: 0.87
      minimum: 0.75
      tasks:
        sg-001:
          name: "Micro-Skill Generation"
          scores:
            functionality: 0.85
            contract_compliance: 0.90
            error_coverage: 0.86
        sg-002:
          name: "Complex Skill Generation"
          scores:
            functionality: 0.88
            structure_compliance: 0.87
            safety_coverage: 0.85

  regressions:
    skill-forge-regression-v1:
      status: "PASS"
      passed: 4
      failed: 0
      failed_tests: []

  human_gates: []  # None triggered
```

### Validation
```yaml
test_validation:
  benchmark_check:
    - all_benchmarks_run: true
    - all_scores_recorded: true

  regression_check:
    - all_tests_run: true
    - failure_details_captured: true

  gate_check:
    - all_gates_evaluated: true
```

---

## Stage 3: COMPARE

Compare baseline vs candidate, decide ACCEPT or REJECT.

### Input
```yaml
compare_input:
  proposal_id: "prop-1734567890123"
  baseline_scores: "{from previous eval}"
  candidate_scores: "{from Stage 2}"
  test_results: "{full test results}"
```

### Process

```javascript
function compareAndDecide(baseline, candidate, testResults) {
  const comparison = {
    proposal_id: testResults.proposal_id,
    timestamp: new Date().toISOString(),
    baseline_scores: baseline,
    candidate_scores: candidate,
    delta: {},
    verdict: null,
    reason: null
  };

  // 1. Calculate deltas
  for (const [metric, candidateScore] of Object.entries(candidate)) {
    const baselineScore = baseline[metric] || 0;
    comparison.delta[metric] = {
      baseline: baselineScore,
      candidate: candidateScore,
      change: candidateScore - baselineScore,
      percent_change: ((candidateScore - baselineScore) / baselineScore * 100).toFixed(2)
    };
  }

  // 2. Check for regressions (hard fail)
  for (const [suite, result] of Object.entries(testResults.regressions)) {
    if (result.status === 'FAIL') {
      comparison.verdict = 'REJECT';
      comparison.reason = `Regression test failed: ${result.failed_tests.join(', ')}`;
      return comparison;
    }
  }

  // 3. Check benchmarks meet minimum (hard fail)
  for (const [suite, result] of Object.entries(testResults.benchmarks)) {
    if (result.status === 'FAIL') {
      comparison.verdict = 'REJECT';
      comparison.reason = `Benchmark ${suite} below minimum: ${result.score} < ${result.minimum}`;
      return comparison;
    }
  }

  // 4. Check for improvement (soft requirement)
  const avgDelta = Object.values(comparison.delta)
    .reduce((sum, d) => sum + d.change, 0) / Object.keys(comparison.delta).length;

  if (avgDelta < 0) {
    comparison.verdict = 'REJECT';
    comparison.reason = `No improvement: average delta = ${avgDelta.toFixed(3)}`;
    return comparison;
  }

  // 5. Check human gates
  if (testResults.human_gates.length > 0) {
    comparison.verdict = 'PENDING_HUMAN_REVIEW';
    comparison.reason = `Human review required: ${testResults.human_gates.join(', ')}`;
    return comparison;
  }

  // 6. All passed - ACCEPT
  comparison.verdict = 'ACCEPT';
  comparison.reason = `All checks passed. Average improvement: +${(avgDelta * 100).toFixed(2)}%`;
  comparison.improvement_summary = {
    average_delta: avgDelta,
    best_improvement: Object.entries(comparison.delta)
      .sort((a, b) => b[1].change - a[1].change)[0],
    regressions_passed: Object.keys(testResults.regressions).length,
    benchmarks_passed: Object.keys(testResults.benchmarks).length
  };

  return comparison;
}
```

### Output
```yaml
comparison_result:
  proposal_id: "prop-1734567890123"
  timestamp: "2025-12-15T10:40:00Z"

  baseline_scores:
    clarity: 0.82
    completeness: 0.78
    precision: 0.80

  candidate_scores:
    clarity: 0.85
    completeness: 0.87
    precision: 0.82

  delta:
    clarity:
      baseline: 0.82
      candidate: 0.85
      change: 0.03
      percent_change: "3.66%"
    completeness:
      baseline: 0.78
      candidate: 0.87
      change: 0.09
      percent_change: "11.54%"
    precision:
      baseline: 0.80
      candidate: 0.82
      change: 0.02
      percent_change: "2.50%"

  verdict: "ACCEPT"
  reason: "All checks passed. Average improvement: +4.67%"

  improvement_summary:
    average_delta: 0.0467
    best_improvement: ["completeness", { change: 0.09 }]
    regressions_passed: 1
    benchmarks_passed: 1
```

### Validation
```yaml
comparison_validation:
  required:
    - verdict: "Must be ACCEPT|REJECT|PENDING_HUMAN_REVIEW"
    - reason: "Must explain decision"

  verdict_rules:
    REJECT:
      - "Any regression failure"
      - "Any benchmark below minimum"
      - "Negative improvement delta"
    PENDING_HUMAN_REVIEW:
      - "Human gate triggered"
    ACCEPT:
      - "All regressions pass"
      - "All benchmarks meet minimum"
      - "Positive improvement delta"
      - "No human gates"
```

---

## Stage 4: COMMIT

Apply changes and create version entry.

### Input
```yaml
commit_input:
  proposal_id: "prop-1734567890123"
  target: "{file path}"
  new_content: "{content with changes applied}"
  comparison_result: "{from Stage 3}"
```

### Process

```javascript
async function commitChanges(proposal, target, newContent, comparison) {
  const commit = {
    id: `commit-${Date.now()}`,
    proposal_id: proposal.id,
    timestamp: new Date().toISOString(),
    target,
    actions: []
  };

  // 1. Archive current version
  const archivePath = getArchivePath(target);
  const currentVersion = await getCurrentVersion(target);
  await writeFile(
    `${archivePath}/SKILL-v${currentVersion}.md`,
    await readFile(target)
  );
  commit.actions.push({
    action: 'archive',
    path: `${archivePath}/SKILL-v${currentVersion}.md`
  });

  // 2. Apply new content
  await writeFile(target, newContent);
  commit.actions.push({
    action: 'update',
    path: target
  });

  // 3. Increment version
  const newVersion = incrementVersion(currentVersion);
  await updateVersionInFile(target, newVersion);
  commit.actions.push({
    action: 'version_bump',
    from: currentVersion,
    to: newVersion
  });

  // 4. Update changelog
  const changelogEntry = formatChangelogEntry(proposal, comparison, newVersion);
  await appendToChangelog(target, changelogEntry);
  commit.actions.push({
    action: 'changelog_update',
    entry: changelogEntry
  });

  // 5. Store commit record in memory
  await storeInMemory(`improvement/commits/${commit.id}`, {
    ...commit,
    proposal,
    comparison
  });

  return commit;
}

function formatChangelogEntry(proposal, comparison, version) {
  return `
## v${version} (${new Date().toISOString().split('T')[0]})

**Proposal**: ${proposal.id}
**Improvement**: ${comparison.reason}

**Changes**:
${proposal.changes.map(c => `- ${c.section}: ${c.rationale}`).join('\n')}

**Metrics**:
${Object.entries(comparison.delta)
  .map(([k, v]) => `- ${k}: ${v.baseline} -> ${v.candidate} (${v.percent_change})`)
  .join('\n')}
`;
}
```

### Output
```yaml
commit_result:
  id: "commit-1734567890456"
  proposal_id: "prop-1734567890123"
  timestamp: "2025-12-15T10:45:00Z"
  target: ".claude/skills/skill-forge/SKILL.md"

  actions:
    - action: "archive"
      path: ".claude/skills/skill-forge/.archive/SKILL-v1.0.0.md"
    - action: "update"
      path: ".claude/skills/skill-forge/SKILL.md"
    - action: "version_bump"
      from: "1.0.0"
      to: "1.1.0"
    - action: "changelog_update"
      entry: "## v1.1.0..."

  status: "SUCCESS"
```

### Validation
```yaml
commit_validation:
  pre_commit:
    - archive_exists: "Verify archive created"
    - backup_verified: "Can restore from archive"

  post_commit:
    - file_updated: "Target file has new content"
    - version_incremented: "Version number updated"
    - changelog_appended: "Changelog has new entry"
    - memory_stored: "Commit record in memory"
```

---

## Stage 5: MONITOR

Track metrics after commit to detect delayed regressions.

### Input
```yaml
monitor_input:
  commit_id: "commit-1734567890456"
  target: "{file path}"
  metrics_window: "7 days"
  alert_thresholds:
    regression: 0.03  # 3% regression triggers alert
```

### Process

```javascript
async function setupMonitoring(commit, window = '7d') {
  const monitor = {
    commit_id: commit.id,
    target: commit.target,
    start_time: new Date().toISOString(),
    end_time: addDays(new Date(), 7).toISOString(),
    baseline_metrics: await getCurrentMetrics(commit.target),
    alerts: [],
    status: 'ACTIVE'
  };

  // Store monitoring config
  await storeInMemory(`improvement/monitors/${commit.id}`, monitor);

  return monitor;
}

async function checkMonitor(commitId) {
  const monitor = await retrieveFromMemory(`improvement/monitors/${commitId}`);
  if (!monitor || monitor.status !== 'ACTIVE') return null;

  const currentMetrics = await getCurrentMetrics(monitor.target);
  const alerts = [];

  // Check for regressions
  for (const [metric, baseline] of Object.entries(monitor.baseline_metrics)) {
    const current = currentMetrics[metric] || 0;
    const delta = current - baseline;

    if (delta < -0.03) { // 3% regression
      alerts.push({
        type: 'REGRESSION',
        metric,
        baseline,
        current,
        delta,
        severity: delta < -0.1 ? 'CRITICAL' : 'WARNING'
      });
    }
  }

  // Update monitor
  monitor.latest_check = new Date().toISOString();
  monitor.current_metrics = currentMetrics;
  monitor.alerts = alerts;

  if (alerts.some(a => a.severity === 'CRITICAL')) {
    monitor.status = 'ALERT_CRITICAL';
    // Trigger rollback consideration
    await notifyRollbackNeeded(monitor);
  }

  await storeInMemory(`improvement/monitors/${commitId}`, monitor);

  return monitor;
}
```

### Output
```yaml
monitor_status:
  commit_id: "commit-1734567890456"
  target: ".claude/skills/skill-forge/SKILL.md"
  status: "ACTIVE"

  baseline_metrics:
    clarity: 0.85
    completeness: 0.87
    precision: 0.82

  current_metrics:
    clarity: 0.84
    completeness: 0.88
    precision: 0.82

  alerts: []
  days_remaining: 5
  next_check: "2025-12-16T10:00:00Z"
```

---

## Stage 6: ROLLBACK

Restore previous version if regressions detected.

### Input
```yaml
rollback_input:
  commit_id: "commit-1734567890456"
  reason: "regression_detected | manual_request"
  evidence: "{alert details or user request}"
```

### Process

```javascript
async function rollback(commitId, reason, evidence) {
  const commit = await retrieveFromMemory(`improvement/commits/${commitId}`);
  if (!commit) throw new Error(`Commit not found: ${commitId}`);

  const rollback = {
    id: `rollback-${Date.now()}`,
    commit_id: commitId,
    target: commit.target,
    timestamp: new Date().toISOString(),
    reason,
    evidence,
    actions: []
  };

  // 1. Find archived version
  const archivePath = getArchivePath(commit.target);
  const previousVersion = decrementVersion(commit.actions
    .find(a => a.action === 'version_bump').to);
  const archiveFile = `${archivePath}/SKILL-v${previousVersion}.md`;

  // 2. Verify archive exists
  if (!await fileExists(archiveFile)) {
    rollback.status = 'FAILED';
    rollback.error = `Archive not found: ${archiveFile}`;
    return rollback;
  }

  // 3. Restore archived content
  const archivedContent = await readFile(archiveFile);
  await writeFile(commit.target, archivedContent);
  rollback.actions.push({
    action: 'restore',
    from: archiveFile,
    to: commit.target
  });

  // 4. Update changelog
  const rollbackEntry = `
## ROLLBACK to v${previousVersion} (${new Date().toISOString().split('T')[0]})

**Rolled back from**: ${commit.actions.find(a => a.action === 'version_bump').to}
**Reason**: ${reason}
**Evidence**: ${JSON.stringify(evidence)}
`;
  await appendToChangelog(commit.target, rollbackEntry);
  rollback.actions.push({
    action: 'changelog_update',
    entry: rollbackEntry
  });

  // 5. Mark commit as rolled back
  commit.rolled_back = true;
  commit.rollback_id = rollback.id;
  await storeInMemory(`improvement/commits/${commitId}`, commit);

  // 6. Store rollback record
  await storeInMemory(`improvement/rollbacks/${rollback.id}`, rollback);

  // 7. Cancel monitoring
  const monitor = await retrieveFromMemory(`improvement/monitors/${commitId}`);
  if (monitor) {
    monitor.status = 'CANCELLED_ROLLBACK';
    await storeInMemory(`improvement/monitors/${commitId}`, monitor);
  }

  rollback.status = 'SUCCESS';
  rollback.restored_version = previousVersion;

  return rollback;
}
```

### Output
```yaml
rollback_result:
  id: "rollback-1734567890789"
  commit_id: "commit-1734567890456"
  target: ".claude/skills/skill-forge/SKILL.md"
  timestamp: "2025-12-15T15:00:00Z"

  reason: "regression_detected"
  evidence:
    alert_type: "REGRESSION"
    metric: "clarity"
    baseline: 0.85
    current: 0.75
    delta: -0.10

  actions:
    - action: "restore"
      from: ".claude/skills/skill-forge/.archive/SKILL-v1.0.0.md"
      to: ".claude/skills/skill-forge/SKILL.md"
    - action: "changelog_update"
      entry: "## ROLLBACK to v1.0.0..."

  status: "SUCCESS"
  restored_version: "1.0.0"
```

### Validation
```yaml
rollback_validation:
  pre_rollback:
    - archive_exists: "Verify archived version available"
    - target_accessible: "Can write to target file"

  post_rollback:
    - content_restored: "File matches archive"
    - changelog_updated: "Rollback documented"
    - commit_marked: "Commit flagged as rolled back"
    - monitor_cancelled: "Monitoring stopped"
```

---

## Pipeline Orchestration

### Full Pipeline Execution

```javascript
async function runImprovementPipeline(target, auditReport) {
  const pipeline = {
    id: `pipeline-${Date.now()}`,
    target,
    timestamp: new Date().toISOString(),
    stages: {}
  };

  try {
    // Stage 1: PROPOSE
    pipeline.stages.propose = await generateProposal(target, auditReport);
    if (pipeline.stages.propose.changes.length === 0) {
      pipeline.result = 'NO_PROPOSALS';
      return pipeline;
    }

    // Stage 2: TEST
    const candidateContent = applyChanges(
      await readFile(target),
      pipeline.stages.propose.changes
    );
    pipeline.stages.test = await runTests(pipeline.stages.propose, candidateContent);

    // Stage 3: COMPARE
    const baseline = await getBaselineScores(target);
    const candidate = extractScores(pipeline.stages.test);
    pipeline.stages.compare = compareAndDecide(baseline, candidate, pipeline.stages.test);

    // Decision point
    if (pipeline.stages.compare.verdict === 'REJECT') {
      pipeline.result = 'REJECTED';
      pipeline.reason = pipeline.stages.compare.reason;
      return pipeline;
    }

    if (pipeline.stages.compare.verdict === 'PENDING_HUMAN_REVIEW') {
      pipeline.result = 'PENDING';
      pipeline.reason = pipeline.stages.compare.reason;
      // Store for human review
      await storeInMemory(`improvement/pending/${pipeline.id}`, pipeline);
      return pipeline;
    }

    // Stage 4: COMMIT
    pipeline.stages.commit = await commitChanges(
      pipeline.stages.propose,
      target,
      candidateContent,
      pipeline.stages.compare
    );

    // Stage 5: MONITOR
    pipeline.stages.monitor = await setupMonitoring(pipeline.stages.commit);

    pipeline.result = 'ACCEPTED';
    pipeline.reason = pipeline.stages.compare.reason;

  } catch (error) {
    pipeline.result = 'ERROR';
    pipeline.error = error.message;
  }

  // Store pipeline record
  await storeInMemory(`improvement/pipelines/${pipeline.id}`, pipeline);

  return pipeline;
}
```

---

## Memory Namespaces

| Namespace | Purpose | Retention |
|-----------|---------|-----------|
| `improvement/proposals/{id}` | Pending proposals | Until resolved |
| `improvement/commits/{id}` | Committed changes | Permanent |
| `improvement/rollbacks/{id}` | Rollback events | Permanent |
| `improvement/monitors/{id}` | Active monitoring | 30 days |
| `improvement/pipelines/{id}` | Full pipeline runs | 90 days |
| `improvement/pending/{id}` | Awaiting human review | Until resolved |

---

---

**Status**: Production-Ready
**Version**: 3.1.1
**Key Constraint**: Every stage has clear inputs, outputs, and validation

---

<promise>IMPROVEMENT_PIPELINE_VCL_V3.1.1_COMPLIANT</promise>
