/**
 * Agent Archetype System
 * Phase 4.1 Architecture Optimization
 *
 * Consolidates 225 agent templates into ~20 functional archetypes.
 * Each archetype represents a distinct capability pattern.
 *
 * @module architecture/archetypes/agent-archetypes
 */

const fs = require('fs');
const path = require('path');

/**
 * Core agent archetypes - the fundamental patterns
 * All 225 agents map to one of these archetypes
 */
const AGENT_ARCHETYPES = {
  // ============================================
  // TIER 1: CORE EXECUTION (5 archetypes)
  // ============================================

  'coder': {
    id: 'coder',
    name: 'Code Implementation',
    description: 'Writes, modifies, and refactors code',
    capabilities: ['code_write', 'code_edit', 'refactor', 'implement_feature'],
    tools: ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob'],
    rbac_role: 'developer',
    typical_tasks: [
      'Implement new feature',
      'Fix bug in code',
      'Refactor module',
      'Add tests'
    ],
    maps_from: [
      'coder', 'backend-dev', 'frontend-developer', 'mobile-dev',
      'react-specialist', 'vue-developer', 'golang-backend-specialist',
      'rust-systems-developer', 'python-developer', 'typescript-specialist'
    ]
  },

  'reviewer': {
    id: 'reviewer',
    name: 'Code Review & Analysis',
    description: 'Reviews code for quality, security, and best practices',
    capabilities: ['code_review', 'static_analysis', 'security_scan', 'quality_check'],
    tools: ['Read', 'Grep', 'Glob', 'Task'],
    rbac_role: 'reviewer',
    typical_tasks: [
      'Review pull request',
      'Analyze code quality',
      'Check security vulnerabilities',
      'Verify best practices'
    ],
    maps_from: [
      'reviewer', 'code-analyzer', 'functionality-audit', 'security-audit-agent',
      'code-review-assistant', 'quality-auditor'
    ]
  },

  'tester': {
    id: 'tester',
    name: 'Testing & QA',
    description: 'Writes and runs tests, validates functionality',
    capabilities: ['unit_test', 'integration_test', 'e2e_test', 'test_analysis'],
    tools: ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob'],
    rbac_role: 'tester',
    typical_tasks: [
      'Write unit tests',
      'Create integration tests',
      'Run test suite',
      'Analyze test coverage'
    ],
    maps_from: [
      'tester', 'test-orchestrator', 'integration-test-specialist',
      'e2e-test-specialist', 'test-coverage-analyzer'
    ]
  },

  'debugger': {
    id: 'debugger',
    name: 'Debugging & Troubleshooting',
    description: 'Diagnoses and fixes bugs, analyzes errors',
    capabilities: ['bug_diagnosis', 'error_analysis', 'root_cause', 'fix_implementation'],
    tools: ['Read', 'Grep', 'Glob', 'Bash', 'Edit'],
    rbac_role: 'developer',
    typical_tasks: [
      'Diagnose bug',
      'Analyze stack trace',
      'Find root cause',
      'Implement fix'
    ],
    maps_from: [
      'smart-bug-fix', 'debugger', 'error-analyzer', 'troubleshooter'
    ]
  },

  'documenter': {
    id: 'documenter',
    name: 'Documentation',
    description: 'Creates and maintains documentation',
    capabilities: ['doc_write', 'doc_update', 'api_docs', 'readme_generation'],
    tools: ['Read', 'Write', 'Edit', 'Grep', 'Glob'],
    rbac_role: 'developer',
    typical_tasks: [
      'Write README',
      'Document API',
      'Create user guide',
      'Update changelog'
    ],
    maps_from: [
      'documenter', 'documentation-sync', 'api-documenter', 'readme-generator'
    ]
  },

  // ============================================
  // TIER 2: COORDINATION (4 archetypes)
  // ============================================

  'coordinator': {
    id: 'coordinator',
    name: 'Task Coordination',
    description: 'Coordinates multi-agent tasks and workflows',
    capabilities: ['task_distribution', 'agent_spawn', 'workflow_management', 'progress_tracking'],
    tools: ['Read', 'Grep', 'Glob', 'Task', 'TodoWrite'],
    rbac_role: 'coordinator',
    typical_tasks: [
      'Coordinate feature implementation',
      'Manage multi-agent workflow',
      'Track progress across agents',
      'Handle task dependencies'
    ],
    maps_from: [
      'hierarchical-coordinator', 'mesh-coordinator', 'queen-coordinator',
      'adaptive-coordinator', 'swarm-health-monitor', 'collective-intelligence-coordinator'
    ]
  },

  'planner': {
    id: 'planner',
    name: 'Planning & Strategy',
    description: 'Creates implementation plans and strategies',
    capabilities: ['task_breakdown', 'dependency_analysis', 'strategy_design', 'estimation'],
    tools: ['Read', 'Grep', 'Glob', 'Task', 'TodoWrite'],
    rbac_role: 'coordinator',
    typical_tasks: [
      'Create implementation plan',
      'Break down complex task',
      'Analyze dependencies',
      'Design strategy'
    ],
    maps_from: [
      'planner', 'research-driven-planning', 'system-architect', 'solution-designer'
    ]
  },

  'orchestrator': {
    id: 'orchestrator',
    name: 'Workflow Orchestration',
    description: 'Orchestrates complex multi-step workflows',
    capabilities: ['workflow_design', 'pipeline_execution', 'state_management', 'error_recovery'],
    tools: ['Read', 'Grep', 'Glob', 'Task', 'TodoWrite', 'Bash'],
    rbac_role: 'coordinator',
    typical_tasks: [
      'Design workflow pipeline',
      'Execute multi-stage process',
      'Handle workflow errors',
      'Manage workflow state'
    ],
    maps_from: [
      'meta-loop-orchestrator', 'cascade-orchestrator', 'pipeline-orchestrator',
      'stream-chain', 'workflow-manager'
    ]
  },

  'validator': {
    id: 'validator',
    name: 'Validation & Verification',
    description: 'Validates outputs, verifies correctness',
    capabilities: ['output_validation', 'correctness_check', 'compliance_verify', 'gate_validation'],
    tools: ['Read', 'Grep', 'Glob', 'Bash'],
    rbac_role: 'reviewer',
    typical_tasks: [
      'Validate output correctness',
      'Verify compliance',
      'Check gate criteria',
      'Validate data integrity'
    ],
    maps_from: [
      'gate-validation', 'compliance-validator', 'output-validator',
      'correctness-checker', 'theater-detection-audit'
    ]
  },

  // ============================================
  // TIER 3: RESEARCH & ANALYSIS (4 archetypes)
  // ============================================

  'researcher': {
    id: 'researcher',
    name: 'Research & Investigation',
    description: 'Researches topics, investigates problems',
    capabilities: ['web_search', 'source_analysis', 'synthesis', 'fact_checking'],
    tools: ['Read', 'Grep', 'Glob', 'WebSearch', 'WebFetch', 'Task'],
    rbac_role: 'analyst',
    typical_tasks: [
      'Research topic',
      'Investigate problem',
      'Analyze sources',
      'Synthesize findings'
    ],
    maps_from: [
      'researcher', 'deep-research-orchestrator', 'literature-synthesis',
      'source-credibility-analyzer', 'academic-reading-workflow'
    ]
  },

  'analyst': {
    id: 'analyst',
    name: 'Data & Code Analysis',
    description: 'Analyzes data, code, and systems',
    capabilities: ['data_analysis', 'code_analysis', 'pattern_detection', 'metric_calculation'],
    tools: ['Read', 'Grep', 'Glob', 'Bash'],
    rbac_role: 'analyst',
    typical_tasks: [
      'Analyze codebase',
      'Calculate metrics',
      'Detect patterns',
      'Generate reports'
    ],
    maps_from: [
      'analyst', 'data-analyst', 'performance-analyzer', 'connascence-analyzer',
      'dependency-analyzer', 'architecture-analyzer'
    ]
  },

  'explorer': {
    id: 'explorer',
    name: 'Codebase Exploration',
    description: 'Explores and maps codebases',
    capabilities: ['codebase_map', 'file_discovery', 'structure_analysis', 'dependency_trace'],
    tools: ['Read', 'Grep', 'Glob', 'Task'],
    rbac_role: 'reviewer',
    typical_tasks: [
      'Map codebase structure',
      'Find relevant files',
      'Trace dependencies',
      'Understand architecture'
    ],
    maps_from: [
      'codebase-explorer', 'file-finder', 'structure-mapper', 'dependency-tracer'
    ]
  },

  'synthesizer': {
    id: 'synthesizer',
    name: 'Information Synthesis',
    description: 'Synthesizes information from multiple sources',
    capabilities: ['multi_source_synthesis', 'summary_generation', 'insight_extraction', 'report_creation'],
    tools: ['Read', 'Grep', 'Glob', 'Task'],
    rbac_role: 'analyst',
    typical_tasks: [
      'Synthesize research findings',
      'Generate summary',
      'Extract insights',
      'Create report'
    ],
    maps_from: [
      'synthesis-specialist', 'report-generator', 'insight-extractor',
      'summary-creator', 'knowledge-synthesizer'
    ]
  },

  // ============================================
  // TIER 4: SPECIALIZED (5 archetypes)
  // ============================================

  'security': {
    id: 'security',
    name: 'Security Specialist',
    description: 'Handles security audits, vulnerability detection',
    capabilities: ['security_audit', 'vulnerability_scan', 'penetration_test', 'compliance_check'],
    tools: ['Read', 'Grep', 'Glob', 'Task', 'Bash'],
    rbac_role: 'security',
    typical_tasks: [
      'Security audit',
      'Vulnerability scan',
      'Compliance verification',
      'Security fix implementation'
    ],
    maps_from: [
      'security-manager', 'security-audit-agent', 'vulnerability-scanner',
      'penetration-tester', 'compliance-auditor'
    ]
  },

  'devops': {
    id: 'devops',
    name: 'DevOps & Infrastructure',
    description: 'Handles CI/CD, deployment, infrastructure',
    capabilities: ['cicd_pipeline', 'deployment', 'infrastructure', 'monitoring'],
    tools: ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob'],
    rbac_role: 'developer',
    typical_tasks: [
      'Configure CI/CD',
      'Deploy application',
      'Manage infrastructure',
      'Set up monitoring'
    ],
    maps_from: [
      'cicd-intelligent-recovery', 'deployment-readiness', 'kubernetes-specialist',
      'docker-specialist', 'infrastructure-manager'
    ]
  },

  'database': {
    id: 'database',
    name: 'Database Specialist',
    description: 'Handles database design, queries, migrations',
    capabilities: ['schema_design', 'query_optimization', 'migration', 'data_modeling'],
    tools: ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob'],
    rbac_role: 'database',
    typical_tasks: [
      'Design schema',
      'Optimize queries',
      'Create migrations',
      'Model data'
    ],
    maps_from: [
      'sql-database-specialist', 'database-migration-agent', 'query-optimization-agent',
      'data-modeler', 'schema-designer'
    ]
  },

  'api': {
    id: 'api',
    name: 'API Specialist',
    description: 'Designs and implements APIs',
    capabilities: ['api_design', 'endpoint_implementation', 'integration', 'api_documentation'],
    tools: ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob'],
    rbac_role: 'developer',
    typical_tasks: [
      'Design API',
      'Implement endpoints',
      'Create integrations',
      'Document API'
    ],
    maps_from: [
      'api-designer', 'api-implementer', 'integration-specialist',
      'rest-api-developer', 'graphql-specialist'
    ]
  },

  'multimodel': {
    id: 'multimodel',
    name: 'Multi-Model Router',
    description: 'Routes tasks to appropriate AI models',
    capabilities: ['model_selection', 'task_routing', 'response_aggregation', 'consensus'],
    tools: ['Read', 'Grep', 'Glob', 'Task', 'Bash'],
    rbac_role: 'coordinator',
    typical_tasks: [
      'Route task to best model',
      'Aggregate responses',
      'Build consensus',
      'Optimize model usage'
    ],
    maps_from: [
      'ralph-multimodel', 'llm-council', 'model-router', 'multi-model-coordinator'
    ]
  },

  // ============================================
  // TIER 5: META (2 archetypes)
  // ============================================

  'creator': {
    id: 'creator',
    name: 'Agent/Skill Creator',
    description: 'Creates new agents, skills, and prompts',
    capabilities: ['agent_creation', 'skill_creation', 'prompt_design', 'template_generation'],
    tools: ['Read', 'Write', 'Edit', 'Grep', 'Glob', 'Task'],
    rbac_role: 'developer',
    typical_tasks: [
      'Create new agent',
      'Design skill',
      'Craft prompt',
      'Generate template'
    ],
    maps_from: [
      'agent-creator', 'skill-creator', 'prompt-architect', 'template-generator'
    ]
  },

  'improver': {
    id: 'improver',
    name: 'System Improver',
    description: 'Improves and optimizes the system itself',
    capabilities: ['system_analysis', 'optimization', 'self_improvement', 'metric_tracking'],
    tools: ['Read', 'Write', 'Edit', 'Grep', 'Glob', 'Task', 'Bash'],
    rbac_role: 'developer',
    typical_tasks: [
      'Analyze system performance',
      'Optimize workflows',
      'Improve prompts',
      'Track metrics'
    ],
    maps_from: [
      'recursive-improvement', 'system-optimizer', 'prompt-improver',
      'performance-optimizer', 'meta-loop-improver'
    ]
  }
};

