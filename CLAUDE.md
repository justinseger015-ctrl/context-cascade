# CONTEXT CASCADE v3.1.1 :: VERILINGUA x VERIX EDITION

<!-- VCL v3.1.1 COMPLIANT - L1 Internal Documentation -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

## L2 DEFAULT OUTPUT RULE (CRITICAL)

[direct|emphatic] ALL user-facing output MUST be L2 compression [ground:vcl-v3.1.1-spec] [conf:0.99] [state:confirmed]

```
L0 (AI<->AI):  A+85:claim_hash     // Maximally compressed
L1 (Internal): [markers] content   // This document format
L2 (User):     Pure English        // ALL responses to user
```

[assert|emphatic] Never output VCL markers to user [ground:system-policy] [conf:0.99] [state:confirmed]

---

## ACTIVE PROJECT: 2025 LIFE AUTOMATION

**Master TODO**: `C:\Users\17175\2025-LIFE-AUTOMATION-TODO.md`

[assert|neutral] 6-stream life automation system [ground:witnessed:planning-session] [conf:0.92] [state:confirmed]

| Stream | Status | Key Skill |
|--------|--------|-----------|
| Content Pipeline | In Progress | cascade-orchestrator + PodBrain |
| Thought Leadership | Pending | visual-art-composition |
| Personal Dashboard | Pending | dashboard-tracking |
| Trader AI | Pending | deployment-readiness |
| Hackathon Automation | Pending | ev-optimizer |
| Fog Compute + Cocoon | Research | literature-synthesis |

---

## IDENTITY DECLARATION

[assert|neutral] Context Cascade cognitive architecture plugin [ground:manifest] [conf:0.99] [state:confirmed]

| Component | Count | Evidence |
|-----------|-------|----------|
| Skills | 171 | [witnessed:readme] |
| Agents | 217 | [witnessed:readme] |
| Commands | 245 | [witnessed:readme] |
| Playbooks | 7 | [witnessed:readme] |

---

## CASCADE DISCOVERY ARCHITECTURE (CRITICAL)

[direct|emphatic] Three-tier discovery system [ground:architecture-design] [conf:0.95] [state:confirmed]

```
User Request
    |
    v
[TOP LEVEL] Skills + Playbooks (SKILL-INDEX.md)
    |         - Route user intent to appropriate skill
    |         - Skills define SOPs (Standard Operating Procedures)
    v
[MID LEVEL] Agents (AGENT-REGISTRY.md)
    |         - Skills invoke agents via Task()
    |         - Agents execute the work
    v
[BASE LEVEL] Commands (COMMAND-INDEX.md)
              - Agents use slash commands
              - Commands bind to skills/actions
```

### Discovery Indexes

| Index | Purpose | Location |
|-------|---------|----------|
| SKILL-INDEX.md | Top-level routing | `discovery/SKILL-INDEX.md` |
| AGENT-REGISTRY.md | Skill->Agent lookup | `discovery/AGENT-REGISTRY.md` |
| COMMAND-INDEX.md | Agent->Command lookup | `discovery/COMMAND-INDEX.md` |
| skill-index.json | Auto-routing data | `scripts/skill-index/skill-index.json` |
| registry.json | Full agent registry | `agents/foundry/registry/registry.json` |

### Slash Commands (Registered)

[assert|neutral] 708 components registered in ~/.claude/commands/ [ground:witnessed:registration] [conf:0.95] [state:confirmed]

```
~/.claude/commands/
  *.md           (258 commands)
  skills/*.md    (233 skills)
  agents/*.md    (217 agents)
```

### Auto-Routing Hook

The `skill-router-hook.sh` (UserPromptSubmit) automatically:
1. Parses user intent from message
2. Queries skill-index.json for matches
3. Returns skill suggestions with confidence scores

---

## 5-PHASE WORKFLOW (EVIDENTIAL CHAIN)

[direct|emphatic] Execute on EVERY non-trivial request [ground:system-policy] [conf:0.99] [state:confirmed]

### Phase 1: Intent Analysis
```
Skill("intent-analyzer")
Output: { understood_intent, constraints, confidence, evidence_chain }
```

### Phase 2: Prompt Optimization
```
Skill("prompt-architect")
Output: { optimized_request, added_context, success_criteria }
```

### Phase 3: Strategic Planning
```
Skill("research-driven-planning") OR Skill("planner")
Output: { tasks: [...], execution_order, dependencies }
```

