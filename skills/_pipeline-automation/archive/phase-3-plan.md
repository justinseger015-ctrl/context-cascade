

## When to Use This Skill

- **Tool Usage**: When you need to execute specific tools, lookup reference materials, or run automation pipelines
- **Reference Lookup**: When you need to access documented patterns, best practices, or technical specifications
- **Automation Needs**: When you need to run standardized workflows or pipeline processes

## When NOT to Use This Skill

- **Manual Processes**: Avoid when manual intervention is more appropriate than automated tools
- **Non-Standard Tools**: Do not use when tools are deprecated, unsupported, or outside standard toolkit

## Success Criteria

- **Tool Executed Correctly**: Verify tool runs without errors and produces expected output
- **Reference Accurate**: Confirm reference material is current and applicable
- **Pipeline Complete**: Ensure automation pipeline completes all stages successfully

## Edge Cases

- **Tool Unavailable**: Handle scenarios where required tool is not installed or accessible
- **Outdated References**: Detect when reference material is obsolete or superseded
- **Pipeline Failures**: Recover gracefully from mid-pipeline failures with clear error messages

## Guardrails

- **NEVER use deprecated tools**: Always verify tool versions and support status before execution
- **ALWAYS verify outputs**: Validate tool outputs match expected format and content
- **ALWAYS check health**: Run tool health checks before critical operations

## Evidence-Based Validation

- **Tool Health Checks**: Execute diagnostic commands to verify tool functionality before use
- **Output Validation**: Compare actual outputs against expected schemas or patterns
- **Pipeline Monitoring**: Track pipeline execution metrics and success rates

# Phase 3: Mass Enhancement Plan
You are executing a multi-stage workflow with defined phase gates. Follow the prescribed sequence rigorously. Validate completion criteria at each stage before advancing. Maintain state consistency across phases. Document decision points and branching logic clearly.
You are executing a multi-stage workflow with defined phase gates. Follow the prescribed sequence rigorously. Validate completion criteria at each stage before advancing. Maintain state consistency across phases. Document decision points and branching logic clearly.

**Date**: 2025-11-02
**Total Skills**: 110
**Already Enhanced**: 8 (5 from Batch 1, 3 pre-existing)
**Needing Enhancement**: 102

---

## Strategy

### Batch Processing Approach
- Process in batches of **10-15 skills** for manageable concurrent agent execution
- Run enhancement → cleanup → audit cycle for each batch
- Track progress and metrics per batch

### Enhancement Pipeline (Proven from Batch 1)
1. **Generate Enhancement Plans**: Run `enhance-skill.py` for all skills in batch
2. **Manual skill.md Creation**: Use skill-forge template for any missing skill.md files
3. **Spawn Enhancement Agents**: Use Claude Code Task tool for parallel content creation
4. **Run Cleanup**: Execute `cleanup-skill.py` on all batch skills
5. **Audit**: Run `audit-skill.py` to validate quality
6. **Iterate**: Fix any failures and re-audit

### Success Criteria
- **Pass Rate**: ≥90% (90+ skills pass audit on first try)
- **Average Score**: ≥85%
- **All Structural Checks**: 100% pass (no orphaned files, proper naming)
- **Completion Time**: <48 hours for all 102 skills

---

## Batch Organization

### Batch Size Determination
- **10 skills** = Conservative, high success rate
- **15 skills** = Balanced, good throughput
- **20 skills** = Aggressive, higher risk of issues

**Recommended**: Start with 15-skill batches, adjust based on pass rate

### Batch Distribution
- **Total**: 102 skills
- **7 batches of 15**: 105 skills (includes 3 from already-enhanced for safety)
- **Estimated Time**: 4-6 hours per batch = 28-42 hours total

---

## Risk Mitigation

### Known Issues from Batch 1
1. ✅ **Missing skill.md** - SOLVED: Manual creation using skill-forge template
2. ✅ **Orphaned files** - SOLVED: cleanup-skill.py automates
3. ✅ **Naming violations** - SOLVED: cleanup-skill.py handles
4. ✅ **Invalid directories** - SOLVED: cleanup-skill.py removes

### New Risks for Phase 3
1. **Scale**: 102 skills vs. 5 in Batch 1
   - *Mitigation*: Batch processing with checkpoints
2. **Variety**: Unknown skill complexity distribution
   - *Mitigation*: Start with simpler skills, adapt as needed
3. **Agent Fatigue**: Long-running parallel tasks
   - *Mitigation*: Batch sizes limit concurrent load
4. **Manual Effort**: 102 skill.md files to create
   - *Mitigation*: Template-based, ~2 min per skill = 3.5 hours total

---

## Execution Plan

### Phase 3A: Preparation (30 minutes)
- [x] Analyze skill inventory
- [ ] Create batch assignments (7 batches of ~15 skills)
- [ ] Generate all enhancement plans
- [ ] Identify any special-case skills

### Phase 3B: Batch Enhancement (28-42 hours)
For each batch:
1. Manual skill.md creation (15 files × 2 min = 30 min)
2. Spawn enhancement agents (25-30 min parallel execution)
3. Run cleanup (2-3 min)
4. Audit all skills (5 min)
5. Fix failures if any (15-30 min)
6. Generate batch report (5 min)

**Per-Batch Time**: 1.5-2 hours
**Total for 7 batches**: 10.5-14 hours actual work + 14-28 hours agent execution

### Phase 3C: Final Validation (2 hours)
- Audit all 102 enhanced skills
- Generate comprehensive metrics
- Create Phase 3 completion report
- Commit all enhancements to repository

---

## Success Tracking

### Metrics to Track
- **Pass Rate per Batch**: % of skills passing audit
- **Average Score per Batch**: Mean audit score
- **Enhancement Velocity**: Skills enhanced per hour
- **Manual Intervention Rate**: % requiring manual fixes
- **Component Coverage**: % with examples/, references/, graphviz/

### Quality Gates
- **Batch Pass Rate < 80%**: STOP and analyze issues before continuing
- **Average Score < 85%**: Investigate root causes
- **Manual Intervention > 20%**: Refine automation scripts

---

## Optimizations

### Parallel Execution
- Use Claude Code Task tool to spawn up to 15 agents concurrently
- Each agent enhances 1 skill independently
- Memory-MCP for coordination and progress tracking

### Automation Improvements
- Consider batch script for running enhance-skill.py on all skills
- Automated skill.md generation using skill-forge template + GPT-4
- Batch audit script to process all skills in one command

### Template Reuse
- skill-forge structure for all skills
- Consistent examples/ format across skills
- Standard graphviz/ workflow diagrams

---

## Estimated Timeline

### Conservative (48 hours total)
- Day 1: Batches 1-3 (45 skills)
- Day 2: Batches 4-5 (30 skills)
- Day 3: Batches 6-7 (27 skills) + final validation

### Aggressive (24 hours total)
- Day 1: Batches 1-4 (60 skills)
- Day 2: Batches 5-7 (42 skills) + final validation

**Recommended**: Conservative approach with checkpoints

---

## Next Steps

1. **Immediate**: Generate batch assignments
2. **Next**: Start Batch 1 (15 skills)
3. **Then**: Iterate through all batches
4. **Finally**: Comprehensive validation and reporting
