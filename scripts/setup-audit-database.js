/**
 * Audit Database Setup Script
 * Creates agent_audit_log table with indexes and views
 * Windows compatible: No Unicode
 * Performance: <1s setup time
 */

const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');

// Paths
const HOOKS_DIR = path.join(__dirname, '..', 'hooks', '12fa');
const DB_PATH = path.join(HOOKS_DIR, 'agent-reality-map.db');
const SQL_SCHEMA = path.join(__dirname, 'create-audit-table.sql');

/**
 * Check if database file exists
 */
function checkDatabaseExists() {
  return fs.existsSync(DB_PATH);
}

/**
 * Create database if it doesn't exist
 */
function createDatabase() {
  return new Promise((resolve, reject) => {
    console.log('[setup] Creating database at:', DB_PATH);

    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE, (err) => {
      if (err) {
        reject(new Error(`Failed to create database: ${err.message}`));
      } else {
        console.log('[setup] Database created successfully');
        db.close();
        resolve();
      }
    });
  });
}

/**
 * Run SQL schema file
 */
function runSchemaFile() {
  return new Promise((resolve, reject) => {
    console.log('[setup] Reading schema file:', SQL_SCHEMA);

    // Read SQL file
    let sqlContent;
    try {
      sqlContent = fs.readFileSync(SQL_SCHEMA, 'utf8');
    } catch (err) {
      return reject(new Error(`Failed to read schema file: ${err.message}`));
    }

    console.log('[setup] Executing schema SQL...');

    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE, (err) => {
      if (err) {
        return reject(new Error(`Failed to open database: ${err.message}`));
      }
    });

    // Execute SQL (sqlite3 doesn't support exec with multiple statements well, so use serialize)
    db.serialize(() => {
      db.exec(sqlContent, (err) => {
        if (err) {
          db.close();
          return reject(new Error(`Failed to execute schema: ${err.message}`));
        }

        console.log('[setup] Schema executed successfully');
        db.close();
        resolve();
      });
    });
  });
}

/**
 * Verify table was created
 */
function verifyTableCreated() {
  return new Promise((resolve, reject) => {
    console.log('[setup] Verifying table creation...');

    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READONLY, (err) => {
      if (err) {
        return reject(new Error(`Failed to open database: ${err.message}`));
      }
    });

    const query = `
      SELECT name FROM sqlite_master
      WHERE type='table' AND name='agent_audit_log'
    `;

    db.get(query, [], (err, row) => {
      db.close();

      if (err) {
        return reject(new Error(`Verification query failed: ${err.message}`));
      }

      if (!row) {
        return reject(new Error('Table agent_audit_log was not created'));
      }

      console.log('[setup] Table verification successful');
      resolve();
    });
  });
}

/**
 * Insert test record
 */
function insertTestRecord() {
  return new Promise((resolve, reject) => {
    console.log('[setup] Inserting test record...');

    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READWRITE, (err) => {
      if (err) {
        return reject(new Error(`Failed to open database: ${err.message}`));
      }
    });

    const query = `
      INSERT INTO agent_audit_log (
        timestamp,
        agent_id,
        agent_role,
        operation,
        tool_name,
        allowed,
        budget_impact,
        session_id,
        metadata
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const params = [
      new Date().toISOString(),
      'test-agent',
      'test-role',
      'database-setup-test',
      'setup-script',
      1,
      0.0,
      'test-session',
      JSON.stringify({ test: true, version: '1.0' })
    ];

    db.run(query, params, function(err) {
      if (err) {
        db.close();
        return reject(new Error(`Test insert failed: ${err.message}`));
      }

      console.log('[setup] Test record inserted with ID:', this.lastID);
      db.close();
      resolve(this.lastID);
    });
  });
}

/**
 * Run validation queries
 */
function runValidationQueries() {
  return new Promise((resolve, reject) => {
    console.log('[setup] Running validation queries...');

    const db = new sqlite3.Database(DB_PATH, sqlite3.OPEN_READONLY, (err) => {
      if (err) {
        return reject(new Error(`Failed to open database: ${err.message}`));
      }
    });

    const queries = [
      // Count total records
      { name: 'Total records', sql: 'SELECT COUNT(*) as count FROM agent_audit_log' },

      // Test denied_operations view
      { name: 'Denied operations view', sql: 'SELECT COUNT(*) as count FROM denied_operations' },

      // Test budget_impact_summary view
      { name: 'Budget summary view', sql: 'SELECT COUNT(*) as count FROM budget_impact_summary' },

      // Test recent_activity view
      { name: 'Recent activity view', sql: 'SELECT COUNT(*) as count FROM recent_activity' },

      // Test indexes exist
      { name: 'Index count', sql: "SELECT COUNT(*) as count FROM sqlite_master WHERE type='index' AND tbl_name='agent_audit_log'" }
    ];

    let completed = 0;
    const results = [];

    queries.forEach((queryInfo) => {
      db.get(queryInfo.sql, [], (err, row) => {
        if (err) {
          console.error(`[setup] Query "${queryInfo.name}" failed:`, err.message);
          results.push({ name: queryInfo.name, success: false, error: err.message });
        } else {
          console.log(`[setup] Query "${queryInfo.name}":`, row);
          results.push({ name: queryInfo.name, success: true, result: row });
        }

        completed++;
        if (completed === queries.length) {
          db.close();

          // Check if any failed
          const failures = results.filter(r => !r.success);
          if (failures.length > 0) {
            return reject(new Error(`${failures.length} validation queries failed`));
          }

          console.log('[setup] All validation queries passed');
          resolve(results);
        }
      });
    });
  });
}

/**
 * Display setup summary
 */
function displaySummary(testRecordId, validationResults) {
  console.log('\n========================================');
  console.log('AUDIT DATABASE SETUP COMPLETE');
  console.log('========================================');
  console.log(`Database: ${DB_PATH}`);
  console.log(`Schema: ${SQL_SCHEMA}`);
  console.log(`Test Record ID: ${testRecordId}`);
  console.log('\nValidation Results:');
  validationResults.forEach(result => {
    const status = result.success ? 'PASS' : 'FAIL';
    console.log(`  [${status}] ${result.name}:`, result.result || result.error);
  });
  console.log('\nNext Steps:');
  console.log('  1. Run test suite: node tests/test-audit-database.js');
  console.log('  2. Verify post-audit-trail hook integration');
  console.log('  3. Check query performance with real data');
  console.log('========================================\n');
}

/**
 * Main setup function
 */
async function main() {
  try {
    console.log('\n[setup] Starting audit database setup...\n');

    // Step 1: Check/create database
    if (!checkDatabaseExists()) {
      await createDatabase();
    } else {
      console.log('[setup] Database already exists, will update schema');
    }

    // Step 2: Run schema file
    await runSchemaFile();

    // Step 3: Verify table created
    await verifyTableCreated();

    // Step 4: Insert test record
    const testRecordId = await insertTestRecord();

    // Step 5: Run validation queries
    const validationResults = await runValidationQueries();

    // Step 6: Display summary
    displaySummary(testRecordId, validationResults);

    console.log('[setup] Setup completed successfully!\n');
    process.exit(0);

  } catch (error) {
    console.error('\n[setup] SETUP FAILED:', error.message);
    console.error('[setup] Stack trace:', error.stack);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

module.exports = { main };
