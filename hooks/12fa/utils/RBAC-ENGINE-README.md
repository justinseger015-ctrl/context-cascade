# RBAC Engine Core - Agent Reality Map Integration

Version: 1.0.0
Status: Production Ready
Last Updated: 2025-01-17

## Overview

The RBAC Engine Core provides comprehensive identity verification and permission enforcement for 207 agents across the Agent Reality Map Integration. It enforces Role-Based Access Control (RBAC) across 3 dimensions: tool whitelist, path scopes, and API access.

## Architecture

```
hooks/12fa/utils/
├── identity.js              # Identity verification (JWT, Ed25519, frontmatter parsing)
├── permission-checker.js    # RBAC enforcement (tools, paths, APIs)
├── validate-rbac-setup.js   # Validation script
├── package.json             # Dependencies
├── __tests__/
│   ├── identity.test.js     # Identity system unit tests
│   └── permission-checker.test.js  # Permission checker unit tests
└── README.md                # This file
```

## Features

### Identity Verification (`identity.js`)

- **JWT Token Generation/Validation**: Secure authentication with HS256 algorithm
- **Ed25519 Signature Verification**: Cryptographic identity validation
- **Frontmatter Parsing**: Extract agent identity from .md files (YAML frontmatter)
- **UUID v4 Validation**: Ensure all agent_id fields are valid UUIDs
- **Identity Caching**: 5-minute TTL for performance (<50ms per check)
- **Windows Compatible**: No Unicode characters

**Key Functions**:
```javascript
const {
  generateJWT,
  validateJWT,
  loadAgentIdentity,
  loadAgentIdentityByName,
  validateAgentIdentity
} = require('./identity');

// Generate JWT token
const token = generateJWT({
  agent_id: '550e8400-e29b-41d4-a716-446655440000',
  name: 'backend-dev',
  role: 'developer'
}, 3600); // expires in 1 hour

// Validate JWT token
const payload = validateJWT(token);
if (payload) {
  console.log('Valid token:', payload);
}

// Load agent identity by file path
const identity = loadAgentIdentity('/path/to/agent.md');

// Load agent identity by name (searches agents directory)
const identity2 = loadAgentIdentityByName('backend-dev');

// Validate identity structure
const validation = validateAgentIdentity(identity);
if (validation.valid) {
  console.log('Identity is valid');
} else {
  console.log('Errors:', validation.errors);
}
```

### Permission Checker (`permission-checker.js`)

- **Tool Whitelist Enforcement**: Does agent's role allow this tool?
- **Path Scope Enforcement**: Is file path within agent's allowed paths?
- **API Access Enforcement**: Does role permit this MCP call?
- **Budget Impact Calculation**: Estimate cost for operations
- **Approval Requirements**: Check if operation requires human approval
- **Performance**: <50ms per check (cached RBAC rules)

**Key Functions**:
```javascript
const {
  checkPermission,
  checkToolPermission,
  checkPathPermission,
  checkAPIPermission,
  validateRBACRules
} = require('./permission-checker');

// Comprehensive permission check
const result = checkPermission({
  role: 'developer',
  toolName: 'Read',
  filePath: 'src/api/users.js',
  apiName: 'github',
  estimatedTokens: 1000
});

if (result.allowed) {
  console.log('Permission granted');
  console.log('Budget impact:', result.budgetImpact);
  console.log('Requires approval:', result.requiresApproval);
} else {
  console.log('Permission denied:', result.reason);
}

// Check individual dimensions
const toolCheck = checkToolPermission('developer', 'Write');
const pathCheck = checkPathPermission('developer', 'src/api/users.js');
const apiCheck = checkAPIPermission('developer', 'github');
```

## RBAC Rules Structure

The system uses `agents/identity/agent-rbac-rules.json` defining 10 roles:

| Role | Level | Tools | Path Scopes | API Access |
|------|-------|-------|-------------|------------|
| admin | 10 | All (*) | All (**) | All (*) |
| developer | 8 | Read, Write, Edit, MultiEdit, Bash, Grep, Glob, Task, TodoWrite | src/**, tests/**, scripts/**, config/** | github, gitlab, memory-mcp |
| reviewer | 6 | Read, Grep, Glob, Task | All (**) | github, memory-mcp, connascence-analyzer |
| security | 7 | Read, Grep, Glob, Task, WebFetch | All (**) | github, memory-mcp, connascence-analyzer |
| database | 7 | Read, Write, Edit, Bash, Task | backend/**, database/**, migrations/**, schemas/** | memory-mcp |
| frontend | 6 | Read, Write, Edit, MultiEdit, Bash, Grep, Glob, Task | frontend/**, src/components/**, src/pages/**, public/**, styles/** | github, memory-mcp |
| backend | 7 | Read, Write, Edit, MultiEdit, Bash, Grep, Glob, Task | backend/**, src/api/**, src/services/**, src/models/**, tests/** | github, gitlab, memory-mcp |
| tester | 6 | Read, Write, Edit, Bash, Grep, Glob, Task | tests/**, e2e/**, **/*.test.*, **/*.spec.* | github, memory-mcp |
| analyst | 5 | Read, Grep, Glob, WebSearch, WebFetch | All (**) | github, memory-mcp |
| coordinator | 8 | Read, Grep, Glob, Task, TodoWrite | All (**) | memory-mcp, flow-nexus, ruv-swarm |

## Installation

```bash
cd hooks/12fa/utils
npm install
```

Dependencies:
- `js-yaml` (4.1.0) - YAML frontmatter parsing
- `minimatch` (9.0.3) - Path glob matching
- `jest` (29.7.0) - Testing framework

## Testing

```bash
# Run all tests with coverage
npm test

# Run specific test suites
npm run test:identity
npm run test:permissions

# Run performance benchmarks
npm run test:performance

# Watch mode (for development)
npm run test:watch
```

## Validation

Run the comprehensive validation script:

```bash
node validate-rbac-setup.js
```

This validates:
1. RBAC rules JSON structure (10 roles, all required fields)
2. All 207 agent identities (UUID format, role validity, frontmatter)
3. Performance benchmarks (<50ms per check)
4. Integration test (full workflow)

## Success Criteria

- [x] Identity verification works with all 207 agent frontmatter formats
- [x] Permission checker enforces all 3 dimensions (tools, paths, APIs)
- [x] Zero false positives (valid agents never blocked)
- [x] Zero false negatives (invalid operations always blocked)
- [x] Performance: <50ms per check (cached)
- [x] Windows compatible: No Unicode
- [x] Comprehensive unit tests (80%+ coverage)
- [x] RBAC rules JSON validation
- [x] Graceful error handling on validation failure

## License

MIT License - See LICENSE file in repository root
