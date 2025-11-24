# Developer Guide - Adding Agents

## Overview

The Agent Reality Map currently manages 207 agents across 10 categories. This guide covers adding new agents to the system.

## Agent Registry Structure

**Location**: `agents/` directory

**Categories** (10 total):
- delivery/ (18 agents)
- foundry/ (19 agents)
- operations/ (28 agents)
- orchestration/ (21 agents)
- platforms/ (44 agents)
- quality/ (18 agents)
- research/ (11 agents)
- security/ (5 agents)
- specialists/ (15 agents)
- tooling/ (24 agents)

## Adding a New Agent

### Step 1: Create Agent Definition

**File**: `agents/{category}/{agent-name}.md`

**Format** (Markdown with YAML frontmatter):

```markdown
---
name: my-specialist
type: specialist
phase: development
category: specialists
capabilities:
  - task-specific-capability
  - another-capability
tools:
  - Read
  - Write
  - Bash
mcp_servers:
  - claude-flow
  - memory-mcp
hooks:
  pre:
    - identity-verify
    - permission-check
  post:
    - audit-trail
quality_gates:
  - connascence: true
  - theater_detection: true
artifact_contracts:
  input: {required_files: [], optional_params: []}
  output: {deliverables: [], success_criteria: []}
---

# Agent Name

## Purpose
What this agent does...

## When to Use
Activate when...

## Capabilities
- Capability 1
- Capability 2

## SOP Workflow
1. Step 1
2. Step 2
3. Step 3

## Integration Points
- Integrates with: other-agent-1, other-agent-2
- Feeds data to: downstream-agent
- Receives from: upstream-agent
```

### Step 2: Register Agent Identity

**File**: `hooks/12fa/.identity-store.json`

```json
{
  "agents": {
    "my-specialist-001": {
      "agent_id": "generate-uuid-here",
      "role": "specialist",
      "capabilities": ["task-specific-capability"],
      "rbac": {
        "allowed_tools": ["Read", "Write", "Edit"],
        "path_scopes": ["src/**", "docs/**"],
        "api_access": ["github"]
      },
      "budget": {
        "max_tokens_per_session": 50000,
        "max_cost_per_day": 20.0
      }
    }
  }
}
```

### Step 3: Add to Database

**Method 1: Backend API**:
```bash
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "uuid-here",
    "name": "my-specialist-001",
    "role": "specialist",
    "capabilities": ["task-specific-capability"],
    "rbac_allowed_tools": ["Read", "Write", "Edit"],
    "rbac_path_scopes": ["src/**"],
    "rbac_api_access": ["github"],
    "budget_max_tokens_per_session": 50000,
    "budget_max_cost_per_day": 20.0,
    "metadata_category": "specialists",
    "metadata_specialist": true,
    "metadata_tags": ["specialist", "task-specific"]
  }'
```

**Method 2: Direct Database Insert**:
```sql
INSERT INTO agents (
  agent_id, name, role, capabilities,
  rbac_allowed_tools, rbac_path_scopes, rbac_api_access,
  budget_max_tokens_per_session, budget_max_cost_per_day,
  metadata_category, metadata_specialist, metadata_tags
) VALUES (
  'uuid-here', 'my-specialist-001', 'specialist', '["capability1"]',
  '["Read","Write"]', '["src/**"]', '["github"]',
  50000, 20.0,
  'specialists', true, '["specialist","task"]'
);
```

### Step 4: Test Agent

```bash
# Test RBAC enforcement
node hooks/12fa/tests/test-rbac-pipeline.js

# Test agent appears in registry
curl http://localhost:8000/api/v1/registry/agents | jq '.[] | select(.name == "my-specialist-001")'

# Test frontend display
# Open http://localhost:3000 and find agent in registry
```

## Agent Categories

### Choosing the Right Category

