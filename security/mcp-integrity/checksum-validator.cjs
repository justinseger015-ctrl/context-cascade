/**
 * MCP Checksum Validator
 * Phase 1.3 Security Hardening
 *
 * Validates integrity of MCP servers before loading to prevent tool poisoning.
 * Maintains a registry of known-good checksums for approved MCP servers.
 *
 * @module security/mcp-integrity/checksum-validator
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Path to checksum registry
const CHECKSUM_REGISTRY_PATH = path.join(__dirname, 'checksum-registry.json');

/**
 * Checksum registry structure
 * @typedef {Object} ChecksumEntry
 * @property {string} name - MCP server name
 * @property {string} version - Version string
 * @property {string} sha256 - SHA256 hash of the main entry file
 * @property {string} sha384 - SHA384 hash for additional security
 * @property {string} addedAt - ISO timestamp when added
 * @property {string} addedBy - Who added this entry
 * @property {boolean} trusted - Whether this is a trusted/verified server
 */

/**
 * Load checksum registry from disk
 * @returns {Object} Registry object
 */
function loadRegistry() {
  try {
    if (fs.existsSync(CHECKSUM_REGISTRY_PATH)) {
      return JSON.parse(fs.readFileSync(CHECKSUM_REGISTRY_PATH, 'utf8'));
    }
  } catch (err) {
    console.error('[MCP-Integrity] Failed to load registry:', err.message);
  }

  // Return default empty registry
  return {
    version: '1.0.0',
    updatedAt: new Date().toISOString(),
    servers: {}
  };
}

/**
 * Save checksum registry to disk
 * @param {Object} registry - Registry object to save
 */
function saveRegistry(registry) {
  registry.updatedAt = new Date().toISOString();
  fs.writeFileSync(CHECKSUM_REGISTRY_PATH, JSON.stringify(registry, null, 2));
}

/**
 * Calculate checksums for a file
 * @param {string} filePath - Path to file
 * @returns {Object} Object with sha256 and sha384 hashes
 */
function calculateChecksums(filePath) {
  const content = fs.readFileSync(filePath);

  return {
    sha256: crypto.createHash('sha256').update(content).digest('hex'),
    sha384: crypto.createHash('sha384').update(content).digest('hex'),
    size: content.length
  };
}

/**
 * Calculate checksum for a directory (recursive)
 * @param {string} dirPath - Path to directory
 * @returns {string} Combined hash of all files
 */
function calculateDirectoryChecksum(dirPath) {
  const hash = crypto.createHash('sha256');
  const files = [];

  function walkDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        // Skip node_modules and .git
        if (entry.name !== 'node_modules' && entry.name !== '.git') {
          walkDir(fullPath);
        }
      } else if (entry.isFile()) {
        files.push(fullPath);
      }
    }
  }

  walkDir(dirPath);

  // Sort for deterministic order
  files.sort();

  // Hash each file
  for (const file of files) {
    const relativePath = path.relative(dirPath, file);
    const content = fs.readFileSync(file);
    hash.update(relativePath);
    hash.update(content);
  }

  return hash.digest('hex');
}

/**
 * Register a new MCP server with its checksum
 * @param {string} name - Server name
 * @param {string} entryPath - Path to main entry file or directory
 * @param {Object} options - Additional options
 * @returns {Object} Registration result
 */
function registerServer(name, entryPath, options = {}) {
  const registry = loadRegistry();

  if (!fs.existsSync(entryPath)) {
    return {
      success: false,
      error: `Path not found: ${entryPath}`
    };
  }

  const stats = fs.statSync(entryPath);
  let checksums;

  if (stats.isDirectory()) {
    checksums = {
      sha256: calculateDirectoryChecksum(entryPath),
      sha384: null, // Directory mode uses single hash
      size: null,
      type: 'directory'
    };
  } else {
    checksums = {
      ...calculateChecksums(entryPath),
      type: 'file'
    };
  }

  registry.servers[name] = {
    name,
    version: options.version || '1.0.0',
    path: entryPath,
    ...checksums,
    addedAt: new Date().toISOString(),
    addedBy: options.addedBy || 'system',
    trusted: options.trusted || false,
    description: options.description || ''
  };

  saveRegistry(registry);

  return {
    success: true,
    entry: registry.servers[name]
  };
}

/**
 * Validation result
 * @typedef {Object} ValidationResult
 * @property {boolean} valid - Whether validation passed
 * @property {string} reason - Explanation
 * @property {Object} details - Additional details
 */

/**
 * Validate an MCP server against registered checksum
 * @param {string} name - Server name
 * @param {string} entryPath - Path to validate
 * @returns {ValidationResult} Validation result
 */
