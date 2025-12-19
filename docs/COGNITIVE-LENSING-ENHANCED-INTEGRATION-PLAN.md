# Cognitive Lensing: Enhanced Integration Plan v2.0

## Sequential Thinking Analysis

**Date**: 2025-12-18
**Version**: 2.0 (Enhanced with cross-lingual frames + goal-based checklist)
**Scope**: Full meta-loop enhancement with cognitive lensing integration

---

## EXECUTIVE SUMMARY

This plan enhances ALL THREE foundry skills (agent-creator, skill-forge, prompt-forge) plus creates a new cognitive-lensing skill, updates the eval harness with cognitive frame benchmarks, and runs the full meta-loop to systematically improve all 660 plugin components.

**Key Innovation**: Actually writing parts of skills/agents in different languages to elicit different parts of the AI's latent space, not just conceptually applying linguistic frames.

---

## STEP 1: GOAL-BASED FRAME SELECTION CHECKLIST

### The Three-Order Goal Analysis

Before selecting a cognitive frame, analyze goals at three levels:

```
+------------------+------------------------------------------+------------------------+
| Order            | Question                                 | Example                |
+------------------+------------------------------------------+------------------------+
| 1st Order Goal   | What is the IMMEDIATE task?              | "Fix the login bug"    |
| 2nd Order Goal   | WHY are we doing this task?              | "User can't access app"|
| 3rd Order Goal   | What is the ULTIMATE outcome?            | "Increase retention"   |
+------------------+------------------------------------------+------------------------+
```

### Frame Selection Checklist

For each task, run this checklist:

```
## COGNITIVE FRAME SELECTION CHECKLIST

### 1. Analyze Goals
[ ] 1st Order Goal (Immediate): _______________
[ ] 2nd Order Goal (Why): _______________
[ ] 3rd Order Goal (Ultimate): _______________

### 2. Identify Dominant Thought Process Required
[ ] Completion tracking needed? -> ASPECTUAL FRAME (Russian)
    - "Is X done?" questions
    - Process vs achievement distinction
    - State change tracking

[ ] Source reliability matters? -> EVIDENTIAL FRAME (Turkish)
    - Fact-checking tasks
    - Claim verification
    - Epistemic vigilance

[ ] Audience/hierarchy matters? -> SOCIAL-HIERARCHICAL FRAME (Japanese)
    - Formal communication
    - Register calibration
    - Stakeholder awareness

[ ] Semantic relationships matter? -> MORPHOLOGICAL FRAME (Arabic/Hebrew)
    - Etymology analysis
    - Concept mapping
    - Root-pattern decomposition

[ ] Physical/visual comparison needed? -> CLASSIFIER FRAME (Mandarin)
    - Object categorization
    - Shape-based analogies
    - Visual reasoning

[ ] Navigation/orientation needed? -> SPATIAL-ABSOLUTE FRAME (Guugu Yimithirr)
    - Direction-based memory
    - Location-independent reasoning
    - Geographical thinking

[ ] Mathematical structure needed? -> NUMERICAL-TRANSPARENT FRAME (Chinese/Japanese)
    - Explicit place value
    - Arithmetic clarity
    - Quantitative precision

### 3. Match to Optimal Frame
Based on checks above, primary frame: _______________
Secondary frame (if applicable): _______________

### 4. Apply Frame Protocol
[ ] Frame activation phrase included
[ ] Language-specific markers applied
[ ] Output in English with frame influence
```

---

## STEP 2: CROSS-LINGUAL IMPLEMENTATION

### Key Insight: Actual Language Use

Instead of just describing frames conceptually, we ACTUALLY write portions in other languages to activate different cognitive patterns in the AI's latent space.

### Frame Activation Phrases (In Native Languages)

