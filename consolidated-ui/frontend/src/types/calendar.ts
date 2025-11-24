/**
 * Calendar Component Types
 *
 * TypeScript types for DayPilot calendar integration
 * and accessibility features
 */

import { Task } from '../store/tasksSlice';

/**
 * Calendar view modes
 */
export type CalendarView = 'day' | 'week' | 'month';

/**
 * DayPilot event format (maps to Task)
 */
export interface DayPilotEvent {
  id: string;
  text: string;
  start: string;
  end: string;
  backColor?: string;
  borderColor?: string;
  fontColor?: string;
  barColor?: string;
  barBackColor?: string;
  html?: string;
  cssClass?: string;
  data?: Task; // Original task data
}

/**
 * Calendar event for drag-and-drop
 */
export interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  task: Task;
}

/**
 * Drag-and-drop event data
 */
export interface DragEventData {
  taskId: string;
  newStart: Date;
  newEnd: Date;
  previousStart: Date;
  previousEnd: Date;
}

/**
 * Keyboard navigation actions
 */
export type KeyboardAction =
  | 'next-day'
  | 'prev-day'
  | 'next-week'
  | 'prev-week'
  | 'next-month'
  | 'prev-month'
  | 'today'
  | 'select-event'
  | 'create-event'
  | 'delete-event'
  | 'edit-event';

/**
 * Accessibility announcement types
 */
export interface A11yAnnouncement {
  message: string;
  priority: 'polite' | 'assertive';
  type: 'task-created' | 'task-updated' | 'task-deleted' | 'view-changed' | 'date-changed';
}

/**
 * WCAG color contrast requirements
 */
export interface ColorContrast {
  background: string;
  foreground: string;
  ratio: number;
  passes: boolean; // Must be >= 4.5:1 for AA
}

/**
 * Focus management state
 */
export interface FocusState {
  focusedDate: Date | null;
  focusedEventId: string | null;
  focusedElement: HTMLElement | null;
}

/**
 * Calendar configuration
 */
export interface CalendarConfig {
  view: CalendarView;
  startDate: Date;
  endDate: Date;
  businessHours: {
    start: number; // 0-23
    end: number;   // 0-23
  };
  weekStartsOn: 0 | 1 | 2 | 3 | 4 | 5 | 6; // 0 = Sunday, 1 = Monday
  timeFormat: '12h' | '24h';
  locale: string;
}

/**
 * View switcher props
 */
export interface ViewSwitcherProps {
  currentView: CalendarView;
  onViewChange: (view: CalendarView) => void;
  ariaLabel?: string;
}

/**
 * Calendar navigation props
 */
export interface CalendarNavigationProps {
  currentDate: Date;
  view: CalendarView;
  onNavigate: (date: Date) => void;
  onToday: () => void;
  ariaLabel?: string;
}

/**
 * Task modal props
 */
export interface TaskModalProps {
  isOpen: boolean;
  task?: Task;
  onClose: () => void;
  onSave: (task: Omit<Task, 'id'> | Task) => Promise<void>;
  onDelete?: (taskId: string) => Promise<void>;
}

/**
 * Accessibility features configuration
 */
export interface A11yConfig {
  enableKeyboardNav: boolean;
  enableScreenReaderAnnouncements: boolean;
  enableHighContrast: boolean;
  enableFocusIndicators: boolean;
  keyboardShortcuts: Map<string, KeyboardAction>;
}

// Re-export Task for other modules
export type { Task }