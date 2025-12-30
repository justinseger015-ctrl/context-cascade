# Cognitive Architecture + Meta-Loop + Ralph Wiggum Integration Guide

## Overview

This guide documents the integration of three subsystems into one coherent, production-safe architecture:

1. **Cognitive Architecture System** - VERILINGUA/VERIX + VectorCodec 14D + PromptBuilder thin waist + modes + MOO
2. **Recursive Self-Improvement Meta Loop** - 8-phase orchestrator + 4 auditors + improvement pipeline + rollback + dogfooding
3. **Ralph Wiggum Hook Loop** - stop-hook iteration engine using filesystem+git as persistent memory

---

## Architecture: Five Planes (MECE)

```
+-------------------------------------------------------------------------+
|                         GOVERNANCE PLANE                                 |
|  8-phase orchestrator | Rollback policy | Auditor consensus             |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         EVIDENCE PLANE                                   |
|  Frozen eval harness | Benchmark suites | Regression tests              |
|  CONSTITUTIONALLY PROTECTED - Does NOT self-improve                     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                       OPTIMIZATION PLANE                                 |
|  GlobalMOO (5D) | PyMOO NSGA-II (14D) | Mode distillation              |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                        COGNITION PLANE                                   |
|  VERILINGUA (7 frames) | VERIX | VectorCodec | PromptBuilder            |
|  THIN WAIST: build(task, task_type) -> (system_prompt, user_prompt)     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                        EXECUTION PLANE                                   |
|  Claude runtime | Ralph loop iterations | Artifact production          |
+-------------------------------------------------------------------------+
```

---

## File Contracts

All integration state lives in `.loop/`:

```
.loop/
+-- runtime_config.json    # CONTROL INPUT - Written ONLY by UnifiedBridge
+-- eval_report.json       # EVIDENCE TRUTH - Written ONLY by Frozen Harness
+-- events.jsonl           # APPEND-ONLY event spine
+-- policy.json            # Governance policy (regression thresholds, gates)
+-- history.json           # Iteration history (harness metrics only)
+-- moo_state.json         # MOO optimization state
+-- task_metadata.json     # Task context for mode selection
```

### runtime_config.json (CONTROL INPUT)

Written ONLY by UnifiedBridge after Governance approval.

```json
{
  "mode": "balanced",
  "vector14": [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
  "verix": {
    "strictness": "MODERATE",
    "compression": "L1",
    "require_ground": true,
    "require_confidence": true
  },
  "frames": {
    "evidential": true,
    "aspectual": true,
    "morphological": false,
    "compositional": false,
    "honorific": false,
    "classifier": false,
    "spatial": false
  },
  "iteration": 7,
  "previous_harness_score": 0.73,
  "exploration_mode": "exploit",
  "updated_at": "2025-12-30T12:34:56-05:00"
}
```

### eval_report.json (EVIDENCE TRUTH)

Written ONLY by Frozen Eval Harness. NEVER by model.

```json
{
  "iteration": 7,
  "timestamp": "2025-12-30T12:34:56-05:00",
  "artifact_path": "./output/latest.txt",
  "artifact_hash": "abc123def456",
  "metrics": {
    "task_accuracy": 0.82,
    "token_efficiency": 0.74,
    "edge_robustness": 0.71,
    "epistemic_consistency": 0.86,
    "overall": 0.78
  },
  "harness_version": "1.0.0",
  "harness_hash": "frozen_abc123"
}
```

### events.jsonl (APPEND-ONLY)

Every iteration appends one line:

```json
{"event_id":"uuid1","timestamp":"2025-12-30T12:34:56-05:00","task_id":"ralph_7","plane":"execution","timescale":"micro","iteration":7,"config":{"mode":"balanced"},"metrics":{"overall":0.78},"decision":"block","reason":"CONTINUE_ITERATION"}
```

---

## Data Flow (Goodhart-Resistant)

```
Ralph (artifact) --> Harness (grades) --> eval_report.json (truth)
                                                  |
                                            Bridge (reads)
                                                  |
                                        runtime_config.json (control)
                                                  |
                                       PromptBuilder (compiles)
                                                  |
                                          Ralph (next iteration)
```

**CRITICAL**: Model NEVER reports its own metrics. Harness is the ONLY source of truth.

---

## How to Run

### Start a Ralph Loop with Integration

```bash
# 1. Initialize .loop/ directory (if needed)
python -c "from integration.unified_bridge import UnifiedBridge; b = UnifiedBridge('.loop'); print('Initialized')"

# 2. Set up task metadata
echo '{"task_type": "coding", "task_description": "Build an API"}' > .loop/task_metadata.json

# 3. Start Ralph loop
/ralph-loop "Build an API with authentication" --completion-promise "API_COMPLETE" --max-iterations 20
```

### Check Loop Status

```bash
python -m loopctl status --loop-dir .loop
```

Output:
```json
{
  "current_iteration": 7,
  "mode": "balanced",
  "exploration_mode": "exploit",
  "last_score": 0.78,
  "history_length": 7,
  "max_iterations": 50
}
```

### Reset Loop State

```bash
python -m loopctl reset --loop-dir .loop
```

---

## Invariants (MUST HOLD)