function validateServer(name, entryPath) {
  const registry = loadRegistry();
  const expected = registry.servers[name];

  if (!expected) {
    return {
      valid: false,
      reason: `MCP_UNKNOWN: Server '${name}' not in checksum registry`,
      details: {
        action: 'Register server before use or add to allowlist'
      }
    };
  }

  if (!fs.existsSync(entryPath)) {
    return {
      valid: false,
      reason: `MCP_MISSING: Server file not found at '${entryPath}'`,
      details: {
        expectedPath: expected.path
      }
    };
  }

  const stats = fs.statSync(entryPath);
  let actual;

  if (stats.isDirectory()) {
    actual = {
      sha256: calculateDirectoryChecksum(entryPath),
      type: 'directory'
    };
  } else {
    actual = {
      ...calculateChecksums(entryPath),
      type: 'file'
    };
  }

  // Compare checksums
  if (actual.sha256 !== expected.sha256) {
    return {
      valid: false,
      reason: `MCP_TAMPERED: Checksum mismatch for '${name}'`,
      details: {
        expected: expected.sha256,
        actual: actual.sha256,
        action: 'Server may have been modified - verify and re-register'
      }
    };
  }

  // For files, also check SHA384 if available
  if (actual.type === 'file' && expected.sha384 && actual.sha384 !== expected.sha384) {
    return {
      valid: false,
      reason: `MCP_TAMPERED: Secondary checksum mismatch for '${name}'`,
      details: {
        expected: expected.sha384,
        actual: actual.sha384
      }
    };
  }

  return {
    valid: true,
    reason: `MCP_VERIFIED: Server '${name}' integrity confirmed`,
    details: {
      trusted: expected.trusted,
      version: expected.version,
      registeredAt: expected.addedAt
    }
  };
}

/**
 * Validate all registered servers
 * @returns {Object} Results for all servers
 */
function validateAllServers() {
  const registry = loadRegistry();
  const results = {};

  for (const [name, entry] of Object.entries(registry.servers)) {
    results[name] = validateServer(name, entry.path);
  }

  return results;
}

/**
 * Remove a server from the registry
 * @param {string} name - Server name
 * @returns {boolean} True if removed
 */
function unregisterServer(name) {
  const registry = loadRegistry();

  if (registry.servers[name]) {
    delete registry.servers[name];
    saveRegistry(registry);
    return true;
  }

  return false;
}

/**
 * List all registered servers
 * @returns {Object[]} Array of server entries
 */
function listServers() {
  const registry = loadRegistry();
  return Object.values(registry.servers);
}

/**
 * Check if a server is trusted
 * @param {string} name - Server name
 * @returns {boolean} True if trusted
 */
function isTrusted(name) {
  const registry = loadRegistry();
  return registry.servers[name]?.trusted || false;
}

/**
 * Mark a server as trusted
 * @param {string} name - Server name
 * @param {boolean} trusted - Trust status
 * @returns {boolean} True if updated
 */
function setTrusted(name, trusted) {
  const registry = loadRegistry();

  if (registry.servers[name]) {
    registry.servers[name].trusted = trusted;
    saveRegistry(registry);
    return true;
  }

  return false;
}

/**
 * Pre-load validation hook for MCP server loading
 * @param {Object} mcpConfig - MCP server configuration from .mcp.json
 * @returns {Object} Validation results with recommendations
 */
function preLoadValidation(mcpConfig) {
  const results = {
    timestamp: new Date().toISOString(),
    servers: {},
    summary: {
      total: 0,
      valid: 0,
      invalid: 0,
      unknown: 0
    }
  };

  for (const [name, config] of Object.entries(mcpConfig.mcpServers || {})) {
    results.summary.total++;

    // Determine entry path from config
    let entryPath = null;
    if (config.args && config.args.length > 0) {
      // Find path-like argument
      for (const arg of config.args) {
        if (arg.includes('/') || arg.includes('\\')) {
          entryPath = arg;
          break;
        }
      }
    }

    if (!entryPath) {
      results.servers[name] = {
        valid: false,
        reason: 'Could not determine entry path from config',
        canValidate: false
      };
      results.summary.unknown++;
      continue;
    }

    const validation = validateServer(name, entryPath);
    results.servers[name] = validation;

    if (validation.valid) {
      results.summary.valid++;
    } else if (validation.reason.includes('UNKNOWN')) {
      results.summary.unknown++;
    } else {
      results.summary.invalid++;
    }
  }

  results.recommendation = results.summary.invalid > 0
    ? 'BLOCK: Some MCP servers failed integrity check'
    : results.summary.unknown > 0
      ? 'WARN: Some MCP servers not in registry'
      : 'ALLOW: All MCP servers verified';

  return results;
}

// Initialize with built-in servers
function initializeBuiltinServers() {
  const builtins = [
    {
      name: 'memory-mcp',
      description: 'Triple-layer memory system',
      trusted: true
    },
    {
      name: 'connascence-analyzer',
      description: 'Code coupling analysis',
      trusted: true
    },
    {
      name: 'sequential-thinking',
      description: 'Sequential reasoning MCP',
      trusted: true
    }
  ];

  // Note: Actual paths would be set during first registration
  console.log('[MCP-Integrity] Registry initialized with', builtins.length, 'builtin definitions');
}

// Export functions
module.exports = {
  loadRegistry,
  saveRegistry,
  calculateChecksums,
  calculateDirectoryChecksum,
  registerServer,
  validateServer,
  validateAllServers,
  unregisterServer,
  listServers,
  isTrusted,
  setTrusted,
  preLoadValidation,
  initializeBuiltinServers
};
