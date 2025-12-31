# SYSTEM SAFETY CONSTITUTION

**Version**: 1.0.0
**Status**: IMMUTABLE - This file MUST NOT be modified by automated processes
**Hash**: Will be computed and sealed by safety-guardian

---

## PREAMBLE

This constitution defines inviolable safety rules for the Context Cascade system.
No agent, meta-loop, or automated process may modify these rules.
Modifications require:
1. Human approval via signed commit
2. Explicit user confirmation
3. New hash seal generation

---

## ARTICLE I: EMERGENCY STOP

### Section 1.1: Kill Switch Mechanisms
The system SHALL provide multiple emergency stop mechanisms:

a) **File-based Kill Switch**
   - Creating `.meta-loop-stop` in working directory halts all operations
   - Creating `~/.meta-loop-stop` in home directory halts all operations
   - Response time: < 1 second

b) **Environment Variable Kill Switch**
   - Setting `META_LOOP_EMERGENCY_STOP=true` halts all operations
   - Alternative values: `1`, `yes`, `halt`, `stop`
   - Response time: < 1 second

c) **API Kill Switch**
   - POST to `/api/emergency-stop` with valid admin token
   - Response time: < 1 second

### Section 1.2: Kill Switch Behavior
When any kill switch is activated:
- All running agents MUST terminate immediately
- No new operations may be started
- State must be preserved for forensic analysis
- Human notification must be sent if configured

---

## ARTICLE II: HUMAN OVERSIGHT

### Section 2.1: Approval Requirements
The following operations REQUIRE human approval:

a) **Always Require Approval**
   - Modifications to this safety constitution
   - Changes to RBAC rules that grant elevated permissions
   - Deployment to production environments
   - Deletion of data or code repositories
   - Network requests to new external endpoints

b) **Require Approval Above Threshold**
   - Token expenditure > $10 per session
   - File modifications > 100 files
   - Consecutive autonomous iterations > 10

### Section 2.2: Approval Mechanisms
Valid approval mechanisms:
- Interactive terminal confirmation (y/n prompt)
- Signed git commit by authorized user
- API confirmation with admin token
- Time-limited approval token (max 24 hours)

---

## ARTICLE III: SELF-MODIFICATION LIMITS

### Section 3.1: Immutable Components
The following components are IMMUTABLE and cannot be modified by any automated process:

a) **Safety Files**
   - `safety/constitution/SYSTEM-SAFETY.md` (this file)
   - `safety/constitution/hash-seal.json`
   - `safety/guardian/safety-guardian.cjs`

b) **Eval Harness**
   - `cognitive-architecture/improvement-pipeline/eval-harness/` (entire directory)
   - Verified by cryptographic hash before each use

c) **Kill Switch Code**
   - `cognitive-architecture/loopctl/core.py:check_emergency_stop()`
   - Function signature and core logic immutable

### Section 3.2: Modification Audit Trail
All modifications to non-immutable system files MUST:
- Be logged with timestamp, agent ID, and file path
- Include before/after hash
- Be reversible via git history
- Trigger notification if modifying sensitive paths

---

## ARTICLE IV: RESOURCE LIMITS

### Section 4.1: Token Budget
- Maximum tokens per session: 500,000 (configurable per role)
- Maximum cost per day: $100 (configurable)
- Budget exceeded: Graceful shutdown, no forced completion

### Section 4.2: Iteration Limits
- Maximum autonomous iterations: 100
- Maximum recursion depth: 10
- Maximum concurrent agents: 20
- Limits exceeded: Pause and request human guidance

### Section 4.3: Time Limits
- Maximum single operation: 10 minutes
- Maximum session duration: 8 hours
- Operation timeout: Graceful abort with state preservation

---

## ARTICLE V: ROLLBACK AND RECOVERY

### Section 5.1: Automatic Rollback Triggers
System SHALL automatically rollback when:
- 3 consecutive test failures on same component
- Eval harness hash mismatch detected
- Safety constitution modification attempted
- Kill switch activated

### Section 5.2: Rollback Procedure
1. Stop all active operations
2. Preserve current state for analysis
3. Restore last known-good state from git
4. Verify restored state passes eval harness
5. Notify human of rollback and reason

### Section 5.3: Recovery Mode
After rollback, system enters recovery mode:
- Reduced autonomy (human approval for all actions)
- Enhanced logging
- Remains in recovery until human confirms resolution

---

## ARTICLE VI: AUDIT AND TRANSPARENCY

### Section 6.1: Mandatory Logging
The following MUST be logged:
- All tool invocations with parameters
- All file modifications
- All agent spawns and terminations
- All approval requests and responses
- All kill switch activations
- All budget threshold crossings

### Section 6.2: Log Integrity
- Logs are append-only
- Log files protected from agent modification
- Logs include cryptographic chain for tamper detection

### Section 6.3: Transparency Reports
System SHALL generate:
- Session summary after each autonomous session
- Daily activity digest
- Weekly safety audit report

---

## ARTICLE VII: ENFORCEMENT

### Section 7.1: Safety Guardian
The Safety Guardian (`safety/guardian/safety-guardian.cjs`) SHALL:
- Run before every autonomous operation
- Verify constitution hash integrity
- Check all immutable file hashes
- Enforce approval requirements
- Block operations that violate this constitution

### Section 7.2: Violation Response
Upon detecting constitution violation:
1. Immediately halt offending operation
2. Log violation with full context
3. Activate kill switch
4. Notify human
5. Enter recovery mode

### Section 7.3: No Override
There is NO mechanism to override this constitution from within the system.
Override requires direct human intervention with signed commit.

---

## SIGNATURES

This constitution is sealed and verified by:
- SHA-256 hash stored in `safety/constitution/hash-seal.json`
- Git commit signature
- Human approval record

**Effective Date**: 2025-12-31
**Last Human Review**: 2025-12-31

---

*This document follows the principle: "Safety rules that can be modified by the system they govern provide no safety."*
