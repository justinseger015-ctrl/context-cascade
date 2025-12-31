/**
 * Unified State Manager
 * Phase 4.3 Architecture Optimization
 *
 * Centralizes state management across the system.
 * Provides ACID-like guarantees for state operations.
 *
 * @module architecture/state/unified-state
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// State storage configuration
const STATE_CONFIG = {
  baseDir: path.join(__dirname, '..', '..', 'state'),
  backupDir: path.join(__dirname, '..', '..', 'state', 'backups'),
  maxBackups: 10,
  autoSaveInterval: 30000 // 30 seconds
};

/**
 * State namespaces for different components
 */
const NAMESPACES = {
  session: 'session',      // Current session state
  agents: 'agents',        // Agent execution state
  workflows: 'workflows',  // Workflow state
  tasks: 'tasks',          // Task queue state
  metrics: 'metrics',      // Performance metrics
  cache: 'cache'           // Temporary cache
};

/**
 * In-memory state store
 */
const stateStore = new Map();

/**
 * State change listeners
 */
const listeners = new Map();

/**
 * Ensure state directories exist
 */
function ensureDirectories() {
  if (!fs.existsSync(STATE_CONFIG.baseDir)) {
    fs.mkdirSync(STATE_CONFIG.baseDir, { recursive: true });
  }
  if (!fs.existsSync(STATE_CONFIG.backupDir)) {
    fs.mkdirSync(STATE_CONFIG.backupDir, { recursive: true });
  }
}

/**
 * Generate state file path
 * @param {string} namespace - State namespace
 * @returns {string} File path
 */
function getStatePath(namespace) {
  ensureDirectories();
  return path.join(STATE_CONFIG.baseDir, `${namespace}.json`);
}

/**
 * Load state from disk
 * @param {string} namespace - State namespace
 * @returns {Object} Loaded state
 */
function loadState(namespace) {
  const filePath = getStatePath(namespace);

  try {
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf8');
      const state = JSON.parse(content);
      stateStore.set(namespace, state);
      return state;
    }
  } catch (err) {
    console.error(`[State] Failed to load ${namespace}:`, err.message);
  }

  // Return default empty state
  const defaultState = {
    namespace,
    version: 1,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    data: {}
  };
  stateStore.set(namespace, defaultState);
  return defaultState;
}

/**
 * Save state to disk
 * @param {string} namespace - State namespace
 * @returns {boolean} Success
 */
function saveState(namespace) {
  const state = stateStore.get(namespace);
  if (!state) return false;

  const filePath = getStatePath(namespace);

  try {
    // Update timestamp
    state.updatedAt = new Date().toISOString();
    state.version = (state.version || 0) + 1;

    // Calculate checksum
    const content = JSON.stringify(state, null, 2);
    state.checksum = crypto.createHash('sha256').update(content).digest('hex').slice(0, 16);

    fs.writeFileSync(filePath, JSON.stringify(state, null, 2));
    return true;
  } catch (err) {
    console.error(`[State] Failed to save ${namespace}:`, err.message);
    return false;
  }
}

/**
 * Create backup of state
 * @param {string} namespace - State namespace
 * @returns {string|null} Backup path or null
 */
function backupState(namespace) {
  const state = stateStore.get(namespace);
  if (!state) return null;

  ensureDirectories();

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupPath = path.join(STATE_CONFIG.backupDir, `${namespace}-${timestamp}.json`);

  try {
    fs.writeFileSync(backupPath, JSON.stringify(state, null, 2));

    // Clean old backups
    cleanOldBackups(namespace);

    return backupPath;
  } catch (err) {
    console.error(`[State] Failed to backup ${namespace}:`, err.message);
    return null;
  }
}

/**
 * Clean old backups keeping only recent ones
 * @param {string} namespace - State namespace
 */
function cleanOldBackups(namespace) {
  try {
    const files = fs.readdirSync(STATE_CONFIG.backupDir)
      .filter(f => f.startsWith(`${namespace}-`))
      .sort()
      .reverse();

    // Remove old backups
    for (let i = STATE_CONFIG.maxBackups; i < files.length; i++) {
      fs.unlinkSync(path.join(STATE_CONFIG.backupDir, files[i]));
    }
  } catch (err) {
    // Ignore cleanup errors
  }
}

/**
 * Restore state from backup
 * @param {string} namespace - State namespace
 * @param {string} backupPath - Path to backup file
 * @returns {boolean} Success
 */
function restoreState(namespace, backupPath) {
  try {
    const content = fs.readFileSync(backupPath, 'utf8');
    const state = JSON.parse(content);
    stateStore.set(namespace, state);
    saveState(namespace);
    return true;
  } catch (err) {
    console.error(`[State] Failed to restore ${namespace}:`, err.message);
    return false;
  }
}

/**
 * Get state value
 * @param {string} namespace - State namespace
 * @param {string} key - Key to get
 * @param {*} defaultValue - Default if not found
 * @returns {*} Value
 */
function get(namespace, key, defaultValue = null) {
  let state = stateStore.get(namespace);
  if (!state) {
    state = loadState(namespace);
  }

  if (key.includes('.')) {
    // Support dot notation
    const parts = key.split('.');
    let value = state.data;
    for (const part of parts) {
      if (value === undefined || value === null) return defaultValue;
      value = value[part];
    }
    return value !== undefined ? value : defaultValue;
  }

  return state.data[key] !== undefined ? state.data[key] : defaultValue;
}

/**
 * Set state value
 * @param {string} namespace - State namespace
 * @param {string} key - Key to set
 * @param {*} value - Value to set
 * @param {boolean} persist - Whether to persist immediately
 * @returns {boolean} Success
 */
