# Meta Loop + Ralph Wiggum Integration v1.1

## Overview

This document specifies how the Ralph Wiggum persistence loop integrates with the Meta Loop recursive improvement system to create a fully autonomous self-improvement pipeline for the foundry skills.

## CRITICAL: How Ralph Loops Actually Work

**The Ralph mechanism uses a SINGLE state file and SEQUENTIAL loops:**

```
~/.claude/ralph-wiggum/loop-state.md   <- THE state file (only one!)
```

### Stop Hook Mechanism

1. User starts Ralph loop via `/ralph-loop` or setup script
2. Setup script creates `loop-state.md` with `active: true` and prompt
3. Claude works on task
4. When Claude tries to exit, Stop hook (`quality-gate-stop-hook.sh`) runs
5. Hook checks: Is loop active? Is promise found? Quality gate passed?
6. If NOT complete: **Exit code 2** blocks exit, re-injects prompt
7. If complete: **Exit code 0** allows normal exit

### State File Format

```yaml
---
session_id: phase-20251228-160000
iteration: 3
max_iterations: 30
completion_promise: "PROPOSAL_READY"
started_at: 2025-12-28T16:00:00
active: true
quality_gate: true
---

[The prompt text goes here after the second ---]
```

### Key Constraints

- **Ralph loops are SEQUENTIAL** (one at a time, not nested)
- The meta loop manages **which phase's loop** is active
- Auditors run as **parallel Task agents**, NOT separate Ralph loops
- Each phase COMPLETES before next phase's loop starts

## The Integrated System

```
INTEGRATED META-LOOP WITH RALPH WIGGUM PERSISTENCE
===================================================

USER REQUEST: "Improve skill X" or "Create agent Y"
    |
    v
+-----------------------------------------------------------+
|              5-PHASE WORKFLOW (Phases 1-4)                |
|  intent-analyzer -> prompt-architect -> planner -> router |
+-----------------------------------------------------------+
    |
    v
+-----------------------------------------------------------+
|              PHASE 5: RALPH-POWERED EXECUTION             |
+-----------------------------------------------------------+
    |
    |   +==================================================+
    |   |            FOUNDRY TRIANGLE                       |
    |   |                                                   |
    |   |         PROMPT FORGE (Meta-Prompt)                |
    |   |              /           \                        |
    |   |             /             \                       |
    |   |            /               \                      |
    |   |  SKILL FORGE -------- AGENT CREATOR               |
    |   |  (Meta-Skill)         (Meta-Agent)                |
    |   |                                                   |
    |   +==================================================+
    |                       |
    |   Each foundry skill runs in Ralph Loop
    |                       |
    v                       v
+-----------------------------------------------------------+
|              RALPH LOOP PER FOUNDRY SKILL                 |
|                                                           |
|   /ralph-loop "                                           |
|     Execute {foundry-skill} for {target}:                 |
|     1. Load domain expertise                              |
|     2. Apply cognitive frame                              |
|     3. Execute all phases                                 |
|     4. Run adversarial testing                            |
|     5. Validate with eval harness                         |
|                                                           |
|     Output <promise>{SKILL}_COMPLETE</promise>            |
|   " --max-iterations 30                                   |
|                                                           |
+-----------------------------------------------------------+
    |
    v
+-----------------------------------------------------------+
|                    AUDITOR PHASE                          |
|   (Single Ralph loop - auditors are parallel Task agents) |
|                                                           |
|   4 Specialized Auditors run as PARALLEL Task() calls:    |
|                                                           |
|   [Single Message - Golden Rule]:                         |
|   Task("Prompt Auditor", "...", "prompt-auditor")         |
|   Task("Skill Auditor", "...", "skill-auditor")           |
|   Task("Expertise Auditor", "...", "expertise-auditor")   |
|   Task("Output Auditor", "...", "output-auditor")         |
|                                                           |
|   The AUDIT Ralph loop iterates until all agents pass,    |
|   then outputs <promise>ALL_AUDITS_PASS</promise>         |
|                                                           |
+-----------------------------------------------------------+
    |
    v
+-----------------------------------------------------------+
|             IMPROVEMENT PROPOSAL GENERATION               |
|                                                           |
|   If any auditor finds issues:                            |
|   - Generate improvement proposal                         |
|   - Route back to appropriate foundry skill               |
|   - Ralph loop until proposal implemented                 |
|                                                           |
+-----------------------------------------------------------+
    |
    v
+===========================================================+
|              EVAL HARNESS (FROZEN - GATE)                 |
|                                                           |
|   Ralph loop for test execution:                          |
|   /ralph-loop "                                           |
|     Run benchmarks: {benchmark_suite}                     |
|     Run regressions: {regression_suite}                   |
|     Fix failures until all pass                           |
|     Output <promise>EVAL_PASS</promise>                   |
|   " --max-iterations 50                                   |
|                                                           |
+===========================================================+
    |
    +--------+--------+
    |                 |
    v                 v
 ACCEPT            REJECT
    |                 |
    v                 v
 COMMIT          LOG FAILURE
    |             (retry with
    v              different
 MONITOR           approach)
 (7 days)
    |
    v
 ROLLBACK if regression
```

