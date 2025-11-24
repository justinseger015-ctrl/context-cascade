/**
 * Identity Verification System for Agent Reality Map Integration
 *
 * Provides JWT token generation/validation and Ed25519 signature verification
 * for 207 agents with UUID-based identities, roles, and RBAC permissions.
 *
 * Features:
 * - JWT token generation and validation
 * - Ed25519 signature verification
 * - Agent identity extraction from frontmatter (.md files)
 * - Identity caching with 5-minute TTL
 * - Windows compatible (no Unicode)
 *
 * @module hooks/12fa/utils/identity
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const yaml = require('js-yaml');

// Cache for validated identities (5-minute TTL)
const identityCache = new Map();
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

// JWT secret (in production, use env variable)
const JWT_SECRET = process.env.JWT_SECRET || 'agent-reality-map-secret-key';

/**
 * Generate JWT token for an agent
 * @param {Object} agentIdentity - Agent identity object
 * @param {string} agentIdentity.agent_id - UUID v4 agent identifier
 * @param {string} agentIdentity.name - Agent name
 * @param {string} agentIdentity.role - RBAC role
 * @param {number} expiresInSeconds - Token expiration time (default: 3600s)
 * @returns {string} JWT token
 */
function generateJWT(agentIdentity, expiresInSeconds = 3600) {
  const header = {
    alg: 'HS256',
    typ: 'JWT'
  };

  const now = Math.floor(Date.now() / 1000);
  const payload = {
    agent_id: agentIdentity.agent_id,
    name: agentIdentity.name,
    role: agentIdentity.role,
    iat: now,
    exp: now + expiresInSeconds
  };

  const encodedHeader = base64UrlEncode(JSON.stringify(header));
  const encodedPayload = base64UrlEncode(JSON.stringify(payload));

  const signature = crypto
    .createHmac('sha256', JWT_SECRET)
    .update(`${encodedHeader}.${encodedPayload}`)
    .digest('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');

  return `${encodedHeader}.${encodedPayload}.${signature}`;
}

/**
 * Validate JWT token
 * @param {string} token - JWT token to validate
 * @returns {Object|null} Decoded payload if valid, null if invalid
 */
function validateJWT(token) {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) {
      return null;
    }

    const [encodedHeader, encodedPayload, signature] = parts;

    // Verify signature
    const expectedSignature = crypto
      .createHmac('sha256', JWT_SECRET)
      .update(`${encodedHeader}.${encodedPayload}`)
      .digest('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');

    if (signature !== expectedSignature) {
      return null;
    }

    // Decode payload
    const payload = JSON.parse(base64UrlDecode(encodedPayload));

    // Check expiration
    const now = Math.floor(Date.now() / 1000);
    if (payload.exp && payload.exp < now) {
      return null;
    }

    return payload;
  } catch (error) {
    console.error('JWT validation error:', error.message);
    return null;
  }
}

/**
 * Verify Ed25519 signature for agent identity
 * @param {string} message - Message that was signed
 * @param {string} signature - Signature to verify (hex string)
 * @param {string} publicKey - Ed25519 public key (hex string)
 * @returns {boolean} True if signature is valid
 */
function verifyEd25519Signature(message, signature, publicKey) {
  try {
    const verify = crypto.createVerify('SHA256');
    verify.update(message);
    verify.end();

    const publicKeyBuffer = Buffer.from(publicKey, 'hex');
    const signatureBuffer = Buffer.from(signature, 'hex');

    return verify.verify(
      {
        key: publicKeyBuffer,
        format: 'der',
        type: 'spki'
      },
      signatureBuffer
    );
  } catch (error) {
    console.error('Ed25519 verification error:', error.message);
    return false;
  }
}

/**
 * Load agent identity from agent .md file frontmatter
 * @param {string} agentFilePath - Absolute path to agent .md file
 * @returns {Object|null} Agent identity object or null if invalid
 */
function loadAgentIdentity(agentFilePath) {
  try {
    // Read file contents
    const fileContents = fs.readFileSync(agentFilePath, 'utf8');

    // Extract frontmatter (YAML between --- delimiters)
    const frontmatterMatch = fileContents.match(/^---\n([\s\S]*?)\n---/);
    if (!frontmatterMatch) {
      console.error(`No frontmatter found in ${agentFilePath}`);
      return null;
    }

    const frontmatter = yaml.load(frontmatterMatch[1]);

    // Validate required fields
    if (!frontmatter.identity || !frontmatter.identity.agent_id) {
      console.error(`Missing identity.agent_id in ${agentFilePath}`);
      return null;
    }

    if (!frontmatter.name) {
      console.error(`Missing name in ${agentFilePath}`);
      return null;
    }

    if (!frontmatter.identity.role) {
      console.error(`Missing identity.role in ${agentFilePath}`);
      return null;
    }

    // Validate agent_id format (UUID v4)
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(frontmatter.identity.agent_id)) {
      console.error(`Invalid UUID v4 format for agent_id in ${agentFilePath}`);
      return null;
    }

    // Construct identity object
    const identity = {
      agent_id: frontmatter.identity.agent_id,
      name: frontmatter.name,
      role: frontmatter.identity.role,
      capabilities: frontmatter.capabilities || [],
      rbac: frontmatter.rbac || {},
      budget: frontmatter.budget || {},
      metadata: frontmatter.metadata || {},
      file_path: agentFilePath
    };

    return identity;
  } catch (error) {
    console.error(`Error loading agent identity from ${agentFilePath}:`, error.message);
    return null;
  }
}

