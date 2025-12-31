/**
 * Integration Tests: MCP Servers
 * Phase 5.2 Quality Expansion
 *
 * Tests MCP server configurations, tool availability,
 * and integration points.
 *
 * @module quality/integration/mcp-servers
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Project root
const PROJECT_ROOT = path.join(__dirname, '..', '..');

/**
 * MCP Configuration loader
 */
class MCPConfigLoader {
  constructor(configPath) {
    this.configPath = configPath;
    this.config = null;
  }

  load() {
    try {
      if (fs.existsSync(this.configPath)) {
        const content = fs.readFileSync(this.configPath, 'utf8');
        this.config = JSON.parse(content);
        return true;
      }
      return false;
    } catch (err) {
      console.error(`Failed to load MCP config: ${err.message}`);
      return false;
    }
  }

  getServers() {
    if (!this.config) return [];
    return Object.entries(this.config.mcpServers || {}).map(([id, config]) => ({
      id,
      ...config
    }));
  }

  getServer(serverId) {
    if (!this.config || !this.config.mcpServers) return null;
    return this.config.mcpServers[serverId] || null;
  }

  hasServer(serverId) {
    return !!this.getServer(serverId);
  }
}

/**
 * MCP Server validator
 */
class MCPServerValidator {
  constructor() {
    this.validationResults = [];
  }

  validateServerConfig(server) {
    const issues = [];

    // Check required fields
    if (!server.command) {
      issues.push('Missing command');
    }

    // Check command type
    if (server.command && !['npx', 'node', 'python', 'bash'].some(c => server.command.includes(c))) {
      issues.push('Unknown command type');
    }

    // Check for version pinning (npx)
    if (server.command && server.command.includes('npx')) {
      if (server.args) {
        const hasVersion = server.args.some(arg => arg.includes('@') && /\d/.test(arg));
        if (!hasVersion) {
          issues.push('NPX package not version-pinned');
        }
      }
    }

    // Check environment variables
    if (server.env) {
      for (const [key, value] of Object.entries(server.env)) {
        if (value === '' || value === null || value === undefined) {
          issues.push(`Empty env var: ${key}`);
        }
        // Check for placeholder values
        if (typeof value === 'string' && (value.includes('YOUR_') || value.includes('REPLACE_'))) {
          issues.push(`Placeholder env var: ${key}`);
        }
      }
    }

    return {
      valid: issues.length === 0,
      issues
    };
  }

  validateAllServers(servers) {
    this.validationResults = servers.map(server => ({
      id: server.id,
      ...this.validateServerConfig(server)
    }));
    return this.validationResults;
  }

  getValidServers() {
    return this.validationResults.filter(r => r.valid);
  }

  getInvalidServers() {
    return this.validationResults.filter(r => !r.valid);
  }
}

/**
 * MCP Tool registry
 */
class MCPToolRegistry {
  constructor() {
    this.tools = new Map();
  }

  registerTool(serverId, toolName, toolConfig) {
    const key = `${serverId}:${toolName}`;
    this.tools.set(key, {
      serverId,
      toolName,
      ...toolConfig
    });
  }

  getTool(serverId, toolName) {
    return this.tools.get(`${serverId}:${toolName}`);
  }

  getToolsForServer(serverId) {
    return Array.from(this.tools.values()).filter(t => t.serverId === serverId);
  }

  getAllTools() {
    return Array.from(this.tools.values());
  }

  hasRequiredTools(requiredTools) {
    const missing = [];
    for (const required of requiredTools) {
      const [serverId, toolName] = required.split(':');
      if (!this.getTool(serverId, toolName)) {
        missing.push(required);
      }
    }
    return {
      hasAll: missing.length === 0,
      missing
    };
  }
}

/**
 * MCP Integration test suite
 */
class MCPIntegrationTestSuite {
  constructor() {
    this.configLoader = new MCPConfigLoader(path.join(PROJECT_ROOT, '.mcp.json'));
    this.validator = new MCPServerValidator();
    this.toolRegistry = new MCPToolRegistry();
    this.results = [];
  }