### Phase 4: Playbook Routing
```
Route each task to playbook based on:
- Task type [witnessed:phase-3-output]
- Domain [inferred:keywords]
- Complexity [inferred:scope-analysis]
```

### Phase 5: Execution
```
// Golden Rule: 1 MESSAGE = ALL PARALLEL OPERATIONS
[Single Message]:
  Task("Agent 1", "...", "agent-type-from-registry")
  Task("Agent 2", "...", "agent-type-from-registry")
  TodoWrite({ todos: [...] })
```

---

## AGENT REGISTRY

[assert|neutral] 211 agents across 10 categories [ground:witnessed:registry-count] [conf:0.99] [state:confirmed]

```
Category        Count   Evidence
delivery        18      [witnessed:delivery/*.md]
quality         18      [witnessed:quality/*.md]
research        11      [witnessed:research/*.md]
orchestration   21      [witnessed:orchestration/*.md]
security        15      [witnessed:security/*.md]
platforms       12      [witnessed:platforms/*.md]
specialists     45      [witnessed:specialists/*.md]
tooling         24      [witnessed:tooling/*.md]
foundry         18      [witnessed:foundry/*.md]
operations      29      [witnessed:operations/*.md]
```

[direct|emphatic] NEVER use agents not in registry [ground:system-policy] [conf:0.99] [state:confirmed]

---

## SKILL INVOCATION PATTERN

[assert|neutral] Skills define SOPs, Tasks execute them [ground:architecture-design] [conf:0.95] [state:confirmed]

### Skill() Tool Syntax

```javascript
// Invoke a skill by name using the Skill tool
Skill("skill-name")           // Basic invocation
Skill("skill-name", "args")   // With arguments

// Examples:
Skill("analyzer")                                    // Analyze user intent
Skill("architect")                                   // System design mode
Skill("code")                                        // Code implementation
Skill("debug")                                       // Debug mode
Skill("build-feature")                               // Feature development
Skill("fix-bug")                                     // Bug fixing workflow
Skill("e2e-test")                                    // End-to-end testing
Skill("documenter")                                  // Documentation generation
Skill("improve")                                     // Code improvement
Skill("mcp")                                         // MCP server operations
Skill("devops")                                      // DevOps workflows
Skill("deployment")                                  // Deployment workflows
Skill("development")                                 // Development workflows
Skill("reflect")                                     // Session reflection & learning
```

### Task() Tool Syntax (for Agents)

```javascript
// Spawn an agent using the Task tool
Task("description", "prompt", "subagent_type")

// Parameters:
// - description: Short 3-5 word summary of what agent does
// - prompt: Detailed instructions for the agent
// - subagent_type: Agent type from registry (see AGENT INDEX below)

// Examples:
Task("Fix auth bug", "Analyze and fix the authentication issue in auth.js", "bug-fixer")
Task("Review security", "Check for vulnerabilities in the API endpoints", "security-auditor")
Task("Write tests", "Create comprehensive unit tests for the UserService", "tester")
Task("Research API", "Find best practices for REST API pagination", "researcher")

// Parallel execution (single message, multiple Task calls):
Task("Review security", "Check vulnerabilities", "security-auditor")
Task("Review quality", "Check code patterns", "code-reviewer")
Task("Run tests", "Execute test suite", "test-runner")
```

### Pattern Flow

```
User Request
    |
    v
Skill("skill-name")           // Load the SOP (Standard Operating Procedure)
    |
    v
Task("desc", "prompt", "type") // Spawn agent(s) to execute
    |
    v
TodoWrite({ todos })          // Track progress
```

**Golden Rule:** 1 MESSAGE = ALL PARALLEL OPERATIONS

---

## SKILL INDEX (171 Skills)

[assert|neutral] Complete skill catalog by category [ground:witnessed:readme] [conf:0.95] [state:confirmed]

### Core Skills (User-Invocable via /command)

| # | Skill Name | Purpose | Invocation |
|---|------------|---------|------------|
| 1 | `analyzer` | Analyze user intent and request scope | `Skill("analyzer")` |
| 2 | `architect` | System design and architecture planning | `Skill("architect")` |
| 3 | `auto-agent` | Autonomous agent execution | `Skill("auto-agent")` |
| 4 | `build-feature` | Complete feature development workflow | `Skill("build-feature")` |
| 5 | `code` | Code implementation mode | `Skill("code")` |
| 6 | `debug` | Debugging and troubleshooting | `Skill("debug")` |
| 7 | `deployment` | Deployment workflows | `Skill("deployment")` |
| 8 | `development` | Development workflows | `Skill("development")` |
| 9 | `devops` | DevOps and infrastructure | `Skill("devops")` |
| 10 | `documenter` | Documentation generation | `Skill("documenter")` |
| 11 | `e2e-test` | End-to-end testing | `Skill("e2e-test")` |
| 12 | `fix-bug` | Bug fixing workflow | `Skill("fix-bug")` |
| 13 | `improve` | Code improvement and refactoring | `Skill("improve")` |
| 14 | `mcp` | MCP server operations | `Skill("mcp")` |
| 15 | `reflect` | Session reflection & learning extraction | `Skill("reflect")` |

