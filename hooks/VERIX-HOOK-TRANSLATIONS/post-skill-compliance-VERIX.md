/*============================================================================*/
/* POST_SKILL_COMPLIANCE :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "post-skill-compliance",
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
[warn|emphatic] !! SKILL EXECUTION COMPLETED - COMPLIANCE CHECK !! [ground:system-policy] [conf:1.0] [state:confirmed]
============================================================

[assert|neutral] You just invoked a Skill. The skill defines the SOP for a task. [ground:witnessed] [conf:0.90] [state:confirmed]
[direct|emphatic] Now you MUST follow the SOP compliance pattern. [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MANDATORY NEXT STEPS: [ground:given] [conf:1.0] [state:confirmed]

[ ] STEP 1: Spawn agents via Task()
  [assert|neutral] Pattern: Task("Agent Name", "Task description", "agent-type") [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Agent type MUST be from registry (206 agents available) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If parallel work: Spawn ALL agents in ONE message [ground:given] [conf:0.95] [state:confirmed]

[ ] STEP 2: Track progress via TodoWrite()
  [assert|neutral] Create 5-10 todos for all planned work [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Include both content and activeForm for each todo [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark in_progress when starting work [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark completed IMMEDIATELY when done (not batched) [ground:given] [conf:0.95] [state:confirmed]

[ ] STEP 3: Load domain expertise (if available)
  [assert|neutral] Check: .claude/expertise/{domain}.yaml [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If exists: Load patterns BEFORE spawning agents [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If not: Agent will create during execution [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] COMPLIANCE CHECKLIST: [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] Did you call Task() to spawn agents?           [ ] [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Are agent types from the registry?             [ ] [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Did you spawn parallel agents in ONE message?  [ ] [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Did you call TodoWrite() with todos?           [ ] [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Did you check for domain expertise?            [ ] [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] If ANY checkbox is UNCHECKED: Complete it NOW before proceeding. [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] PATTERN REMINDER: [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] Skill() defines the SOP [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | (you are here - skill just completed) [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] v [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Task() spawns registry agents to execute SOP [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] v [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] TodoWrite() tracks progress with todos [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] VIOLATION TRACKING: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] If you skip Task(): VIOLATION logged (missing_agents) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If you skip TodoWrite(): VIOLATION logged (missing_todowrite) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If you use generic agent: VIOLATION logged (generic_agent) [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] Your compliance is being tracked. Follow the pattern. [ground:witnessed] [conf:0.90] [state:confirmed]

============================================================

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_DATA [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>POST_SKILL_COMPLIANCE_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
