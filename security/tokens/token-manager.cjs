/**
 * Agent Token Manager
 * Phase 1.2 Security Hardening
 *
 * Provides cryptographic token generation and validation for agent identity.
 * Tokens are used to authenticate agents before RBAC enforcement.
 *
 * @module security/tokens/token-manager
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Token configuration
const TOKEN_CONFIG = {
  algorithm: 'aes-256-gcm',
  keyLength: 32,
  ivLength: 16,
  saltLength: 16,
  tagLength: 16,
  tokenExpiry: 24 * 60 * 60 * 1000, // 24 hours in milliseconds
};

// Secret key for token encryption (in production, use proper key management)
let MASTER_KEY = null;

/**
 * Initialize or load the master key
 * @returns {Buffer} Master key
 */
function getMasterKey() {
  if (MASTER_KEY) return MASTER_KEY;

  const keyPath = path.join(__dirname, '.master-key');

  try {
    if (fs.existsSync(keyPath)) {
      MASTER_KEY = Buffer.from(fs.readFileSync(keyPath, 'utf8'), 'hex');
    } else {
      // Generate new key
      MASTER_KEY = crypto.randomBytes(TOKEN_CONFIG.keyLength);
      fs.writeFileSync(keyPath, MASTER_KEY.toString('hex'), { mode: 0o600 });
      console.log('[TokenManager] Generated new master key');
    }
  } catch (err) {
    // Fallback to environment variable or generate ephemeral key
    if (process.env.AGENT_MASTER_KEY) {
      MASTER_KEY = Buffer.from(process.env.AGENT_MASTER_KEY, 'hex');
    } else {
      MASTER_KEY = crypto.randomBytes(TOKEN_CONFIG.keyLength);
      console.warn('[TokenManager] Using ephemeral key - tokens will not persist');
    }
  }

  return MASTER_KEY;
}

/**
 * Token payload structure
 * @typedef {Object} TokenPayload
 * @property {string} agentId - Agent identifier
 * @property {string} role - RBAC role
 * @property {number} issuedAt - Timestamp when token was issued
 * @property {number} expiresAt - Timestamp when token expires
 * @property {string} nonce - Random nonce for uniqueness
 */

/**
 * Generate a secure token for an agent
 * @param {string} agentId - Unique agent identifier
 * @param {string} role - RBAC role for the agent
 * @param {Object} options - Optional configuration
 * @param {number} options.expiryMs - Custom expiry in milliseconds
 * @returns {Object} Token object with token string and metadata
 */