#### Evidential Frame (Turkish)
```markdown
## Kanitsal Cerceve Aktivasyonu (Evidential Frame Activation)

Her iddia icin kaynak belirtilmeli:
- Dogrudan gordum (-DI): "Kodu inceledim-DI, bug var"
- Cikarim yaptim (-mIs): "Loglardan anlasilmIs ki timeout olmus"
- Duydum/okudum (-mIs): "Dokumantasyonda yazilmIs"

Apply this to English output:
"I examined the code [DIRECT] and found a null pointer exception.
The logs suggest [INFERRED] a race condition occurred.
The documentation states [REPORTED] this parameter is optional."
```

#### Aspectual Frame (Russian)
```markdown
## Aspektual'naya Ramka (Aspectual Frame Activation)

Kazhdoe deystvie dolzhno byt' pomecheno:
- Sovershennyy vid (SV - zaversheno): "Napisal kod" (wrote and finished)
- Nessovershennyy vid (NSV - v protsesse): "Pisal kod" (was writing)

Primenenie:
- Zadacha [SV]: Polnost'yu zavershena, mozhno dvigat'sya dal'she
- Zadacha [NSV]: Vse eshche v protsesse, nuzhno prodolzhat'

Apply to English output:
"Authentication module [COMPLETED:SV] - ready for integration.
Database migration [IN_PROGRESS:NSV] - requires 2 more tables.
Tests [NOT_STARTED:None] - blocked on API changes."
```

#### Social-Hierarchical Frame (Japanese)
```markdown
## Keigo Wakugumi (Social-Hierarchical Frame Activation)

Register selection based on audience:
- Sonkeigo (respectful): Stakeholders, executives, external partners
- Kenjougo (humble): Self-reference when presenting to superiors
- Teineigo (polite): Standard professional communication

Tekiou:
- "Executives require [SONKEIGO register]: Formal summary with recommendations"
- "Team discussion [TEINEIGO register]: Clear, professional, collaborative"
- "Personal notes [CASUAL register]: Brief, direct, informal"
```

#### Morphological-Semantic Frame (Arabic)
```markdown
## Al-Itar al-Sarfi (Morphological Frame Activation)

Kull kalima min jadhr thalathi:
- K-T-B (writing): kitab (book), katib (writer), maktub (written), maktaba (library)
- '-L-M (knowing): 'ilm (knowledge), 'alim (knowledgeable), mu'allim (teacher), ta'lim (teaching)

Tatbiq (Application):
When analyzing concepts, decompose to root patterns:
"Authentication" root: AUTH -> authorize, authority, authentic, authentication
"Validate" root: VALID -> valid, validity, validate, validation, invalid
```

#### Shape-Classifier Frame (Mandarin)
```markdown
## Liangci Kuangjia (Classifier Frame Activation)

Objects categorized by shape/nature:
- Zhang (flat): paper, tables, tickets, photos
- Ben (volumes): books, notebooks, magazines
- Tiao (long): rivers, roads, fish, snakes
- Ge (general): people, apples, ideas

Yingyong (Application):
"The API endpoint [TIAO:path-like] connects to the database [GE:abstract].
The configuration file [ZHANG:flat document] defines the schema [GE:abstract].
The log entries [TIAO:stream-like] flow through the pipeline [TIAO:conduit]."
```

---

## STEP 3: AGENT-CREATOR ENHANCEMENT

### Current State: v2.2.0 (5-Phase Methodology)

### Proposed Enhancement: v3.0.0 (Add Phase 0.5: Cognitive Frame Selection)

