/**
 * MCP Session Manager
 * Enable/disable MCPs before starting a Claude session
 *
 * Workflow:
 * 1. Open Claude Code
 * 2. Open dashboard (localhost:8765)
 * 3. Select profile or individual MCPs
 * 4. Click "Apply" - updates .mcp.json
 * 5. Start typing in Claude
 */

const fs = require('fs');
const path = require('path');
const { EventEmitter } = require('events');

// Paths
const USER_HOME = process.env.USERPROFILE || process.env.HOME;
const CLAUDE_MCP_PATH = path.join(USER_HOME, '.claude', 'claude_desktop_config.json');
const PROJECT_MCP_PATH = path.join(__dirname, '..', '..', '.mcp.json');

// All available MCP configs
const MCP_CATALOG_PATHS = {
  catalog: path.join(__dirname, 'mcp-catalog.json'),
  complete: path.join(USER_HOME, 'MCP-SERVERS-COMPLETE-CONFIG.json'),
  universal: path.join(USER_HOME, 'MCP-UNIVERSAL-CONFIG.json'),
  codeQuality: path.join(USER_HOME, 'MCP-SITUATIONAL-CODE-QUALITY.json'),
  automation: path.join(USER_HOME, 'MCP-SITUATIONAL-AUTOMATION.json'),
  documentation: path.join(USER_HOME, 'MCP-SITUATIONAL-DOCUMENTATION.json'),
  payments: path.join(USER_HOME, 'MCP-SITUATIONAL-PAYMENTS.json')
};

/**
 * Profile definitions
 */
const PROFILES = {
  minimal: {
    name: 'Minimal',
    description: 'No MCPs - fastest startup',
    mcps: []
  },
  universal: {
    name: 'Universal',
    description: 'Core MCPs for general work',
    mcps: ['memory-mcp', 'fetch', 'sequential-thinking', 'filesystem']
  },
  codeReview: {
    name: 'Code Review',
    description: 'Code quality analysis tools',
    mcps: ['memory-mcp', 'connascence-analyzer', 'focused-changes', 'sequential-thinking']
  },
  research: {
    name: 'Research',
    description: 'Web fetching and memory',
    mcps: ['memory-mcp', 'fetch', 'sequential-thinking']
  },
  automation: {
    name: 'Automation',
    description: 'Browser automation with Playwright',
    mcps: ['memory-mcp', 'playwright', 'sequential-thinking']
  },
  documentation: {
    name: 'Documentation',
    description: 'Doc generation tools',
    mcps: ['memory-mcp', 'toc', 'sequential-thinking']
  },
  full: {
    name: 'Full Power',
    description: 'All MCPs enabled (high context cost)',
    mcps: ['memory-mcp', 'connascence-analyzer', 'fetch', 'sequential-thinking',
           'filesystem', 'playwright', 'agentic-payments', 'focused-changes', 'toc']
  }
};

/**
 * MCP Session Manager
 */
class MCPSessionManager extends EventEmitter {
  constructor() {
    super();
    this.catalog = {};      // All available MCPs
    this.active = {};       // Currently active MCPs
    this.profiles = PROFILES;
  }

  /**
   * Load all available MCPs from catalog files
   */
  loadCatalog() {
    this.catalog = {};
    this.categories = {};

    // Load from our catalog first (has the most complete list)
    if (fs.existsSync(MCP_CATALOG_PATHS.catalog)) {
      try {
        const catalogData = JSON.parse(fs.readFileSync(MCP_CATALOG_PATHS.catalog, 'utf8'));
        Object.assign(this.catalog, catalogData.mcpServers || {});
        this.categories = catalogData.categories || {};
        // Load profiles from catalog
        if (catalogData.profiles) {
          this.profiles = catalogData.profiles;
        }
      } catch (err) {
        this.emit('error', { error: `Failed to load catalog: ${err.message}` });
      }
    }

    // Load from complete config
    if (fs.existsSync(MCP_CATALOG_PATHS.complete)) {
      try {
        const config = JSON.parse(fs.readFileSync(MCP_CATALOG_PATHS.complete, 'utf8'));
        for (const [id, mcp] of Object.entries(config.mcpServers || {})) {
          if (!this.catalog[id]) {
            this.catalog[id] = mcp;
          }
        }
      } catch (err) {
        // Ignore
      }
    }

    // Load from other configs to fill gaps
    for (const [name, configPath] of Object.entries(MCP_CATALOG_PATHS)) {
      if (name === 'catalog' || name === 'complete') continue;
      if (fs.existsSync(configPath)) {
        try {
          const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
          for (const [id, mcp] of Object.entries(config.mcpServers || {})) {
            if (!this.catalog[id]) {
              this.catalog[id] = mcp;
            }
          }
        } catch (err) {
          // Ignore individual file errors
        }
      }
    }

    this.emit('catalog:loaded', { count: Object.keys(this.catalog).length });
    return this.catalog;
  }

