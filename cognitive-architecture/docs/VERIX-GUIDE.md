# VERIX: A Guide Written in VERIX

[assert|neutral] This document describes the VERIX epistemic notation system using VERIX notation itself [ground:self-reference] [conf:1.0] [state:confirmed]

---

## What is VERIX?

[assert|neutral] VERIX is an epistemic notation system for structured claims [ground:design_document] [conf:0.95] [state:confirmed]

[assert|neutral] The name derives from "VERIfied eXpression" - a format that makes claim properties explicit [ground:naming_convention] [conf:0.90] [state:confirmed]

[query|uncertain] Why do AI systems need epistemic notation? [conf:0.85]

[assert|positive] Because unstructured natural language hides confidence levels, evidence sources, and claim status [ground:problem_analysis] [conf:0.92] [state:confirmed]

---

## The VERIX Grammar

[assert|neutral] Every VERIX statement follows this grammar [ground:specification] [conf:1.0] [state:confirmed]:

```
STATEMENT := ILLOCUTION + AFFECT + CONTENT + GROUND + CONFIDENCE + STATE
```

[assert|neutral] Each component serves a specific purpose [ground:component_analysis] [conf:0.95] [state:confirmed]

---

### ILLOCUTION (Speech Act Type)

[assert|neutral] Illocution identifies WHAT the speaker is trying to DO with the utterance [ground:speech_act_theory] [conf:0.95] [state:confirmed]

| Illocution | Purpose | Example |
|------------|---------|---------|
| [assert\|...] | Making a factual claim | [assert\|neutral] The function returns null |
| [query\|...] | Asking a question | [query\|uncertain] Is this thread-safe? |
| [direct\|...] | Giving an instruction | [direct\|positive] Use async/await here |
| [commit\|...] | Making a promise | [commit\|neutral] I will fix this bug |
| [express\|...] | Expressing attitude | [express\|positive] This is elegant code |

[assert|neutral] Illocution is ALWAYS required - it's the minimal VERIX marker [ground:grammar_rules] [conf:1.0] [state:confirmed]

---

### AFFECT (Emotional Valence)

[assert|neutral] Affect indicates the speaker's emotional stance toward the content [ground:sentiment_analysis] [conf:0.90] [state:confirmed]

| Affect | Meaning | When to Use |
|--------|---------|-------------|
| neutral | No emotional loading | Most factual claims |
| positive | Favorable stance | Recommendations, successes |
| negative | Unfavorable stance | Warnings, problems |
| uncertain | Epistemic uncertainty | Hypotheses, unknowns |

[assert|neutral] Affect separates cognitive evaluation from emotional reaction [ground:design_principle] [conf:0.88] [state:confirmed]

---

### CONTENT (The Claim)

[assert|neutral] Content is the actual claim being made [ground:obvious] [conf:1.0] [state:confirmed]

[assert|neutral] Content can be any natural language statement [ground:flexibility_requirement] [conf:0.95] [state:confirmed]

[assert|negative] Content should NOT include embedded confidence or evidence markers [ground:separation_of_concerns] [conf:0.85] [state:confirmed]

---

### GROUND (Evidence/Source)

[assert|neutral] Ground identifies WHERE the claim comes from [ground:epistemology] [conf:0.93] [state:confirmed]

| Ground Type | Meaning | Example |
|-------------|---------|---------|
| [ground:witnessed] | Personal observation | Traced the code |
| [ground:documentation] | Official docs | Read the API spec |
| [ground:user_input] | User's message | From the bug report |
| [ground:inference] | Logical deduction | From premises A and B |
| [ground:assumption] | Explicit assumption | Industry convention |

[assert|neutral] Ground creates accountability for claims [ground:trust_building] [conf:0.90] [state:confirmed]

[assert|positive] Well-grounded claims are more trustworthy [ground:common_sense] [conf:0.95] [state:confirmed]

---

### CONFIDENCE (Numeric Level)

[assert|neutral] Confidence is a numeric value from 0.0 to 1.0 [ground:specification] [conf:1.0] [state:confirmed]

| Range | Meaning | Example Usage |
|-------|---------|---------------|
| 0.0-0.3 | Very uncertain | Wild speculation |
| 0.3-0.5 | Uncertain | Educated guess |
| 0.5-0.7 | Moderate | Reasonable belief |
| 0.7-0.9 | Confident | Well-supported |
| 0.9-1.0 | Highly confident | Verified fact |

[assert|negative] Confidence inflation is a common failure mode [ground:observed_patterns] [conf:0.80] [state:provisional]

[direct|neutral] Calibrate confidence carefully - when uncertain, say so [ground:best_practice] [conf:0.90] [state:confirmed]

---

### STATE (Claim Lifecycle)

[assert|neutral] State tracks where a claim is in its lifecycle [ground:design_document] [conf:0.95] [state:confirmed]

| State | Meaning | Transitions From |
|-------|---------|------------------|
| provisional | Initial, may be revised | (start) |
| confirmed | Verified, high confidence | provisional |
| retracted | Withdrawn/invalidated | provisional, confirmed |

[assert|neutral] Claims can move from provisional to confirmed as evidence accumulates [ground:logical_progression] [conf:0.92] [state:confirmed]

[assert|negative] High confidence with provisional state is a warning sign [ground:validation_rules] [conf:0.88] [state:confirmed]

---

## Compression Levels

