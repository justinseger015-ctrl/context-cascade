#!/usr/bin/env node
/**
 * validate-all.js
 * Validates all components against Anthropic official format
 *
 * Usage:
 *   node validate-all.js [--verbose] [--fix]
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '../..');
const VERBOSE = process.argv.includes('--verbose');

const results = {
  pluginJson: { valid: false, errors: [] },
  skills: { total: 0, valid: 0, errors: [] },
  agents: { total: 0, valid: 0, errors: [] },
  commands: { total: 0, valid: 0, errors: [] }
};

function log(msg) {
  console.log(`[validate] ${msg}`);
}

function verbose(msg) {
  if (VERBOSE) console.log(`  ${msg}`);
}

// Validate plugin.json
function validatePluginJson() {
  const pluginPath = path.join(ROOT_DIR, '.claude-plugin', 'plugin.json');

  try {
    const content = fs.readFileSync(pluginPath, 'utf-8');
    const plugin = JSON.parse(content);

    const requiredFields = ['name', 'description', 'version', 'author'];
    const officialPathFields = ['commands', 'agents', 'skills'];

    for (const field of requiredFields) {
      if (!plugin[field]) {
        results.pluginJson.errors.push(`Missing required field: ${field}`);
      }
    }

    for (const field of officialPathFields) {
      if (!plugin[field]) {
        results.pluginJson.errors.push(`Missing path field: ${field}`);
      } else if (typeof plugin[field] !== 'string') {
        results.pluginJson.errors.push(`Field ${field} should be a path string`);
      }
    }

    results.pluginJson.valid = results.pluginJson.errors.length === 0;

  } catch (err) {
    results.pluginJson.errors.push(`Parse error: ${err.message}`);
  }
}

// Find files recursively
function findFiles(dir, pattern) {
  const results = [];

  function walk(currentDir) {
    if (!fs.existsSync(currentDir)) return;
    const items = fs.readdirSync(currentDir);
    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        walk(fullPath);
      } else if (pattern.test(item)) {
        results.push(fullPath);
      }
    }
  }

  walk(dir);
  return results;
}

// Parse YAML frontmatter
function parseYamlFrontmatter(content) {
  // Skip any leading /* */ comment blocks before frontmatter
  let cleanContent = content;
  while (cleanContent.match(/^\s*\/\*[\s\S]*?\*\/\s*/)) {
    cleanContent = cleanContent.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, '');
  }

  // Handle both LF and CRLF line endings
  const match = cleanContent.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return null;

  // Normalize line endings (remove \r)
  const lines = match[1].split('\n').map(l => l.replace(/\r$/, ''));
  const result = {};

  for (const line of lines) {
    const kvMatch = line.match(/^([a-z_-]+):\s*(.*)$/i);
    if (kvMatch && kvMatch[1] && !kvMatch[1].startsWith(' ')) {
      result[kvMatch[1]] = kvMatch[2] || true;
    }
  }

  return result;
}

// Official fields (Anthropic format) - only these allowed in SKILL.md/agent frontmatter
const OFFICIAL_SKILL_FIELDS = ['name', 'description', 'allowed-tools', 'model'];
const OFFICIAL_AGENT_FIELDS = ['name', 'description', 'tools', 'model', 'permissionMode', 'skills'];

// Sidecar tracking
const sidecarStats = {
  withSidecar: 0,
  withoutSidecar: 0
};

// Validate custom field has x- prefix
function validateCustomFieldPrefix(frontmatter, officialFields) {
  const warnings = [];
  for (const key of Object.keys(frontmatter)) {
    if (!officialFields.includes(key) && !key.startsWith('x-')) {
      warnings.push(`WARNING: Custom field "${key}" should be prefixed with "x-" (use "x-${key}")`);
    }
  }
  return warnings;
}

// Validate a skill file (Option C: official format + metadata.json sidecar)
function validateSkill(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const frontmatter = parseYamlFrontmatter(content);
  const errors = [];
  const skillDir = path.dirname(filePath);

  if (!frontmatter) {
    errors.push('No YAML frontmatter found');
  } else {
    if (!frontmatter.name) {
      errors.push('Missing required field: name');
    }
    if (!frontmatter.description) {
      errors.push('Missing required field: description');
    }
    // Check for allowed-tools (recommended in Anthropic format)
    if (!frontmatter['allowed-tools']) {
      errors.push('WARNING: Missing recommended field: allowed-tools');
    }
    // Check if description contains VERIX notation (warning, not error)
    if (frontmatter.description && frontmatter.description.includes('[assert|')) {
      errors.push('WARNING: description contains VERIX notation (should be plain text)');
    }
    // In Option C format, no custom fields allowed in SKILL.md - they go in metadata.json
    const nonOfficialFields = Object.keys(frontmatter).filter(k => !OFFICIAL_SKILL_FIELDS.includes(k));
    if (nonOfficialFields.length > 0) {
      errors.push(`WARNING: Non-official fields in SKILL.md (should be in metadata.json): ${nonOfficialFields.join(', ')}`);
    }
  }

  // Check for metadata.json sidecar (Option C format)
  const metadataPath = path.join(skillDir, 'metadata.json');
  if (fs.existsSync(metadataPath)) {
    sidecarStats.withSidecar++;
    // Validate metadata.json structure
    try {
      const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf-8'));
      if (!metadata.version && !metadata.category) {
        errors.push('WARNING: metadata.json missing version or category');
      }
    } catch (e) {
      errors.push(`ERROR: Invalid metadata.json: ${e.message}`);
    }
  } else {
    sidecarStats.withoutSidecar++;
  }

  return errors;
}

