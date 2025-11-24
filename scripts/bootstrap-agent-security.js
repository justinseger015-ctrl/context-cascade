#!/usr/bin/env node

/**
 * Agent Identity & RBAC Migration Script
 *
 * Migrates 207 agents to Agent Reality Map compliance by adding:
 * - Unique UUIDs
 * - RBAC roles (auto-assigned via capability matrix)
 * - Budget limits
 * - Security permissions
 *
 * Features:
 * - Dry-run mode (no modifications)
 * - Automatic backup before migration
 * - Incremental migration (20 agents at a time)
 * - Rollback support
 * - Comprehensive validation
 *
 * Usage:
 *   node scripts/bootstrap-agent-security.js --dry-run
 *   node scripts/bootstrap-agent-security.js --migrate
 *   node scripts/bootstrap-agent-security.js --validate
 *   node scripts/bootstrap-agent-security.js --rollback
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Constants
const PLUGIN_ROOT = path.join(__dirname, '..');
const AGENTS_DIR = path.join(PLUGIN_ROOT, 'agents');
const IDENTITY_DIR = path.join(PLUGIN_ROOT, 'agents', 'identity');
const BACKUP_DIR = path.join(PLUGIN_ROOT, '.agent-migration-backup');

// Load schemas
const identitySchema = JSON.parse(fs.readFileSync(path.join(IDENTITY_DIR, 'agent-identity-schema.json'), 'utf8'));
const rbacRules = JSON.parse(fs.readFileSync(path.join(IDENTITY_DIR, 'agent-rbac-rules.json'), 'utf8'));
const capabilityMatrix = JSON.parse(fs.readFileSync(path.join(IDENTITY_DIR, 'agent-capability-matrix.json'), 'utf8'));

// State tracking
let migrationState = {
  totalAgents: 0,
  migratedAgents: 0,
  failedAgents: [],
  skippedAgents: [],
  validationErrors: []
};

/**
 * Generate UUIDv4
 */
function generateUUID() {
  return crypto.randomUUID();
}

/**
 * Parse YAML frontmatter from markdown file
 */
function parseFrontmatter(content) {
  const frontmatterRegex = /^---\n([\s\S]*?)\n---/;
  const match = content.match(frontmatterRegex);

  if (!match) {
    return { frontmatter: null, content: content };
  }

  const frontmatterText = match[1];
  const remainingContent = content.substring(match[0].length);

  // Simple YAML parser (good enough for our needs)
  const frontmatter = {};
  const lines = frontmatterText.split('\n');
  let currentKey = null;
  let currentArray = null;

  for (const line of lines) {
    if (line.trim() === '') continue;

    // Handle array items
    if (line.trim().startsWith('-')) {
      if (currentArray) {
        currentArray.push(line.trim().substring(1).trim());
      }
      continue;
    }

    // Handle key-value pairs
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      const value = line.substring(colonIndex + 1).trim();

      if (value === '') {
        // Start of array
        currentKey = key;
        currentArray = [];
        frontmatter[key] = currentArray;
      } else if (value.startsWith('"') && value.endsWith('"')) {
        // Quoted string
        frontmatter[key] = value.substring(1, value.length - 1);
      } else if (value === 'true' || value === 'false') {
        // Boolean
        frontmatter[key] = value === 'true';
      } else if (!isNaN(value)) {
        // Number
        frontmatter[key] = parseFloat(value);
      } else {
        // Plain string
        frontmatter[key] = value;
      }
    }
  }

  return { frontmatter, content: remainingContent };
}

/**
 * Serialize frontmatter to YAML
 */
function serializeFrontmatter(frontmatter) {
  let yaml = '';

  for (const [key, value] of Object.entries(frontmatter)) {
    if (Array.isArray(value)) {
      yaml += `${key}:\n`;
      for (const item of value) {
        if (typeof item === 'string') {
          yaml += `  - ${item}\n`;
        } else {
          yaml += `  - ${JSON.stringify(item)}\n`;
        }
      }
    } else if (typeof value === 'object' && value !== null) {
      yaml += `${key}:\n`;
      for (const [subKey, subValue] of Object.entries(value)) {
        if (Array.isArray(subValue)) {
          yaml += `  ${subKey}:\n`;
          for (const item of subValue) {
            yaml += `    - ${item}\n`;
          }
        } else if (typeof subValue === 'object' && subValue !== null) {
          yaml += `  ${subKey}:\n`;
          for (const [subSubKey, subSubValue] of Object.entries(subValue)) {
            yaml += `    ${subSubKey}: ${subSubValue}\n`;
          }
        } else if (typeof subValue === 'string') {
          yaml += `  ${subKey}: "${subValue}"\n`;
        } else {
          yaml += `  ${subKey}: ${subValue}\n`;
        }
      }
    } else if (typeof value === 'string') {
      yaml += `${key}: "${value}"\n`;
    } else {
      yaml += `${key}: ${value}\n`;
    }
  }

  return yaml;
}