  /**
   * Load currently active MCPs from project .mcp.json
   */
  loadActive() {
    this.active = {};

    if (fs.existsSync(PROJECT_MCP_PATH)) {
      try {
        const config = JSON.parse(fs.readFileSync(PROJECT_MCP_PATH, 'utf8'));
        this.active = config.mcpServers || {};
      } catch (err) {
        this.emit('error', { error: `Failed to load active config: ${err.message}` });
      }
    }

    this.emit('active:loaded', { count: Object.keys(this.active).length });
    return this.active;
  }

  /**
   * Get all available MCPs with their status
   */
  getAllMCPs() {
    const mcps = [];

    for (const [id, config] of Object.entries(this.catalog)) {
      mcps.push({
        id,
        enabled: id in this.active,
        type: this.detectType(config),
        command: config.command,
        package: this.extractPackage(config)
      });
    }

    return mcps;
  }

  /**
   * Detect MCP type from config
   */
  detectType(config) {
    if (config.command === 'npx') return 'npx';
    if (config.command?.includes('python')) return 'python';
    if (config.command === 'node') return 'node';
    if (config.command === 'cmd') return 'cmd';
    return 'unknown';
  }

  /**
   * Extract package name from config
   */
  extractPackage(config) {
    if (config.args && config.args.length > 0) {
      const first = config.args[0];
      if (first.startsWith('@') || !first.startsWith('-')) {
        return first;
      }
    }
    return null;
  }

  /**
   * Enable an MCP
   * @param {string} mcpId - MCP identifier
   */
  enable(mcpId) {
    if (!this.catalog[mcpId]) {
      this.emit('error', { error: `MCP ${mcpId} not in catalog` });
      return false;
    }

    this.active[mcpId] = this.catalog[mcpId];
    this.emit('mcp:enabled', { mcpId });
    return true;
  }

  /**
   * Disable an MCP
   * @param {string} mcpId - MCP identifier
   */
  disable(mcpId) {
    if (this.active[mcpId]) {
      delete this.active[mcpId];
      this.emit('mcp:disabled', { mcpId });
      return true;
    }
    return false;
  }

  /**
   * Apply a profile
   * @param {string} profileId - Profile identifier
   */
  applyProfile(profileId) {
    const profile = this.profiles[profileId];
    if (!profile) {
      this.emit('error', { error: `Profile ${profileId} not found` });
      return false;
    }

    // Clear current active
    this.active = {};

    // Enable profile MCPs
    for (const mcpId of profile.mcps) {
      if (this.catalog[mcpId]) {
        this.active[mcpId] = this.catalog[mcpId];
      }
    }

    this.emit('profile:applied', { profileId, mcpCount: Object.keys(this.active).length });
    return true;
  }

  /**
   * Save current active MCPs to .mcp.json
   */
  save() {
    const config = { mcpServers: this.active };

    try {
      fs.writeFileSync(PROJECT_MCP_PATH, JSON.stringify(config, null, 2));
      this.emit('config:saved', { path: PROJECT_MCP_PATH, count: Object.keys(this.active).length });
      return true;
    } catch (err) {
      this.emit('error', { error: `Failed to save: ${err.message}` });
      return false;
    }
  }

  /**
   * Get current status
   */
  getStatus() {
    return {
      catalogCount: Object.keys(this.catalog).length,
      activeCount: Object.keys(this.active).length,
      activeMCPs: Object.keys(this.active),
      profiles: Object.keys(this.profiles)
    };
  }

  /**
   * Estimate context cost
   */
  estimateContextCost() {
    // Rough estimates per MCP type
    const costs = {
      'memory-mcp': 2000,
      'connascence-analyzer': 1500,
      'fetch': 500,
      'sequential-thinking': 800,
      'filesystem': 1000,
      'playwright': 2000,
      'agentic-payments': 1000,
      'focused-changes': 800,
      'toc': 500
    };

    let total = 0;
    for (const mcpId of Object.keys(this.active)) {
      total += costs[mcpId] || 500;
    }

    return {
      tokens: total,
      percentage: Math.round((total / 200000) * 100 * 10) / 10  // Assume 200k context
    };
  }
}

