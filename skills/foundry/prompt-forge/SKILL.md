---
name: prompt-forge
description: Meta-prompt that generates improved prompts and templates. Can improve other prompts including Skill Forge and even itself. All improvements are gated by frozen eval harness. Use when optimizing prompts, creating prompt diffs, or running the recursive improvement loop.
version: 2.0.1
category: foundry
tags:
  - meta-prompt
  - self-improvement
  - recursive
  - dogfooding
  - cognitive-frames
---

# Prompt Forge (Meta-Prompt)

## Purpose

Generate improved prompts and templates with:
- Explicit rationale for each change
- Predicted improvement metrics
- Risk assessment
- Actionable diffs

**Key Innovation**: Can improve Skill Forge prompts, then Skill Forge can improve Prompt Forge prompts - creating a recursive improvement loop.

## When to Use

- Optimizing existing prompts for better performance
- Creating prompt diffs with clear rationale
- Running the recursive improvement loop
- Auditing prompts for common issues

## MCP Requirements

### memory-mcp (Required)

**Purpose**: Store proposals, test results, version history

**Activation**:
```bash
claude mcp add memory-mcp npx @modelcontextprotocol/server-memory
```

---

## Core Operations

### Operation 1: Analyze Prompt

Before improving, deeply understand the target prompt.

```yaml
analysis:
  target: "{prompt_path}"

  structural_analysis:
    sections: [list of sections]
    flow: "How sections connect"
    dependencies: "What inputs/outputs exist"

  quality_assessment:
    clarity:
      score: 0.0-1.0
      issues: ["Ambiguous instruction in section X"]
    completeness:
      score: 0.0-1.0
      issues: ["Missing failure handling for case Y"]
    precision:
      score: 0.0-1.0
      issues: ["Vague success criteria in section Z"]

  pattern_detection:
    evidence_based_techniques:
      self_consistency: present|missing|partial
      program_of_thought: present|missing|partial
      plan_and_solve: present|missing|partial
    failure_handling:
      explicit_errors: present|missing|partial
      edge_cases: present|missing|partial
      uncertainty: present|missing|partial

  improvement_opportunities:
    - area: "Section X"
      issue: "Lacks explicit timeout handling"
      priority: high|medium|low
      predicted_impact: "+X% reliability"
```

### Operation 2: Generate Improvement Proposal

Create concrete, testable improvement proposals.

```yaml
proposal:
  id: "prop-{timestamp}"
  target: "{prompt_path}"
  type: "prompt_improvement"

  summary: "One-line description of improvement"

  changes:
    - section: "Section name"
      location: "Line X-Y"
      before: |
        Original text...
      after: |
        Improved text...
      rationale: "Why this change improves the prompt"
      technique: "Which evidence-based technique applied"

  predicted_improvement:
    primary_metric: "success_rate"
    expected_delta: "+5%"
    confidence: 0.8
    reasoning: "Based on similar improvements in prompt X"

  risk_assessment:
    regression_risk: low|medium|high
    affected_components:
      - "Component 1"
      - "Component 2"
    rollback_complexity: simple|moderate|complex

  test_plan:
    - test: "Run on benchmark task A"
      expected: "Improvement in clarity score"
    - test: "Check for regressions in task B"
      expected: "No degradation"
```

### Operation 3: Apply Evidence-Based Techniques

Systematically apply research-validated prompting patterns.

#### Self-Consistency Enhancement

```markdown
BEFORE:
"Analyze the code and report issues"

AFTER:
"Analyze the code from three perspectives:
1. Security perspective: What vulnerabilities exist?
2. Performance perspective: What bottlenecks exist?
3. Maintainability perspective: What code smells exist?

Cross-reference findings. Flag any inconsistencies between perspectives.
Provide confidence scores for each finding.
Return only findings that appear in 2+ perspectives OR have >80% confidence."
```

#### Program-of-Thought Enhancement