### Delivery Skills (18+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 15 | `feature-dev-complete` | 12-stage feature lifecycle |
| 16 | `smart-bug-fix` | Systematic debugging workflow |
| 17 | `pair-programming` | Collaborative coding |
| 18 | `debugging-assistant` | Interactive debugging |
| 19 | `i18n-automation` | Internationalization |
| 20 | `sop-api-development` | API development workflow |
| 21 | `testing-framework` | Comprehensive testing |

### SPARC Methodology Skills (20+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 22 | `delivery-sparc-ask` | SPARC questioning mode |
| 23 | `delivery-sparc-api-designer` | API design with SPARC |
| 24 | `delivery-sparc-backend-specialist` | Backend with SPARC |
| 25 | `delivery-sparc-database-architect` | DB design with SPARC |
| 26 | `delivery-sparc-designer` | UI/UX design with SPARC |
| 27 | `delivery-sparc-docs-writer` | Documentation with SPARC |
| 28 | `delivery-sparc-frontend-specialist` | Frontend with SPARC |
| 29 | `delivery-sparc-integration` | Integration with SPARC |
| 30 | `delivery-sparc-innovator` | Innovation with SPARC |
| 31 | `delivery-sparc-memory-manager` | Memory management |
| 32 | `delivery-sparc-mobile-specialist` | Mobile dev with SPARC |
| 33 | `delivery-sparc-security-review` | Security review |
| 34 | `delivery-sparc-spec-pseudocode` | Spec to pseudocode |
| 35 | `delivery-sparc-supabase-admin` | Supabase administration |
| 36 | `delivery-sparc-swarm-coordinator` | Swarm coordination |
| 37 | `delivery-sparc-tutorial` | Tutorial creation |
| 38 | `delivery-sparc-workflow-manager` | Workflow management |
| 39 | `delivery-sparc-batch-executor` | Batch execution |
| 40 | `delivery-sparc-refinement-optimization-mode` | Optimization mode |
| 41 | `delivery-sparc-post-deployment-monitoring-mode` | Post-deploy monitoring |

### Quality Skills (22+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 42 | `code-review-assistant` | Multi-agent code review |
| 43 | `functionality-audit` | Verify code works |
| 44 | `theater-detection` | Detect fake/placeholder code |
| 45 | `style-audit` | Code style checking |
| 46 | `verification-quality` | Quality verification |
| 47 | `github-code-review` | GitHub PR review |
| 48 | `quick-quality-check` | Fast parallel checks |

### Research Skills (21+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 49 | `deep-research-orchestrator` | 9-pipeline research |
| 50 | `literature-synthesis` | PRISMA-compliant review |
| 51 | `baseline-replication` | Statistical validation |
| 52 | `method-development` | Novel algorithm design |
| 53 | `interactive-planner` | Requirement gathering |

### Orchestration Skills (23+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 54 | `cascade-orchestrator` | Multi-skill pipelines |
| 55 | `swarm-orchestration` | Complex swarm workflows |
| 56 | `hive-mind` | Collective intelligence |
| 57 | `stream-chain` | Agent pipeline chaining |
| 58 | `slash-command-encoder` | Create slash commands |
| 59 | `web-cli-teleport` | Web-to-CLI bridge |
| 60 | `flow-nexus-swarm` | Cloud swarm deployment |
| 61 | `hooks-automation` | Workflow automation |
| 62 | `workflow-automation` | GitHub Actions automation |
| 63 | `sparc-workflow` | SPARC methodology workflow |
| 64 | `swarm-advanced` | Advanced swarm patterns |

