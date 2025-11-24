# E2B Sandboxes + Claude Code Hooks Integration Plan

**Date**: 2025-11-18
**Status**: Analysis Complete, Ready for Implementation
**Based On**: YouTube transcripts analysis via Sequential Thinking MCP

---

## Executive Summary

Analysis of two cutting-edge agentic coding patterns reveals our Agent Reality Map system is **80% architecturally complete** and positioned to leverage both patterns immediately. We already have Flow Nexus MCP with sandbox orchestration - we just need to wire it into our hooks system to unlock Best-of-N competitive execution and comprehensive observability.

---

## Key Insights from Video Analysis

### Video 1: E2B Agent Sandboxes (Reddit Landing Page Fix)

**Core Pattern**: Scale Compute → Scale Impact

**Architecture**:
```
Orchestrator Agent
    ↓
Spawn N Parallel Agents (9 in video)
    ↓
Each Agent:
    - Gets isolated E2B sandbox
    - Clones codebase to unique branch
    - Makes changes independently
    - Creates PR + public URL
    ↓
Human Reviews N Solutions
    ↓
Select Best Solution (Best-of-N)
```

**Key Metrics**:
- 9 sandboxes spawned in parallel
- 30-minute sandbox lifetime (ephemeral)
- Each sandbox: Full git environment + Node.js + auto-deployed URL
- Pattern: Same prompt × N agents = N different solutions

**Value Proposition**:
1. **Isolation**: Each agent has dedicated environment (no contamination)
2. **Scale**: Parallel compute (9× faster than sequential)
3. **Agency**: Agents have full autonomy in their sandbox

**Cost Trade-off**:
- Requires API usage (not covered by Claude Pro)
- Sandboxes are ephemeral (auto-delete after timeout)
- Acceptable cost for quality improvements

---

### Video 2: Claude Code Hooks (Observability + Control)

**Core Pattern**: Measure → Improve

**Hook Lifecycle**:
```
PreToolUse → [Tool Execution] → PostToolUse
                                      ↓
                                 Stop Hook
                                      ↓
                              SubagentStop Hook
```

**Key Hooks**:

1. **PreToolUse** (CONTROL)
   - Block dangerous commands (`rm -rf`)
   - Enforce RBAC rules
   - Validate environment access
   - Non-blocking continuation option

2. **PostToolUse** (OBSERVABILITY)
   - Log every tool execution
   - Capture tool inputs/outputs
   - Record execution time
   - Store in structured logs

3. **Stop** (COMPLETION)
   - Dump full chat transcript
   - Send notifications (text-to-speech in video)
   - Archive session state
   - Trigger post-processing

4. **SubagentStop** (PARALLEL TRACKING)
   - Track parallel agent completions
   - Aggregate results
   - Report individual successes/failures

**Implementation Pattern** (from video):
- Single-file Python scripts with Astral UV
- Modular utilities (TTS, logging, validation)
- Read from stdin → Process → Write to logs
- Non-blocking execution (always return success)

**The Big Three**: Context, Model, Prompt
- Never goes away regardless of tool/model
- Hooks give control over all three
- Observability lets you improve all three

---

## Our Current Architecture (What We Have)

### ✅ COMPLETE Components

1. **Agent Reality Map Backend**
   - FastAPI with 20+ endpoints
   - SQLite database (agent_audit_log table)
   - AuditLog model with full schema
   - WebSocket server at /ws
   - CORS configured for frontend

2. **Visibility Pipeline Hook**
   - `hooks/12fa/visibility-pipeline.js` (239 lines)
   - PostToolUse hook capturing all tool events
   - Database logging via backend API
   - Fallback file logging
   - Real-time event broadcasting

3. **Agent Registry**
   - 207 agents with UUID, role, RBAC
   - Complete identity schema (JSON Schema v7)
   - 10 roles with granular permissions
   - Runtime identity store

4. **Flow Nexus MCP** (CRITICAL DISCOVERY)
   - ✅ `mcp__flow-nexus__sandbox_create`
   - ✅ `mcp__flow-nexus__sandbox_execute`
   - ✅ `mcp__flow-nexus__sandbox_status`
   - ✅ `mcp__flow-nexus__sandbox_stop`
   - ✅ E2B integration ALREADY AVAILABLE

