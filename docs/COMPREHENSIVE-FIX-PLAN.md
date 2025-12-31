# Comprehensive Fix Plan: Context Cascade Architecture Remediation

## Synthesized from Three Independent Audits
- Claude Direct Analysis (primary)
- Codex/ChatGPT External Audit
- Gemini Forensic Architecture Review

---

## Executive Summary

Context Cascade is a sophisticated multi-agent cognitive architecture with 211 agents, 196 skills, and 245 commands. Three independent audits have identified critical architectural gaps between the system's aspirational design and actual implementation.

**Key Insight**: The system exhibits "Security Theater" and "Protocol Theater" - where sophisticated terminology (VeriX, Byzantine Consensus, RBAC) is used in documentation but not implemented in code.

**Total Issues Identified**: 15 distinct problems across 4 severity levels
**Estimated Fix Time**: 5-6 weeks for full remediation
**Quick Wins Available**: 3 issues fixable in <1 day

---

## Phase 0: Immediate Fixes (Day 1)

### 0.1 Remove claude-flow@alpha Dependency
**Severity**: CRITICAL
**Effort**: 15 minutes
**Impact**: Eliminates broken dependency

```json
// BEFORE: .mcp.json
{
  "claude-flow": {
    "command": "cmd",
    "args": ["/c", "npx", "claude-flow@alpha", "mcp", "start"]
  }
}

// AFTER: Remove entirely - ruv-swarm + flow-nexus provide same functionality
```

**Verification**: Run `npx mcp-client list-tools` to confirm no broken connections.

### 0.2 Rename VeriX to Epistemic Notation
**Severity**: CRITICAL
**Effort**: 30 minutes
**Impact**: Eliminates misleading terminology

```bash
# Files to rename:
# cognitive-architecture/core/verix.py -> epistemic_notation.py
# cognitive-architecture/commands/verix.py -> epistemic_commands.py

# Update all imports and references
```

**New Documentation Header**:
```python
"""
EPISTEMIC NOTATION (formerly Verix)

NOTE: This is a structured notation system for epistemic claims.
It is NOT formal verification in the mathematical sense (no SMT solvers).
It provides structured reasoning, not mathematical proofs.
"""
```

### 0.3 Add Emergency Kill Switch
**Severity**: HIGH
**Effort**: 1 hour
**Impact**: Prevents runaway meta-loop

```python
# Add to cognitive-architecture/loopctl/core.py

import os
from pathlib import Path

def check_emergency_stop() -> bool:
    """Check for emergency stop signals."""
    # File-based kill switch
    if Path('.meta-loop-stop').exists():
        return True
    if Path(os.path.expanduser('~/.meta-loop-stop')).exists():
        return True

    # Environment variable kill switch
    if os.environ.get('META_LOOP_EMERGENCY_STOP', '').lower() == 'true':
        return True

    return False

# Add at start of ralph_iteration_complete():
if check_emergency_stop():
    return {
        "decision": "allow",
        "reason": "EMERGENCY_HALT: Kill switch activated",
    }
```

---

## Phase 1: Security Hardening (Week 1)

### 1.1 RBAC Enforcement Layer
**Severity**: CRITICAL
**Effort**: 3 days
**Impact**: Transforms semantic security to real security

**Current State**: JSON rules exist at `agents/identity/agent-rbac-rules.json` but are not enforced.

**Target Architecture**:
```
Agent Request -> Identity Check -> Permission Validator -> Tool Execution
                      |                    |
                      v                    v
                 agent-tokens/      agent-rbac-rules.json
```

**Implementation**:

