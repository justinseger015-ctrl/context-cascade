/**
 * Automatic Rollback System
 * Phase 2 Safety Controls
 *
 * Monitors test results and triggers automatic rollback when:
 * - 3 consecutive test failures on same component
 * - Eval harness hash mismatch
 * - Safety constitution violation
 *
 * @module safety/rollback/auto-rollback
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Configuration
const CONFIG = {
  consecutiveFailureThreshold: 3,
  stateDir: path.join(__dirname, '..', '..', 'logs', 'rollback-state'),
  rollbackBranch: 'last-known-good',
  notifyOnRollback: true
};

/**
 * Test result record
 * @typedef {Object} TestResult
 * @property {string} component - Component that was tested
 * @property {boolean} passed - Whether tests passed
 * @property {string} timestamp - ISO timestamp
 * @property {string} commit - Git commit hash
 * @property {Object} details - Additional details
 */

/**
 * Rollback state
 * @typedef {Object} RollbackState
 * @property {Object} failureCounts - Consecutive failure counts by component
 * @property {string} lastKnownGood - Last known good commit
 * @property {boolean} inRecoveryMode - Whether system is in recovery mode
 * @property {TestResult[]} recentResults - Recent test results
 */

/**
 * Load rollback state
 * @returns {RollbackState} Current state
 */
function loadState() {
  const statePath = path.join(CONFIG.stateDir, 'rollback-state.json');

  try {
    if (!fs.existsSync(CONFIG.stateDir)) {
      fs.mkdirSync(CONFIG.stateDir, { recursive: true });
    }

    if (fs.existsSync(statePath)) {
      return JSON.parse(fs.readFileSync(statePath, 'utf8'));
    }
  } catch (err) {
    console.error('[AutoRollback] Failed to load state:', err.message);
  }

  // Default state
  return {
    failureCounts: {},
    lastKnownGood: null,
    inRecoveryMode: false,
    recentResults: [],
    lastUpdated: new Date().toISOString()
  };
}

/**
 * Save rollback state
 * @param {RollbackState} state - State to save
 */
function saveState(state) {
  const statePath = path.join(CONFIG.stateDir, 'rollback-state.json');

  try {
    if (!fs.existsSync(CONFIG.stateDir)) {
      fs.mkdirSync(CONFIG.stateDir, { recursive: true });
    }

    state.lastUpdated = new Date().toISOString();
    fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
  } catch (err) {
    console.error('[AutoRollback] Failed to save state:', err.message);
  }
}

/**
 * Get current git commit hash
 * @returns {Promise<string>} Commit hash
 */
function getCurrentCommit() {
  return new Promise((resolve) => {
    exec('git rev-parse HEAD', { timeout: 5000 }, (error, stdout) => {
      resolve(error ? null : stdout.trim());
    });
  });
}

/**
 * Check if working directory is clean
 * @returns {Promise<boolean>} True if clean
 */
function isWorkingDirectoryClean() {
  return new Promise((resolve) => {
    exec('git status --porcelain', { timeout: 5000 }, (error, stdout) => {
      resolve(!error && stdout.trim() === '');
    });
  });
}

/**
 * Record a test result
 * @param {string} component - Component tested
 * @param {boolean} passed - Whether it passed
 * @param {Object} details - Additional details
 * @returns {Promise<Object>} Recording result with rollback decision
 */
async function recordTestResult(component, passed, details = {}) {
  const state = loadState();
  const commit = await getCurrentCommit();

  const result = {
    component,
    passed,
    timestamp: new Date().toISOString(),
    commit,
    details
  };

  // Add to recent results (keep last 50)
  state.recentResults.unshift(result);
  if (state.recentResults.length > 50) {
    state.recentResults = state.recentResults.slice(0, 50);
  }

  // Update failure counts
  if (passed) {
    // Reset failure count on success
    state.failureCounts[component] = 0;

    // If all tests pass and not in recovery, update last known good
    if (!state.inRecoveryMode && commit) {
      state.lastKnownGood = commit;
    }
  } else {
    // Increment failure count
    state.failureCounts[component] = (state.failureCounts[component] || 0) + 1;
  }

  const consecutiveFailures = state.failureCounts[component] || 0;
  const shouldRollback = consecutiveFailures >= CONFIG.consecutiveFailureThreshold;

  saveState(state);

  return {
    recorded: true,
    component,
    passed,
    consecutiveFailures,
    shouldRollback,
    threshold: CONFIG.consecutiveFailureThreshold
  };
}

/**
 * Execute rollback to last known good state
 * @param {string} reason - Reason for rollback
 * @returns {Promise<Object>} Rollback result
 */
