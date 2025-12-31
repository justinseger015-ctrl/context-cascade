/**
 * Cross-Platform Compatibility
 * Phase 5.4 Quality Expansion
 *
 * Provides platform-agnostic path handling and environment detection.
 * Fixes hardcoded Windows paths for Linux/Mac compatibility.
 *
 * @module quality/platform/cross-platform
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * Platform detection
 */
const PLATFORM = {
  isWindows: process.platform === 'win32',
  isMac: process.platform === 'darwin',
  isLinux: process.platform === 'linux',
  name: process.platform,
  arch: process.arch,
  homeDir: os.homedir(),
  tempDir: os.tmpdir()
};

/**
 * Path utilities for cross-platform compatibility
 */
const PathUtils = {
  /**
   * Normalize path separators for current platform
   * @param {string} inputPath - Path to normalize
   * @returns {string} Normalized path
   */
  normalize(inputPath) {
    if (!inputPath) return inputPath;

    // Convert Windows paths to Unix on non-Windows
    if (!PLATFORM.isWindows) {
      // Handle C:\Users\... style paths
      inputPath = inputPath.replace(/^[A-Z]:\\/i, '/');
      inputPath = inputPath.replace(/\\/g, '/');
    }

    return path.normalize(inputPath);
  },

  /**
   * Convert Windows-style path to platform-appropriate path
   * @param {string} windowsPath - Windows-style path
   * @returns {string} Platform-appropriate path
   */
  fromWindows(windowsPath) {
    if (!windowsPath) return windowsPath;

    if (PLATFORM.isWindows) {
      return windowsPath;
    }

    // Convert drive letter to /mnt/c or just /
    let converted = windowsPath;

    // C:\Users\username -> /home/username (Linux) or /Users/username (Mac)
    const userMatch = windowsPath.match(/^[A-Z]:\\Users\\([^\\]+)(.*)/i);
    if (userMatch) {
      const username = userMatch[1];
      const rest = userMatch[2].replace(/\\/g, '/');
      if (PLATFORM.isMac) {
        converted = `/Users/${username}${rest}`;
      } else {
        converted = `/home/${username}${rest}`;
      }
    } else {
      // Generic conversion: C:\path -> /path
      converted = windowsPath.replace(/^[A-Z]:\\/i, '/').replace(/\\/g, '/');
    }

    return converted;
  },

  /**
   * Get user home directory
   * @returns {string} Home directory path
   */
  getHomeDir() {
    return PLATFORM.homeDir;
  },

  /**
   * Get Claude config directory (platform-appropriate)
   * @returns {string} Claude config directory
   */
  getClaudeConfigDir() {
    if (PLATFORM.isWindows) {
      return path.join(PLATFORM.homeDir, '.claude');
    } else if (PLATFORM.isMac) {
      return path.join(PLATFORM.homeDir, '.claude');
    } else {
      return path.join(PLATFORM.homeDir, '.claude');
    }
  },

  /**
   * Get project root dynamically
   * @returns {string} Project root path
   */
  getProjectRoot() {
    // Walk up from this file to find package.json or CLAUDE.md
    let current = __dirname;
    while (current !== path.dirname(current)) {
      if (fs.existsSync(path.join(current, 'CLAUDE.md')) ||
          fs.existsSync(path.join(current, 'package.json'))) {
        return current;
      }
      current = path.dirname(current);
    }
    return __dirname;
  },

  /**
   * Join paths in platform-appropriate way
   * @param {...string} parts - Path parts
   * @returns {string} Joined path
   */
  join(...parts) {
    return path.join(...parts);
  },

  /**
   * Make path relative to project root
   * @param {string} absolutePath - Absolute path
   * @returns {string} Relative path
   */
  makeRelative(absolutePath) {
    const projectRoot = this.getProjectRoot();
    if (absolutePath.startsWith(projectRoot)) {
      return absolutePath.slice(projectRoot.length + 1);
    }
    return absolutePath;
  }
};

/**
 * Shell command utilities
 */