/**
 * Generate session manager HTML page
 */
function generateSessionManagerHTML(manager) {
  const mcps = manager.getAllMCPs();
  const status = manager.getStatus();
  const cost = manager.estimateContextCost();

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MCP Session Manager</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #0a0a0a;
      color: #e0e0e0;
      padding: 20px;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    h1 { color: #4fc3f7; margin-bottom: 10px; }
    .subtitle { color: #888; margin-bottom: 30px; }

    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    @media (max-width: 800px) { .grid { grid-template-columns: 1fr; } }

    .card {
      background: #1a1a1a;
      border-radius: 8px;
      padding: 20px;
      border: 1px solid #333;
    }
    .card h2 {
      color: #81d4fa;
      font-size: 1rem;
      margin-bottom: 15px;
      padding-bottom: 10px;
      border-bottom: 1px solid #333;
    }

    .profile-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; }
    .profile-btn {
      background: #252525;
      border: 1px solid #444;
      border-radius: 6px;
      padding: 12px;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s;
    }
    .profile-btn:hover { background: #333; border-color: #4fc3f7; }
    .profile-btn.active { background: #1e3a5f; border-color: #4fc3f7; }
    .profile-name { font-weight: 600; color: #e0e0e0; }
    .profile-desc { font-size: 0.75rem; color: #888; margin-top: 4px; }

    .mcp-list { max-height: 400px; overflow-y: auto; }
    .mcp-item {
      display: flex;
      align-items: center;
      padding: 10px;
      border-bottom: 1px solid #333;
    }
    .mcp-item:last-child { border-bottom: none; }
    .mcp-toggle {
      width: 44px;
      height: 24px;
      background: #333;
      border-radius: 12px;
      position: relative;
      cursor: pointer;
      transition: background 0.2s;
    }
    .mcp-toggle.on { background: #1e88e5; }
    .mcp-toggle::after {
      content: '';
      position: absolute;
      width: 20px;
      height: 20px;
      background: white;
      border-radius: 50%;
      top: 2px;
      left: 2px;
      transition: left 0.2s;
    }
    .mcp-toggle.on::after { left: 22px; }
    .mcp-info { margin-left: 15px; flex: 1; }
    .mcp-name { font-weight: 600; }
    .mcp-type { font-size: 0.75rem; color: #888; }

    .cost-bar {
      height: 8px;
      background: #333;
      border-radius: 4px;
      overflow: hidden;
      margin: 10px 0;
    }
    .cost-fill {
      height: 100%;
      background: linear-gradient(90deg, #4caf50, #ffeb3b, #f44336);
      transition: width 0.3s;
    }
    .cost-text { font-size: 0.85rem; color: #888; }

    .actions {
      margin-top: 20px;
      display: flex;
      gap: 10px;
    }
    .btn {
      padding: 12px 24px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 1rem;
      font-weight: 600;
    }
    .btn-primary { background: #1e88e5; color: white; }
    .btn-primary:hover { background: #1565c0; }
    .btn-secondary { background: #333; color: #e0e0e0; border: 1px solid #444; }
    .btn-secondary:hover { background: #444; }

    .status {
      background: #1b5e20;
      color: #a5d6a7;
      padding: 10px 15px;
      border-radius: 6px;
      margin-top: 20px;
      display: none;
    }
    .status.show { display: block; }
  </style>
</head>
<body>
  <div class="container">
    <h1>MCP Session Manager</h1>
    <p class="subtitle">Enable MCPs before you start typing in Claude</p>

    <div class="grid">
      <div class="card">
        <h2>Quick Profiles</h2>
        <div class="profile-grid">
          ${Object.entries(manager.profiles).map(([id, p]) => `
          <button class="profile-btn" data-profile="${id}" onclick="applyProfile('${id}')">
            <div class="profile-name">${p.name}</div>
            <div class="profile-desc">${p.mcps.length} MCPs</div>
          </button>
          `).join('')}
        </div>
      </div>

      <div class="card">
        <h2>Context Cost Estimate</h2>
        <div class="cost-bar">
          <div class="cost-fill" id="costFill" style="width: ${Math.min(cost.percentage, 100)}%"></div>
        </div>
        <p class="cost-text">
          <span id="tokenCount">${cost.tokens.toLocaleString()}</span> tokens
          (<span id="tokenPct">${cost.percentage}</span>% of context)
        </p>
        <p class="cost-text" style="margin-top: 10px;">
          Active: <strong id="activeCount">${status.activeCount}</strong> / ${status.catalogCount} MCPs
        </p>
      </div>
    </div>

    <div class="card" style="margin-top: 20px;">
      <h2>Individual MCPs</h2>
      <div class="mcp-list">
        ${mcps.map(m => `
        <div class="mcp-item">
          <div class="mcp-toggle ${m.enabled ? 'on' : ''}" data-mcp="${m.id}" onclick="toggleMCP('${m.id}')"></div>
          <div class="mcp-info">
            <div class="mcp-name">${m.id}</div>
            <div class="mcp-type">${m.type} ${m.package ? '- ' + m.package : ''}</div>
          </div>
        </div>
        `).join('')}
      </div>
    </div>

    <div class="actions">
      <button class="btn btn-primary" onclick="saveConfig()">Apply & Save</button>
      <button class="btn btn-secondary" onclick="location.reload()">Reset</button>
    </div>

    <div class="status" id="status"></div>
  </div>

  <script>
    let activeMCPs = new Set(${JSON.stringify(status.activeMCPs)});
    const costs = {
      'memory-mcp': 2000,
      'connascence-analyzer': 1500,
      'fetch': 500,
      'sequential-thinking': 800,
      'filesystem': 1000,
      'playwright': 2000,
      'agentic-payments': 1000,
      'focused-changes': 800,
      'toc': 500
    };

    function toggleMCP(id) {
      const toggle = document.querySelector(\`.mcp-toggle[data-mcp="\${id}"]\`);
      if (activeMCPs.has(id)) {
        activeMCPs.delete(id);
        toggle.classList.remove('on');
      } else {
        activeMCPs.add(id);
        toggle.classList.add('on');
      }
      updateCost();
    }

    function applyProfile(profileId) {
      fetch('/api/session/profile/' + profileId, { method: 'POST' })
        .then(r => r.json())
        .then(data => {
          activeMCPs = new Set(data.activeMCPs || []);
          document.querySelectorAll('.mcp-toggle').forEach(t => {
            t.classList.toggle('on', activeMCPs.has(t.dataset.mcp));
          });
          document.querySelectorAll('.profile-btn').forEach(b => {
            b.classList.toggle('active', b.dataset.profile === profileId);
          });
          updateCost();
          showStatus('Profile applied: ' + profileId);
        });
    }

    function updateCost() {
      let total = 0;
      activeMCPs.forEach(id => { total += costs[id] || 500; });
      const pct = Math.round((total / 200000) * 100 * 10) / 10;
      document.getElementById('tokenCount').textContent = total.toLocaleString();
      document.getElementById('tokenPct').textContent = pct;
      document.getElementById('costFill').style.width = Math.min(pct, 100) + '%';
      document.getElementById('activeCount').textContent = activeMCPs.size;
    }

    function saveConfig() {
      fetch('/api/session/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mcps: Array.from(activeMCPs) })
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          showStatus('Saved! ' + data.count + ' MCPs active. Start typing in Claude now.');
        }
      });
    }

    function showStatus(msg) {
      const el = document.getElementById('status');
      el.textContent = msg;
      el.classList.add('show');
      setTimeout(() => el.classList.remove('show'), 5000);
    }
  </script>
</body>
</html>`;
}

// Export
module.exports = {
  MCPSessionManager,
  PROFILES,
  MCP_CATALOG_PATHS,
  generateSessionManagerHTML
};

// Test if run directly
if (require.main === module) {
  const manager = new MCPSessionManager();

  manager.on('catalog:loaded', (d) => console.log(`[Session] Catalog: ${d.count} MCPs`));
  manager.on('active:loaded', (d) => console.log(`[Session] Active: ${d.count} MCPs`));
  manager.on('profile:applied', (d) => console.log(`[Session] Profile ${d.profileId}: ${d.mcpCount} MCPs`));

  manager.loadCatalog();
  manager.loadActive();

  console.log('\n[Session] Status:', manager.getStatus());
  console.log('[Session] Cost:', manager.estimateContextCost());
  console.log('\n[Session] Available Profiles:');
  for (const [id, p] of Object.entries(PROFILES)) {
    console.log(`  ${id}: ${p.name} (${p.mcps.length} MCPs)`);
  }
}