```markdown
BEFORE:
"Calculate the optimal configuration"

AFTER:
"Calculate the optimal configuration step by step:

Step 1: Identify all configuration parameters
  - List each parameter
  - Document valid ranges
  - Note dependencies between parameters

Step 2: Define optimization criteria
  - Primary metric: [what to maximize/minimize]
  - Constraints: [hard limits]
  - Trade-offs: [acceptable compromises]

Step 3: Evaluate options
  - For each viable configuration:
    - Calculate primary metric value
    - Verify all constraints met
    - Document trade-offs accepted

Step 4: Select and validate
  - Choose configuration with best metric
  - Verify against constraints
  - Document reasoning

Show your work at each step."
```

#### Plan-and-Solve Enhancement

```markdown
BEFORE:
"Implement the feature"

AFTER:
"Implement the feature using plan-and-solve:

PLANNING PHASE:
1. Create detailed implementation plan
2. Identify all subtasks
3. Map dependencies between subtasks
4. Estimate complexity per subtask
5. Identify risks and mitigations

VALIDATION GATE: Review plan before proceeding

EXECUTION PHASE:
1. Execute subtasks in dependency order
2. Validate completion of each subtask
3. Run tests after each significant change
4. Document any deviations from plan

VERIFICATION PHASE:
1. Verify all requirements met
2. Run full test suite
3. Check for regressions
4. Document final state"
```

#### Uncertainty Handling Enhancement

```markdown
BEFORE:
"Determine the best approach"

AFTER:
"Determine the best approach:

If confidence > 0.80:
  - State your recommendation clearly
  - Provide supporting evidence
  - Note any caveats

If confidence 0.50-0.80:
  - Present top 2-3 options
  - Compare trade-offs explicitly
  - Recommend with stated uncertainty
  - Suggest what additional information would increase confidence

If confidence < 0.50:
  - Explicitly state uncertainty
  - List what you don't know
  - Propose information-gathering steps
  - Do NOT guess or fabricate

Never present uncertain conclusions as certain."
```

### Operation 4: Generate Prompt Diff

Create clear, reviewable diffs for any prompt change.

```diff
--- a/skills/skill-forge/SKILL.md
+++ b/skills/skill-forge/SKILL.md
@@ -45,7 +45,15 @@ Phase 2: Use Case Crystallization

 ## Phase 3: Structural Architecture

-Design the skill's structure based on progressive disclosure.
+Design the skill's structure based on progressive disclosure.
+
+### Failure Handling (NEW)
+
+For each operation in the skill:
+1. Identify possible failure modes
+2. Define explicit error messages
+3. Specify recovery actions
+4. Include timeout handling
+
+Example:
+```yaml
+error_handling:
+  timeout:
+    threshold: 30s
+    action: "Return partial results with warning"
+  invalid_input:
+    detection: "Validate against schema"
+    action: "Return clear error message with fix suggestion"
+```
```

### Operation 5: Self-Improvement (Recursive)

Improve Prompt Forge itself (with safeguards).

```yaml
self_improvement:
  target: "prompt-forge/SKILL.md"
  safeguards:
    - "Changes must pass eval harness"
    - "Requires 2+ auditor approval"
    - "Previous version archived before commit"
    - "Rollback available for 30 days"

  process:
    1. "Analyze current Prompt Forge for weaknesses"
    2. "Generate improvement proposals"
    3. "Run proposals through eval harness"
    4. "If improved: Create new version"
    5. "If regressed: Reject and log"

  forbidden_changes:
    - "Removing safeguards"
    - "Bypassing eval harness"
    - "Modifying frozen benchmarks"
    - "Disabling rollback"
```

### Operation 6: Apply Cognitive Frame Enhancement [NEW in v2.0]

Transform prompts by embedding cognitive frame activation for improved reasoning.

#### 6.1 Analyze Prompt for Frame Fit