5. **Hooks Infrastructure**
   - `hooks/hooks.json` configuration
   - PreToolUse, PostToolUse, Stop, SubagentStop definitions
   - Hook categories (coordination, memory, automation, security, observability)

---

## ❌ MISSING Components (Gaps from Audit)

### Gap #1: Frontend Dashboard (Priority 1)
**Status**: Archived but not restored
**Location**: `C:\Users\17175\archive\ruv-sparc-ui-dashboard-20251115\`
**Effort**: 1 hour
**Impact**: Unlocks visual monitoring

### Gap #2: Backend Services Layer (Priority 2)
**Status**: Directory exists but empty
**Expected**: `backend/app/services/hooks_ingestion.py`, `quality_score_service.py`, `agent_registry_service.py`
**Effort**: 3-4 hours
**Impact**: Clean architecture, better testability

### Gap #3: Connascence Quality Pipeline (Priority 3)
**Status**: Not started
**File**: `hooks/12fa/connascence-pipeline.js`
**Effort**: 2-3 hours
**Impact**: Automated quality gates

### Gap #4: Best-of-N Pipeline (Priority 4)
**Status**: Not started
**File**: `hooks/12fa/best-of-n-pipeline.js`
**Effort**: 2-3 hours
**Impact**: Quality selection via parallel execution

### Gap #5: Security Hooks Implementation
**Status**: Defined in hooks.json but .js files missing
**Files Needed**:
- `hooks/12fa/security-hooks/pre-identity-verify.js`
- `hooks/12fa/security-hooks/pre-permission-check.js`
- `hooks/12fa/security-hooks/pre-budget-enforce.js`
- `hooks/12fa/security-hooks/pre-approval-gate.js`
- `hooks/12fa/security-hooks/post-budget-deduct.js`

**Effort**: 2-3 hours
**Impact**: RBAC enforcement, security compliance

---

## Integration Strategy: Apply Video Patterns to Our Gaps

### Pattern 1: E2B Sandboxes → Best-of-N Pipeline

**Implementation Plan**:

```javascript
// hooks/12fa/best-of-n-pipeline.js

/**
 * Best-of-N Competitive Execution Pipeline
 * Spawns N agents in parallel Flow Nexus sandboxes
 * Each solves same problem independently
 * Selects best solution based on quality metrics
 */

async function execute(context) {
  const N = 3; // Number of parallel attempts
  const sandboxes = [];

  // 1. Create N sandboxes via Flow Nexus MCP
  for (let i = 0; i < N; i++) {
    const sandbox = await mcp__flow_nexus__sandbox_create({
      template: 'node',
      name: `best-of-n-${context.taskId}-fork-${i}`,
      timeout: 1800, // 30 minutes
      env_vars: {
        TASK_PROMPT: context.prompt,
        FORK_ID: i.toString()
      }
    });
    sandboxes.push(sandbox);
  }

  // 2. Execute same task in parallel across all sandboxes
  const results = await Promise.all(
    sandboxes.map(sandbox =>
      mcp__flow_nexus__sandbox_execute({
        sandbox_id: sandbox.id,
        code: context.taskCode,
        timeout: 300
      })
    )
  );

  // 3. Evaluate quality of each solution
  const evaluated = await Promise.all(
    results.map(async (result, i) => {
      // Run connascence analysis on output
      const quality = await analyzeQuality(result.output);
      return {
        fork: i,
        sandbox: sandboxes[i],
        result: result,
        quality: quality,
        score: calculateScore(quality)
      };
    })
  );

  // 4. Select best solution
  const winner = evaluated.sort((a, b) => b.score - a.score)[0];

  // 5. Log to database via visibility pipeline
  await logBestOfNResult({
    task_id: context.taskId,
    attempts: N,
    winner_fork: winner.fork,
    winner_score: winner.score,
    all_scores: evaluated.map(e => e.score)
  });

  // 6. Cleanup sandboxes
  await Promise.all(
    sandboxes.map(s => mcp__flow_nexus__sandbox_stop({ sandbox_id: s.id }))
  );

  return {
    success: true,
    winner: winner.result,
    quality_score: winner.score,
    attempts: N
  };
}
```

**Benefits**:
- Leverages existing Flow Nexus MCP (no new infrastructure)
- Parallel execution (3× faster than sequential)
- Quality-based selection (not random)
- Isolated environments (no contamination)

---

### Pattern 2: Claude Code Hooks → Security Enforcement

**Implementation Plan**:

```javascript
// hooks/12fa/security-hooks/pre-identity-verify.js

