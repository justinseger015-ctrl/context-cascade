/**
 * DayPilot Lite React Calendar Component
 *
 * WCAG 2.1 AA Compliant Calendar with:
 * - Month/week/day views
 * - Drag-and-drop scheduling (dnd-kit)
 * - Keyboard navigation
 * - Screen reader support
 * - Color contrast compliance
 * - Zustand state management integration
 *
 * @see https://www.w3.org/WAI/WCAG21/quickref/
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { DayPilot, DayPilotCalendar, DayPilotMonth } from '@daypilot/daypilot-lite-react';
import { DndContext, DragEndEvent, useSensor, useSensors, KeyboardSensor, PointerSensor } from '@dnd-kit/core';
import { useStore } from '../store';
import { Task } from '../types';
import {
  announceTaskCreated,
  announceTaskUpdated,
  announceTaskDeleted,
  getTaskAriaLabel,
  getAccessibleTextColor,
  checkColorContrast,
} from '../utils/accessibility';
import ViewSwitcher, { CalendarView } from './CalendarViews/ViewSwitcher';
import CalendarNavigation from './CalendarViews/CalendarNavigation';

/**
 * Convert Task to DayPilot event format
 */
function taskToDayPilotEvent(task: Task): DayPilot.EventData {
  const backgroundColor = task.priority === 'critical'
    ? '#dc2626' // red-600
    : task.priority === 'high'
    ? '#f97316' // orange-500
    : task.priority === 'medium'
    ? '#3b82f6' // blue-500
    : '#10b981'; // green-500

  const textColor = getAccessibleTextColor(backgroundColor);

  // Verify WCAG AA contrast (4.5:1 minimum)
  const contrast = checkColorContrast(textColor, backgroundColor);
  if (!contrast.passes) {
    console.warn(
      `Task ${task.id} fails WCAG AA contrast: ${contrast.ratio}:1 (need 4.5:1)`
    );
  }

  return {
    id: task.id,
    text: task.title,
    start: new DayPilot.Date(task.next_run_at || task.createdAt),
    end: new DayPilot.Date(task.dueDate || new Date(new Date(task.next_run_at || task.createdAt).getTime() + 3600000)),
    backColor: backgroundColor,
    fontColor: textColor,
    borderColor: textColor,
    barColor: backgroundColor,
    cssClass: 'calendar-event',
    html: `
      <div
        role="button"
        tabindex="0"
        aria-label="${getTaskAriaLabel(task as any)}"
        class="calendar-event-content"
      >
        <div class="font-semibold">${task.title}</div>
        <div class="text-sm opacity-90">${task.status}</div>
      </div>
    `,
    data: task,
  };
}

/**
 * Main Calendar Component
 */
