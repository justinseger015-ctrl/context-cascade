import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright Configuration for E2E Integration Tests
 * P4_T7 - End-to-End Workflows with Docker Compose
 *
 * Features:
 * - Docker Compose integration
 * - PostgreSQL/Redis/Memory MCP backends
 * - WebSocket real-time testing
 * - Multi-browser testing
 * - Parallel execution
 * - Visual regression
 * - Accessibility validation
 */

export default defineConfig({
  testDir: './tests/e2e/workflows',
  testMatch: '**/*.spec.ts',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1, // Retry once locally, twice in CI
  workers: process.env.CI ? 2 : 4, // More workers locally for speed
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/e2e-results.json' }],
    ['junit', { outputFile: 'test-results/e2e-junit.xml' }],
    ['list'], // Console output
  ],

  // Global timeout for each test
  timeout: 60000, // 60 seconds for complex E2E workflows

  // Expect timeout for assertions
  expect: {
    timeout: 10000, // 10 seconds for assertions
  },

  use: {
    // Base URL for Docker Compose environment
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',

    // API endpoint for backend
    extraHTTPHeaders: {
      'Accept': 'application/json',
    },

    // Trace on first retry and failure
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on first retry
    video: 'retain-on-failure',

    // Collect browser console logs
    launchOptions: {
      args: ['--disable-dev-shm-usage'], // Docker compatibility
    },

    // Context options
    contextOptions: {
      ignoreHTTPSErrors: true, // Docker self-signed certs
    },
  },

  // Test projects for different browsers
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 },
      },
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        viewport: { width: 1920, height: 1080 },
      },
    },
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        viewport: { width: 1920, height: 1080 },
      },
    },
    // Mobile testing
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 5'],
      },
    },
    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 13'],
      },
    },
  ],

  // Global setup and teardown
  globalSetup: require.resolve('./tests/e2e/global-setup.ts'),
  globalTeardown: require.resolve('./tests/e2e/global-teardown.ts'),

  // Web server configuration (use Docker Compose instead)
  // webServer is disabled - Docker Compose handles all services
  // Run: docker-compose -f docker-compose.test.yml up before tests
});