## Integration Points

### 1. Foundry Skill Execution via Ralph

Each foundry skill (agent-creator, skill-forge, prompt-forge) executes within a Ralph loop:

```yaml
foundry_ralph_integration:
  agent_creator:
    prompt: |
      Execute agent-creator for: {agent_spec}

      Phase 0: Load domain expertise from .claude/expertise/
      Phase 0.5: Select cognitive frame (evidential/aspectual/hierarchical)
      Phase 1: Analysis & Intent Decoding
      Phase 2: Meta-Cognitive Extraction
      Phase 3: Architecture Design
      Phase 4: Technical Enhancement

      After completion:
      - Run eval harness validation
      - Generate agent metrics

      Output <promise>AGENT_CREATED</promise> when validated
    max_iterations: 30
    completion_promise: "AGENT_CREATED"

  skill_forge:
    prompt: |
      Execute skill-forge for: {skill_spec}

      Phase 0: Schema Definition
      Phase 0.5: Cognitive Frame Design
      Phase 1: Intent Archaeology + COV
      Phase 2: Use Case Crystallization
      Phase 3: Structural Architecture
      Phase 4: Metadata Engineering
      Phase 5: Instruction Crafting + COV
      Phase 6: Resource Development
      Phase 7: Validation + Adversarial Testing
      Phase 8: Metrics Tracking

      Output <promise>SKILL_FORGED</promise> when Phase 7 passes
    max_iterations: 40
    completion_promise: "SKILL_FORGED"

  prompt_forge:
    prompt: |
      Execute prompt-forge for: {prompt_target}

      Operation 1: Analyze current prompt
      Operation 2: Generate improvement proposal
      Operation 3: Apply evidence-based techniques
      Operation 4: Generate diff
      Operation 5: Self-verify improvements
      Operation 6: Apply cognitive frame enhancement

      Output <promise>PROMPT_IMPROVED</promise> when metrics improve
    max_iterations: 20
    completion_promise: "PROMPT_IMPROVED"
```

### 2. Auditor Loops

Each auditor runs in its own mini-Ralph loop:

```yaml
auditor_ralph_integration:
  prompt_auditor:
    prompt: |
      Audit prompt/instructions in: {target}

      Check:
      - Clarity score >= 0.8
      - Completeness score >= 0.8
      - Precision score >= 0.8
      - Evidence-based techniques applied

      If issues found: Generate proposal
      Output <promise>PROMPT_AUDIT_PASS</promise>
    max_iterations: 10

  skill_auditor:
    prompt: |
      Audit skill structure in: {target}

      Check:
      - Tier 1-2 sections at 100%
      - Tier 3-4 sections at 80%+
      - YAML frontmatter valid
      - Examples present
      - Adversarial testing complete

      If issues found: Generate proposal
      Output <promise>SKILL_AUDIT_PASS</promise>
    max_iterations: 10

  expertise_auditor:
    prompt: |
      Audit domain expertise in: {target}

      Check:
      - File locations accurate (test against actual files)
      - Patterns match current code
      - No stale information
      - Adversarial validation survives

      If issues found: Update expertise file
      Output <promise>EXPERTISE_AUDIT_PASS</promise>
    max_iterations: 15

  output_auditor:
    prompt: |
      Audit generated output: {target}

      Check:
      - Output matches specification
      - Quality metrics met
      - No regression from baseline
      - Passes format validation

      If issues found: Route back to foundry
      Output <promise>OUTPUT_AUDIT_PASS</promise>
    max_iterations: 10
```

