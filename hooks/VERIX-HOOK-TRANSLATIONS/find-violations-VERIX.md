/*============================================================================*/
/* FIND_VIOLATIONS :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "find-violations",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

=== Violation Report ===

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] CURRENT SESSION: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Session: $SESSION_ID [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Violations: $VIOLATIONS [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] ARCHIVED SESSIONS: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Session: $SESSION_ID [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Started: $STARTED [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Violations: $VIOLATIONS [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S9 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SUMMARY: [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S10 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Total Archived Sessions: $(echo [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S11 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] Total Violations: $TOTAL_VIOLATIONS [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S12 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] No archived sessions found [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S13 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

=== End of Report ===

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>FIND_VIOLATIONS_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
