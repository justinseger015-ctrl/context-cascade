/*============================================================================*/
/* POST_TASK_SPAWN :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "post-task-spawn",
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
[warn|emphatic] !! AGENT SPAWNED VIA TASK !! [ground:system-policy] [conf:1.0] [state:confirmed]
============================================================

[assert|neutral] An agent has been spawned. Great! [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] NEXT MANDATORY STEPS: [ground:given] [conf:1.0] [state:confirmed]

[ ] STEP 1: Verify agent type is from registry
  [assert|neutral] Registry: claude-code-plugins/context-cascade/agents/ [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] 206 agents in 10 categories [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If you used a generic type: FIX IT NOW [ground:given] [conf:0.95] [state:confirmed]

[ ] STEP 2: If spawning multiple agents (parallel work):
  [assert|neutral] Spawn ALL agents in THIS message [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Do NOT spawn one, wait, spawn another [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Golden Rule: 1 MESSAGE = ALL PARALLEL OPERATIONS [ground:given] [conf:0.95] [state:confirmed]

[ ] STEP 3: After ALL agents spawned, call TodoWrite()
  [assert|neutral] Create 5-10 todos for all planned work [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Format: {content: "Do X", status: "pending", activeForm: "Doing X"} [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark in_progress when starting work [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark completed IMMEDIATELY when done [ground:given] [conf:0.95] [state:confirmed]

[ ] STEP 4: Ensure domain expertise was loaded (if available)
  [assert|neutral] Did you check .claude/expertise/{domain}.yaml? [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If exists: Did you load it BEFORE spawning? [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If not: Agent will create during execution [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] POST-SPAWN CHECKLIST: [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] Are ALL parallel agents spawned in THIS message?  [ ] [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Did you call TodoWrite() with todos?              [ ] [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Did todos include both content and activeForm?    [ ] [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Did you load domain expertise before spawning?    [ ] [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] PATTERN REMINDER: [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] Skill() -> Task() -> TodoWrite() [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] ^^^^^ [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] (you are here) [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] v [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] TodoWrite() <- REQUIRED NEXT [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] LIMITATION NOTE: [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] This hook may not have access to your agent type parameter [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Validation will happen via transcript parsing [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Please ensure you used a registry agent type [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] STATE TRACKING: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Agent spawn logged (if parameters accessible) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Compliance check will run after TodoWrite [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Violations recorded in state file [ground:given] [conf:0.95] [state:confirmed]

============================================================

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_DATA [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_DATA [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_DATA [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_DATA [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>POST_TASK_SPAWN_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
