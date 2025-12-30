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

## SKILL-SPECIFIC GUIDANCE

### When to Use This Skill
- Triggering interactive-planner skill when gathering requirements detected
- Auto-invoking structured multi-select questions for architecture decisions
- Ensuring comprehensive requirements collection before planning
- Reducing assumption-based design by collecting explicit user choices
- Specialized tool wrapper for requirements gathering scenarios

### When NOT to Use This Skill
- Requirements already defined (skip to planner)
- Single-choice decisions (not multi-select)
- When interactive-planner already invoked directly
- Follow-up scenarios where context exists

### Success Criteria
- [assert|neutral] Interactive-planner skill successfully invoked [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] User presented with 5-10 multi-select questions [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] All critical choices captured before planning proceeds [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Requirements document exported [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Plan reflects user selections accurately [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases & Limitations
- User bypasses questions: respect preference, document assumptions made
- Skill invocation fails: fallback to manual requirements gathering
- Too many nested tool calls: simplify to direct interactive-planner invocation
- Contradictory selections: flag for resolution before proceeding
- Missing context: gather minimal required info before invoking

### Critical Guardrails
- NEVER invoke if interactive-planner already active (avoid recursion)
- ALWAYS verify requirements gathering truly needed
- NEVER force questions if user has clear requirements
- ALWAYS respect user preference to skip
- NEVER proceed to planning without confirmation

### Evidence-Based Validation
- Validate invocation appropriateness: is requirements gathering truly needed?
- Cross-check skill availability: is interactive-planner accessible?
- Test user intent: does user want structured questions or prefer freeform?
- Verify context: is this right moment to invoke (not mid-execution)?
- Confirm fallback: if invocation fails, can manual gathering proceed?

---
name: when-gathering-requirements-use-interactive-planner
description: '```yaml'
version: 1.0.0
category: research
tags:
- research
- analysis
- planning
author: ruv
---

# Interactive Requirements Planning SOP

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



```yaml
metadata:
  skill_name: when-gathering-requirements-use-interactive-planner
  version: 1.0.0
  category: specialized-tools
  difficulty: beginner
  estimated_duration: 15-30 minutes
  trigger_patterns:
    - "gather requirements"
    - "interactive questions"
    - "requirements gathering"
    - "clarify requirements"
  agents:
    - planner
    - researcher
    - system-architect
  success_criteria:
    - Requirements gathered
    - Specifications documented
    - Stakeholder approval
    - Action plan created
```

## Overview

Use Claude Code's AskUserQuestion tool to gather comprehensive requirements through structured multi-select questions.

## Phases

### Phase 1: Discover Needs (3-5 min)
Ask initial questions about project goals and scope using AskUserQuestion tool.

### Phase 2: Clarify Details (5-10 min)
Follow up with detailed technical and timeline questions.

### Phase 3: Structure Requirements (3-5 min)
Organize responses into formal specifications document.

### Phase 4: Validate Completeness (2-5 min)
Review with stakeholders and get approval.

### Phase 5: Document Specifications (2-5 min)
Create final documentation and action plan.

## Best Practices

1. Ask open, clear questions
2. Provide descriptive options
3. Use multi-select for priorities
4. Document all responses
5. Validate with stakeholders
6. Create actionable plans

## Workflow Summary

**Duration:** 15-30 minutes

**Deliverables:**
- Requirements specification
- Technical architecture
- Action plan
- Validation report


---
*Promise: `<promise>WHEN_GATHERING_REQUIREMENTS_USE_INTERACTIVE_PLANNER_SKILL_VERIX_COMPLIANT</promise>`*
