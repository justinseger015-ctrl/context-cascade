---
skill: codex-auto
description: Run Codex CLI in Full Auto mode for unattended, sandboxed prototyping and repair
tags: [codex, openai, prototyping, automation, full-auto, scaffolding]
version: 1.1.0
source: /skills/references/codex-auto.md
related-skills: [codex-reasoning, audit-pipeline, functionality-audit]
---

## Purpose
Enable autonomous code changes in a secure sandbox. Codex Full Auto can read/write/execute without approvals, making it ideal for overnight scaffolding, repair loops, and exploratory prototyping. This doc follows Prompt Architect structure (intent → constraints → optimized flow) and Skill Forge guardrails (structure-first, validation, explicit confidence ceilings).

## When to Use
- Rapidly scaffold a feature or project without supervision.
- Run iterative fix/test loops in isolation while you are away.
- Explore alternative implementations while protecting the primary workspace.

## When Not to Use / Reroute
- Needs human-in-the-loop approvals or production access.
- Tasks focused on prompt shaping → `foundry/prompt-architect`.
- New skill creation → `foundry/skill-forge`.

## Inputs (constraint extraction)
- **HARD**: Task goal, sandbox path, time budget, allowed command set.
- **SOFT**: Style/tech preferences, test command, performance/security expectations.
- **INFERRED**: Rollback plan, artifact export location; confirm before launch.

## SOP
1. **Initialize Sandbox**
   - Create/verify isolated workspace; ensure network is disabled.
   - Seed with minimal instructions and constraints; log WHO/WHY context.
2. **Autonomous Loop**
   - Invoke `codex --full-auto "<task>"` with clear success criteria.
   - Monitor for stuck loops; cap runtime and step count.
   - Preserve interim artifacts for inspection.
3. **Validation & Handoff**
   - Run declared tests and linters inside the sandbox.
   - Export diffs, logs, and artifacts; summarize changes and open risks.
   - Apply to main workspace only after human review.

## Quality Gates
- Sandbox only (no production writes); network off.
- Tests and linters passing inside sandbox.
- Diff review completed before promotion.
- Confidence statement with ceiling included in the summary.

## Anti-Patterns
- Letting Full Auto touch production directories.
- Skipping a final human review or test pass.
- Vague tasks without success criteria.
- Omitting confidence ceilings or English-only outputs.

## Usage Examples
```bash
# Scaffold an API
/codex-auto "Create Express REST API with JWT auth, SQLite persistence, Jest tests"

# Overnight refactor
/codex-auto "Refactor src/components to hooks; fix resulting tests; format codebase"
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Structured to mirror Prompt Architect and Skill Forge safeguards; increase confidence once sandbox validation artifacts are collected.
