# META-LOOP BOOTSTRAP PLAN

## The Vision (User's Insight)

We built a **dual-layer DSPy x MOO x VERILINGUA x VERIX optimization system** to:

### Layer 1: Language Evolution (Slow, Monthly)
Optimize the VERILINGUA x VERIX language ITSELF by finding patterns in:
- What frame combinations work for which task types
- What VERIX strictness levels produce best outcomes
- How compression levels trade off against accuracy

### Layer 2: Prompt Expression (Fast, Per-Cluster)
Optimize the PROMPTS that USE the language:
- Task() calls to subagents
- Commands, skills, playbooks content
- The meta-tools themselves (agent-creator, skill-forge, prompt-architect)

### The Meta-Loop Core
The recursive triangle that can improve everything:

```
        AGENT CREATOR
           /     \
          /       \
         v         v
  SKILL FORGE <---> PROMPT ARCHITECT
```

**Key Insight**: If these three are perfected, improvements can spread everywhere.

---

## PHASE 1: INTENT ANALYSIS

### Understood Intent (Confidence: 95%)

**Primary Goal**: Bootstrap the meta-loop core to self-referential perfection using:
1. Ralph Wiggum hooks to force authenticated success
2. Real debugging task (Triple Memory MCP) to generate optimization data
3. Feed data back into DSPy x MOO optimization
4. Perfect the core, then spread outward

### Explicit Constraints
- Use Ralph Wiggum persistence loops (already in plugin)
- Apply Connascence Analyzer for code quality
- Target Triple Memory MCP as data-gathering task
- Enforce success authentication before completion

### Implicit Constraints
- Must not break existing functionality
- Eval harness must remain FROZEN
- Multi-agent disagreement triggers human review
- All changes must be reversible (90-day rollback)

### Task Decomposition

| Task | Type | Data Source |
|------|------|-------------|
| Fix Triple Memory MCP violations | Real debugging | Connascence results |
| Audit agent-creator skill | Meta-improvement | Bootstrap loop |
| Audit skill-forge skill | Meta-improvement | Bootstrap loop |
| Audit prompt-architect skill | Meta-improvement | Bootstrap loop |
| Feed outcomes to optimization | Layer 2 | Execution metrics |
| Evolve language patterns | Layer 1 | Aggregated outcomes |

---

## PHASE 2: OPTIMIZED REQUEST

### Original Request
"Review the REASON we built all this... make a plan that includes research and debugging the triple memory mcp project and using the connascence analyzer to improve its code."

### Optimized Request
"Execute a two-track meta-loop bootstrap:

**TRACK A (Data Generation)**: Debug Triple Memory MCP using Connascence Analyzer
- Fix 45 identified violations across 19 files
- Track all outcomes (success/failure, time, patterns)
- Feed metrics to optimization layer

**TRACK B (Meta-Loop Perfection)**: Bootstrap the core triangle
- Run agent-creator through 6-phase improvement cycle
- Run skill-forge through 6-phase improvement cycle
- Run prompt-architect through 6-phase improvement cycle
- Use Ralph Wiggum hooks to enforce completion

**CONVERGENCE**: Use Track A data to optimize Track B operations

**SUCCESS CRITERIA**:
1. All 45 Memory MCP violations fixed (verified by Connascence)
2. All three meta-tools pass eval harness benchmarks
3. Optimization data logged for Layer 1/2 analysis
4. Ralph loops complete with authenticated success"

---

## PHASE 3: STRATEGIC PLAN

### Dependency Graph

```
[Parallel Track A]                    [Parallel Track B]
        |                                     |
   Connascence Analysis              Load Meta-Tool Skills
        |                                     |
   Identify Violations                 Audit Each Tool
        |                                     |
   Fix Violations (in Ralph loop)      Propose Improvements
        |                                     |
   Verify Fixes                        Apply via Skill Forge
        |                                     |
        +---------> CONVERGE <--------+
                       |
              Aggregate Outcomes
                       |
              Feed to Optimization
                       |
             [5-dim GlobalMOO Pass]
                       |
             [14-dim PyMOO Refinement]
                       |
              Update Named Modes
```

### Sequential Phases

#### PHASE A: PREPARATION (Sequential - Must Complete First)
1. Load existing Connascence analysis for Triple Memory MCP
2. Load meta-tool skills (agent-creator, skill-forge, prompt-architect)
3. Verify Ralph Wiggum hooks are active
4. Initialize optimization tracking

#### PHASE B: PARALLEL EXECUTION (Can Run Concurrently)

**Track A: Memory MCP Debugging**
- Ralph loop: Fix violations until Connascence passes
- Target: 0 critical, 0 high violations
- Max iterations: 30
- Completion promise: "CONNASCENCE_CLEAN"

**Track B-1: Agent Creator Improvement**
- 6-phase bootstrap loop
- Auditor: skill-auditor
- Completion promise: "AGENT_CREATOR_IMPROVED"

**Track B-2: Skill Forge Improvement**
- 6-phase bootstrap loop (uses previous version)
- Auditor: prompt-auditor
- Completion promise: "SKILL_FORGE_IMPROVED"