```javascript
// hooks/12fa/rbac-enforcer.js

const crypto = require('crypto');
const fs = require('fs');

const RBAC_RULES = JSON.parse(
  fs.readFileSync('agents/identity/agent-rbac-rules.json', 'utf8')
);

function enforceRBAC(agentId, toolName, targetPath) {
  // 1. Validate agent identity token
  const token = process.env[`AGENT_TOKEN_${agentId}`];
  if (!token) {
    throw new Error(`RBAC: No token for agent ${agentId}`);
  }

  // 2. Get agent's role
  const role = getAgentRole(agentId);
  const permissions = RBAC_RULES.roles[role]?.permissions;

  if (!permissions) {
    throw new Error(`RBAC: Unknown role ${role}`);
  }

  // 3. Check tool permission
  if (!permissions.tools.includes(toolName) && !permissions.tools.includes('*')) {
    throw new Error(`RBAC: Agent ${agentId} (${role}) cannot use ${toolName}`);
  }

  // 4. Check path permission
  if (!matchPath(targetPath, permissions.paths)) {
    throw new Error(`RBAC: Agent ${agentId} cannot access ${targetPath}`);
  }

  return true;
}

module.exports = { enforceRBAC };
```

### 1.2 MCP Checksum Validation
**Severity**: HIGH
**Effort**: 2 days
**Impact**: Prevents tool poisoning attacks

```javascript
// scripts/mcp-integrity-checker.js

const crypto = require('crypto');
const fs = require('fs');

const KNOWN_CHECKSUMS = {
  'ruv-swarm': 'sha256:abc123...',
  'flow-nexus': 'sha256:def456...',
  'memory-mcp': 'sha256:ghi789...',
};

function validateMCPServer(serverName, serverPath) {
  const content = fs.readFileSync(serverPath);
  const hash = crypto.createHash('sha256').update(content).digest('hex');

  if (KNOWN_CHECKSUMS[serverName] !== `sha256:${hash}`) {
    throw new Error(`MCP TAMPERED: ${serverName} checksum mismatch`);
  }

  return true;
}
```

---

## Phase 2: Provider Abstraction Layer (Week 2)

### 2.1 Company-Agnostic Model Router
**Severity**: MEDIUM
**Effort**: 5 days
**Impact**: Removes vendor lock-in

**Directory Structure**:
```
orchestration-pal/
  providers/
    base-provider.js      # Abstract interface
    claude-provider.js    # Anthropic Claude
    codex-provider.js     # OpenAI Codex
    gemini-provider.js    # Google Gemini
    openrouter-provider.js # Multi-model
  router/
    model-router.js       # Task -> Provider routing
    fallback-handler.js   # Automatic failover
  config/
    providers.json        # Provider credentials
    routing-rules.json    # Task routing rules
```

**Base Provider Interface**:
```javascript
// orchestration-pal/providers/base-provider.js

class BaseProvider {
  constructor(config) {
    this.name = config.name;
    this.enabled = config.enabled;
  }

  async complete(prompt, options = {}) {
    throw new Error('Must implement complete()');
  }

  async isHealthy() {
    throw new Error('Must implement isHealthy()');
  }

  getStrengths() {
    throw new Error('Must implement getStrengths()');
  }
}
```

### 2.2 Unified MCP Server
**Severity**: MEDIUM
**Effort**: 4 days
**Impact**: Replaces broken claude-flow@alpha

```javascript
// mcp-servers/context-cascade-orchestrator/index.js

const { Server } = require('@anthropic-ai/mcp');
const ruvSwarmAdapter = require('./adapters/ruv-swarm');
const flowNexusAdapter = require('./adapters/flow-nexus');
const memoryMCPAdapter = require('./adapters/memory-mcp');

const server = new Server('context-cascade-orchestrator');

// Wrap existing MCPs with unified interface
server.tool('orchestrator.spawn_agent', async (params) => {
  return ruvSwarmAdapter.agentSpawn(params);
});

server.tool('orchestrator.run_sandbox', async (params) => {
  return flowNexusAdapter.sandboxExecute(params);
});

server.tool('orchestrator.store_memory', async (params) => {
  return memoryMCPAdapter.store(params);
});
```

---

## Phase 3: Agent Archetype Consolidation (Week 3)

### 3.1 Reduce 211 Agents to 20 Archetypes
**Severity**: MEDIUM
**Effort**: 1 week
**Impact**: Reduces classification complexity

