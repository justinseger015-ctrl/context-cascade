/**
 * Ground Truth Validation
 * Phase 4.4 Architecture Optimization
 *
 * Replaces LLM consensus with deterministic test-based validation.
 * Validates code through execution, not through LLM voting.
 *
 * @module architecture/validation/ground-truth
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * Validation strategies
 */
const VALIDATION_STRATEGIES = {
  // Code validation through test execution
  test_execution: {
    id: 'test_execution',
    name: 'Test Execution',
    description: 'Run tests to validate code changes',
    deterministic: true,
    method: 'executeTests'
  },

  // Syntax validation through parsing
  syntax_check: {
    id: 'syntax_check',
    name: 'Syntax Check',
    description: 'Parse code to check syntax validity',
    deterministic: true,
    method: 'checkSyntax'
  },

  // Type checking
  type_check: {
    id: 'type_check',
    name: 'Type Check',
    description: 'Run type checker (TypeScript, mypy)',
    deterministic: true,
    method: 'checkTypes'
  },

  // Linting
  lint: {
    id: 'lint',
    name: 'Lint',
    description: 'Run linter for code quality',
    deterministic: true,
    method: 'runLint'
  },

  // Hash comparison
  hash_compare: {
    id: 'hash_compare',
    name: 'Hash Comparison',
    description: 'Compare file hashes for integrity',
    deterministic: true,
    method: 'compareHashes'
  },

  // Output comparison
  output_compare: {
    id: 'output_compare',
    name: 'Output Comparison',
    description: 'Compare actual vs expected output',
    deterministic: true,
    method: 'compareOutputs'
  }
};

/**
 * Execute tests and return results
 * @param {string} testCommand - Test command to run
 * @param {Object} options - Options
 * @returns {Promise<Object>} Test results
 */
async function executeTests(testCommand, options = {}) {
  const cwd = options.cwd || process.cwd();
  const timeout = options.timeout || 300000;

  return new Promise((resolve) => {
    const startTime = Date.now();

    exec(testCommand, { cwd, timeout }, (error, stdout, stderr) => {
      const duration = Date.now() - startTime;

      // Parse test output for counts
      const passMatch = stdout.match(/(\d+)\s*(passing|passed|pass)/i);
      const failMatch = stdout.match(/(\d+)\s*(failing|failed|fail)/i);

      resolve({
        valid: !error,
        strategy: 'test_execution',
        deterministic: true,
        passed: !error,
        testsPassed: passMatch ? parseInt(passMatch[1]) : 0,
        testsFailed: failMatch ? parseInt(failMatch[1]) : 0,
        duration,
        exitCode: error ? error.code : 0,
        stdout: stdout.slice(0, 5000),
        stderr: stderr.slice(0, 2000)
      });
    });
  });
}

/**
 * Check syntax validity
 * @param {string} filePath - File to check
 * @param {string} language - Programming language
 * @returns {Promise<Object>} Syntax check result
 */
async function checkSyntax(filePath, language = 'javascript') {
  const commands = {
    javascript: `node --check "${filePath}"`,
    typescript: `npx tsc --noEmit "${filePath}"`,
    python: `python -m py_compile "${filePath}"`,
    json: `node -e "JSON.parse(require('fs').readFileSync('${filePath}', 'utf8'))"`
  };

  const command = commands[language];
  if (!command) {
    return { valid: false, error: `Unknown language: ${language}` };
  }

  return new Promise((resolve) => {
    exec(command, { timeout: 30000 }, (error, stdout, stderr) => {
      resolve({
        valid: !error,
        strategy: 'syntax_check',
        deterministic: true,
        language,
        filePath,
        error: error ? stderr || error.message : null
      });
    });
  });
}

/**
 * Run type checker
 * @param {string} target - File or directory
 * @param {string} checker - Type checker to use
 * @returns {Promise<Object>} Type check result
 */