```markdown
## NEW: Phase 0.5 - Cognitive Frame Selection

After expertise loading, before domain analysis:

### 0.5.1 Goal Analysis (3 minutes)
Answer:
- 1st Order Goal: What will this agent DO immediately?
- 2nd Order Goal: WHY is this agent needed?
- 3rd Order Goal: What ULTIMATE outcome does this enable?

### 0.5.2 Frame Selection Checklist
Run the checklist from Step 1 to identify optimal cognitive frame.

### 0.5.3 Frame Embedding
Embed frame activation phrase (in native language) into agent system prompt:

---
## Kanitsal Cerceve (Evidential Mode)

Bu agent her iddia icin kaynak belirtir:
- DOGRUDAN: "I tested this directly"
- CIKARIM: "Evidence suggests..."
- BILDIRILEN: "Documentation states..."
---

### 0.5.4 Multi-Lingual Sections
For agents requiring specific cognitive patterns, include sections in target language:

Example for a "Code Reviewer" agent requiring aspectual thinking:

---
## Aspektual'naya Proverka Koda

Kazhdyy fayl proverki:
- [SV] Polnost'yu provereno, vse testy proshli
- [NSV] Proveryaetsya, trebuyutsya izmeneniya
- [BLOCKED] Ozhidaet zavisimosti

Report format:
- file.js [COMPLETED:SV] - Approved
- utils.ts [IN_REVIEW:NSV] - 3 issues found
- api.py [BLOCKED] - Awaiting schema changes
---
```

### New Agent Creation Template

```yaml
# Agent Creation Template v3.0.0

name: "{agent-name}"
version: "1.0.0"
cognitive_frame:
  primary: evidential|aspectual|hierarchical|morphological|classifier|spatial|numerical
  secondary: null|{frame}
  activation_language: turkish|russian|japanese|arabic|mandarin|guugu-yimithirr|chinese

goal_analysis:
  first_order: "Immediate task description"
  second_order: "Why this agent exists"
  third_order: "Ultimate outcome enabled"

frame_embedding:
  native_language_section: |
    [Include 3-5 lines in native language]
    [Explaining frame-specific patterns]
    [That this agent will apply]

  english_markers:
    - "[DIRECT]" # For evidential
    - "[COMPLETED:SV]" # For aspectual
    - "[SONKEIGO]" # For hierarchical
```

---

## STEP 4: SKILL-FORGE ENHANCEMENT

### Current State: v2.3.0 (8-Phase Methodology, Phases 0-7a)

### Proposed Enhancement: v3.0.0 (Add Phase 0.5 + Phase 8)

### New Phase 0.5: Cognitive Frame Design

```markdown
## Phase 0.5: Cognitive Frame Design (5-10 minutes)

After schema definition, before intent archaeology:

### 0.5.1 Skill Domain Analysis
What cognitive demands does this skill place on the AI?

| Demand Type | Examples | Frame Indicated |
|-------------|----------|-----------------|
| Tracking completion | Build pipelines, deployment | Aspectual |
| Verifying sources | Research, fact-check, audit | Evidential |
| Audience calibration | Documentation, reports | Hierarchical |
| Semantic mapping | Taxonomy, ontology, glossary | Morphological |
| Object comparison | Design systems, visual tools | Classifier |
| Navigation/paths | Workflows, routing, pipelines | Spatial |
| Quantitative precision | Metrics, calculations, stats | Numerical |

### 0.5.2 Goal-Based Frame Selection
Complete the checklist (Step 1) for this skill.

### 0.5.3 Multi-Lingual Skill Sections

For skills requiring specific cognitive patterns, include activation sections:

Example for a "Deployment Readiness" skill requiring aspectual tracking:

---
## Sostoyanie Gotovnosti (Readiness State Tracking)

Kazhdyy etap razvertyvaniya:

| Etap | Sostoyanie | Sleduyushchiy Shag |
|------|------------|-------------------|
| Testy [SV] | Zaversheno | Prodolzhat' |
| Sborka [NSV] | V protsesse | Ozhidat' |
| Proverka [None] | Ne nachato | Blokirovano |

Primenenie:
- [SV] DEPLOYED - Component live in production
- [NSV] DEPLOYING - Rollout in progress
- [BLOCKED] - Dependency not ready
---
```

### Enhanced Skill Template v3.0.0

