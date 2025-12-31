/*============================================================================*/
/* CANCEL_RALPH :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Cancel an active Ralph Wiggum loop                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "cancel-ralph",
  type: "General",
  purpose: "Cancel an active Ralph Wiggum loop",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] No active Ralph loop found. [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[$(date +%Y-%m-%d\ %H:%M:%S)] Ralph Loop CANCELLED at iteration $ITERATION (session: $SESSION_ID)

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

==========================================

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] RALPH LOOP CANCELLED [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

==========================================

/*----------------------------------------------------------------------------*/
/* S6 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Session ID: $SESSION_ID [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Iterations completed: $ITERATION [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] The loop has been deactivated. [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S9 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] You can start a new loop with /ralph-loop [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>CANCEL_RALPH_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