/**
 * Pre-Identity-Verify Hook
 * Blocks tool use if agent identity is invalid or missing
 * Priority: 1 (first in security chain)
 */

const VALID_AGENTS = require('../../agents/identity/agent-registry.json');

function isDangerousCommand(context) {
  const dangerous = [
    /rm\s+-rf/,
    /del\s+\/s/,
    /format\s+c:/,
    /dd\s+if=/
  ];

  if (context.toolName === 'Bash') {
    const command = context.command || '';
    return dangerous.some(pattern => pattern.test(command));
  }

  return false;
}

function isEnvironmentFileAccess(context) {
  const envFiles = ['.env', '.env.local', 'credentials.json', 'secrets.yaml'];

  if (context.toolName === 'Read' || context.toolName === 'Edit') {
    const filePath = context.file_path || context.filePath || '';
    return envFiles.some(file => filePath.includes(file));
  }

  return false;
}

function verifyAgentIdentity(context) {
  const agentId = context.agentId || context.agent_id;

  if (!agentId) {
    return {
      allowed: false,
      reason: 'Agent identity missing (agentId required)'
    };
  }

  const agent = VALID_AGENTS.find(a => a.agent_id === agentId);

  if (!agent) {
    return {
      allowed: false,
      reason: `Unknown agent: ${agentId} (not in registry)`
    };
  }

  // Check RBAC permissions
  const toolName = context.toolName;
  const allowedTools = agent.rbac?.allowed_tools || [];

  if (!allowedTools.includes(toolName)) {
    return {
      allowed: false,
      reason: `Agent ${agentId} not authorized for tool: ${toolName}`
    };
  }

  return {
    allowed: true,
    reason: 'Agent identity verified',
    agent: agent
  };
}

async function execute(context) {
  // Check dangerous commands
  if (isDangerousCommand(context)) {
    console.error('[pre-identity-verify] BLOCKED: Dangerous command detected');
    return {
      success: false,
      reason: 'Command blocked: Dangerous operation (rm -rf, del /s, etc.)',
      allowed: false,
      blocking: true
    };
  }

  // Check environment file access
  if (isEnvironmentFileAccess(context)) {
    console.error('[pre-identity-verify] BLOCKED: Environment file access');
    return {
      success: false,
      reason: 'File access blocked: Environment/credentials file',
      allowed: false,
      blocking: true
    };
  }

  // Verify agent identity
  const verification = verifyAgentIdentity(context);

  if (!verification.allowed) {
    console.error(`[pre-identity-verify] BLOCKED: ${verification.reason}`);
    return {
      success: false,
      reason: verification.reason,
      allowed: false,
      blocking: true
    };
  }

  console.log(`[pre-identity-verify] ALLOWED: ${verification.agent.name} (${verification.agent.role})`);

  return {
    success: true,
    reason: verification.reason,
    allowed: true,
    agent: verification.agent
  };
}

module.exports = { execute };
```

**Benefits**:
- Prevents dangerous operations (like rm -rf in video)
- Enforces RBAC before tool execution
- Protects sensitive files (.env, credentials)
- Non-blocking for allowed operations

---

### Pattern 3: Comprehensive Observability → Enhanced Visibility Pipeline

**Enhancement Plan** (additions to existing visibility-pipeline.js):

```javascript
// Add chat transcript logging (from Stop hook pattern in video)

function logFullChatTranscript(context) {
  const transcript = {
    session_id: context.sessionId,
    messages: context.messages || [],
    total_tokens: context.totalTokens || 0,
    agent_count: context.agentCount || 1,
    tools_used: extractToolsUsed(context.messages),
    timestamp: new Date().toISOString()
  };

  fs.writeFileSync(
    path.join(__dirname, '..', 'logs', `chat-${context.sessionId}.json`),
    JSON.stringify(transcript, null, 2)
  );
}

