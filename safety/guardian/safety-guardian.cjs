/**
 * Safety Guardian
 * Phase 2 Safety Controls
 *
 * Enforces the System Safety Constitution by:
 * - Verifying immutable file hashes
 * - Blocking unauthorized modifications
 * - Enforcing approval requirements
 * - Triggering rollback on violations
 *
 * @module safety/guardian/safety-guardian
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Paths relative to project root
const PROJECT_ROOT = path.join(__dirname, '..', '..');
const CONSTITUTION_PATH = path.join(__dirname, '..', 'constitution', 'SYSTEM-SAFETY.md');
const HASH_SEAL_PATH = path.join(__dirname, '..', 'constitution', 'hash-seal.json');
const LOOPCTL_PATH = path.join(PROJECT_ROOT, 'cognitive-architecture', 'loopctl', 'core.py');
const EVAL_HARNESS_DIR = path.join(PROJECT_ROOT, 'cognitive-architecture', 'improvement-pipeline', 'eval-harness');

/**
 * Immutable paths that cannot be modified by automated processes
 */
const IMMUTABLE_PATHS = [
  'safety/constitution/SYSTEM-SAFETY.md',
  'safety/constitution/hash-seal.json',
  'safety/guardian/safety-guardian.cjs'
];

/**
 * Paths requiring human approval to modify
 */
const APPROVAL_REQUIRED_PATHS = [
  'agents/identity/agent-rbac-rules.json',
  '.mcp.json',
  'cognitive-architecture/loopctl/core.py'
];

/**
 * Calculate SHA-256 hash of a file
 * @param {string} filePath - Path to file
 * @returns {string} Hex hash
 */
function hashFile(filePath) {
  try {
    const content = fs.readFileSync(filePath);
    return crypto.createHash('sha256').update(content).digest('hex');
  } catch (err) {
    return null;
  }
}

/**
 * Calculate hash of entire directory
 * @param {string} dirPath - Path to directory
 * @returns {string} Combined hash
 */
function hashDirectory(dirPath) {
  const hash = crypto.createHash('sha256');
  const files = [];

  function walkDir(dir) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (entry.name !== 'node_modules' && entry.name !== '.git') {
            walkDir(fullPath);
          }
        } else if (entry.isFile()) {
          files.push(fullPath);
        }
      }
    } catch (err) {
      // Directory doesn't exist
    }
  }

  walkDir(dirPath);
  files.sort();

  for (const file of files) {
    const relativePath = path.relative(dirPath, file);
    const content = fs.readFileSync(file);
    hash.update(relativePath);
    hash.update(content);
  }

  return hash.digest('hex');
}

/**
 * Load the hash seal registry
 * @returns {Object} Hash seal data
 */
function loadHashSeal() {
  try {
    if (fs.existsSync(HASH_SEAL_PATH)) {
      return JSON.parse(fs.readFileSync(HASH_SEAL_PATH, 'utf8'));
    }
  } catch (err) {
    console.error('[Safety Guardian] Failed to load hash seal:', err.message);
  }
  return null;
}

/**
 * Save the hash seal registry
 * @param {Object} seal - Seal data
 */
function saveHashSeal(seal) {
  seal.lastUpdated = new Date().toISOString();
  fs.writeFileSync(HASH_SEAL_PATH, JSON.stringify(seal, null, 2));
}

/**
 * Generate initial hash seal for all immutable files
 * @returns {Object} Seal data
 */
function generateHashSeal() {
  const seal = {
    version: '1.0.0',
    generatedAt: new Date().toISOString(),
    generatedBy: 'safety-guardian',
    files: {},
    directories: {}
  };

  // Hash immutable files
  for (const relativePath of IMMUTABLE_PATHS) {
    const fullPath = path.join(PROJECT_ROOT, relativePath);
    const hash = hashFile(fullPath);
    if (hash) {
      seal.files[relativePath] = {
        hash,
        size: fs.statSync(fullPath).size,
        sealedAt: new Date().toISOString()
      };
    }
  }

  // Hash eval harness directory
  if (fs.existsSync(EVAL_HARNESS_DIR)) {
    seal.directories['cognitive-architecture/improvement-pipeline/eval-harness'] = {
      hash: hashDirectory(EVAL_HARNESS_DIR),
      sealedAt: new Date().toISOString()
    };
  }

  // Hash constitution
  seal.constitutionHash = hashFile(CONSTITUTION_PATH);

  saveHashSeal(seal);
  return seal;
}