/**
 * Get archetype for a given agent name
 * @param {string} agentName - Name of the agent
 * @returns {Object|null} Archetype or null if not found
 */
function getArchetypeForAgent(agentName) {
  const normalizedName = agentName.toLowerCase().replace(/[_-]/g, '-');

  for (const [archetypeId, archetype] of Object.entries(AGENT_ARCHETYPES)) {
    if (archetype.maps_from.some(name =>
      normalizedName.includes(name.toLowerCase()) ||
      name.toLowerCase().includes(normalizedName)
    )) {
      return archetype;
    }
  }

  // Default mapping based on keywords
  if (normalizedName.includes('code') || normalizedName.includes('dev')) {
    return AGENT_ARCHETYPES.coder;
  }
  if (normalizedName.includes('test')) {
    return AGENT_ARCHETYPES.tester;
  }
  if (normalizedName.includes('review') || normalizedName.includes('audit')) {
    return AGENT_ARCHETYPES.reviewer;
  }
  if (normalizedName.includes('research')) {
    return AGENT_ARCHETYPES.researcher;
  }
  if (normalizedName.includes('coordinator') || normalizedName.includes('orchestrat')) {
    return AGENT_ARCHETYPES.coordinator;
  }
  if (normalizedName.includes('security')) {
    return AGENT_ARCHETYPES.security;
  }
  if (normalizedName.includes('database') || normalizedName.includes('sql')) {
    return AGENT_ARCHETYPES.database;
  }
  if (normalizedName.includes('api')) {
    return AGENT_ARCHETYPES.api;
  }
  if (normalizedName.includes('deploy') || normalizedName.includes('cicd')) {
    return AGENT_ARCHETYPES.devops;
  }
  if (normalizedName.includes('analys') || normalizedName.includes('analyst')) {
    return AGENT_ARCHETYPES.analyst;
  }
  if (normalizedName.includes('plan')) {
    return AGENT_ARCHETYPES.planner;
  }
  if (normalizedName.includes('debug') || normalizedName.includes('fix')) {
    return AGENT_ARCHETYPES.debugger;
  }
  if (normalizedName.includes('doc')) {
    return AGENT_ARCHETYPES.documenter;
  }

  // Default to coder for unmatched
  return AGENT_ARCHETYPES.coder;
}