### 3. Eval Harness Loop

The eval harness runs in a Ralph loop with test-fix iteration:

```yaml
eval_harness_ralph:
  prompt: |
    Run complete eval harness for: {target}

    Benchmark Suite: {benchmark_id}
    - Run all benchmark tests
    - Record metrics

    Regression Suite: {regression_id}
    - Run regression tests
    - Compare to baseline

    If any test fails:
    1. Analyze failure
    2. Generate fix
    3. Apply fix
    4. Re-run tests

    Requirements:
    - All benchmarks PASS
    - No regressions (0 failures)
    - Metrics improved or unchanged

    Output <promise>EVAL_HARNESS_PASS</promise>
  max_iterations: 50
  completion_promise: "EVAL_HARNESS_PASS"
```

## Complete Meta Loop Cycle

### Invocation Command

```bash
/meta-loop-foundry "<task>" --target "<artifact>" --foundry "<skill>"
```

### Example: Improve Skill Forge

```bash
/meta-loop-foundry "Add cognitive frame integration to Phase 1" \
  --target "skills/foundry/skill-forge/SKILL.md" \
  --foundry "prompt-forge"
```

### Execution Sequence

```
1. PREPARE
   |
   +-> Parse task and target
   +-> Detect domain (foundry)
   +-> Load expertise: .claude/expertise/foundry.yaml
   +-> Select foundry skill (prompt-forge for improvements)

2. EXECUTE (Ralph Loop #1)
   |
   /ralph-loop "
     Execute prompt-forge to improve skill-forge:
     - Analyze current Phase 1 instructions
     - Identify cognitive frame integration points
     - Generate improvement proposal
     - Apply evidence-based techniques
     - Create diff for Phase 1 changes

     Output <promise>PROPOSAL_READY</promise>
   " --max-iterations 20

3. IMPLEMENT (Ralph Loop #2)
   |
   /ralph-loop "
     Apply proposal to skill-forge/SKILL.md:
     - Edit Phase 1 section
     - Add cognitive frame loading
     - Update examples
     - Run validation

     Output <promise>CHANGES_APPLIED</promise>
   " --max-iterations 15

4. AUDIT (Parallel Ralph Loops)
   |
   [Parallel - Single Message]:
   +-> /ralph-loop "prompt-auditor..." --max-iterations 10
   +-> /ralph-loop "skill-auditor..." --max-iterations 10
   +-> /ralph-loop "expertise-auditor..." --max-iterations 10
   +-> /ralph-loop "output-auditor..." --max-iterations 10

5. EVAL (Ralph Loop #3)
   |
   /ralph-loop "
     Run eval harness:
     - skill-generation-benchmark-v1
     - skill-forge-regression-v1
     - Fix any failures

     Output <promise>EVAL_PASS</promise>
   " --max-iterations 50

6. COMPARE
   |
   Compare metrics:
   - Before: {baseline}
   - After: {candidate}

   If improved >= 0%: ACCEPT
   If regressed: REJECT

7. COMMIT (if accepted)
   |
   git add skill-forge/SKILL.md
   git commit -m "feat(skill-forge): Add cognitive frame integration to Phase 1"

8. MONITOR (7-day Ralph Loop)
   |
   /ralph-loop "
     Monitor deployment:
     - Daily check for regressions
     - Track usage metrics
     - Alert if issues

     Output <promise>MONITOR_COMPLETE</promise>
   " --max-iterations 7  # One per day
```

## State Management

### Loop State Files

```
~/.claude/ralph-wiggum/
  loop-state.md           # Current active loop
  meta-loop-state.yaml    # Meta loop orchestration state
  foundry-sessions/       # Session history per foundry skill
    agent-creator-{id}.yaml
    skill-forge-{id}.yaml
    prompt-forge-{id}.yaml
  auditor-sessions/       # Auditor session history
```

### Meta Loop State Schema

