# Cognitive Lensing System: Integration Analysis

## Sequential Thinking Analysis

**Date**: 2025-12-18
**Analyst**: Claude Opus 4.5 via meta-loop analysis
**Target**: Cognitive Lensing System prompt vs existing Context Cascade infrastructure

---

## STEP 1: DECOMPOSE THE COGNITIVE LENSING SYSTEM

### What the Cognitive Lensing System Proposes

| Phase | Component | Purpose |
|-------|-----------|---------|
| Phase 0 | Research Protocol | Understand Claude Code architecture |
| Phase 1 | Cognitive Lens Taxonomy | 6-tier MECE framework for problem classification |
| Phase 2 | Problem Classifier | Skill that maps problems to dimensions |
| Phase 3 | Subagent Templates | Specialized agents (frame-analyst, adversarial-critic) |
| Phase 4 | Hooks Implementation | Quality gates at lifecycle events |
| Phase 5 | CLAUDE.md Integration | Protocol documentation |

### The 6 Tiers of Cognitive Lensing

1. **TIER 1: Cognitive Frames** - "Through what lens?"
   - Linguistic frames (Evidential, Aspectual, Social-Hierarchical, etc.)
   - Disciplinary frames (Physical, Biological, Economic, etc.)
   - Mathematical frames (Algebraic, Probabilistic, etc.)
   - Temporal perspectives (Historical, Prospective, Counterfactual)
   - Scale frames (Spatial, Temporal)
   - Abstraction levels (Concrete, Pattern, Principle, Meta)

2. **TIER 2: Cognitive Process** - "By what method?"
   - Inferential direction (Deductive/Inductive/Abductive)
   - Reasoning directive (Step-by-Step/CoT/ToT/Adversarial)
   - Attention allocation (Narrow-Deep/Wide-Survey)
   - Exploration mode (Exploit/Explore)

3. **TIER 3: Representation** - "In what form?"
   - Propositional, Schematic, Imagistic, Procedural, Network, etc.

4. **TIER 4: Context** - "With what knowledge?"
   - Domain knowledge, exemplars, constraints, goals, persona

5. **TIER 5: Output** - "For whom?"
   - Structure, length, formality, register

6. **TIER 6: Architecture** - "At what configuration?"
   - Model, temperature, topology, iteration pattern, tools

---

## STEP 2: MAP TO EXISTING INFRASTRUCTURE

### Direct Overlaps (Already Have)

| Cognitive Lensing Concept | Our Existing Component | Coverage |
|---------------------------|------------------------|----------|
| Phase 0: Research Protocol | Explore agent + Glob/Grep/Read | 100% |
| Intent Archaeology | intent-analyzer skill | 95% |
| Problem Classification | 5-phase workflow (Phase 3: planner) | 80% |
| Subagent Templates | Agent Registry (211 agents) | 100% |
| Hooks Implementation | `.claude/hooks/` enforcement system | 90% |
| CLAUDE.md Integration | CLAUDE.md v2.3 | 100% |
| Self-Consistency Prompting | prompt-forge (evidence-based techniques) | 100% |
| Plan-and-Solve | research-driven-planning skill | 95% |
| Quality Gates | recursive-improvement (frozen eval harness) | 100% |
| Multi-Agent Topology | swarm-orchestration, hive-mind-advanced | 100% |

### Partial Overlaps (Could Enhance)

| Cognitive Lensing Concept | Our Component | Gap |
|---------------------------|---------------|-----|
| Linguistic Frames (Evidential, Aspectual) | None | NEW - not addressed |
| Disciplinary Frame Selection | Implicit in skill routing | Could be explicit |
| MECE Dimensional Framework | Implicit in playbook selection | Could be formalized |
| Frame Selection Heuristics | Skill trigger keywords | Could be cognitive |
| Scale Awareness (Spatial/Temporal) | Not explicit | NEW |
| Abstraction Level Detection | Not explicit | NEW |

### Novel Concepts (Don't Have)

1. **Linguistic Cognitive Frames** - Applying language-specific cognitive patterns
   - Evidential frame (Turkish): Source marking on every claim
   - Aspectual frame (Russian): Completion status marking
   - Social-hierarchical frame (Japanese): Register calibration
   - Morphological frame (Arabic): Root-pattern semantic analysis

2. **Multi-Dimensional Problem Classification** - 116 dimensions across 6 tiers
   - Current system: Binary routing (keyword -> playbook)
   - Proposed: Rich dimensional analysis before routing

