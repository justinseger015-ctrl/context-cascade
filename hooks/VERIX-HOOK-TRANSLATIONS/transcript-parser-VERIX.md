/*============================================================================*/
/* TRANSCRIPT_PARSER :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "transcript-parser",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Transcript file not found: $TRANSCRIPT_FILE [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] No Task() calls found in transcript [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] Found Task() calls, parsing... [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $task_calls [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $task_line [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] INVALID AGENT TYPE: $agent_type [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Valid agent type: $agent_type [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Loading agent registry from: $REGISTRY_FILE [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S9 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] Loaded $(echo [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S10 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] Registry file not found, using hardcoded types [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S11 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

=== Transcript Parser - Agent Type Validation ===

/*----------------------------------------------------------------------------*/
/* S12 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

=== Validation Complete ===

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>TRANSCRIPT_PARSER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
