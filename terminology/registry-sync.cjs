/**
 * Registry Sync Tool
 * Phase 3 Terminology Cleanup
 *
 * Verifies that documented counts match actual filesystem contents.
 * Identifies ghost code (undocumented) and missing files (documented but not present).
 *
 * @module terminology/registry-sync
 */

const fs = require('fs');
const path = require('path');

// Project root
const PROJECT_ROOT = path.join(__dirname, '..');

/**
 * Count files matching a pattern in a directory
 * @param {string} dir - Directory to search
 * @param {string} extension - File extension to match
 * @param {boolean} recursive - Whether to search recursively
 * @returns {Object} Count and file list
 */
function countFiles(dir, extension = '.md', recursive = true) {
  const files = [];

  function walkDir(currentDir) {
    try {
      const entries = fs.readdirSync(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);

        // Skip certain directories
        if (entry.isDirectory()) {
          if (['node_modules', '.git', 'backup', '.backup'].some(skip =>
            entry.name.includes(skip))) {
            continue;
          }
          if (recursive) {
            walkDir(fullPath);
          }
        } else if (entry.isFile() && entry.name.endsWith(extension)) {
          // Skip backup files
          if (!entry.name.includes('.backup') && !entry.name.includes('.pre-')) {
            files.push(fullPath);
          }
        }
      }
    } catch (err) {
      // Directory doesn't exist or permission denied
    }
  }

  walkDir(dir);

  return {
    count: files.length,
    files: files.map(f => path.relative(PROJECT_ROOT, f))
  };
}

/**
 * Count agents in the registry
 * @returns {Object} Agent count breakdown
 */
function countAgents() {
  const agentsDir = path.join(PROJECT_ROOT, 'agents');
  const result = countFiles(agentsDir, '.md');

  // Categorize agents
  const categories = {};
  for (const file of result.files) {
    const parts = file.split(path.sep);
    if (parts.length >= 2) {
      const category = parts[1];
      categories[category] = (categories[category] || 0) + 1;
    }
  }

  return {
    total: result.count,
    files: result.files,
    categories
  };
}

/**
 * Count skills in the registry
 * @returns {Object} Skill count breakdown
 */
function countSkills() {
  const skillsDir = path.join(PROJECT_ROOT, 'skills');
  const result = countFiles(skillsDir, 'SKILL.md');

  // Categorize skills
  const categories = {};
  for (const file of result.files) {
    const parts = file.split(path.sep);
    if (parts.length >= 2) {
      const category = parts[1];
      categories[category] = (categories[category] || 0) + 1;
    }
  }

  return {
    total: result.count,
    files: result.files,
    categories
  };
}

/**
 * Count commands
 * @returns {Object} Command count
 */
function countCommands() {
  const commandsDir = path.join(PROJECT_ROOT, 'commands');
  return countFiles(commandsDir, '.md');
}

/**
 * Count playbooks
 * @returns {Object} Playbook count
 */
function countPlaybooks() {
  const playbooksDir = path.join(PROJECT_ROOT, 'playbooks');
  return countFiles(playbooksDir, '.md');
}

/**
 * Count hooks
 * @returns {Object} Hook count
 */
function countHooks() {
  const hooksDir = path.join(PROJECT_ROOT, 'hooks');
  const shHooks = countFiles(hooksDir, '.sh');
  const jsHooks = countFiles(hooksDir, '.js');

  return {
    count: shHooks.count + jsHooks.count,
    files: [...shHooks.files, ...jsHooks.files]
  };
}

/**
 * Get documented counts from CLAUDE.md
 * @returns {Object} Documented counts
 */
function getDocumentedCounts() {
  const claudeMdPath = path.join(PROJECT_ROOT, 'CLAUDE.md');

  try {
    const content = fs.readFileSync(claudeMdPath, 'utf8');

    // Parse counts from the table
    const skillsMatch = content.match(/Skills\s*\|\s*(\d+)/i);
    const agentsMatch = content.match(/Agents\s*\|\s*(\d+)/i);
    const commandsMatch = content.match(/Commands\s*\|\s*(\d+)/i);
    const playbooksMatch = content.match(/Playbooks\s*\|\s*(\d+)/i);

    return {
      skills: skillsMatch ? parseInt(skillsMatch[1]) : null,
      agents: agentsMatch ? parseInt(agentsMatch[1]) : null,
      commands: commandsMatch ? parseInt(commandsMatch[1]) : null,
      playbooks: playbooksMatch ? parseInt(playbooksMatch[1]) : null
    };
  } catch (err) {
    return { error: err.message };
  }
}

/**
 * Full registry sync check
 * @returns {Object} Sync results
 */