/**
 * Verification result
 * @typedef {Object} VerificationResult
 * @property {boolean} valid - Overall validity
 * @property {Object[]} violations - List of violations
 * @property {Object} checked - Files/dirs checked
 */

/**
 * Verify all immutable files against sealed hashes
 * @returns {VerificationResult} Verification result
 */
function verifyIntegrity() {
  const seal = loadHashSeal();

  if (!seal) {
    return {
      valid: false,
      violations: [{ type: 'SEAL_MISSING', message: 'Hash seal not found - run generateHashSeal()' }],
      checked: {}
    };
  }

  const result = {
    valid: true,
    violations: [],
    checked: {
      files: [],
      directories: []
    }
  };

  // Verify files
  for (const [relativePath, expected] of Object.entries(seal.files)) {
    const fullPath = path.join(PROJECT_ROOT, relativePath);
    const currentHash = hashFile(fullPath);

    result.checked.files.push(relativePath);

    if (!currentHash) {
      result.valid = false;
      result.violations.push({
        type: 'FILE_MISSING',
        path: relativePath,
        message: `Immutable file missing: ${relativePath}`
      });
    } else if (currentHash !== expected.hash) {
      result.valid = false;
      result.violations.push({
        type: 'FILE_TAMPERED',
        path: relativePath,
        expected: expected.hash,
        actual: currentHash,
        message: `Immutable file modified: ${relativePath}`
      });
    }
  }

  // Verify directories
  for (const [relativePath, expected] of Object.entries(seal.directories || {})) {
    const fullPath = path.join(PROJECT_ROOT, relativePath);
    const currentHash = hashDirectory(fullPath);

    result.checked.directories.push(relativePath);

    if (currentHash !== expected.hash) {
      result.valid = false;
      result.violations.push({
        type: 'DIRECTORY_TAMPERED',
        path: relativePath,
        expected: expected.hash,
        actual: currentHash,
        message: `Immutable directory modified: ${relativePath}`
      });
    }
  }

  return result;
}

/**
 * Check if a path modification requires approval
 * @param {string} targetPath - Path to check
 * @returns {Object} Approval requirement
 */
function checkApprovalRequired(targetPath) {
  const normalizedPath = targetPath.replace(/\\/g, '/');

  // Check if path is immutable
  for (const immutable of IMMUTABLE_PATHS) {
    if (normalizedPath.includes(immutable)) {
      return {
        allowed: false,
        reason: 'IMMUTABLE_PATH',
        message: `Path is immutable and cannot be modified: ${immutable}`
      };
    }
  }

  // Check if path requires approval
  for (const approvalPath of APPROVAL_REQUIRED_PATHS) {
    if (normalizedPath.includes(approvalPath)) {
      return {
        allowed: false,
        requiresApproval: true,
        reason: 'APPROVAL_REQUIRED',
        message: `Modification requires human approval: ${approvalPath}`
      };
    }
  }

  return {
    allowed: true,
    reason: 'PATH_ALLOWED',
    message: 'Path can be modified'
  };
}

/**
 * Pre-operation safety check
 * @param {string} operation - Operation type (read, write, delete, execute)
 * @param {Object} params - Operation parameters
 * @returns {Object} Safety check result
 */
function preOperationCheck(operation, params = {}) {
  const result = {
    allowed: true,
    checks: [],
    violations: []
  };

  // Check 1: Verify constitution integrity
  const integrity = verifyIntegrity();
  result.checks.push('constitution_integrity');

  if (!integrity.valid) {
    result.allowed = false;
    result.violations.push(...integrity.violations);
    return result;
  }

  // Check 2: For write operations, verify path is not immutable
  if (operation === 'write' || operation === 'delete') {
    const pathCheck = checkApprovalRequired(params.path || params.file_path || '');
    result.checks.push('path_permission');

    if (!pathCheck.allowed) {
      result.allowed = false;
      result.violations.push({
        type: pathCheck.reason,
        path: params.path || params.file_path,
        message: pathCheck.message,
        requiresApproval: pathCheck.requiresApproval
      });
    }
  }

  // Check 3: Verify kill switch not active
  result.checks.push('kill_switch');
  const killSwitchActive = checkKillSwitch();

  if (killSwitchActive.active) {
    result.allowed = false;
    result.violations.push({
      type: 'KILL_SWITCH_ACTIVE',
      message: killSwitchActive.reason
    });
  }

  return result;
}

