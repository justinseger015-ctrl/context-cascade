/**
 * Create skill cache entries for Claude Code invocability.
 *
 * Reads all SKILL.md files from the plugin and creates simplified
 * versions in the cache directory that Claude Code can invoke.
 */

const fs = require('fs');
const path = require('path');

const SOURCE_DIR = 'C:/Users/17175/claude-code-plugins/context-cascade/skills';
const CACHE_DIR = 'C:/Users/17175/.claude/plugins/cache/claude-code-plugins/context-cascade/3.0.0/skills';

// Ensure cache directory exists
if (!fs.existsSync(CACHE_DIR)) {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
}

// Find all SKILL.md files
function findSkillFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      // Skip backup and hidden directories
      if (!entry.name.startsWith('.') && entry.name !== 'backup') {
        findSkillFiles(fullPath, files);
      }
    } else if (entry.name === 'SKILL.md') {
      files.push(fullPath);
    }
  }

  return files;
}

// Parse frontmatter from SKILL.md
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const frontmatter = {};
  const lines = match[1].split('\n');

  let currentKey = null;
  let inMultiline = false;
  let multilineValue = [];

  for (const line of lines) {
    if (inMultiline) {
      if (line.startsWith('  ') || line.startsWith('\t')) {
        multilineValue.push(line.trim());
      } else {
        frontmatter[currentKey] = multilineValue.join(' ').trim();
        inMultiline = false;
        multilineValue = [];
      }
    }

    if (!inMultiline) {
      const keyMatch = line.match(/^(\w[\w-]*?):\s*(.*)$/);
      if (keyMatch) {
        currentKey = keyMatch[1];
        const value = keyMatch[2].trim();

        if (value) {
          frontmatter[currentKey] = value;
        } else {
          inMultiline = true;
          multilineValue = [];
        }
      }
    }
  }

  if (inMultiline && currentKey) {
    frontmatter[currentKey] = multilineValue.join(' ').trim();
  }

  return frontmatter;
}

// Get skill name from path or frontmatter
function getSkillName(filePath, frontmatter) {
  if (frontmatter && frontmatter.name) {
    return frontmatter.name;
  }

  // Extract from path: skills/category/skill-name/SKILL.md
  const parts = filePath.split(/[\/\\]/);
  const skillIdx = parts.indexOf('SKILL.md');
  if (skillIdx > 0) {
    return parts[skillIdx - 1];
  }

  return 'unknown-skill';
}

// Get short description (first sentence or first 200 chars)
function getShortDescription(frontmatter, content) {
  let desc = '';

  if (frontmatter && frontmatter.description) {
    desc = frontmatter.description;
  } else {
    // Try to extract from content
    const afterFrontmatter = content.replace(/^---[\s\S]*?---\n?/, '');
    const firstPara = afterFrontmatter.match(/^[^#\n].*?[.!?]/);
    if (firstPara) {
      desc = firstPara[0].trim();
    }
  }

  // Clean up and truncate
  desc = desc.replace(/\s+/g, ' ').trim();

  // Get first sentence
  const firstSentence = desc.match(/^[^.!?]*[.!?]/);
  if (firstSentence && firstSentence[0].length < 300) {
    return firstSentence[0].trim();
  }

  // Truncate if too long
  if (desc.length > 300) {
    return desc.substring(0, 297) + '...';
  }

  return desc || 'Skill from context-cascade plugin.';
}

// Create simplified SKILL.md
function createCacheEntry(skillName, description, originalPath) {
  const skillDir = path.join(CACHE_DIR, skillName);

  // Ensure directory exists
  if (!fs.existsSync(skillDir)) {
    fs.mkdirSync(skillDir, { recursive: true });
  }

  // Create simplified SKILL.md
  const content = `---
name: ${skillName}
description: ${description}
source: context-cascade
---

# ${skillName.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}

${description}

For full implementation details, see: ${originalPath.replace(/\\/g, '/')}
`;

  const cachePath = path.join(skillDir, 'SKILL.md');
  fs.writeFileSync(cachePath, content);

  return cachePath;
}

// Main execution
console.log('Finding skill files...');
const skillFiles = findSkillFiles(SOURCE_DIR);
console.log(`Found ${skillFiles.length} skill files.`);

let created = 0;
let failed = 0;
const skills = [];

for (const filePath of skillFiles) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const frontmatter = parseFrontmatter(content);
    const skillName = getSkillName(filePath, frontmatter);
    const description = getShortDescription(frontmatter, content);

    // Skip if skill name is too long or has special chars
    if (skillName.length > 50 || /[^a-zA-Z0-9_-]/.test(skillName)) {
      console.log(`  Skipping: ${skillName} (invalid name)`);
      continue;
    }

    const cachePath = createCacheEntry(skillName, description, filePath);
    created++;
    skills.push({ name: skillName, description, cachePath });

  } catch (err) {
    console.error(`Failed to process ${filePath}: ${err.message}`);
    failed++;
  }
}

console.log(`\nCreated ${created} cache entries.`);
console.log(`Failed: ${failed}`);

// Write skill index
const indexPath = path.join(CACHE_DIR, 'skill-index.json');
fs.writeFileSync(indexPath, JSON.stringify({
  version: '3.0.0',
  generated: new Date().toISOString(),
  count: skills.length,
  skills: skills.map(s => ({ name: s.name, description: s.description }))
}, null, 2));

console.log(`\nSkill index written to: ${indexPath}`);
console.log('\nDone!');
