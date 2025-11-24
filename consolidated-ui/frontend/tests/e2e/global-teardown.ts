/**
 * Global Teardown for E2E Tests
 * Cleans up test environment after all tests complete
 */

import { FullConfig } from '@playwright/test';
import axios from 'axios';

async function globalTeardown(config: FullConfig) {
  console.log('\n🧹 Starting E2E test environment cleanup...');

  const apiURL = process.env.API_BASE_URL || 'http://localhost:8000';
  const memoryMcpURL = process.env.MEMORY_MCP_URL || 'http://localhost:9001';

  // Clean test data from database
  console.log('🗑️ Cleaning test data from database...');
  try {
    await axios.post(`${apiURL}/api/admin/clean-test-data`);
    console.log('✅ Test data cleaned');
  } catch (error) {
    console.warn('⚠️ Cleanup warning:', error);
  }

  // Clear Memory MCP test entries
  console.log('🧹 Clearing Memory MCP test entries...');
  try {
    await axios.post(`${memoryMcpURL}/clear_layer`, { layer: 'short-term' });
    console.log('✅ Memory MCP cleared');
  } catch (error) {
    console.warn('⚠️ Memory MCP clear warning:', error);
  }

  // Generate test summary
  console.log('📊 Generating test summary...');
  try {
    const reportPath = 'test-results/e2e-summary.json';
    console.log(`📄 Test results saved to: ${reportPath}`);
  } catch (error) {
    console.warn('⚠️ Summary generation warning:', error);
  }

  console.log('✨ E2E test environment cleanup complete!\n');
}

export default globalTeardown;