3. **Frame Activation Protocol** - Internally activate cognitive frame
   - Apply language-specific thinking patterns to problems

---

## STEP 3: ANALYZE WHAT TO EXECUTE VS LEVERAGE

### EXECUTE AS DESCRIBED (New Value)

These components should be built because they're genuinely novel:

#### 1. Linguistic Frame Taxonomy (Tier 1 Extension)

**Why New**: Our intent-analyzer focuses on understanding WHAT the user wants, not HOW to cognitively approach it. Linguistic frames add the "through what cognitive lens" dimension.

**Implementation**: Create `cognitive-frames.yaml` with frame definitions:
```yaml
frames:
  evidential:
    source_language: Turkish/Quechua
    obligatory_feature: Source marking on every claim
    activation_pattern: "For each assertion, mark: witnessed (-DI) / inferred (-mIs) / reported"
    when_to_use:
      - Source reliability questions
      - Fact-checking tasks
      - Epistemic vigilance needed

  aspectual:
    source_language: Russian/Slavic
    obligatory_feature: Completion status on every action
    activation_pattern: "For each action, classify: Perfective (done) / Imperfective (ongoing)"
    when_to_use:
      - "Is it done?" questions
      - Process vs. completion distinction
      - Tracking task status
```

**Integration Point**: After intent-analyzer (Phase 1), before prompt-architect (Phase 2)

#### 2. Multi-Dimensional Problem Classifier

**Why New**: Current routing is keyword-based (flat). A dimensional classifier would provide richer problem understanding.

**Implementation**: Extend `prompt-architect` with dimensional analysis:
```yaml
dimensional_analysis:
  tier1_frames:
    linguistic: evidential  # Source reliability matters
    disciplinary: engineering  # Technical system
    temporal: present_analytical  # Analyzing current state
    abstraction: pattern_level  # Looking for recurring issues

  tier2_process:
    inferential: abductive  # Best explanation from evidence
    reasoning: step_by_step  # Methodical analysis
    attention: narrow_deep  # Focus on specific issue

  tier3_representation:
    working: procedural  # Step-by-step process
    output: tabular  # Comparison/data format
```

**Integration Point**: Merge into prompt-architect as "dimensional pre-analysis"

#### 3. Frame Selection Heuristics

**Why New**: Converting problem patterns to optimal frames is novel.

**Implementation**: Create heuristic lookup table:
```yaml
heuristics:
  - pattern: "Is X done/complete/finished?"
    frame: aspectual
    reasoning: "Completion status is primary concern"

  - pattern: "How reliable is this source?"
    frame: evidential
    reasoning: "Source tracking needed"

  - pattern: "Navigate/directions/location"
    frame: spatial_absolute
    reasoning: "Orientation-independent memory"

  - pattern: "Formal communication/hierarchy"
    frame: social_hierarchical
    reasoning: "Register calibration needed"
```

**Integration Point**: Add to intent-analyzer as "frame detection" sub-phase

### LEVERAGE EXISTING (Already Have)

These should use our existing infrastructure, not rebuild:

#### 1. Research Protocol (Phase 0)

**Leverage**: Use Explore agent with Glob/Grep/Read
- Already have comprehensive codebase exploration
- No need for separate research phase

#### 2. Subagent Templates (Phase 3)

**Leverage**: Use Agent Registry (211 agents)
- Don't create new "frame-analyst" and "adversarial-critic" agents
- Instead, ADD to registry: `frame-analyst`, `adversarial-critic`
- These become part of the 211+ agent ecosystem

**DO NOT**: Create parallel agent system

#### 3. Hooks Implementation (Phase 4)

**Leverage**: Use existing `.claude/hooks/` system
- Already have UserPromptSubmit, PreToolUse, PostToolUse, PreCompact, Stop
- Add cognitive lensing to existing hooks

**Enhancement**: Add frame detection to `five-phase-enforcer.sh`:
```bash
# After intent analysis, detect optimal cognitive frame
if [ "$complexity" == "high" ]; then
  echo "[COGNITIVE LENSING] Activating dimensional analysis..."
fi
```

#### 4. CLAUDE.md Integration (Phase 5)

**Leverage**: Add to existing CLAUDE.md v2.3 Section 1
- Don't create separate protocol document
- Integrate into 5-phase workflow

#### 5. Self-Consistency, Plan-and-Solve (Evidence-Based Techniques)

**Leverage**: Already in prompt-forge skill
- Don't recreate evidence-based prompting
- Use existing implementation

#### 6. Quality Gates

