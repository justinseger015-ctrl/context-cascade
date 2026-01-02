---
skill: master-skills-index
description: Canonical directory of all skills with pointers to their locations and summaries
tags: [index, catalog, routing, orchestration]
version: 1.1.0
source: /skills/references/master-skills-index.md
related-skills: [multi-model, audit-pipeline, prompt-architect, skill-forge]
---

## Purpose
Provide a concise, current inventory of all skills with paths and summaries to support fast routing. Structured with Prompt Architect clarity (intent, constraints, success) and enforced by Skill Forge guardrails (structure-first, validation, confidence ceilings).

## When to Use
- You need to find the right skill quickly by category or capability.
- Building orchestrations or pipelines that depend on multiple skills.
- Verifying coverage or detecting gaps in the skill suite.

## When Not to Use / Reroute
- Creating or improving a skill → `foundry/skill-forge`.
- Prompt-only tuning → `foundry/prompt-architect`.
- Deep research on a single skill → open its specific `SKILL.md`.

## Inputs (constraint extraction)
- **HARD**: Desired category or skill name pattern, freshness requirement.
- **SOFT**: Output format (table, list), level of detail.
- **INFERRED**: Deprecated skill handling, cross-links to references — confirm before publishing.

## SOP
1. **Gather & Validate**
   - Enumerate skills and categories; confirm paths and descriptions from source `SKILL.md`.
2. **Summarize**
   - Present category tables with name, path, and a one-line summary.
   - Flag missing descriptions or deprecated entries.
3. **Publish**
   - Deliver in English; include update timestamp and confidence.
   - Note any gaps requiring Skill Forge follow-up.

## Quality Gates
- Paths resolve to real skill directories.
- Descriptions pulled or restated from authoritative `SKILL.md`.
- Confidence ceiling included; English-only output.

## Anti-Patterns
- Listing skills without verifying path existence.
- Omitting categories or leaving stale summaries unmarked.
- Missing confidence statements.

## Example Structure
```
## Foundry
| Skill | Path | Summary |
|-------|------|---------|
| prompt-architect | `foundry/prompt-architect` | Optimize prompts for clarity and epistemic hygiene |
| skill-forge | `foundry/skill-forge` | Create production-grade skill definitions with validation loops |
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Recast with Prompt Architect/Skill Forge discipline; raise confidence after reconciling against the current repo snapshot.
