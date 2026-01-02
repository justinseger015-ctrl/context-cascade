---
skill: audit-pipeline
description: Three-phase code quality pipeline that removes theater, verifies functionality in a sandbox, and polishes style for production readiness
tags: [audit, quality, pipeline, orchestration, theater, functionality, style, codex]
version: 1.1.0
source: /skills/references/audit-pipeline.md
related-skills: [theater-detection-audit, functionality-audit, style-audit, codex-auto, codex-reasoning]
---

## Purpose
Deliver a theater-free, production-ready codebase through a fixed sequence: (1) detect and remediate theater, (2) validate functionality with sandboxed fixes, and (3) refine style and maintainability. Written in the Prompt Architect pattern (intent → constraints → optimized plan) and enforced with Skill Forge guardrails (structure-first, adversarial validation, confidence ceilings).

## When to Use
- You need a repeatable audit that ends with tested, production-quality code.
- You suspect placeholders, mocks, or stubs and want them eliminated before testing.
- You want Codex Full Auto to iterate on fixes safely inside a sandbox.

## When Not to Use / Reroute
- Pure prompt optimization → `foundry/prompt-architect`.
- Net-new skill creation → `foundry/skill-forge` or `foundry/micro-skill-creator`.
- Single-file style tweaks without execution risk → `style-audit` directly.

## Inputs (constraint extraction)
- **HARD**: Target scope (paths/services), install/runtime prerequisites, canonical test/command to run.
- **SOFT**: Severity threshold for blocking issues, minimum coverage, preferred style guide.
- **INFERRED**: Ownership/approvers, environment parity, rollout constraints — confirm before acting.

## Outputs
- Phase reports (theater findings, functionality results, style deltas) with file:line citations.
- Applied fixes or explicit deferrals with rationale.
- Confidence statement per phase using ceiling syntax (inference/report: 0.70, research: 0.85, observation/definition: 0.95).

## SOP (structure-first, three phases)
1. **Theater Detection**
   - Scan for mocks, TODO/FIXME, stubbed logic, hardcoded data.
   - Prioritize by user impact and execution risk; block progression until resolved or approved.
2. **Functionality Audit (sandboxed)**
   - Run the declared test/command in isolation.
   - For each failure: capture evidence → iterate with `codex-auto --full-auto` inside the sandbox → retest until green.
   - Record root causes, fixes, and residual risks.
3. **Style & Quality**
   - Run linters/formatters and manual readability/security checks.
   - Re-run tests after refactors; ensure no regressions.
   - Summarize polish deltas and any remaining quality debt.

## Quality Gates
- Theater backlog cleared or formally accepted.
- Tests pass in sandbox after Codex iterations.
- Style/security/performance checks clean; no new regressions.
- English-only output with explicit confidence ceilings.

## Anti-Patterns
- Skipping theater detection before testing.
- Applying Codex changes outside a sandbox or without retests.
- Delivering findings without file:line proof.
- Omitting confidence ceilings or mixing non-English output.

## Usage Examples
```bash
# Full pipeline with strict style
/audit-pipeline "Audit src/api and services/payments; use codex-auto for fixes; enforce strict style"

# Theater-only triage
/audit-pipeline "Phase 1 only for packages/auth"
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Rewritten with Prompt Architect structure and Skill Forge guardrails; project-specific evidence will raise confidence.