async function checkTypes(target, checker = 'tsc') {
  const commands = {
    tsc: `npx tsc --noEmit ${target}`,
    mypy: `mypy ${target}`,
    pyright: `pyright ${target}`
  };

  const command = commands[checker];
  if (!command) {
    return { valid: false, error: `Unknown checker: ${checker}` };
  }

  return new Promise((resolve) => {
    exec(command, { timeout: 120000 }, (error, stdout, stderr) => {
      // Count errors
      const errorCount = (stdout + stderr).match(/error/gi)?.length || 0;

      resolve({
        valid: !error && errorCount === 0,
        strategy: 'type_check',
        deterministic: true,
        checker,
        errorCount,
        output: (stdout + stderr).slice(0, 3000)
      });
    });
  });
}

/**
 * Run linter
 * @param {string} target - File or directory
 * @param {string} linter - Linter to use
 * @returns {Promise<Object>} Lint result
 */
async function runLint(target, linter = 'eslint') {
  const commands = {
    eslint: `npx eslint ${target} --format json`,
    pylint: `pylint ${target} --output-format=json`,
    flake8: `flake8 ${target}`
  };

  const command = commands[linter];
  if (!command) {
    return { valid: false, error: `Unknown linter: ${linter}` };
  }

  return new Promise((resolve) => {
    exec(command, { timeout: 120000 }, (error, stdout, stderr) => {
      let errorCount = 0;
      let warningCount = 0;

      try {
        if (linter === 'eslint' && stdout) {
          const results = JSON.parse(stdout);
          for (const file of results) {
            errorCount += file.errorCount || 0;
            warningCount += file.warningCount || 0;
          }
        }
      } catch (e) {
        // Non-JSON output, count by regex
        errorCount = (stdout + stderr).match(/error/gi)?.length || 0;
        warningCount = (stdout + stderr).match(/warning/gi)?.length || 0;
      }

      resolve({
        valid: errorCount === 0,
        strategy: 'lint',
        deterministic: true,
        linter,
        errorCount,
        warningCount,
        output: (stdout + stderr).slice(0, 3000)
      });
    });
  });
}

/**
 * Compare file hashes
 * @param {string} filePath - File to check
 * @param {string} expectedHash - Expected hash
 * @returns {Object} Hash comparison result
 */
function compareHashes(filePath, expectedHash) {
  try {
    const content = fs.readFileSync(filePath);
    const actualHash = crypto.createHash('sha256').update(content).digest('hex');

    return {
      valid: actualHash === expectedHash,
      strategy: 'hash_compare',
      deterministic: true,
      filePath,
      expectedHash,
      actualHash,
      match: actualHash === expectedHash
    };
  } catch (err) {
    return {
      valid: false,
      strategy: 'hash_compare',
      deterministic: true,
      error: err.message
    };
  }
}

/**
 * Compare outputs
 * @param {*} actual - Actual output
 * @param {*} expected - Expected output
 * @param {Object} options - Comparison options
 * @returns {Object} Comparison result
 */
function compareOutputs(actual, expected, options = {}) {
  const strict = options.strict !== false;
  const ignoreWhitespace = options.ignoreWhitespace || false;

  let actualStr = typeof actual === 'string' ? actual : JSON.stringify(actual);
  let expectedStr = typeof expected === 'string' ? expected : JSON.stringify(expected);

  if (ignoreWhitespace) {
    actualStr = actualStr.replace(/\s+/g, ' ').trim();
    expectedStr = expectedStr.replace(/\s+/g, ' ').trim();
  }

  const match = strict ? actualStr === expectedStr : actualStr.includes(expectedStr);

  return {
    valid: match,
    strategy: 'output_compare',
    deterministic: true,
    match,
    actualLength: actualStr.length,
    expectedLength: expectedStr.length
  };
}

/**
 * Run comprehensive validation suite
 * @param {Object} target - What to validate
 * @param {string[]} strategies - Strategies to use
 * @returns {Promise<Object>} Validation results
 */