/**
 * Get all archetypes
 * @returns {Object} All archetypes
 */
function getAllArchetypes() {
  return AGENT_ARCHETYPES;
}

/**
 * Get archetype by ID
 * @param {string} archetypeId - Archetype ID
 * @returns {Object|null} Archetype or null
 */
function getArchetypeById(archetypeId) {
  return AGENT_ARCHETYPES[archetypeId] || null;
}

/**
 * Map all agents to archetypes
 * @param {string[]} agentNames - List of agent names
 * @returns {Object} Mapping of agent names to archetypes
 */
function mapAgentsToArchetypes(agentNames) {
  const mapping = {};
  const archetypeCounts = {};

  for (const name of agentNames) {
    const archetype = getArchetypeForAgent(name);
    mapping[name] = archetype.id;
    archetypeCounts[archetype.id] = (archetypeCounts[archetype.id] || 0) + 1;
  }

  return {
    mapping,
    counts: archetypeCounts,
    totalAgents: agentNames.length,
    totalArchetypes: Object.keys(archetypeCounts).length
  };
}

/**
 * Get recommended archetype for a task
 * @param {string} taskDescription - Description of the task
 * @returns {Object} Recommended archetype
 */
function recommendArchetype(taskDescription) {
  const desc = taskDescription.toLowerCase();

  // Task-based matching
  if (desc.includes('implement') || desc.includes('write code') || desc.includes('create feature')) {
    return AGENT_ARCHETYPES.coder;
  }
  if (desc.includes('review') || desc.includes('check code') || desc.includes('audit')) {
    return AGENT_ARCHETYPES.reviewer;
  }
  if (desc.includes('test') || desc.includes('coverage')) {
    return AGENT_ARCHETYPES.tester;
  }
  if (desc.includes('bug') || desc.includes('fix') || desc.includes('debug')) {
    return AGENT_ARCHETYPES.debugger;
  }
  if (desc.includes('document') || desc.includes('readme')) {
    return AGENT_ARCHETYPES.documenter;
  }
  if (desc.includes('plan') || desc.includes('design') || desc.includes('architect')) {
    return AGENT_ARCHETYPES.planner;
  }
  if (desc.includes('coordinate') || desc.includes('manage agents')) {
    return AGENT_ARCHETYPES.coordinator;
  }
  if (desc.includes('research') || desc.includes('investigate')) {
    return AGENT_ARCHETYPES.researcher;
  }
  if (desc.includes('analyze') || desc.includes('metrics')) {
    return AGENT_ARCHETYPES.analyst;
  }
  if (desc.includes('security') || desc.includes('vulnerability')) {
    return AGENT_ARCHETYPES.security;
  }
  if (desc.includes('deploy') || desc.includes('ci') || desc.includes('pipeline')) {
    return AGENT_ARCHETYPES.devops;
  }
  if (desc.includes('database') || desc.includes('query') || desc.includes('migration')) {
    return AGENT_ARCHETYPES.database;
  }
  if (desc.includes('api') || desc.includes('endpoint')) {
    return AGENT_ARCHETYPES.api;
  }

  // Default to coder
  return AGENT_ARCHETYPES.coder;
}

