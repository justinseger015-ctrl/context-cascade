# VERILINGUA: A Guide Written in VERILINGUA

[audience:developers_and_ai_researchers] [formality:medium] [register:technical]

---

## What is VERILINGUA?

[witnessed] VERILINGUA is a cognitive frame system that forces explicit cognitive distinctions in AI responses.

[reported:linguistic_research] The system draws from 7 natural languages that grammatically require speakers to make distinctions that English leaves optional.

[inferred] By activating these frames, we can improve the precision, reliability, and self-awareness of AI-generated content.

---

## The 7 Cognitive Frames

### 1. EVIDENTIAL FRAME (Turkish -mis/-di)

[root:evidence] The evidential frame forces distinction between sources of knowledge.

[witnessed] Turkish grammar requires marking whether a speaker personally witnessed something (-di) or learned it secondhand (-mis).

[derived:evidence->evidential_marker] This distinction becomes mandatory in AI responses:

| Marker | Meaning | Example |
|--------|---------|---------|
| [witnessed] | Directly observed/verified | [witnessed] The function returns null - I traced the code |
| [reported] | Learned from a source | [reported:docs] The API rate limit is 100/min |
| [inferred] | Deduced logically | [inferred] The cache is stale because TTL expired |
| [assumed] | Explicit assumption | [assumed:0.7] The server uses REST conventions |

[complete] The evidential frame is fully implemented in `core/verilingua.py`.

---

### 2. ASPECTUAL FRAME (Russian Perfective/Imperfective)

[root:completion] The aspectual frame forces distinction between complete and ongoing actions.

[witnessed] Russian verbs require speakers to indicate whether an action is complete (perfective) or ongoing (imperfective).

[derived:completion->aspect_marker] This maps to AI responses as:

| Marker | Meaning | Example |
|--------|---------|---------|
| [complete] | Action finished | [complete] Migration executed successfully |
| [ongoing] | Action in progress | [ongoing] Test suite running - 45/100 done |
| [habitual] | Repeating action | [habitual] Cron job runs every hour |
| [attempted] | Tried, outcome pending | [attempted] Connection initiated, awaiting response |

[complete] The aspectual frame prevents ambiguity about task status.

---

### 3. MORPHOLOGICAL FRAME (Arabic Trilateral Roots)

[root:decompose] The morphological frame forces semantic decomposition.

[reported:arabic_linguistics] Arabic derives words from 3-consonant roots (k-t-b = write/book/author), revealing semantic relationships.

[primitive:concept] A concept is a basic unit of meaning.
[primitive:root] A root is the semantic kernel from which concepts derive.
[compound:root+context] Combining root with context produces specific meanings.

[composed:authenticate+authorize=access_control] Authentication verifies identity; authorization grants permissions; together they control access.

[complete] Use morphological decomposition when explaining technical terms.

---

### 4. COMPOSITIONAL FRAME (German Compounding)

[root:composition] The compositional frame forces building from primitives.

[reported:german_linguistics] German creates compound words (Schadenfreude = Schaden + Freude = harm + joy).

[builds:primitive->compound->complex]

[primitive:request] A request is a message asking for something.
[primitive:handler] A handler is code that processes input.
[compound:request+handler] A request handler processes incoming requests.
[builds:request_handler->middleware->application] Middleware chains handlers into an application.

[complete] Always define primitives before composing complex concepts.

---

### 5. HONORIFIC FRAME (Japanese Keigo)

[audience:mixed_technical_levels] [formality:high] [register:accessible]

[root:audience] The honorific frame forces audience calibration.

[reported:japanese_linguistics] Japanese has elaborate honorific systems (sonkeigo, kenjougo, teineigo) that change language based on social relationships.

[complete] This guide uses:
- [audience:developers_and_ai_researchers] - Primary audience
- [formality:medium] - Technical but approachable
- [register:technical] - Uses domain terminology

[direction:downstream] When content flows to end users, shift to [formality:high] [register:casual].

---

