#!/usr/bin/env node
/**
 * migrate-to-sidecar.js
 * Migrates skills to Anthropic official format with metadata.json sidecars
 *
 * Option C Migration:
 * - SKILL.md: Only official fields (name, description, allowed-tools, model)
 * - metadata.json: Custom extensions (version, category, tags, etc.)
 *
 * Usage:
 *   node migrate-to-sidecar.js [--dry-run] [--verbose]
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '../..');
const SKILLS_DIR = path.join(ROOT_DIR, 'skills');
const DRY_RUN = process.argv.includes('--dry-run');
const VERBOSE = process.argv.includes('--verbose');

// Official Anthropic fields (only these stay in SKILL.md)
const OFFICIAL_FIELDS = ['name', 'description', 'allowed-tools', 'model'];

// Stats tracking
const stats = {
  total: 0,
  migrated: 0,
  skipped: 0,
  renamed: 0,
  errors: []
};

function log(msg) {
  console.log(`[migrate] ${msg}`);
}

function verbose(msg) {
  if (VERBOSE) console.log(`  ${msg}`);
}

// Parse YAML frontmatter from SKILL.md
function parseFrontmatter(content) {
  // Skip comment blocks
  let cleanContent = content;
  while (cleanContent.match(/^\s*\/\*[\s\S]*?\*\/\s*/)) {
    cleanContent = cleanContent.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, '');
  }

  const match = cleanContent.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return { frontmatter: null, body: content };

  const lines = match[1].split('\n').map(l => l.replace(/\r$/, ''));
  const frontmatter = {};
  let currentKey = null;
  let currentValue = [];
  let inArray = false;

  for (const line of lines) {
    // Check for new key
    const kvMatch = line.match(/^([a-z_-]+):\s*(.*)$/i);

    if (kvMatch && !line.startsWith('  ') && !line.startsWith('\t')) {
      // Save previous key if exists
      if (currentKey) {
        if (inArray) {
          frontmatter[currentKey] = currentValue;
        } else {
          frontmatter[currentKey] = currentValue.join('\n').trim() || true;
        }
      }

      currentKey = kvMatch[1];
      const value = kvMatch[2].trim();

      if (value === '' || value === '|' || value === '>') {
        currentValue = [];
        inArray = false;
      } else if (value.startsWith('[') && value.endsWith(']')) {
        // Inline array
        frontmatter[currentKey] = value.slice(1, -1).split(',').map(s => s.trim());
        currentKey = null;
        currentValue = [];
        inArray = false;
      } else {
        currentValue = [value];
        inArray = false;
      }
    } else if (line.match(/^\s+-\s+(.+)$/)) {
      // Array item
      const itemMatch = line.match(/^\s+-\s+(.+)$/);
      if (itemMatch) {
        if (!inArray) {
          currentValue = [];
          inArray = true;
        }
        currentValue.push(itemMatch[1].trim());
      }
    } else if (line.match(/^\s+\S/) && currentKey) {
      // Continuation of multiline value
      currentValue.push(line.trim());
    }
  }

  // Save last key
  if (currentKey) {
    if (inArray) {
      frontmatter[currentKey] = currentValue;
    } else {
      frontmatter[currentKey] = currentValue.join('\n').trim() || true;
    }
  }

  // Get body (content after frontmatter)
  const bodyMatch = cleanContent.match(/^---\r?\n[\s\S]*?\r?\n---\r?\n([\s\S]*)$/);
  const body = bodyMatch ? bodyMatch[1] : '';

  return { frontmatter, body };
}

// Serialize frontmatter to YAML
function serializeFrontmatter(fm) {
  let yaml = '---\n';

  for (const [key, value] of Object.entries(fm)) {
    if (Array.isArray(value)) {
      yaml += `${key}:\n`;
      for (const item of value) {
        yaml += `  - ${item}\n`;
      }
    } else if (typeof value === 'object') {
      yaml += `${key}:\n`;
      for (const [subKey, subValue] of Object.entries(value)) {
        if (Array.isArray(subValue)) {
          yaml += `  ${subKey}: [${subValue.join(', ')}]\n`;
        } else {
          yaml += `  ${subKey}: ${subValue}\n`;
        }
      }
    } else {
      yaml += `${key}: ${value}\n`;
    }
  }

  yaml += '---\n';
  return yaml;
}

// Extract skill name from directory path
function extractSkillName(dirPath) {
  const dirName = path.basename(dirPath);

  // Handle "when-X-use-Y" pattern -> extract Y
  const whenMatch = dirName.match(/^when-.*-use-(.+)$/);
  if (whenMatch) {
    return whenMatch[1];
  }

  return dirName;
}

// Create metadata.json from custom fields
function createMetadataJson(frontmatter, dirName) {
  const metadata = {
    "$schema": "../../../schemas/skill-metadata.schema.json",
    "migrated_from": "SKILL.md frontmatter",
    "migration_date": new Date().toISOString().split('T')[0]
  };

  // Extract custom fields (anything not in OFFICIAL_FIELDS)
  for (const [key, value] of Object.entries(frontmatter)) {
    if (!OFFICIAL_FIELDS.includes(key)) {
      // Remove x- prefix if present for cleaner JSON
      const cleanKey = key.startsWith('x-') ? key.slice(2) : key;
      metadata[cleanKey] = value;
    }
  }

  // Add original directory name if it was a "when-X-use-Y" pattern
  if (dirName.includes('when-')) {
    metadata.original_directory = dirName;
    metadata.triggers = metadata.triggers || [];
    // Extract trigger keywords from directory name
    const triggerMatch = dirName.match(/^when-(.+)-use-/);
    if (triggerMatch) {
      const triggerPhrase = triggerMatch[1].replace(/-/g, ' ');
      if (!metadata.triggers.includes(triggerPhrase)) {
        metadata.triggers.push(triggerPhrase);
      }
    }
  }

  return metadata;
}

