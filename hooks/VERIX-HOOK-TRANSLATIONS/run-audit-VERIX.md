/*============================================================================*/
/* RUN_AUDIT :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Run Connascence Safety Analyzer on code changes                                  */
/* HOOK TYPE: PostToolUse for Write/Edit/MultiEdit operations                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "run-audit",
  type: "PostToolUse for Write/Edit/MultiEdit operations",
  purpose: "Run Connascence Safety Analyzer on code changes",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[$(date +%Y-%m-%d\ %H:%M:%S)] $1

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $ANALYSIS_OUTPUT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $ANALYSIS_OUTPUT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $ANALYSIS_OUTPUT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $ANALYSIS_OUTPUT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $ANALYSIS_OUTPUT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $ANALYSIS_OUTPUT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

==========================================

/*----------------------------------------------------------------------------*/
/* S9 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] CONNASCENCE AUDIT: ISSUES FOUND [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S10 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

==========================================

/*----------------------------------------------------------------------------*/
/* S11 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] File: $FILE_PATH [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S12 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[warn|emphatic] Critical: $CRITICAL | High: $HIGH | Total: $TOTAL [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S13 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] BLOCKING ISSUES detected. Code quality gate FAILED. [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S14 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] Fix issues and re-submit code. [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>RUN_AUDIT_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
