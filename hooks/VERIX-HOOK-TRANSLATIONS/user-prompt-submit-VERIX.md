/*============================================================================*/
/* USER_PROMPT_SUBMIT :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "user-prompt-submit",
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
[warn|emphatic] !! 5-PHASE WORKFLOW ENFORCEMENT ACTIVE !! [ground:system-policy] [conf:1.0] [state:confirmed]
================================================================

[define|neutral] This is a NON-TRIVIAL request. MANDATORY 5-phase workflow: [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] PHASE 1: INTENT ANALYSIS [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Tool: Skill("intent-analyzer") [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Output: Understood intent + confidence score [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Gate: If confidence < 80%, ask clarifying questions [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] PHASE 2: PROMPT OPTIMIZATION [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Tool: Skill("prompt-architect") [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Output: Optimized request + success criteria [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] PHASE 3: STRATEGIC PLANNING [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Tool: Skill("research-driven-planning") OR Skill("planner") [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Output: Task breakdown + dependencies + parallelization [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] PHASE 4: PLAYBOOK/SKILL ROUTING [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Action: Match tasks to playbooks/skills from catalog [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Output: Routing decisions for each task [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] PHASE 5: EXECUTION [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Tools: Skill() -> Task() -> TodoWrite() [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Pattern: Skills define SOP, Task spawns agents, TodoWrite tracks [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Golden Rule: 1 MESSAGE = ALL PARALLEL OPERATIONS [ground:given] [conf:1.0] [state:confirmed]

[warn|emphatic] CRITICAL CHECKS BEFORE EXECUTION: [ground:system-policy] [conf:1.0] [state:confirmed]

[assert|neutral] 1. DOMAIN EXPERTISE CHECK [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] Location: .claude/expertise/{domain}.yaml [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] If EXISTS: Load and validate BEFORE Phase 3 [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] If MISSING: Agent discovers and creates during execution [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] 2. AGENT REGISTRY ENFORCEMENT [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] Registry: claude-code-plugins/context-cascade/agents/ [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Count: 206 agents in 10 categories [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Categories: delivery, foundry, operations, orchestration, [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] platforms, quality, research, security, [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] specialists, tooling [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] Fallbacks: coder, researcher, tester, reviewer [ground:given] [conf:1.0] [state:confirmed]
[direct|emphatic] NEVER use generic/made-up agent types [ground:system-policy] [conf:1.0] [state:confirmed]

[assert|neutral] 3. SOP COMPLIANCE PATTERN [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Skill() -> Define how to accomplish task [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] v [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Task() -> Spawn registry agents to execute [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] | [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] v [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] TodoWrite() -> Track progress with 5-10 todos [ground:witnessed] [conf:0.90] [state:confirmed]

[assert|neutral] 4. PARALLEL EXECUTION RULE [ground:witnessed] [conf:0.90] [state:confirmed]
[define|neutral] WRONG: Spawn agent 1, wait, spawn agent 2 [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] RIGHT: Single message with ALL Task() calls [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] STATE TRACKING ACTIVE: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] All skill invocations logged [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] All agent spawns tracked [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Violations detected and recorded [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Compliance checked at each step [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] DO NOT skip phases. DO NOT use generic agents. DO NOT forget TodoWrite. [ground:witnessed] [conf:0.90] [state:confirmed]

================================================================

/*----------------------------------------------------------------------------*/
/* S2 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $USER_MESSAGE [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $USER_MESSAGE [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S4 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $MESSAGE_TEXT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[assert|neutral] $MESSAGE_TEXT [ground:witnessed] [conf:0.90] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>USER_PROMPT_SUBMIT_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
