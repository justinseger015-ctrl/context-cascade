import { render, screen, fireEvent } from '@testing-library/react';
import { DndContext } from '@dnd-kit/core';
import { TaskItem } from './TaskItem';
import type { Task } from '../types';

// Mock useSortable
jest.mock('@dnd-kit/sortable', () => ({
  useSortable: () => ({
    attributes: {},
    listeners: {},
    setNodeRef: jest.fn(),
    transform: null,
    transition: null,
    isDragging: false,
  }),
}));

describe('TaskItem', () => {
  const mockTask: Task = {
    id: 'task-1',
    projectId: 'project-1',
    title: 'Test Task',
    description: 'Test description',
    status: 'pending',
    priority: 'high',
    skill_name: 'react-developer',
    schedule: '0 0 * * *',
    next_run_at: new Date('2025-01-15T10:00:00Z'),
    createdAt: new Date('2025-01-01T00:00:00Z'),
    updatedAt: new Date('2025-01-01T00:00:00Z'),
  };

  const mockHandlers = {
    onEdit: jest.fn(),
    onDelete: jest.fn(),
    onRunNow: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  const renderWithDnd = (task: Task) => {
    return render(
      <DndContext>
        <TaskItem task={task} {...mockHandlers} />
      </DndContext>
    );
  };

  it('renders task information', () => {
    renderWithDnd(mockTask);

    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test description')).toBeInTheDocument();
    expect(screen.getByText('react-developer')).toBeInTheDocument();
    expect(screen.getByText('0 0 * * *')).toBeInTheDocument();
  });

  it('displays correct status icon and styling', () => {
    renderWithDnd(mockTask);

    const container = screen.getByText('Test Task').closest('div')?.parentElement;
    expect(container).toHaveClass('bg-gray-100', 'text-gray-800', 'border-gray-300');
  });

  it('shows Run Now button for non-running tasks', () => {
    renderWithDnd(mockTask);

    const runButton = screen.getByTitle('Run now');
    expect(runButton).toBeInTheDocument();
  });

  it('hides Run Now button for running tasks', () => {
    const runningTask = { ...mockTask, status: 'running' as const };
    renderWithDnd(runningTask);

    expect(screen.queryByTitle('Run now')).not.toBeInTheDocument();
  });

  it('calls onEdit when edit button clicked', () => {
    renderWithDnd(mockTask);

    fireEvent.click(screen.getByTitle('Edit'));

    expect(mockHandlers.onEdit).toHaveBeenCalledWith(mockTask);
  });

  it('calls onRunNow when run button clicked', () => {
    renderWithDnd(mockTask);

    fireEvent.click(screen.getByTitle('Run now'));

    expect(mockHandlers.onRunNow).toHaveBeenCalledWith('task-1');
  });

  it('shows confirmation before deleting', () => {
    global.confirm = jest.fn(() => true);
    renderWithDnd(mockTask);

    fireEvent.click(screen.getByTitle('Delete'));

    expect(global.confirm).toHaveBeenCalledWith('Delete task "Test Task"?');
    expect(mockHandlers.onDelete).toHaveBeenCalledWith('task-1');
  });

  it('does not delete if confirmation cancelled', () => {
    global.confirm = jest.fn(() => false);
    renderWithDnd(mockTask);

    fireEvent.click(screen.getByTitle('Delete'));

    expect(mockHandlers.onDelete).not.toHaveBeenCalled();
  });

  it('displays last run time if available', () => {
    const taskWithLastRun = {
      ...mockTask,
      last_run_at: new Date('2025-01-10T12:00:00Z'),
    };
    renderWithDnd(taskWithLastRun);

    expect(screen.getByText(/Last run:/)).toBeInTheDocument();
  });

  it('formats dates correctly', () => {
    renderWithDnd(mockTask);

    // Check that a date is displayed (format may vary by locale)
    expect(screen.getByText(/Jan|15/)).toBeInTheDocument();
  });

  it('applies different colors for different statuses', () => {
    const statuses: Array<Task['status']> = ['pending', 'running', 'completed', 'failed'];
    const colors = ['bg-gray-100', 'bg-blue-100', 'bg-green-100', 'bg-red-100'];

    statuses.forEach((status, index) => {
      const { container } = renderWithDnd({ ...mockTask, status });
      const taskElement = container.querySelector('.bg-white');

      if (taskElement) {
        expect(taskElement).toHaveClass(colors[index]);
      }
    });
  });
});
