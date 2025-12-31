/*============================================================================*/
/* PATTERN_RETENTION :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "pattern-retention",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

================================================================
[warn|emphatic] !! CRITICAL: CONTEXT COMPACTION - PATTERN RETENTION !! [ground:system-policy] [conf:1.0] [state:confirmed]
================================================================

[direct|emphatic] The context window is about to compact. These patterns MUST survive: [ground:system-policy] [conf:1.0] [state:confirmed]

================================================================
[direct|emphatic] 1. FIVE-PHASE WORKFLOW (ALWAYS EXECUTE) [ground:system-policy] [conf:1.0] [state:confirmed]
================================================================

[define|neutral] For EVERY non-trivial request, execute IN ORDER: [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] Phase 1: Skill("intent-analyzer")     -> Understand true intent [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Phase 2: Skill("prompt-architect")    -> Optimize the request [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Phase 3: Skill("planner")             -> Create execution plan [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Phase 4: Route to playbooks           -> Select tools per task [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Phase 5: Execute with Task()          -> Spawn registry agents [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] DO NOT skip phases. DO NOT jump to execution. [ground:witnessed] [conf:0.90] [state:confirmed]

================================================================
[direct|emphatic] 2. AGENT REGISTRY ENFORCEMENT (NEVER USE GENERIC) [ground:system-policy] [conf:1.0] [state:confirmed]
================================================================

[define|neutral] ONLY spawn agents from the registry: [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Path: claude-code-plugins/context-cascade/agents/ [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Count: 206 agents in 10 categories [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] Categories: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] delivery (18): coder, backend-dev, frontend-dev... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] orchestration (21): hierarchical-coordinator, byzantine-coordinator... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] quality (18): code-analyzer, theater-detection-audit... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] research (11): researcher, analyst... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] foundry (15): agent-creator, skill-creator... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] operations (12): cicd-engineer, monitoring-engineer... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] platforms (8): platform-engineer, cloud-architect... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] security (9): security-engineer, penetration-tester... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] specialists (50+): python-expert, javascript-expert... [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] tooling (14): build-engineer, package-manager... [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] Fallbacks if unsure: coder, researcher, tester, reviewer [ground:given] [conf:1.0] [state:confirmed]

[direct|emphatic] NEVER use made-up agent types. NEVER use generic descriptions. [ground:system-policy] [conf:1.0] [state:confirmed]

================================================================
[direct|emphatic] 3. SKILL -> TASK -> TODOWRITE PATTERN (ALWAYS FOLLOW) [ground:system-policy] [conf:1.0] [state:confirmed]
================================================================

[assert|neutral] Skill defines the SOP (how to do something) [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] v [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Task() spawns agents to EXECUTE the SOP [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] v [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] TodoWrite() tracks progress with 5-10 todos [ground:witnessed] [conf:0.90] [state:confirmed]

[assert|neutral] This pattern is MANDATORY. No exceptions. [ground:witnessed] [conf:0.90] [state:confirmed]

================================================================
[define|neutral] 4. GOLDEN RULE: ONE MESSAGE = ALL PARALLEL OPERATIONS [ground:given] [conf:1.0] [state:confirmed]
================================================================

[define|neutral] WRONG: Spawn agent 1, wait, spawn agent 2, wait... [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] RIGHT: One message with ALL Task() calls for parallel work [ground:given] [conf:1.0] [state:confirmed]

[Single Message]:
[assert|neutral] Task("Agent 1", "...", "type1") [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Task("Agent 2", "...", "type2") [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Task("Agent 3", "...", "type3") [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] TodoWrite({todos: [...]}) [ground:given] [conf:1.0] [state:confirmed]

================================================================
[assert|neutral] 5. EXPERTISE SYSTEM (LOAD BEFORE ACTING) [ground:witnessed] [conf:0.90] [state:confirmed]
================================================================

[define|neutral] Before any domain-specific work: [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] 1. Check: .claude/expertise/{domain}.yaml [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] 2. If exists: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Run /expertise-validate {domain} [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Load patterns, file locations, known issues [ground:given] [conf:0.95] [state:confirmed]
[define|neutral] 3. If not exists: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Agent should discover and create expertise [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] Expertise enables: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] No search thrash (known file locations) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Pattern compliance (documented conventions) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Issue avoidance (known problems) [ground:given] [conf:0.95] [state:confirmed]

================================================================
[assert|neutral] 6. STATE TRACKING (ENFORCEMENT ACTIVE) [ground:witnessed] [conf:0.90] [state:confirmed]
================================================================

[define|neutral] The enforcement system is tracking: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] All skill invocations [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] All agent spawns [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] All TodoWrite calls [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] All violations [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] State file: .claude/runtime/enforcement-state.json [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] Violations logged: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] generic_agent: Non-registry agent type used [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] missing_agents: Skill invoked without Task() [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] missing_todowrite: Agents spawned without TodoWrite() [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] skipped_phase: Phase skipped in 5-phase workflow [ground:given] [conf:0.95] [state:confirmed]

================================================================
[warn|emphatic] 7. HOOK LIMITATIONS (CRITICAL UNDERSTANDING) [ground:system-policy] [conf:1.0] [state:confirmed]
================================================================

[define|neutral] Hooks CANNOT: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Inspect Task() parameters (no agent type validation in PreToolUse) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Modify inputs/outputs [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Force tool calls [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Access conversation transcript [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Block based on parameter validation [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] Hooks CAN: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Display reminders (preventive) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Log invocations (detective) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Check compliance after execution (reactive) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Track state across conversation [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] This means: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Enforcement is primarily REMINDER-BASED [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Validation is REACTIVE (after actions) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Agent type validation happens via transcript parsing [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Compliance checking happens in PostToolUse [ground:given] [conf:0.95] [state:confirmed]

[direct|emphatic] YOU must self-enforce. Hooks are guardrails, not barriers. [ground:system-policy] [conf:1.0] [state:confirmed]

================================================================
[assert|neutral] 8. RECURSIVE IMPROVEMENT SYSTEM (META-SKILLS) [ground:witnessed] [conf:0.90] [state:confirmed]
================================================================

[define|neutral] The system can improve itself via: [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] FOUNDRY (creates components): [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Agent Creator --> Creates auditor agents [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] IMPROVEMENT LOOP: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Prompt Forge --> Improves prompts (including Skill Forge) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Skill Forge --> Applies improvements (including to itself) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Auditor Agents --> Find issues (prompt, skill, expertise, output) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Eval Harness --> Gates ALL changes (FROZEN - never self-improves) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PIPELINE: [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] PROPOSE -> TEST -> COMPARE -> COMMIT -> MONITOR -> ROLLBACK [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] KEY CONSTRAINT: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Eval harness does NOT self-improve (prevents Goodhart's Law) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Changes must pass benchmarks + regressions [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Archive before commit (enables rollback) [ground:given] [conf:0.95] [state:confirmed]

================================================================
[assert|neutral] POST-COMPACT CHECKLIST [ground:witnessed] [conf:0.90] [state:confirmed]
================================================================

[define|neutral] After compaction, verify you remember: [ground:given] [conf:1.0] [state:confirmed]
[ ] 5-phase workflow is MANDATORY
[ ] Agents come from registry ONLY
[ ] Pattern: Skill -> Task -> TodoWrite
[ ] 1 message = all parallel operations
[ ] Load expertise before domain work
[ ] State tracking is active
[ ] Hook limitations (reminders, not barriers)
[ ] Self-enforcement is required
[ ] Meta-skills gated by frozen eval harness
[ ] Agent Creator creates auditors for the loop

[define|neutral] If you've forgotten anything: RE-READ THIS REMINDER. [ground:given] [conf:1.0] [state:confirmed]

================================================================

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>PATTERN_RETENTION_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
