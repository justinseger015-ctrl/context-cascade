---
skill: gemini-megacontext
description: Analyze entire codebases with Gemini’s 1M-token context for architecture, dependency, and pattern mapping
tags: [gemini, codebase-analysis, architecture, large-context, multi-file]
version: 1.1.0
source: /skills/references/gemini-megacontext.md
related-skills: [gemini-search, multi-model, reverse-engineer-debug]
---

## Purpose
Load and reason over whole codebases (≈30K LOC) in a single pass. Uses Prompt Architect framing (explicit intent/constraints) and Skill Forge guardrails (structure-first, validation, confidence ceilings) to avoid vague, unfocused analysis.

## When to Use
- Need a holistic architecture map, dependency graph, or cross-cutting pattern search.
- Preparing migrations, large refactors, or security/quality sweeps that require global context.

## When Not to Use / Reroute
- Small-module questions → Claude local analysis.
- Prompt-only improvements → `foundry/prompt-architect`.
- Skill authoring → `foundry/skill-forge`.

## Inputs (constraint extraction)
- **HARD**: Repository root, scope include/exclude patterns, primary questions, output format.
- **SOFT**: Priority areas (auth, data, performance), file citation requirements, diagram needs.
- **INFERRED**: Size limits, sensitive file handling, redaction rules — confirm before run.

## SOP
1. **Scope & Questions**
   - Define target directories and explicit questions (architecture, endpoints, migrations).
   - Set output expectations (markdown summary, tables, diagrams).
2. **Gemini Analysis**
   - Run Gemini CLI with `--all-files` (or equivalent) under the defined scope.
   - Capture key findings: components, interactions, hotspots, anti-patterns.
3. **Validate & Summarize**
   - Ensure findings map to asked questions and cite file:line where possible.
   - Flag uncertainties; propose follow-up focused analyses.

## Quality Gates
- Answers each declared question with evidence.
- Provides citations/paths for claims; highlights unknowns.
- Confidence ceiling included; English-only outputs.

## Anti-Patterns
- Running without scope filters on very large repos (noisy results).
- Returning unsourced claims or missing confidence ceilings.
- Mixing unrelated tasks (refactor + design + audit) into one run.

## Usage Examples
```bash
/gemini-megacontext "Map all auth flows and data stores across the repo; include file citations"
/gemini-megacontext "Identify all API endpoints and their auth methods; produce a dependency table"
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Structured with Prompt Architect clarity and Skill Forge validation; confidence rises after inspecting Gemini output and citations.
