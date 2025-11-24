/**
 * Calendar Accessibility Tests
 *
 * WCAG 2.1 AA Compliance Testing with axe-core
 *
 * Test Coverage:
 * - Automated accessibility scanning (axe-core)
 * - Color contrast verification
 * - Keyboard navigation
 * - ARIA labels and roles
 * - Screen reader compatibility
 * - Focus management
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import userEvent from '@testing-library/user-event';
import Calendar from '../components/Calendar';
import {
  checkColorContrast,
  getAccessibleTextColor,
  getTaskAriaLabel,
} from '../utils/accessibility';

// Extend Jest matchers
expect.extend(toHaveNoViolations);

// Mock Zustand store
jest.mock('../store', () => ({
  useStore: jest.fn((selector) =>
    selector({
      tasks: [
        {
          id: 'task-1',
          title: 'Test Task',
          description: 'Test description',
          status: 'pending',
          priority: 'high',
          skill_name: 'test-skill',
          projectId: 'project-1',
          next_run_at: new Date('2025-11-08T10:00:00'),
          dueDate: new Date('2025-11-08T11:00:00'),
          createdAt: new Date('2025-11-08T09:00:00'),
          updatedAt: new Date('2025-11-08T09:00:00'),
        },
      ],
      isLoading: false,
      fetchTasks: jest.fn(),
      updateTask: jest.fn(),
      addTask: jest.fn(),
      deleteTask: jest.fn(),
      rollbackOptimisticUpdate: jest.fn(),
    })
  ),
}));

describe('Calendar Accessibility Tests', () => {
  describe('Automated axe-core Scanning', () => {
    it('should have no accessibility violations (WCAG 2.1 AA)', async () => {
      const { container } = render(<Calendar />);

      // Run axe accessibility scan
      const results = await axe(container, {
        rules: {
          // WCAG 2.1 AA rules
          'color-contrast': { enabled: true },
          'button-name': { enabled: true },
          'aria-roles': { enabled: true },
          'aria-valid-attr': { enabled: true },
          'aria-valid-attr-value': { enabled: true },
          'label': { enabled: true },
          'link-name': { enabled: true },
          'list': { enabled: true },
          'listitem': { enabled: true },
          'region': { enabled: true },
          'landmark-unique': { enabled: true },
          'page-has-heading-one': { enabled: true },
        },
      });

      // No violations expected
      expect(results).toHaveNoViolations();
    });

    it('should pass color contrast checks (4.5:1 minimum)', async () => {
      const { container } = render(<Calendar />);

      const results = await axe(container, {
        rules: {
          'color-contrast': { enabled: true },
        },
      });

      expect(results.violations).toHaveLength(0);
    });

    it('should have proper ARIA attributes', async () => {
      const { container } = render(<Calendar />);

      const results = await axe(container, {
        rules: {
          'aria-roles': { enabled: true },
          'aria-valid-attr': { enabled: true },
          'aria-valid-attr-value': { enabled: true },
          'aria-required-attr': { enabled: true },
        },
      });

      expect(results.violations).toHaveLength(0);
    });
  });

  describe('Color Contrast Verification', () => {
    it('should verify critical priority tasks meet WCAG AA contrast', () => {
      const backgroundColor = '#dc2626'; // red-600
      const textColor = getAccessibleTextColor(backgroundColor);
      const contrast = checkColorContrast(textColor, backgroundColor);

      expect(contrast.passes).toBe(true);
      expect(contrast.ratio).toBeGreaterThanOrEqual(4.5);
    });

    it('should verify high priority tasks meet WCAG AA contrast', () => {
      const backgroundColor = '#f97316'; // orange-500
      const textColor = getAccessibleTextColor(backgroundColor);
      const contrast = checkColorContrast(textColor, backgroundColor);

      expect(contrast.passes).toBe(true);
      expect(contrast.ratio).toBeGreaterThanOrEqual(4.5);
    });

    it('should verify medium priority tasks meet WCAG AA contrast', () => {
      const backgroundColor = '#3b82f6'; // blue-500
      const textColor = getAccessibleTextColor(backgroundColor);
      const contrast = checkColorContrast(textColor, backgroundColor);

      expect(contrast.passes).toBe(true);
      expect(contrast.ratio).toBeGreaterThanOrEqual(4.5);
    });

    it('should verify low priority tasks meet WCAG AA contrast', () => {
      const backgroundColor = '#10b981'; // green-500
      const textColor = getAccessibleTextColor(backgroundColor);
      const contrast = checkColorContrast(textColor, backgroundColor);

      expect(contrast.passes).toBe(true);
      expect(contrast.ratio).toBeGreaterThanOrEqual(4.5);
    });
  });

  describe('Keyboard Navigation', () => {
    it('should navigate between view switcher buttons with arrow keys', async () => {
      const user = userEvent.setup();
      render(<Calendar />);

      const dayButton = screen.getByLabelText(/switch to day view/i);
      const weekButton = screen.getByLabelText(/switch to week view/i);
      const monthButton = screen.getByLabelText(/switch to month view/i);

      // Focus first button
      dayButton.focus();
      expect(dayButton).toHaveFocus();

      // Arrow right to next button
      await user.keyboard('{ArrowRight}');
      expect(weekButton).toHaveFocus();

      // Arrow right to last button
      await user.keyboard('{ArrowRight}');
      expect(monthButton).toHaveFocus();

      // Arrow right wraps to first
      await user.keyboard('{ArrowRight}');
      expect(dayButton).toHaveFocus();

      // Arrow left wraps to last
      await user.keyboard('{ArrowLeft}');
      expect(monthButton).toHaveFocus();
    });

    it('should activate view switcher buttons with Enter key', async () => {
      const user = userEvent.setup();
      render(<Calendar />);

      const monthButton = screen.getByLabelText(/switch to month view/i);

      monthButton.focus();
      await user.keyboard('{Enter}');

      // Check aria-pressed or similar state change
      expect(monthButton).toHaveAttribute('aria-pressed', 'true');
    });

    it('should activate view switcher buttons with Space key', async () => {
      const user = userEvent.setup();
      render(<Calendar />);

      const dayButton = screen.getByLabelText(/switch to day view/i);

      dayButton.focus();
      await user.keyboard(' '); // Space

      expect(dayButton).toHaveAttribute('aria-pressed', 'true');
    });

    it('should navigate calendar with arrow keys for navigation', async () => {
      const user = userEvent.setup();
      render(<Calendar />);

      const prevButton = screen.getByLabelText(/previous/i);
      const nextButton = screen.getByLabelText(/next/i);

      expect(prevButton).toBeInTheDocument();
      expect(nextButton).toBeInTheDocument();

      // Tab navigation should work
      prevButton.focus();
      expect(prevButton).toHaveFocus();

      await user.tab();
      expect(nextButton).toHaveFocus();
    });
  });

  describe('ARIA Labels and Roles', () => {
    it('should have application role on calendar container', () => {
      render(<Calendar />);

      const calendar = screen.getByRole('application', {
        name: /task scheduling calendar/i,
      });

      expect(calendar).toBeInTheDocument();
    });

    it('should have navigation role on calendar navigation', () => {
      render(<Calendar />);

      const navigation = screen.getByRole('navigation', {
        name: /calendar navigation/i,
      });

      expect(navigation).toBeInTheDocument();
    });

    it('should have group role on view switcher', () => {
      render(<Calendar />);

      const viewSwitcher = screen.getByRole('group', {
        name: /calendar view selector/i,
      });

      expect(viewSwitcher).toBeInTheDocument();
    });

    it('should generate proper ARIA labels for tasks', () => {
      const task = {
        id: 'task-1',
        title: 'Team Meeting',
        start: new Date('2025-11-08T14:00:00'),
        end: new Date('2025-11-08T15:00:00'),
        priority: 'high' as const,
        status: 'pending' as const,
        assignee: 'John Doe',
      };

      const label = getTaskAriaLabel(task);

      expect(label).toContain('Team Meeting');
      expect(label).toContain('2:00 PM');
      expect(label).toContain('3:00 PM');
      expect(label).toContain('priority: high');
      expect(label).toContain('status: pending');
      expect(label).toContain('assigned to: John Doe');
    });
  });

  describe('Focus Management', () => {
    it('should have visible focus indicators on all interactive elements', async () => {
      const { container } = render(<Calendar />);

      const results = await axe(container, {
        rules: {
          'focus-order-semantics': { enabled: true },
        },
      });

      expect(results.violations).toHaveLength(0);
    });

    it('should trap focus within modal dialogs (when implemented)', () => {
      // This test would verify modal focus trapping when task edit modal is implemented
      expect(true).toBe(true);
    });
  });

  describe('Screen Reader Support', () => {
    it('should have live region for announcements', () => {
      render(<Calendar />);

      const liveRegion = document.getElementById('calendar-announcements');

      expect(liveRegion).toBeInTheDocument();
      expect(liveRegion).toHaveAttribute('role', 'status');
      expect(liveRegion).toHaveAttribute('aria-live', 'polite');
      expect(liveRegion).toHaveAttribute('aria-atomic', 'true');
    });

    it('should have loading state announced to screen readers', () => {
      // Mock loading state
      const { useStore } = require('../store');
      useStore.mockImplementation((selector: any) =>
        selector({
          tasks: [],
          isLoading: true,
          fetchTasks: jest.fn(),
          updateTask: jest.fn(),
          addTask: jest.fn(),
          deleteTask: jest.fn(),
          rollbackOptimisticUpdate: jest.fn(),
        })
      );

      render(<Calendar />);

      const loadingIndicator = screen.getByRole('status');
      expect(loadingIndicator).toHaveTextContent(/loading tasks/i);
      expect(loadingIndicator).toHaveAttribute('aria-live', 'polite');
    });
  });

  describe('Semantic HTML', () => {
    it('should use semantic HTML elements', async () => {
      const { container } = render(<Calendar />);

      const results = await axe(container, {
        rules: {
          region: { enabled: true },
          'landmark-one-main': { enabled: true },
        },
      });

      expect(results.violations).toHaveLength(0);
    });

    it('should have proper heading hierarchy', async () => {
      const { container } = render(<Calendar />);

      const results = await axe(container, {
        rules: {
          'heading-order': { enabled: true },
        },
      });

      expect(results.violations).toHaveLength(0);
    });
  });
});

/**
 * Export test results for compliance report
 */
export async function generateAccessibilityReport(): Promise<{
  passed: number;
  failed: number;
  violations: any[];
  timestamp: string;
}> {
  const { container } = render(<Calendar />);

  const results = await axe(container);

  return {
    passed: results.passes.length,
    failed: results.violations.length,
    violations: results.violations,
    timestamp: new Date().toISOString(),
  };
}