**Track B-3: Prompt Architect Improvement**
- 6-phase bootstrap loop
- Auditor: output-auditor
- Completion promise: "PROMPT_ARCHITECT_IMPROVED"

#### PHASE C: CONVERGENCE (Sequential - After All Complete)
1. Aggregate all execution outcomes
2. Extract patterns for optimization
3. Run 5-dim GlobalMOO pass with new data
4. Run 14-dim PyMOO refinement
5. Update named modes

#### PHASE D: VALIDATION (Sequential - Final)
1. Verify all Ralph loops completed with success
2. Verify Connascence shows clean
3. Verify eval harness passes
4. Document lessons learned

---

## PHASE 4: PLAYBOOK/SKILL ROUTING

### Track A Routing

| Task | Playbook | Skills | Agents |
|------|----------|--------|--------|
| Load Connascence results | quality-check | connascence-quality-gate | code-analyzer |
| Fix violations | smart-bug-fix | debugging, clarity-linter | coder, reviewer |
| Verify fixes | functionality-audit | testing-quality | tester |
| Track metrics | observability | performance-analysis | evaluator |

### Track B Routing

| Task | Playbook | Skills | Agents |
|------|----------|--------|--------|
| Audit meta-tools | comprehensive-review | code-review-assistant | reviewer, code-analyzer |
| Propose improvements | research-driven-planning | prompt-architect | prompt-improver |
| Apply improvements | three-loop-system | skill-forge | sparc-coder |
| Evaluate results | testing-quality | verification-quality | tester, evaluator |

### Meta-Loop Routing

| Component | Improvement Target | Auditor Agent |
|-----------|-------------------|---------------|
| agent-creator | Agent generation prompts | skill-auditor |
| skill-forge | Skill creation methodology | prompt-auditor |
| prompt-architect | Prompt optimization patterns | output-auditor |

---

## PHASE 5: EXECUTION PLAN

### Step 1: Initialize Ralph Loops

```bash
# Track A: Memory MCP Debugging
/ralph-loop "Fix all Connascence violations in Triple Memory MCP.
Use mcp__connascence-analyzer__analyze_workspace on memory-mcp directory.
Fix each violation following NASA/MECE guidelines.
Re-run analysis after each fix batch.
Output <promise>CONNASCENCE_CLEAN</promise> when 0 critical and 0 high violations." \
  --completion-promise "CONNASCENCE_CLEAN" \
  --max-iterations 30

# Track B-1: Agent Creator
/meta-loop-foundry "Improve agent generation prompts for clarity and completeness" \
  --target "skills/agent-creator/SKILL.md" \
  --foundry "prompt-forge"

# Track B-2: Skill Forge
/meta-loop-foundry "Improve skill creation methodology for better structure" \
  --target "skills/skill-forge/SKILL.md" \
  --foundry "skill-forge"

# Track B-3: Prompt Architect
/meta-loop-foundry "Improve prompt optimization patterns for precision" \
  --target "skills/prompt-architect/SKILL.md" \
  --foundry "prompt-forge"
```

### Step 2: Monitor and Converge

```python
# Pseudo-code for convergence
outcomes = []

for track in [track_a, track_b1, track_b2, track_b3]:
    result = wait_for_ralph_completion(track)
    outcomes.append({
        "track": track.name,
        "success": result.success,
        "iterations": result.iteration_count,
        "metrics": result.quality_scores,
        "patterns": extract_patterns(result.execution_log)
    })

# Feed to optimization
optimization_data = aggregate_outcomes(outcomes)
run_globalmoo_5dim(optimization_data)
run_pymoo_refinement(optimization_data)
update_named_modes()
```

### Step 3: Validation Checklist

- [ ] Triple Memory MCP passes Connascence (0 critical, 0 high)
- [ ] agent-creator passes eval harness benchmarks
- [ ] skill-forge passes eval harness benchmarks
- [ ] prompt-architect passes eval harness benchmarks
- [ ] All Ralph loops exited with authenticated success
- [ ] Optimization data logged to storage
- [ ] Named modes updated with new insights

---

## SUCCESS METRICS

| Metric | Target | Measurement |
|--------|--------|-------------|
| Memory MCP violations | 0 critical, 0 high | Connascence report |
| Meta-tool improvement | >60% accepted | Proposal acceptance rate |
| Ralph completion | 100% | All loops exit with promise |
| Optimization cycles | >=1 complete | GlobalMOO + PyMOO runs |
| Data points generated | >50 | Execution outcomes logged |

---

## RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| Ralph loop infinite | Max iterations = 30, hard stop |
| Meta-tool regression | Eval harness gate, instant rollback |
| Connascence false positive | Manual review of critical findings |
| Optimization divergence | Use existing Pareto as anchor |

---

## NEXT IMMEDIATE ACTIONS

1. **Read existing Connascence analysis** for Memory MCP
2. **Verify Ralph hooks** are properly configured
3. **Start Track A** (Memory MCP debugging) first to generate data
4. **Start Track B** (Meta-loop bootstrap) in parallel
5. **Monitor convergence** and feed to optimization

---

*Generated: 2025-12-28*
*Method: 5-Phase Workflow with UltraThink Analysis*
