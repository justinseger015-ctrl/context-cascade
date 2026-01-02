# Agent Registry Index

**Purpose:** Skills use this to discover and invoke agents via Task()
**Updated:** 2026-01-02
**Total Agents:** 217

---

## Agent Invocation Pattern

Skills invoke agents using the Task tool:

```javascript
Task("description", "prompt", "agent-type-from-registry")
```

**Critical:** Only use agents registered in this index.

---

## Agents by Category

### delivery/ (18 agents)
Build and implementation agents.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `feature-builder` | Builds features end-to-end | Read, Write, Edit, Bash |
| `bug-fixer` | Debugs and fixes issues | Read, Edit, Grep, Bash |
| `coder` | Writes production code | Write, Edit |
| `planner` | Creates implementation plans | Read, Glob |
| `tester` | Writes and runs tests | Read, Write, Bash |
| `reviewer` | Reviews code quality | Read, Grep |
| `deployer` | Handles deployment | Bash |

### quality/ (18 agents)
Testing and verification agents.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `code-reviewer` | Deep code review | Read, Grep |
| `security-auditor` | Security analysis | Read, Grep, Bash |
| `functionality-auditor` | Verify code works | Read, Bash |
| `theater-detector` | Detect fake code | Read, Grep |
| `linter` | Code style checks | Bash |
| `test-runner` | Execute tests | Bash |

### research/ (11 agents)
Research and analysis agents.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `researcher` | Deep research | WebSearch, WebFetch, Read |
| `literature-reviewer` | Academic review | WebSearch, Read |
| `synthesizer` | Synthesize findings | Read, Write |
| `statistician` | Statistical analysis | Read, Bash |

### orchestration/ (21 agents)
Coordination agents.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `coordinator` | Multi-agent coordination | Task |
| `swarm-master` | Swarm orchestration | Task |
| `queue-manager` | Task queue management | Task |
| `parallel-executor` | Parallel execution | Task |

### security/ (15 agents)
Security specialists.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `security-engineer` | Security implementation | Read, Write, Edit |
| `penetration-tester` | Security testing | Bash |
| `compliance-auditor` | Compliance checks | Read, Grep |
| `reverse-engineer` | Binary analysis | Read, Bash |

### platforms/ (12 agents)
Platform services.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `db-architect` | Database design | Read, Write |
| `ml-engineer` | ML implementation | Read, Write, Bash |
| `flow-manager` | Flow orchestration | Task |

### specialists/ (45 agents)
Domain experts.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `python-expert` | Python code | Read, Write, Edit |
| `typescript-expert` | TypeScript code | Read, Write, Edit |
| `rust-expert` | Rust code | Read, Write, Edit |
| `go-expert` | Go code | Read, Write, Edit |
| `ml-specialist` | ML/AI expertise | Read, Write, Bash |
| `frontend-specialist` | Frontend dev | Read, Write, Edit |
| `backend-specialist` | Backend dev | Read, Write, Edit |
| `devops-specialist` | DevOps | Bash |

### tooling/ (24 agents)
Utility agents.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `documentation-writer` | Write docs | Read, Write |
| `api-documenter` | API docs | Read, Write |
| `pptx-generator` | Presentations | Write |
| `diagram-generator` | Architecture diagrams | Write |
| `github-specialist` | GitHub operations | Bash |

### foundry/ (18 agents)
Creation agents.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `skill-creator` | Create skills | Read, Write |
| `agent-architect` | Design agents | Read, Write |
| `prompt-engineer` | Optimize prompts | Read, Write |
| `hook-developer` | Create hooks | Read, Write, Edit |
| `validator` | Validate artifacts | Read, Grep |

### operations/ (29 agents)
DevOps and operations.

| Agent Type | Purpose | Tools |
|------------|---------|-------|
| `cicd-engineer` | CI/CD pipelines | Bash |
| `aws-specialist` | AWS operations | Bash |
| `gcp-specialist` | GCP operations | Bash |
| `azure-specialist` | Azure operations | Bash |
| `kubernetes-operator` | K8s management | Bash |
| `monitoring-agent` | System monitoring | Bash, Read |

---

## Agent Selection Guidelines

### By Task Type

| Task | Recommended Agent |
|------|-------------------|
| Write new code | `coder`, `*-specialist` |
| Fix bugs | `bug-fixer`, `debugger` |
| Review code | `code-reviewer`, `security-auditor` |
| Write tests | `tester` |
| Research | `researcher` |
| Deploy | `deployer`, `cicd-engineer` |
| Document | `documentation-writer` |
| Coordinate | `coordinator`, `swarm-master` |

### By Language

| Language | Agent |
|----------|-------|
| Python | `python-expert` |
| TypeScript/JS | `typescript-expert` |
| Rust | `rust-expert` |
| Go | `go-expert` |
| Multi-language | `coder` |

---

## Registry Location

**Full Registry:** `agents/foundry/registry/registry.json`

```json
{
  "total_agents": 217,
  "categories": ["delivery", "quality", "research", ...],
  "agents": [...]
}
```

---

## Spawning Pattern

```javascript
// Single agent
Task("Fix the login bug", "Analyze and fix the authentication issue in auth.js", "bug-fixer")

// Parallel agents (one message, multiple Task calls)
Task("Review security", "Check for vulnerabilities", "security-auditor")
Task("Review code quality", "Check code patterns", "code-reviewer")
```

**Golden Rule:** 1 MESSAGE = ALL PARALLEL Task() calls