**Proposed Archetypes**:
| Archetype | Covers | Count Reduction |
|-----------|--------|-----------------|
| SystemsArchitect | system-architect, infrastructure-*, devops-* | 8 -> 1 |
| BackendEngineer | backend-dev, api-*, golang-*, rust-*, python-* | 25 -> 1 |
| FrontendEngineer | react-*, vue-*, ui-*, css-*, a11y-* | 15 -> 1 |
| DataEngineer | sql-*, database-*, etl-* | 10 -> 1 |
| QualityEngineer | tester, reviewer, qa-*, audit-* | 18 -> 1 |
| SecurityEngineer | security-*, compliance-*, pentest-* | 12 -> 1 |
| MLEngineer | ml-*, tensorflow-*, pytorch-* | 8 -> 1 |
| DevOpsEngineer | docker-*, k8s-*, cicd-* | 12 -> 1 |
| Coordinator | hierarchical-*, mesh-*, queen-* | 15 -> 1 |
| Researcher | deep-research-*, literature-* | 10 -> 1 |

**Dynamic Context Injection**:
```javascript
// Instead of 211 separate agents:
const backendEngineer = new Archetype('BackendEngineer');

// Inject domain context dynamically:
backendEngineer.withContext({ language: 'rust' });
backendEngineer.withContext({ framework: 'actix-web' });
```

---

## Phase 4: Protocol Implementation or Removal (Week 4)

### 4.1 Decision: Implement or Remove Byzantine/Raft/Paxos

**Option A: Implement Properly**
- Use actual distributed systems libraries
- Redis-backed leader election for Raft
- Cryptographic signatures for Byzantine

**Option B: Remove Claims (RECOMMENDED)**
- Delete protocol descriptions from skills
- Replace with "single-verifier + human review"
- Honest about what system actually does

**Recommendation**: Option B - The system doesn't need distributed consensus. It's running on a single machine with API calls. Remove the aspirational protocol descriptions.

### 4.2 Replace Consensus with Ground Truth
```javascript
// Instead of: "5 agents vote on code quality"
// Use: "1 agent runs tests, exit code is truth"

async function validateCode(code) {
  // Deterministic ground truth, not LLM consensus
  const testResult = await runTests(code);
  const lintResult = await runLinter(code);
  const typeResult = await runTypeCheck(code);

  return {
    valid: testResult.passed && lintResult.passed && typeResult.passed,
    evidence: { testResult, lintResult, typeResult }
  };
}
```

---

## Phase 5: Test Coverage Expansion (Ongoing)

### 5.1 E2E Tests for Critical Paths
**Current**: 38 test files
**Target**: 200+ test files

**Priority Tests**:
1. Three-loop workflow (planning -> implementation -> CI/CD)
2. Agent spawn and communication
3. RBAC enforcement
4. Kill switch activation
5. MCP tool invocation

```javascript
// tests/e2e/three-loop-workflow.test.js

describe('Three-Loop Workflow', () => {
  test('Loop 1: Planning produces valid task breakdown', async () => {
    const result = await executeLoop1('Add login feature');
    expect(result.tasks).toHaveLength(greaterThan(0));
    expect(result.tasks[0]).toHaveProperty('description');
    expect(result.tasks[0]).toHaveProperty('agent');
  });

  test('Loop 2: Implementation produces working code', async () => {
    const result = await executeLoop2(mockTasks);
    expect(result.code).toBeDefined();
    expect(await runTests(result.code)).toEqual({ passed: true });
  });

  test('Loop 3: CI/CD validates and deploys', async () => {
    const result = await executeLoop3(mockImplementation);
    expect(result.validated).toBe(true);
    expect(result.deployed).toBe(true);
  });
});
```

---

## Phase 6: Codex Sandbox Integration (Week 5)

### 6.1 Route All Tests Through Sandbox
**Severity**: MEDIUM
**Effort**: 3 days
**Impact**: Isolated test execution

```javascript
// testing/sandbox-runner.js

async function runInSandbox(command, options = {}) {
  const mode = options.networkRequired ? 'workspace-write' : 'read-only';

  // Use Codex CLI for sandboxed execution
  const result = await exec(
    `bash -lc "codex --sandbox ${mode} exec '${command}'"`
  );

  return {
    output: result.stdout,
    exitCode: result.exitCode,
    sandboxed: true,
    mode
  };
}

// Usage:
const testResult = await runInSandbox('npm test');
```

