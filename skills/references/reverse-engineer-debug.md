---
skill: reverse-engineer-debug
description: Perform systematic reverse engineering and root-cause analysis to isolate and fix failures
tags: [debugging, rca, root-cause-analysis, reverse-engineering, investigation, forensics]
version: 1.1.0
source: /skills/references/reverse-engineer-debug.md
related-skills: [audit-pipeline, functionality-audit, codex-reasoning]
---

## Purpose
Diagnose mysterious or intermittent failures by working backward from symptoms to true root causes. Uses Prompt Architect framing (clear intent, constraints, evidence) and Skill Forge guardrails (structure-first, adversarial validation, confidence ceilings).

## When to Use
- Production incidents, intermittent errors, performance regressions, or post-deploy surprises.
- Legacy or opaque systems that need forensic analysis.

## When Not to Use / Reroute
- Straightforward bug fixes already localized by tests.
- Prompt-only refinement → `foundry/prompt-architect`.
- Skill authoring → `foundry/skill-forge`.

## Inputs (constraint extraction)
- **HARD**: Symptom description, reproduction steps (if any), environment, recent changes, logs/traces.
- **SOFT**: Business impact, SLO/SLA thresholds, rollback options, observability tools available.
- **INFERRED**: Data sensitivity, access boundaries, third-party dependencies — confirm before investigation.

## SOP
1. **Evidence Intake**
   - Capture error messages, timestamps, traces, repro steps; build a timeline.
   - Separate symptoms from hypotheses; avoid premature conclusions.
2. **Hypothesis & Trace**
   - Generate multiple hypotheses; design minimal experiments.
   - Trace from failure point backward through dependencies (code, config, infra).
3. **Validate & Fix**
   - Confirm root cause explains all symptoms.
   - Propose targeted fixes with regression checks; run tests/benchmarks where applicable.
   - Document prevention steps and monitoring hooks.

## Quality Gates
- Root cause is evidenced (file:line/config/endpoint) and explains all symptoms.
- Repro case validated pre/post fix; tests or benchmarks updated.
- Confidence ceiling included; English-only RCA summary.

## Anti-Patterns
- Anchoring on first hypothesis; skipping parallel hypotheses.
- Ignoring recent changes or environmental factors.
- Shipping fixes without validation or prevention steps.
- Omitting confidence ceilings or evidence links.

## Usage Examples
```bash
/reverse-engineer-debug "Intermittent 500s: 'Cannot read property id of undefined' after db migration"
/reverse-engineer-debug "Checkout timeouts in production after latest deployment; affects ~10% requests"
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Built with Prompt Architect clarity and Skill Forge validation; confidence increases after reproducing and testing the identified root cause.
