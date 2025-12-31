/*============================================================================*/
/* PRE_TASK_SPAWN :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Hook script                                  */
/* HOOK TYPE: General                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "pre-task-spawn",
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
[warn|emphatic] !! TASK (AGENT SPAWN) DETECTED !! [ground:system-policy] [conf:1.0] [state:confirmed]
============================================================

[assert|neutral] You are about to spawn an agent via Task(). [ground:witnessed] [conf:0.90] [state:confirmed]

[warn|emphatic] CRITICAL: Agent type MUST be from registry! [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] AGENT REGISTRY: claude-code-plugins/context-cascade/agents/ [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] VALID CATEGORIES (206 agents): [ground:given] [conf:1.0] [state:confirmed]

[assert|neutral] 1. DELIVERY (18 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] coder, backend-dev, frontend-dev, fullstack-dev [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] mobile-dev, devops-engineer, sre, release-engineer [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] api-developer, database-dev, integration-dev, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 2. RESEARCH (11 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] researcher, analyst, data-scientist, ml-engineer [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] experiment-designer, paper-reader, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 3. QUALITY (18 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] tester, qa-engineer, security-tester, load-tester [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] reviewer, code-analyzer, auditor, compliance-checker [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] theater-detection-audit, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 4. ORCHESTRATION (21 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] hierarchical-coordinator, byzantine-coordinator [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] workflow-orchestrator, task-router, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 5. FOUNDRY (15 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] agent-creator, skill-creator, prompt-engineer [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] template-generator, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 6. OPERATIONS (12 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] cicd-engineer, monitoring-engineer, incident-responder [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] backup-manager, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 7. PLATFORMS (8 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] platform-engineer, cloud-architect, kubernetes-expert [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] terraform-expert, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 8. SECURITY (9 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] security-engineer, penetration-tester, crypto-expert [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] compliance-auditor, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 9. SPECIALISTS (tech-specific, 50+ agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] python-expert, javascript-expert, rust-expert [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] react-expert, vue-expert, etc. [ground:given] [conf:0.95] [state:confirmed]

[assert|neutral] 10. TOOLING (14 agents) [ground:witnessed] [conf:0.90] [state:confirmed]
  [assert|neutral] build-engineer, package-manager, dependency-analyzer [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] linter-configurator, etc. [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] FALLBACK AGENTS (if unsure): [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] coder (general coding) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] researcher (research/analysis) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] tester (testing) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] reviewer (code review) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] DOMAIN EXPERTISE CHECK: [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Before spawning agents, check if domain expertise exists: [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] Location: .claude/expertise/{domain}.yaml [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] If EXISTS: [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] 1. Run: /expertise-validate {domain} [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] 2. Load patterns and file locations [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] 3. Spawn agents with expertise context [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] If NOT EXISTS: [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] Agent will discover and create expertise during execution [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] AFTER SPAWNING: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Call TodoWrite() with 5-10 todos [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark todos in_progress when starting [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Mark completed immediately when done [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PARALLEL SPAWN RULE: [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] Spawn ALL independent agents in ONE message [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Do NOT spawn sequentially [ground:witnessed] [conf:0.90] [state:confirmed]

[define|neutral] LIMITATION WARNING: [ground:given] [conf:1.0] [state:confirmed]
[assert|neutral] This hook CANNOT validate your agent type (hook constraint) [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Validation happens AFTER spawn via transcript parsing [ground:witnessed] [conf:0.90] [state:confirmed]
[assert|neutral] Please ensure agent type is from registry above [ground:witnessed] [conf:0.90] [state:confirmed]

============================================================

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>PRE_TASK_SPAWN_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
