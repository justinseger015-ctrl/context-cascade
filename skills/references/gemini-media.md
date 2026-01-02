---
skill: gemini-media
description: Generate images and videos via Gemini’s Imagen and Veo integrations for diagrams, UI mockups, and demos
tags: [gemini, image-generation, video-generation, visualization, media, imagen, veo]
version: 1.1.0
source: /skills/references/gemini-media.md
related-skills: [gemini-search, gemini-extensions, multi-model]
---

## Purpose
Create visual assets (images, diagrams, short videos) that Claude cannot generate natively. Structured with Prompt Architect clarity (intent, constraints, success) and Skill Forge guardrails (structure-first, validation, confidence ceilings).

## When to Use
- Architecture diagrams, flowcharts, UI mockups, or illustrative visuals for docs.
- Short demo or concept videos (onboarding, pipeline animations).

## When Not to Use / Reroute
- Editing existing media (use dedicated tooling).
- Text-only prompt refinement → `foundry/prompt-architect`.
- Skill creation → `foundry/skill-forge`.

## Inputs (constraint extraction)
- **HARD**: Media type (image/video), subject/scene, required resolution/aspect ratio, output path.
- **SOFT**: Style (wireframe, photorealistic), branding colors, duration (for video).
- **INFERRED**: Licensing/attribution needs, accessibility overlays — confirm before delivery.

## SOP
1. **Define Brief**
   - State purpose, audience, and key constraints (dimensions, style, duration).
   - Include must-have elements and avoid list.
2. **Generate with Gemini**
   - Run Gemini CLI with the brief; request multiple variations if needed.
   - Capture generation parameters (model, seed, resolution) for reproducibility.
3. **Validate & Export**
   - Check alignment to constraints; ensure no sensitive content.
   - Save to agreed path; provide alt text and refinement suggestions.

## Quality Gates
- Dimensions, style, and content match the brief.
- No sensitive data or trademarked assets unless approved.
- Confidence ceiling declared; outputs and explanations in English.

## Anti-Patterns
- Vague prompts without size/style targets.
- Skipping alt text or accessibility notes.
- Omitting generation parameters or save location.

## Usage Examples
```bash
/gemini-media "Create a flowchart for password reset: request → email → link → new password → success" --type image
/gemini-media "Generate a dark-theme dashboard mockup with sidebar, metrics cards, and charts" --type image
/gemini-media "10s video: CI/CD pipeline animation from commit to deploy with captions" --type video
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Built with Prompt Architect clarity and Skill Forge validation; increase confidence after reviewing generated samples against the brief.