function generateToken(agentId, role, options = {}) {
  const key = getMasterKey();
  const iv = crypto.randomBytes(TOKEN_CONFIG.ivLength);
  const salt = crypto.randomBytes(TOKEN_CONFIG.saltLength);

  const now = Date.now();
  const expiryMs = options.expiryMs || TOKEN_CONFIG.tokenExpiry;

  // Create payload
  const payload = {
    agentId,
    role,
    issuedAt: now,
    expiresAt: now + expiryMs,
    nonce: crypto.randomBytes(8).toString('hex')
  };

  // Derive key from master key and salt
  const derivedKey = crypto.pbkdf2Sync(key, salt, 100000, TOKEN_CONFIG.keyLength, 'sha512');

  // Encrypt payload
  const cipher = crypto.createCipheriv(TOKEN_CONFIG.algorithm, derivedKey, iv);
  const payloadStr = JSON.stringify(payload);

  let encrypted = cipher.update(payloadStr, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();

  // Combine all parts: salt + iv + authTag + encrypted
  const token = Buffer.concat([
    salt,
    iv,
    authTag,
    Buffer.from(encrypted, 'hex')
  ]).toString('base64url');

  return {
    token,
    agentId,
    role,
    issuedAt: new Date(now).toISOString(),
    expiresAt: new Date(now + expiryMs).toISOString()
  };
}

/**
 * Validate and decode a token
 * @param {string} token - Token string to validate
 * @returns {Object} Validation result with payload if valid
 */
function validateToken(token) {
  try {
    const key = getMasterKey();

    // Decode token
    const tokenBuffer = Buffer.from(token, 'base64url');

    // Extract parts
    const salt = tokenBuffer.subarray(0, TOKEN_CONFIG.saltLength);
    const iv = tokenBuffer.subarray(
      TOKEN_CONFIG.saltLength,
      TOKEN_CONFIG.saltLength + TOKEN_CONFIG.ivLength
    );
    const authTag = tokenBuffer.subarray(
      TOKEN_CONFIG.saltLength + TOKEN_CONFIG.ivLength,
      TOKEN_CONFIG.saltLength + TOKEN_CONFIG.ivLength + TOKEN_CONFIG.tagLength
    );
    const encrypted = tokenBuffer.subarray(
      TOKEN_CONFIG.saltLength + TOKEN_CONFIG.ivLength + TOKEN_CONFIG.tagLength
    );

    // Derive key
    const derivedKey = crypto.pbkdf2Sync(key, salt, 100000, TOKEN_CONFIG.keyLength, 'sha512');

    // Decrypt
    const decipher = crypto.createDecipheriv(TOKEN_CONFIG.algorithm, derivedKey, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(encrypted, null, 'utf8');
    decrypted += decipher.final('utf8');

    const payload = JSON.parse(decrypted);

    // Check expiry
    if (Date.now() > payload.expiresAt) {
      return {
        valid: false,
        reason: 'Token expired',
        expiredAt: new Date(payload.expiresAt).toISOString()
      };
    }

    return {
      valid: true,
      payload
    };

  } catch (err) {
    return {
      valid: false,
      reason: `Token validation failed: ${err.message}`
    };
  }
}

/**
 * Refresh a token (issue new token with same claims)
 * @param {string} token - Existing valid token
 * @param {Object} options - Options for new token
 * @returns {Object} New token or error
 */
function refreshToken(token, options = {}) {
  const validation = validateToken(token);

  if (!validation.valid) {
    return {
      error: true,
      reason: validation.reason
    };
  }

  return generateToken(
    validation.payload.agentId,
    validation.payload.role,
    options
  );
}

/**
 * Revoke a token (add to revocation list)
 * @param {string} token - Token to revoke
 * @returns {boolean} True if revoked
 */
function revokeToken(token) {
  const revocationPath = path.join(__dirname, '.revoked-tokens');

  try {
    // Get token hash for revocation list
    const tokenHash = crypto.createHash('sha256').update(token).digest('hex');

    // Add to revocation list
    fs.appendFileSync(revocationPath, tokenHash + '\n');

    return true;
  } catch (err) {
    console.error('[TokenManager] Failed to revoke token:', err.message);
    return false;
  }
}

/**
 * Check if a token has been revoked
 * @param {string} token - Token to check
 * @returns {boolean} True if revoked
 */
function isRevoked(token) {
  const revocationPath = path.join(__dirname, '.revoked-tokens');

  try {
    if (!fs.existsSync(revocationPath)) {
      return false;
    }

    const tokenHash = crypto.createHash('sha256').update(token).digest('hex');
    const revoked = fs.readFileSync(revocationPath, 'utf8');

    return revoked.includes(tokenHash);
  } catch (err) {
    return false;
  }
}

/**
 * Full token validation including revocation check
 * @param {string} token - Token to validate
 * @returns {Object} Complete validation result
 */
function fullValidation(token) {
  // Check revocation first
  if (isRevoked(token)) {
    return {
      valid: false,
      reason: 'Token has been revoked'
    };
  }

  return validateToken(token);
}

/**
 * Generate a simple API key (for less secure contexts)
 * @param {string} agentId - Agent identifier
 * @returns {string} API key
 */
function generateApiKey(agentId) {
  const key = getMasterKey();
  const data = `${agentId}:${Date.now()}:${crypto.randomBytes(8).toString('hex')}`;
  const hmac = crypto.createHmac('sha256', key).update(data).digest('hex');
  return `cc_${agentId}_${hmac.substring(0, 32)}`;
}

/**
 * Token store for active sessions
 */
const TOKEN_STORE = new Map();

/**
 * Store a token for an agent session
 * @param {string} agentId - Agent identifier
 * @param {string} token - Token to store
 */
function storeToken(agentId, token) {
  TOKEN_STORE.set(agentId, {
    token,
    storedAt: Date.now()
  });
}

/**
 * Get stored token for an agent
 * @param {string} agentId - Agent identifier
 * @returns {string|null} Token or null
 */
function getStoredToken(agentId) {
  const entry = TOKEN_STORE.get(agentId);
  return entry ? entry.token : null;
}

/**
 * Clear stored token for an agent
 * @param {string} agentId - Agent identifier
 */
function clearStoredToken(agentId) {
  TOKEN_STORE.delete(agentId);
}

// Export functions
module.exports = {
  generateToken,
  validateToken,
  refreshToken,
  revokeToken,
  isRevoked,
  fullValidation,
  generateApiKey,
  storeToken,
  getStoredToken,
  clearStoredToken,
  TOKEN_CONFIG
};
