---
skill: gemini-search
description: Use Gemini’s Google Search grounding for real-time web research with citations
tags: [gemini, web-search, real-time, documentation, current-info]
version: 1.1.0
source: /skills/references/gemini-search.md
related-skills: [gemini-megacontext, multi-model, gemini-extensions]
---

## Purpose
Fetch current web information (docs, advisories, changelogs) with grounded citations. Applies Prompt Architect clarity (intent, constraints, success) and Skill Forge guardrails (structure-first, validation, confidence ceilings).

## When to Use
- Need up-to-date API docs, breaking changes, security advisories, or version status.
- Validating best practices against current standards or comparing technologies.

## When Not to Use / Reroute
- Information is local to the repo or offline resources.
- Prompt-only rewriting → `foundry/prompt-architect`.
- Skill authoring → `foundry/skill-forge`.

## Inputs (constraint extraction)
- **HARD**: Query/topic, recency or version targets, citation requirement.
- **SOFT**: Preferred sources (vendor docs, RFCs), format (bullets/table), depth.
- **INFERRED**: Regional/language bias, cache/TTL expectations — confirm before run.

## SOP
1. **Frame the Query**
   - Specify version/date filters and desired output structure.
2. **Search & Ground**
   - Run Gemini with search grounding; collect top relevant sources.
   - Extract key findings with URLs.
3. **Validate & Present**
   - Check consistency across sources; flag conflicts.
   - Summarize in English with citations and confidence ceiling.

## Quality Gates
- At least two corroborating sources for critical claims.
- Explicit URLs cited; conflicting info highlighted.
- Confidence ceiling included; English-only output.

## Anti-Patterns
- Using vague queries without recency/version constraints.
- Omitting citations or returning vendor marketing without verification.
- Failing to note conflicts or uncertainties.

## Usage Examples
```bash
/gemini-search "React 19 breaking changes and migration steps" 
/gemini-search "Latest Stripe API auth methods (2025) with citations"
/gemini-search "Recent CVEs for lodash and remediation guidance"
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Built with Prompt Architect framing and Skill Forge validation; increase confidence after verifying cited sources.
