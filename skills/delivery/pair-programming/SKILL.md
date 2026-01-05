---
name: pair-programming
description: Structured AI-assisted pairing with clear roles, cadence, and validation to keep quality and knowledge flow high.
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
Deliver collaborative coding sessions (driver/navigator/switch/TDD) with explicit guardrails, shared context, and validated output.

### Trigger Conditions
- **Positive:** collaborative coding, live code review, debugging together, mentoring/onboarding, TDD sessions.
- **Negative:** solo quick fixes or documentation-only asks.

### Guardrails
- **Structure-first:** maintain `examples/`, `tests/`, `resources/`, `references/` to capture session artifacts.
- **Constraint extraction:** HARD (timebox, repo rules, CI gates), SOFT (tooling preferences), INFERRED (communication cadence) — confirm inferred.
- **Cadence:** rotate roles every 20–30 minutes; schedule breaks; keep decisions in notes.
- **Confidence ceilings:** `{inference/report:0.70, research:0.85, observation/definition:0.95}` for recommendations and reviews.
- **Psychological safety:** critique code, not people; narrate reasoning.

### Execution Phases
1. **Session Setup**
   - Define goal, CTA (e.g., implement test, fix bug), and done criteria.
   - Choose mode (driver/navigator/switch/TDD) and tools; record constraints.
2. **Context Load**
   - Review relevant files/tests; capture open questions; store in `resources/`.
3. **Collaborative Build**
   - Driver codes aloud; navigator challenges assumptions and tracks constraints.
   - Keep diffs small; log decisions and TODOs; add/adjust tests in `tests/`.
4. **Review & Validation**
   - Swap roles; run tests/linters; perform quick perf/security sanity checks.
   - Note confidence with ceilings for approvals or concerns.
5. **Close & Handoff**
   - Summarize changes, risks, and next steps; ensure commits/notes ready.
   - Save snippets and lessons in `examples/`; cite references.

### Output Format
- Goal + constraints (HARD/SOFT/INFERRED) with confirmations.
- Mode chosen, decisions made, and validation results.
- Action items/next steps with owners.
- Evidence and **Confidence: X.XX (ceiling: TYPE Y.YY)**.

### Validation Checklist
- [ ] Constraints agreed; mode + cadence set.
- [ ] Tests/linters run; results captured.
- [ ] Decisions and risks documented; references linked.
- [ ] Confidence ceilings noted for approvals/concerns.
- [ ] Artifacts saved to `examples/` or `resources/`.

### MCP / Memory Tags
- Namespace: `skills/delivery/pair-programming/{project}/{session}`
- Tags: `WHO=pair-programming-{session}`, `WHY=skill-execution`, `WHAT=collab-coding`

Confidence: 0.70 (ceiling: inference 0.70) - SOP integrates skill-forge structure-first and prompt-architect constraint/ceiling guidance.