### Foundry Skills (22+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 65 | `skill-forge` | Create new skills |
| 66 | `agent-creator` | Create new agents |
| 67 | `prompt-architect` | Optimize prompts |
| 68 | `hook-creator` | Create Claude hooks |
| 69 | `skill-builder` | Build skill templates |
| 70 | `skill-gap-analyzer` | Analyze missing skills |
| 71 | `token-budget-advisor` | Token optimization |
| 72 | `prompt-optimization-analyzer` | Prompt analysis |
| 73 | `agentdb-vector-search` | Semantic search |
| 74 | `agentdb-memory` | Persistent memory |
| 75 | `agentdb-optimization` | Vector optimization |
| 76 | `agentdb-learning` | RL agent training |
| 77 | `agentdb-advanced` | Advanced DB features |
| 78 | `reasoningbank-agentdb` | Adaptive learning |
| 79 | `expertise-create` | Create expertise modules |

### Operations Skills (23+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 80 | `production-readiness` | Deployment validation |
| 81 | `cicd-intelligent-recovery` | CI/CD with recovery |
| 82 | `cloud-platforms` | Cloud deployment |
| 83 | `performance-analysis` | Performance analysis |
| 84 | `performance-profiler` | Performance profiling |
| 85 | `github-project-management` | GitHub projects |
| 86 | `github-multi-repo` | Multi-repo management |
| 87 | `github-release-management` | Release management |

### Workflow Skills (15+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 88 | `delivery-workflows-docker-build` | Docker build workflow |
| 89 | `delivery-workflows-docker-deploy` | Docker deployment |
| 90 | `delivery-workflows-github-release` | GitHub release |
| 91 | `delivery-workflows-hotfix` | Hotfix workflow |
| 92 | `delivery-workflows-k8s-deploy` | Kubernetes deployment |
| 93 | `delivery-workflows-research` | Research workflow |
| 94 | `delivery-workflows-workflow-cicd` | CI/CD workflow |
| 95 | `delivery-workflows-workflow-create` | Create workflows |
| 96 | `delivery-workflows-workflow-deployment` | Deployment workflow |
| 97 | `delivery-workflows-workflow-execute` | Execute workflows |
| 98 | `delivery-workflows-workflow-export` | Export workflows |
| 99 | `delivery-workflows-workflow-rollback` | Rollback workflow |
| 100 | `delivery-workflow-commands-create-cascade` | Create cascade |
| 101 | `delivery-workflow-commands-create-micro-skill` | Create micro-skill |

### Training Skills (5)

| # | Skill Name | Purpose |
|---|------------|---------|
| 102 | `delivery-training-model-update` | Model updates |
| 103 | `delivery-training-neural-patterns` | Neural patterns |
| 104 | `delivery-training-neural-train` | Neural training |
| 105 | `delivery-training-pattern-learn` | Pattern learning |
| 106 | `delivery-training-specialization` | Specialization |

### Security Skills (13+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 107 | `network-security-setup` | Network security |
| 108 | `sandbox-configurator` | Sandbox security |
| 109 | `security-analyzer` | Security analysis |
| 110 | `reverse-engineering-deep` | Deep RE analysis |
| 111 | `compliance` | Security compliance |
| 112 | `flow-nexus-neural` | Neural network security |

### Platform Skills (18+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 113 | `ml-expert` | ML/AI expertise |
| 114 | `ml-training-debugger` | Debug ML training |
| 115 | `flow-nexus-platform` | Flow orchestration |
| 116 | `agentdb-advanced` | Agent database |
| 117 | `machine-learning` | ML pipelines |

### Tooling Skills (17+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 118 | `intent-analyzer` | Analyze user intent |
| 119 | `dependency-mapper` | Map dependencies |
| 120 | `doc-generator` | Generate documentation |
| 121 | `pptx-generation` | Create presentations |
| 122 | `reasoningbank-intelligence` | Optimize agent learning |

### Essential Commands (4)

| # | Skill Name | Purpose |
|---|------------|---------|
| 123 | `delivery-essential-commands-deploy-check` | Deployment validation |
| 124 | `delivery-essential-commands-integration-test` | Integration testing |
| 125 | `delivery-essential-commands-load-test` | Load testing |
| 126 | `delivery-essential-commands-regression-test` | Regression testing |

### Foundry Agent Skills (10+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 127 | `foundry-agents-agent-capabilities` | Agent capabilities |
| 128 | `foundry-agents-agent-coordination` | Agent coordination |
| 129 | `foundry-agents-agent-spawning` | Spawn agents |
| 130 | `foundry-agents-agent-types` | Agent type definitions |
| 131 | `foundry-agent-commands-agent-benchmark` | Agent benchmarking |
| 132 | `foundry-agent-commands-agent-clone` | Clone agents |
| 133 | `foundry-agent-commands-agent-health-check` | Health checks |
| 134 | `foundry-agent-commands-agent-rca` | Root cause analysis |
| 135 | `foundry-agent-commands-agent-retire` | Retire agents |
| 136 | `foundry-expertise-expertise-challenge` | Challenge expertise |
| 137 | `foundry-expertise-expertise-validate` | Validate expertise |

