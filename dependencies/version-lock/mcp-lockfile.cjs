/**
 * MCP Version Lockfile Manager
 * Phase 6.1 Dependency Hardening
 *
 * Pins MCP server versions and maintains a lockfile for reproducible deployments.
 * Inspired by npm/yarn lockfile patterns.
 *
 * @module dependencies/version-lock/mcp-lockfile
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { exec } = require('child_process');

// Paths
const PROJECT_ROOT = path.join(__dirname, '..', '..');
const LOCKFILE_PATH = path.join(__dirname, 'mcp-lock.json');
const MCP_CONFIG_PATH = path.join(PROJECT_ROOT, '.mcp.json');

/**
 * Lockfile structure
 */
const DEFAULT_LOCKFILE = {
  version: '1.0.0',
  lockfileVersion: 1,
  createdAt: null,
  updatedAt: null,
  servers: {}
};

/**
 * Load lockfile from disk
 * @returns {Object} Lockfile object
 */
function loadLockfile() {
  try {
    if (fs.existsSync(LOCKFILE_PATH)) {
      return JSON.parse(fs.readFileSync(LOCKFILE_PATH, 'utf8'));
    }
  } catch (err) {
    console.error('[Lockfile] Failed to load:', err.message);
  }
  return { ...DEFAULT_LOCKFILE, createdAt: new Date().toISOString() };
}

/**
 * Save lockfile to disk
 * @param {Object} lockfile - Lockfile to save
 */
function saveLockfile(lockfile) {
  lockfile.updatedAt = new Date().toISOString();
  fs.writeFileSync(LOCKFILE_PATH, JSON.stringify(lockfile, null, 2));
}

/**
 * Load MCP configuration
 * @returns {Object} MCP config
 */
function loadMCPConfig() {
  try {
    if (fs.existsSync(MCP_CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(MCP_CONFIG_PATH, 'utf8'));
    }
  } catch (err) {
    console.error('[Lockfile] Failed to load MCP config:', err.message);
  }
  return { mcpServers: {} };
}

/**
 * Extract version from npx package spec
 * @param {string[]} args - Command args
 * @returns {Object} Package info
 */
function extractNPXPackageInfo(args) {
  for (const arg of args) {
    // Match @scope/package@version or package@version
    const match = arg.match(/^(@?[^@]+)(?:@(.+))?$/);
    if (match && !arg.startsWith('-')) {
      return {
        package: match[1],
        version: match[2] || 'latest',
        isPinned: !!match[2]
      };
    }
  }
  return null;
}

/**
 * Get installed npm package version
 * @param {string} packageName - Package name
 * @returns {Promise<string|null>} Version or null
 */
function getNPMPackageVersion(packageName) {
  return new Promise((resolve) => {
    exec(`npm view ${packageName} version`, { timeout: 10000 }, (err, stdout) => {
      if (err) {
        resolve(null);
      } else {
        resolve(stdout.trim());
      }
    });
  });
}

/**
 * Calculate checksum for server configuration
 * @param {Object} serverConfig - Server configuration
 * @returns {string} SHA256 hash
 */
function calculateConfigChecksum(serverConfig) {
  const normalized = JSON.stringify(serverConfig, Object.keys(serverConfig).sort());
  return crypto.createHash('sha256').update(normalized).digest('hex').slice(0, 16);
}

/**
 * Lock a single MCP server
 * @param {string} serverId - Server ID
 * @param {Object} serverConfig - Server configuration
 * @returns {Promise<Object>} Lock entry
 */
async function lockServer(serverId, serverConfig) {
  const entry = {
    id: serverId,
    command: serverConfig.command,
    lockedAt: new Date().toISOString(),
    configChecksum: calculateConfigChecksum(serverConfig),
    type: 'unknown',
    version: null,
    isPinned: false
  };

  // Detect server type and extract version
  if (serverConfig.command === 'npx' || (serverConfig.args && serverConfig.args.includes('npx'))) {
    entry.type = 'npx';
    const args = serverConfig.args || [];
    const pkgInfo = extractNPXPackageInfo(args);
    if (pkgInfo) {
      entry.package = pkgInfo.package;
      entry.version = pkgInfo.version;
      entry.isPinned = pkgInfo.isPinned;

      // If not pinned, resolve latest version
      if (!pkgInfo.isPinned) {
        const latestVersion = await getNPMPackageVersion(pkgInfo.package);
        if (latestVersion) {
          entry.resolvedVersion = latestVersion;
        }
      }
    }
  } else if (serverConfig.command.includes('python')) {
    entry.type = 'python';
    entry.pythonPath = serverConfig.command;
    entry.module = serverConfig.args ? serverConfig.args.find(a => a === '-m') ? serverConfig.args[serverConfig.args.indexOf('-m') + 1] : null : null;
  } else if (serverConfig.command === 'node') {
    entry.type = 'node';
    entry.script = serverConfig.args ? serverConfig.args[0] : null;
  } else if (serverConfig.command === 'cmd') {
    entry.type = 'cmd';
    // Check if it's wrapping npx
    const args = serverConfig.args || [];
    if (args.includes('npx')) {
      entry.type = 'npx-cmd';
      const npxIndex = args.indexOf('npx');
      const pkgInfo = extractNPXPackageInfo(args.slice(npxIndex + 1));
      if (pkgInfo) {
        entry.package = pkgInfo.package;
        entry.version = pkgInfo.version;
        entry.isPinned = pkgInfo.isPinned;

        if (!pkgInfo.isPinned) {
          const latestVersion = await getNPMPackageVersion(pkgInfo.package);
          if (latestVersion) {
            entry.resolvedVersion = latestVersion;
          }
        }
      }
    }
  }

  // Store environment variables (keys only for security)
  if (serverConfig.env) {
    entry.envKeys = Object.keys(serverConfig.env);
  }

  // Store working directory
  if (serverConfig.cwd) {
    entry.cwd = serverConfig.cwd;
  }

  return entry;
}