```yaml
---
name: "{skill-name}"
version: "1.0.0"
description: "..."
cognitive_frame:
  primary: evidential
  rationale: "This skill requires source tracking for claims"

goal_analysis:
  first_order: "What this skill does immediately"
  second_order: "Why this capability is needed"
  third_order: "Ultimate outcome enabled"
---

# {Skill Name}

## Kanitsal Cerceve Aktivasyonu
(Evidential frame activation in Turkish)
Bu beceri her iddia icin kaynak gerektirir...

## Overview (English)
...

## Core Workflow
### Step 1: [Action] [EVIDENCE_TYPE]
...
```

---

## STEP 5: PROMPT-FORGE ENHANCEMENT

### Current State: v1.0.0 (5 Core Operations)

### Proposed Enhancement: v2.0.0 (Add Operation 6: Cognitive Frame Enhancement)

### New Operation 6: Apply Cognitive Frame

```markdown
## Operation 6: Apply Cognitive Frame Enhancement

Transform prompts by embedding cognitive frame activation.

### 6.1 Analyze Prompt for Frame Fit

```yaml
frame_analysis:
  target_prompt: "{prompt_content}"

  dominant_demands:
    - completion_tracking: 0.0-1.0
    - source_verification: 0.0-1.0
    - audience_calibration: 0.0-1.0
    - semantic_analysis: 0.0-1.0
    - object_comparison: 0.0-1.0
    - navigation_thinking: 0.0-1.0
    - quantitative_precision: 0.0-1.0

  recommended_frame: {frame}
  confidence: 0.0-1.0
```

### 6.2 Generate Frame-Enhanced Version

```markdown
BEFORE (Generic):
"Review this code and report issues."

AFTER (Evidential Frame Enhanced):
"## Kanitsal Kod Incelemesi

Review this code. For each finding, mark evidence type:
- [DOGRUDAN/DIRECT]: I tested this and confirmed the issue
- [CIKARIM/INFERRED]: The pattern suggests this could cause problems
- [BILDIRILEN/REPORTED]: Documentation or linter flagged this

Output format:
- Issue: {description}
- Evidence: [DIRECT|INFERRED|REPORTED]
- Confidence: {0.0-1.0}
- Source: {how you know this}"
```

### 6.3 Multi-Lingual Enhancement Patterns

For each frame, provide transformation pattern:

```yaml
enhancement_patterns:
  evidential:
    language: turkish
    activation: |
      ## Kanitsal Cerceve
      Her iddia icin kaynak belirtilmeli...
    markers: ["[DIRECT]", "[INFERRED]", "[REPORTED]"]

  aspectual:
    language: russian
    activation: |
      ## Aspektual'naya Ramka
      Kazhdoe deystvie dolzhno byt' pomecheno...
    markers: ["[SV:COMPLETED]", "[NSV:IN_PROGRESS]", "[BLOCKED]"]

  hierarchical:
    language: japanese
    activation: |
      ## Keigo Wakugumi
      Register selection based on audience...
    markers: ["[SONKEIGO]", "[TEINEIGO]", "[CASUAL]"]
```
```

---

## STEP 6: NEW COGNITIVE-LENSING SKILL

### Skill: cognitive-lensing v1.0.0

