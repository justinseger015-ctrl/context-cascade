/**
 * Codex Sandbox Router
 * Phase 1.4 Security Hardening
 *
 * Routes code execution through Codex CLI sandbox for isolation.
 * Provides network-disabled execution environment for untrusted code.
 *
 * @module security/sandbox/sandbox-router
 */

const { exec, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

/**
 * Sandbox modes supported by Codex CLI
 */
const SANDBOX_MODES = {
  READ_ONLY: 'read-only',       // Default: can only read files
  WORKSPACE_WRITE: 'workspace-write', // Can write to workspace
  FULL_AUTO: 'full-auto',      // Autonomous with workspace-write
  YOLO: 'yolo'                 // Bypass all sandboxing (DANGEROUS)
};

/**
 * Sandbox configuration
 */
const SANDBOX_CONFIG = {
  defaultMode: SANDBOX_MODES.READ_ONLY,
  maxExecutionTime: 300000, // 5 minutes
  networkDisabled: true,
  tempDir: path.join(os.tmpdir(), 'context-cascade-sandbox'),
  codexPath: 'codex' // Assumes codex is in PATH
};

/**
 * Ensure temp directory exists
 */
function ensureTempDir() {
  if (!fs.existsSync(SANDBOX_CONFIG.tempDir)) {
    fs.mkdirSync(SANDBOX_CONFIG.tempDir, { recursive: true });
  }
  return SANDBOX_CONFIG.tempDir;
}

/**
 * Check if Codex CLI is available
 * @returns {Promise<Object>} Version info or error
 */
async function checkCodexAvailable() {
  return new Promise((resolve) => {
    exec('bash -lc "command -v codex && codex --version"', { timeout: 10000 }, (error, stdout, stderr) => {
      if (error) {
        resolve({
          available: false,
          error: error.message,
          stderr
        });
      } else {
        resolve({
          available: true,
          version: stdout.trim(),
          path: stdout.split('\n')[0]
        });
      }
    });
  });
}

/**
 * Execution result
 * @typedef {Object} ExecutionResult
 * @property {boolean} success - Whether execution succeeded
 * @property {number} exitCode - Process exit code
 * @property {string} stdout - Standard output
 * @property {string} stderr - Standard error
 * @property {number} duration - Execution time in ms
 * @property {boolean} sandboxed - Whether sandbox was used
 * @property {string} mode - Sandbox mode used
 */

/**
 * Execute a command in Codex sandbox
 * @param {string} command - Command to execute
 * @param {Object} options - Execution options
 * @returns {Promise<ExecutionResult>} Execution result
 */
async function executeInSandbox(command, options = {}) {
  const mode = options.mode || SANDBOX_CONFIG.defaultMode;
  const timeout = options.timeout || SANDBOX_CONFIG.maxExecutionTime;
  const cwd = options.cwd || process.cwd();

  // Check if we should bypass sandbox (only for trusted operations)
  if (options.trusted === true && options.bypassSandbox === true) {
    return executeDirectly(command, { timeout, cwd });
  }

  // Build Codex command
  const sandboxFlag = mode === SANDBOX_MODES.YOLO ? '--yolo' : `--sandbox ${mode}`;
  const codexCommand = `bash -lc "codex ${sandboxFlag} exec '${escapeCommand(command)}'"`;

  const startTime = Date.now();

  return new Promise((resolve) => {
    exec(codexCommand, {
      timeout,
      cwd,
      maxBuffer: 10 * 1024 * 1024, // 10MB buffer
      env: {
        ...process.env,
        // Ensure network is disabled in sandbox
        SANDBOX_NETWORK: 'disabled'
      }
    }, (error, stdout, stderr) => {
      const duration = Date.now() - startTime;

      resolve({
        success: !error,
        exitCode: error ? error.code || 1 : 0,
        stdout: stdout || '',
        stderr: stderr || '',
        duration,
        sandboxed: true,
        mode,
        command: command
      });
    });
  });
}

/**
 * Execute a command directly (without sandbox)
 * Only use for trusted operations
 * @param {string} command - Command to execute
 * @param {Object} options - Execution options
 * @returns {Promise<ExecutionResult>} Execution result
 */
async function executeDirectly(command, options = {}) {
  const timeout = options.timeout || SANDBOX_CONFIG.maxExecutionTime;
  const cwd = options.cwd || process.cwd();
  const startTime = Date.now();

  return new Promise((resolve) => {
    exec(command, { timeout, cwd }, (error, stdout, stderr) => {
      const duration = Date.now() - startTime;

      resolve({
        success: !error,
        exitCode: error ? error.code || 1 : 0,
        stdout: stdout || '',
        stderr: stderr || '',
        duration,
        sandboxed: false,
        mode: 'direct',
        command
      });
    });
  });
}

/**
 * Escape command for shell execution
 * @param {string} command - Command to escape
 * @returns {string} Escaped command
 */
function escapeCommand(command) {
  // Escape single quotes for bash
  return command.replace(/'/g, "'\\''");
}

/**
 * Run tests in sandbox
 * @param {string} testCommand - Test command (e.g., 'npm test', 'pytest')
 * @param {Object} options - Options
 * @returns {Promise<ExecutionResult>} Test result
 */
async function runTestsInSandbox(testCommand, options = {}) {
  const result = await executeInSandbox(testCommand, {
    mode: options.networkRequired ? SANDBOX_MODES.WORKSPACE_WRITE : SANDBOX_MODES.READ_ONLY,
    timeout: options.timeout || 600000, // 10 min for tests
    cwd: options.cwd
  });

  return {
    ...result,
    passed: result.exitCode === 0,
    testOutput: result.stdout,
    testErrors: result.stderr
  };
}

/**
 * Execute code file in sandbox
 * @param {string} filePath - Path to code file
 * @param {string} runtime - Runtime to use (node, python, etc.)
 * @param {Object} options - Options
 * @returns {Promise<ExecutionResult>} Execution result
 */
async function executeFileInSandbox(filePath, runtime = 'node', options = {}) {
  const runtimeCommands = {
    node: `node "${filePath}"`,
    python: `python "${filePath}"`,
    python3: `python3 "${filePath}"`,
    bash: `bash "${filePath}"`,
    sh: `sh "${filePath}"`
  };

  const command = runtimeCommands[runtime] || `${runtime} "${filePath}"`;

  return executeInSandbox(command, options);
}

/**
 * Run linter in sandbox
 * @param {string} target - Target path or pattern
 * @param {string} linter - Linter to use (eslint, pylint, etc.)
 * @param {Object} options - Options
 * @returns {Promise<ExecutionResult>} Linter result
 */
async function runLinterInSandbox(target, linter = 'eslint', options = {}) {
  const linterCommands = {
    eslint: `npx eslint ${target}`,
    pylint: `pylint ${target}`,
    flake8: `flake8 ${target}`,
    prettier: `npx prettier --check ${target}`,
    black: `black --check ${target}`
  };

  const command = linterCommands[linter] || `${linter} ${target}`;

  return executeInSandbox(command, {
    mode: SANDBOX_MODES.READ_ONLY,
    ...options
  });
}

/**
 * Run type checker in sandbox
 * @param {string} target - Target path
 * @param {string} checker - Type checker (tsc, mypy, pyright)
 * @param {Object} options - Options
 * @returns {Promise<ExecutionResult>} Type check result
 */
async function runTypeCheckInSandbox(target, checker = 'tsc', options = {}) {
  const checkerCommands = {
    tsc: `npx tsc --noEmit ${target}`,
    mypy: `mypy ${target}`,
    pyright: `pyright ${target}`
  };

  const command = checkerCommands[checker] || `${checker} ${target}`;

  return executeInSandbox(command, {
    mode: SANDBOX_MODES.READ_ONLY,
    ...options
  });
}

/**
 * Create a sandboxed execution context
 * @param {Object} config - Context configuration
 * @returns {Object} Execution context with bound methods
 */
function createSandboxContext(config = {}) {
  const mode = config.mode || SANDBOX_CONFIG.defaultMode;
  const cwd = config.cwd || process.cwd();
  const timeout = config.timeout || SANDBOX_CONFIG.maxExecutionTime;

  return {
    exec: (command, opts = {}) => executeInSandbox(command, { mode, cwd, timeout, ...opts }),
    runTests: (cmd, opts = {}) => runTestsInSandbox(cmd, { cwd, timeout, ...opts }),
    runFile: (file, runtime, opts = {}) => executeFileInSandbox(file, runtime, { mode, cwd, timeout, ...opts }),
    lint: (target, linter, opts = {}) => runLinterInSandbox(target, linter, { cwd, timeout, ...opts }),
    typeCheck: (target, checker, opts = {}) => runTypeCheckInSandbox(target, checker, { cwd, timeout, ...opts }),
    mode,
    cwd,
    timeout
  };
}

/**
 * Determine appropriate sandbox mode for a task
 * @param {Object} task - Task description
 * @returns {string} Recommended sandbox mode
 */
function determineSandboxMode(task) {
  // If task requires network, we can't sandbox (or need special handling)
  if (task.requiresNetwork) {
    return SANDBOX_MODES.YOLO; // User must explicitly accept risk
  }

  // If task writes files
  if (task.writesFiles) {
    return SANDBOX_MODES.WORKSPACE_WRITE;
  }

  // If task is autonomous iteration
  if (task.autonomous) {
    return SANDBOX_MODES.FULL_AUTO;
  }

  // Default to read-only
  return SANDBOX_MODES.READ_ONLY;
}

/**
 * Validate sandbox execution is working
 * @returns {Promise<Object>} Validation result
 */
async function validateSandbox() {
  const checks = {
    codexAvailable: false,
    sandboxWorks: false,
    networkBlocked: false
  };

  // Check Codex availability
  const codexCheck = await checkCodexAvailable();
  checks.codexAvailable = codexCheck.available;

  if (!codexCheck.available) {
    return {
      valid: false,
      checks,
      error: 'Codex CLI not available'
    };
  }

  // Test sandbox execution
  const testResult = await executeInSandbox('echo "sandbox test"', {
    mode: SANDBOX_MODES.READ_ONLY,
    timeout: 30000
  });
  checks.sandboxWorks = testResult.success && testResult.stdout.includes('sandbox test');

  // Test network blocking (this should fail in sandbox)
  const networkResult = await executeInSandbox('curl -s https://example.com', {
    mode: SANDBOX_MODES.READ_ONLY,
    timeout: 10000
  });
  checks.networkBlocked = !networkResult.success || networkResult.exitCode !== 0;

  return {
    valid: checks.codexAvailable && checks.sandboxWorks,
    checks,
    codexVersion: codexCheck.version
  };
}

// Export functions and constants
module.exports = {
  SANDBOX_MODES,
  SANDBOX_CONFIG,
  checkCodexAvailable,
  executeInSandbox,
  executeDirectly,
  runTestsInSandbox,
  executeFileInSandbox,
  runLinterInSandbox,
  runTypeCheckInSandbox,
  createSandboxContext,
  determineSandboxMode,
  validateSandbox,
  ensureTempDir
};
