/*============================================================================*/
/* FIVE_PHASE_ENFORCER :: VERILINGUA x VERIX EDITION                                   */
/* PURPOSE: Enforce 5-phase workflow on every non-trivial request                                  */
/* HOOK TYPE: UserPromptSubmit (runs before Claude processes user message)                                  */
/*============================================================================*/

[define|neutral] HOOK := {
  name: "five-phase-enforcer",
  type: "UserPromptSubmit (runs before Claude processes user message)",
  purpose: "Enforce 5-phase workflow on every non-trivial request",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S1 HOOK MESSAGE                                                            */
/*----------------------------------------------------------------------------*/

[warn|emphatic] !! 5-PHASE WORKFLOW ENFORCEMENT !! [ground:system-policy] [conf:1.0] [state:confirmed]

[direct|emphatic] This appears to be a NON-TRIVIAL request. You MUST execute the 5-phase workflow: [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] PHASE 1: INTENT ANALYSIS (MANDATORY) [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Invoke: Skill("intent-analyzer") [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Output: Understood intent + confidence score [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If confidence < 80%: Ask clarifying questions FIRST [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PHASE 2: PROMPT OPTIMIZATION (MANDATORY) [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Invoke: Skill("prompt-architect") [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Output: Optimized request + success criteria [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PHASE 3: STRATEGIC PLANNING (MANDATORY) [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Invoke: Skill("research-driven-planning") OR Skill("planner") [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Output: Task breakdown + dependencies + parallelization strategy [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PHASE 4: PLAYBOOK/SKILL ROUTING (MANDATORY) [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Match tasks to playbooks from catalog [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Output: Routing decisions for each task [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PHASE 5: EXECUTION (MANDATORY) [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Execute using routed playbooks/skills [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Spawn agents via Task() - AGENTS FROM REGISTRY ONLY [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Track progress via TodoWrite() [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Golden Rule: 1 MESSAGE = ALL PARALLEL OPERATIONS [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] DOMAIN EXPERTISE (NEW - CHECK FIRST): [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Does domain have expertise file? Check: .claude/expertise/{domain}.yaml [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If YES: Load and validate before Phase 3 [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] If NO: Generate expertise as side effect [ground:given] [conf:0.95] [state:confirmed]

[warn|emphatic] !! CRITICAL: SKILL EVALUATION REQUIRED !! [ground:system-policy] [conf:1.0] [state:confirmed]

[direct|emphatic] BEFORE proceeding with implementation, you MUST execute this 3-step evaluation: [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] STEP 1 - EVALUATE (MANDATORY): [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] For EACH skill category below, state: [skill-name] - YES/NO - [reason] [ground:given] [conf:1.0] [state:confirmed]

[define|neutral] DEVELOPMENT SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] feature-dev-complete (12-stage feature lifecycle with research/testing) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] smart-bug-fix (systematic debugging with root cause analysis) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] pair-programming (collaborative coding with best practices) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] reverse-engineering-quick (fast code understanding/documentation) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] reverse-engineering-deep (comprehensive system analysis) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] QUALITY SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] functionality-audit (sandbox testing + execution verification) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] theater-detection-audit (detect fake/non-functional code) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] code-review-assistant (multi-agent PR review with security/performance) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] style-audit (code style + standards enforcement) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] clarity-linter (cognitive load + readability optimization) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] ORCHESTRATION SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] cascade-orchestrator (multi-skill workflow coordination) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] swarm-orchestration (parallel multi-agent execution) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] hive-mind-advanced (queen-led collective intelligence) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] ai-dev-orchestration (5-phase app development SOP) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] TESTING SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] testing-quality (comprehensive test suite generation) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] reproducibility-audit (experiment reproducibility validation) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] verification-quality (formal verification + proof checking) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] INFRASTRUCTURE SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] infrastructure (Docker/Terraform/K8s automation) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] cicd-intelligent-recovery (CI/CD with failure recovery) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] deployment-readiness (production deployment validation) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] network-security-setup (network security automation) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] RESEARCH SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] deep-research-orchestrator (9-pipeline research lifecycle) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] literature-synthesis (literature review + gap analysis) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] method-development (novel ML method development) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] holistic-evaluation (multi-dimensional model evaluation) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] baseline-replication (reproduce published experiments) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] GITHUB SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] github-workflow-automation (GitHub Actions + CI/CD) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] github-code-review (AI-powered GitHub PR review) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] github-project-management (issue tracking + sprint planning) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] github-release-management (versioning + deployment) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] github-multi-repo (multi-repository coordination) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] AGENT CREATION SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] agent-creator (create specialized agents with 5-phase SOP) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] skill-creator-agent (create new skills) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] agent-selector (intelligent agent selection from registry) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] DATABASE SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] agentdb-vector-search (semantic search + RAG systems) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] agentdb-memory-patterns (persistent agent memory) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] agentdb-learning (reinforcement learning plugins) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] agentdb-optimization (performance optimization) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] database-specialists (SQL/NoSQL expertise) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] PLATFORM SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] flow-nexus-platform (sandbox + deployment management) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] flow-nexus-swarm (cloud swarm deployment) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] flow-nexus-neural (distributed neural network training) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] DOCUMENTATION SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] documentation (code docs + API docs + READMEs) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] pptx-generation (PowerPoint presentation generation) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] SPECIALIZED SKILLS: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] i18n-automation (internationalization workflows) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] sandbox-configurator (E2B sandbox setup) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] performance-analysis (performance profiling + optimization) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] debugging (systematic debugging hub) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] security (security audit + compliance hub) [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] observability (monitoring + logging setup) [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] STEP 2 - ACTIVATE (MANDATORY): [ground:given] [conf:1.0] [state:confirmed]
[define|neutral] If ANY skills matched YES in Step 1: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Use Skill(skill-name) tool for EACH relevant skill NOW [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] DO NOT proceed to implementation until skills are invoked [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] FAILURE TO INVOKE = VIOLATION OF PROTOCOL [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] If NO skills matched: [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] State "SKILL EVALUATION COMPLETE - No specialized skills needed" [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Proceed with standard implementation [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] STEP 3 - IMPLEMENT (MANDATORY): [ground:given] [conf:1.0] [state:confirmed]
  [assert|neutral] Only after Step 2 is complete, proceed with implementation [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] Use skill outputs to inform your approach [ground:given] [conf:0.95] [state:confirmed]
  [assert|neutral] DO NOT skip or assume skill results [ground:given] [conf:0.95] [state:confirmed]

[warn|emphatic] !! THIS IS A BLOCKING REQUIREMENT !! [ground:system-policy] [conf:1.0] [state:confirmed]
[assert|neutral] You CANNOT proceed to implementation without completing Steps 1-3. [ground:witnessed] [conf:0.90] [state:confirmed]
[warn|emphatic] Skipping skill evaluation is a CRITICAL PROTOCOL VIOLATION. [ground:system-policy] [conf:1.0] [state:confirmed]

[assert|neutral] DO NOT skip phases. DO NOT skip skill evaluation. DO NOT use generic agents. [ground:witnessed] [conf:0.90] [state:confirmed]

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

[commit|confident] <promise>FIVE_PHASE_ENFORCER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