/**
 * Load agent identity by name (searches agents directory)
 * @param {string} agentName - Agent name (e.g., "backend-dev", "coder")
 * @param {string} agentsDir - Root agents directory (default: auto-detect)
 * @returns {Object|null} Agent identity or null if not found
 */
function loadAgentIdentityByName(agentName, agentsDir = null) {
  // Auto-detect agents directory
  if (!agentsDir) {
    agentsDir = path.join(__dirname, '..', '..', '..', 'agents');
  }

  // Check cache first
  const cacheKey = `agent:${agentName}`;
  const cached = getFromCache(cacheKey);
  if (cached) {
    return cached;
  }

  try {
    // Search recursively for agent file
    const agentFile = findAgentFile(agentsDir, agentName);
    if (!agentFile) {
      console.error(`Agent file not found for: ${agentName}`);
      return null;
    }

    const identity = loadAgentIdentity(agentFile);
    if (identity) {
      // Cache the identity
      setInCache(cacheKey, identity);
    }

    return identity;
  } catch (error) {
    console.error(`Error loading agent identity by name ${agentName}:`, error.message);
    return null;
  }
}

/**
 * Validate agent identity against schema
 * @param {Object} identity - Agent identity object
 * @returns {Object} Validation result {valid: boolean, errors: string[]}
 */
function validateAgentIdentity(identity) {
  const errors = [];

  // Required fields
  if (!identity.agent_id) {
    errors.push('Missing agent_id');
  }

  if (!identity.name) {
    errors.push('Missing name');
  }

  if (!identity.role) {
    errors.push('Missing role');
  }

  // Validate agent_id format (UUID v4)
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  if (identity.agent_id && !uuidRegex.test(identity.agent_id)) {
    errors.push('Invalid UUID v4 format for agent_id');
  }

  // Validate role (must be one of 10 defined roles)
  const validRoles = [
    'admin', 'developer', 'reviewer', 'security', 'database',
    'frontend', 'backend', 'tester', 'analyst', 'coordinator'
  ];
  if (identity.role && !validRoles.includes(identity.role)) {
    errors.push(`Invalid role: ${identity.role}. Must be one of: ${validRoles.join(', ')}`);
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Get item from cache if not expired
 * @param {string} key - Cache key
 * @returns {any|null} Cached value or null if expired/not found
 */
function getFromCache(key) {
  const cached = identityCache.get(key);
  if (!cached) {
    return null;
  }

  const now = Date.now();
  if (now - cached.timestamp > CACHE_TTL_MS) {
    // Expired, remove from cache
    identityCache.delete(key);
    return null;
  }

  return cached.value;
}

/**
 * Set item in cache with timestamp
 * @param {string} key - Cache key
 * @param {any} value - Value to cache
 */
function setInCache(key, value) {
  identityCache.set(key, {
    value,
    timestamp: Date.now()
  });
}

/**
 * Clear entire identity cache
 */
function clearCache() {
  identityCache.clear();
}

/**
 * Find agent .md file by agent name (recursive search)
 * @param {string} directory - Directory to search
 * @param {string} agentName - Agent name to find
 * @returns {string|null} Full path to agent file or null if not found
 */
function findAgentFile(directory, agentName) {
  try {
    const files = fs.readdirSync(directory);

    for (const file of files) {
      const fullPath = path.join(directory, file);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        // Recurse into subdirectory
        const found = findAgentFile(fullPath, agentName);
        if (found) {
          return found;
        }
      } else if (file.endsWith('.md')) {
        // Check if this file contains the agent
        try {
          const contents = fs.readFileSync(fullPath, 'utf8');
          const frontmatterMatch = contents.match(/^---\n([\s\S]*?)\n---/);
          if (frontmatterMatch) {
            const frontmatter = yaml.load(frontmatterMatch[1]);
            if (frontmatter.name === agentName) {
              return fullPath;
            }
          }
        } catch (error) {
          // Skip files that can't be parsed
          continue;
        }
      }
    }

    return null;
  } catch (error) {
    console.error(`Error searching directory ${directory}:`, error.message);
    return null;
  }
}

/**
 * Base64 URL encoding (for JWT)
 * @param {string} str - String to encode
 * @returns {string} Base64 URL encoded string
 */
function base64UrlEncode(str) {
  return Buffer.from(str)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}

/**
 * Base64 URL decoding (for JWT)
 * @param {string} str - Base64 URL encoded string
 * @returns {string} Decoded string
 */
function base64UrlDecode(str) {
  // Add padding if necessary
  str = str.replace(/-/g, '+').replace(/_/g, '/');
  while (str.length % 4 !== 0) {
    str += '=';
  }
  return Buffer.from(str, 'base64').toString('utf8');
}

module.exports = {
  generateJWT,
  validateJWT,
  verifyEd25519Signature,
  loadAgentIdentity,
  loadAgentIdentityByName,
  validateAgentIdentity,
  getFromCache,
  setInCache,
  clearCache
};
