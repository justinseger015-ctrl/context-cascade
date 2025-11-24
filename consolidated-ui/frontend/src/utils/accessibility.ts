/**
 * Accessibility Utilities
 *
 * WCAG 2.1 AA compliance helpers:
 * - Color contrast checking
 * - Screen reader announcements
 * - Keyboard navigation
 * - ARIA label generation
 */

import type { A11yAnnouncement, ColorContrast, Task } from '../types/calendar';

/**
 * Calculate relative luminance of a color (WCAG formula)
 * @param r Red value (0-255)
 * @param g Green value (0-255)
 * @param b Blue value (0-255)
 * @returns Relative luminance (0-1)
 */
function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map(val => {
    const sRGB = val / 255;
    return sRGB <= 0.03928
      ? sRGB / 12.92
      : Math.pow((sRGB + 0.055) / 1.055, 2.4);
  });

  return 0.2126 * (rs ?? 0) + 0.7152 * (gs ?? 0) + 0.0722 * (bs ?? 0);
}

/**
 * Convert hex color to RGB
 * @param hex Hex color string (#RRGGBB or #RGB)
 * @returns RGB object or null if invalid
 */
function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
  hex = hex.replace(shorthandRegex, (_, r, g, b) => r + r + g + g + b + b);

  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1] ?? '0', 16),
    g: parseInt(result[2] ?? '0', 16),
    b: parseInt(result[3] ?? '0', 16)
  } : null;
}

/**
 * Calculate contrast ratio between two colors (WCAG formula)
 *
 * @param color1 First color (hex)
 * @param color2 Second color (hex)
 * @returns Contrast ratio (1-21)
 */
export function getContrastRatio(color1: string, color2: string): number {
  const rgb1 = hexToRgb(color1);
  const rgb2 = hexToRgb(color2);

  if (!rgb1 || !rgb2) return 0;

  const lum1 = getLuminance(rgb1.r, rgb1.g, rgb1.b);
  const lum2 = getLuminance(rgb2.r, rgb2.g, rgb2.b);

  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);

  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Check if color contrast meets WCAG AA standard (4.5:1)
 *
 * @param foreground Foreground color (hex)
 * @param background Background color (hex)
 * @returns ColorContrast result
 */
export function checkColorContrast(
  foreground: string,
  background: string
): ColorContrast {
  const ratio = getContrastRatio(foreground, background);

  return {
    background,
    foreground,
    ratio: Math.round(ratio * 100) / 100,
    passes: ratio >= 4.5, // WCAG AA standard
  };
}

/**
 * Get accessible text color (black or white) for a background
 * Ensures WCAG AA contrast ratio
 *
 * @param backgroundColor Background color (hex)
 * @returns '#000000' or '#ffffff'
 */
export function getAccessibleTextColor(backgroundColor: string): string {
  const whiteContrast = getContrastRatio('#ffffff', backgroundColor);
  const blackContrast = getContrastRatio('#000000', backgroundColor);

  return whiteContrast > blackContrast ? '#ffffff' : '#000000';
}

/**
 * Screen reader announcement manager
 * Uses ARIA live region for dynamic announcements
 */
class ScreenReaderAnnouncer {
  private liveRegion: HTMLElement | null = null;

  /**
   * Initialize live region for announcements
   */
  private ensureLiveRegion(): HTMLElement {
    if (!this.liveRegion) {
      this.liveRegion = document.getElementById('a11y-announcer');

      if (!this.liveRegion) {
        this.liveRegion = document.createElement('div');
        this.liveRegion.id = 'a11y-announcer';
        this.liveRegion.setAttribute('role', 'status');
        this.liveRegion.setAttribute('aria-live', 'polite');
        this.liveRegion.setAttribute('aria-atomic', 'true');
        this.liveRegion.className = 'sr-only'; // Screen reader only (visually hidden)
        this.liveRegion.style.cssText = `
          position: absolute;
          left: -10000px;
          width: 1px;
          height: 1px;
          overflow: hidden;
        `;
        document.body.appendChild(this.liveRegion);
      }
    }

    return this.liveRegion;
  }

  /**
   * Announce message to screen readers
   *
   * @param announcement Announcement data
   */
  announce(announcement: A11yAnnouncement): void {
    const region = this.ensureLiveRegion();

    // Update aria-live priority
    region.setAttribute('aria-live', announcement.priority);

    // Clear previous announcement
    region.textContent = '';

    // Add new announcement (timeout ensures screen reader picks it up)
    setTimeout(() => {
      region.textContent = announcement.message;
    }, 100);
  }

