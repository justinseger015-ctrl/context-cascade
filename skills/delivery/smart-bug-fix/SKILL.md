---
name: smart-bug-fix
description: Advanced defect eradication with hypothesis-driven RCA, guarded fixes, and comprehensive validation.
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
Handle complex or high-risk bugs with structured root-cause analysis, evidence-backed fixes, and regression protection.

### Trigger Conditions
- **Positive:** production-grade defects, performance degradations, security/regression issues, multi-service failures.
- **Negative:** simple fixes or greenfield work (route to `debugging` or `feature-dev-complete` respectively).

### Guardrails
- **Structure-first:** maintain `examples/`, `tests/`, `resources/`, `references/` for each incident.
- **Constraint extraction:** HARD (blast radius, uptime targets, data safety), SOFT (tooling preferences), INFERRED (rollback tolerance) — confirm inferred.
- **Hypothesis discipline:** every suspected cause must include evidence and ceilinged confidence.
- **Confidence ceilings:** `{inference/report:0.70, research:0.85, observation/definition:0.95}` on diagnosis and fix claims.
- **Safety:** avoid production mutations without backups; preserve audit logs.

### Execution Phases
1. **Intake & Repro**
   - Capture signals, incidents, and constraints; build minimal repro.
   - Store logs/traces in `resources/`.
2. **Root-Cause Analysis**
   - Form hypotheses with evidence; iterate 5-Whys; tag ceilings.
   - Document rejected hypotheses in `references/` for reuse.
3. **Fix Design**
   - Choose minimal, reversible change; plan rollout + rollback.
   - Define required tests; stage diff for review.
4. **Implement & Validate**
   - Implement fix; add regression tests in `tests/`.
   - Run unit/integration/perf/security checks as applicable; record outputs.
5. **Stabilize & Document**
   - Monitor post-fix signals; ensure no secondary failures.
   - Summarize cause, fix, validation, residual risk, and **Confidence: X.XX (ceiling: TYPE Y.YY)**.

### Output Format
- Constraints ledger (HARD/SOFT/INFERRED) with confirmations.
- Hypotheses, evidence, and status (accepted/rejected) with confidence ceilings.
- Fix plan, validation results, rollback path.
- Artifacts/links and next steps.

### Validation Checklist
- [ ] Repro confirmed; blast radius understood.
- [ ] Hypotheses evidenced; ceilings stated; rejected items logged.
- [ ] Tests added/updated and passing; monitoring plan noted.
- [ ] Rollback path defined; artifacts stored in `resources/` and `references/`.
- [ ] Confidence ceilings attached to diagnosis and validation claims.

### MCP / Memory Tags
- Namespace: `skills/delivery/smart-bug-fix/{project}/{incident}`
- Tags: `WHO=smart-bug-fix-{session}`, `WHY=skill-execution`, `WHAT=complex-fix`

Confidence: 0.70 (ceiling: inference 0.70) - SOP incorporates skill-forge structure-first and prompt-architect constraint/ceiling discipline.
