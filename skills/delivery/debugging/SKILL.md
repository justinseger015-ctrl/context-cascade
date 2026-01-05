---
name: debugging
description: Structured debugging protocol for rapid triage, isolation, and fix verification with evidence-backed confidence ceilings.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.2.0
x-category: delivery
x-vcl-compliance: v3.1.1
x-cognitive-frames:
  - HON
  - MOR
  - COM
  - CLS
  - EVD
  - ASP
  - SPC
---


## STANDARD OPERATING PROCEDURE

### Purpose
Diagnose and resolve code defects quickly while preventing regressions and documenting learning.

### Trigger Conditions
- **Positive:** bug reports, failing tests, production incidents, performance regressions, flaky behavior, unexplained logs.
- **Negative:** net-new feature asks (route to feature-dev-complete) or pure prompt design (route to prompt-architect).

### Guardrails
- Enforce **structure-first**: keep `examples/`, `tests/`, `resources/`, and `references/` populated for each debugging effort.
- Apply **constraint extraction** (HARD/SOFT/INFERRED) on scope, environments, and risk tolerance; confirm inferred constraints.
- **Do not** modify production data or disable tests; use safe repro environments first.
- State **confidence with ceilings** `{inference/report:0.70, research:0.85, observation/definition:0.95}` for diagnoses and fixes.

### Execution Phases
1. **Triage & Intake**
   - Capture signals (logs, traces, alerts) and classify severity.
   - Create a minimal repro goal; log HARD constraints (uptime, data safety).
2. **Reproduce**
   - Build minimal failing case; note environment and dataset.
   - Record what was tried; store artifacts under `resources/`.
3. **Isolate**
   - Use hypothesis-driven narrowing (binary search, feature flags, diff analysis).
   - Trace data flow; identify confidence ceiling for suspected root causes.
4. **Design & Implement Fix**
   - Choose smallest safe change; plan rollback.
   - Add/adjust tests in `tests/` for the repro path.
5. **Validate**
   - Run unit/integration/perf checks; verify no new errors.
   - Confirm logs/metrics recovered; update `references/` with evidence links.
6. **Document & Hand-off**
   - Summarize root cause, fix, test coverage, and residual risk.
   - Capture lessons in `examples/` for future cases.

### Output Format
- Intent + constraints (HARD/SOFT/INFERRED) with confirmations.
- Repro notes, suspected root causes with **Confidence: X.XX (ceiling: TYPE Y.YY)**.
- Fix plan, validation steps, and rollback instructions.
- Evidence links and updated artifacts.

### Validation Checklist
- [ ] Repro established; scope and environment captured.
- [ ] Root cause stated with ceilinged confidence.
- [ ] Tests added/updated; all suites relevant to the change pass.
- [ ] Rollback path defined; production impact assessed.
- [ ] Documentation and artifacts stored in `resources/` and `references/`.

### MCP / Memory Tags
- Namespace: `skills/delivery/debugging/{project}/{incident}`
- Tags: `WHO=debugging-{session}`, `WHY=skill-execution`, `WHAT=triage+fix`

Confidence: 0.70 (ceiling: inference 0.70) - SOP aligns with skill-forge structure-first and prompt-architect confidence/constraint rules.
