/**
 * WCAG 2.1 AA Accessibility Testing with axe-core
 * Automated + Manual Testing Guidance
 *
 * Usage: npm run test:a11y
 */

const { chromium } = require('@playwright/test');
const { injectAxe, checkA11y, getViolations } = require('axe-playwright');
const fs = require('fs');
const path = require('path');

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:5173';
const RESULTS_FILE = './axe-core-scan-results.json';

const testResults = {
  timestamp: new Date().toISOString(),
  url: FRONTEND_URL,
  standard: 'WCAG 2.1 AA',
  pages: [],
  summary: {
    totalPages: 0,
    totalViolations: 0,
    critical: 0,
    serious: 0,
    moderate: 0,
    minor: 0
  },
  manualTestsRequired: []
};

// Pages to test
const PAGES_TO_TEST = [
  { path: '/', name: 'Dashboard Home' },
  { path: '/tasks', name: 'Tasks Page' },
  { path: '/calendar', name: 'Calendar Page' },
  { path: '/settings', name: 'Settings Page' },
  { path: '/login', name: 'Login Page' }
];

// Manual testing checklist
const MANUAL_TESTS = [
  {
    category: 'Keyboard Navigation',
    tests: [
      'Tab through all interactive elements in logical order',
      'Verify focus indicators are visible on all focusable elements',
      'Test Shift+Tab for reverse navigation',
      'Ensure no keyboard traps exist',
      'Test Escape key closes modals/dialogs',
      'Verify Skip to Main Content link works',
      'Test arrow keys in calendar navigation',
      'Verify drag-and-drop works with keyboard only (Space/Enter to grab, arrows to move, Space/Enter to drop)'
    ]
  },
  {
    category: 'Screen Reader Testing',
    tests: [
      'Test with NVDA (Windows) - download from https://www.nvaccess.org/',
      'Test with JAWS (Windows) - https://www.freedomscientific.com/products/software/jaws/',
      'Verify all images have alt text or aria-labels',
      'Check form labels are properly associated',
      'Verify ARIA landmarks (main, navigation, complementary)',
      'Test calendar announcements for date changes',
      'Verify task status changes are announced',
      'Test drag-and-drop with screen reader feedback'
    ]
  },
  {
    category: 'Color Contrast',
    tests: [
      'Verify text has 4.5:1 contrast ratio (normal text)',
      'Verify large text has 3:1 contrast ratio (18pt+ or 14pt+ bold)',
      'Test with browser color blindness simulators',
      'Verify focus indicators have 3:1 contrast with background',
      'Check interactive elements maintain contrast in all states (hover, focus, active)',
      'Test dark mode if available'
    ]
  },
  {
    category: 'Responsive & Zoom',
    tests: [
      'Test 200% zoom (WCAG requirement)',
      'Test 400% zoom (no horizontal scrolling)',
      'Verify text reflows properly',
      'Test on mobile screen sizes (320px width)',
      'Verify touch targets are 44x44px minimum'
    ]
  },
  {
    category: 'Forms & Validation',
    tests: [
      'Verify error messages are announced',
      'Test required field indicators',
      'Verify autocomplete attributes',
      'Test form submission with keyboard only',
      'Verify validation errors are programmatically associated with inputs'
    ]
  }
];

