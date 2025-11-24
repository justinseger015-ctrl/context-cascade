import React, { useMemo } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { TaskItem } from './TaskItem';
import type { Task, TaskFilters, TaskSort } from '../types';

interface TaskListProps {
  tasks: Task[];
  filters: TaskFilters;
  sort: TaskSort;
  onReorder: (tasks: Task[]) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onRunNow: (taskId: string) => void;
  onSortChange: (sort: TaskSort) => void;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  filters,
  sort,
  onReorder,
  onEdit,
  onDelete,
  onRunNow,
  onSortChange,
}) => {
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px movement required to start drag
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Filter and sort tasks
  const filteredAndSortedTasks = useMemo(() => {
    let result = [...tasks];

    // Apply filters
    if (filters.status && filters.status.length > 0) {
      result = result.filter((task) => filters.status!.includes(task.status));
    }

    if (filters.skill_name && filters.skill_name.length > 0) {
      result = result.filter((task) => filters.skill_name!.includes(task.skill_name));
    }

    // Apply sorting
    result.sort((a, b) => {
      let comparison = 0;

      switch (sort.field) {
        case 'createdAt':
          comparison = new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
          break;
        case 'next_run_at':
          const aTime = a.next_run_at ? new Date(a.next_run_at).getTime() : 0;
          const bTime = b.next_run_at ? new Date(b.next_run_at).getTime() : 0;
          comparison = aTime - bTime;
          break;
        case 'status':
          const statusOrder = { pending: 0, running: 1, completed: 2, failed: 3 };
          comparison = statusOrder[a.status] - statusOrder[b.status];
          break;
      }

      return sort.direction === 'asc' ? comparison : -comparison;
    });

    return result;
  }, [tasks, filters, sort]);

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const oldIndex = filteredAndSortedTasks.findIndex((task) => task.id === active.id);
      const newIndex = filteredAndSortedTasks.findIndex((task) => task.id === over.id);

      const reorderedTasks = arrayMove(filteredAndSortedTasks, oldIndex, newIndex);
      onReorder(reorderedTasks);
    }
  };

  const toggleSortDirection = () => {
    onSortChange({
      ...sort,
      direction: sort.direction === 'asc' ? 'desc' : 'asc',
    });
  };

  const changeSortField = (field: TaskSort['field']) => {
    onSortChange({
      field,
      direction: sort.field === field && sort.direction === 'desc' ? 'asc' : 'desc',
    });
  };

  if (tasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <div className="text-gray-400 mb-2">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
        <p className="text-gray-600">Create your first task to get started</p>
      </div>
    );
  }

  if (filteredAndSortedTasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <div className="text-gray-400 mb-2">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks match filters</h3>
        <p className="text-gray-600">Try adjusting your filters</p>
      </div>
    );
  }

  return (
    <div>
      {/* Sort Controls */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-700">Sort by:</span>
          <div className="flex gap-2">
            {[
              { field: 'createdAt' as const, label: 'Created' },
              { field: 'next_run_at' as const, label: 'Next Run' },
              { field: 'status' as const, label: 'Status' },
            ].map(({ field, label }) => (
              <button
                key={field}
                onClick={() => changeSortField(field)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  sort.field === field
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={toggleSortDirection}
          className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          title={`Sort ${sort.direction === 'asc' ? 'descending' : 'ascending'}`}
        >
          <svg
            className={`w-5 h-5 transition-transform ${sort.direction === 'desc' ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"
            />
          </svg>
        </button>
      </div>

      {/* Task List with Drag and Drop */}
      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={filteredAndSortedTasks.map((t) => t.id)} strategy={verticalListSortingStrategy}>
          {filteredAndSortedTasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onEdit={onEdit}
              onDelete={onDelete}
              onRunNow={onRunNow}
            />
          ))}
        </SortableContext>
      </DndContext>
    </div>
  );
};
