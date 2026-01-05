---
name: feature-dev-complete
description: End-to-end feature delivery (discovery → design → build → test → release) with explicit quality gates and confidence ceilings.
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
Deliver production-ready features with clear scope, architecture, validated code, docs, and release notes.

### Trigger Conditions
- **Positive:** net-new feature requests, multi-story implementations, end-to-end delivery ownership.
- **Negative:** pure bugfix (route to `debugging`/`smart-bug-fix`) or doc-only asks (route to `documentation`).

### Guardrails
- **Structure-first:** ensure `examples/`, `tests/`, `resources/` exist; `references/` recommended for ADRs.
- **Constraint extraction:** HARD (scope, deadlines, SLAs), SOFT (tech preferences), INFERRED (UX tone); confirm inferred.
- **Confidence ceilings:** `{inference/report:0.70, research:0.85, observation/definition:0.95}` for requirements, estimates, and validation claims.
- **Quality gates:** architecture review, security/perf considerations, test coverage, rollback and release notes.

### Execution Phases
1. **Discovery & Framing**
   - Clarify intent, success metrics, dependencies, and blockers.
   - Produce acceptance criteria and definition of done; tag constraints.
2. **Design**
   - Draft architecture, sequence diagrams, and data contracts; store in `resources/`.
   - Validate feasibility; capture alternatives with ceilings on risk/effort.
3. **Plan & Traceability**
   - Break down into stories/tasks/subtasks with ownership and status.
   - Define tests to add; map them to acceptance criteria.
4. **Build**
   - Implement smallest viable increments; keep code + tests paired.
   - Maintain changelog notes and migration steps if schema/config changes occur.
5. **Validate**
   - Run unit/integration/e2e and non-functional checks as applicable.
   - Ensure rollback plan; document results in `tests/` artifacts.
6. **Document & Release**
   - Update READMEs/API docs as needed; prepare release notes.
   - Store decisions in `references/`; add reusable flows to `examples/`.

### Output Format
- Feature summary + constraints (HARD/SOFT/INFERRED) and confirmations.
- Design decisions, task breakdown, and planned/actual validation.
- Delivery state (ready/requires follow-up) and **Confidence: X.XX (ceiling: TYPE Y.YY)**.

### Validation Checklist
- [ ] Acceptance criteria confirmed; constraints logged and resolved/waived.
- [ ] Design reviewed; risks and alternatives recorded.
- [ ] Tests added/updated; results captured; rollback path defined.
- [ ] Docs/release notes updated; artifacts stored in `resources/` and `references/`.
- [ ] Confidence ceilings attached to estimates and claims.

### MCP / Memory Tags
- Namespace: `skills/delivery/feature-dev-complete/{project}/{feature}`
- Tags: `WHO=feature-dev-complete-{session}`, `WHY=skill-execution`, `WHAT=delivery`

Confidence: 0.70 (ceiling: inference 0.70) - SOP follows skill-forge structure-first and prompt-architect constraint/ceiling requirements.