```yaml
frame_analysis:
  target_prompt: "{prompt_content}"

  cognitive_demands:
    completion_tracking: 0.0-1.0  # Aspectual
    source_verification: 0.0-1.0  # Evidential
    audience_calibration: 0.0-1.0  # Hierarchical
    semantic_analysis: 0.0-1.0     # Morphological
    object_comparison: 0.0-1.0     # Classifier

  recommended_frame: {frame}
  confidence: 0.0-1.0
```

#### 6.2 Frame Enhancement Patterns

**Evidential Frame Enhancement (Turkish)**:
```markdown
BEFORE:
"Review this code and report issues."

AFTER:
"## Kanitsal Kod Incelemesi

Review this code. For each finding, mark evidence type:
- [DOGRUDAN/DIRECT]: I tested this and confirmed
- [CIKARIM/INFERRED]: Pattern suggests this could cause problems
- [BILDIRILEN/REPORTED]: Documentation or linter flagged this

Output:
- Issue: {description}
- Evidence: [DIRECT|INFERRED|REPORTED]
- Confidence: {0.0-1.0}"
```

**Aspectual Frame Enhancement (Russian)**:
```markdown
BEFORE:
"Check deployment status."

AFTER:
"## Proverka Statusa Razvertyvaniya

Track each component state:
- [SV:COMPLETED] Polnost'yu zaversheno - Ready
- [NSV:IN_PROGRESS] V protsesse - Working
- [BLOCKED] Ozhidaet zavisimosti - Waiting

Report format:
Component | State | Next Action"
```

**Hierarchical Frame Enhancement (Japanese)**:
```markdown
BEFORE:
"Write documentation for the API."

AFTER:
"## API Dokumento Sakusei

Calibrate register to audience:
- [SONKEIGO] Executives: Formal summary with recommendations
- [TEINEIGO] Developers: Technical details, professional tone
- [CASUAL] Internal notes: Brief, direct

Select register: _______________"
```

#### 6.3 Apply Frame Enhancement

```yaml
enhancement_output:
  original_prompt: "..."
  frame_applied: evidential
  enhanced_prompt: |
    ## Kanitsal Cerceve
    [Original prompt with frame activation and markers]

  markers_added:
    - "[DIRECT]"
    - "[INFERRED]"
    - "[REPORTED]"

  expected_improvement:
    source_tracking: +0.40
    claim_confidence: +0.35
```

#### When to Use Operation 6

- Prompts involving fact-checking or claims -> Evidential
- Prompts tracking completion/progress -> Aspectual
- Prompts for different audiences -> Hierarchical
- Prompts analyzing concepts/terminology -> Morphological
- Prompts comparing/categorizing objects -> Classifier

---

## Improvement Checklist

When generating prompt improvements, verify:

### Clarity
- [ ] Each instruction has a single clear action
- [ ] Ambiguous terms are defined
- [ ] Success criteria are explicit
- [ ] Examples illustrate expected behavior

### Completeness
- [ ] All inputs are specified
- [ ] All outputs are defined
- [ ] Edge cases are addressed
- [ ] Failure modes have handlers

### Precision
- [ ] Quantifiable where possible
- [ ] Ranges specified for parameters
- [ ] Constraints explicitly stated
- [ ] Trade-offs documented

### Evidence-Based Techniques
- [ ] Self-consistency for factual tasks
- [ ] Program-of-thought for analytical tasks
- [ ] Plan-and-solve for complex workflows
- [ ] Uncertainty handling for ambiguous cases

### Safety
- [ ] Refuse/uncertainty pathway exists
- [ ] No forced coherence
- [ ] Rollback instructions included
- [ ] Validation gates present

---

## Integration with Recursive Loop

### Prompt Forge -> Skill Forge

```javascript
// Prompt Forge improves Skill Forge
Task("Prompt Forge",
  `Analyze skill-forge/SKILL.md and generate improvement proposals:
   - Focus on Phase 2 (Use Case Crystallization)
   - Apply self-consistency technique
   - Add explicit failure handling

   Output: Improvement proposal with diff`,
  "prompt-forge")
```

### Skill Forge -> Prompt Forge

