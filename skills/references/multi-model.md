---
skill: multi-model
description: Route work to the optimal model (Gemini, Codex, Claude) based on task requirements
tags: [orchestration, multi-model, routing, automation, gemini, codex]
version: 1.1.0
source: /skills/references/multi-model.md
related-skills: [gemini-megacontext, gemini-search, gemini-media, codex-auto, codex-reasoning]
---

## Purpose
Automatically select the right model/skill for each subtask, blending Gemini (search, mega-context, media, extensions), Codex (full-auto, alternative reasoning), and Claude (implementation, integration). Follows Prompt Architect clarity and Skill Forge guardrails for structure, validation, and confidence ceilings.

## When to Use
- Tasks that span research, prototyping, and documentation.
- You are unsure which model is best for a given subtask.
- You want a repeatable routing decision with rationale.

## When Not to Use / Reroute
- Single-model tasks with known best fit (e.g., pure prompt design → `prompt-architect`).
- Skill authoring → `foundry/skill-forge`.

## Inputs (constraint extraction)
- **HARD**: Overall objective, subtask list, constraints (data sensitivity, runtime, network).
- **SOFT**: Cost/time budgets, depth vs breadth preference, format for outputs.
- **INFERRED**: Parallelization tolerance, artifact storage paths — confirm before execution.

## SOP
1. **Task Decomposition**
   - Break the objective into subtasks; tag each with capabilities needed.
2. **Routing Decision**
   - Map subtasks to models: Gemini (search/mega-context/media/extensions), Codex (full-auto/prototyping/alt reasoning), Claude (integration/refinement).
   - Record rationale and any ordering/parallelism.
3. **Execute & Integrate**
   - Run routed skills; capture outputs and citations.
   - Integrate results in Claude; resolve conflicts; finalize deliverable.

## Quality Gates
- Each subtask has an explicit model choice and rationale.
- Outputs integrated with clear lineage and citations.
- Confidence ceiling included; English-only summary.

## Anti-Patterns
- Defaulting to one model without considering constraints.
- Mixing sensitive data into external tools without checks.
- Omitting integration/validation after parallel runs.

## Usage Examples
```bash
/multi-model "Research React 19 changes, scaffold a dashboard, and generate UI mockups"
# Routes: gemini-search → codex-auto → gemini-media → Claude integration

/multi-model "Understand architecture of a 40K LOC repo and propose refactor"
# Routes: gemini-megacontext → codex-reasoning (alternatives) → Claude synthesis
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Mirrors Prompt Architect clarity and Skill Forge validation; confidence rises after executing routed subtasks and validating outputs.