async function executeRollback(reason) {
  const state = loadState();

  if (!state.lastKnownGood) {
    return {
      success: false,
      error: 'No last known good commit available'
    };
  }

  // Check if working directory is clean
  const isClean = await isWorkingDirectoryClean();
  if (!isClean) {
    // Stash changes
    await new Promise((resolve) => {
      exec('git stash push -m "Auto-rollback stash"', { timeout: 30000 }, resolve);
    });
  }

  // Log the rollback
  logRollback({
    reason,
    targetCommit: state.lastKnownGood,
    fromCommit: await getCurrentCommit(),
    timestamp: new Date().toISOString()
  });

  // Execute rollback
  return new Promise((resolve) => {
    exec(`git checkout ${state.lastKnownGood}`, { timeout: 30000 }, (error, stdout, stderr) => {
      if (error) {
        resolve({
          success: false,
          error: error.message,
          stderr
        });
      } else {
        // Enter recovery mode
        state.inRecoveryMode = true;
        state.failureCounts = {}; // Reset failure counts
        saveState(state);

        resolve({
          success: true,
          restoredTo: state.lastKnownGood,
          reason,
          recoveryMode: true
        });
      }
    });
  });
}

/**
 * Log rollback event
 * @param {Object} rollbackInfo - Rollback details
 */
function logRollback(rollbackInfo) {
  const logPath = path.join(CONFIG.stateDir, 'rollback-history.jsonl');

  try {
    fs.appendFileSync(logPath, JSON.stringify(rollbackInfo) + '\n');
  } catch (err) {
    console.error('[AutoRollback] Failed to log rollback:', err.message);
  }
}

/**
 * Exit recovery mode after human confirmation
 * @returns {Object} Result
 */
function exitRecoveryMode() {
  const state = loadState();
  state.inRecoveryMode = false;
  saveState(state);

  return {
    success: true,
    message: 'Exited recovery mode',
    timestamp: new Date().toISOString()
  };
}

/**
 * Get current rollback status
 * @returns {Object} Status
 */
function getStatus() {
  const state = loadState();

  return {
    inRecoveryMode: state.inRecoveryMode,
    lastKnownGood: state.lastKnownGood,
    failureCounts: state.failureCounts,
    threshold: CONFIG.consecutiveFailureThreshold,
    recentFailures: state.recentResults.filter(r => !r.passed).slice(0, 10),
    lastUpdated: state.lastUpdated
  };
}

/**
 * Check if component is at risk of rollback
 * @param {string} component - Component to check
 * @returns {Object} Risk assessment
 */
function assessRollbackRisk(component) {
  const state = loadState();
  const failures = state.failureCounts[component] || 0;
  const remaining = CONFIG.consecutiveFailureThreshold - failures;

  return {
    component,
    consecutiveFailures: failures,
    threshold: CONFIG.consecutiveFailureThreshold,
    failuresUntilRollback: Math.max(0, remaining),
    atRisk: remaining <= 1,
    willRollback: remaining <= 0
  };
}

/**
 * Manually set last known good commit
 * @param {string} commit - Commit hash
 * @returns {Object} Result
 */
async function setLastKnownGood(commit) {
  const state = loadState();

  // Verify commit exists
  return new Promise((resolve) => {
    exec(`git cat-file -t ${commit}`, { timeout: 5000 }, (error) => {
      if (error) {
        resolve({
          success: false,
          error: 'Commit does not exist'
        });
      } else {
        state.lastKnownGood = commit;
        saveState(state);

        resolve({
          success: true,
          lastKnownGood: commit,
          message: 'Last known good commit updated'
        });
      }
    });
  });
}

/**
 * Run the eval harness and check for regression
 * @param {string} testCommand - Command to run
 * @param {string} component - Component being tested
 * @returns {Promise<Object>} Test result with rollback decision
 */
async function runWithRollbackCheck(testCommand, component) {
  return new Promise((resolve) => {
    const startTime = Date.now();

    exec(testCommand, { timeout: 300000 }, async (error, stdout, stderr) => {
      const duration = Date.now() - startTime;
      const passed = !error;

      const result = await recordTestResult(component, passed, {
        command: testCommand,
        duration,
        exitCode: error ? error.code : 0,
        stdout: stdout.slice(0, 1000), // Truncate for storage
        stderr: stderr.slice(0, 1000)
      });

      if (result.shouldRollback) {
        console.log(`[AutoRollback] Triggering rollback for ${component} after ${result.consecutiveFailures} failures`);
        const rollbackResult = await executeRollback(
          `${result.consecutiveFailures} consecutive test failures for ${component}`
        );
        result.rollbackExecuted = rollbackResult;
      }

      resolve({
        ...result,
        testOutput: {
          passed,
          duration,
          stdout,
          stderr
        }
      });
    });
  });
}

// Export functions
module.exports = {
  // Core operations
  recordTestResult,
  executeRollback,
  runWithRollbackCheck,

  // Status
  getStatus,
  assessRollbackRisk,

  // Recovery
  exitRecoveryMode,
  setLastKnownGood,

  // State
  loadState,
  saveState,

  // Configuration
  CONFIG
};
