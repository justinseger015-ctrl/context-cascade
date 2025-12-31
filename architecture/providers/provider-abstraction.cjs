/**
 * Provider Abstraction Layer
 * Phase 4.2 Architecture Optimization
 *
 * Unified interface for multiple AI providers (Claude, Codex, Gemini).
 * Enables provider-agnostic task execution and model routing.
 *
 * @module architecture/providers/provider-abstraction
 */

const { exec } = require('child_process');
const path = require('path');

/**
 * Provider configurations
 */
const PROVIDERS = {
  claude: {
    id: 'claude',
    name: 'Claude (Anthropic)',
    type: 'native',
    strengths: ['complex_reasoning', 'code_generation', 'analysis', 'safety'],
    contextWindow: 200000,
    costTier: 'high',
    available: true, // Always available as native
    checkCommand: null
  },

  codex: {
    id: 'codex',
    name: 'Codex CLI (OpenAI)',
    type: 'cli',
    strengths: ['autonomous_coding', 'sandbox_execution', 'iteration'],
    contextWindow: 128000,
    costTier: 'medium',
    available: null, // Check at runtime
    checkCommand: 'bash -lc "command -v codex && codex --version"',
    execCommand: 'bash -lc "codex {mode} exec \'{task}\'"',
    modes: {
      default: '',
      fullAuto: '--full-auto',
      yolo: '--yolo',
      sandbox: '--sandbox read-only'
    }
  },

  gemini: {
    id: 'gemini',
    name: 'Gemini CLI (Google)',
    type: 'cli',
    strengths: ['web_search', 'mega_context', 'multimodal', 'current_info'],
    contextWindow: 1000000,
    costTier: 'medium',
    available: null, // Check at runtime
    checkCommand: 'bash -lc "command -v gemini && gemini --version"',
    execCommand: 'bash -lc "gemini {options} \'{query}\'"',
    options: {
      default: '',
      allFiles: '--all-files',
      json: '-o json'
    }
  }
};

/**
 * Task-to-provider routing rules
 */
const ROUTING_RULES = {
  // Research tasks - Gemini preferred for web search
  research: {
    preferred: 'gemini',
    fallback: 'claude',
    reason: 'Google Search grounding for current information'
  },

  // Large codebase analysis - Gemini preferred for 1M context
  megacontext: {
    preferred: 'gemini',
    fallback: 'claude',
    reason: '1M token context window'
  },

  // Autonomous coding iteration - Codex preferred
  autonomous: {
    preferred: 'codex',
    fallback: 'claude',
    reason: 'Full-auto and YOLO modes for iteration'
  },

  // Sandboxed execution - Codex preferred
  sandbox: {
    preferred: 'codex',
    fallback: 'claude',
    reason: 'OS-level sandbox isolation'
  },

  // Complex reasoning - Claude preferred
  reasoning: {
    preferred: 'claude',
    fallback: 'gemini',
    reason: 'Multi-step logic and analysis'
  },

  // Safety-critical - Claude preferred
  safety: {
    preferred: 'claude',
    fallback: null,
    reason: 'Constitutional AI safety guarantees'
  },

  // Default
  default: {
    preferred: 'claude',
    fallback: 'codex',
    reason: 'Default to native provider'
  }
};

/**
 * Provider availability cache
 */
const availabilityCache = {
  codex: null,
  gemini: null,
  lastCheck: null
};

/**
 * Check if a CLI provider is available
 * @param {string} providerId - Provider ID
 * @returns {Promise<Object>} Availability result
 */
async function checkProviderAvailability(providerId) {
  const provider = PROVIDERS[providerId];

  if (!provider) {
    return { available: false, error: 'Unknown provider' };
  }

  if (provider.type === 'native') {
    return { available: true, version: 'native' };
  }

  if (!provider.checkCommand) {
    return { available: false, error: 'No check command' };
  }

  return new Promise((resolve) => {
    exec(provider.checkCommand, { timeout: 10000 }, (error, stdout, stderr) => {
      if (error) {
        resolve({
          available: false,
          error: error.message,
          stderr
        });
      } else {
        resolve({
          available: true,
          version: stdout.trim().split('\n').pop(),
          path: stdout.trim().split('\n')[0]
        });
      }
    });
  });
}

/**
 * Check all providers
 * @returns {Promise<Object>} All provider statuses
 */
async function checkAllProviders() {
  const results = {};

  for (const providerId of Object.keys(PROVIDERS)) {
    results[providerId] = await checkProviderAvailability(providerId);
    PROVIDERS[providerId].available = results[providerId].available;
  }

  availabilityCache.lastCheck = new Date().toISOString();

  return results;
}

/**
 * Get best provider for a task type
 * @param {string} taskType - Type of task
 * @returns {Object} Provider recommendation
 */
async function getBestProvider(taskType) {
  const rule = ROUTING_RULES[taskType] || ROUTING_RULES.default;

  // Check preferred provider availability
  const preferredCheck = await checkProviderAvailability(rule.preferred);

  if (preferredCheck.available) {
    return {
      provider: PROVIDERS[rule.preferred],
      reason: rule.reason,
      isPreferred: true
    };
  }

  // Try fallback
  if (rule.fallback) {
    const fallbackCheck = await checkProviderAvailability(rule.fallback);

    if (fallbackCheck.available) {
      return {
        provider: PROVIDERS[rule.fallback],
        reason: `Fallback: ${rule.preferred} not available`,
        isPreferred: false
      };
    }
  }

  // Default to Claude (always available)
  return {
    provider: PROVIDERS.claude,
    reason: 'Default fallback to native provider',
    isPreferred: false
  };
}

