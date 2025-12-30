/**
 * Agent Identity Management v3.0
 * Verifies agent identity using keypair-based authentication
 * Performance: <5ms per verification
 *
 * v3.0: Uses x- prefixed custom fields for Anthropic compliance
 * - Custom metadata fields should use x- prefix (e.g., x-category, x-role)
 * - Backward compatibility maintained for reading old format
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const IDENTITY_STORE = path.join(__dirname, '.identity-store.json');

class AgentIdentity {
  constructor() {
    this.identities = this.loadIdentities();
  }

  loadIdentities() {
    try {
      if (fs.existsSync(IDENTITY_STORE)) {
        return JSON.parse(fs.readFileSync(IDENTITY_STORE, 'utf8'));
      }
    } catch (error) {
      console.error('[Identity] Failed to load identities:', error.message);
    }
    return {};
  }

  saveIdentities() {
    try {
      fs.writeFileSync(IDENTITY_STORE, JSON.stringify(this.identities, null, 2));
    } catch (error) {
      console.error('[Identity] Failed to save identities:', error.message);
    }
  }

  /**
   * Register a new agent identity
   * v3.0: Normalizes metadata to use x- prefixed custom fields
   * @param {string} agentId - Agent identifier
   * @param {string} publicKey - Public key for verification
   * @param {object} metadata - Additional agent metadata (custom fields should use x- prefix)
   */
  register(agentId, publicKey, metadata = {}) {
    // v3.0: Normalize metadata to x- prefixed format
    const normalizedMetadata = this.normalizeMetadata(metadata);

    this.identities[agentId] = {
      publicKey,
      metadata: normalizedMetadata,
      'x-registered-at': new Date().toISOString(),
      'x-last-verified': null,
      'x-schema-version': '3.0'
    };
    this.saveIdentities();
    return { success: true, agentId };
  }

  /**
   * Normalize metadata to v3.0 x- prefixed format
   * @param {object} metadata - Raw metadata
   * @returns {object} Normalized metadata with x- prefixes
   */
  normalizeMetadata(metadata) {
    const normalized = {};
    const fieldsToPrefix = ['category', 'role', 'capabilities', 'team', 'tier', 'version'];

    for (const [key, value] of Object.entries(metadata)) {
      if (key.startsWith('x-')) {
        // Already in v3.0 format
        normalized[key] = value;
      } else if (fieldsToPrefix.includes(key)) {
        // Convert known custom fields to x- prefix
        normalized[`x-${key}`] = value;
      } else {
        // Keep other fields as-is (may be standard fields)
        normalized[key] = value;
      }
    }

    return normalized;
  }

  /**
   * Verify agent identity
   * @param {string} agentId - Agent identifier
   * @param {string} signature - Signed challenge
   * @param {string} challenge - Original challenge
   * @returns {object} Verification result
   */
  verify(agentId, signature = null, challenge = null) {
    const startTime = Date.now();

    if (!this.identities[agentId]) {
      return {
        verified: false,
        reason: 'Agent not registered',
        agentId,
        verificationTime: Date.now() - startTime
      };
    }

    // For now, allow agents without signature (trust on first use)
    // In production, require cryptographic signature verification
    if (!signature && !challenge) {
      this.identities[agentId].lastVerified = new Date().toISOString();
      this.saveIdentities();

      return {
        verified: true,
        agentId,
        metadata: this.identities[agentId].metadata,
        verificationTime: Date.now() - startTime
      };
    }

    // Cryptographic verification (if signature provided)
    try {
      const verifier = crypto.createVerify('SHA256');
      verifier.update(challenge);
      verifier.end();

      const isValid = verifier.verify(
        this.identities[agentId].publicKey,
        signature,
        'base64'
      );

      if (isValid) {
        this.identities[agentId].lastVerified = new Date().toISOString();
        this.saveIdentities();
      }

      return {
        verified: isValid,
        reason: isValid ? 'Signature valid' : 'Invalid signature',
        agentId,
        metadata: this.identities[agentId].metadata,
        verificationTime: Date.now() - startTime
      };
    } catch (error) {
      return {
        verified: false,
        reason: `Verification error: ${error.message}`,
        agentId,
        verificationTime: Date.now() - startTime
      };
    }
  }

  /**
   * Get agent metadata
   * @param {string} agentId - Agent identifier
   */
  getMetadata(agentId) {
    return this.identities[agentId]?.metadata || null;
  }

  /**
   * List all registered agents
   */
  listAgents() {
    return Object.keys(this.identities).map(agentId => ({
      agentId,
      metadata: this.identities[agentId].metadata,
      registeredAt: this.identities[agentId].registeredAt,
      lastVerified: this.identities[agentId].lastVerified
    }));
  }
}

module.exports = new AgentIdentity();
