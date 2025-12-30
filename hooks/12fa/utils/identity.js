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
 * - Anthropic-compliant format support (x- prefixed custom fields)
 *
 * @module hooks/12fa/utils/identity
 * @version 2.0.0
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
 * Supports both Anthropic-compliant format (x- prefixed) and legacy format
 *
 * Anthropic Official Fields:
 * - name (required)
 * - description (required)
 * - tools (required, comma-separated)
 * - model (optional: opus, sonnet, haiku)
 *
 * Custom Extensions (x- prefixed):
 * - x-agent_id (UUID v4)
 * - x-role (admin, developer, reviewer, etc.)
 * - x-capabilities (array)
 * - x-rbac (object with denied_tools, path_scopes, api_access)
 * - x-budget (object with max_tokens_per_session, max_cost_per_day)
 * - x-metadata (object with category, tags, version)
 *
 * @param {string} agentFilePath - Absolute path to agent .md file
 * @returns {Object|null} Agent identity object or null if invalid
 */
function loadAgentIdentity(agentFilePath) {
  try {
    // Read file contents
    const fileContents = fs.readFileSync(agentFilePath, 'utf8');

    // Extract frontmatter (YAML between --- delimiters)
    const frontmatterMatch = fileContents.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!frontmatterMatch) {
      console.error(`No frontmatter found in ${agentFilePath}`);
      return null;
    }

    const frontmatter = yaml.load(frontmatterMatch[1]);

    // Check for Anthropic-compliant format (x- prefixed fields)
    const isAnthropicFormat = frontmatter['x-agent_id'] || frontmatter['x-role'];

    // Extract agent_id (new format: x-agent_id, old format: identity.agent_id)
    const agentId = isAnthropicFormat
      ? frontmatter['x-agent_id']
      : (frontmatter.identity && frontmatter.identity.agent_id);

    // Extract role (new format: x-role, old format: identity.role)
    const role = isAnthropicFormat
      ? frontmatter['x-role']
      : (frontmatter.identity && frontmatter.identity.role);

    // Validate required Anthropic official fields
    if (!frontmatter.name) {
      console.error(`Missing name in ${agentFilePath}`);
      return null;
    }

    // agent_id and role are optional in Anthropic format but required for RBAC
    // Generate a deterministic ID from name if not provided
    let finalAgentId = agentId;
    if (!finalAgentId) {
      // Generate deterministic UUID from name for backward compatibility
      const hash = crypto.createHash('md5').update(frontmatter.name).digest('hex');
      finalAgentId = `${hash.slice(0,8)}-${hash.slice(8,12)}-4${hash.slice(13,16)}-8${hash.slice(17,20)}-${hash.slice(20,32)}`;
    }

    // Validate agent_id format (UUID v4) if provided
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    if (agentId && !uuidRegex.test(agentId)) {
      console.error(`Invalid UUID v4 format for agent_id in ${agentFilePath}`);
      return null;
    }

    // Default role if not specified
    const finalRole = role || 'developer';

    // Extract capabilities (new format: x-capabilities, old format: capabilities)
    const capabilities = isAnthropicFormat
      ? (frontmatter['x-capabilities'] || [])
      : (frontmatter.capabilities || []);

    // Extract RBAC (new format: x-rbac, old format: rbac)
    const rbac = isAnthropicFormat
      ? (frontmatter['x-rbac'] || {})
      : (frontmatter.rbac || {});

    // Extract budget (new format: x-budget, old format: budget)
    const budget = isAnthropicFormat
      ? (frontmatter['x-budget'] || {})
      : (frontmatter.budget || {});

    // Extract metadata (new format: x-metadata, old format: metadata)
    const metadata = isAnthropicFormat
      ? (frontmatter['x-metadata'] || {})
      : (frontmatter.metadata || {});

    // Construct identity object
    const identity = {
      agent_id: finalAgentId,
      name: frontmatter.name,
      description: frontmatter.description || '',
      tools: frontmatter.tools || '',
      model: frontmatter.model || 'sonnet',
      role: finalRole,
      capabilities: capabilities,
      rbac: rbac,
      budget: budget,
      metadata: metadata,
      file_path: agentFilePath,
      format: isAnthropicFormat ? 'anthropic' : 'legacy'
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
 * Validate agent identity against Anthropic-compliant schema
 * @param {Object} identity - Agent identity object
 * @returns {Object} Validation result {valid: boolean, errors: string[], warnings: string[]}
 */
function validateAgentIdentity(identity) {
  const errors = [];
  const warnings = [];

  // Required Anthropic official fields
  if (!identity.name) {
    errors.push('Missing name (Anthropic required field)');
  }

  // Description is required in Anthropic format but we'll warn if missing
  if (!identity.description) {
    warnings.push('Missing description (Anthropic required field)');
  }

  // Tools is required in Anthropic format but we'll warn if missing
  if (!identity.tools) {
    warnings.push('Missing tools (Anthropic required field)');
  }

  // agent_id can be auto-generated, so only validate format if provided
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
    warnings.push(`Non-standard role: ${identity.role}. Standard roles: ${validRoles.join(', ')}`);
  }

  // Validate model if provided
  const validModels = ['opus', 'sonnet', 'haiku'];
  if (identity.model && !validModels.includes(identity.model)) {
    warnings.push(`Non-standard model: ${identity.model}. Valid models: ${validModels.join(', ')}`);
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings
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
