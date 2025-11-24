import { useState, useCallback, useRef } from 'react';
import {
  DragEndEvent,
  DragStartEvent,
  DragOverEvent,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragCancelEvent,
} from '@dnd-kit/core';
import { arrayMove } from '@dnd-kit/sortable';
import type { Task } from '../types';

interface UseDragAndDropOptions {
  tasks: Task[];
  onReorder: (reorderedTasks: Task[]) => void;
  onReorderComplete?: (reorderedTasks: Task[]) => void;
}

interface DragAnnouncement {
  message: string;
  timestamp: number;
}

/**
 * Custom hook for drag-and-drop functionality with WCAG 2.1 AA compliance
 *
 * Features:
 * - Keyboard support (Space to grab, Arrow keys to move, Space to drop)
 * - Screen reader announcements for all drag events
 * - Focus management during drag operations
 * - Optimistic UI updates with rollback on error
 */
export function useDragAndDrop({ tasks, onReorder, onReorderComplete }: UseDragAndDropOptions) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const [announcement, setAnnouncement] = useState<DragAnnouncement | null>(null);
  const previousTasksRef = useRef<Task[]>(tasks);

  // Configure sensors for both pointer and keyboard interactions
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px threshold to prevent accidental drags
      },
    }),
    useSensor(KeyboardSensor, {
      // Custom keyboard coordination for WCAG compliance
      coordinateGetter: (event, { currentCoordinates, context }) => {
        const { active, over } = context;

        if (!active || !over) return currentCoordinates;

        // Space key activates/deactivates drag
        if (event.code === 'Space') {
          return currentCoordinates;
        }

        // Arrow keys move the item
        const delta = { x: 0, y: 0 };

        switch (event.code) {
          case 'ArrowUp':
            delta.y = -20;
            break;
          case 'ArrowDown':
            delta.y = 20;
            break;
          case 'ArrowLeft':
            delta.x = -20;
            break;
          case 'ArrowRight':
            delta.x = 20;
            break;
        }

        return {
          x: currentCoordinates.x + delta.x,
          y: currentCoordinates.y + delta.y,
        };
      },
    })
  );

  /**
   * Announce message to screen readers
   */
  const announce = useCallback((message: string) => {
    setAnnouncement({ message, timestamp: Date.now() });
    // Clear announcement after 3 seconds to prevent stale messages
    setTimeout(() => setAnnouncement(null), 3000);
  }, []);

  /**
   * Get task title by ID for announcements
   */
  const getTaskTitle = useCallback(
    (id: string) => {
      const task = tasks.find((t) => t.id === id);
      return task?.title || 'Unknown task';
    },
    [tasks]
  );

  /**
   * Handle drag start event
   */
  const handleDragStart = useCallback(
    (event: DragStartEvent) => {
      const { active } = event;
      setActiveId(active.id as string);
      previousTasksRef.current = tasks; // Store for potential rollback

      const taskTitle = getTaskTitle(active.id as string);
      announce(`Picked up task: ${taskTitle}. Use arrow keys to move, Space to drop, Escape to cancel.`);
    },
    [tasks, getTaskTitle, announce]
  );

  /**
   * Handle drag over event for visual feedback
   */
  const handleDragOver = useCallback(
    (event: DragOverEvent) => {
      const { active, over } = event;

      if (!over || active.id === over.id) return;

      const activeTask = getTaskTitle(active.id as string);
      const overTask = getTaskTitle(over.id as string);

      // Announce position change to screen reader
      announce(`Moving ${activeTask} over ${overTask}`);
    },
    [getTaskTitle, announce]
  );

  /**
   * Handle drag end event - reorder tasks
   */
  const handleDragEnd = useCallback(
    (event: DragEndEvent) => {
      const { active, over } = event;
      setActiveId(null);

      if (!over || active.id === over.id) {
        announce('Task returned to original position');
        return;
      }

      const oldIndex = tasks.findIndex((task) => task.id === active.id);
      const newIndex = tasks.findIndex((task) => task.id === over.id);

      if (oldIndex === -1 || newIndex === -1) return;

      // Optimistic update
      const reorderedTasks = arrayMove(tasks, oldIndex, newIndex);
      onReorder(reorderedTasks);

      const taskTitle = getTaskTitle(active.id as string);
      const position = newIndex + 1;
      const total = tasks.length;
      announce(`Dropped ${taskTitle} at position ${position} of ${total}`);

      // Call completion handler if provided (for API persistence)
      if (onReorderComplete) {
        try {
          onReorderComplete(reorderedTasks);
        } catch (error) {
          // Rollback on error
          onReorder(previousTasksRef.current);
          announce(`Failed to reorder task: ${taskTitle}. Changes reverted.`);
          console.error('Error persisting task order:', error);
        }
      }
    },
    [tasks, onReorder, onReorderComplete, getTaskTitle, announce]
  );

  /**
   * Handle drag cancel event
   */
  const handleDragCancel = useCallback(
    (event: DragCancelEvent) => {
      setActiveId(null);

      if (event.active) {
        const taskTitle = getTaskTitle(event.active.id as string);
        announce(`Cancelled dragging ${taskTitle}. Returned to original position.`);
      }
    },
    [getTaskTitle, announce]
  );

  return {
    sensors,
    activeId,
    announcement,
    handleDragStart,
    handleDragOver,
    handleDragEnd,
    handleDragCancel,
  };
}