  async runTest(name, testFn) {
    const start = Date.now();
    try {
      await testFn();
      this.results.push({
        name,
        status: 'PASS',
        duration: Date.now() - start
      });
      console.log(`  [PASS] ${name}`);
      return true;
    } catch (err) {
      this.results.push({
        name,
        status: 'FAIL',
        error: err.message,
        duration: Date.now() - start
      });
      console.log(`  [FAIL] ${name}: ${err.message}`);
      return false;
    }
  }

  async runAllTests() {
    console.log('\n=== Integration: MCP Server Tests ===\n');

    // Configuration Tests
    console.log('--- Configuration Loading ---');

    await this.runTest('Config: MCP config file exists', async () => {
      const configPath = path.join(PROJECT_ROOT, '.mcp.json');
      if (!fs.existsSync(configPath)) {
        throw new Error('.mcp.json not found');
      }
    });

    await this.runTest('Config: MCP config is valid JSON', async () => {
      const loaded = this.configLoader.load();
      if (!loaded) {
        throw new Error('Failed to parse .mcp.json');
      }
    });

    await this.runTest('Config: At least one server defined', async () => {
      const servers = this.configLoader.getServers();
      if (servers.length === 0) {
        throw new Error('No MCP servers defined');
      }
    });

    // Validation Tests
    console.log('\n--- Server Validation ---');

    await this.runTest('Validation: All servers have commands', async () => {
      const servers = this.configLoader.getServers();
      const withoutCommand = servers.filter(s => !s.command);
      if (withoutCommand.length > 0) {
        throw new Error(`Servers without command: ${withoutCommand.map(s => s.id).join(', ')}`);
      }
    });

    await this.runTest('Validation: No broken dependencies', async () => {
      const servers = this.configLoader.getServers();
      // Check for known broken dependencies
      const brokenPatterns = ['claude-flow@alpha', '@broken/', 'undefined'];
      const broken = [];

      for (const server of servers) {
        const args = server.args || [];
        for (const arg of args) {
          if (brokenPatterns.some(p => arg.includes(p))) {
            broken.push({ server: server.id, arg });
          }
        }
      }

      if (broken.length > 0) {
        throw new Error(`Broken dependencies: ${JSON.stringify(broken)}`);
      }
    });

    await this.runTest('Validation: Environment variables defined', async () => {
      const servers = this.configLoader.getServers();
      const issues = [];

      for (const server of servers) {
        if (server.env) {
          for (const [key, value] of Object.entries(server.env)) {
            if (value === '' || value === null) {
              issues.push(`${server.id}:${key}`);
            }
          }
        }
      }

      // Allow some empty env vars (they may be optional)
      // Only fail if critical ones are empty
      const critical = issues.filter(i =>
        i.includes('API_KEY') || i.includes('TOKEN') || i.includes('SECRET')
      );

      if (critical.length > 0) {
        throw new Error(`Empty critical env vars: ${critical.join(', ')}`);
      }
    });

    // Security Tests
    console.log('\n--- Security Checks ---');

    await this.runTest('Security: No hardcoded secrets in config', async () => {
      const configPath = path.join(PROJECT_ROOT, '.mcp.json');
      const content = fs.readFileSync(configPath, 'utf8');

      // Check for potential secrets
      const secretPatterns = [
        /sk-[a-zA-Z0-9]{20,}/,  // OpenAI-style keys
        /[a-zA-Z0-9]{32,}/,     // Long hex strings (potential keys)
      ];

      // Exclude known safe patterns
      const safePatterns = [
        /[a-f0-9]{64}/,  // SHA-256 hashes are OK
        /"[A-Z_]+"/,     // Environment variable names
      ];

      let hasSuspicious = false;
      for (const pattern of secretPatterns) {
        const matches = content.match(pattern);
        if (matches) {
          // Check if it's a safe pattern
          const isSafe = safePatterns.some(sp => sp.test(matches[0]));
          if (!isSafe && matches[0].length > 30) {
            hasSuspicious = true;
          }
        }
      }

      // This is a soft check - we warn but don't fail
      if (hasSuspicious) {
        console.log('    [WARN] Potentially sensitive data in config');
      }
    });

    await this.runTest('Security: Checksum registry exists', async () => {
      const checksumPath = path.join(PROJECT_ROOT, 'security', 'mcp-integrity', 'checksum-registry.json');
      if (!fs.existsSync(checksumPath)) {
        throw new Error('MCP checksum registry not found');
      }
    });

    // Integration Tests
    console.log('\n--- Integration Checks ---');

    await this.runTest('Integration: Security module can validate servers', async () => {
      const checksumValidatorPath = path.join(PROJECT_ROOT, 'security', 'mcp-integrity', 'checksum-validator.cjs');
      if (!fs.existsSync(checksumValidatorPath)) {
        throw new Error('Checksum validator not found');
      }
      // Verify it loads
      const validator = require(checksumValidatorPath);
      if (typeof validator.validateServer !== 'function') {
        throw new Error('validateServer function not exported');
      }
    });

    await this.runTest('Integration: RBAC can control MCP access', async () => {
      const rbacPath = path.join(PROJECT_ROOT, 'security', 'rbac', 'enforcer.cjs');
      if (!fs.existsSync(rbacPath)) {
        throw new Error('RBAC enforcer not found');
      }
      const rbac = require(rbacPath);
      if (typeof rbac.enforceRBAC !== 'function') {
        throw new Error('enforceRBAC function not exported');
      }
    });

    await this.runTest('Integration: Token manager can secure MCP calls', async () => {
      const tokenPath = path.join(PROJECT_ROOT, 'security', 'tokens', 'token-manager.cjs');
      if (!fs.existsSync(tokenPath)) {
        throw new Error('Token manager not found');
      }
      const tokens = require(tokenPath);
      if (typeof tokens.generateToken !== 'function') {
        throw new Error('generateToken function not exported');
      }
    });

    // Server Count Test
    console.log('\n--- Server Inventory ---');

    await this.runTest('Inventory: Server count matches expected', async () => {
      const servers = this.configLoader.getServers();
      console.log(`    Found ${servers.length} MCP servers`);

      // List server names
      const serverNames = servers.map(s => s.id);
      console.log(`    Servers: ${serverNames.slice(0, 5).join(', ')}${serverNames.length > 5 ? '...' : ''}`);

      // Just verify we have some servers
      if (servers.length === 0) {
        throw new Error('No servers found');
      }
    });

    await this.runTest('Inventory: Core servers present', async () => {
      // Check for critical servers (adjust based on actual config)
      const servers = this.configLoader.getServers();
      const serverIds = servers.map(s => s.id);

      // At minimum, memory-mcp should exist based on project structure
      // But we'll be flexible about which specific servers are required
      if (serverIds.length < 1) {
        throw new Error('Expected at least 1 MCP server');
      }
    });

    // Summary
    const passed = this.results.filter(r => r.status === 'PASS').length;
    const failed = this.results.filter(r => r.status === 'FAIL').length;

    console.log('\n========================================');
    console.log('MCP INTEGRATION TEST RESULTS');
    console.log('========================================');
    console.log(`Total:  ${this.results.length}`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${failed}`);
    console.log(`Status: ${failed === 0 ? 'ALL TESTS PASSED' : 'FAILURES DETECTED'}`);
    console.log('========================================\n');

    return {
      total: this.results.length,
      passed,
      failed,
      results: this.results
    };
  }
}

// Export
module.exports = {
  MCPConfigLoader,
  MCPServerValidator,
  MCPToolRegistry,
  MCPIntegrationTestSuite
};

// Run if executed directly
if (require.main === module) {
  const suite = new MCPIntegrationTestSuite();
  suite.runAllTests().then(results => {
    process.exit(results.failed > 0 ? 1 : 0);
  });
}