/**
 * Execute task with a specific provider
 * @param {string} providerId - Provider to use
 * @param {string} task - Task description
 * @param {Object} options - Execution options
 * @returns {Promise<Object>} Execution result
 */
async function executeWithProvider(providerId, task, options = {}) {
  const provider = PROVIDERS[providerId];

  if (!provider) {
    return { success: false, error: 'Unknown provider' };
  }

  // For Claude, return instruction (native execution)
  if (provider.type === 'native') {
    return {
      success: true,
      provider: providerId,
      type: 'native',
      instruction: `Execute task: ${task}`,
      message: 'Native provider - execute directly'
    };
  }

  // For CLI providers, build and execute command
  const availability = await checkProviderAvailability(providerId);
  if (!availability.available) {
    return {
      success: false,
      error: `Provider ${providerId} not available`,
      details: availability
    };
  }

  let command = provider.execCommand;

  // Apply mode/options
  if (providerId === 'codex') {
    const mode = options.mode || 'default';
    command = command.replace('{mode}', provider.modes[mode] || '');
  } else if (providerId === 'gemini') {
    const opt = options.option || 'default';
    command = command.replace('{options}', provider.options[opt] || '');
  }

  // Replace task placeholder
  command = command.replace('{task}', task.replace(/'/g, "'\\''"));
  command = command.replace('{query}', task.replace(/'/g, "'\\''"));

  const timeout = options.timeout || 300000; // 5 min default

  return new Promise((resolve) => {
    exec(command, { timeout }, (error, stdout, stderr) => {
      resolve({
        success: !error,
        provider: providerId,
        type: 'cli',
        command,
        stdout: stdout || '',
        stderr: stderr || '',
        error: error ? error.message : null,
        exitCode: error ? error.code : 0
      });
    });
  });
}

/**
 * Route and execute task automatically
 * @param {string} task - Task description
 * @param {Object} options - Options including taskType
 * @returns {Promise<Object>} Execution result
 */
async function routeAndExecute(task, options = {}) {
  const taskType = options.taskType || detectTaskType(task);
  const recommendation = await getBestProvider(taskType);

  return {
    routing: {
      taskType,
      selectedProvider: recommendation.provider.id,
      reason: recommendation.reason,
      isPreferred: recommendation.isPreferred
    },
    execution: await executeWithProvider(
      recommendation.provider.id,
      task,
      options
    )
  };
}

/**
 * Detect task type from description
 * @param {string} task - Task description
 * @returns {string} Detected task type
 */
function detectTaskType(task) {
  const lower = task.toLowerCase();

  if (lower.includes('search') || lower.includes('research') || lower.includes('current') || lower.includes('latest')) {
    return 'research';
  }
  if (lower.includes('analyze entire') || lower.includes('whole codebase') || lower.includes('all files')) {
    return 'megacontext';
  }
  if (lower.includes('autonomous') || lower.includes('iterate') || lower.includes('full-auto')) {
    return 'autonomous';
  }
  if (lower.includes('sandbox') || lower.includes('isolated') || lower.includes('safe execution')) {
    return 'sandbox';
  }
  if (lower.includes('reason') || lower.includes('analyze') || lower.includes('think through')) {
    return 'reasoning';
  }
  if (lower.includes('safety') || lower.includes('secure') || lower.includes('critical')) {
    return 'safety';
  }

  return 'default';
}

/**
 * Get provider status summary
 * @returns {Promise<Object>} Status summary
 */
async function getProviderStatus() {
  const checks = await checkAllProviders();

  return {
    timestamp: new Date().toISOString(),
    providers: Object.entries(PROVIDERS).map(([id, provider]) => ({
      id,
      name: provider.name,
      type: provider.type,
      available: checks[id].available,
      version: checks[id].version || 'N/A',
      strengths: provider.strengths,
      contextWindow: provider.contextWindow
    })),
    availableCount: Object.values(checks).filter(c => c.available).length,
    totalCount: Object.keys(PROVIDERS).length
  };
}

/**
 * Generate provider abstraction report
 * @returns {Promise<string>} Markdown report
 */
async function generateProviderReport() {
  const status = await getProviderStatus();

  let report = `# Provider Abstraction Layer

**Generated**: ${status.timestamp}
**Available Providers**: ${status.availableCount}/${status.totalCount}

## Provider Status

| Provider | Type | Available | Version | Context Window |
|----------|------|-----------|---------|----------------|
${status.providers.map(p =>
  `| ${p.name} | ${p.type} | ${p.available ? 'Yes' : 'No'} | ${p.version} | ${(p.contextWindow / 1000).toFixed(0)}K |`
).join('\n')}

## Routing Rules

| Task Type | Preferred | Fallback | Reason |
|-----------|-----------|----------|--------|
${Object.entries(ROUTING_RULES).map(([type, rule]) =>
  `| ${type} | ${rule.preferred} | ${rule.fallback || 'None'} | ${rule.reason} |`
).join('\n')}

## Provider Strengths

`;

  for (const provider of status.providers) {
    report += `### ${provider.name}
- **Strengths**: ${provider.strengths.join(', ')}
- **Context**: ${(provider.contextWindow / 1000).toFixed(0)}K tokens

`;
  }

  return report;
}

// Export
module.exports = {
  PROVIDERS,
  ROUTING_RULES,
  checkProviderAvailability,
  checkAllProviders,
  getBestProvider,
  executeWithProvider,
  routeAndExecute,
  detectTaskType,
  getProviderStatus,
  generateProviderReport
};
