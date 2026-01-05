---
name: sop-api-development
description: End-to-end REST/HTTP API delivery SOP with clear contracts, TDD focus, and deployment readiness.
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
Design, build, and release APIs with reliable contracts, tests, documentation, and rollout controls.

### Trigger Conditions
- **Positive:** new REST endpoints, breaking changes, contract updates, or API hardening.
- **Negative:** doc-only requests (route to `documentation`) or non-API feature builds (route to `feature-dev-complete`).

### Guardrails
- **Structure-first:** ensure `examples/`, `tests/`, `resources/`, `references/` accompany `SKILL.md`.
- **Constraint extraction:** HARD (SLAs, auth, compliance), SOFT (style, versioning), INFERRED (traffic patterns, migration risk); confirm inferred.
- **Contract-first:** define OpenAPI/JSON schema before coding; keep error model and versioning explicit.
- **Confidence ceilings:** `{inference/report:0.70, research:0.85, observation/definition:0.95}` across design, performance, and rollout claims.

### Execution Phases
1. **Intent & Contract**
   - Capture objectives, consumers, and constraints; produce OpenAPI/JSON schema; store in `resources/`.
   - Define auth, rate limits, idempotency, and error formats.
2. **Plan & Test Design**
   - Outline endpoints, data flows, and dependencies; map acceptance criteria to tests in `tests/`.
   - Identify migration/deprecation plan; log in `references/`.
3. **Implement**
   - Build handlers, validation, and persistence with smallest increments.
   - Keep logging/observability consistent; add feature flags if needed.
4. **Validate**
   - Run unit/integration/contract tests; fuzz critical inputs; load/perf sample if relevant.
   - Verify backward compatibility and security (authz/authn, input sanitization).
5. **Document & Release**
   - Update API docs and changelog; provide rollout/rollback steps.
   - Summarize evidence and **Confidence: X.XX (ceiling: TYPE Y.YY)**.

### Output Format
- Constraint ledger (HARD/SOFT/INFERRED) with confirmations.
- Contract artifacts, implementation status, and validation results.
- Release/rollback guidance and evidence links.
- Confidence statement with ceiling.

### Validation Checklist
- [ ] Contracts defined and versioned; constraints confirmed.
- [ ] Tests mapped to acceptance criteria; results captured.
- [ ] Security, auth, and error models validated.
- [ ] Docs and changelog updated; references stored.
- [ ] Confidence ceilings applied to claims and rollout readiness.

### MCP / Memory Tags
- Namespace: `skills/delivery/sop-api-development/{service}/{version}`
- Tags: `WHO=sop-api-development-{session}`, `WHY=skill-execution`, `WHAT=api-delivery`

Confidence: 0.70 (ceiling: inference 0.70) - SOP mirrors skill-forge structure-first and prompt-architect constraint/ceiling rules.