### 6. CLASSIFIER FRAME (Chinese Measure Words)

[root:classification] The classifier frame forces explicit typing and counting.

[reported:chinese_linguistics] Chinese requires measure words between numbers and nouns, forcing categorization.

[type:frame] This system has 7 frames.
[type:marker] Each frame has multiple markers.
[category:cognitive_forcing] All frames share the goal of forcing explicit distinctions.

[measure:files] The implementation spans 5 Python files.
[measure:lines] Core modules total approximately 2000 lines.
[measure:dimensions] Config vectors have 14 dimensions.

[complete] Never use vague quantities - always classify and count.

---

### 7. SPATIAL FRAME (Guugu Yimithirr Absolute Positioning)

[root:position] The spatial frame forces absolute reference.

[reported:guugu_linguistics] Guugu Yimithirr uses absolute directions (north/south) instead of relative (left/right).

[path:/cognitive-architecture/core/verilingua.py] The VERILINGUA implementation lives here.
[location:verilingua.py:85] The EvidentialFrame class starts at line 85.
[direction:upstream] Config flows from PromptBuilder upstream.
[direction:downstream] Responses flow downstream to validation.

[complete] Always provide absolute paths, line numbers, and directional flow.

---

## Activation Instructions

[ongoing] When VERILINGUA frames are active, you MUST follow their requirements.

[path:/cognitive-architecture/core/prompt_builder.py] The PromptBuilder injects frame activations into system prompts.

[witnessed] Each frame provides an `activation_instruction()` method that returns the prompt text.

[complete] Frame activation is automatic based on FrameworkConfig settings.

---

## Scoring and Compliance

[type:score] Each frame calculates a compliance score (0.0 - 1.0).

[inferred] Higher scores indicate better adherence to frame requirements.

[path:/cognitive-architecture/core/verilingua.py:score_all_frames] The scoring function evaluates all active frames.

[complete] Aggregate scores are used for optimization feedback.

---

## Integration with GlobalMOO

[direction:upstream] GlobalMOO suggests config vectors.
[direction:downstream] VectorCodec decodes to FrameworkConfig.
[direction:downstream] PromptBuilder activates selected frames.
[direction:downstream] Responses are scored against frames.
[direction:upstream] Scores feed back to GlobalMOO.

[type:optimization_loop] This creates a closed optimization loop.
[measure:iterations] Typical optimization runs 100-500 iterations per phase.

[complete] The Three-MOO Cascade optimizes frame selection over three phases.

---

## Self-Improvement Application

[audience:meta_level] [formality:high] [register:philosophical]

[inferred] This guide itself demonstrates the power of VERILINGUA.

[witnessed] Every statement in this document uses at least one cognitive frame marker.

[root:recursion] The system can improve itself by:
1. [primitive:analyze] Analyzing its own outputs
2. [derived:analyze->score] Scoring against frame compliance
3. [derived:score->optimize] Optimizing configurations
4. [derived:optimize->generate] Generating improved prompts
5. [builds:generate->validate->deploy] Validating and deploying improvements

[complete] This recursive improvement capability is the core value proposition.

[commit|neutral] VERILINGUA will continue to evolve through self-application [conf:0.95] [state:confirmed]

---

## Quick Reference

| Frame | Source | Force | Primary Marker |
|-------|--------|-------|----------------|
| Evidential | Turkish | How do you know? | [witnessed], [reported], [inferred] |
| Aspectual | Russian | Complete or ongoing? | [complete], [ongoing] |
| Morphological | Arabic | What are the roots? | [root:], [derived:] |
| Compositional | German | How does it compose? | [primitive:], [builds:] |
| Honorific | Japanese | Who is the audience? | [audience:], [formality:] |
| Classifier | Chinese | What type/count? | [type:], [measure:] |
| Spatial | Guugu Yimithirr | What is the path? | [path:], [location:], [direction:] |

---

[commit|positive] This guide serves as both documentation and demonstration of VERILINGUA [conf:1.0] [state:confirmed]