// Add text-to-speech notifications (optional enhancement)

async function sendNotification(message) {
  // Could integrate with 11Labs API or local TTS
  // For now, just console log
  console.log(`[NOTIFICATION] ${message}`);

  // Future: Text-to-speech
  // const audio = await elevenLabs.textToSpeech(message);
  // audio.play();
}
```

---

## Implementation Roadmap (6-8 Hours to 100%)

### Phase 1: Security Foundation (2-3 hours)

**Tasks**:
1. Implement `pre-identity-verify.js` (1 hour)
2. Implement `pre-permission-check.js` (30 min)
3. Implement `pre-budget-enforce.js` (30 min)
4. Implement `pre-approval-gate.js` (30 min)
5. Test security hooks with dangerous commands (30 min)

**Deliverable**: Full RBAC enforcement with dangerous command blocking

---

### Phase 2: Best-of-N Pipeline (2-3 hours)

**Tasks**:
1. Create `best-of-n-pipeline.js` hook (1.5 hours)
2. Integrate with Flow Nexus MCP sandboxes (1 hour)
3. Add quality scoring (connascence integration) (30 min)
4. Test with 3 parallel agents (30 min)

**Deliverable**: Competitive execution with quality selection

---

### Phase 3: Connascence Quality Gates (2-3 hours)

**Tasks**:
1. Create `connascence-pipeline.js` hook (1.5 hours)
2. Integrate with connascence-analyzer MCP (1 hour)
3. Add quality thresholds (configurable) (30 min)
4. Test with code quality violations (30 min)

**Deliverable**: Automated quality gates blocking low-quality code

---

### Phase 4: Frontend Dashboard (1 hour)

**Tasks**:
1. Restore from archive (15 min)
2. Update API endpoints (15 min)
3. Test WebSocket integration (15 min)
4. Deploy to localhost:3000 (15 min)

**Deliverable**: Visual monitoring of all agent activity

---

## Technical Architecture (Post-Implementation)

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Tool Use                      │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────▼─────────────┐
        │   PreToolUse Hooks       │
        │  (Security Pipeline)     │
        ├──────────────────────────┤
        │ 1. pre-identity-verify   │ ← Block dangerous commands
        │ 2. pre-permission-check  │ ← Enforce RBAC
        │ 3. pre-budget-enforce    │ ← Check budget limits
        │ 4. pre-approval-gate     │ ← Human approval (if needed)
        └────────────┬─────────────┘
                     │
              [ALLOWED?]
                     │
                    YES
                     │
        ┌────────────▼─────────────┐
        │    Tool Execution        │
        └────────────┬─────────────┘
                     │
        ┌────────────▼─────────────┐
        │  PostToolUse Hooks       │
        │  (Observability Pipeline)│
        ├──────────────────────────┤
        │ 1. visibility-pipeline   │ ← Log to database + WebSocket
        │ 2. post-audit-trail      │ ← Audit compliance
        │ 3. post-budget-deduct    │ ← Deduct costs
        └────────────┬─────────────┘
                     │
        ┌────────────▼─────────────┐
        │ Backend API              │
        │ /api/v1/events/ingest    │
        └────────┬─────────┬───────┘
                 │         │
           ┌─────▼──┐   ┌──▼──────┐
           │Database│   │WebSocket│
           │SQLite  │   │  /ws    │
           └────────┘   └────┬────┘
                             │
                        ┌────▼────┐
                        │Dashboard│
                        │ React   │
                        └─────────┘

For Best-of-N Tasks:
┌─────────────────────────────────────────────────────────────┐
│             best-of-n-pipeline.js                            │
└────────────────────┬────────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
│ Sandbox 1 │  │ Sandbox 2 │  │ Sandbox 3 │
│ (E2B/Flow)│  │ (E2B/Flow)│  │ (E2B/Flow)│
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
            ┌────────▼────────┐
            │ Quality Scorer  │
            │ (Connascence)   │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │ Select Winner   │
            └─────────────────┘
```

---

## Key Patterns Applied

### 1. Context, Model, Prompt (The Big Three)

