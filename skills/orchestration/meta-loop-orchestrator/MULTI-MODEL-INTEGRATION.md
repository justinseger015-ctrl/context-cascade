# Multi-Model Integration for Meta-Loop

## Overview

This document describes how the multi-model integration (Codex CLI + Gemini CLI) enhances the Meta-Loop orchestration flow.

## Enhanced Architecture

```
META-LOOP WITH MULTI-MODEL INTEGRATION
======================================

INPUT: Task + Target + Foundry Skill
                |
                v
        +---------------+
        |   PREPARE     |
        |   - Parse     |
        |   - Load exp  |
        |   - Select    |
        +---------------+
                |
                v
    +===========================+
    |   RESEARCH (NEW PHASE)    |  <-- Gemini Discovery Agent
    |   - Find existing solns   |
    |   - Search best practices |
    |   - Evaluate libraries    |
    +===========================+
                |
                v
    +=======================+
    |   EXECUTE (Ralph #1)  |
    |   Foundry skill runs  |
    |   until proposal ready|
    +=======================+
                |
                v
    +===========================+
    |  IMPLEMENT (ENHANCED)     |  <-- Codex Autonomous Agent
    |   - Route to Codex        |
    |   - Iterate until pass    |
    |   - Sandbox risky changes |
    +===========================+
                |
                v
    +-------+-------+-------+-------+
    |       |       |       |       |
    v       v       v       v       v
  [R#3]   [R#4]   [R#5]   [R#6]   <- Parallel Ralph Loops
  Prompt  Skill   Expert  Output
  Audit   Audit   Audit   Audit
    |       |       |       |
    +-------+-------+-------+
                |
                v
    +===========================+
    |    EVAL (ENHANCED)        |  <-- Codex for test fixing
    |    Run eval harness       |
    |    Fix until pass (Codex) |
    +===========================+
                |
                v
        +---------------+
        |    COMPARE    |
        |   baseline vs |
        |   candidate   |
        +---------------+
                |
        +-------+-------+
        |               |
        v               v
     ACCEPT          REJECT
        |               |
        v               v
     COMMIT        LOG FAILURE
        |           (retry)
        v
    +=======================+
    |  MONITOR (Ralph #8)   |
    |    7-day watch        |
    +=======================+
        |
        v
     COMPLETE
```

## New Phase: RESEARCH

Before executing the foundry skill, use Gemini to discover existing solutions:

```yaml
research_phase:
  agent: gemini-discovery-agent
  trigger_conditions:
    - New feature implementation
    - Library selection needed
    - Pattern adoption required

  workflow:
    1. Formulate discovery queries
    2. Invoke Gemini with search grounding
    3. Capture existing solutions
    4. Evaluate build vs buy
    5. Store findings in Memory-MCP
    6. Proceed to EXECUTE with context

  invocation:
    bash -lc "gemini 'Find existing solutions for: {task description}'"
    # OR
    ./scripts/multi-model/delegate.sh gemini "{query}"
```

## Enhanced IMPLEMENT Phase

Route implementation to Codex for autonomous iteration:

```yaml
implement_phase:
  agent: codex-autonomous-agent
  modes:
    full_auto:
      command: bash -lc "codex --full-auto exec '{task}'"
      risk: medium
      use_for: Standard implementation

    sandbox:
      command: bash -lc "codex --sandbox workspace-write exec '{task}'"
      risk: low
      use_for: Risky refactoring, major changes

    yolo:
      command: bash -lc "codex --yolo exec '{task}'"
      risk: high
      use_for: Speed-critical, trusted patterns

  workflow:
    1. Assess risk level of changes
    2. Select appropriate mode
    3. Invoke Codex with iteration limit
    4. Monitor iteration progress
    5. Review changes before proceeding
    6. Store patterns in Memory-MCP
```

## Enhanced EVAL Phase

Use Codex to fix failing tests iteratively:

