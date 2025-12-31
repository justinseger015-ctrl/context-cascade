/*============================================================================*/
/* PRE_TASK_PLUGIN_REMINDER :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "pre-task-plugin-reminder",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

==================================================

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[warn|emphatic] !! RUV-SPARC PLUGIN REMINDER !! [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

==================================================

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] BEFORE spawning this agent, verify: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] 1. Agent exists in registry: claude-code-plugins/context-cascade/agents/ [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] 2. Agent name matches registry (not invented) [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] 3. You invoked a Skill() before this Task() [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Agent Categories Available: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S9 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] delivery (18): backend, frontend, architecture [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S10 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] foundry (19): agent creation, templates [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S11 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] operations (28): DevOps, infrastructure [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S12 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] orchestration (21): swarm coordinators [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S13 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] platforms (44): AI/ML, neural, data [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S14 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] quality (18): analysis, testing [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S15 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] research (11): research, reasoning [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S16 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] security (5): compliance, pentest [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S17 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] specialists (15): business, domain [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S18 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] tooling (24): docs, GitHub [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S19 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] If agent not in registry, use fallback: coder, researcher, tester, reviewer [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S20 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

==================================================

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>PRE_TASK_PLUGIN_REMINDER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