/**
 * Assign RBAC role to agent based on capabilities and category
 */
function assignRole(agentName, capabilities, category) {
  // Step 1: Try capability-based matching
  for (const rule of capabilityMatrix.capability_to_role_mapping.rules) {
    const matchCount = rule.capabilities.filter(cap =>
      capabilities.some(agentCap =>
        agentCap.toLowerCase().includes(cap.toLowerCase()) ||
        cap.toLowerCase().includes(agentCap.toLowerCase())
      )
    ).length;

    if (matchCount > 0 && rule.confidence >= 0.7) {
      return {
        role: rule.assigned_role,
        confidence: rule.confidence,
        reasoning: rule.reasoning
      };
    }
  }

  // Step 2: Try category-based matching
  const categoryParts = category.split('/');
  const mainCategory = categoryParts[0];
  const subCategory = categoryParts[1];

  if (capabilityMatrix.agent_category_to_role_mapping[mainCategory]) {
    const categoryMapping = capabilityMatrix.agent_category_to_role_mapping[mainCategory];

    if (subCategory && categoryMapping.subcategories && categoryMapping.subcategories[subCategory]) {
      return {
        role: categoryMapping.subcategories[subCategory],
        confidence: 0.8,
        reasoning: `Category mapping: ${mainCategory}/${subCategory}`
      };
    }

    return {
      role: categoryMapping.default_role,
      confidence: 0.7,
      reasoning: `Category mapping: ${mainCategory}`
    };
  }

  // Step 3: Fallback to developer role
  return {
    role: 'developer',
    confidence: 0.5,
    reasoning: 'Fallback to default developer role'
  };
}

/**
 * Generate identity metadata for agent
 */
function generateIdentityMetadata(agentName, frontmatter, filePath) {
  // Extract category from file path
  const relativePath = path.relative(AGENTS_DIR, filePath);
  const category = path.dirname(relativePath).split(path.sep)[0] || 'foundry';

  // Extract capabilities
  const capabilities = frontmatter.capabilities || [];

  // Assign role
  const roleAssignment = assignRole(agentName, capabilities, category);

  // Get RBAC rules for role
  const rbacForRole = rbacRules.roles[roleAssignment.role];

  // Generate identity metadata
  const identity = {
    agent_id: generateUUID(),
    role: roleAssignment.role,
    role_confidence: roleAssignment.confidence,
    role_reasoning: roleAssignment.reasoning
  };

  // Generate RBAC metadata
  const rbac = {
    allowed_tools: rbacForRole.permissions.tools.filter(tool => tool !== '*'),
    denied_tools: [],
    path_scopes: rbacForRole.permissions.paths,
    api_access: rbacForRole.permissions.api_access || [],
    requires_approval: rbacForRole.permissions.requires_approval,
    approval_threshold: rbacForRole.permissions.approval_threshold || 10.0
  };

  // Generate budget metadata
  const budget = {
    max_tokens_per_session: rbacForRole.budget.max_tokens_per_session,
    max_cost_per_day: rbacForRole.budget.max_cost_per_day,
    currency: "USD"
  };

  // Generate metadata
  const metadata = {
    category: category,
    specialist: frontmatter.specialist || false,
    requires_approval: frontmatter.requires_approval || false,
    version: frontmatter.version || "1.0.0",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    tags: frontmatter.tags || []
  };

  return { identity, rbac, budget, metadata };
}

/**
 * Migrate single agent file
 */