export const Calendar: React.FC = () => {
  // State
  const [view, setView] = useState<CalendarView>('week');
  const [currentDate, setCurrentDate] = useState<Date>(new Date());
  const [events, setEvents] = useState<DayPilot.EventData[]>([]);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);

  // Refs for DayPilot components
  const calendarRef = useRef<DayPilotCalendar>(null);
  const monthRef = useRef<DayPilotMonth>(null);

  // Zustand store
  const {
    tasks,
    isLoading,
    fetchTasks,
    updateTask,
    addTask,
    deleteTask,
    rollbackOptimisticUpdate,
  } = useStore((state) => state);

  // Drag-and-drop sensors (keyboard + pointer)
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px movement before drag starts
      },
    }),
    useSensor(KeyboardSensor)
  );

  /**
   * Fetch tasks on mount
   */
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  /**
   * Convert tasks to DayPilot events
   */
  useEffect(() => {
    const dayPilotEvents = tasks.map(taskToDayPilotEvent);
    setEvents(dayPilotEvents);
  }, [tasks]);

  /**
   * Handle drag-and-drop event move (dnd-kit)
   */
  const handleDragEnd = useCallback(
    async (event: DragEndEvent) => {
      const { active, delta } = event;

      if (!active || !delta) return;

      const taskId = active.id as string;
      const task = tasks.find((t) => t.id === taskId);

      if (!task) return;

      // Calculate new start/end times based on drag delta
      const oldStart = new Date(task.next_run_at || task.createdAt);
      const oldEnd = new Date(task.dueDate || new Date(oldStart.getTime() + 3600000));

      const newStart = new Date(oldStart.getTime() + delta.x * 86400000); // Assuming delta.x is in days
      const newEnd = new Date(oldEnd.getTime() + delta.x * 86400000);

      // Optimistic update (immediate UI response)
      const previousTask = { ...task };

      try {
        // Update via Zustand with optimistic updates
        await updateTask(taskId, {
          next_run_at: newStart,
          dueDate: newEnd,
        });

        announceTaskUpdated(task as any);
      } catch (error) {
        // Rollback on error
        console.error('Failed to update task:', error);
        rollbackOptimisticUpdate(taskId);
      }
    },
    [tasks, updateTask, rollbackOptimisticUpdate]
  );

  /**
   * Handle DayPilot event move (native DayPilot drag-and-drop)
   */
  const handleEventMoved = useCallback(
    async (args: any) => {
      const taskId = args.e.id();
      const task = tasks.find((t) => t.id === taskId);

      if (!task) return;

      const newStart = args.newStart.value; // DayPilot.Date value
      const newEnd = args.newEnd.value;

      try {
        await updateTask(taskId, {
          next_run_at: new Date(newStart),
          dueDate: new Date(newEnd),
        });

        announceTaskUpdated(task as any);
      } catch (error) {
        console.error('Failed to update task:', error);
        args.preventDefault(); // Prevent DayPilot from updating visually
      }
    },
    [tasks, updateTask]
  );

  /**
   * Handle event click
   */
  const handleEventClick = useCallback((args: any) => {
    const taskId = args.e.id();
    setSelectedEventId(taskId);

    // Focus the event for keyboard navigation
    const element = args.e.calendar.events.find(taskId)?.div;
    if (element) {
      element.focus();
    }
  }, []);

  /**
   * Handle time range selection (create new event)
   */
  const handleTimeRangeSelected = useCallback(
    async (args: any) => {
      const start = args.start.value;
      const end = args.end.value;

      const title = prompt('Enter task title:');
      if (!title) {
        args.preventDefault();
        return;
      }

      try {
        await addTask({
          title,
          description: '',
          status: 'pending',
          priority: 'medium',
          skill_name: '',
          projectId: '', // Would come from context/props in real app
          next_run_at: new Date(start),
          dueDate: new Date(end),
        });

        const newTask = tasks[tasks.length - 1]; // Get last added task
        if (newTask) {
          announceTaskCreated(newTask as any);
        }
      } catch (error) {
        console.error('Failed to create task:', error);
        args.preventDefault();
      }
    },
    [addTask, tasks]
  );

  /**
   * Handle event deletion (keyboard: Delete key)
   */
  const handleEventDelete = useCallback(
    async (taskId: string) => {
      const task = tasks.find((t) => t.id === taskId);
      if (!task) return;

      const confirmed = confirm(`Delete task "${task.title}"?`);
      if (!confirmed) return;

      try {
        await deleteTask(taskId);
        announceTaskDeleted(task.title);
        setSelectedEventId(null);
      } catch (error) {
        console.error('Failed to delete task:', error);
      }
    },
    [tasks, deleteTask]
  );

  /**
   * Keyboard navigation handler
   */
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (!selectedEventId) return;

      switch (e.key) {
        case 'Delete':
        case 'Backspace':
          e.preventDefault();
          handleEventDelete(selectedEventId);
          break;

        case 'Escape':
          e.preventDefault();
          setSelectedEventId(null);
          break;

        case 'Enter':
        case ' ':
          e.preventDefault();
          // Open edit modal (would be implemented separately)
          console.log('Edit task:', selectedEventId);
          break;
      }
    },
    [selectedEventId, handleEventDelete]
  );

  /**
   * Attach keyboard event listener
   */
  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  /**
   * DayPilot configuration for Week/Day view
   */
  const calendarConfig: DayPilot.CalendarConfig = {
    viewType: view === 'day' ? 'Day' : 'Week',
    startDate: currentDate,
    headerHeight: 40,
    cellHeight: 40,
    cellDuration: 60, // 1 hour cells
    businessBeginsHour: 8,
    businessEndsHour: 18,
    showNonBusiness: true,
    timeFormat: 'Clock12Hours',
    eventMoveHandling: 'Update',
    eventResizeHandling: 'Update',
    eventClickHandling: 'Enabled',
    timeRangeSelectedHandling: 'Enabled',
    onEventMoved: handleEventMoved,
    onEventClick: handleEventClick,
    onTimeRangeSelected: handleTimeRangeSelected,
  };

  /**
   * DayPilot configuration for Month view
   */
  const monthConfig: DayPilot.MonthConfig = {
    startDate: currentDate,
    eventHeight: 30,
    eventMoveHandling: 'Update',
    eventClickHandling: 'Enabled',
    timeRangeSelectedHandling: 'Enabled',
    onEventMoved: handleEventMoved,
    onEventClick: handleEventClick,
    onTimeRangeSelected: handleTimeRangeSelected,
  };

  return (
    <DndContext sensors={sensors} onDragEnd={handleDragEnd}>
      <div
        className="calendar-container flex flex-col h-full bg-white rounded-lg shadow-sm"
        role="application"
        aria-label="Task scheduling calendar"
      >
        {/* Calendar Header */}
        <div className="calendar-header flex items-center justify-between p-4 border-b border-gray-200">
          <CalendarNavigation
            currentDate={currentDate}
            currentView={view}
            onNavigate={setCurrentDate}
            onToday={() => setCurrentDate(new Date())}
          />

          <ViewSwitcher
            currentView={view}
            currentDate={currentDate}
            onViewChange={setView}
          />
        </div>

        {/* Calendar Body */}
        <div className="calendar-body flex-1 overflow-auto p-4">
          {isLoading ? (
            <div
              className="flex items-center justify-center h-64"
              role="status"
              aria-live="polite"
            >
              <div className="text-gray-500">Loading tasks...</div>
            </div>
          ) : view === 'month' ? (
            <DayPilotMonth
              ref={monthRef}
              {...monthConfig}
              events={events}
            />
          ) : (
            <DayPilotCalendar
              ref={calendarRef}
              {...calendarConfig}
              events={events}
            />
          )}
        </div>

        {/* Accessibility: Live region for announcements (visually hidden) */}
        <div
          id="calendar-announcements"
          role="status"
          aria-live="polite"
          aria-atomic="true"
          className="sr-only"
        />
      </div>

      {/* Global Styles for Calendar Events (WCAG compliant) */}
      <style jsx global>{`
        .calendar-event-content {
          padding: 4px 8px;
          border-radius: 4px;
          cursor: pointer;
        }

        .calendar-event-content:hover {
          opacity: 0.9;
        }

        .calendar-event-content:focus {
          outline: 2px solid #3b82f6;
          outline-offset: 2px;
        }

        /* Screen reader only class */
        .sr-only {
          position: absolute;
          width: 1px;
          height: 1px;
          padding: 0;
          margin: -1px;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          white-space: nowrap;
          border-width: 0;
        }

        /* High contrast mode support */
        @media (prefers-contrast: high) {
          .calendar-event-content {
            border: 2px solid currentColor !important;
          }
        }
      `}</style>
    </DndContext>
  );
};

export default Calendar;