async function testPage(browser, page, pageInfo) {
  console.log(`\n🧪 Testing: ${pageInfo.name} (${pageInfo.path})`);

  try {
    await page.goto(`${FRONTEND_URL}${pageInfo.path}`, { waitUntil: 'networkidle' });

    // Inject axe-core
    await injectAxe(page);

    // Run axe-core scan
    const results = await page.evaluate(() => {
      return new Promise((resolve) => {
        window.axe.run({
          runOnly: {
            type: 'tag',
            values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']
          }
        }, (err, results) => {
          if (err) throw err;
          resolve(results);
        });
      });
    });

    const pageResult = {
      name: pageInfo.name,
      path: pageInfo.path,
      violations: results.violations.map(violation => ({
        id: violation.id,
        impact: violation.impact,
        description: violation.description,
        help: violation.help,
        helpUrl: violation.helpUrl,
        nodes: violation.nodes.length,
        wcagTags: violation.tags.filter(tag => tag.startsWith('wcag')),
        examples: violation.nodes.slice(0, 3).map(node => ({
          html: node.html,
          target: node.target,
          failureSummary: node.failureSummary
        }))
      })),
      passes: results.passes.length,
      incomplete: results.incomplete.length
    };

    // Count by severity
    pageResult.violations.forEach(v => {
      testResults.summary.totalViolations++;
      switch(v.impact) {
        case 'critical': testResults.summary.critical++; break;
        case 'serious': testResults.summary.serious++; break;
        case 'moderate': testResults.summary.moderate++; break;
        case 'minor': testResults.summary.minor++; break;
      }
    });

    testResults.pages.push(pageResult);

    // Log violations
    if (pageResult.violations.length > 0) {
      console.log(`  ❌ Found ${pageResult.violations.length} violations:`);
      pageResult.violations.forEach(v => {
        const emoji = v.impact === 'critical' ? '🚨' :
                     v.impact === 'serious' ? '🔴' :
                     v.impact === 'moderate' ? '🟡' : '🔵';
        console.log(`    ${emoji} [${v.impact.toUpperCase()}] ${v.id}: ${v.description}`);
        console.log(`       ${v.nodes} instance(s) - ${v.helpUrl}`);
      });
    } else {
      console.log('  ✅ No violations found');
    }

    // Take screenshot for documentation
    await page.screenshot({
      path: `./docs/security/screenshots/${pageInfo.name.toLowerCase().replace(/\s+/g, '-')}.png`,
      fullPage: true
    });

  } catch (error) {
    console.error(`  ❌ Error testing ${pageInfo.name}:`, error.message);
    testResults.pages.push({
      name: pageInfo.name,
      path: pageInfo.path,
      error: error.message
    });
  }
}

async function runAutomatedTests() {
  console.log('🔍 Starting WCAG 2.1 AA Automated Testing with axe-core\n');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // Create screenshots directory
  const screenshotsDir = './docs/security/screenshots';
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  for (const pageInfo of PAGES_TO_TEST) {
    await testPage(browser, page, pageInfo);
  }

  await browser.close();
}

function generateReport() {
  testResults.summary.totalPages = testResults.pages.length;
  testResults.manualTestsRequired = MANUAL_TESTS;

  console.log('\n📊 WCAG 2.1 AA Accessibility Test Summary\n');
  console.log('═'.repeat(80));
  console.log(`Total Pages Tested: ${testResults.summary.totalPages}`);
  console.log(`Total Violations: ${testResults.summary.totalViolations}`);
  console.log('\nSeverity Breakdown:');
  console.log(`🚨 Critical: ${testResults.summary.critical}`);
  console.log(`🔴 Serious: ${testResults.summary.serious}`);
  console.log(`🟡 Moderate: ${testResults.summary.moderate}`);
  console.log(`🔵 Minor: ${testResults.summary.minor}`);
  console.log('═'.repeat(80));

  // Write to file
  fs.writeFileSync(RESULTS_FILE, JSON.stringify(testResults, null, 2));
  console.log(`\n✅ Results saved to ${RESULTS_FILE}`);

  // Print manual test requirements
  console.log('\n📋 MANUAL TESTING REQUIRED:\n');
  console.log('Automated testing covers ~30-50% of WCAG. Manual testing is REQUIRED for:');
  MANUAL_TESTS.forEach(category => {
    console.log(`\n${category.category}:`);
    category.tests.forEach((test, i) => {
      console.log(`  ${i + 1}. ${test}`);
    });
  });

  console.log('\n⚠️ PRIORITY MANUAL TESTS:');
  console.log('  1. Keyboard-only navigation (no mouse!)');
  console.log('  2. NVDA/JAWS screen reader testing');
  console.log('  3. Calendar drag-and-drop with keyboard');
  console.log('  4. Color contrast verification (Chrome DevTools)');

  return testResults.summary.critical + testResults.summary.serious;
}

async function main() {
  try {
    await runAutomatedTests();
    const criticalIssues = generateReport();

    if (criticalIssues > 0) {
      console.error('\n❌ ACCESSIBILITY AUDIT FAILED: Critical/serious violations found!');
      process.exit(1);
    } else {
      console.log('\n✅ AUTOMATED ACCESSIBILITY AUDIT PASSED');
      console.log('⚠️ Remember: Manual testing still required for full WCAG 2.1 AA compliance');
      process.exit(0);
    }

  } catch (error) {
    console.error('❌ Test execution failed:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main, testResults };