// Validate an agent file
function validateAgent(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const frontmatter = parseYamlFrontmatter(content);
  const errors = [];

  if (!frontmatter) {
    errors.push('No YAML frontmatter found');
  } else {
    if (!frontmatter.name) {
      errors.push('Missing required field: name');
    }
    if (!frontmatter.description) {
      errors.push('Missing required field: description');
    }
    // Check for official 'tools' field
    if (!frontmatter.tools) {
      errors.push('Missing official field: tools (should replace rbac.allowed_tools)');
    }
    // Check for official 'model' field (optional but recommended)
    if (!frontmatter.model) {
      errors.push('WARNING: Missing recommended field: model (sonnet, opus, haiku)');
    }
    // Check if description contains VERIX notation (warning)
    if (frontmatter.description && frontmatter.description.includes('[assert|')) {
      errors.push('WARNING: description contains VERIX notation');
    }
    // Check for x- prefix on custom fields
    const prefixWarnings = validateCustomFieldPrefix(frontmatter, OFFICIAL_AGENT_FIELDS);
    errors.push(...prefixWarnings);
  }

  return errors;
}

// Validate skills
function validateSkills() {
  const skillsDir = path.join(ROOT_DIR, 'skills');
  const skillFiles = findFiles(skillsDir, /^SKILL\.md$/);

  results.skills.total = skillFiles.length;

  for (const filePath of skillFiles) {
    const relativePath = path.relative(skillsDir, filePath);
    const errors = validateSkill(filePath);

    if (errors.length === 0) {
      results.skills.valid++;
      verbose(`VALID: ${relativePath}`);
    } else {
      results.skills.errors.push({
        file: relativePath,
        errors: errors
      });
      verbose(`INVALID: ${relativePath} - ${errors.join(', ')}`);
    }
  }
}

// Validate agents
function validateAgents() {
  const agentsDir = path.join(ROOT_DIR, 'agents');
  const agentFiles = findFiles(agentsDir, /\.md$/).filter(f => {
    const name = path.basename(f);
    return name !== 'README.md' && name !== 'index.md';
  });

  results.agents.total = agentFiles.length;

  for (const filePath of agentFiles) {
    const relativePath = path.relative(agentsDir, filePath);

    // Check if file has frontmatter (is an agent definition)
    const content = fs.readFileSync(filePath, 'utf-8');
    if (!content.startsWith('---')) {
      continue;  // Skip non-agent md files
    }

    const errors = validateAgent(filePath);

    if (errors.length === 0) {
      results.agents.valid++;
      verbose(`VALID: ${relativePath}`);
    } else {
      // Only count as invalid if it has actual errors (not just warnings)
      const realErrors = errors.filter(e => !e.startsWith('WARNING'));
      if (realErrors.length === 0) {
        results.agents.valid++;
      } else {
        results.agents.errors.push({
          file: relativePath,
          errors: errors
        });
      }
      verbose(`CHECKED: ${relativePath} - ${errors.join(', ')}`);
    }
  }
}

// Generate report
function generateReport() {
  console.log('\n' + '='.repeat(60));
  console.log('ANTHROPIC FORMAT COMPLIANCE VALIDATION REPORT');
  console.log('='.repeat(60));

  console.log('\n1. PLUGIN.JSON');
  console.log('-'.repeat(40));
  if (results.pluginJson.valid) {
    console.log('   Status: COMPLIANT');
  } else {
    console.log('   Status: NON-COMPLIANT');
    results.pluginJson.errors.forEach(e => console.log(`   - ${e}`));
  }

  console.log('\n2. SKILLS (Option C: SKILL.md + metadata.json)');
  console.log('-'.repeat(40));
  console.log(`   Total:  ${results.skills.total}`);
  console.log(`   Valid:  ${results.skills.valid}`);
  console.log(`   Invalid: ${results.skills.errors.length}`);
  console.log(`   With metadata.json sidecar: ${sidecarStats.withSidecar}`);
  console.log(`   Without sidecar: ${sidecarStats.withoutSidecar}`);
  if (results.skills.errors.length > 0 && VERBOSE) {
    results.skills.errors.slice(0, 10).forEach(e => {
      console.log(`   - ${e.file}: ${e.errors.join(', ')}`);
    });
    if (results.skills.errors.length > 10) {
      console.log(`   ... and ${results.skills.errors.length - 10} more`);
    }
  }

  console.log('\n3. AGENTS');
  console.log('-'.repeat(40));
  console.log(`   Total:  ${results.agents.total}`);
  console.log(`   Valid:  ${results.agents.valid}`);
  console.log(`   Invalid: ${results.agents.errors.length}`);
  if (results.agents.errors.length > 0 && VERBOSE) {
    results.agents.errors.slice(0, 10).forEach(e => {
      console.log(`   - ${e.file}: ${e.errors.join(', ')}`);
    });
    if (results.agents.errors.length > 10) {
      console.log(`   ... and ${results.agents.errors.length - 10} more`);
    }
  }

  console.log('\n' + '='.repeat(60));

  const totalValid = (results.pluginJson.valid ? 1 : 0) +
                     results.skills.valid +
                     results.agents.valid;
  const totalChecked = 1 + results.skills.total + results.agents.total;
  const compliance = ((totalValid / totalChecked) * 100).toFixed(1);

  console.log(`OVERALL COMPLIANCE: ${compliance}% (${totalValid}/${totalChecked})`);
  console.log('='.repeat(60));

  // Return exit code
  return results.pluginJson.valid &&
         results.skills.errors.length === 0 &&
         results.agents.errors.length === 0 ? 0 : 1;
}

function main() {
  log('Starting validation...\n');

  validatePluginJson();
  validateSkills();
  validateAgents();

  const exitCode = generateReport();
  process.exit(exitCode);
}

try {
  main();
} catch (err) {
  console.error(`[validate] FATAL: ${err.message}`);
  process.exit(1);
}