/**
 * Generate lockfile from current MCP configuration
 * @returns {Promise<Object>} Generated lockfile
 */
async function generateLockfile() {
  const config = loadMCPConfig();
  const lockfile = loadLockfile();

  console.log('[Lockfile] Generating lockfile for MCP servers...');

  for (const [serverId, serverConfig] of Object.entries(config.mcpServers || {})) {
    console.log(`[Lockfile] Locking ${serverId}...`);
    lockfile.servers[serverId] = await lockServer(serverId, serverConfig);
  }

  saveLockfile(lockfile);
  console.log(`[Lockfile] Locked ${Object.keys(lockfile.servers).length} servers`);

  return lockfile;
}

/**
 * Verify current config matches lockfile
 * @returns {Object} Verification result
 */
function verifyLockfile() {
  const config = loadMCPConfig();
  const lockfile = loadLockfile();

  const result = {
    valid: true,
    mismatches: [],
    missing: [],
    extra: []
  };

  // Check each locked server
  for (const [serverId, locked] of Object.entries(lockfile.servers)) {
    const current = config.mcpServers?.[serverId];

    if (!current) {
      result.missing.push(serverId);
      result.valid = false;
      continue;
    }

    const currentChecksum = calculateConfigChecksum(current);
    if (currentChecksum !== locked.configChecksum) {
      result.mismatches.push({
        server: serverId,
        expected: locked.configChecksum,
        actual: currentChecksum
      });
      result.valid = false;
    }
  }

  // Check for unlocked servers
  for (const serverId of Object.keys(config.mcpServers || {})) {
    if (!lockfile.servers[serverId]) {
      result.extra.push(serverId);
      result.valid = false;
    }
  }

  return result;
}

/**
 * Get unpinned packages that should be pinned
 * @returns {Object[]} List of unpinned packages
 */
function getUnpinnedPackages() {
  const lockfile = loadLockfile();
  const unpinned = [];

  for (const [serverId, entry] of Object.entries(lockfile.servers)) {
    if ((entry.type === 'npx' || entry.type === 'npx-cmd') && !entry.isPinned) {
      unpinned.push({
        server: serverId,
        package: entry.package,
        currentVersion: entry.version,
        resolvedVersion: entry.resolvedVersion,
        suggestion: entry.resolvedVersion ? `${entry.package}@${entry.resolvedVersion}` : null
      });
    }
  }

  return unpinned;
}

/**
 * Generate pinned MCP config
 * @returns {Object} Config with pinned versions
 */
function generatePinnedConfig() {
  const config = loadMCPConfig();
  const lockfile = loadLockfile();
  const pinned = JSON.parse(JSON.stringify(config));

  for (const [serverId, entry] of Object.entries(lockfile.servers)) {
    if (!pinned.mcpServers[serverId]) continue;

    if ((entry.type === 'npx' || entry.type === 'npx-cmd') && entry.resolvedVersion && !entry.isPinned) {
      const args = pinned.mcpServers[serverId].args || [];
      const newArgs = args.map(arg => {
        if (arg === entry.package) {
          return `${entry.package}@${entry.resolvedVersion}`;
        }
        if (arg.startsWith('-y') || arg.startsWith('--yes')) {
          return arg;
        }
        return arg;
      });
      pinned.mcpServers[serverId].args = newArgs;
    }
  }

  return pinned;
}

/**
 * Generate lockfile report
 * @returns {string} Markdown report
 */
function generateLockfileReport() {
  const lockfile = loadLockfile();
  const verification = verifyLockfile();
  const unpinned = getUnpinnedPackages();

  let report = `# MCP Lockfile Report

**Generated**: ${new Date().toISOString()}
**Lockfile Version**: ${lockfile.lockfileVersion}
**Total Servers**: ${Object.keys(lockfile.servers).length}

## Verification Status

| Metric | Value |
|--------|-------|
| Valid | ${verification.valid ? 'Yes' : 'No'} |
| Mismatches | ${verification.mismatches.length} |
| Missing | ${verification.missing.length} |
| Extra | ${verification.extra.length} |

## Locked Servers

| Server | Type | Package | Version | Pinned |
|--------|------|---------|---------|--------|
`;

  for (const [serverId, entry] of Object.entries(lockfile.servers)) {
    report += `| ${serverId} | ${entry.type} | ${entry.package || '-'} | ${entry.version || entry.resolvedVersion || '-'} | ${entry.isPinned ? 'Yes' : 'No'} |\n`;
  }

  if (unpinned.length > 0) {
    report += `\n## Unpinned Packages (Action Required)\n\n`;
    for (const pkg of unpinned) {
      report += `- **${pkg.server}**: ${pkg.package} (current: ${pkg.currentVersion}, resolved: ${pkg.resolvedVersion})\n`;
      if (pkg.suggestion) {
        report += `  - Suggestion: Use \`${pkg.suggestion}\`\n`;
      }
    }
  }

  return report;
}

// Export
module.exports = {
  loadLockfile,
  saveLockfile,
  loadMCPConfig,
  lockServer,
  generateLockfile,
  verifyLockfile,
  getUnpinnedPackages,
  generatePinnedConfig,
  generateLockfileReport,
  calculateConfigChecksum,
  LOCKFILE_PATH,
  MCP_CONFIG_PATH
};

// Run if executed directly
if (require.main === module) {
  generateLockfile().then(() => {
    console.log('\n' + generateLockfileReport());
  });
}
