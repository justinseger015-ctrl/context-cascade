import React from 'react';
import {
  DndContext,
  closestCenter,
  DragOverlay,
  defaultDropAnimationSideEffects,
  DropAnimation,
} from '@dnd-kit/core';
import {
  SortableContext,
  verticalListSortingStrategy,
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { useDragAndDrop } from '../hooks/useDragAndDrop';
import type { Task } from '../types';

// Drop animation configuration
const dropAnimationConfig: DropAnimation = {
  sideEffects: defaultDropAnimationSideEffects({
    styles: {
      active: {
        opacity: '0.5',
      },
    },
  }),
};

interface DraggableTaskListProps {
  projectId: string;
  tasks: Task[];
  onReorder: (reorderedTasks: Task[]) => void;
  onReorderComplete?: (reorderedTasks: Task[]) => void;
  className?: string;
}

/**
 * Sortable task item with drag handle and accessibility features
 */
function SortableTaskItem({ task, isDragging }: { task: Task; isDragging: boolean }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({ id: task.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isSortableDragging ? 0.5 : 1,
  };

  // Priority color mapping
  const priorityColors = {
    low: 'bg-gray-100 border-gray-300',
    medium: 'bg-blue-50 border-blue-300',
    high: 'bg-yellow-50 border-yellow-400',
    critical: 'bg-red-50 border-red-400',
  };

  // Status badge colors
  const statusColors = {
    pending: 'bg-gray-500',
    running: 'bg-blue-500',
    completed: 'bg-green-500',
    failed: 'bg-red-500',
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`
        group relative flex items-center gap-3 p-4 mb-2 rounded-lg border-2
        ${priorityColors[task.priority]}
        ${isDragging ? 'shadow-lg ring-2 ring-blue-500' : 'hover:shadow-md'}
        transition-all duration-200
      `}
      // Accessibility attributes
      role="listitem"
      aria-label={`Task: ${task.title}, Priority: ${task.priority}, Status: ${task.status}`}
    >
      {/* Drag Handle - Visual indicator */}
      <div
        {...listeners}
        {...attributes}
        className="
          flex-shrink-0 cursor-grab active:cursor-grabbing
          p-2 rounded hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500
          transition-colors
        "
        role="button"
        aria-label={`Drag handle for task: ${task.title}`}
        tabIndex={0}
      >
        <svg
          className="w-5 h-5 text-gray-400 group-hover:text-gray-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 8h16M4 16h16"
          />
        </svg>
      </div>

      {/* Task Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <h3 className="font-semibold text-gray-900 truncate">{task.title}</h3>
          <span
            className={`
              px-2 py-1 text-xs font-medium text-white rounded-full
              ${statusColors[task.status]}
            `}
          >
            {task.status}
          </span>
        </div>
        <p className="text-sm text-gray-600 line-clamp-2">{task.description}</p>
        <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
          <span>Skill: {task.skill_name}</span>
          {task.schedule && <span>Schedule: {task.schedule}</span>}
          {task.next_run_at && (
            <span>Next run: {new Date(task.next_run_at).toLocaleString()}</span>
          )}
        </div>
      </div>

      {/* Drop Indicator - Shows where item will be dropped */}
      {isDragging && (
        <div
          className="
            absolute inset-0 border-2 border-dashed border-blue-500 rounded-lg
            bg-blue-50 bg-opacity-50 pointer-events-none
          "
          aria-hidden="true"
        />
      )}
    </div>
  );
}

/**
 * Draggable task list component with WCAG 2.1 AA accessibility
 *
 * Features:
 * - Sortable task list with drag handles
 * - Keyboard navigation (Space to grab, Arrow keys to move)
 * - Screen reader announcements
 * - Visual drop indicators
 * - Optimistic updates with Zustand
 * - Focus management
 */
export function DraggableTaskList({
  projectId,
  tasks,
  onReorder,
  onReorderComplete,
  className = '',
}: DraggableTaskListProps) {
  const {
    sensors,
    activeId,
    announcement,
    handleDragStart,
    handleDragOver,
    handleDragEnd,
    handleDragCancel,
  } = useDragAndDrop({
    tasks,
    onReorder,
    onReorderComplete,
  });

  // Sort tasks by order property
  const sortedTasks = [...tasks].sort((a, b) => (a.order || 0) - (b.order || 0));

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>No tasks yet. Create your first task to get started.</p>
      </div>
    );
  }

  return (
    <>
      {/* Screen reader announcements */}
      <div
        role="status"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
      >
        {announcement?.message}
      </div>

      {/* Instructions for keyboard users */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Keyboard navigation:</strong> Tab to drag handle, Space to grab, Arrow keys to move, Space to drop, Escape to cancel
        </p>
      </div>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragStart={handleDragStart}
        onDragOver={handleDragOver}
        onDragEnd={handleDragEnd}
        onDragCancel={handleDragCancel}
      >
        <SortableContext
          items={sortedTasks.map((task) => task.id)}
          strategy={verticalListSortingStrategy}
        >
          <div
            className={className}
            role="list"
            aria-label={`Sortable task list for project ${projectId}`}
          >
            {sortedTasks.map((task) => (
              <SortableTaskItem
                key={task.id}
                task={task}
                isDragging={task.id === activeId}
              />
            ))}
          </div>
        </SortableContext>

        {/* Drag overlay for smooth dragging experience */}
        <DragOverlay dropAnimation={dropAnimationConfig}>
          {activeId ? (
            <div className="opacity-90">
              <SortableTaskItem
                task={sortedTasks.find((t) => t.id === activeId)!}
                isDragging={true}
              />
            </div>
          ) : null}
        </DragOverlay>
      </DndContext>
    </>
  );
}
