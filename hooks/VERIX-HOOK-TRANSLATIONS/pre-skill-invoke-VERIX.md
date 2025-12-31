/*============================================================================*/
/* PRE_SKILL_INVOKE :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "pre-skill-invoke",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

============================================================
[warn|emphatic] !! SKILL INVOCATION DETECTED !! [ground:system-policy] [conf:1.0] [state:confirmed]
============================================================

[assert|neutral] Skills are SOPs (Standard Operating Procedures) that define [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] HOW to accomplish tasks. They are NOT direct execution tools. [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] MANDATORY PATTERN: Skill -> Task -> TodoWrite [ground:given] [conf:1.0] [state:confirmed]

[direct|emphatic] After this skill completes, you MUST: [ground:system-policy] [conf:1.0] [state:confirmed]

[assert|neutral] 1. SPAWN AGENTS via Task() [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] Pattern: Task("Agent Name", "Task description", "agent-type") [ground:given] [conf:1.0] [state:confirmed]

[direct|emphatic] Agent types MUST be from registry: [ground:system-policy] [conf:1.0] [state:confirmed]
  [assert|neutral] Registry: claude-code-plugins/context-cascade/agents/ [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] 206 agents in 10 categories [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Fallbacks if unsure: coder, researcher, tester, reviewer [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 2. CREATE TODOS via TodoWrite() [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] Create 5-10 todos for planned work [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark in_progress when starting [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark completed immediately when done [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 3. SPAWN IN PARALLEL (Golden Rule) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] 1 MESSAGE = ALL Task() calls for parallel work [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Do NOT spawn agents sequentially [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 4. LOAD DOMAIN EXPERTISE (if available) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] Check: .claude/expertise/{domain}.yaml [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If exists: Load BEFORE spawning agents [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If not: Agent discovers during execution [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] STATE TRACKING: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] This skill invocation is being logged [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Compliance will be checked after execution [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Violations will be recorded [ground:given] [conf:0.95] [state:confirmed]

============================================================

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_DATA [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>PRE_SKILL_INVOKE_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
