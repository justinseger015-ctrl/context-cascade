---
skill: three-loop-integration-architecture
description: Three-loop integrated delivery system (Planning → Implementation → CI/CD Quality) with continuous feedback
tags: [orchestration, delivery, cicd, planning, quality]
version: 1.1.0
source: /skills/references/three-loop-integration-architecture.md
related-skills: [audit-pipeline, multi-model, cascade-orchestrator]
---

## Purpose
Coordinate three linked loops to deliver theater-free, production-grade software: Loop 1 (Planning), Loop 2 (Implementation), Loop 3 (CI/CD Quality). Written with Prompt Architect clarity and Skill Forge guardrails to keep structure, validation, and confidence ceilings explicit.

## Loop Overview
- **Loop 1 — Planning (discovery-planning-loop)**: Specification, research, MECE planning, pre-mortem risk analysis → produces a planning package.
- **Loop 2 — Implementation (development-swarm-loop)**: Multi-agent build with theater detection, integration, and coverage → produces a delivery package.
- **Loop 3 — CI/CD Quality (cicd-quality-loop)**: Hook-driven analysis, root-cause fixes, validation, and failure-pattern capture → produces feedback for Loop 1.

## Data Hand-offs (must be explicit)
- **Loop 1 → Loop 2**: `.claude/.artifacts/loop1-planning-package.json` (spec, research, plan, risks).
- **Loop 2 → Loop 3**: `.claude/.artifacts/loop2-delivery-package.json` (implementation, tests, theater baseline, coverage).
- **Loop 3 → Loop 1**: `.claude/.artifacts/loop3-failure-patterns.json` (patterns, root causes, prevention, premortem prompts).

## SOP
1. **Plan (Loop 1)**
   - Define scope, gather research, run pre-mortem, and produce planning package.
   - Quality gate: failure confidence < 3%, risks documented.
2. **Implement (Loop 2)**
   - Initialize swarm, eliminate theater, build and test, capture coverage.
   - Quality gate: theater cleared, tests passing, integration notes recorded.
3. **Validate (Loop 3)**
   - Run CI/CD hooks, RCA for failures, apply fixes, and log patterns.
   - Quality gate: 100% targeted checks pass; failure patterns exported.

## Quality Gates (global)
- Each loop must meet its gate before progressing.
- Artifacts are stored with paths and timestamps; lineage is preserved.
- Confidence ceilings declared in each loop summary (inference/report: 0.70, research: 0.85, observation/definition: 0.95).

## Anti-Patterns
- Skipping theater detection before integration.
- Advancing loops without exporting artifacts or citations.
- Mixing languages/notation in user-facing outputs; keep English only.
- Omitting confidence ceilings or risk deltas between loops.

## Usage Examples
```bash
# Kick off end-to-end
/three-loop-integration-architecture "Deliver feature X with planning → build → CI/CD validation"

# Run Loop 2 and Loop 3 using existing planning package
/development-swarm-loop --plan .claude/.artifacts/loop1-planning-package.json
/cicd-quality-loop --delivery .claude/.artifacts/loop2-delivery-package.json
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Reframed with Prompt Architect intent/constraints and Skill Forge structure/validation; raise confidence after verifying artifact availability per loop.
