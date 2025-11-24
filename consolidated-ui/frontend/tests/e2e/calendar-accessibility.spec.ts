/**
 * Playwright E2E Accessibility Tests
 *
 * Tests WCAG 2.1 AA compliance in real browser environments
 * Uses @axe-core/playwright for automated scanning
 */

import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y, getViolations } from '@axe-core/playwright';

test.describe('Calendar Component - WCAG 2.1 AA Compliance', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to calendar page
    await page.goto('http://localhost:5173'); // Adjust URL as needed

    // Inject axe-core
    await injectAxe(page);
  });

  test('should pass axe accessibility scan on initial load', async ({ page }) => {
    // Run axe scan
    await checkA11y(page, undefined, {
      detailedReport: true,
      detailedReportOptions: {
        html: true,
      },
    });
  });

  test('should have no color contrast violations', async ({ page }) => {
    await checkA11y(page, undefined, {
      rules: {
        'color-contrast': { enabled: true },
      },
    });
  });

  test('should support keyboard navigation', async ({ page }) => {
    // Tab to first interactive element
    await page.keyboard.press('Tab');

    // Verify focus is visible
    const focusedElement = await page.evaluate(() => {
      const focused = document.activeElement;
      if (!focused) return null;

      const styles = window.getComputedStyle(focused);
      return {
        outline: styles.outline,
        outlineWidth: styles.outlineWidth,
        boxShadow: styles.boxShadow,
      };
    });

    expect(focusedElement).toBeDefined();
    expect(
      focusedElement?.outline !== 'none' ||
      focusedElement?.outlineWidth !== '0px' ||
      focusedElement?.boxShadow !== 'none'
    ).toBe(true);
  });

  test('should navigate view switcher with arrow keys', async ({ page }) => {
    // Find view switcher buttons
    const dayButton = page.getByLabel(/switch to day view/i);
    const weekButton = page.getByLabel(/switch to week view/i);
    const monthButton = page.getByLabel(/switch to month view/i);

    // Focus first button
    await dayButton.focus();
    await expect(dayButton).toBeFocused();

    // Navigate with arrow keys
    await page.keyboard.press('ArrowRight');
    await expect(weekButton).toBeFocused();

    await page.keyboard.press('ArrowRight');
    await expect(monthButton).toBeFocused();

    // Wrap around
    await page.keyboard.press('ArrowRight');
    await expect(dayButton).toBeFocused();
  });

  test('should activate buttons with Enter and Space keys', async ({ page }) => {
    const monthButton = page.getByLabel(/switch to month view/i);

    await monthButton.focus();
    await page.keyboard.press('Enter');

    // Verify month view is active
    await expect(monthButton).toHaveAttribute('aria-pressed', 'true');

    // Switch back with Space
    const weekButton = page.getByLabel(/switch to week view/i);
    await weekButton.focus();
    await page.keyboard.press('Space');

    await expect(weekButton).toHaveAttribute('aria-pressed', 'true');
  });

  test('should announce view changes to screen readers', async ({ page }) => {
    // Click month view
    await page.getByLabel(/switch to month view/i).click();

    // Check for live region update
    const announcement = await page.locator('#a11y-announcer').textContent();

    expect(announcement).toContain('month view');
  });

  test('should have proper ARIA landmarks', async ({ page }) => {
    // Application role
    const calendar = page.getByRole('application', {
      name: /task scheduling calendar/i,
    });
    await expect(calendar).toBeVisible();

    // Navigation role
    const navigation = page.getByRole('navigation', {
      name: /calendar navigation/i,
    });
    await expect(navigation).toBeVisible();

    // Group role for view switcher
    const viewSwitcher = page.getByRole('group', {
      name: /calendar view selector/i,
    });
    await expect(viewSwitcher).toBeVisible();
  });

  test('should support screen reader users', async ({ page }) => {
    // Check for screen reader only elements
    const srElements = await page.locator('.sr-only').count();
    expect(srElements).toBeGreaterThan(0);

    // Verify live region exists
    const liveRegion = page.locator('#calendar-announcements');
    await expect(liveRegion).toHaveAttribute('role', 'status');
    await expect(liveRegion).toHaveAttribute('aria-live', 'polite');
  });

  test('should have proper heading hierarchy', async ({ page }) => {
    await checkA11y(page, undefined, {
      rules: {
        'heading-order': { enabled: true },
      },
    });
  });

  test('should have semantic HTML structure', async ({ page }) => {
    await checkA11y(page, undefined, {
      rules: {
        region: { enabled: true },
        landmark: { enabled: true },
      },
    });
  });

  test('should support high contrast mode', async ({ page }) => {
    // Emulate high contrast mode
    await page.emulateMedia({ forcedColors: 'active' });

    // Verify calendar still renders correctly
    const calendar = page.getByRole('application');
    await expect(calendar).toBeVisible();

    // Run accessibility scan in high contrast
    await checkA11y(page);
  });

  test('should export accessibility report', async ({ page }) => {
    const violations = await getViolations(page);

    const report = {
      url: page.url(),
      timestamp: new Date().toISOString(),
      violations: violations.length,
      details: violations,
    };

    console.log('Accessibility Report:', JSON.stringify(report, null, 2));

    expect(violations.length).toBe(0);
  });
});

test.describe('Screen Reader Testing Simulation', () => {
  test('should navigate with screen reader shortcuts', async ({ page }) => {
    // Navigate to calendar
    await page.goto('http://localhost:5173');

    // Simulate screen reader navigation (headings)
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
    expect(headings.length).toBeGreaterThan(0);

    // Simulate screen reader navigation (landmarks)
    const navigation = await page.getByRole('navigation').all();
    expect(navigation.length).toBeGreaterThan(0);

    // Simulate screen reader navigation (buttons)
    const buttons = await page.getByRole('button').all();
    expect(buttons.length).toBeGreaterThan(0);
  });

  test('should provide descriptive labels for all interactive elements', async ({ page }) => {
    await page.goto('http://localhost:5173');

    // Get all buttons
    const buttons = await page.getByRole('button').all();

    for (const button of buttons) {
      const accessibleName = await button.getAttribute('aria-label') ||
        await button.textContent();

      expect(accessibleName).toBeTruthy();
      expect(accessibleName?.trim().length).toBeGreaterThan(0);
    }
  });
});
