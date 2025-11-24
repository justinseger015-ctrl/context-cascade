import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { DraggableTaskList } from './DraggableTaskList';
import type { Task } from '../types';
import type { useDragAndDrop as UseDragAndDropType } from '../hooks/useDragAndDrop';

// Mock useDragAndDrop hook
jest.mock('../hooks/useDragAndDrop', () => ({
  useDragAndDrop: jest.fn(() => ({
    sensors: [],
    activeId: null,
    announcement: null,
    handleDragStart: jest.fn(),
    handleDragOver: jest.fn(),
    handleDragEnd: jest.fn(),
    handleDragCancel: jest.fn(),
  })),
}));

describe('DraggableTaskList', () => {
  const mockTasks: Task[] = [
    {
      id: 'task-1',
      projectId: 'project-1',
      title: 'First Task',
      description: 'Description for first task',
      status: 'pending',
      priority: 'high',
      skill_name: 'code-review',
      order: 0,
      createdAt: new Date('2025-01-01'),
      updatedAt: new Date('2025-01-01'),
    },
    {
      id: 'task-2',
      projectId: 'project-1',
      title: 'Second Task',
      description: 'Description for second task',
      status: 'running',
      priority: 'medium',
      skill_name: 'testing',
      order: 1,
      createdAt: new Date('2025-01-02'),
      updatedAt: new Date('2025-01-02'),
    },
    {
      id: 'task-3',
      projectId: 'project-1',
      title: 'Third Task',
      description: 'Description for third task',
      status: 'completed',
      priority: 'low',
      skill_name: 'deployment',
      order: 2,
      createdAt: new Date('2025-01-03'),
      updatedAt: new Date('2025-01-03'),
    },
  ];

  const mockOnReorder = jest.fn();
  const mockOnReorderComplete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('renders empty state when no tasks provided', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={[]}
          onReorder={mockOnReorder}
        />
      );

      expect(screen.getByText(/No tasks yet/i)).toBeInTheDocument();
    });

    it('renders all tasks in correct order', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      expect(screen.getByText('First Task')).toBeInTheDocument();
      expect(screen.getByText('Second Task')).toBeInTheDocument();
      expect(screen.getByText('Third Task')).toBeInTheDocument();
    });

    it('displays task details correctly', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const firstTask = screen.getByText('First Task');
      expect(firstTask).toBeInTheDocument();
      expect(screen.getByText('Description for first task')).toBeInTheDocument();
      expect(screen.getByText('Skill: code-review')).toBeInTheDocument();
      expect(screen.getByText('pending')).toBeInTheDocument();
    });

    it('renders keyboard navigation instructions', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      expect(screen.getByText(/Keyboard navigation/i)).toBeInTheDocument();
      expect(screen.getByText(/Space to grab/i)).toBeInTheDocument();
      expect(screen.getByText(/Arrow keys to move/i)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has proper ARIA roles for task list', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const taskList = screen.getByRole('list');
      expect(taskList).toHaveAttribute(
        'aria-label',
        'Sortable task list for project project-1'
      );
    });

    it('has proper ARIA labels for drag handles', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const dragHandles = screen.getAllByRole('button');
      expect(dragHandles[0]).toHaveAttribute(
        'aria-label',
        'Drag handle for task: First Task'
      );
      expect(dragHandles[1]).toHaveAttribute(
        'aria-label',
        'Drag handle for task: Second Task'
      );
    });

    it('has screen reader announcement region', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const announcementRegion = screen.getByRole('status');
      expect(announcementRegion).toHaveAttribute('aria-live', 'assertive');
      expect(announcementRegion).toHaveAttribute('aria-atomic', 'true');
      expect(announcementRegion).toHaveClass('sr-only');
    });

    it('has tabindex on drag handles for keyboard navigation', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const dragHandles = screen.getAllByRole('button');
      dragHandles.forEach((handle) => {
        expect(handle).toHaveAttribute('tabindex', '0');
      });
    });

    it('has ARIA label on task items', () => {
      const { container } = render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const taskItems = container.querySelectorAll('[role="listitem"]');
      expect(taskItems[0]).toHaveAttribute(
        'aria-label',
        'Task: First Task, Priority: high, Status: pending'
      );
    });
  });

  describe('Visual Feedback', () => {
    it('applies correct priority color classes', () => {
      const { container } = render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const taskItems = container.querySelectorAll('[role="listitem"]');
      expect(taskItems[0]).toHaveClass('bg-yellow-50', 'border-yellow-400'); // high priority
      expect(taskItems[1]).toHaveClass('bg-blue-50', 'border-blue-300'); // medium priority
      expect(taskItems[2]).toHaveClass('bg-gray-100', 'border-gray-300'); // low priority
    });

    it('applies correct status badge colors', () => {
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const pendingBadge = screen.getByText('pending');
      const runningBadge = screen.getByText('running');
      const completedBadge = screen.getByText('completed');

      expect(pendingBadge).toHaveClass('bg-gray-500');
      expect(runningBadge).toHaveClass('bg-blue-500');
      expect(completedBadge).toHaveClass('bg-green-500');
    });

    it('shows drag handle icon with proper styling', () => {
      const { container } = render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      const dragIcons = container.querySelectorAll('svg');
      expect(dragIcons.length).toBeGreaterThan(0);
      dragIcons.forEach((icon) => {
        expect(icon).toHaveClass('w-5', 'h-5', 'text-gray-400');
        expect(icon).toHaveAttribute('aria-hidden', 'true');
      });
    });
  });

  describe('Task Sorting', () => {
    it('sorts tasks by order property', () => {
      const unsortedTasks: Task[] = [
        { ...mockTasks[0], order: 2 },
        { ...mockTasks[1], order: 0 },
        { ...mockTasks[2], order: 1 },
      ];

      const { container } = render(
        <DraggableTaskList
          projectId="project-1"
          tasks={unsortedTasks}
          onReorder={mockOnReorder}
        />
      );

      const taskTitles = Array.from(container.querySelectorAll('h3')).map(
        (el) => el.textContent
      );

      expect(taskTitles).toEqual(['Second Task', 'Third Task', 'First Task']);
    });

    it('handles missing order property gracefully', () => {
      const tasksWithoutOrder: Task[] = mockTasks.map((task) => {
        const { order, ...rest } = task;
        return rest as Task;
      });

      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={tasksWithoutOrder}
          onReorder={mockOnReorder}
        />
      );

      expect(screen.getByText('First Task')).toBeInTheDocument();
      expect(screen.getByText('Second Task')).toBeInTheDocument();
    });
  });

  describe('Integration with useDragAndDrop Hook', () => {
    it('passes tasks to useDragAndDrop hook', async () => {
      const { useDragAndDrop } = await import('../hooks/useDragAndDrop');

      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
        />
      );

      expect(useDragAndDrop).toHaveBeenCalledWith(
        expect.objectContaining({
          tasks: mockTasks,
          onReorder: mockOnReorder,
        })
      );
    });

    it('passes onReorderComplete callback when provided', async () => {
      const { useDragAndDrop } = await import('../hooks/useDragAndDrop');

      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={mockTasks}
          onReorder={mockOnReorder}
          onReorderComplete={mockOnReorderComplete}
        />
      );

      expect(useDragAndDrop).toHaveBeenCalledWith(
        expect.objectContaining({
          tasks: mockTasks,
          onReorder: mockOnReorder,
          onReorderComplete: mockOnReorderComplete,
        })
      );
    });
  });

  describe('Edge Cases', () => {
    it('handles single task gracefully', () => {
      const singleTask = [mockTasks[0]];

      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={singleTask}
          onReorder={mockOnReorder}
        />
      );

      expect(screen.getByText('First Task')).toBeInTheDocument();
      expect(screen.getAllByRole('button')).toHaveLength(1);
    });

    it('handles very long task titles with truncation', () => {
      const longTitleTask: Task = {
        ...mockTasks[0],
        title: 'This is a very long task title that should be truncated to prevent layout issues',
      };

      const { container } = render(
        <DraggableTaskList
          projectId="project-1"
          tasks={[longTitleTask]}
          onReorder={mockOnReorder}
        />
      );

      const title = container.querySelector('h3');
      expect(title).toHaveClass('truncate');
    });

    it('handles tasks with optional fields missing', () => {
      const minimalTask: Task = {
        id: 'task-min',
        projectId: 'project-1',
        title: 'Minimal Task',
        description: 'Description',
        status: 'pending',
        priority: 'low',
        skill_name: 'test',
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={[minimalTask]}
          onReorder={mockOnReorder}
        />
      );

      expect(screen.getByText('Minimal Task')).toBeInTheDocument();
    });
  });

  describe('Performance', () => {
    it('renders large task lists efficiently', () => {
      const largeTasks: Task[] = Array.from({ length: 100 }, (_, i) => ({
        id: `task-${i}`,
        projectId: 'project-1',
        title: `Task ${i}`,
        description: `Description ${i}`,
        status: 'pending' as const,
        priority: 'medium' as const,
        skill_name: `skill-${i}`,
        order: i,
        createdAt: new Date(),
        updatedAt: new Date(),
      }));

      const startTime = performance.now();
      render(
        <DraggableTaskList
          projectId="project-1"
          tasks={largeTasks}
          onReorder={mockOnReorder}
        />
      );
      const endTime = performance.now();

      // Should render 100 tasks in less than 1 second
      expect(endTime - startTime).toBeLessThan(1000);
      expect(screen.getByText('Task 0')).toBeInTheDocument();
      expect(screen.getByText('Task 99')).toBeInTheDocument();
    });
  });
});