const ShellUtils = {
  /**
   * Get shell command for current platform
   * @param {string} command - Unix-style command
   * @returns {string} Platform-appropriate command
   */
  getCommand(command) {
    if (PLATFORM.isWindows) {
      // Convert common Unix commands to Windows equivalents
      const conversions = {
        'ls': 'dir',
        'cat': 'type',
        'rm': 'del',
        'rm -rf': 'rmdir /s /q',
        'cp': 'copy',
        'mv': 'move',
        'mkdir -p': 'mkdir',
        'touch': 'type nul >',
        'which': 'where',
        'pwd': 'cd'
      };

      for (const [unix, win] of Object.entries(conversions)) {
        if (command.startsWith(unix + ' ') || command === unix) {
          command = command.replace(unix, win);
        }
      }
    }
    return command;
  },

  /**
   * Get shell executable for current platform
   * @returns {string} Shell path
   */
  getShell() {
    if (PLATFORM.isWindows) {
      return process.env.COMSPEC || 'cmd.exe';
    }
    return process.env.SHELL || '/bin/bash';
  },

  /**
   * Get shell arguments for running a command
   * @param {string} command - Command to run
   * @returns {string[]} Shell args
   */
  getShellArgs(command) {
    if (PLATFORM.isWindows) {
      return ['/c', command];
    }
    return ['-c', command];
  }
};

/**
 * Environment utilities
 */
const EnvUtils = {
  /**
   * Get environment variable with fallback
   * @param {string} name - Variable name
   * @param {string} fallback - Fallback value
   * @returns {string} Value
   */
  get(name, fallback = '') {
    return process.env[name] || fallback;
  },

  /**
   * Check if running in CI environment
   * @returns {boolean} Is CI
   */
  isCI() {
    return !!(
      process.env.CI ||
      process.env.GITHUB_ACTIONS ||
      process.env.GITLAB_CI ||
      process.env.CIRCLECI ||
      process.env.TRAVIS
    );
  },

  /**
   * Get path separator for current platform
   * @returns {string} Path separator
   */
  getPathSeparator() {
    return path.sep;
  },

  /**
   * Get line ending for current platform
   * @returns {string} Line ending
   */
  getLineEnding() {
    return PLATFORM.isWindows ? '\r\n' : '\n';
  }
};

/**
 * File path scanner for hardcoded Windows paths
 */
class HardcodedPathScanner {
  constructor() {
    this.windowsPathPattern = /[A-Z]:\\[^"'\s]+/g;
    this.userPathPattern = /C:\\Users\\[^\\]+/gi;
    this.findings = [];
  }

  /**
   * Scan a file for hardcoded Windows paths
   * @param {string} filePath - File to scan
   * @returns {Object[]} Findings
   */
  scanFile(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const lines = content.split('\n');
      const fileFindings = [];

      lines.forEach((line, index) => {
        const matches = line.match(this.windowsPathPattern) || [];
        for (const match of matches) {
          // Skip if it's in a comment explaining the issue
          if (line.includes('// ') && line.indexOf('//') < line.indexOf(match)) {
            continue;
          }
          // Skip if it's a placeholder or example
          if (match.includes('YOUR_') || match.includes('EXAMPLE')) {
            continue;
          }

          fileFindings.push({
            file: filePath,
            line: index + 1,
            path: match,
            context: line.trim().slice(0, 100)
          });
        }
      });

      this.findings.push(...fileFindings);
      return fileFindings;
    } catch (err) {
      return [];
    }
  }

  /**
   * Scan directory for hardcoded Windows paths
   * @param {string} dir - Directory to scan
   * @param {string[]} extensions - File extensions to check
   * @returns {Object[]} All findings
   */
  scanDirectory(dir, extensions = ['.js', '.cjs', '.ts', '.json', '.md']) {
    const files = this.getFilesRecursive(dir, extensions);
    for (const file of files) {
      this.scanFile(file);
    }
    return this.findings;
  }

  /**
   * Get files recursively
   */
  getFilesRecursive(dir, extensions, files = []) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          // Skip node_modules and .git
          if (entry.name !== 'node_modules' && entry.name !== '.git') {
            this.getFilesRecursive(fullPath, extensions, files);
          }
        } else if (extensions.some(ext => entry.name.endsWith(ext))) {
          files.push(fullPath);
        }
      }
    } catch (err) {
      // Ignore permission errors
    }
    return files;
  }

  /**
   * Get summary of findings
   */
  getSummary() {
    return {
      totalFindings: this.findings.length,
      uniqueFiles: [...new Set(this.findings.map(f => f.file))].length,
      findings: this.findings
    };
  }

  /**
   * Generate fix suggestions
   */
  generateFixes() {
    return this.findings.map(finding => ({
      ...finding,
      suggestion: `Replace with: path.join(os.homedir(), '${finding.path.replace(/^C:\\Users\\[^\\]+/, '').replace(/\\/g, "', '")}')`
    }));
  }
}