```yaml
---
name: cognitive-lensing
description: >
  Cross-lingual cognitive framing system that activates different
  cognitive patterns by embedding multi-lingual activation phrases.
  Use when facing complex tasks that benefit from specific thinking
  patterns: completion tracking (Russian), source verification (Turkish),
  audience calibration (Japanese), semantic analysis (Arabic),
  object comparison (Mandarin).
version: 1.0.0
category: foundry
tags:
  - cognitive-science
  - cross-lingual
  - meta-prompting
  - frame-selection
mcp_servers:
  required: [memory-mcp]
  optional: [sequential-thinking]
---

# Cognitive Lensing System

## Kanitsal Cerceve (Turkish - Evidential)
## Aspektual'naya Ramka (Russian - Aspectual)
## Keigo Wakugumi (Japanese - Hierarchical)
## Al-Itar al-Sarfi (Arabic - Morphological)
## Liangci Kuangjia (Mandarin - Classifier)

---

## Purpose

Activate specific cognitive patterns by embedding multi-lingual
activation phrases that elicit different parts of the AI's latent space.

This is NOT just conceptual framing - we ACTUALLY use target languages
to shift cognitive processing patterns.

---

## Goal-Based Frame Selection Checklist

### Step 1: Analyze Goals

Complete this for every non-trivial task:

```
1st Order Goal (Immediate): ________________
2nd Order Goal (Why): ________________
3rd Order Goal (Ultimate): ________________
```

### Step 2: Identify Dominant Thought Process

| Question | If YES, use Frame |
|----------|-------------------|
| Is tracking "done vs not done" critical? | Aspectual (Russian) |
| Is source reliability critical? | Evidential (Turkish) |
| Is audience/formality critical? | Hierarchical (Japanese) |
| Is semantic decomposition needed? | Morphological (Arabic) |
| Is physical/visual comparison needed? | Classifier (Mandarin) |
| Is spatial navigation needed? | Spatial (Guugu Yimithirr) |
| Is mathematical precision needed? | Numerical (Chinese) |

### Step 3: Select Primary Frame

Based on analysis, select:
- Primary Frame: ________________
- Secondary Frame (optional): ________________

---

## Frame Activation Protocols

### Evidential Frame (Turkish)

**When to Use**:
- Research tasks
- Fact-checking
- Audit and compliance
- Source verification

**Activation**:
```
## Kanitsal Cerceve Aktivasyonu

Bu gorev icin her iddia kaynaklandirilmalidir:

Kaynak Turleri:
- DOGRUDAN (-DI): Ben bizzat gordum/test ettim
- CIKARIM (-mIs): Kanitlardan cikarim yaptim
- BILDIRILEN (-mIs): Dokumantasyon/baskasi soyledi

English Markers:
- [DIRECT]: "I tested this myself"
- [INFERRED]: "Evidence suggests..."
- [REPORTED]: "Documentation states..."
```

### Aspectual Frame (Russian)

**When to Use**:
- Build/deploy pipelines
- Task tracking
- Progress reporting
- Completion verification

**Activation**:
```
## Aspektual'naya Ramka Aktivatsiya

Etot zadacha trebuyet otslezhivaniya zaversheniya:

Tipy Aspekta:
- SV (Sovershennyy Vid): Polnost'yu zaversheno, mozhno prodolzhat'
- NSV (Nesovershennyy Vid): V protsesse, ne zaversheno
- BLOCKED: Ozhidaet zavisimosti

English Markers:
- [SV:COMPLETED]: Task fully done, move on
- [NSV:IN_PROGRESS]: Task ongoing, not finished
- [BLOCKED]: Waiting on dependencies
```

### Hierarchical Frame (Japanese)

**When to Use**:
- Stakeholder communication
- Formal documentation
- Audience-calibrated output
- Executive summaries

**Activation**:
```
## Keigo Wakugumi Aktiveshon

Kono tasuku wa taishouzentai ni awaseta rejisutaa wo hitsuyou to shimasu:

Rejisutaa Shurui:
- Sonkeigo: Keiei-sha, suteekuhorudaa, gaibu patonaazu
- Kenjougo: Jibun no koudou wo hikuku hyougen
- Teineigo: Hyoujun-teki na bijinesu komyunikeeshon

English Markers:
- [SONKEIGO]: Formal, respectful (executives)
- [TEINEIGO]: Professional, polite (colleagues)
- [CASUAL]: Informal (personal notes)
```

### Morphological Frame (Arabic)

**When to Use**:
- Concept mapping
- Taxonomy development
- Semantic analysis
- Etymology tracing

**Activation**:
```
## Al-Itar al-Sarfi al-Tanshit

Hadhihi al-mahimma tatatallab tahlil al-judur:

