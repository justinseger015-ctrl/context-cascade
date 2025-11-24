import { render, screen, waitFor } from '@testing-library/react';
import { ProjectDashboard } from './ProjectDashboard';
import { useProjectStore } from '../store/useProjectStore';
import type { Project, Task } from '../types';

// Mock the store
jest.mock('../store/useProjectStore');

// Mock child components
jest.mock('./TaskList', () => ({
  TaskList: ({ tasks }: { tasks: Task[] }) => (
    <div data-testid="task-list">TaskList: {tasks.length} tasks</div>
  ),
}));

jest.mock('./TaskFilters', () => ({
  TaskFilters: () => <div data-testid="task-filters">TaskFilters</div>,
}));

describe('ProjectDashboard', () => {
  const mockProject: Project = {
    id: 'project-1',
    name: 'Test Project',
    description: 'Test project description',
    status: 'in_progress',
    createdAt: new Date('2025-01-01T00:00:00Z'),
    updatedAt: new Date('2025-01-01T00:00:00Z'),
    tasks: [
      {
        id: 'task-1',
        projectId: 'project-1',
        title: 'Task 1',
        description: 'Description 1',
        status: 'completed',
        priority: 'high',
        skill_name: 'react-developer',
        createdAt: new Date('2025-01-01T00:00:00Z'),
        updatedAt: new Date('2025-01-01T00:00:00Z'),
      },
      {
        id: 'task-2',
        projectId: 'project-1',
        title: 'Task 2',
        description: 'Description 2',
        status: 'running',
        priority: 'medium',
        skill_name: 'api-designer',
        createdAt: new Date('2025-01-02T00:00:00Z'),
        updatedAt: new Date('2025-01-02T00:00:00Z'),
      },
      {
        id: 'task-3',
        projectId: 'project-1',
        title: 'Task 3',
        description: 'Description 3',
        status: 'pending',
        priority: 'low',
        skill_name: 'tester',
        createdAt: new Date('2025-01-03T00:00:00Z'),
        updatedAt: new Date('2025-01-03T00:00:00Z'),
      },
      {
        id: 'task-4',
        projectId: 'project-1',
        title: 'Task 4',
        description: 'Description 4',
        status: 'failed',
        priority: 'critical',
        skill_name: 'react-developer',
        createdAt: new Date('2025-01-04T00:00:00Z'),
        updatedAt: new Date('2025-01-04T00:00:00Z'),
      },
    ],
  };

  const mockStore = {
    projects: [mockProject],
    updateTask: jest.fn(),
    deleteTask: jest.fn(),
    reorderTasks: jest.fn(),
    runTaskNow: jest.fn(),
  };

  beforeEach(() => {
    (useProjectStore as unknown as jest.Mock).mockReturnValue(mockStore);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders project header with name and description', () => {
    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText('Test Project')).toBeInTheDocument();
    expect(screen.getByText('Test project description')).toBeInTheDocument();
  });

  it('displays project status badge', () => {
    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText(/In progress/i)).toBeInTheDocument();
  });

  it('calculates and displays correct stats', () => {
    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText('4')).toBeInTheDocument(); // Total tasks
    expect(screen.getByText('1')).toBeInTheDocument(); // Running tasks
    // Completion rate: 1/4 = 25%
    expect(screen.getByText('25.0%')).toBeInTheDocument();
  });

  it('displays all stat cards', () => {
    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText('Total Tasks')).toBeInTheDocument();
    expect(screen.getByText('Running')).toBeInTheDocument();
    expect(screen.getByText('Completed')).toBeInTheDocument();
    expect(screen.getByText('Failed')).toBeInTheDocument();
    expect(screen.getByText('Completion')).toBeInTheDocument();
  });

  it('renders TaskFilters component', () => {
    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByTestId('task-filters')).toBeInTheDocument();
  });

  it('renders TaskList component with tasks', () => {
    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByTestId('task-list')).toBeInTheDocument();
    expect(screen.getByText('TaskList: 4 tasks')).toBeInTheDocument();
  });

  it('shows not found message for invalid project', () => {
    render(<ProjectDashboard projectId="invalid-id" />);

    expect(screen.getByText('Project not found')).toBeInTheDocument();
    expect(screen.getByText('The requested project could not be found.')).toBeInTheDocument();
  });

  it('displays created date', () => {
    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText(/Created/)).toBeInTheDocument();
    expect(screen.getByText(/1\/1\/2025/)).toBeInTheDocument();
  });

  it('displays task count with correct pluralization', () => {
    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText('4 tasks')).toBeInTheDocument();
  });

  it('handles project with no tasks', () => {
    const emptyProject = { ...mockProject, tasks: [] };
    (useProjectStore as unknown as jest.Mock).mockReturnValue({
      ...mockStore,
      projects: [emptyProject],
    });

    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText('0 tasks')).toBeInTheDocument();
    expect(screen.getByText('0.0%')).toBeInTheDocument(); // 0% completion
  });

  it('calculates stats correctly with all completed tasks', () => {
    const completedProject = {
      ...mockProject,
      tasks: mockProject.tasks!.map((t) => ({ ...t, status: 'completed' as const })),
    };
    (useProjectStore as unknown as jest.Mock).mockReturnValue({
      ...mockStore,
      projects: [completedProject],
    });

    render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText('100.0%')).toBeInTheDocument();
  });

  it('renders progress bar with correct width', () => {
    const { container } = render(<ProjectDashboard projectId="project-1" />);

    const progressBar = container.querySelector('.bg-purple-600');
    expect(progressBar).toHaveStyle({ width: '25%' });
  });

  it('updates when project changes', async () => {
    const { rerender } = render(<ProjectDashboard projectId="project-1" />);

    expect(screen.getByText('Test Project')).toBeInTheDocument();

    const updatedProject = { ...mockProject, name: 'Updated Project' };
    (useProjectStore as unknown as jest.Mock).mockReturnValue({
      ...mockStore,
      projects: [updatedProject],
    });

    rerender(<ProjectDashboard projectId="project-1" />);

    await waitFor(() => {
      expect(screen.getByText('Updated Project')).toBeInTheDocument();
    });
  });
});