/**
 * Platform compatibility test suite
 */
class PlatformCompatibilityTests {
  constructor() {
    this.results = [];
  }

  test(name, fn) {
    try {
      fn();
      this.results.push({ name, status: 'PASS' });
      console.log(`  [PASS] ${name}`);
    } catch (err) {
      this.results.push({ name, status: 'FAIL', error: err.message });
      console.log(`  [FAIL] ${name}: ${err.message}`);
    }
  }

  runAll() {
    console.log('\n=== Platform Compatibility Tests ===\n');

    console.log('--- Path Utilities ---');

    this.test('PathUtils: normalize works', () => {
      const result = PathUtils.normalize('a/b/c');
      if (!result) throw new Error('normalize returned empty');
    });

    this.test('PathUtils: fromWindows converts paths', () => {
      const result = PathUtils.fromWindows('C:\\Users\\test\\project');
      if (PLATFORM.isWindows) {
        if (result !== 'C:\\Users\\test\\project') {
          throw new Error('Should not modify on Windows');
        }
      } else {
        if (result.includes('\\')) {
          throw new Error('Should convert backslashes');
        }
      }
    });

    this.test('PathUtils: getHomeDir returns string', () => {
      const home = PathUtils.getHomeDir();
      if (typeof home !== 'string' || home.length < 2) {
        throw new Error('Invalid home dir');
      }
    });

    this.test('PathUtils: getProjectRoot finds root', () => {
      const root = PathUtils.getProjectRoot();
      if (!fs.existsSync(root)) {
        throw new Error('Project root does not exist');
      }
    });

    console.log('\n--- Shell Utilities ---');

    this.test('ShellUtils: getShell returns valid shell', () => {
      const shell = ShellUtils.getShell();
      if (!shell) throw new Error('No shell returned');
    });

    this.test('ShellUtils: getShellArgs works', () => {
      const args = ShellUtils.getShellArgs('echo test');
      if (!Array.isArray(args) || args.length < 2) {
        throw new Error('Invalid args');
      }
    });

    console.log('\n--- Environment Utilities ---');

    this.test('EnvUtils: getPathSeparator works', () => {
      const sep = EnvUtils.getPathSeparator();
      if (sep !== '/' && sep !== '\\') {
        throw new Error('Invalid separator');
      }
    });

    this.test('EnvUtils: getLineEnding works', () => {
      const ending = EnvUtils.getLineEnding();
      if (ending !== '\n' && ending !== '\r\n') {
        throw new Error('Invalid line ending');
      }
    });

    console.log('\n--- Hardcoded Path Scanner ---');

    this.test('Scanner: Can scan files', () => {
      const scanner = new HardcodedPathScanner();
      // Scan a known file
      const result = scanner.scanFile(__filename);
      // This file might have Windows paths in comments/examples
    });

    this.test('Scanner: getSummary works', () => {
      const scanner = new HardcodedPathScanner();
      const summary = scanner.getSummary();
      if (typeof summary.totalFindings !== 'number') {
        throw new Error('Invalid summary');
      }
    });

    // Summary
    const passed = this.results.filter(r => r.status === 'PASS').length;
    const failed = this.results.filter(r => r.status === 'FAIL').length;

    console.log('\n========================================');
    console.log('PLATFORM COMPATIBILITY RESULTS');
    console.log('========================================');
    console.log(`Platform: ${PLATFORM.name} (${PLATFORM.arch})`);
    console.log(`Total:  ${this.results.length}`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${failed}`);
    console.log(`Status: ${failed === 0 ? 'ALL TESTS PASSED' : 'FAILURES DETECTED'}`);
    console.log('========================================\n');

    return {
      platform: PLATFORM,
      total: this.results.length,
      passed,
      failed,
      results: this.results
    };
  }
}

// Export
module.exports = {
  PLATFORM,
  PathUtils,
  ShellUtils,
  EnvUtils,
  HardcodedPathScanner,
  PlatformCompatibilityTests
};

// Run if executed directly
if (require.main === module) {
  const tests = new PlatformCompatibilityTests();
  const results = tests.runAll();
  process.exit(results.failed > 0 ? 1 : 0);
}