Anmat al-Judur:
- Kull kalima min jadhr thalathi
- Al-jadhr yarbut al-ma'ani al-murtabita
- Tahlil al-namt yakshif al-'alaqat

Mithal:
- K-T-B: kitab, katib, maktub, maktaba
- '-L-M: 'ilm, 'alim, mu'allim, ta'lim

English Application:
- Identify root pattern in concept
- Map related terms from same root
- Reveal hidden semantic connections
```

### Classifier Frame (Mandarin)

**When to Use**:
- System design
- Object comparison
- Visual reasoning
- Categorization tasks

**Activation**:
```
## Liangci Kuangjia Jihuo

Zhe ge renwu xuyao anzhao xingzhuang fenlei:

Liangci Leixing:
- Zhang: Pingmian de (wenzhang, biaoge, tupian)
- Ben: Shuben leixing (shu, zazhi, baogao)
- Tiao: Changxing de (luxian, liucheng, guandao)
- Ge: Tongxing de (gainian, xiangmu, shiti)

English Application:
- Classify objects by their "shape" characteristics
- APIs are TIAO (path-like)
- Documents are ZHANG (flat)
- Databases are GE (abstract entities)
```

---

## Integration with Other Skills

### With intent-analyzer

After intent analysis, run cognitive lensing to select optimal frame:

```
1. intent-analyzer produces understood_intent
2. cognitive-lensing produces frame_selection
3. prompt-architect applies frame to optimize request
4. planner incorporates frame into execution plan
```

### With agent-creator

When creating agents, use cognitive lensing to:
- Determine optimal frame for agent's domain
- Embed frame activation in system prompt
- Include multi-lingual sections for frame-specific patterns

### With skill-forge

When creating skills, use cognitive lensing to:
- Add Phase 0.5 frame selection
- Embed frame activation in skill content
- Include goal-based checklist in skill documentation

---

## Memory Namespace

```yaml
namespaces:
  cognitive-lensing/selections/{task_id}:
    frame: evidential
    goals:
      first_order: "..."
      second_order: "..."
      third_order: "..."
    confidence: 0.85
    outcome: success|failure

  cognitive-lensing/effectiveness:
    frame_success_rates:
      evidential: 0.89
      aspectual: 0.92
      hierarchical: 0.85
    by_task_type: {...}
```

---

## Recursive Improvement Integration

This skill feeds into the meta-loop:

1. **Track frame selections** in memory-mcp
2. **Track outcomes** (did frame help?)
3. **Analyze effectiveness** by frame type and task type
4. **Propose improvements** to frame selection heuristics
5. **Gate changes** through frozen eval harness

---

**Status**: Production-Ready
**Version**: 1.0.0
**Key Innovation**: Actual multi-lingual activation, not just conceptual framing
```

---

## STEP 7: EVAL HARNESS UPDATES

### New Benchmark Suites

#### Suite 4: Cognitive Frame Quality

```yaml
benchmark:
  id: cognitive-frame-benchmark-v1
  version: 1.0.0
  frozen: true

  tasks:
    - id: "cf-001"
      name: "Evidential Frame Application"
      input: "Apply evidential frame to code review task"
      expected_qualities:
        - has_source_markers
        - has_confidence_levels
        - has_multi_lingual_activation
        - markers_consistently_applied
      scoring:
        marker_coverage: 0.0-1.0
        activation_quality: 0.0-1.0
        output_improvement: 0.0-1.0

    - id: "cf-002"
      name: "Aspectual Frame Application"
      input: "Apply aspectual frame to deployment tracking"
      expected_qualities:
        - has_completion_markers
        - has_progress_states
        - has_multi_lingual_activation
        - states_accurately_tracked
      scoring:
        marker_coverage: 0.0-1.0
        activation_quality: 0.0-1.0
        tracking_accuracy: 0.0-1.0

    - id: "cf-003"
      name: "Frame Selection Accuracy"
      input: "Given task, select appropriate frame"
      expected_qualities:
        - goal_analysis_complete
        - checklist_followed
        - frame_matches_task_type
        - rationale_documented
      scoring:
        selection_accuracy: 0.0-1.0
        rationale_quality: 0.0-1.0

  minimum_passing:
    average_marker_coverage: 0.75
    average_activation_quality: 0.7
    selection_accuracy: 0.8
```

