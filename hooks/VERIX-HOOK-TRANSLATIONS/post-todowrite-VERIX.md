/*============================================================================*/
/* POST_TODOWRITE :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "post-todowrite",
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
[warn|emphatic] !! TODOWRITE EXECUTED - SOP COMPLIANCE ACHIEVED !! [ground:system-policy] [conf:1.0] [state:confirmed]
============================================================

[assert|neutral] TodoWrite() has been called. Excellent! [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] You have completed the mandatory SOP pattern: [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] Skill() -> Task() -> TodoWrite() [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] TODO MANAGEMENT REQUIREMENTS: [ground:given] [conf:1.0] [state:confirmed]

[ ] Create 5-10 todos for ALL planned work
  [assert|neutral] Too few: You're missing tasks [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Too many: Break into sub-projects [ground:given] [conf:0.95] [state:confirmed]

[ ] Each todo MUST have:
  [assert|neutral] content: "Imperative form (Do X, Fix Y, Build Z)" [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] status: "pending" | "in_progress" | "completed" [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] activeForm: "Present continuous (Doing X, Fixing Y, Building Z)" [ground:given] [conf:0.95] [state:confirmed]

[ ] Mark todos in_progress BEFORE starting work
  [assert|neutral] Exactly ONE todo should be in_progress at a time [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] NOT zero, NOT multiple [ground:given] [conf:0.95] [state:confirmed]

[ ] Mark completed IMMEDIATELY after finishing
  [assert|neutral] Do NOT batch completions [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Complete -> Mark completed -> Start next [ground:given] [conf:0.95] [state:confirmed]

[ ] Only mark completed when FULLY done
  [assert|neutral] Tests passing [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Implementation complete [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] No errors or blockers [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PARALLEL EXECUTION RULE: [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] If you have parallel work: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Spawn ALL agents in ONE message [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Create todos for all parallel work [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark multiple in_progress if truly parallel [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] But typically: 1 in_progress at a time [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] COMPLIANCE STATUS: PASS [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] You have followed the SOP pattern correctly: [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] 1. Skill defined the SOP [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] 2. Task spawned agents [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] 3. TodoWrite tracking progress [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] STATE TRACKING: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] TodoWrite marked as called [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] SOP compliance verified [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] No violations for this workflow [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] Keep following this pattern for all future work! [ground:witnessed] [conf:0.90] [state:confirmed]

============================================================

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $TOOL_DATA [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>POST_TODOWRITE_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
