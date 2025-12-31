/*============================================================================*/
/* SESSION_STOP :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "session-stop",
  type: "General",
  purpose: "Hook script",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

================================================================
[warn|emphatic] !! SESSION ENDING - PATTERN RETENTION FOR NEXT SESSION !! [ground:system-policy] [conf:1.0] [state:confirmed]
================================================================

[assert|neutral] This session is ending. State has been archived. [ground:witnessed] [conf:0.90] [state:confirmed]

[warn|emphatic] CRITICAL PATTERNS TO REMEMBER FOR NEXT SESSION: [ground:system-policy] [conf:1.0] [state:confirmed]

[assert|neutral] 1. 5-PHASE WORKFLOW IS MANDATORY [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] Phase 1: Skill("intent-analyzer") [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Phase 2: Skill("prompt-architect") [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Phase 3: Skill("planner") [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Phase 4: Route to playbooks [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Phase 5: Execute with Skill -> Task -> TodoWrite [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] 2. AGENTS FROM REGISTRY ONLY [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] Location: claude-code-plugins/context-cascade/agents/ [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] 206 agents in 10 categories [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] Fallbacks: coder, researcher, tester, reviewer [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] 3. SOP PATTERN: SKILL -> TASK -> TODOWRITE [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] Skill defines SOP [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Task spawns agents [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] TodoWrite tracks progress [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] 4. GOLDEN RULE: 1 MESSAGE = ALL PARALLEL OPERATIONS [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] Spawn all independent agents in single message [ground:witnessed] [conf:0.90] [state:confirmed]

[assert|neutral] 5. LOAD EXPERTISE BEFORE DOMAIN WORK [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] Check: .claude/expertise/{domain}.yaml [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] Load patterns and file locations before acting [ground:witnessed] [conf:0.90] [state:confirmed]

[assert|neutral] 6. STATE TRACKING IS ACTIVE [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] All actions logged to enforcement state [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Violations recorded and archived [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Compliance checked at each step [ground:witnessed] [conf:0.90] [state:confirmed]

[assert|neutral] 7. HOOK LIMITATIONS [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Hooks remind, not enforce [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Parameter validation is reactive [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Self-enforcement required [ground:witnessed] [conf:0.90] [state:confirmed]

[assert|neutral] 8. META-SKILLS GATED BY FROZEN EVAL HARNESS [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Agent Creator creates auditors for improvement loop [ground:witnessed] [conf:0.90] [state:confirmed]
[direct|emphatic] Eval harness never self-improves (prevents Goodhart's Law) [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] SESSION STATS: [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] (See archived state file for detailed metrics) [ground:witnessed] [conf:0.90] [state:confirmed]

[assert|neutral] Next session will start fresh with these patterns. [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] The enforcement system will activate on first non-trivial request. [ground:witnessed] [conf:0.90] [state:confirmed]

[direct|emphatic] Remember: YOU must follow the patterns. Hooks are guardrails. [ground:system-policy] [conf:1.0] [state:confirmed]

================================================================

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>SESSION_STOP_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