### 1. Thin Waist Contract is Sacred

```python
def build(task: str, task_type: str) -> Tuple[str, str]:
    """Returns (system_prompt, user_prompt)"""
```

This signature MUST remain unchanged. Optimize AROUND it, never THROUGH it.

### 2. Evidence Plane is Constitutionally Protected

- Frozen eval harness is authoritative and MUST NOT self-improve
- Do NOT derive metrics from model output text
- Only the harness produces eval_report.json metrics

### 3. Ralph is Executor, Not Governor

- Ralph iterates; it does NOT grade, authorize, or decide "goodness"
- Governance + harness decide block/allow continuation
- Ralph produces ARTIFACTS; harness produces TRUTH

### 4. Bridge is the Only Cross-Plane Mutation Gate

- Only UnifiedBridge may write runtime_config.json
- All config changes flow through this gate

### 5. Event Log is Append-Only

- events.jsonl is NEVER overwritten
- Events support audit/replay/debug

### 6. Timescale Isolation

```
MACRO (days/weeks)  - Governance: skills, auditors, architecture
  |
  +-- MESO (hours/days) - Optimization: vectors, modes
        |
        +-- MICRO (minutes) - Execution: Ralph iterations
```

Inner loops COMPLETE before outer loops observe results.

---

## Components

### UnifiedBridge

Location: `integration/unified_bridge.py`

The ONLY place where loop state influences prompt generation.

```python
from integration import UnifiedBridge

bridge = UnifiedBridge(Path(".loop"))
builder = bridge.get_prompt_builder()
system_prompt, user_prompt = builder.build(task, task_type)
```

### loopctl CLI

Location: `loopctl/__main__.py`

Single authority for Ralph loop decisions.

```bash
python -m loopctl ralph_iteration_complete --state .claude/ralph-loop.local.md --loop-dir .loop
```

### VERIX-Speaking Auditors

Location: `integration/auditors.py`

Four auditors that emit structured JSON with VERIX claims:

| Auditor   | Question                                    | Primary Frame              |
|-----------|---------------------------------------------|----------------------------|
| Skill     | Does it demonstrate the intended capability?| Compositional + Classifier |
| Prompt    | Did compilation/config behave as intended?  | Evidential                 |
| Expertise | Is domain reasoning sound for audience?     | Honorific                  |
| Output    | Does it meet acceptance criteria?           | Classifier + Spatial       |

```python
from integration.auditors import AuditorPanel

panel = AuditorPanel()
result = panel.audit_all(artifact, eval_report, runtime_config)
print(result["consensus"])  # {"decision": "ACCEPT", "confidence": 0.85}
```

### Telemetry Bridge

Location: `integration/telemetry_bridge.py`

Bridges loop state to cognitive architecture telemetry format and Memory-MCP v3.0.

```python
from integration.telemetry_bridge import TelemetryBridge

bridge = TelemetryBridge(Path(".loop"))
records = bridge.sync_all()
mcp_format = bridge.export_to_memory_mcp()
```

---

## Tests

Run integration invariant tests:

```bash
pytest tests/test_integration_invariants.py -v
```

Tests verify:
- E1: Thin waist contract unchanged
- E2: Harness is authoritative
- E3: Bridge is only writer
- E4: Events are append-only
- E5: Ralph E2E smoke
- E6: Regression gate works
- E7: Cache key includes config

---

## Interpreting events.jsonl

Each event records a complete iteration:

```json
{
  "event_id": "uuid",
  "timestamp": "ISO8601",
  "task_id": "ralph_7",
  "plane": "execution",
  "timescale": "micro",
  "iteration": 7,
  "git_head": "abc1234",
  "config": {
    "mode": "balanced",
    "vector14": [1,1,0,0,0,0,0,1,1,1,1,0,0,0],
    "frames": ["evidential", "aspectual"],
    "verix_strictness": "MODERATE"
  },
  "metrics": {
    "task_accuracy": 0.82,
    "overall": 0.78
  },
  "decision": "block",
  "reason": "CONTINUE_ITERATION",
  "grounds": "[assert|confident] Decision based on harness metrics [ground:eval_report] [conf:0.95]"
}
```

Use this for:
- Audit trail of all decisions
- Debugging configuration changes
- Performance analysis over time
- Replay/rollback scenarios

---

## Troubleshooting

### Loop Stuck at Max Iterations

Check policy.json max_iterations and increase if needed:
```bash
jq '.max_iterations = 100' .loop/policy.json > tmp.json && mv tmp.json .loop/policy.json
```

### Regression Gate Blocking Progress

Lower threshold temporarily (not recommended for production):
```bash
jq '.regression_threshold = 0.10' .loop/policy.json > tmp.json && mv tmp.json .loop/policy.json
```

### Harness Hash Mismatch

If harness was legitimately updated, update policy:
```bash
jq '.harness_hash = "frozen_eval_harness_v1.1.0"' .loop/policy.json > tmp.json && mv tmp.json .loop/policy.json
```

---

## Version History

- **v1.0.0** (2025-12-30): Initial integration
  - UnifiedBridge + loopctl CLI
  - 4 VERIX-speaking auditors
  - Telemetry bridge for schema alignment
  - 7 invariant test suites
  - Full documentation
