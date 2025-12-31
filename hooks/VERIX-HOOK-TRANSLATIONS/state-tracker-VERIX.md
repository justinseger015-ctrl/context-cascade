/*============================================================================*/
/* STATE_TRACKER :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "state-tracker",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] session-$(date +%s) [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] State initialized: $session_id [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Logged skill: $skill_name (phase: $phase) [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Logged agent: $agent_type ($category) [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] VIOLATION: $violation_type - $details [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] TodoWrite marked as called [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Expertise loaded: $domain [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Phase completed: $phase [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S9 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $state [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S10 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $state [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S11 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] VIOLATION: Skill invoked but no agents spawned [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S12 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $state [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S13 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] VIOLATION: Agents spawned but no TodoWrite [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S14 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $state [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S15 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] VIOLATION: $generic_count generic agents used [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S16 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Compliance check: $violations violations found [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S17 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] State archived to: $archive_file [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S18 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Session Summary: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S19 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Skills invoked: $skills [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S20 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Agents spawned: $agents [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S21 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Violations: $violations [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S22 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Usage: $0 {init_state|get_state|log_skill|log_agent|log_violation|mark_todowrite|mark_expertise|mark_phase_complete|check_compliance|archive_state} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>STATE_TRACKER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