---

## Configuration Changes

### Updated .mcp.json
```json
{
  "mcpServers": {
    "context-cascade-orchestrator": {
      "command": "node",
      "args": ["claude-code-plugins/context-cascade/mcp-servers/context-cascade-orchestrator/index.js"],
      "env": {
        "PROVIDERS_CONFIG": "claude-code-plugins/context-cascade/orchestration-pal/config/providers.json",
        "RBAC_ENABLED": "true"
      }
    },
    "ruv-swarm": {
      "command": "npx",
      "args": ["@anthropic/ruv-swarm", "start"],
      "checksum": "sha256:abc123..."
    },
    "flow-nexus": {
      "command": "npx",
      "args": ["@anthropic/flow-nexus", "start"],
      "checksum": "sha256:def456..."
    },
    "memory-mcp": {
      "command": "node",
      "args": ["D:/Projects/memory-mcp-triple-system/dist/index.js"]
    }
  }
}
```

### Safety Configuration
```json
// safety/config/safety-rules.json
{
  "metaLoop": {
    "killSwitch": {
      "fileChecks": [".meta-loop-stop", "~/.meta-loop-stop"],
      "envVar": "META_LOOP_EMERGENCY_STOP"
    },
    "limits": {
      "maxIterationsPerCycle": 10,
      "maxConsecutiveRegressions": 3,
      "maxDailyModifications": 50
    },
    "humanApprovalRequired": [
      "skill-modification",
      "agent-modification",
      "security-rule-changes",
      "eval-harness-changes"
    ]
  },
  "rbac": {
    "enabled": true,
    "enforceAtToolLevel": true,
    "auditLogging": true
  }
}
```

---

## Success Metrics

| Metric | Current | Target | Verification |
|--------|---------|--------|--------------|
| Broken MCP connections | 1 (claude-flow) | 0 | `npx mcp-client list-tools` |
| RBAC enforced in code | No | Yes | Integration test |
| Kill switch response time | N/A | <1s | Manual test |
| Test coverage | 38 files | 200+ files | `find . -name "*.test.*"` |
| Agent archetypes | 211 | 20 | Count after consolidation |
| Misleading terminology | 3+ instances | 0 | Grep for "VeriX formal" |
| MCP checksum validation | No | Yes | Security audit |

---

## Timeline Summary

| Week | Phase | Deliverables |
|------|-------|--------------|
| Day 1 | Phase 0 | Remove claude-flow, add kill switch, rename VeriX |
| Week 1 | Phase 1 | RBAC enforcement, MCP checksums |
| Week 2 | Phase 2 | Provider abstraction, unified MCP |
| Week 3 | Phase 3 | Agent archetypes (211 -> 20) |
| Week 4 | Phase 4 | Protocol cleanup, ground truth validation |
| Week 5 | Phase 5-6 | Test expansion, sandbox integration |
| Ongoing | Maintenance | Documentation sync, regression prevention |

---

## Appendix: Files to Modify

### Immediate (Phase 0)
- `.mcp.json` - Remove claude-flow@alpha
- `cognitive-architecture/core/verix.py` - Rename and add disclaimer
- `cognitive-architecture/loopctl/core.py` - Add kill switch check

### Week 1 (Phase 1)
- `hooks/12fa/rbac-enforcer.js` - New file
- `scripts/mcp-integrity-checker.js` - New file
- `agents/identity/agent-tokens/` - New directory

### Week 2 (Phase 2)
- `orchestration-pal/` - New directory structure
- `mcp-servers/context-cascade-orchestrator/` - New MCP server

### Week 3 (Phase 3)
- `agents/archetypes/` - New consolidated agents
- `agents/deprecated/` - Move old granular agents

### Week 4 (Phase 4)
- `skills/orchestration/advanced-coordination/SKILL.md` - Remove protocol claims
- `playbooks/docs/PLAYBOOK-META-LOOP-GUARDRAILS.md` - Update to match reality

---

*Document generated from synthesis of Claude, Codex, and Gemini audits.*
*Last updated: 2025-12-31*