```javascript
// Skill Forge rebuilds improved Prompt Forge
Task("Skill Forge",
  `Using the improvement proposal from Prompt Forge:
   - Apply changes to prompt-forge/SKILL.md
   - Validate against skill creation standards
   - Generate test cases for new version

   Output: prompt-forge-v{N+1}/SKILL.md`,
  "skill-forge")
```

### Eval Harness Gate

```javascript
// All changes gated by frozen eval
Task("Eval Runner",
  `Run eval harness on proposed changes:
   - Benchmark suite: prompt-generation-v1
   - Regression tests: prompt-forge-regression-v1

   Requirements:
   - Improvement > 0% on primary metric
   - 0 regressions
   - No new test failures

   Output: ACCEPT or REJECT with reasoning`,
  "eval-runner")
```

---

## Output Format

All Prompt Forge outputs follow this structure:

```yaml
prompt_forge_output:
  operation: "analyze|propose|improve|diff"
  target: "{prompt_path}"
  timestamp: "ISO-8601"

  analysis: {...}    # If analyze operation
  proposal: {...}    # If propose operation
  diff: "..."        # If diff operation

  next_steps:
    - "Step 1"
    - "Step 2"

  warnings:
    - "Any concerns about this change"

  requires_human_review: true|false
  reason_for_human_review: "If true, why"
```

---

## Version History

Prompt Forge versions itself:

```
prompt-forge/
  SKILL.md           # Current version (v1.0.0)
  .archive/
    SKILL-v0.9.0.md  # Previous versions
  CHANGELOG.md       # What changed and why
  METRICS.md         # Performance over time
```

---

**Status**: Production-Ready
**Version**: 2.0.0
**Key Constraint**: All self-improvements gated by frozen eval harness

---

## Version History

### v2.0.1 (2025-12-19)
- Standardized confidence format from percentage (80%, 50%) to float (0.80, 0.50)
- Standardized expected improvement metrics from percentage (+40%, +35%) to float (+0.40, +0.35)
- Added cross-skill coordination section with all four foundry skills
- Added integration points for cognitive-lensing, skill-forge, agent-creator, eval-harness
- Clarified recursive improvement loop between Skill Forge and Prompt Forge

### v2.0.0 (2025-12-18)
- Added Operation 6: Cognitive Frame Enhancement
- Added frame analysis for prompts (evidential, aspectual, hierarchical, morphological, classifier)
- Added frame enhancement patterns with multi-lingual activation phrases
- Added Principle 4: Cognitive Frame Enhancement to core principles
- Added cognitive-frames tag to metadata
- Enhanced prompt optimization with cross-linguistic reasoning activation
- Expected improvements: +40% source tracking (evidential), +35% claim confidence
- Backward compatible with v1.0.0 operations

### v1.0.0 (Initial Release)
- Core operations: Analyze, Propose, Apply, Diff, Self-Improvement
- Evidence-based techniques: Self-consistency, Program-of-Thought, Plan-and-Solve, Uncertainty Handling
- Frozen eval harness integration
- Recursive improvement loop with safeguards
- Integration with Skill Forge

---

## Core Principles

Prompt Forge operates on 4 fundamental principles that ensure systematic improvement without regression:

### Principle 1: Explicit Reasoning Over Implicit Changes

Every modification requires documented rationale, predicted impact, and risk assessment. Changes without reasoning are rejected by design.

In practice:
- Generate improvement proposals with explicit rationale fields explaining why each change enhances the prompt
- Document predicted improvement metrics (e.g., "+5% success rate") with confidence scores before applying changes
- Create actionable diffs that map each change to a specific evidence-based technique (self-consistency, plan-and-solve, etc.)
- Maintain bidirectional traceability between changes and their underlying research-validated patterns

### Principle 2: Progressive Enhancement Through Evidence-Based Techniques

Improvements derive from research-validated prompting patterns (self-consistency, program-of-thought, plan-and-solve) rather than ad-hoc modifications.