**Leverage**: recursive-improvement with frozen eval harness
- Don't create new quality gate system
- Use existing propose-test-compare-commit pipeline

#### 7. Multi-Agent Topology

**Leverage**: swarm-orchestration, hive-mind-advanced, cascade-orchestrator
- Don't create new "Clone Army" concept
- Use existing topology options: Hierarchical, Mesh, Adaptive, Byzantine

---

## STEP 4: PRE-MORTEM ANALYSIS

### Risk: Cognitive Overload from 116 Dimensions

**Problem**: 4^116 possible configurations is overwhelming. Even the prompt acknowledges this requires heuristic selection.

**Mitigation**:
- Use pattern-matching heuristics (not enumeration)
- Default to "standard" configuration for most tasks
- Only activate dimensional analysis for complex/ambiguous requests
- Leverage existing playbook routing as first-pass filter

### Risk: Frame Selection Conflicts

**Problem**: What if multiple frames are equally relevant?

**Mitigation**:
- Use weighted scoring (similar to dogfooding pattern ranking)
- Allow frame composition (e.g., Evidential + Social-Hierarchical for formal fact-checking)
- Default to "no frame" for clear, straightforward tasks

### Risk: Integration Complexity

**Problem**: Adding 6 tiers to existing 5-phase workflow could create friction.

**Mitigation**:
- Embed dimensional analysis INTO existing phases (not separate)
- Phase 1 (intent-analyzer): Add frame detection
- Phase 2 (prompt-architect): Add dimensional classification
- Don't add new phases

### Risk: Goodhart's Law on Frame Selection

**Problem**: Optimizing for "correct frame" rather than problem-solving.

**Mitigation**:
- Frame selection is INTERNAL (not shown to user unless requested)
- Success measured by output quality, not frame accuracy
- Use recursive-improvement to validate frame selections work

### Risk: Overhead for Simple Tasks

**Problem**: "Fix this typo" doesn't need dimensional analysis.

**Mitigation**:
- Only activate for complexity > threshold (existing hook logic)
- Maintain escape hatches (explicit skill invocation bypasses)
- Use existing "When NOT to Use" patterns

---

## STEP 5: INTEGRATION PLAN

### Phase A: Create Linguistic Frame Skill (NEW)

**Deliverable**: `skills/foundry/cognitive-frames/SKILL.md`

**Content**:
- 7 linguistic frames with activation patterns
- Frame selection heuristics
- Internal application protocol (not shown unless `*reason` requested)

**Integration**:
- Triggers: "through what lens", "cognitive frame", complex + ambiguous tasks
- Agents: frame-analyst (new), prompt-architect (enhanced)
- MCP: memory-mcp (store frame selections for learning)

### Phase B: Enhance Intent-Analyzer with Frame Detection

**Deliverable**: Update `intent-analyzer/SKILL.md`

**Changes**:
- Add "Frame Detection" sub-phase after constraint detection
- Detect optimal cognitive frame from problem pattern
- Output frame recommendation with confidence score

**Integration**:
- Becomes part of Phase 1 in 5-phase workflow
- Feeds into prompt-architect (Phase 2)

### Phase C: Enhance Prompt-Architect with Dimensional Analysis

**Deliverable**: Update `prompt-architect/SKILL.md` (if exists) or create

**Changes**:
- Add dimensional classification section
- Take frame recommendation from intent-analyzer
- Apply frame-specific prompting patterns

**Integration**:
- Becomes part of Phase 2 in 5-phase workflow
- Uses prompt-forge evidence-based techniques

### Phase D: Add Frame-Analyst Agent to Registry

**Deliverable**: `agents/research/frame-analyst.md`

**Content**:
```yaml
name: frame-analyst
description: Analyzes problems to identify optimal cognitive frames
category: research
mcp_servers:
  required: [memory-mcp]
  optional: []
```

**Integration**:
- Part of 211+ agent registry
- Spawnable via Task() like other agents

### Phase E: Add Adversarial-Critic Agent to Registry

**Deliverable**: `agents/quality/adversarial-critic.md`

**Note**: May already exist as `reviewer` or `code-analyzer`
- Check if existing agents cover this function
- If not, add to registry

### Phase F: Update CLAUDE.md with Cognitive Lensing Protocol

**Deliverable**: Update CLAUDE.md Section 1.7

**Content**:
```markdown
## 1.7 COGNITIVE LENSING (Optional Enhancement)

For complex tasks, the system can apply cognitive frame analysis:

### When Activated
- Complexity > threshold (detected by hooks)
- Explicit invocation: "analyze through cognitive lensing"
- Ambiguity > 30% (multiple interpretations)

### Frame Selection Heuristics
[Quick reference table from analysis]

### Internal Operation
Frame selection is INTERNAL. Output reasoning only with `*reason` flag.
```