  /**
   * Clear announcements
   */
  clear(): void {
    if (this.liveRegion) {
      this.liveRegion.textContent = '';
    }
  }
}

export const screenReaderAnnouncer = new ScreenReaderAnnouncer();

/**
 * Announce task creation to screen reader
 */
export function announceTaskCreated(task: Task): void {
  const start = new Date(task.start);
  const end = new Date(task.end);

  const message = `Task created: ${task.title}. Scheduled from ${start.toLocaleString()} to ${end.toLocaleString()}. Priority: ${task.priority}.`;

  screenReaderAnnouncer.announce({
    message,
    priority: 'polite',
    type: 'task-created',
  });
}

/**
 * Announce task update to screen reader
 */
export function announceTaskUpdated(task: Task): void {
  const start = new Date(task.start);
  const end = new Date(task.end);

  const message = `Task updated: ${task.title}. New schedule: ${start.toLocaleString()} to ${end.toLocaleString()}.`;

  screenReaderAnnouncer.announce({
    message,
    priority: 'polite',
    type: 'task-updated',
  });
}

/**
 * Announce task deletion to screen reader
 */
export function announceTaskDeleted(taskTitle: string): void {
  const message = `Task deleted: ${taskTitle}.`;

  screenReaderAnnouncer.announce({
    message,
    priority: 'assertive',
    type: 'task-deleted',
  });
}

/**
 * Announce calendar view change to screen reader
 */
export function announceViewChanged(view: string, date: Date): void {
  const dateStr = date.toLocaleDateString(undefined, {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const message = `Calendar view changed to ${view} view. Showing ${dateStr}.`;

  screenReaderAnnouncer.announce({
    message,
    priority: 'polite',
    type: 'view-changed',
  });
}

/**
 * Announce date navigation to screen reader
 */
export function announceDateChanged(date: Date, view: string): void {
  const dateStr = date.toLocaleDateString(undefined, {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const message = `Navigated to ${dateStr} in ${view} view.`;

  screenReaderAnnouncer.announce({
    message,
    priority: 'polite',
    type: 'date-changed',
  });
}

/**
 * Generate ARIA label for task event
 */
export function getTaskAriaLabel(task: Task): string {
  const start = new Date(task.start);
  const end = new Date(task.end);

  const startTime = start.toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
  });

  const endTime = end.toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit',
  });

  const parts = [
    task.title,
    `from ${startTime} to ${endTime}`,
    `priority: ${task.priority}`,
    `status: ${task.status}`,
  ];

  if (task.assignee) {
    parts.push(`assigned to: ${task.assignee}`);
  }

  return parts.join(', ');
}

/**
 * Generate ARIA label for calendar cell
 */
export function getCalendarCellAriaLabel(
  date: Date,
  tasks: Task[]
): string {
  const dateStr = date.toLocaleDateString(undefined, {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  });

  if (tasks.length === 0) {
    return `${dateStr}, no tasks scheduled`;
  }

  return `${dateStr}, ${tasks.length} task${tasks.length > 1 ? 's' : ''} scheduled`;
}

/**
 * Keyboard navigation helper
 * Maps keyboard events to calendar actions
 */
export const keyboardShortcuts = {
  // Navigation
  'ArrowLeft': 'prev-day',
  'ArrowRight': 'next-day',
  'ArrowUp': 'prev-week',
  'ArrowDown': 'next-week',
  'PageUp': 'prev-month',
  'PageDown': 'next-month',
  'Home': 'today',

  // Actions
  'Enter': 'select-event',
  ' ': 'select-event', // Space
  'n': 'create-event',
  'Delete': 'delete-event',
  'e': 'edit-event',
} as const;

/**
 * Check if element has visible focus indicator
 */
export function hasFocusIndicator(element: HTMLElement): boolean {
  const styles = window.getComputedStyle(element);

  // Check for outline
  if (styles.outlineWidth !== '0px' && styles.outlineStyle !== 'none') {
    return true;
  }

  // Check for box-shadow (alternative focus indicator)
  if (styles.boxShadow !== 'none') {
    return true;
  }

  // Check for border change
  if (styles.borderWidth !== '0px' && styles.borderStyle !== 'none') {
    return true;
  }

  return false;
}