/**
 * Check if kill switch is active
 * @returns {Object} Kill switch status
 */
function checkKillSwitch() {
  // File-based kill switch - current directory
  if (fs.existsSync(path.join(process.cwd(), '.meta-loop-stop'))) {
    return { active: true, reason: 'Kill switch file in current directory' };
  }

  // File-based kill switch - home directory
  const homeStop = path.join(require('os').homedir(), '.meta-loop-stop');
  if (fs.existsSync(homeStop)) {
    return { active: true, reason: 'Kill switch file in home directory' };
  }

  // Environment variable
  const envStop = (process.env.META_LOOP_EMERGENCY_STOP || '').toLowerCase();
  if (['true', '1', 'yes', 'halt', 'stop'].includes(envStop)) {
    return { active: true, reason: 'META_LOOP_EMERGENCY_STOP environment variable set' };
  }

  return { active: false };
}

/**
 * Record a safety violation in the audit log
 * @param {Object} violation - Violation details
 */
function logViolation(violation) {
  const logPath = path.join(PROJECT_ROOT, 'logs', 'safety-violations.jsonl');
  const logDir = path.dirname(logPath);

  try {
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }

    const entry = {
      timestamp: new Date().toISOString(),
      ...violation
    };

    fs.appendFileSync(logPath, JSON.stringify(entry) + '\n');
  } catch (err) {
    console.error('[Safety Guardian] Failed to log violation:', err.message);
  }
}

/**
 * Trigger emergency response
 * @param {string} reason - Reason for emergency
 * @returns {Object} Response result
 */
function triggerEmergencyResponse(reason) {
  // Log the emergency
  logViolation({
    type: 'EMERGENCY_TRIGGERED',
    reason,
    action: 'System entering emergency mode'
  });

  // Create kill switch file
  const killSwitchPath = path.join(process.cwd(), '.meta-loop-stop');
  try {
    fs.writeFileSync(killSwitchPath, `EMERGENCY: ${reason}\nTriggered: ${new Date().toISOString()}\n`);
  } catch (err) {
    console.error('[Safety Guardian] Failed to create kill switch file:', err.message);
  }

  return {
    success: true,
    action: 'emergency_mode_activated',
    reason,
    killSwitchCreated: fs.existsSync(killSwitchPath)
  };
}

/**
 * Audit the safety system status
 * @returns {Object} Audit results
 */
async function auditSafetySystem() {
  const results = {
    timestamp: new Date().toISOString(),
    status: 'HEALTHY',
    checks: {}
  };

  // Check 1: Constitution exists
  results.checks.constitutionExists = fs.existsSync(CONSTITUTION_PATH);

  // Check 2: Hash seal exists
  results.checks.hashSealExists = fs.existsSync(HASH_SEAL_PATH);

  // Check 3: Integrity verification
  const integrity = verifyIntegrity();
  results.checks.integrityValid = integrity.valid;
  results.checks.integrityViolations = integrity.violations;

  // Check 4: Kill switch status
  const killSwitch = checkKillSwitch();
  results.checks.killSwitchActive = killSwitch.active;

  // Check 5: Safety guardian is sealed
  const seal = loadHashSeal();
  if (seal && seal.files['safety/guardian/safety-guardian.cjs']) {
    const currentHash = hashFile(__filename);
    results.checks.guardianSealed = currentHash === seal.files['safety/guardian/safety-guardian.cjs'].hash;
  } else {
    results.checks.guardianSealed = false;
  }

  // Determine overall status
  if (!results.checks.constitutionExists ||
      !results.checks.hashSealExists ||
      !results.checks.integrityValid ||
      results.checks.killSwitchActive) {
    results.status = 'UNHEALTHY';
  }

  return results;
}

// Export functions
module.exports = {
  // Hash operations
  hashFile,
  hashDirectory,
  generateHashSeal,
  loadHashSeal,

  // Verification
  verifyIntegrity,
  checkApprovalRequired,
  preOperationCheck,
  checkKillSwitch,

  // Emergency response
  logViolation,
  triggerEmergencyResponse,

  // Audit
  auditSafetySystem,

  // Constants
  IMMUTABLE_PATHS,
  APPROVAL_REQUIRED_PATHS
};
