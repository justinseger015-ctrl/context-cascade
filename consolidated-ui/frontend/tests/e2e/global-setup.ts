/**
 * Global Setup for E2E Tests
 * Initializes test environment before running tests
 */

import { FullConfig } from '@playwright/test';
import axios from 'axios';

async function globalSetup(config: FullConfig) {
  console.log('🚀 Starting E2E test environment setup...');

  const baseURL = config.use?.baseURL || 'http://localhost:3000';
  const apiURL = process.env.API_BASE_URL || 'http://localhost:8000';
  const memoryMcpURL = process.env.MEMORY_MCP_URL || 'http://localhost:9001';

  // Wait for services to be ready
  await waitForService(apiURL, '/health', 'Backend API', 60000);
  await waitForService(baseURL, '/', 'Frontend', 60000);
  await waitForService(memoryMcpURL, '/health', 'Memory MCP', 30000);

  // Run database migrations
  console.log('📊 Running database migrations...');
  try {
    await axios.post(`${apiURL}/api/admin/migrate`);
    console.log('✅ Database migrations completed');
  } catch (error) {
    console.warn('⚠️ Migration warning:', error);
  }

  // Seed test data
  console.log('🌱 Seeding test data...');
  try {
    await axios.post(`${apiURL}/api/admin/seed-test-data`);
    console.log('✅ Test data seeded');
  } catch (error) {
    console.warn('⚠️ Seeding warning:', error);
  }

  // Clear Memory MCP short-term layer
  console.log('🧹 Clearing Memory MCP test data...');
  try {
    await axios.post(`${memoryMcpURL}/clear_layer`, { layer: 'short-term' });
    console.log('✅ Memory MCP cleared');
  } catch (error) {
    console.warn('⚠️ Memory MCP clear warning:', error);
  }

  console.log('✨ E2E test environment setup complete!\n');
}

/**
 * Wait for service to be ready
 */
async function waitForService(
  baseUrl: string,
  endpoint: string,
  serviceName: string,
  timeout: number
): Promise<void> {
  const startTime = Date.now();
  const url = `${baseUrl}${endpoint}`;

  console.log(`⏳ Waiting for ${serviceName} at ${url}...`);

  while (Date.now() - startTime < timeout) {
    try {
      const response = await axios.get(url, {
        timeout: 5000,
        validateStatus: (status) => status < 500, // Accept any non-500 status
      });

      if (response.status < 400) {
        console.log(`✅ ${serviceName} is ready`);
        return;
      }
    } catch (error) {
      // Service not ready yet, continue waiting
    }

    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  throw new Error(
    `❌ ${serviceName} did not become ready within ${timeout}ms. ` +
    `Please ensure Docker Compose services are running: ` +
    `docker-compose -f docker-compose.test.yml up`
  );
}

export default globalSetup;