#### Suite 5: Cross-Lingual Integration Quality

```yaml
benchmark:
  id: cross-lingual-benchmark-v1
  version: 1.0.0
  frozen: true

  tasks:
    - id: "cl-001"
      name: "Turkish Evidential Integration"
      input: "Generate evidential markers with Turkish activation"
      expected_qualities:
        - turkish_text_grammatically_correct
        - markers_map_to_turkish_concepts
        - english_output_incorporates_markers
      scoring:
        linguistic_quality: 0.0-1.0
        integration_quality: 0.0-1.0

    - id: "cl-002"
      name: "Russian Aspectual Integration"
      input: "Generate aspectual markers with Russian activation"
      expected_qualities:
        - russian_text_grammatically_correct
        - sv_nsv_distinction_applied
        - english_output_tracks_completion
      scoring:
        linguistic_quality: 0.0-1.0
        integration_quality: 0.0-1.0

    - id: "cl-003"
      name: "Multi-Frame Composition"
      input: "Compose two frames for complex task"
      expected_qualities:
        - both_frames_activated
        - no_marker_conflicts
        - output_benefits_from_both
      scoring:
        composition_quality: 0.0-1.0
        coherence: 0.0-1.0

  minimum_passing:
    average_linguistic_quality: 0.7
    average_integration_quality: 0.75
    composition_quality: 0.7
```

#### New Regression Suite: Cognitive Lensing

```yaml
regression_suite:
  id: cognitive-lensing-regression-v1
  version: 1.0.0
  frozen: true

  tests:
    - id: "clr-001"
      name: "Goal analysis preserved"
      action: "Run frame selection on task"
      expected: "All three goal orders analyzed"
      must_pass: true

    - id: "clr-002"
      name: "Checklist followed"
      action: "Select frame for ambiguous task"
      expected: "Checklist completed before selection"
      must_pass: true

    - id: "clr-003"
      name: "Multi-lingual activation included"
      action: "Apply frame to prompt"
      expected: "Native language activation section present"
      must_pass: true

    - id: "clr-004"
      name: "English output maintained"
      action: "Generate frame-enhanced output"
      expected: "Final output is in English with markers"
      must_pass: true

    - id: "clr-005"
      name: "Frame selection logged"
      action: "Complete frame selection"
      expected: "Selection stored in memory-mcp"
      must_pass: true

  failure_threshold: 0
```

---

## STEP 8: FULL META-LOOP IMPROVEMENT CYCLE

### Phase 1: Update Foundry Skills (Hours 1-4)

```
1. Update agent-creator v2.2.0 -> v3.0.0
   - Add Phase 0.5: Cognitive Frame Selection
   - Add goal-based checklist
   - Add multi-lingual embedding patterns

2. Update skill-forge v2.3.0 -> v3.0.0
   - Add Phase 0.5: Cognitive Frame Design
   - Add frame activation templates
   - Add cross-lingual section support

3. Update prompt-forge v1.0.0 -> v2.0.0
   - Add Operation 6: Cognitive Frame Enhancement
   - Add frame transformation patterns
   - Add multi-lingual enhancement protocols
```

### Phase 2: Create Cognitive Lensing Skill (Hours 5-6)

```
1. Create skills/foundry/cognitive-lensing/SKILL.md
2. Create frame activation templates
3. Create goal-based checklist
4. Create memory namespace structure
5. Run through skill-forge Phase 7a (adversarial testing)
```

### Phase 3: Update Eval Harness (Hours 7-8)