function syncCheck() {
  const documented = getDocumentedCounts();
  const agents = countAgents();
  const skills = countSkills();
  const commands = countCommands();
  const playbooks = countPlaybooks();
  const hooks = countHooks();

  const results = {
    timestamp: new Date().toISOString(),
    documented,
    actual: {
      agents: agents.total,
      skills: skills.total,
      commands: commands.count,
      playbooks: playbooks.count,
      hooks: hooks.count
    },
    discrepancies: [],
    categories: {
      agents: agents.categories,
      skills: skills.categories
    }
  };

  // Check for discrepancies
  if (documented.agents !== null && documented.agents !== agents.total) {
    results.discrepancies.push({
      type: 'agents',
      documented: documented.agents,
      actual: agents.total,
      difference: agents.total - documented.agents
    });
  }

  if (documented.skills !== null && documented.skills !== skills.total) {
    results.discrepancies.push({
      type: 'skills',
      documented: documented.skills,
      actual: skills.total,
      difference: skills.total - documented.skills
    });
  }

  if (documented.commands !== null && documented.commands !== commands.count) {
    results.discrepancies.push({
      type: 'commands',
      documented: documented.commands,
      actual: commands.count,
      difference: commands.count - documented.commands
    });
  }

  if (documented.playbooks !== null && documented.playbooks !== playbooks.count) {
    results.discrepancies.push({
      type: 'playbooks',
      documented: documented.playbooks,
      actual: playbooks.count,
      difference: playbooks.count - documented.playbooks
    });
  }

  results.synced = results.discrepancies.length === 0;

  return results;
}

/**
 * Find duplicate agent/skill names
 * @returns {Object} Duplicates found
 */
function findDuplicates() {
  const agents = countAgents();
  const skills = countSkills();

  const agentNames = {};
  const skillNames = {};
  const duplicates = { agents: [], skills: [] };

  // Check agent duplicates
  for (const file of agents.files) {
    const name = path.basename(file, '.md');
    if (agentNames[name]) {
      duplicates.agents.push({
        name,
        files: [agentNames[name], file]
      });
    } else {
      agentNames[name] = file;
    }
  }

  // Check skill duplicates
  for (const file of skills.files) {
    const dir = path.dirname(file);
    const name = path.basename(dir);
    if (skillNames[name]) {
      duplicates.skills.push({
        name,
        files: [skillNames[name], file]
      });
    } else {
      skillNames[name] = file;
    }
  }

  return duplicates;
}

/**
 * Generate sync report
 * @returns {string} Markdown report
 */
function generateSyncReport() {
  const sync = syncCheck();
  const duplicates = findDuplicates();

  let report = `# Registry Sync Report

**Generated**: ${sync.timestamp}
**Status**: ${sync.synced ? 'SYNCED' : 'DISCREPANCIES FOUND'}

## Counts

| Component | Documented | Actual | Difference |
|-----------|------------|--------|------------|
| Agents | ${sync.documented.agents || 'N/A'} | ${sync.actual.agents} | ${sync.documented.agents ? sync.actual.agents - sync.documented.agents : 'N/A'} |
| Skills | ${sync.documented.skills || 'N/A'} | ${sync.actual.skills} | ${sync.documented.skills ? sync.actual.skills - sync.documented.skills : 'N/A'} |
| Commands | ${sync.documented.commands || 'N/A'} | ${sync.actual.commands} | ${sync.documented.commands ? sync.actual.commands - sync.documented.commands : 'N/A'} |
| Playbooks | ${sync.documented.playbooks || 'N/A'} | ${sync.actual.playbooks} | ${sync.documented.playbooks ? sync.actual.playbooks - sync.documented.playbooks : 'N/A'} |
| Hooks | N/A | ${sync.actual.hooks} | N/A |

## Agent Categories

| Category | Count |
|----------|-------|
${Object.entries(sync.categories.agents).map(([cat, count]) => `| ${cat} | ${count} |`).join('\n')}

## Skill Categories

| Category | Count |
|----------|-------|
${Object.entries(sync.categories.skills).map(([cat, count]) => `| ${cat} | ${count} |`).join('\n')}

`;

  if (sync.discrepancies.length > 0) {
    report += `## Discrepancies

`;
    for (const d of sync.discrepancies) {
      report += `- **${d.type}**: Documented ${d.documented}, Actual ${d.actual} (${d.difference > 0 ? '+' : ''}${d.difference})
`;
    }
  }

  if (duplicates.agents.length > 0 || duplicates.skills.length > 0) {
    report += `
## Duplicates Found

`;
    if (duplicates.agents.length > 0) {
      report += `### Agent Duplicates
`;
      for (const d of duplicates.agents) {
        report += `- ${d.name}: ${d.files.join(', ')}
`;
      }
    }
    if (duplicates.skills.length > 0) {
      report += `### Skill Duplicates
`;
      for (const d of duplicates.skills) {
        report += `- ${d.name}: ${d.files.join(', ')}
`;
      }
    }
  }

  return report;
}

// Export functions
module.exports = {
  countFiles,
  countAgents,
  countSkills,
  countCommands,
  countPlaybooks,
  countHooks,
  getDocumentedCounts,
  syncCheck,
  findDuplicates,
  generateSyncReport
};

// CLI execution
if (require.main === module) {
  console.log(generateSyncReport());
}
