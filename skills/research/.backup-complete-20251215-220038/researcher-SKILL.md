---

## RESEARCH ANALYSIS GUARDRAILS

**Source Verification Required**:
- NEVER cite sources without verification
- ALWAYS check publication date and relevance
- Verify author credentials and expertise
- Cross-reference claims with multiple sources

**Credibility Scoring**:
- Tier 1 (90-100%): Peer-reviewed, official docs
- Tier 2 (75-89%): Industry reports, credible news
- Tier 3 (60-74%): Expert blogs, technical forums
- Tier 4 (<60%): Unverified, opinion pieces
- REJECT sources below threshold

**Evidence-Based Reasoning**:
- Support claims with concrete evidence
- Distinguish facts from interpretations
- Identify and disclose biases
- Report contradictory evidence when found

**Documentation Standards**:
- Provide full citations (APA, IEEE, or ACM format)
- Include access dates for web sources
- Link to primary sources when available
- Archive sources for reproducibility
name: researcher
description: Multi-level research with Gemini Search integration supporting 3 research
  depths. Use when gathering information, conducting systematic analysis, or synthesizing
  knowledge from multiple sources. Applies 90%+ credibility scoring and comprehensive
  source evaluation.
version: 1.0.0
category: research
tags:
- research
- analysis
- planning
author: ruv

## SKILL-SPECIFIC GUIDANCE

### When to Use This Skill
- Multi-source investigation requiring 3-5+ credible sources (Level 2-3 research)
- Technical documentation analysis with credibility scoring (>85%)
- Cross-referencing claims across industry reports, academic papers, official docs
- Building knowledge bases for unfamiliar technologies or domains
- Systematic information gathering with comprehensive source evaluation

### When NOT to Use This Skill
- Single-source quick lookups (use web search directly)
- Non-technical questions not requiring credibility analysis
- When speed is prioritized over source verification (<5 min deadline)
- Opinion-based topics without objective truth (use judgment, not research)

### Success Criteria
- [assert|neutral] 90%+ average credibility score across all cited sources [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] 3+ independent sources corroborate key claims [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] All sources annotated with credibility breakdown (Authority, Accuracy, Objectivity, Currency, Coverage) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Contradictory evidence reported and analyzed [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Full citations provided (APA/IEEE/ACM format with access dates) [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases & Limitations
- Paywalled sources: Use institutional access, preprints, contact authors
- Conflicting expert opinions: Present both sides, analyze methodology/bias
- Rapidly changing topics (AI, crypto): Prioritize Currency (15%), accept lower coverage
- Niche topics with limited sources: Expand to Tier 3 (expert blogs), disclose limitations
- Biased sources: Flag bias score, require 3+ independent corroborations

### Critical Guardrails
- NEVER cite without credibility scoring (use 0-100% rubric)
- ALWAYS cross-reference claims with 2+ independent Tier 1/2 sources
- NEVER accept <70% credibility sources without explicit disclosure
- ALWAYS distinguish facts (verifiable) from interpretations (opinion)
- NEVER skip source publication date verification (check Currency dimension)

### Evidence-Based Validation
- Validate source authority: Check author credentials (H-index, institutional affiliation)
- Cross-validate factual claims: Search for contradictory evidence actively
- Verify objectivity: Check funding sources, conflicts of interest
- Test currency: Compare publication date to topic evolution, flag outdated info
- Confirm coverage: Verify comprehensive treatment vs. surface-level overview

---
---

# Researcher - Systematic Information Gathering

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Systematic multi-level research with integrated Gemini Search for comprehensive knowledge synthesis.

## When to Use This Skill

Use when conducting technical research, gathering information on unfamiliar topics, comparing technologies or approaches, validating claims with credible sources, or building comprehensive knowledge bases.

## 3-Level Research Methodology

### Level 1: Basic Research (< 5 minutes)
- Quick factual queries
- Single-source validation
- Surface-level understanding
- Immediate answers needed

**Process**:
1. Query Gemini Search for primary information
2. Validate source credibility (>70%)
3. Extract key facts
4. Provide concise summary

### Level 2: Multi-Source Research (15-30 minutes)
- Cross-reference multiple sources
- Deeper analysis required
- Technical understanding needed
- Comprehensive overview desired

**Process**:
1. Query 3-5 authoritative sources
2. Compare and contrast findings
3. Identify consensus and disagreements
4. Synthesize into coherent analysis
5. Score sources for credibility (>85%)

### Level 3: Deep Dive Research (1+ hours)
- Extensive investigation
- Academic rigor required
- Complex topic with nuances
- Publication-ready research

**Process**:
1. Systematic literature review
2. Query 10+ diverse sources
3. Analyze methodology and evidence
4. Identify research gaps
5. Synthesize comprehensive report
6. Ensure 90%+ source credibility

## Source Evaluation Criteria

### Credibility Scoring (0-100%)
- **Authority** (30%): Expert author, institutional backing
- **Accuracy** (25%): Fact-checked, peer-reviewed, verifiable
- **Objectivity** (20%): Minimal bias, balanced perspective
- **Currency** (15%): Recent publication, up-to-date information
- **Coverage** (10%): Comprehensive treatment of topic

### Source Types by Reliability
1. **Tier 1 (90-100%)**: Peer-reviewed journals, official documentation
2. **Tier 2 (75-89%)**: Industry reports, credible news outlets
3. **Tier 3 (60-74%)**: Blog posts from experts, technical forums
4. **Tier 4 (<60%)**: Unverified sources, opinion pieces

## Gemini Search Integration

- Use `gemini-search` skill for web queries
- Enable grounded search for factual accuracy
- Leverage Google Search API for broad coverage
- Apply source verification automatically

## Output Formats

- **Summary**: Key findings in bullet points
- **Synthesis**: Coherent narrative combining sources
- **Bibliography**: Annotated source list with credibility scores
- **Analysis**: Detailed evaluation with evidence

---
*Promise: `<promise>RESEARCHER_SKILL_VERIX_COMPLIANT</promise>`*