function set(namespace, key, value, persist = false) {
  let state = stateStore.get(namespace);
  if (!state) {
    state = loadState(namespace);
  }

  const oldValue = get(namespace, key);

  if (key.includes('.')) {
    // Support dot notation
    const parts = key.split('.');
    let obj = state.data;
    for (let i = 0; i < parts.length - 1; i++) {
      if (!obj[parts[i]]) obj[parts[i]] = {};
      obj = obj[parts[i]];
    }
    obj[parts[parts.length - 1]] = value;
  } else {
    state.data[key] = value;
  }

  // Notify listeners
  notifyListeners(namespace, key, value, oldValue);

  if (persist) {
    return saveState(namespace);
  }

  return true;
}

/**
 * Delete state value
 * @param {string} namespace - State namespace
 * @param {string} key - Key to delete
 * @param {boolean} persist - Whether to persist immediately
 * @returns {boolean} Success
 */
function del(namespace, key, persist = false) {
  let state = stateStore.get(namespace);
  if (!state) return true;

  const oldValue = get(namespace, key);

  if (key.includes('.')) {
    const parts = key.split('.');
    let obj = state.data;
    for (let i = 0; i < parts.length - 1; i++) {
      if (!obj[parts[i]]) return true;
      obj = obj[parts[i]];
    }
    delete obj[parts[parts.length - 1]];
  } else {
    delete state.data[key];
  }

  notifyListeners(namespace, key, undefined, oldValue);

  if (persist) {
    return saveState(namespace);
  }

  return true;
}

/**
 * Get all keys in namespace
 * @param {string} namespace - State namespace
 * @returns {string[]} Keys
 */
function keys(namespace) {
  let state = stateStore.get(namespace);
  if (!state) {
    state = loadState(namespace);
  }
  return Object.keys(state.data);
}

/**
 * Clear all state in namespace
 * @param {string} namespace - State namespace
 * @param {boolean} persist - Whether to persist
 * @returns {boolean} Success
 */
function clear(namespace, persist = false) {
  let state = stateStore.get(namespace);
  if (!state) {
    state = loadState(namespace);
  }

  // Backup before clearing
  backupState(namespace);

  state.data = {};

  if (persist) {
    return saveState(namespace);
  }

  return true;
}

/**
 * Add state change listener
 * @param {string} namespace - State namespace
 * @param {Function} callback - Callback(key, newValue, oldValue)
 * @returns {string} Listener ID
 */
function addListener(namespace, callback) {
  const listenerId = crypto.randomBytes(8).toString('hex');

  if (!listeners.has(namespace)) {
    listeners.set(namespace, new Map());
  }

  listeners.get(namespace).set(listenerId, callback);
  return listenerId;
}

/**
 * Remove state change listener
 * @param {string} namespace - State namespace
 * @param {string} listenerId - Listener ID
 */
function removeListener(namespace, listenerId) {
  if (listeners.has(namespace)) {
    listeners.get(namespace).delete(listenerId);
  }
}

/**
 * Notify listeners of state change
 * @param {string} namespace - State namespace
 * @param {string} key - Changed key
 * @param {*} newValue - New value
 * @param {*} oldValue - Old value
 */
function notifyListeners(namespace, key, newValue, oldValue) {
  if (!listeners.has(namespace)) return;

  for (const callback of listeners.get(namespace).values()) {
    try {
      callback(key, newValue, oldValue);
    } catch (err) {
      console.error(`[State] Listener error:`, err.message);
    }
  }
}

/**
 * Transaction support - batch operations
 * @param {string} namespace - State namespace
 * @param {Function} operations - Function receiving state operations
 * @returns {boolean} Success
 */
function transaction(namespace, operations) {
  // Backup before transaction
  const state = stateStore.get(namespace) || loadState(namespace);
  const backup = JSON.parse(JSON.stringify(state));

  try {
    // Run operations
    operations({
      get: (key, def) => get(namespace, key, def),
      set: (key, value) => set(namespace, key, value, false),
      del: (key) => del(namespace, key, false)
    });

    // Persist
    return saveState(namespace);
  } catch (err) {
    // Rollback
    stateStore.set(namespace, backup);
    console.error(`[State] Transaction failed, rolled back:`, err.message);
    return false;
  }
}

/**
 * Get state summary for a namespace
 * @param {string} namespace - State namespace
 * @returns {Object} Summary
 */
function getSummary(namespace) {
  const state = stateStore.get(namespace) || loadState(namespace);

  return {
    namespace,
    version: state.version,
    keyCount: Object.keys(state.data).length,
    createdAt: state.createdAt,
    updatedAt: state.updatedAt,
    checksum: state.checksum
  };
}

/**
 * Get all state summaries
 * @returns {Object[]} Summaries
 */
function getAllSummaries() {
  return Object.values(NAMESPACES).map(ns => getSummary(ns));
}

/**
 * Persist all namespaces
 * @returns {Object} Results
 */
function persistAll() {
  const results = {};

  for (const namespace of Object.values(NAMESPACES)) {
    if (stateStore.has(namespace)) {
      results[namespace] = saveState(namespace);
    }
  }

  return results;
}

// Export
module.exports = {
  // Configuration
  STATE_CONFIG,
  NAMESPACES,

  // Core operations
  get,
  set,
  del,
  keys,
  clear,

  // Persistence
  loadState,
  saveState,
  backupState,
  restoreState,
  persistAll,

  // Transactions
  transaction,

  // Listeners
  addListener,
  removeListener,

  // Info
  getSummary,
  getAllSummaries
};