- **delivery**: Feature/product implementation
- **foundry**: Agent creation, templates
- **operations**: DevOps, infra, monitoring
- **orchestration**: Goal planning, coordination
- **platforms**: Data, ML, cloud platforms
- **quality**: Analysis, audit, testing
- **research**: Research, reasoning
- **security**: Compliance, pentesting
- **specialists**: Domain experts (business, legal, etc.)
- **tooling**: Documentation, GitHub tools

## Best Practices

1. **Name Convention**: `{role}-{number}` (e.g., `coder-001`)
2. **Unique UUIDs**: Generate with `uuidgen` or `node -e "console.log(crypto.randomUUID())"`
3. **Minimal Permissions**: Start with least privilege, expand as needed
4. **Budget Appropriately**: Match budget to expected usage
5. **Document Thoroughly**: Clear purpose, capabilities, integration points
6. **Test Before Production**: Run RBAC tests, verify in frontend
7. **Version Control**: Commit agent definition to git

## Integration Checklist

When adding a new agent:

- [ ] Agent definition file created (`agents/{category}/{name}.md`)
- [ ] Identity registered (`.identity-store.json`)
- [ ] Database record created (via API or SQL)
- [ ] RBAC permissions configured
- [ ] Budget limits set
- [ ] MCP servers specified
- [ ] Hooks configured (pre/post)
- [ ] Quality gates enabled
- [ ] Documentation complete
- [ ] RBAC tests passing
- [ ] Agent visible in frontend
- [ ] Git commit created

## Example: Adding a TypeScript Specialist

```bash
# 1. Create definition
cat > agents/specialists/typescript-expert.md <<EOF
---
name: typescript-expert
type: specialist
category: specialists
capabilities: [typescript, type-safety, refactoring]
tools: [Read, Write, Edit]
---
# TypeScript Expert
Specializes in TypeScript development, type safety, and refactoring.
EOF

# 2. Generate UUID
UUID=$(node -e "console.log(crypto.randomUUID())")

# 3. Register identity
node -e "
const fs = require('fs');
const store = JSON.parse(fs.readFileSync('hooks/12fa/.identity-store.json'));
store.agents['typescript-expert-001'] = {
  agent_id: '$UUID',
  role: 'specialist',
  capabilities: ['typescript', 'type-safety'],
  rbac: {
    allowed_tools: ['Read', 'Write', 'Edit'],
    path_scopes: ['src/**'],
    api_access: []
  },
  budget: {
    max_tokens_per_session: 50000,
    max_cost_per_day: 20.0
  }
};
fs.writeFileSync('hooks/12fa/.identity-store.json', JSON.stringify(store, null, 2));
"

# 4. Add to database
curl -X POST http://localhost:8000/api/v1/agents/ \
  -H "Content-Type: application/json" \
  -d "{\"agent_id\": \"$UUID\", \"name\": \"typescript-expert-001\", ...}"

# 5. Test
node hooks/12fa/tests/test-rbac-pipeline.js
```

## Troubleshooting

### Agent Not Appearing

1. Check database: `curl http://localhost:8000/api/v1/agents/ | grep "agent-name"`
2. Check identity store: `grep "agent-name" hooks/12fa/.identity-store.json`
3. Check category folder: `ls agents/{category}/{agent-name}.md`

### RBAC Blocking Agent

1. Review role permissions in `agents/identity/agent-rbac-rules.json`
2. Check audit log: `grep "agent-name" hooks/12fa/.audit-trail.log`
3. Verify allowed_tools match attempted operations

### Budget Issues

1. Check budget config in `.identity-store.json`
2. Review usage: `grep "agent-name" hooks/12fa/.audit-trail.log | grep budget`
3. Increase limits if needed

## Support

- **Agent Registry**: View all agents at `agents/README.md`
- **RBAC Rules**: See `agents/identity/agent-rbac-rules.json`
- **Capability Matrix**: See `agents/identity/agent-capability-matrix.json`
