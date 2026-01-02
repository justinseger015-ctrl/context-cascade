---
skill: codex-reasoning
description: Use GPT-5-Codex for alternative reasoning paths, second opinions, and algorithmic variants
tags: [codex, openai, gpt-5-codex, reasoning, alternative-solutions]
version: 1.1.0
source: /skills/references/codex-reasoning.md
related-skills: [codex-auto, multi-model, audit-pipeline]
---

## Purpose
Provide a deliberate second viewpoint from GPT-5-Codex to complement Claude’s reasoning. Aligns to Prompt Architect framing (clarify intent and constraints) and Skill Forge guardrails (structure-first, validation, explicit confidence ceilings).

## When to Use
- You want alternative architectures, algorithms, or optimization strategies.
- You need a tie-breaker or sanity check on a proposed approach.
- You are blocked and want a fresh reasoning trajectory.

## When Not to Use / Reroute
- Routine implementation where consensus already exists.
- Prompt reshaping → `foundry/prompt-architect`.
- Net-new skill definition → `foundry/skill-forge`.

## Inputs (constraint extraction)
- **HARD**: Problem statement, constraints (performance, memory, compatibility), target language/stack.
- **SOFT**: Preferences (FP vs OOP, recursion vs iterative), readability vs speed.
- **INFERRED**: Deployment environment, latency/SLO expectations — confirm before accepting.

## SOP
1. **Frame the Question**
   - Define the intent and constraints explicitly; include edge cases.
   - Provide current solution sketch to avoid re-deriving basics.
2. **Codex Exploration**
   - Query GPT-5-Codex for 1–3 alternative paths; request trade-offs and complexity notes.
   - Ask for failure modes and mitigations.
3. **Validation & Integration**
   - Compare alternatives against constraints; run quick benchmarks/tests where applicable.
   - Select or merge the best elements; document decision and risks.

## Quality Gates
- Alternatives include trade-offs, complexity, and edge cases.
- At least one concrete example or pseudocode path provided.
- English-only output with explicit confidence ceiling.

## Anti-Patterns
- Accepting Codex output without constraints, tests, or comparisons.
- Letting stylistic preference trump hard requirements.
- Omitting a confidence statement or evidence trail.

## Usage Examples
```bash
/codex-reasoning "Propose alternative approaches to rate limiting for a multi-tenant API in Node.js"
/codex-reasoning "Second opinion: optimize Dijkstra implementation for dense graphs; Python preferred"
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Structured with Prompt Architect intent/constraint clarity and Skill Forge validation checkpoints; raise confidence after benchmarking chosen alternative.
