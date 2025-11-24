/**
 * Calendar View Switcher Component
 *
 * WCAG 2.1 AA Compliant:
 * - Keyboard navigation (Tab, Arrow keys, Enter/Space)
 * - ARIA labels for screen readers
 * - Color contrast 4.5:1 minimum
 * - Visible focus indicators
 * - Screen reader announcements for view changes
 */

import React from 'react';
import { announceViewChanged } from '../../utils/accessibility';

export type CalendarView = 'day' | 'week' | 'month';

export interface ViewSwitcherProps {
  currentView: CalendarView;
  currentDate: Date;
  onViewChange: (view: CalendarView) => void;
  className?: string;
  ariaLabel?: string;
}

const viewLabels: Record<CalendarView, string> = {
  day: 'Day View',
  week: 'Week View',
  month: 'Month View',
};

const viewIcons: Record<CalendarView, string> = {
  day: '📅',
  week: '📆',
  month: '🗓️',
};

/**
 * ViewSwitcher Component
 *
 * Accessible button group for switching calendar views
 */
export const ViewSwitcher: React.FC<ViewSwitcherProps> = ({
  currentView,
  currentDate,
  onViewChange,
  className = '',
  ariaLabel = 'Calendar view selector',
}) => {
  const views: CalendarView[] = ['day', 'week', 'month'];

  /**
   * Handle view change with screen reader announcement
   */
  const handleViewChange = (view: CalendarView) => {
    if (view !== currentView) {
      onViewChange(view);
      announceViewChanged(viewLabels[view], currentDate);
    }
  };

  /**
   * Handle keyboard navigation within button group
   */
  const handleKeyDown = (
    e: React.KeyboardEvent,
    view: CalendarView,
    index: number
  ) => {
    let newIndex = index;

    switch (e.key) {
      case 'ArrowLeft':
        e.preventDefault();
        newIndex = index > 0 ? index - 1 : views.length - 1;
        break;

      case 'ArrowRight':
        e.preventDefault();
        newIndex = index < views.length - 1 ? index + 1 : 0;
        break;

      case 'Home':
        e.preventDefault();
        newIndex = 0;
        break;

      case 'End':
        e.preventDefault();
        newIndex = views.length - 1;
        break;

      case 'Enter':
      case ' ': // Space
        e.preventDefault();
        handleViewChange(view);
        return;

      default:
        return;
    }

    // Focus the target button
    const buttons = e.currentTarget.parentElement?.querySelectorAll('button');
    if (buttons && buttons[newIndex]) {
      (buttons[newIndex] as HTMLButtonElement).focus();
    }
  };

  return (
    <div
      className={`inline-flex rounded-lg border border-gray-300 bg-white ${className}`}
      role="group"
      aria-label={ariaLabel}
    >
      {views.map((view, index) => {
        const isActive = view === currentView;
        const label = viewLabels[view];
        const icon = viewIcons[view];

        return (
          <button
            key={view}
            type="button"
            onClick={() => handleViewChange(view)}
            onKeyDown={(e) => handleKeyDown(e, view, index)}
            className={`
              px-4 py-2 text-sm font-medium transition-colors
              first:rounded-l-lg last:rounded-r-lg

              ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }

              ${!isActive && 'border-r border-gray-300 last:border-r-0'}

              /* WCAG Focus Indicator */
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
              focus:z-10

              /* High Contrast Mode Support */
              @media (prefers-contrast: high) {
                ${isActive ? 'border-2 border-blue-800' : 'border-2 border-gray-600'}
              }

              /* Disabled State */
              disabled:opacity-50 disabled:cursor-not-allowed
            `}
            aria-pressed={isActive}
            aria-label={`Switch to ${label.toLowerCase()}`}
            aria-current={isActive ? 'true' : undefined}
            tabIndex={isActive ? 0 : -1}
          >
            <span className="flex items-center gap-2" aria-hidden="true">
              <span className="text-base">{icon}</span>
              <span className="hidden sm:inline">{label}</span>
            </span>
            <span className="sr-only">
              {isActive ? `Current view: ${label}` : label}
            </span>
          </button>
        );
      })}
    </div>
  );
};

export default ViewSwitcher;