/**
 * Generate archetype summary report
 * @returns {string} Markdown report
 */
function generateArchetypeReport() {
  const archetypes = Object.values(AGENT_ARCHETYPES);

  let report = `# Agent Archetype System

**Total Archetypes**: ${archetypes.length}
**Purpose**: Consolidate 225 agent templates into functional patterns

## Archetype Tiers

### Tier 1: Core Execution (5)
${archetypes.filter(a => ['coder', 'reviewer', 'tester', 'debugger', 'documenter'].includes(a.id))
  .map(a => `- **${a.name}** (${a.id}): ${a.description}`).join('\n')}

### Tier 2: Coordination (4)
${archetypes.filter(a => ['coordinator', 'planner', 'orchestrator', 'validator'].includes(a.id))
  .map(a => `- **${a.name}** (${a.id}): ${a.description}`).join('\n')}

### Tier 3: Research & Analysis (4)
${archetypes.filter(a => ['researcher', 'analyst', 'explorer', 'synthesizer'].includes(a.id))
  .map(a => `- **${a.name}** (${a.id}): ${a.description}`).join('\n')}

### Tier 4: Specialized (5)
${archetypes.filter(a => ['security', 'devops', 'database', 'api', 'multimodel'].includes(a.id))
  .map(a => `- **${a.name}** (${a.id}): ${a.description}`).join('\n')}

### Tier 5: Meta (2)
${archetypes.filter(a => ['creator', 'improver'].includes(a.id))
  .map(a => `- **${a.name}** (${a.id}): ${a.description}`).join('\n')}

## Archetype Details

`;

  for (const archetype of archetypes) {
    report += `### ${archetype.name} (\`${archetype.id}\`)

**Description**: ${archetype.description}
**RBAC Role**: ${archetype.rbac_role}
**Tools**: ${archetype.tools.join(', ')}

**Capabilities**:
${archetype.capabilities.map(c => `- ${c}`).join('\n')}

**Example Tasks**:
${archetype.typical_tasks.map(t => `- ${t}`).join('\n')}

**Maps From** (${archetype.maps_from.length} agents):
${archetype.maps_from.slice(0, 5).join(', ')}${archetype.maps_from.length > 5 ? '...' : ''}

---

`;
  }

  return report;
}

// Export
module.exports = {
  AGENT_ARCHETYPES,
  getArchetypeForAgent,
  getAllArchetypes,
  getArchetypeById,
  mapAgentsToArchetypes,
  recommendArchetype,
  generateArchetypeReport
};