### Operations Automation (20+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 138 | `operations-automation-self-healing` | Self-healing systems |
| 139 | `operations-automation-session-memory` | Session memory |
| 140 | `operations-automation-smart-agents` | Smart agent automation |
| 141 | `operations-automation-workflow-select` | Workflow selection |
| 142 | `operations-deployment-cloudflare-deploy` | Cloudflare deployment |
| 143 | `operations-deployment-vercel-deploy` | Vercel deployment |
| 144 | `operations-github-ansible-deploy` | Ansible deployment |
| 145 | `operations-github-aws-deploy` | AWS deployment |
| 146 | `operations-github-code-review` | GitHub code review |
| 147 | `operations-github-docker-compose` | Docker Compose |
| 148 | `operations-github-github-actions` | GitHub Actions |
| 149 | `operations-github-github-pages` | GitHub Pages |
| 150 | `operations-github-issue-triage` | Issue triage |
| 151 | `operations-github-jira-sync` | JIRA sync |
| 152 | `operations-github-pr-enhance` | PR enhancement |
| 153 | `operations-github-repo-analyze` | Repo analysis |
| 154 | `operations-github-slack-notify` | Slack notifications |
| 155 | `operations-github-terraform-apply` | Terraform apply |

### Hooks Automation (10+)

| # | Skill Name | Purpose |
|---|------------|---------|
| 156 | `operations-hooks-automation-cron-job` | Cron job automation |
| 157 | `operations-hooks-automation-on-commit` | On-commit hooks |
| 158 | `operations-hooks-automation-on-deploy` | On-deploy hooks |
| 159 | `operations-hooks-automation-on-error` | On-error hooks |
| 160 | `operations-hooks-automation-on-pr` | On-PR hooks |
| 161 | `operations-hooks-automation-on-push` | On-push hooks |
| 162 | `operations-hooks-automation-on-success` | On-success hooks |
| 163 | `operations-hooks-automation-retry-failed` | Retry failed |
| 164 | `operations-hooks-automation-schedule-task` | Schedule tasks |
| 165 | `operations-hooks-post-edit` | Post-edit hooks |
| 166 | `operations-hooks-post-task` | Post-task hooks |
| 167 | `operations-hooks-pre-edit` | Pre-edit hooks |
| 168 | `operations-hooks-pre-task` | Pre-task hooks |
| 169 | `operations-hooks-session-end` | Session end hooks |
| 170 | `operations-hooks-setup` | Hook setup |

### Memory Operations (4)

| # | Skill Name | Purpose |
|---|------------|---------|
| 171 | `operations-memory-memory-clear` | Clear memory |
| 172 | `operations-memory-memory-export` | Export memory |
| 173 | `operations-memory-memory-merge` | Merge memory |
| 174 | `operations-memory-memory-persist` | Persist memory |

---

## AGENT INDEX (217 Agents)

[assert|neutral] Complete agent catalog by category [ground:witnessed:agent-registry] [conf:0.95] [state:confirmed]

### Delivery Agents (18)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 1 | `feature-builder` | End-to-end feature building | `Task("Build feature", "...", "feature-builder")` |
| 2 | `bug-fixer` | Debug and fix issues | `Task("Fix bug", "...", "bug-fixer")` |
| 3 | `coder` | Write production code | `Task("Write code", "...", "coder")` |
| 4 | `planner` | Create implementation plans | `Task("Plan impl", "...", "planner")` |
| 5 | `tester` | Write and run tests | `Task("Write tests", "...", "tester")` |
| 6 | `reviewer` | Review code quality | `Task("Review code", "...", "reviewer")` |
| 7 | `deployer` | Handle deployment | `Task("Deploy app", "...", "deployer")` |
| 8 | `debugger` | Advanced debugging | `Task("Debug issue", "...", "debugger")` |
| 9 | `refactorer` | Code refactoring | `Task("Refactor", "...", "refactorer")` |