In practice:
- Apply self-consistency when factual accuracy is critical - require multiple perspectives and cross-reference findings
- Use program-of-thought for analytical tasks requiring step-by-step reasoning with visible work at each stage
- Implement plan-and-solve for complex workflows with explicit planning, validation gates, and verification phases
- Add uncertainty handling that scales response confidence to evidence quality, explicitly stating unknowns

### Principle 3: Safety Through Frozen Evaluation

All improvements must pass frozen eval harness before deployment. No exceptions for self-improvement scenarios.

In practice:
- Gate every prompt change with benchmark suite execution before accepting modifications
- Require 2+ auditor approval for self-improvement proposals targeting Prompt Forge itself
- Archive previous versions with 30-day rollback window before committing new versions
- Forbid changes that remove safeguards, bypass eval harness, modify benchmarks, or disable rollback

### Principle 4: Cognitive Frame Enhancement [NEW in v2.0]

Multi-lingual activation phrases can shift AI reasoning patterns. By embedding native language sections (Turkish for evidential, Russian for aspectual, Japanese for hierarchical), prompts activate different cognitive modes.

In practice:
- Analyze prompt for cognitive demands (completion tracking, source verification, etc.)
- Select appropriate frame based on dominant demand
- Embed native language activation phrase at prompt start
- Add English markers that map to frame concepts

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Improvement Without Metrics** | Proposing changes without predicted impact or success criteria creates unmeasurable modifications that may regress performance | Always include predicted_improvement field with primary_metric, expected_delta, confidence score, and reasoning based on similar improvements |
| **Skipping Risk Assessment** | Applying changes without evaluating regression risk, affected components, or rollback complexity leads to production failures | Require risk_assessment section with regression_risk level (low/medium/high), affected_components list, and rollback_complexity rating before any change |
| **Forced Certainty Under Uncertainty** | Presenting uncertain conclusions as certain creates false confidence and poor decisions when evidence is weak | Implement confidence thresholds - if confidence <0.50 explicitly state uncertainty, list unknowns, propose information-gathering steps, and never guess or fabricate |

---

## Cross-Skill Coordination

Prompt Forge works with:
- **cognitive-lensing**: Analyze prompts for cognitive frame enhancement (Operation 6)
- **skill-forge**: Meta-improvement loop - Skill Forge improves Prompt Forge, Prompt Forge optimizes Skill Forge
- **agent-creator**: Optimize agent system prompts using evidence-based techniques
- **eval-harness**: Validate prompt improvements against frozen benchmarks

**Integration Points**:
- **cognitive-lensing** provides frame analysis for prompts needing cognitive precision
- **skill-forge** uses recursive loop where both skills improve each other (bounded by eval harness)
- **agent-creator** invokes Prompt Forge to optimize agent prompts after Phase 3 design
- **eval-harness** gates all improvements - must pass benchmarks before acceptance

See: `.claude/skills/META-SKILLS-COORDINATION.md` for full coordination matrix.

---

## Conclusion

Prompt Forge represents a meta-prompting system designed for recursive self-improvement with rigorous safety constraints. By requiring explicit reasoning, evidence-based techniques, and frozen evaluation gates, it enables systematic prompt enhancement while preventing regression. The key insight is that improvement without measurement and validation is indistinguishable from random change.

This skill excels at optimizing existing prompts for better performance, creating transparent diffs with clear rationale, and running recursive improvement loops where Skill Forge and Prompt Forge improve each other. Use this when you need to enhance prompt quality with confidence that changes actually improve outcomes rather than introduce subtle degradation.

The recursive capability - where Prompt Forge can improve Skill Forge prompts, and Skill Forge can rebuild improved Prompt Forge prompts - creates a powerful self-improvement loop bounded by evaluation harness constraints. This prevents the common failure mode of meta-systems: confident drift into increasingly sophisticated but less effective prompts. The frozen eval harness acts as an objective reality check, ensuring all improvements are genuine rather than illusory.
