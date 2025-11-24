import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AgentMonitor } from './AgentMonitor';
import { useStore } from '../store';
import type { Agent, AgentActivity } from '../types';

// Mock Zustand store
jest.mock('../store', () => ({
  useStore: jest.fn(),
}));

// Mock ReactFlow to avoid canvas rendering issues in tests
jest.mock('reactflow', () => ({
  __esModule: true,
  default: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="react-flow">{children}</div>
  ),
  Background: () => <div data-testid="react-flow-background" />,
  Controls: () => <div data-testid="react-flow-controls" />,
  MiniMap: () => <div data-testid="react-flow-minimap" />,
  Panel: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  useNodesState: (initialNodes: unknown[]) => [
    initialNodes,
    jest.fn(),
    jest.fn(),
  ],
  useEdgesState: (initialEdges: unknown[]) => [
    initialEdges,
    jest.fn(),
    jest.fn(),
  ],
  ConnectionMode: { Loose: 'loose' },
}));

describe('AgentMonitor', () => {
  const mockAgents: Agent[] = [
    {
      id: 'agent-1',
      name: 'Research Agent',
      type: 'researcher',
      status: 'busy',
      capabilities: ['research', 'analysis'],
      currentTask: 'task-1',
    },
    {
      id: 'agent-2',
      name: 'Coder Agent',
      type: 'coder',
      status: 'idle',
      capabilities: ['coding', 'testing'],
    },
    {
      id: 'agent-3',
      name: 'Tester Agent',
      type: 'tester',
      status: 'error',
      capabilities: ['testing', 'qa'],
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
  ];

  const mockFetchAgents = jest.fn().mockResolvedValue(undefined);
  const mockFetchAgentActivity = jest.fn().mockResolvedValue(undefined);

  beforeEach(() => {
    jest.clearAllMocks();

    (useStore as unknown as jest.Mock).mockImplementation((selector) => {
      const state = {
        agents: mockAgents,
        agentActivity: mockAgentActivity,
        isLoading: false,
        error: null,
        fetchAgents: mockFetchAgents,
        fetchAgentActivity: mockFetchAgentActivity,
        updateAgent: jest.fn(),
        updateTask: jest.fn(),
      };

      return selector ? selector(state) : state;
    });
  });

  describe('Rendering', () => {
    it('renders agent monitor header', () => {
      render(<AgentMonitor />);

      expect(screen.getByText('Agent Monitor')).toBeInTheDocument();
      expect(
        screen.getByText(
          'Real-time agent activity tracking and workflow visualization'
        )
      ).toBeInTheDocument();
    });

    it('displays summary statistics', () => {
      render(<AgentMonitor />);

      expect(screen.getByText('Total Agents')).toBeInTheDocument();
      expect(screen.getByText('3')).toBeInTheDocument(); // 3 total agents

      expect(screen.getByText('Active Agents')).toBeInTheDocument();
      expect(screen.getByText('2')).toBeInTheDocument(); // busy + idle

      expect(screen.getByText('Busy Agents')).toBeInTheDocument();
      expect(screen.getByText('1')).toBeInTheDocument(); // 1 busy

      expect(screen.getByText('Error Agents')).toBeInTheDocument();
      // Error count also shows 1
    });

    it('fetches agents on mount', () => {
      render(<AgentMonitor />);

      expect(mockFetchAgents).toHaveBeenCalledTimes(1);
    });
  });

  describe('Tab Navigation', () => {
    it('defaults to activity feed tab', () => {
      render(<AgentMonitor />);

      const feedTab = screen.getByRole('button', { name: /activity feed/i });
      const graphTab = screen.getByRole('button', { name: /workflow graph/i });

      expect(feedTab).toHaveClass('text-blue-600');
      expect(graphTab).toHaveClass('text-gray-500');
    });

    it('switches to workflow graph tab when clicked', async () => {
      const user = userEvent.setup();
      render(<AgentMonitor />);

      const graphTab = screen.getByRole('button', { name: /workflow graph/i });
      await user.click(graphTab);

      expect(graphTab).toHaveClass('text-blue-600');
      expect(screen.getByTestId('react-flow')).toBeInTheDocument();
    });

    it('switches back to activity feed tab', async () => {
      const user = userEvent.setup();
      render(<AgentMonitor />);

      // Switch to graph
      const graphTab = screen.getByRole('button', { name: /workflow graph/i });
      await user.click(graphTab);

      // Switch back to feed
      const feedTab = screen.getByRole('button', { name: /activity feed/i });
      await user.click(feedTab);

      expect(feedTab).toHaveClass('text-blue-600');
      expect(screen.getByText('Agent Activity Feed')).toBeInTheDocument();
    });
  });

  describe('Loading State', () => {
    it('shows loading state when fetching agents', () => {
      (useStore as unknown as jest.Mock).mockImplementation((selector) => {
        const state = {
          agents: [],
          agentActivity: [],
          isLoading: true,
          error: null,
          fetchAgents: mockFetchAgents,
          fetchAgentActivity: mockFetchAgentActivity,
        };
        return selector ? selector(state) : state;
      });

      render(<AgentMonitor />);

      expect(screen.getByText('Loading agents...')).toBeInTheDocument();
    });
  });

  describe('Error State', () => {
    it('displays error message when fetch fails', () => {
      (useStore as unknown as jest.Mock).mockImplementation((selector) => {
        const state = {
          agents: [],
          agentActivity: [],
          isLoading: false,
          error: 'Failed to fetch agents',
          fetchAgents: mockFetchAgents,
          fetchAgentActivity: mockFetchAgentActivity,
        };
        return selector ? selector(state) : state;
      });

      render(<AgentMonitor />);

      expect(screen.getByText(/Error: Failed to fetch agents/i)).toBeInTheDocument();
    });
  });

  describe('Empty State', () => {
    it('shows empty state when no agents exist', () => {
      (useStore as unknown as jest.Mock).mockImplementation((selector) => {
        const state = {
          agents: [],
          agentActivity: [],
          isLoading: false,
          error: null,
          fetchAgents: mockFetchAgents,
          fetchAgentActivity: mockFetchAgentActivity,
        };
        return selector ? selector(state) : state;
      });

      render(<AgentMonitor />);

      expect(screen.getByText('No agents found')).toBeInTheDocument();
      expect(
        screen.getByText('Agents will appear here once they start executing tasks')
      ).toBeInTheDocument();
    });
  });

  describe('Activity Feed Integration', () => {
    it('renders activity feed component in feed tab', () => {
      render(<AgentMonitor />);

      expect(screen.getByText('Agent Activity Feed')).toBeInTheDocument();
      expect(mockFetchAgentActivity).toHaveBeenCalledWith(undefined, 100);
    });

    it('displays recent activities', () => {
      render(<AgentMonitor />);

      expect(screen.getByText('Started research task')).toBeInTheDocument();
      expect(screen.getByText('Completed coding task')).toBeInTheDocument();
    });
  });

  describe('Workflow Graph Integration', () => {
    it('renders workflow graph when tab is active', async () => {
      const user = userEvent.setup();
      render(<AgentMonitor />);

      const graphTab = screen.getByRole('button', { name: /workflow graph/i });
      await user.click(graphTab);

      expect(screen.getByTestId('react-flow')).toBeInTheDocument();
    });
  });

  describe('Statistics Calculation', () => {
    it('calculates active agents correctly', () => {
      render(<AgentMonitor />);

      // Active = busy + idle = 1 + 1 = 2
      const activeCount = screen.getAllByText('2')[0];
      expect(activeCount).toBeInTheDocument();
    });

    it('updates statistics when agents change', () => {
      const { rerender } = render(<AgentMonitor />);

      // Update mock to have more busy agents
      (useStore as unknown as jest.Mock).mockImplementation((selector) => {
        const state = {
          agents: [
            ...mockAgents,
            {
              id: 'agent-4',
              name: 'New Agent',
              type: 'coder',
              status: 'busy',
              capabilities: [],
            },
          ],
          agentActivity: mockAgentActivity,
          isLoading: false,
          error: null,
          fetchAgents: mockFetchAgents,
          fetchAgentActivity: mockFetchAgentActivity,
          updateAgent: jest.fn(),
          updateTask: jest.fn(),
        };
        return selector ? selector(state) : state;
      });

      rerender(<AgentMonitor />);

      expect(screen.getByText('4')).toBeInTheDocument(); // 4 total agents
    });
  });

  describe('Accessibility', () => {
    it('has proper ARIA roles for tabs', () => {
      render(<AgentMonitor />);

      const feedTab = screen.getByRole('button', { name: /activity feed/i });
      const graphTab = screen.getByRole('button', { name: /workflow graph/i });

      expect(feedTab).toBeInTheDocument();
      expect(graphTab).toBeInTheDocument();
    });

    it('has descriptive text for statistics', () => {
      render(<AgentMonitor />);

      expect(screen.getByText('Total Agents')).toBeInTheDocument();
      expect(screen.getByText('Active Agents')).toBeInTheDocument();
      expect(screen.getByText('Busy Agents')).toBeInTheDocument();
      expect(screen.getByText('Error Agents')).toBeInTheDocument();
    });
  });
});