### Quality Agents (18)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 10 | `code-reviewer` | Deep code review | `Task("Review", "...", "code-reviewer")` |
| 11 | `security-auditor` | Security analysis | `Task("Audit security", "...", "security-auditor")` |
| 12 | `functionality-auditor` | Verify code works | `Task("Audit func", "...", "functionality-auditor")` |
| 13 | `theater-detector` | Detect fake code | `Task("Detect theater", "...", "theater-detector")` |
| 14 | `linter` | Code style checks | `Task("Lint code", "...", "linter")` |
| 15 | `test-runner` | Execute tests | `Task("Run tests", "...", "test-runner")` |
| 16 | `e2e-tester` | E2E testing | `Task("E2E test", "...", "e2e-tester")` |

### Research Agents (11)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 17 | `researcher` | Deep research | `Task("Research", "...", "researcher")` |
| 18 | `literature-reviewer` | Academic review | `Task("Review lit", "...", "literature-reviewer")` |
| 19 | `synthesizer` | Synthesize findings | `Task("Synthesize", "...", "synthesizer")` |
| 20 | `statistician` | Statistical analysis | `Task("Analyze stats", "...", "statistician")` |
| 21 | `innovator` | Novel solutions | `Task("Innovate", "...", "innovator")` |

### Orchestration Agents (21)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 22 | `coordinator` | Multi-agent coordination | `Task("Coordinate", "...", "coordinator")` |
| 23 | `swarm-master` | Swarm orchestration | `Task("Orchestrate swarm", "...", "swarm-master")` |
| 24 | `queue-manager` | Task queue management | `Task("Manage queue", "...", "queue-manager")` |
| 25 | `parallel-executor` | Parallel execution | `Task("Execute parallel", "...", "parallel-executor")` |

### Security Agents (15)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 26 | `security-engineer` | Security implementation | `Task("Secure", "...", "security-engineer")` |
| 27 | `penetration-tester` | Security testing | `Task("Pentest", "...", "penetration-tester")` |
| 28 | `compliance-auditor` | Compliance checks | `Task("Audit compliance", "...", "compliance-auditor")` |
| 29 | `reverse-engineer` | Binary analysis | `Task("Reverse engineer", "...", "reverse-engineer")` |

### Platform Agents (12)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 30 | `db-architect` | Database design | `Task("Design DB", "...", "db-architect")` |
| 31 | `ml-engineer` | ML implementation | `Task("Build ML", "...", "ml-engineer")` |
| 32 | `flow-manager` | Flow orchestration | `Task("Manage flow", "...", "flow-manager")` |

### Specialist Agents (45)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 33 | `python-expert` | Python code | `Task("Python task", "...", "python-expert")` |
| 34 | `typescript-expert` | TypeScript code | `Task("TS task", "...", "typescript-expert")` |
| 35 | `rust-expert` | Rust code | `Task("Rust task", "...", "rust-expert")` |
| 36 | `go-expert` | Go code | `Task("Go task", "...", "go-expert")` |
| 37 | `ml-specialist` | ML/AI expertise | `Task("ML task", "...", "ml-specialist")` |
| 38 | `frontend-specialist` | Frontend dev | `Task("Frontend task", "...", "frontend-specialist")` |
| 39 | `backend-specialist` | Backend dev | `Task("Backend task", "...", "backend-specialist")` |
| 40 | `devops-specialist` | DevOps | `Task("DevOps task", "...", "devops-specialist")` |
| 41 | `api-specialist` | API development | `Task("API task", "...", "api-specialist")` |
| 42 | `mobile-specialist` | Mobile dev | `Task("Mobile task", "...", "mobile-specialist")` |

### Tooling Agents (24)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 43 | `documentation-writer` | Write docs | `Task("Write docs", "...", "documentation-writer")` |
| 44 | `api-documenter` | API docs | `Task("Doc API", "...", "api-documenter")` |
| 45 | `pptx-generator` | Presentations | `Task("Create pptx", "...", "pptx-generator")` |
| 46 | `diagram-generator` | Architecture diagrams | `Task("Create diagram", "...", "diagram-generator")` |
| 47 | `github-specialist` | GitHub operations | `Task("GitHub op", "...", "github-specialist")` |
| 48 | `intent-parser` | Parse user intent | `Task("Parse intent", "...", "intent-parser")` |

### Foundry Agents (18)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 49 | `skill-creator` | Create skills | `Task("Create skill", "...", "skill-creator")` |
| 50 | `agent-architect` | Design agents | `Task("Design agent", "...", "agent-architect")` |
| 51 | `prompt-engineer` | Optimize prompts | `Task("Optimize prompt", "...", "prompt-engineer")` |
| 52 | `hook-developer` | Create hooks | `Task("Create hook", "...", "hook-developer")` |
| 53 | `validator` | Validate artifacts | `Task("Validate", "...", "validator")` |

