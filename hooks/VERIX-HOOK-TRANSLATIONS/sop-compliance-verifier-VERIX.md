/*============================================================================*/
/* SOP_COMPLIANCE_VERIFIER :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Verify that Skill SOPs are being followed correctly                                  */
/* HOOK TYPE: PostToolUse (runs after Skill invocation)                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "sop-compliance-verifier",
  type: "PostToolUse (runs after Skill invocation)",
  purpose: "Verify that Skill SOPs are being followed correctly",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

============================================================
[warn|emphatic] !! SKILL SOP COMPLIANCE CHECK !! [ground:system-policy] [conf:1.0] [state:confirmed]
============================================================

[assert|neutral] You just invoked a Skill. Skills are SOPs (Standard Operating Procedures) [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] that define HOW to accomplish tasks. They are NOT execution tools. [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] MANDATORY POST-SKILL REQUIREMENTS: [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] 1. SPAWN AGENTS via Task() [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] Skills define the SOP [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Task() spawns agents to EXECUTE the SOP [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Pattern: Task("Agent Name", "Task description", "agent-type") [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Agent types MUST be from registry (206 agents available) [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 2. AGENTS FROM REGISTRY ONLY [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] Registry: claude-code-plugins/context-cascade/agents/ [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Categories: delivery, foundry, operations, orchestration, platforms, [ground:given] [conf:0.95] [state:confirmed]
[assert|neutral] quality, research, security, specialists, tooling [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] If unsure: Use fallback types (coder, researcher, tester, reviewer) [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 3. TRACK WITH TodoWrite() [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] Create 5-10 todos for all planned work [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark in_progress when starting a task [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark completed when done (IMMEDIATELY, not batched) [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 4. SPAWN IN PARALLEL (Golden Rule) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] 1 MESSAGE = ALL PARALLEL Task() calls [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Don't spawn one agent, wait, spawn another [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Spawn ALL independent agents in a SINGLE message [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 5. LOAD DOMAIN EXPERTISE [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] Check: .claude/expertise/{domain}.yaml [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If exists: Load BEFORE spawning agents [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If not: Agent should discover and create expertise [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] COMPLIANCE CHECK: [ground:given] [conf:1.0] [state:confirmed]
[ ] Did you call Task() to spawn agents?
[ ] Is agent type from the registry?
[ ] Did you call TodoWrite() with todos?
[ ] Are parallel tasks in ONE message?
[ ] Did you load domain expertise if available?

[define|neutral] If ANY checkbox is unchecked: DO IT NOW before proceeding. [ground:given] [conf:1.0] [state:confirmed]

============================================================

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_DATA [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>SOP_COMPLIANCE_VERIFIER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