async function validateComprehensive(target, strategies = ['test_execution', 'syntax_check', 'lint']) {
  const results = {
    timestamp: new Date().toISOString(),
    target,
    strategies: [],
    allPassed: true,
    summary: {}
  };

  for (const strategyId of strategies) {
    const strategy = VALIDATION_STRATEGIES[strategyId];
    if (!strategy) continue;

    let result;

    switch (strategy.method) {
      case 'executeTests':
        result = await executeTests(target.testCommand || 'npm test', target);
        break;
      case 'checkSyntax':
        result = await checkSyntax(target.filePath, target.language);
        break;
      case 'checkTypes':
        result = await checkTypes(target.filePath || '.', target.checker);
        break;
      case 'runLint':
        result = await runLint(target.filePath || '.', target.linter);
        break;
      case 'compareHashes':
        result = compareHashes(target.filePath, target.expectedHash);
        break;
      case 'compareOutputs':
        result = compareOutputs(target.actual, target.expected, target.options);
        break;
      default:
        result = { valid: false, error: 'Unknown method' };
    }

    results.strategies.push({
      id: strategyId,
      name: strategy.name,
      ...result
    });

    if (!result.valid) {
      results.allPassed = false;
    }
  }

  results.summary = {
    total: results.strategies.length,
    passed: results.strategies.filter(s => s.valid).length,
    failed: results.strategies.filter(s => !s.valid).length
  };

  return results;
}

/**
 * Validate code change with ground truth
 * @param {Object} change - Code change to validate
 * @returns {Promise<Object>} Validation result
 */
async function validateCodeChange(change) {
  const results = {
    changeId: change.id || crypto.randomBytes(8).toString('hex'),
    timestamp: new Date().toISOString(),
    validations: []
  };

  // 1. Syntax check for modified files
  if (change.files) {
    for (const file of change.files) {
      const ext = path.extname(file);
      const langMap = { '.js': 'javascript', '.ts': 'typescript', '.py': 'python', '.json': 'json' };
      const lang = langMap[ext];

      if (lang) {
        const syntaxResult = await checkSyntax(file, lang);
        results.validations.push(syntaxResult);
      }
    }
  }

  // 2. Run tests if specified
  if (change.testCommand) {
    const testResult = await executeTests(change.testCommand, { cwd: change.cwd });
    results.validations.push(testResult);
  }

  // 3. Type check if specified
  if (change.typeCheck) {
    const typeResult = await checkTypes(change.typeCheckTarget || '.', change.typeChecker);
    results.validations.push(typeResult);
  }

  // 4. Lint if specified
  if (change.lint) {
    const lintResult = await runLint(change.lintTarget || '.', change.linter);
    results.validations.push(lintResult);
  }

  // Summary
  results.allPassed = results.validations.every(v => v.valid);
  results.summary = {
    total: results.validations.length,
    passed: results.validations.filter(v => v.valid).length,
    failed: results.validations.filter(v => !v.valid).length
  };

  return results;
}

/**
 * Generate validation report
 * @param {Object} results - Validation results
 * @returns {string} Markdown report
 */
function generateValidationReport(results) {
  let report = `# Ground Truth Validation Report

**Timestamp**: ${results.timestamp}
**Status**: ${results.allPassed ? 'PASSED' : 'FAILED'}

## Summary

| Metric | Value |
|--------|-------|
| Total Validations | ${results.summary.total} |
| Passed | ${results.summary.passed} |
| Failed | ${results.summary.failed} |

## Validation Details

`;

  for (const validation of results.validations || results.strategies || []) {
    const status = validation.valid ? 'PASS' : 'FAIL';
    report += `### ${validation.name || validation.strategy} - ${status}

- **Strategy**: ${validation.strategy}
- **Deterministic**: ${validation.deterministic ? 'Yes' : 'No'}
`;

    if (validation.error) {
      report += `- **Error**: ${validation.error}\n`;
    }
    if (validation.testsPassed !== undefined) {
      report += `- **Tests Passed**: ${validation.testsPassed}\n`;
      report += `- **Tests Failed**: ${validation.testsFailed}\n`;
    }
    if (validation.errorCount !== undefined) {
      report += `- **Errors**: ${validation.errorCount}\n`;
    }

    report += '\n';
  }

  return report;
}

// Export
module.exports = {
  VALIDATION_STRATEGIES,
  executeTests,
  checkSyntax,
  checkTypes,
  runLint,
  compareHashes,
  compareOutputs,
  validateComprehensive,
  validateCodeChange,
  generateValidationReport
};