**Maps to Our Three-Loop System**:
- **Loop 1** (research-driven-planning) = Better CONTEXT through research
- **Loop 2** (parallel-swarm-implementation) = Optimal MODELS (agent selection)
- **Loop 3** (cicd-intelligent-recovery) = Validated PROMPTS through testing

**Enhanced with Hooks**:
- PreToolUse → Control CONTEXT (what agents can access)
- PostToolUse → Measure MODEL performance
- Stop Hook → Capture full PROMPTS (chat transcripts)

---

### 2. Best-of-N Competitive Execution

**Pattern from Video**:
- Same prompt × N agents = N solutions
- Human reviews all solutions
- Select best based on quality

**Our Implementation**:
- Same task × 3 sandboxes = 3 solutions
- Automated quality scoring (connascence metrics)
- Select winner programmatically
- Deploy winner, discard losers

---

### 3. Comprehensive Observability

**Pattern from Video**:
- PreToolUse logs (block dangerous operations)
- PostToolUse logs (record all executions)
- Stop logs (full chat transcript)
- SubagentStop logs (parallel tracking)

**Our Implementation**:
- All hooks log to database via backend API
- Real-time WebSocket broadcasting
- Structured JSON logs for analysis
- Audit compliance (90-day retention)

---

## Success Metrics (Post-Implementation)

| Metric | Current | Target | How |
|--------|---------|--------|-----|
| Implementation Completeness | 96% | 100% | Complete all 4 gaps |
| Security Coverage | 60% | 100% | Implement all 5 security hooks |
| Observability | 70% | 100% | Full chat logs + metrics |
| Quality Automation | 0% | 100% | Connascence + Best-of-N pipelines |
| Visual Monitoring | 0% | 100% | Restore frontend dashboard |
| Hook Latency | 35-60ms | <50ms | Optimize database writes |
| Agent Autonomy | Medium | High | E2B sandboxes for isolation |

---

## Cost Analysis

### Sandbox Costs (Flow Nexus/E2B)

**Per Sandbox**:
- Compute: ~$0.01-0.05 per hour
- Lifetime: 30 minutes default
- Cost per sandbox: ~$0.005-0.025

**Best-of-N (3 sandboxes)**:
- 3 sandboxes × $0.015 avg = $0.045 per run
- Expected runs: 5-10 per day
- Monthly cost: $6.75-13.50

**ROI Calculation**:
- Cost: $10/month (estimate)
- Value: Automated quality selection (saves 2-4 hours/week)
- Engineer time saved: 8-16 hours/month
- ROI: 80-160× at $100/hour rate

**Verdict**: Highly cost-effective for quality improvements

---

## Next Steps (Immediate Actions)

1. **Implement Security Hooks** (2-3 hours)
   - Use pre-identity-verify.js template above
   - Test with dangerous commands
   - Verify RBAC enforcement

2. **Implement Best-of-N Pipeline** (2-3 hours)
   - Use best-of-n-pipeline.js template above
   - Test with Flow Nexus sandboxes
   - Integrate quality scoring

3. **Restore Frontend Dashboard** (1 hour)
   - Copy from archive
   - Update API endpoints
   - Test WebSocket integration

4. **Document Everything** (1 hour)
   - Update VISIBILITY-PIPELINE-COMPLETE.md
   - Create BEST-OF-N-COMPLETE.md
   - Create SECURITY-HOOKS-COMPLETE.md

---

## References

- **Video 1**: E2B Agent Sandboxes - Reddit Landing Page Fix
- **Video 2**: Claude Code Hooks - Advanced Agentic Coding
- **Audit Report**: `docs/AUDIT-COMPLETION-SYNTHESIS.md`
- **Visibility Pipeline**: `docs/VISIBILITY-PIPELINE-COMPLETE.md`
- **Flow Nexus MCP**: Available MCP tools (sandbox_create, sandbox_execute, etc.)
- **Agent Registry**: `agents/identity/agent-registry.json`

---

**Status**: Ready for implementation
**Total Effort**: 6-8 hours to 100% completion
**Priority**: Security hooks first, then Best-of-N, then frontend
**ROI**: 80-160× return on investment
