/**
 * Calendar Navigation Component
 *
 * WCAG 2.1 AA Compliant:
 * - Keyboard navigation
 * - ARIA labels
 * - Screen reader announcements
 * - Color contrast 4.5:1
 */

import React from 'react';
import { announceDateChanged } from '../../utils/accessibility';
import type { CalendarView } from './ViewSwitcher';

export interface CalendarNavigationProps {
  currentDate: Date;
  currentView: CalendarView;
  onNavigate: (date: Date) => void;
  onToday: () => void;
  className?: string;
}

/**
 * CalendarNavigation Component
 *
 * Navigation controls for calendar date selection
 */
export const CalendarNavigation: React.FC<CalendarNavigationProps> = ({
  currentDate,
  currentView,
  onNavigate,
  onToday,
  className = '',
}) => {
  /**
   * Navigate to previous period (day/week/month)
   */
  const handlePrevious = () => {
    const newDate = new Date(currentDate);

    switch (currentView) {
      case 'day':
        newDate.setDate(newDate.getDate() - 1);
        break;
      case 'week':
        newDate.setDate(newDate.getDate() - 7);
        break;
      case 'month':
        newDate.setMonth(newDate.getMonth() - 1);
        break;
    }

    onNavigate(newDate);
    announceDateChanged(newDate, currentView);
  };

  /**
   * Navigate to next period (day/week/month)
   */
  const handleNext = () => {
    const newDate = new Date(currentDate);

    switch (currentView) {
      case 'day':
        newDate.setDate(newDate.getDate() + 1);
        break;
      case 'week':
        newDate.setDate(newDate.getDate() + 7);
        break;
      case 'month':
        newDate.setMonth(newDate.getMonth() + 1);
        break;
    }

    onNavigate(newDate);
    announceDateChanged(newDate, currentView);
  };

  /**
   * Navigate to today
   */
  const handleToday = () => {
    const today = new Date();
    onNavigate(today);
    announceDateChanged(today, currentView);
  };

  /**
   * Format date based on current view
   */
  const formatDate = (): string => {
    const options: Intl.DateTimeFormatOptions = {};

    switch (currentView) {
      case 'day':
        return currentDate.toLocaleDateString(undefined, {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        });

      case 'week': {
        const startOfWeek = new Date(currentDate);
        startOfWeek.setDate(currentDate.getDate() - currentDate.getDay());

        const endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 6);

        return `${startOfWeek.toLocaleDateString(undefined, {
          month: 'short',
          day: 'numeric',
        })} - ${endOfWeek.toLocaleDateString(undefined, {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
        })}`;
      }

      case 'month':
        return currentDate.toLocaleDateString(undefined, {
          year: 'numeric',
          month: 'long',
        });

      default:
        return currentDate.toLocaleDateString();
    }
  };

  const isToday = (): boolean => {
    const today = new Date();
    return (
      currentDate.getDate() === today.getDate() &&
      currentDate.getMonth() === today.getMonth() &&
      currentDate.getFullYear() === today.getFullYear()
    );
  };

  return (
    <nav
      className={`flex items-center justify-between gap-4 ${className}`}
      aria-label="Calendar navigation"
    >
      {/* Previous Button */}
      <button
        type="button"
        onClick={handlePrevious}
        className="
          inline-flex items-center justify-center
          px-3 py-2 rounded-lg
          bg-white border border-gray-300
          text-gray-700 hover:bg-gray-50
          transition-colors

          /* WCAG Focus Indicator */
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
        "
        aria-label={`Previous ${currentView}`}
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
        <span className="sr-only">Previous {currentView}</span>
      </button>

      {/* Current Date Display */}
      <div className="flex items-center gap-2">
        <h2
          className="text-lg font-semibold text-gray-900"
          aria-live="polite"
          aria-atomic="true"
        >
          {formatDate()}
        </h2>

        {/* Today Button */}
        {!isToday() && (
          <button
            type="button"
            onClick={handleToday}
            className="
              px-3 py-1.5 rounded-md text-sm font-medium
              bg-blue-600 text-white hover:bg-blue-700
              transition-colors

              /* WCAG Focus Indicator */
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
            "
            aria-label="Go to today"
          >
            Today
          </button>
        )}
      </div>

      {/* Next Button */}
      <button
        type="button"
        onClick={handleNext}
        className="
          inline-flex items-center justify-center
          px-3 py-2 rounded-lg
          bg-white border border-gray-300
          text-gray-700 hover:bg-gray-50
          transition-colors

          /* WCAG Focus Indicator */
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
        "
        aria-label={`Next ${currentView}`}
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
        <span className="sr-only">Next {currentView}</span>
      </button>
    </nav>
  );
};

export default CalendarNavigation;
