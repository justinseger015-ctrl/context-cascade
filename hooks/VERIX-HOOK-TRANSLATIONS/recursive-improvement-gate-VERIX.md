/*============================================================================*/
/* RECURSIVE_IMPROVEMENT_GATE :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Gate all self-improvement changes through eval harness                                  */
/* HOOK TYPE: PreToolUse (runs before Write/Edit on improvement targets)                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "recursive-improvement-gate",
  type: "PreToolUse (runs before Write/Edit on improvement targets)",
  purpose: "Gate all self-improvement changes through eval harness",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

================================================================
[warn|emphatic] !! RECURSIVE IMPROVEMENT GATE !! [ground:system-policy] [conf:1.0] [state:confirmed]
================================================================

[assert|neutral] You are modifying a META-SKILL that powers the recursive improvement system. [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] TARGET DETECTED: This file is part of the self-improvement loop. [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] MANDATORY REQUIREMENTS: [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] 1. EVAL HARNESS GATE [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] ALL changes to meta-skills MUST pass eval-harness [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Run: Skill("eval-harness") after changes [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Benchmarks + Regressions must pass [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 2. ARCHIVE BEFORE MODIFY [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] Current version MUST be archived first [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Path: .archive/SKILL-v{current}.md [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Enables rollback if regression detected [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 3. FORBIDDEN CHANGES [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] NEVER remove safeguards [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] NEVER bypass eval harness [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] NEVER modify frozen benchmarks [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] NEVER weaken contract requirements [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 4. SPECIAL RULES FOR EVAL-HARNESS [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] eval-harness does NOT self-improve [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Changes to eval-harness require MANUAL human approval [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Only expansion allowed (never reduction) [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 5. SELF-REBUILD SAFETY [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] skill-forge rebuilding itself uses PREVIOUS version [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Never use current version to rebuild current version [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PROCEED ONLY IF: [ground:given] [conf:1.0] [state:confirmed]
[ ] Change improves the system (not just different)
[ ] Eval harness will be run after
[ ] Archive exists for rollback
[ ] No forbidden changes included

================================================================

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_INPUT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $FILE_PATH [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>RECURSIVE_IMPROVEMENT_GATE_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