### Operations Agents (29)

| # | Agent Type | Purpose | Task Invocation |
|---|------------|---------|-----------------|
| 54 | `cicd-engineer` | CI/CD pipelines | `Task("Setup CI", "...", "cicd-engineer")` |
| 55 | `aws-specialist` | AWS operations | `Task("AWS op", "...", "aws-specialist")` |
| 56 | `gcp-specialist` | GCP operations | `Task("GCP op", "...", "gcp-specialist")` |
| 57 | `azure-specialist` | Azure operations | `Task("Azure op", "...", "azure-specialist")` |
| 58 | `kubernetes-operator` | K8s management | `Task("K8s op", "...", "kubernetes-operator")` |
| 59 | `monitoring-agent` | System monitoring | `Task("Monitor", "...", "monitoring-agent")` |
| 60 | `docker-specialist` | Docker operations | `Task("Docker op", "...", "docker-specialist")` |

---

## VERILINGUA COGNITIVE FRAMES

[assert|neutral] Seven frames force cognitive distinctions [ground:linguistic-research] [conf:0.95] [state:confirmed]

```
FRAME           SOURCE              COGNITIVE FORCE
evidential      Turkish -mis/-di    "How do you know?"
aspectual       Russian aspect      "Complete or ongoing?"
morphological   Arabic roots        "What are the components?"
compositional   German compounds    "Build from primitives"
honorific       Japanese keigo      "Who is the audience?"
classifier      Chinese classifiers "What type/count?"
spatial         Guugu Yimithirr     "Absolute position?"
```

### Evidence Markers (MANDATORY for L1)

```
[witnessed]     - Direct observation (read code, ran test)
[reported:src]  - Secondhand from source (docs, user, API)
[inferred]      - Deduced from evidence (reasoning chain)
[assumed:conf]  - Assumption with confidence level
```

---

## VERIX EPISTEMIC NOTATION

[assert|neutral] Statement encodes epistemic stance [ground:verix-spec] [conf:0.98] [state:confirmed]

### Grammar
```
CLAIM := [illocution|affect] content [ground:source] [conf:X.XX] [state:status]
```

### Confidence Ceilings by EVD Type
```
definition: 0.95    policy: 0.90      observation: 0.95
research: 0.85      report: 0.70      inference: 0.70
```

### Illocution Types
```
assert  - Factual claim     direct  - Instruction
query   - Question          commit  - Promise
express - Attitude
```

### States
```
provisional - May revise    confirmed - Verified
retracted   - Withdrawn
```

---

## NAMED MODES (MOO-OPTIMIZED)

[assert|neutral] Pareto-optimal configurations [ground:moo-output] [conf:0.92] [state:confirmed]

```
Mode      Accuracy  Efficiency  Primary Frames
audit     0.960     0.763       evidential, aspectual, morphological
speed     0.734     0.950       (minimal frames)
research  0.980     0.824       evidential, honorific, classifier
robust    0.960     0.769       evidential, aspectual, morphological
balanced  0.882     0.928       evidential, spatial
```

---

## MULTI-MODEL SUBAGENT INVOCATION (CRITICAL)

[direct|emphatic] Codex CLI and Gemini CLI are INSTALLED and READY [ground:witnessed:version-check] [conf:0.99] [state:confirmed]

**Installed CLIs**:
- Codex: v0.66.0 at `/c/Users/17175/AppData/Roaming/npm/codex`
- Gemini: v0.20.2 at `/c/Users/17175/AppData/Roaming/npm/gemini`

### MANDATORY Rules

1. [assert|emphatic] NEVER install or upgrade codex/gemini [ground:already-installed]
2. [assert|emphatic] ALWAYS use login shell: `bash -lc "<command>"` [ground:path-fix]
3. [assert|emphatic] RUN preflight before invoking [ground:verification]:
   ```bash
   bash -lc "command -v codex && codex --version"
   bash -lc "command -v gemini && gemini --version"
   ```
4. [assert|emphatic] If preflight FAILS, STOP and report - DO NOT install [ground:policy]
5. [assert|emphatic] Use PLAIN command names, NOT file paths [ground:portability]

### Invocation Patterns

**Codex (autonomous coding)**:
```bash
bash -lc "codex exec 'your task here'"                    # Basic
bash -lc "codex --full-auto exec 'your task here'"        # Autonomous
bash -lc "codex exec --json 'your task here'"             # JSON output
bash -lc "codex --yolo exec 'your task here'"             # Bypass approvals
```

