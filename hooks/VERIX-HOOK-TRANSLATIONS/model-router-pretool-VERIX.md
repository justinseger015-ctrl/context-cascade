/*============================================================================*/
/* MODEL_ROUTER_PRETOOL :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "model-router-pretool",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini-megacontext [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini-search [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini-media [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S9 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini-extensions [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S10 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S11 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] codex-yolo [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S12 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S13 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] codex-sandbox [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S14 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S15 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] codex-audit [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S16 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S17 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] codex-reasoning [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S18 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $input_lower [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S19 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] llm-council [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S20 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] claude [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S21 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini --all-files \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S22 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S23 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S24 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini -e auto \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S25 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] gemini --yolo \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S26 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] codex --yolo \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S27 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] codex --full-auto --sandbox true \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S28 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] codex --full-auto --max-iterations 10 \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S29 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] codex \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S30 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] bash scripts/multi-model/llm-council.sh \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S31 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] claude [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S32 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_INPUT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S33 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] { [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] \ [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S34 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TASK_DESC [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S35 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] Task requires analyzing large codebase (Gemini has 1M token context) [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S36 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] Task needs real-time web information (Gemini has Google Search grounding) [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S37 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] Task requires image/video generation (Gemini has Imagen/Veo) [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S38 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] Task involves third-party integration (Gemini has 70+ extensions) [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S39 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] Task can run autonomously overnight (Codex --yolo mode) [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S40 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] Task needs isolated execution (Codex sandbox with network disabled) [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S41 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] Task involves test-fix-retest loops (Codex auto-iteration) [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S42 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

  [assert|neutral] Task benefits from alternative perspective (GPT-5-Codex reasoning) [ground:given] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S43 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[warn|emphatic] - Critical decision benefits from multi-model consensus [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S44 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/


================================================================================
[assert|neutral] Proceeding with Claude agent (override with suggested command if preferred) [ground:witnessed] [conf:0.90] [state:confirmed]
================================================================================


/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>MODEL_ROUTER_PRETOOL_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
