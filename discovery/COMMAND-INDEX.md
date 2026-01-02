# Command Index

**Purpose:** Agents use this to discover available slash commands
**Updated:** 2026-01-02
**Total Commands:** 245

---

## Command Structure

Commands are invoked as: `/command-name [args]`

All commands follow VCL v3.1.1 format with:
- YAML frontmatter
- Standard Operating Procedure
- Success criteria
- Error handling

---

## Commands by Category

### SPARC Commands (Core Development)

| Command | Purpose | Binding |
|---------|---------|---------|
| `/sparc` | Primary SPARC workflow | skill:sparc |
| `/code` | Write production code | skill:coder |
| `/debug` | Debug issues | skill:debugger |
| `/architect` | Design architecture | skill:architect |
| `/tdd` | Test-driven development | skill:tester |
| `/reviewer` | Code review | skill:reviewer |
| `/tester` | Write tests | skill:tester |
| `/researcher` | Research topics | skill:researcher |
| `/documenter` | Write documentation | skill:documenter |
| `/analyzer` | Analyze code | skill:analyzer |
| `/optimizer` | Optimize performance | skill:optimizer |
| `/devops` | DevOps operations | skill:devops |
| `/security-review` | Security audit | skill:security |
| `/mcp` | MCP server operations | skill:mcp |

### Essential Commands

| Command | Purpose |
|---------|---------|
| `/build-feature` | Build a new feature |
| `/fix-bug` | Fix a bug |
| `/review-pr` | Review pull request |
| `/quick-check` | Fast quality check |
| `/smoke-test` | Basic smoke testing |
| `/e2e-test` | End-to-end testing |
| `/integration-test` | Integration testing |
| `/load-test` | Load testing |

### Quality Commands

| Command | Purpose |
|---------|---------|
| `/quality-loop` | Full quality cycle |
| `/code-audit` | Deep code audit |
| `/security-audit` | Security audit |

### Workflow Commands

| Command | Purpose |
|---------|---------|
| `/development` | Development workflow |
| `/deployment` | Deployment workflow |
| `/testing` | Testing workflow |
| `/hotfix` | Hotfix workflow |

### Foundry Commands

| Command | Purpose |
|---------|---------|
| `/improve` | Run improvement cycle |
| `/expertise-create` | Create expertise |

### Operations Commands

| Command | Purpose |
|---------|---------|
| `/smart-spawn` | Smart agent spawning |
| `/auto-agent` | Automatic agent selection |
| `/docker-deploy` | Docker deployment |
| `/k8s-deploy` | Kubernetes deployment |
| `/vercel-deploy` | Vercel deployment |
| `/cloudflare-deploy` | Cloudflare deployment |

### Training Commands

| Command | Purpose |
|---------|---------|
| `/neural-train` | Neural network training |
| `/pattern-learn` | Pattern learning |
| `/model-update` | Model updates |

---

## Command Locations

### Registered Commands
All 245+ commands are registered in `~/.claude/commands/`:

```
~/.claude/commands/
  sparc.md
  code.md
  debug.md
  delivery-sparc-*.md
  delivery-essential-commands-*.md
  ...
  skills/
    skill-*.md
  agents/
    agent-*.md
```

### Source Commands
Original commands in plugin:

```
context-cascade/commands/
  delivery/
    sparc/
    essential-commands/
    workflows/
  quality/
  research/
  orchestration/
  foundry/
  operations/
  security/
  platforms/
  tooling/
```

---

## Command Binding

Commands can bind to skills:

```yaml
---
name: code
binding: skill:coder
---
```

When invoked, the command loads and activates the bound skill.

---

## Usage Examples

```bash
# SPARC commands
/sparc build a user authentication system
/code implement the login function
/debug fix the null pointer error
/tdd write tests for the auth module

# Essential commands
/build-feature add dark mode toggle
/fix-bug resolve the memory leak
/review-pr check PR #123

# Workflow commands
/development start feature development
/deployment deploy to production
```

---

## Command Discovery

Agents can list available commands:
```bash
ls ~/.claude/commands/*.md | head -20
```

Or search by keyword:
```bash
grep -l "security" ~/.claude/commands/*.md
```