function migrateAgent(filePath, dryRun = false) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const { frontmatter, content: remainingContent } = parseFrontmatter(content);

    if (!frontmatter) {
      migrationState.skippedAgents.push({
        file: filePath,
        reason: 'No frontmatter found'
      });
      return false;
    }

    // Skip if already migrated
    if (frontmatter.identity && frontmatter.identity.agent_id) {
      migrationState.skippedAgents.push({
        file: filePath,
        reason: 'Already migrated (has agent_id)'
      });
      return false;
    }

    const agentName = frontmatter.name || path.basename(filePath, '.md');

    // Generate new metadata
    const { identity, rbac, budget, metadata } = generateIdentityMetadata(agentName, frontmatter, filePath);

    // Merge with existing frontmatter
    const updatedFrontmatter = {
      ...frontmatter,
      identity,
      rbac,
      budget,
      metadata: {
        ...frontmatter.metadata,
        ...metadata
      }
    };

    // Serialize back to YAML + Markdown
    const updatedContent = `---\n${serializeFrontmatter(updatedFrontmatter)}---${remainingContent}`;

    if (!dryRun) {
      fs.writeFileSync(filePath, updatedContent, 'utf8');
    }

    console.log(`✅ Migrated: ${agentName} (${filePath})`);
    console.log(`   Role: ${identity.role} (confidence: ${identity.role_confidence})`);
    console.log(`   Budget: $${budget.max_cost_per_day}/day, ${budget.max_tokens_per_session} tokens/session`);

    migrationState.migratedAgents++;
    return true;

  } catch (error) {
    migrationState.failedAgents.push({
      file: filePath,
      error: error.message
    });
    console.error(`❌ Failed to migrate ${filePath}: ${error.message}`);
    return false;
  }
}

/**
 * Find all agent files recursively
 */
function findAgentFiles(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      // Skip identity directory
      if (entry.name === 'identity') continue;
      findAgentFiles(fullPath, files);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(fullPath);
    }
  }

  return files;
}

/**
 * Create backup of agents directory
 */
function createBackup() {
  if (fs.existsSync(BACKUP_DIR)) {
    console.log('⚠️  Backup already exists. Remove it first or use --rollback.');
    return false;
  }

  console.log('📦 Creating backup...');
  fs.mkdirSync(BACKUP_DIR, { recursive: true });

  const agentFiles = findAgentFiles(AGENTS_DIR);

  for (const file of agentFiles) {
    const relativePath = path.relative(AGENTS_DIR, file);
    const backupPath = path.join(BACKUP_DIR, relativePath);
    fs.mkdirSync(path.dirname(backupPath), { recursive: true });
    fs.copyFileSync(file, backupPath);
  }

  console.log(`✅ Backed up ${agentFiles.length} files to ${BACKUP_DIR}`);
  return true;
}

/**
 * Rollback migration
 */
function rollback() {
  if (!fs.existsSync(BACKUP_DIR)) {
    console.log('❌ No backup found. Cannot rollback.');
    return false;
  }

  console.log('🔄 Rolling back migration...');

  const backupFiles = findAgentFiles(BACKUP_DIR);

  for (const backupFile of backupFiles) {
    const relativePath = path.relative(BACKUP_DIR, backupFile);
    const originalPath = path.join(AGENTS_DIR, relativePath);
    fs.copyFileSync(backupFile, originalPath);
  }

  // Remove backup directory
  fs.rmSync(BACKUP_DIR, { recursive: true, force: true });

  console.log(`✅ Rolled back ${backupFiles.length} files`);
  return true;
}

/**
 * Validate migrated agents
 */
function validate() {
  console.log('🔍 Validating migrated agents...');

  const agentFiles = findAgentFiles(AGENTS_DIR);
  const validationResults = {
    totalAgents: agentFiles.length,
    validAgents: 0,
    invalidAgents: [],
    duplicateUUIDs: []
  };

  const uuidMap = new Map();

  for (const file of agentFiles) {
    try {
      const content = fs.readFileSync(file, 'utf8');
      const { frontmatter } = parseFrontmatter(content);

      if (!frontmatter) {
        validationResults.invalidAgents.push({
          file,
          reason: 'No frontmatter'
        });
        continue;
      }

      // Check for required fields
      if (!frontmatter.identity || !frontmatter.identity.agent_id) {
        validationResults.invalidAgents.push({
          file,
          reason: 'Missing identity.agent_id'
        });
        continue;
      }

      if (!frontmatter.rbac) {
        validationResults.invalidAgents.push({
          file,
          reason: 'Missing rbac'
        });
        continue;
      }

      if (!frontmatter.budget) {
        validationResults.invalidAgents.push({
          file,
          reason: 'Missing budget'
        });
        continue;
      }

      // Check for duplicate UUIDs
      const uuid = frontmatter.identity.agent_id;
      if (uuidMap.has(uuid)) {
        validationResults.duplicateUUIDs.push({
          uuid,
          files: [uuidMap.get(uuid), file]
        });
      } else {
        uuidMap.set(uuid, file);
      }

      validationResults.validAgents++;

    } catch (error) {
      validationResults.invalidAgents.push({
        file,
        reason: error.message
      });
    }
  }

  console.log(`\n📊 Validation Results:`);
  console.log(`   Total agents: ${validationResults.totalAgents}`);
  console.log(`   Valid agents: ${validationResults.validAgents}`);
  console.log(`   Invalid agents: ${validationResults.invalidAgents.length}`);
  console.log(`   Duplicate UUIDs: ${validationResults.duplicateUUIDs.length}`);

  if (validationResults.invalidAgents.length > 0) {
    console.log(`\n❌ Invalid agents:`);
    for (const invalid of validationResults.invalidAgents) {
      console.log(`   ${invalid.file}: ${invalid.reason}`);
    }
  }

  if (validationResults.duplicateUUIDs.length > 0) {
    console.log(`\n⚠️  Duplicate UUIDs found:`);
    for (const dup of validationResults.duplicateUUIDs) {
      console.log(`   UUID ${dup.uuid}:`);
      for (const file of dup.files) {
        console.log(`     - ${file}`);
      }
    }
  }

  return validationResults.invalidAgents.length === 0 && validationResults.duplicateUUIDs.length === 0;
}