// Clean frontmatter to only official fields
function cleanFrontmatter(frontmatter, expectedName) {
  const clean = {};

  // Name - ensure it matches expected (kebab-case directory name)
  clean.name = expectedName;

  // Description - remove VERIX notation
  if (frontmatter.description) {
    let desc = frontmatter.description;
    // Remove VERIX annotations
    desc = desc.replace(/\[assert\|[^\]]*\]\s*/g, '');
    desc = desc.replace(/\[ground:[^\]]*\]\s*/g, '');
    desc = desc.replace(/\[conf:[^\]]*\]\s*/g, '');
    desc = desc.replace(/\[state:[^\]]*\]\s*/g, '');
    desc = desc.replace(/\[define\|[^\]]*\]\s*/g, '');
    desc = desc.trim();
    clean.description = desc;
  }

  // Allowed-tools
  if (frontmatter['allowed-tools']) {
    clean['allowed-tools'] = frontmatter['allowed-tools'];
  }

  // Model (optional but recommended)
  if (frontmatter.model) {
    clean.model = frontmatter.model;
  }

  return clean;
}

// Find all SKILL.md files
function findSkillFiles(dir) {
  const results = [];

  function walk(currentDir) {
    if (!fs.existsSync(currentDir)) return;
    const items = fs.readdirSync(currentDir);

    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        // Skip backup directories
        if (item.includes('backup') || item.includes('.git')) continue;
        walk(fullPath);
      } else if (item === 'SKILL.md') {
        results.push(fullPath);
      }
    }
  }

  walk(dir);
  return results;
}

// Migrate a single skill
function migrateSkill(skillPath) {
  const skillDir = path.dirname(skillPath);
  const dirName = path.basename(skillDir);
  const relativePath = path.relative(SKILLS_DIR, skillDir);

  verbose(`Processing: ${relativePath}`);
  stats.total++;

  try {
    // Read SKILL.md
    const content = fs.readFileSync(skillPath, 'utf-8');
    const { frontmatter, body } = parseFrontmatter(content);

    if (!frontmatter) {
      verbose(`  SKIP: No frontmatter found`);
      stats.skipped++;
      return;
    }

    // Check if already migrated (metadata.json exists)
    const metadataPath = path.join(skillDir, 'metadata.json');
    if (fs.existsSync(metadataPath)) {
      verbose(`  SKIP: Already migrated (metadata.json exists)`);
      stats.skipped++;
      return;
    }

    // Extract expected skill name
    const expectedName = extractSkillName(skillDir);

    // Create metadata.json with custom fields
    const metadata = createMetadataJson(frontmatter, dirName);

    // Clean frontmatter to official fields only
    const cleanedFrontmatter = cleanFrontmatter(frontmatter, expectedName);

    // Generate new SKILL.md content
    const newContent = serializeFrontmatter(cleanedFrontmatter) + '\n' + body;

    if (DRY_RUN) {
      log(`[DRY-RUN] Would migrate: ${relativePath}`);
      verbose(`  metadata.json keys: ${Object.keys(metadata).join(', ')}`);
      verbose(`  clean frontmatter: ${JSON.stringify(cleanedFrontmatter)}`);
    } else {
      // Backup original
      const backupPath = path.join(skillDir, 'SKILL.md.pre-sidecar-backup');
      fs.writeFileSync(backupPath, content);

      // Write metadata.json
      fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2) + '\n');

      // Write cleaned SKILL.md
      fs.writeFileSync(skillPath, newContent);

      verbose(`  Created: metadata.json`);
      verbose(`  Updated: SKILL.md`);
    }

    stats.migrated++;

  } catch (err) {
    stats.errors.push({ path: relativePath, error: err.message });
    log(`ERROR: ${relativePath} - ${err.message}`);
  }
}

// Generate report
function generateReport() {
  console.log('\n' + '='.repeat(60));
  console.log('SKILL SIDECAR MIGRATION REPORT');
  console.log('='.repeat(60));

  console.log(`\nMode: ${DRY_RUN ? 'DRY RUN' : 'LIVE MIGRATION'}`);
  console.log(`\nStatistics:`);
  console.log(`  Total skills found:  ${stats.total}`);
  console.log(`  Successfully migrated: ${stats.migrated}`);
  console.log(`  Skipped (already done): ${stats.skipped}`);
  console.log(`  Errors: ${stats.errors.length}`);

  if (stats.errors.length > 0) {
    console.log(`\nErrors:`);
    stats.errors.forEach(e => {
      console.log(`  - ${e.path}: ${e.error}`);
    });
  }

  console.log('\n' + '='.repeat(60));

  if (DRY_RUN) {
    console.log('This was a DRY RUN. No files were modified.');
    console.log('Run without --dry-run to perform actual migration.');
  } else {
    console.log('Migration complete!');
    console.log('Backups saved as SKILL.md.pre-sidecar-backup');
  }

  console.log('='.repeat(60) + '\n');
}

// Main
function main() {
  log('Starting Option C Sidecar Migration...\n');

  if (DRY_RUN) {
    log('*** DRY RUN MODE - No files will be modified ***\n');
  }

  const skillFiles = findSkillFiles(SKILLS_DIR);
  log(`Found ${skillFiles.length} SKILL.md files\n`);

  for (const skillPath of skillFiles) {
    migrateSkill(skillPath);
  }

  generateReport();
}

try {
  main();
} catch (err) {
  console.error(`[migrate] FATAL: ${err.message}`);
  process.exit(1);
}