```yaml
eval_phase:
  agent: codex-autonomous-agent
  trigger: eval harness failures

  workflow:
    1. Run eval harness
    2. If failures detected:
       - Invoke Codex: "Fix failing tests"
       - Iterate until pass or limit reached
    3. Re-run eval harness
    4. Compare to baseline
    5. Accept/Reject decision

  invocation:
    ./scripts/multi-model/codex-yolo.sh \
      "Fix all failing tests in {eval_target}" \
      "{task_id}" \
      "." \
      15 \
      full-auto
```

## Decision Routing via multi-model-router.sh

The router automatically detects task type and routes to optimal model:

```bash
# Automatic routing based on keywords
./scripts/multi-model/multi-model-router.sh "{task description}"

# Routing rules:
# - "find existing", "best practices" -> gemini-research
# - "analyze codebase", "architecture" -> gemini-megacontext
# - "fix", "implement", "debug" -> codex
# - "decide", "choose approach" -> council
# - Default complex reasoning -> claude
```

## Integration with Ralph Loops

Each Ralph loop can now leverage multi-model capabilities:

| Ralph Loop | Primary Model | Multi-Model Enhancement |
|------------|---------------|------------------------|
| Execute (R#1) | Claude | Gemini research for context |
| Implement (R#2) | Claude | Codex autonomous iteration |
| Auditors (R#3-6) | Claude | Parallel validation |
| Eval (R#7) | Claude | Codex test fixing |
| Monitor (R#8) | Claude | (unchanged) |

## Skills and Agents Reference

### Skills (for SOPs)
- `multi-model-discovery`: Research before implementation
- `codex-iterative-fix`: Autonomous test fixing
- `codex-safe-experiment`: Sandbox experimentation
- `gemini-codebase-onboard`: Full codebase analysis

### Agents (for execution)
- `gemini-discovery-agent`: Delegates to Gemini CLI
- `codex-autonomous-agent`: Delegates to Codex CLI

## Memory Integration

All multi-model operations store results:

```yaml
memory_namespaces:
  discovery: "multi-model/discovery/{project}/{task_id}"
  implementation: "multi-model/codex/iterative-fix/{project}/{task_id}"
  experiment: "multi-model/codex/experiment/{project}/{task_id}"
  codebase: "multi-model/gemini/onboard/{project}/{task_id}"

tagging:
  WHO: "{agent-name}"
  WHEN: "ISO8601_timestamp"
  PROJECT: "{project_name}"
  WHY: "{phase_purpose}"
```

## Example: Full Meta-Loop with Multi-Model

```yaml
task: "Add rate limiting to API endpoints"

meta_loop_execution:
  1_prepare:
    - Parse task and target
    - Detect domain: "api-security"

  2_research:  # NEW PHASE
    - agent: gemini-discovery-agent
    - query: "Best rate limiting libraries Node.js 2024"
    - result: "Recommended: express-rate-limit"

  3_execute:
    - agent: planner
    - proposal: "Add express-rate-limit middleware"

  4_implement:  # ENHANCED
    - agent: codex-autonomous-agent
    - mode: full-auto
    - result: Implementation complete

  5_audit:
    - Prompt Auditor: PASS
    - Skill Auditor: PASS
    - Expert Auditor: PASS
    - Output Auditor: PASS

  6_eval:  # ENHANCED
    - Run eval harness
    - 2 tests failing
    - agent: codex-autonomous-agent
    - Fix: 5 iterations
    - Result: All tests pass

  7_compare:
    - Baseline: 98.5%
    - Candidate: 99.2%
    - Decision: ACCEPT

  8_commit:
    - git commit -m "feat: Add rate limiting"

  9_monitor:
    - 7-day watch initiated
```

## Guardrails

NEVER:
- Install or upgrade Codex/Gemini CLI
- Skip research phase for new implementations
- Use Codex without iteration limits
- Trust sandbox results blindly

ALWAYS:
- Use bash -lc for CLI invocation
- Store all findings in Memory-MCP
- Review changes before commit
- Set appropriate mode for risk level