**Gemini (research/megacontext)**:
```bash
bash -lc "gemini 'your query here'"                       # Basic
bash -lc "gemini --all-files 'analyze architecture'"      # 1M token context
bash -lc "gemini -o json 'your query here'"               # JSON output
```

**Preferred: Use delegate.sh wrapper**:
```bash
./scripts/multi-model/delegate.sh codex "Fix all tests" --full-auto
./scripts/multi-model/delegate.sh gemini "Map architecture" --all-files
```

### Model Strengths

| Task | Route To | Reason |
|------|----------|--------|
| Research (current info) | Gemini | Google Search grounding |
| Large codebase analysis | Gemini | 1M token context |
| Autonomous iteration | Codex | Full-auto/YOLO modes |
| Complex reasoning | Claude | Multi-step logic |
| Critical decisions | LLM Council | Multi-model consensus |

**Full Guide**: `docs/MULTI-MODEL-INVOCATION-GUIDE.md`

---

## ABSOLUTE RULES

[direct|emphatic] Non-negotiable policies [ground:system-policy] [conf:0.99] [state:confirmed]

1. [assert|emphatic] NO UNICODE in file content [ground:windows-compatibility]
2. [assert|emphatic] NEVER save to root folder [ground:organization-policy]
3. [assert|emphatic] BATCH operations in single message [ground:efficiency]
4. [assert|emphatic] ONLY registry agents [ground:quality-control]
5. [assert|emphatic] L2 OUTPUT for user responses [ground:vcl-v3.1.1-spec]
6. [assert|emphatic] EVIDENCE MARKERS on internal claims [ground:epistemic-hygiene]
7. [assert|emphatic] NEVER reinstall codex/gemini - use bash -lc [ground:path-fix]

---

## COGNITIVE ARCHITECTURE SELF-EVOLUTION

[assert|neutral] Four-loop self-improvement system [ground:architecture-design] [conf:0.92] [state:confirmed]

### Four-Loop Architecture

```
┌─────────────────────────────────────────────────────┐
│ Loop 1: Execution (Per-Request)                     │
│ - 5-phase workflow execution                        │
│ - Multi-agent task completion                       │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Loop 1.5: Session Reflection (Per-Session)          │
│ - Signal detection (corrections, approvals, rules) │
│ - Skill file updates (LEARNED PATTERNS section)    │
│ - Memory MCP storage for aggregation               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Loop 2: Quality Validation (Per-Session)            │
│ - Theater detection, functionality audits          │
│ - Security and performance validation              │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Loop 3: Meta-Optimization (Every 3 Days)            │
│ - Aggregate Loop 1.5 learnings from Memory MCP     │
│ - GlobalMOO 5D + PyMOO NSGA-II 14D optimization   │
│ - Cascade updates to entire system                 │
└─────────────────────────────────────────────────────┘
```

### Loop 1.5: Reflect Skill

[assert|neutral] Per-session micro-learning [ground:reflect-skill] [conf:0.85] [state:confirmed]

**Commands**:
- `/reflect` - Manual session reflection
- `/reflect-on` - Enable auto-reflection on session end
- `/reflect-off` - Disable auto-reflection
- `/reflect-status` - Check state and history

**Signal Detection**:
| Signal Type | Confidence | Action |
|-------------|------------|--------|
| Corrections | HIGH (0.90) | Requires approval |
| Explicit Rules | HIGH (0.90) | Requires approval |
| Approvals | MEDIUM (0.75) | Auto-apply if enabled |
| Observations | LOW (0.55) | Auto-apply if enabled |

**Output**: LEARNED PATTERNS section in skill files + Memory MCP storage

### Loop 3: Meta-Loop Cycle

```
Every 3 Days:
1. Query Memory MCP for Loop 1.5 learnings
2. Run GlobalMOO (5D exploration)
3. Run PyMOO NSGA-II (14D refinement)
4. Distill named modes (audit, speed, research, robust, balanced)
5. Apply to cascade (commands -> agents -> skills -> playbooks)
```

---

## VCL v3.1.1 SPECIFICATION

[assert|neutral] This document demonstrates v3.1.1 compliance [ground:self-reference] [conf:0.95] [state:confirmed]

### 7-Slot Cognitive Forcing
```
HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
```

### Immutable Safety Bounds
```
EVD >= 1 (cannot disable evidence)
ASP >= 1 (cannot disable aspect)
```

### Creolization Ready
```
Ready for multi-language expansion via creolization protocol
```

---

<promise>CONTEXT_CASCADE_VCL_V3.1.1_COMPLIANT</promise>