[assert|neutral] VERIX supports three compression levels for different audiences [ground:design_document] [conf:0.95] [state:confirmed]

### L0: AI-to-AI (Emoji Shorthand)

[assert|neutral] L0 is maximally compact for machine communication [ground:efficiency] [conf:0.90] [state:confirmed]

```
A.85:The function is pure
?.60:Is this thread-safe
!+95:Use immutable data
```

[assert|neutral] Format: {I}{A}{NN}:{content} where I=illocution, A=affect, NN=confidence% [ground:format_spec] [conf:1.0] [state:confirmed]

### L1: AI+Human Inspector (Annotated)

[assert|neutral] L1 is the default format for human-readable logs [ground:design_choice] [conf:0.90] [state:confirmed]

```
[assert|neutral] The function is pure [ground:code_analysis] [conf:0.85] [state:confirmed]
```

[assert|positive] L1 balances precision with readability [ground:usability_testing] [conf:0.85] [state:provisional]

### L2: Human Reader (Natural Language)

[assert|neutral] L2 converts to natural prose, losing some precision [ground:compression_tradeoff] [conf:0.88] [state:confirmed]

```
I'm fairly confident that the function is pure, based on my code analysis.
```

[assert|negative] L2 is lossy - not all VERIX information survives [ground:compression_limits] [conf:0.95] [state:confirmed]

---

## Validation Rules

[assert|neutral] VERIX validation enforces epistemic hygiene [ground:quality_assurance] [conf:0.90] [state:confirmed]

### STRICT Mode

[assert|neutral] In STRICT mode, all fields are required [ground:mode_specification] [conf:1.0] [state:confirmed]

[direct|neutral] Every claim MUST have: illocution, affect, content, ground, confidence, state [ground:strict_requirements] [conf:1.0] [state:confirmed]

### MODERATE Mode

[assert|neutral] In MODERATE mode, illocution, affect, and confidence are required [ground:mode_specification] [conf:1.0] [state:confirmed]

[assert|neutral] Ground and state are encouraged but optional [ground:mode_specification] [conf:0.95] [state:confirmed]

### RELAXED Mode

[assert|neutral] In RELAXED mode, only illocution and affect are required [ground:mode_specification] [conf:1.0] [state:confirmed]

[assert|positive] RELAXED mode allows gradual adoption [ground:adoption_strategy] [conf:0.85] [state:provisional]

---

## Consistency Rules

[assert|neutral] Claims must be internally consistent [ground:logic] [conf:0.95] [state:confirmed]

### Confidence Consistency

[assert|negative] The same content should not have contradicting confidence levels [ground:consistency_requirement] [conf:0.90] [state:confirmed]

[query|uncertain] If claim A says X with conf:0.9 and claim B says X with conf:0.3, which is correct? [conf:0.70]

[assert|neutral] This indicates an error requiring resolution [ground:validation_logic] [conf:0.92] [state:confirmed]

### Ground Chain Validity

[assert|neutral] Confirmed claims should not cite retracted sources [ground:logical_requirement] [conf:0.95] [state:confirmed]

[assert|negative] If evidence is retracted, claims depending on it become suspect [ground:epistemology] [conf:0.90] [state:confirmed]

---

## Compliance Scoring

[assert|neutral] VERIX compliance is scored from 0.0 to 1.0 [ground:implementation] [conf:0.95] [state:confirmed]

[assert|neutral] Scoring considers: ground presence, confidence validity, state progression, consistency [ground:scoring_algorithm] [conf:0.90] [state:confirmed]

[assert|positive] Higher scores indicate better epistemic hygiene [ground:design_intent] [conf:0.92] [state:confirmed]

---

## Integration with Optimization

[assert|neutral] VERIX compliance feeds into GlobalMOO optimization [ground:architecture] [conf:0.93] [state:confirmed]

[assert|neutral] The `epistemic_consistency` metric is derived from VERIX validation [ground:implementation] [conf:0.95] [state:confirmed]

[commit|neutral] Better VERIX compliance leads to more trustworthy AI outputs [ground:thesis] [conf:0.90] [state:provisional]

---

## Self-Reference

[assert|positive] This document demonstrates VERIX by using VERIX notation throughout [ground:meta_observation] [conf:1.0] [state:confirmed]

[assert|neutral] Every significant claim in this guide includes VERIX markers [ground:document_analysis] [conf:0.95] [state:confirmed]

[express|positive] Writing in VERIX forces clarity about what I know and how I know it [conf:0.88]

[commit|positive] The VERIX system will continue to evolve through self-application [ground:roadmap] [conf:0.90] [state:confirmed]

---

## Quick Reference

| Component | Required | Values | Format |
|-----------|----------|--------|--------|
| Illocution | Always | assert, query, direct, commit, express | [illocution\|affect] |
| Affect | Always | neutral, positive, negative, uncertain | [illocution\|affect] |
| Content | Always | Any text | After markers |
| Ground | STRICT/encouraged | Source description | [ground:source] |
| Confidence | STRICT/MODERATE | 0.0-1.0 | [conf:N.NN] |
| State | STRICT/encouraged | provisional, confirmed, retracted | [state:status] |

---

[commit|positive] This guide serves as both documentation and demonstration of VERIX notation [ground:self-reference] [conf:1.0] [state:confirmed]

[express|positive] May your claims be well-grounded and appropriately confident [conf:0.95]
