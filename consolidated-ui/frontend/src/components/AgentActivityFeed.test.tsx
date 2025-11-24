import { render, screen } from '@testing-library/react';
import { AgentActivityFeed } from './AgentActivityFeed';
import { useStore } from '../store';
import type { Agent, AgentActivity } from '../types';

// Mock Zustand store
jest.mock('../store', () => ({
  useStore: jest.fn(),
}));

describe('AgentActivityFeed', () => {
  const mockAgents: Agent[] = [
    {
      id: 'agent-1',
      name: 'Research Agent',
      type: 'researcher',
      status: 'busy',
      capabilities: ['research'],
    },
    {
      id: 'agent-2',
      name: 'Coder Agent',
      type: 'coder',
      status: 'idle',
      capabilities: ['coding'],
    },
  ];

  const mockAgentActivity: AgentActivity[] = [
    {
      id: 'activity-1',
      agentId: 'agent-1',
      action: 'Started research task',
      timestamp: new Date('2025-01-01T10:00:00Z'),
      details: {
        taskId: 'task-1',
        taskTitle: 'Research ML frameworks',
        status: 'running',
        skillName: 'research-workflow',
      },
    },
    {
      id: 'activity-2',
      agentId: 'agent-2',
      action: 'Completed coding task',
      timestamp: new Date('2025-01-01T09:00:00Z'),
      details: {
        taskId: 'task-2',
        taskTitle: 'Implement API endpoint',
        status: 'completed',
        completedAt: '2025-01-01T09:05:00Z',
        outputPreview: 'Successfully implemented /api/users endpoint',
      },
    },
    {
      id: 'activity-3',
      agentId: 'agent-2',
      action: 'Failed deployment',
      timestamp: new Date('2025-01-01T08:00:00Z'),
      details: {
        taskId: 'task-3',
        taskTitle: 'Deploy to production',
        status: 'failed',
        error: 'Connection timeout',
      },
    },
  ];

  const mockFetchAgentActivity = jest.fn().mockResolvedValue(undefined);

  beforeEach(() => {
    jest.clearAllMocks();

    (useStore as unknown as jest.Mock).mockReturnValue({
      agentActivity: mockAgentActivity,
      agents: mockAgents,
      fetchAgentActivity: mockFetchAgentActivity,
      isLoading: false,
      error: null,
    });
  });

  describe('Rendering', () => {
    it('renders activity feed header', () => {
      render(<AgentActivityFeed />);

      expect(screen.getByText('Agent Activity Feed')).toBeInTheDocument();
      expect(screen.getByText('3 recent activities')).toBeInTheDocument();
    });

    it('fetches agent activity on mount', () => {
      render(<AgentActivityFeed />);

      expect(mockFetchAgentActivity).toHaveBeenCalledWith(undefined, 100);
    });

    it('displays all activities', () => {
      render(<AgentActivityFeed />);

      expect(screen.getByText('Started research task')).toBeInTheDocument();
      expect(screen.getByText('Completed coding task')).toBeInTheDocument();
      expect(screen.getByText('Failed deployment')).toBeInTheDocument();
    });
  });

  describe('Activity Details', () => {
    it('displays agent name and type', () => {
      render(<AgentActivityFeed />);

      expect(screen.getByText('Research Agent')).toBeInTheDocument();
      expect(screen.getByText('researcher')).toBeInTheDocument();
      expect(screen.getAllByText('coder')).toHaveLength(2); // 2 activities from coder
    });

    it('displays task information', () => {
      render(<AgentActivityFeed />);

      expect(screen.getByText(/Research ML frameworks/)).toBeInTheDocument();
      expect(screen.getByText(/Implement API endpoint/)).toBeInTheDocument();
    });

    it('displays skill name', () => {
      render(<AgentActivityFeed />);

      expect(screen.getByText('research-workflow')).toBeInTheDocument();
    });

    it('displays status badges with correct colors', () => {
      render(<AgentActivityFeed />);

      const runningBadge = screen.getByText('running');
      expect(runningBadge).toHaveClass('text-blue-600');

      const completedBadge = screen.getByText('completed');
      expect(completedBadge).toHaveClass('text-green-600');

      const failedBadge = screen.getByText('failed');
      expect(failedBadge).toHaveClass('text-red-600');
    });
  });

  describe('Duration Calculation', () => {
    it('displays duration for completed activities', () => {
      render(<AgentActivityFeed />);

      // Activity 2: completed in 5 minutes (300000ms)
      expect(screen.getByText('5m 0s')).toBeInTheDocument();
    });

    it('does not display duration for running activities', () => {
      render(<AgentActivityFeed />);

      const activities = screen.getAllByRole('generic');
      const runningActivity = activities.find((el) =>
        el.textContent?.includes('Started research task')
      );

      expect(runningActivity?.textContent).not.toMatch(/\d+m \d+s/);
    });

    it('formats milliseconds correctly', () => {
      const activityWithMs: AgentActivity = {
        id: 'activity-ms',
        agentId: 'agent-1',
        action: 'Quick task',
        timestamp: new Date('2025-01-01T10:00:00.000Z'),
        details: {
          status: 'completed',
          completedAt: '2025-01-01T10:00:00.500Z',
        },
      };

      (useStore as unknown as jest.Mock).mockReturnValue({
        agentActivity: [activityWithMs],
        agents: mockAgents,
        fetchAgentActivity: mockFetchAgentActivity,
        isLoading: false,
        error: null,
      });

      render(<AgentActivityFeed />);

      expect(screen.getByText('500ms')).toBeInTheDocument();
    });
  });

  describe('Output Preview', () => {
    it('displays output preview when available', () => {
      render(<AgentActivityFeed />);

      expect(
        screen.getByText('Successfully implemented /api/users endpoint')
      ).toBeInTheDocument();
    });

    it('does not display preview section when not available', () => {
      render(<AgentActivityFeed />);

      const activities = screen.getAllByRole('generic');
      const activityWithoutPreview = activities.find((el) =>
        el.textContent?.includes('Started research task')
      );

      expect(activityWithoutPreview?.querySelector('.bg-gray-50')).not.toBeInTheDocument();
    });
  });

  describe('Error Display', () => {
    it('displays error message for failed activities', () => {
      render(<AgentActivityFeed />);

      expect(screen.getByText(/Error: Connection timeout/)).toBeInTheDocument();
    });

    it('styles error messages appropriately', () => {
      render(<AgentActivityFeed />);

      const errorMessage = screen.getByText(/Error: Connection timeout/);
      const errorContainer = errorMessage.closest('div');

      expect(errorContainer).toHaveClass('bg-red-50', 'border-red-200', 'text-red-600');
    });
  });

  describe('Sorting', () => {
    it('displays activities in reverse chronological order', () => {
      render(<AgentActivityFeed />);

      const activities = screen.getAllByText(/task/i);

      // Most recent first (10:00) → Started research task
      // Then 09:00 → Completed coding task
      // Then 08:00 → Failed deployment
      expect(activities[0]).toHaveTextContent('Started research task');
    });
  });

  describe('Loading State', () => {
    it('shows loading message when fetching', () => {
      (useStore as unknown as jest.Mock).mockReturnValue({
        agentActivity: [],
        agents: [],
        fetchAgentActivity: mockFetchAgentActivity,
        isLoading: true,
        error: null,
      });

      render(<AgentActivityFeed />);

      expect(screen.getByText('Loading agent activities...')).toBeInTheDocument();
    });
  });

  describe('Error State', () => {
    it('displays error message when fetch fails', () => {
      (useStore as unknown as jest.Mock).mockReturnValue({
        agentActivity: [],
        agents: [],
        fetchAgentActivity: mockFetchAgentActivity,
        isLoading: false,
        error: 'Failed to fetch activities',
      });

      render(<AgentActivityFeed />);

      expect(
        screen.getByText(/Error loading activities: Failed to fetch activities/)
      ).toBeInTheDocument();
    });
  });

  describe('Empty State', () => {
    it('shows empty message when no activities exist', () => {
      (useStore as unknown as jest.Mock).mockReturnValue({
        agentActivity: [],
        agents: [],
        fetchAgentActivity: mockFetchAgentActivity,
        isLoading: false,
        error: null,
      });

      render(<AgentActivityFeed />);

      expect(screen.getByText('No agent activity yet')).toBeInTheDocument();
    });
  });

  describe('Activity Enhancement', () => {
    it('enhances activities with agent metadata', () => {
      render(<AgentActivityFeed />);

      // Check that agent names from the agents array are displayed
      expect(screen.getByText('Research Agent')).toBeInTheDocument();
      expect(screen.getByText('Coder Agent')).toBeInTheDocument();
    });

    it('handles missing agent gracefully', () => {
      const activityWithoutAgent: AgentActivity = {
        id: 'activity-orphan',
        agentId: 'unknown-agent',
        action: 'Mystery task',
        timestamp: new Date('2025-01-01T10:00:00Z'),
        details: {},
      };

      (useStore as unknown as jest.Mock).mockReturnValue({
        agentActivity: [activityWithoutAgent],
        agents: mockAgents,
        fetchAgentActivity: mockFetchAgentActivity,
        isLoading: false,
        error: null,
      });

      render(<AgentActivityFeed />);

      // Should display agent ID when agent not found
      expect(screen.getByText('unknown-agent')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has proper structure for screen readers', () => {
      render(<AgentActivityFeed />);

      const heading = screen.getByText('Agent Activity Feed');
      expect(heading.tagName).toBe('H3');
    });
  });
});