```yaml
# ~/.claude/ralph-wiggum/meta-loop-state.yaml
---
session_id: meta-20251228-160000
active: true
phase: EXECUTE  # PREPARE|EXECUTE|IMPLEMENT|AUDIT|EVAL|COMPARE|COMMIT|MONITOR
started_at: 2025-12-28T16:00:00
task: "Add cognitive frame integration"
target: "skills/foundry/skill-forge/SKILL.md"
foundry_skill: prompt-forge

nested_loops:
  - id: ralph-execute-001
    phase: EXECUTE
    status: complete
    iterations: 8

  - id: ralph-implement-002
    phase: IMPLEMENT
    status: active
    iterations: 3

auditor_status:
  prompt: pending
  skill: pending
  expertise: pending
  output: pending

metrics:
  baseline:
    clarity: 0.85
    completeness: 0.82
  candidate:
    clarity: null  # Not yet measured
    completeness: null
---
```

## Memory Namespace Integration

```yaml
namespaces:
  meta-loop/
    sessions/{session_id}:
      description: Complete meta loop session
      ttl: 90d

    foundry/{skill}/{session_id}:
      description: Foundry skill execution

    auditors/{type}/{session_id}:
      description: Auditor results

    proposals/{session_id}:
      description: Improvement proposals

    comparisons/{session_id}:
      description: Baseline vs candidate

    monitoring/{session_id}:
      description: 7-day monitoring data

  ralph-wiggum/
    loop-state:
      description: Current active Ralph loop

    history/{id}:
      description: Completed loop history
```

## Safety Constraints

### Hard Rules

1. **Eval Harness NEVER in Ralph Loop for Self-Modification**
   - Eval harness tests other code
   - Eval harness code itself is FROZEN
   - Ralph cannot modify eval harness files

2. **Max Iterations Per Phase**
   ```yaml
   max_iterations:
     execute: 30
     implement: 20
     audit: 10
     eval: 50
     monitor: 7
   ```

3. **Human Gates**
   - Council decisions with confidence < 0.80 flagged for human review
   - Any change affecting > 500 lines requires human approval
   - Rollback after 7-day monitoring requires human confirmation

4. **Rollback Always Available**
   - 90-day archive of all previous versions
   - One-command rollback: `/rollback {session_id}`

### Forbidden Operations

```yaml
forbidden_in_ralph_loop:
  - Modifying eval harness code
  - Removing safety constraints
  - Bypassing auditor checks
  - Skipping comparison phase
  - Committing without eval pass
  - Disabling monitoring
```

## Commands

### /meta-loop-foundry

Start a meta loop cycle targeting foundry skills.

```bash
/meta-loop-foundry "<task>" \
  --target "<file_path>" \
  --foundry "agent-creator|skill-forge|prompt-forge" \
  [--max-iterations 30] \
  [--skip-monitor]
```

### /meta-loop-status

Check current meta loop status.

```bash
/meta-loop-status
# Output: Current phase, iterations, nested loops, auditor status
```

### /meta-loop-cancel

Cancel active meta loop.

```bash
/meta-loop-cancel [--force]
```

### /meta-loop-rollback

Rollback a completed meta loop session.

```bash
/meta-loop-rollback {session_id}
```

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Meta loop completion rate | >80% | Sessions completing all phases |
| Average iterations per phase | <15 | Total iterations / phases |
| Auditor pass rate | >90% | First-pass auditor approvals |
| Eval harness pass rate | >85% | Tests passing without iteration |
| Improvement acceptance rate | >60% | ACCEPT vs total decisions |
| 7-day regression rate | <5% | Rollbacks / committed changes |

## Integration with CLAUDE.md

Add to CLAUDE.md Section 7.4:

```markdown
### 7.4 Meta Loop + Ralph Wiggum Integration

**When**: Recursive self-improvement of foundry skills

**Architecture**:
```
5-PHASE WORKFLOW (1-4)
        |
        v
   FOUNDRY TRIANGLE (in Ralph Loops)
        |
        v
   4 AUDITORS (parallel Ralph Loops)
        |
        v
   EVAL HARNESS (Ralph Loop)
        |
        v
   COMPARE -> ACCEPT/REJECT -> COMMIT -> MONITOR
```

**Commands**:
- `/meta-loop-foundry "<task>" --target <file> --foundry <skill>`
- `/meta-loop-status`
- `/meta-loop-cancel`

**Key Insight**: Each phase runs in its own Ralph loop, creating nested persistence that ensures completion before moving to the next phase.

**Triggers**: "recursive improvement", "improve foundry", "meta loop", "self-improvement"
```

---

**Version**: 1.0.0
**Status**: Specification Complete
**Next Step**: Implement meta-loop-orchestrator skill