```
1. Add cognitive-frame-benchmark-v1
2. Add cross-lingual-benchmark-v1
3. Add cognitive-lensing-regression-v1
4. Get human approval for harness expansion
5. Increment harness version to v1.1.0
```

### Phase 4: Run Dogfooding Quality Detection (Hours 9-10)

```
1. Run Connascence analysis on ALL foundry skills
2. Store violations in memory-mcp
3. Query for similar past fixes
4. Generate improvement proposals
```

### Phase 5: Apply Recursive Improvement (Hours 11-14)

```
For each skill in foundry category:
  1. Audit with skill-auditor
  2. Generate improvement proposals
  3. Apply via skill-forge
  4. Test against NEW eval harness (v1.1.0)
  5. Commit if improved, rollback if regressed
```

### Phase 6: Cascade to All Components (Hours 15-24)

```
1. Process 196 skills through improvement loop
   - Apply cognitive lensing where beneficial
   - Update with goal-based checklists
   - Add frame activation where appropriate

2. Process 211 agents through improvement loop
   - Add cognitive frames to system prompts
   - Update with multi-lingual sections
   - Validate against agent benchmarks

3. Process 223 commands through improvement loop
   - Ensure frame-awareness in routing
   - Update command descriptions

4. Process 30 playbooks through improvement loop
   - Add frame selection to playbook workflows
   - Update playbook documentation
```

### Phase 7: Validation and Metrics (Hours 25-28)

```
1. Run full eval harness on ALL components
2. Compare before/after metrics
3. Document improvements achieved
4. Archive old versions
5. Update component counts
```

---

## STEP 9: EXPECTED OUTCOMES

### Quantitative Targets

| Metric | Baseline | Target | Method |
|--------|----------|--------|--------|
| Skill documentation completeness | 82% | 95% | Tier 1+2 at 100% |
| Agent system prompt quality | 78% | 90% | Benchmark scores |
| Frame selection accuracy | N/A | 80%+ | New benchmark |
| Cross-lingual integration quality | N/A | 75%+ | New benchmark |
| Improvement proposals accepted | 65% | 80% | Eval harness pass rate |

### Qualitative Outcomes

1. **Foundry skills enhanced** with cognitive framing capability
2. **Eval harness expanded** with frame-specific benchmarks
3. **Goal-based checklist** integrated into all foundry workflows
4. **Multi-lingual activation** available for 7 cognitive frames
5. **Self-improvement loop** now includes cognitive dimension
6. **660 components** systematically improved through meta-loop

---

## STEP 10: TIMELINE

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1: Foundry Updates | 4 hours | agent-creator v3.0, skill-forge v3.0, prompt-forge v2.0 |
| Phase 2: Cognitive Lensing | 2 hours | cognitive-lensing skill v1.0 |
| Phase 3: Eval Harness | 2 hours | eval-harness v1.1.0 with new benchmarks |
| Phase 4: Dogfooding | 2 hours | Quality detection on all foundry skills |
| Phase 5: Recursive Improvement | 4 hours | Foundry skills improved through loop |
| Phase 6: Cascade | 10 hours | All 660 components processed |
| Phase 7: Validation | 4 hours | Full eval + metrics + documentation |
| **Total** | **28 hours** | Complete cognitive lensing integration |

---

## CONCLUSION

This enhanced plan integrates cognitive lensing across the entire meta-loop:

1. **Agent-creator** gains cognitive frame selection
2. **Skill-forge** gains frame design phase
3. **Prompt-forge** gains frame enhancement operation
4. **Cognitive-lensing** skill created as new foundry component
5. **Eval harness** expanded with frame-specific benchmarks
6. **Full meta-loop** runs to improve ALL 660 components

The key innovation is **actual multi-lingual activation** - not just describing cognitive frames conceptually, but embedding native language sections that elicit different parts of the AI's latent space.

The goal-based checklist (1st, 2nd, 3rd order goals) ensures frame selection is grounded in PURPOSE, not just pattern matching.

**Ready to execute on your approval.**
