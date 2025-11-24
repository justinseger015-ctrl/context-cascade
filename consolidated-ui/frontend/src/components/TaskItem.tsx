import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { Task } from '../types';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onRunNow: (taskId: string) => void;
}

const statusColors = {
  pending: 'bg-gray-100 text-gray-800 border-gray-300',
  running: 'bg-blue-100 text-blue-800 border-blue-300',
  completed: 'bg-green-100 text-green-800 border-green-300',
  failed: 'bg-red-100 text-red-800 border-red-300',
};

const statusIcons = {
  pending: '⏸️',
  running: '▶️',
  completed: '✅',
  failed: '❌',
};

export const TaskItem: React.FC<TaskItemProps> = ({ task, onEdit, onDelete, onRunNow }) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: task.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const formatDate = (date?: Date) => {
    if (!date) return 'Not scheduled';
    const d = new Date(date);
    return d.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    onEdit(task);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm(`Delete task "${task.title}"?`)) {
      onDelete(task.id);
    }
  };

  const handleRunNow = (e: React.MouseEvent) => {
    e.stopPropagation();
    onRunNow(task.id);
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={`bg-white rounded-lg border-2 p-4 mb-3 transition-all hover:shadow-md ${
        statusColors[task.status]
      } ${isDragging ? 'shadow-xl' : ''}`}
    >
      <div className="flex items-start justify-between">
        {/* Drag Handle */}
        <div
          {...attributes}
          {...listeners}
          className="cursor-move mr-3 text-gray-400 hover:text-gray-600 mt-1"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M7 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 2zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 8zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 14zm6-8a2 2 0 1 0-.001-4.001A2 2 0 0 0 13 6zm0 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 8zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 14z" />
          </svg>
        </div>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-lg">{statusIcons[task.status]}</span>
            <h4 className="text-lg font-semibold text-gray-900 truncate">{task.title}</h4>
          </div>

          <p className="text-sm text-gray-600 mb-2 line-clamp-2">{task.description}</p>

          <div className="flex flex-wrap gap-2 text-sm text-gray-600">
            <span className="inline-flex items-center px-2 py-1 rounded bg-purple-100 text-purple-800 font-medium">
              {task.skill_name}
            </span>
            {task.schedule && (
              <span className="inline-flex items-center gap-1">
                <span>📅</span>
                <span>{task.schedule}</span>
              </span>
            )}
            <span className="inline-flex items-center gap-1">
              <span>⏰</span>
              <span>{formatDate(task.next_run_at)}</span>
            </span>
          </div>

          {task.last_run_at && (
            <div className="mt-2 text-xs text-gray-500">
              Last run: {formatDate(task.last_run_at)}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2 ml-4">
          {task.status !== 'running' && (
            <button
              onClick={handleRunNow}
              className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              title="Run now"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </button>
          )}

          <button
            onClick={handleEdit}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            title="Edit"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>

          <button
            onClick={handleDelete}
            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Delete"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};