/**
 * Main migration function
 */
function migrate(dryRun = false, batchSize = 20) {
  console.log(`\n🚀 Starting agent migration (${dryRun ? 'DRY RUN' : 'LIVE'})...\n`);

  if (!dryRun) {
    if (!createBackup()) {
      return false;
    }
  }

  const agentFiles = findAgentFiles(AGENTS_DIR);
  migrationState.totalAgents = agentFiles.length;

  console.log(`Found ${agentFiles.length} agent files\n`);

  // Process in batches
  for (let i = 0; i < agentFiles.length; i += batchSize) {
    const batch = agentFiles.slice(i, i + batchSize);
    console.log(`\n📦 Processing batch ${Math.floor(i / batchSize) + 1} (${batch.length} agents)...\n`);

    for (const file of batch) {
      migrateAgent(file, dryRun);
    }
  }

  // Print summary
  console.log(`\n📊 Migration Summary:`);
  console.log(`   Total agents: ${migrationState.totalAgents}`);
  console.log(`   Migrated: ${migrationState.migratedAgents}`);
  console.log(`   Skipped: ${migrationState.skippedAgents.length}`);
  console.log(`   Failed: ${migrationState.failedAgents.length}`);

  if (migrationState.skippedAgents.length > 0) {
    console.log(`\n⚠️  Skipped agents:`);
    for (const skipped of migrationState.skippedAgents) {
      console.log(`   ${skipped.file}: ${skipped.reason}`);
    }
  }

  if (migrationState.failedAgents.length > 0) {
    console.log(`\n❌ Failed agents:`);
    for (const failed of migrationState.failedAgents) {
      console.log(`   ${failed.file}: ${failed.error}`);
    }
  }

  if (!dryRun && migrationState.failedAgents.length === 0) {
    console.log(`\n✅ Migration complete! Run with --validate to verify.`);
  }

  return migrationState.failedAgents.length === 0;
}

// CLI
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
Agent Identity & RBAC Migration Script

Usage:
  node bootstrap-agent-security.js [OPTIONS]

Options:
  --dry-run          Show what would be migrated without making changes
  --migrate          Perform actual migration with backup
  --validate         Validate migrated agents
  --rollback         Rollback to backup
  --batch-size N     Process N agents at a time (default: 20)
  --help, -h         Show this help message

Examples:
  # See what would be migrated
  node bootstrap-agent-security.js --dry-run

  # Migrate all agents
  node bootstrap-agent-security.js --migrate

  # Validate migration
  node bootstrap-agent-security.js --validate

  # Rollback if needed
  node bootstrap-agent-security.js --rollback
  `);
  process.exit(0);
}

if (args.includes('--dry-run')) {
  migrate(true);
} else if (args.includes('--migrate')) {
  const batchSizeIndex = args.indexOf('--batch-size');
  const batchSize = batchSizeIndex !== -1 ? parseInt(args[batchSizeIndex + 1]) : 20;
  migrate(false, batchSize);
} else if (args.includes('--validate')) {
  const isValid = validate();
  process.exit(isValid ? 0 : 1);
} else if (args.includes('--rollback')) {
  rollback();
} else {
  console.log('Please specify an option. Use --help for usage information.');
  process.exit(1);
}
