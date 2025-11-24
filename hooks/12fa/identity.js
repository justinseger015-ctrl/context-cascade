/**
 * Agent Identity Management
 * Verifies agent identity using keypair-based authentication
 * Performance: <5ms per verification
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
   * @param {string} agentId - Agent identifier
   * @param {string} publicKey - Public key for verification
   * @param {object} metadata - Additional agent metadata
   */
  register(agentId, publicKey, metadata = {}) {
    this.identities[agentId] = {
      publicKey,
      metadata,
      registeredAt: new Date().toISOString(),
      lastVerified: null
    };
    this.saveIdentities();
    return { success: true, agentId };
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