### Phase G: Integrate with Dogfooding/Meta-Loop

**Deliverable**: Connect to recursive-improvement

**Integration**:
- Store frame selections in memory-mcp
- Track which frames produce successful outcomes
- Recursive improvement on frame selection heuristics
- Dogfooding: Apply cognitive lensing to its own skill improvements

---

## STEP 6: LEVERAGING META-LOOP FOR ENHANCEMENT

### How Dogfooding System Can Enhance Cognitive Lensing

1. **Quality Detection Phase**:
   - Detect when cognitive frame selection led to poor outcomes
   - Track "frame mismatch" as a new violation type

2. **Pattern Retrieval Phase**:
   - Store successful frame applications in memory-mcp
   - Query for similar problems and their effective frames

3. **Continuous Improvement Phase**:
   - Apply frame selection improvements in sandbox
   - Validate with frozen eval harness
   - Commit only if frame accuracy improves

### How Meta-Loop Can Enhance Cognitive Lensing

1. **Skill-Auditor**: Audit cognitive-frames skill for completeness
2. **Prompt-Auditor**: Validate frame selection prompts use evidence-based techniques
3. **Propose-Test-Compare-Commit**: Frame selection heuristics evolve over time
4. **Frozen Eval Harness**: Frame selections validated against quality benchmarks

### New Dogfooding Violation Types

```yaml
violations:
  - type: frame_mismatch
    description: Cognitive frame selection didn't match problem pattern
    detection: Track frame selected vs. task type, compare to heuristics
    severity: medium

  - type: frame_overhead
    description: Dimensional analysis applied to simple task
    detection: Task complexity < threshold but frame analysis occurred
    severity: low

  - type: missing_frame_detection
    description: Complex task proceeded without frame analysis
    detection: Complexity > threshold but no frame selection
    severity: high
```

---

## STEP 7: SUMMARY - WHAT TO DO

### BUILD NEW

1. **Linguistic Frame Taxonomy** - Novel cognitive science approach
2. **Frame Selection Heuristics** - Pattern -> Frame mapping
3. **Dimensional Analysis Module** - 6-tier classification (simplified)
4. **frame-analyst Agent** - Add to registry

### LEVERAGE EXISTING

1. **Research Protocol** - Use Explore agent
2. **Subagent System** - Use Agent Registry
3. **Hooks** - Extend existing enforcement
4. **Quality Gates** - Use recursive-improvement
5. **Evidence-Based Prompting** - Use prompt-forge
6. **Multi-Agent Topology** - Use swarm-orchestration

### INTEGRATE

1. Embed frame detection in intent-analyzer (Phase 1)
2. Embed dimensional analysis in prompt-architect (Phase 2)
3. Add frame-analyst to agent registry
4. Connect to dogfooding for continuous improvement
5. Gate improvements with frozen eval harness

### DON'T DO

1. Don't create parallel agent system - use registry
2. Don't create new hooks system - extend existing
3. Don't rebuild evidence-based prompting - use prompt-forge
4. Don't create new quality gates - use recursive-improvement
5. Don't enumerate 4^116 configurations - use heuristics

---

## CONCLUSION

The Cognitive Lensing System introduces genuinely novel concepts (linguistic frames, dimensional classification) while proposing infrastructure we already have (hooks, subagents, quality gates, evidence-based prompting).

**Optimal Integration Strategy**:
1. Extract the novel cognitive science insights (linguistic frames, dimensional analysis)
2. Build them as skills/agents within existing infrastructure
3. Leverage existing 5-phase workflow, agent registry, hooks, and meta-loop
4. Use dogfooding to continuously improve frame selection
5. Gate all changes through frozen eval harness

This approach captures the cognitive lensing value without duplicating infrastructure.

**Estimated Effort**:
- Phase A (Cognitive Frames Skill): 2-3 hours
- Phase B (Intent-Analyzer Enhancement): 1-2 hours
- Phase C (Prompt-Architect Enhancement): 1-2 hours
- Phase D-E (Agent Registry): 30 minutes
- Phase F (CLAUDE.md Update): 30 minutes
- Phase G (Meta-Loop Integration): 1-2 hours

**Total**: 6-10 hours of focused implementation

**Value**: Rich cognitive analysis for complex problems while maintaining efficiency for simple tasks.
