/**
 * Task Status Color Mapping
 * Provides consistent color theming for task statuses across UI components
 *
 * P4_T3: Real-time status updates trigger color changes
 * - Calendar: Task color updates on status change
 * - Project Dashboard: Status badge color changes
 * - Agent Monitor: Task execution color indicators
 */

import { TaskStatus } from '../types';

/**
 * Status color map for UI components
 * Maps task status to Tailwind CSS color classes
 */
export const TASK_STATUS_COLORS: Record<
  TaskStatus,
  {
    bg: string;
    border: string;
    text: string;
    badge: string;
    hover: string;
  }
> = {
  pending: {
    bg: 'bg-blue-50',
    border: 'border-blue-300',
    text: 'text-blue-700',
    badge: 'bg-blue-100 text-blue-800',
    hover: 'hover:bg-blue-100',
  },
  running: {
    bg: 'bg-yellow-50',
    border: 'border-yellow-300',
    text: 'text-yellow-700',
    badge: 'bg-yellow-100 text-yellow-800',
    hover: 'hover:bg-yellow-100',
  },
  completed: {
    bg: 'bg-green-50',
    border: 'border-green-300',
    text: 'text-green-700',
    badge: 'bg-green-100 text-green-800',
    hover: 'hover:bg-green-100',
  },
  failed: {
    bg: 'bg-red-50',
    border: 'border-red-300',
    text: 'text-red-700',
    badge: 'bg-red-100 text-red-800',
    hover: 'hover:bg-red-100',
  },
};

/**
 * Get status color classes for a task
 * @param status Task status
 * @returns Object with Tailwind CSS color classes
 */
export function getTaskStatusColors(status: TaskStatus) {
  return TASK_STATUS_COLORS[status] || TASK_STATUS_COLORS.pending;
}

/**
 * Get calendar event color based on task status
 * @param status Task status
 * @returns Hex color code for calendar event
 */
export function getCalendarEventColor(status: TaskStatus): string {
  const colorMap: Record<TaskStatus, string> = {
    pending: '#3B82F6', // Blue
    running: '#F59E0B', // Yellow/Amber
    completed: '#10B981', // Green
    failed: '#EF4444', // Red
  };

  return colorMap[status] || colorMap.pending;
}

/**
 * Get status badge text
 * @param status Task status
 * @returns Human-readable status text
 */
export function getStatusBadgeText(status: TaskStatus): string {
  const textMap: Record<TaskStatus, string> = {
    pending: 'Pending',
    running: 'Running',
    completed: 'Completed',
    failed: 'Failed',
  };

  return textMap[status] || 'Unknown';
}

/**
 * Get status icon name (for icon libraries like Heroicons)
 * @param status Task status
 * @returns Icon name
 */
export function getStatusIcon(status: TaskStatus): string {
  const iconMap: Record<TaskStatus, string> = {
    pending: 'ClockIcon',
    running: 'PlayIcon',
    completed: 'CheckCircleIcon',
    failed: 'XCircleIcon',
  };

  return iconMap[status] || 'QuestionMarkCircleIcon';
}
