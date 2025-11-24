import { render, screen } from '@testing-library/react';
import { WebSocketIndicator, WebSocketBadge } from './WebSocketIndicator';
import { useStore } from '../store';

describe('WebSocketIndicator', () => {
  beforeEach(() => {
    useStore.setState({
      connectionStatus: 'disconnected',
      reconnectAttempts: 0,
      error: null,
    });
  });

  it('renders connected status', () => {
    useStore.setState({ connectionStatus: 'connected' });

    render(<WebSocketIndicator />);

    expect(screen.getByText('Connected')).toBeInTheDocument();
    expect(screen.getByText('Connected')).toHaveClass('text-green-700');
  });

  it('renders connecting status', () => {
    useStore.setState({ connectionStatus: 'connecting' });

    render(<WebSocketIndicator />);

    expect(screen.getByText('Connecting...')).toBeInTheDocument();
    expect(screen.getByText('Connecting...')).toHaveClass('text-yellow-700');
  });

  it('renders reconnecting status with attempt count', () => {
    useStore.setState({
      connectionStatus: 'reconnecting',
      reconnectAttempts: 3,
    });

    render(<WebSocketIndicator />);

    expect(screen.getByText('Reconnecting... (3)')).toBeInTheDocument();
    expect(screen.getByText('Reconnecting... (3)')).toHaveClass(
      'text-orange-700'
    );
  });

  it('renders disconnected status', () => {
    useStore.setState({ connectionStatus: 'disconnected' });

    render(<WebSocketIndicator />);

    expect(screen.getByText('Disconnected')).toBeInTheDocument();
    expect(screen.getByText('Disconnected')).toHaveClass('text-red-700');
  });

  it('displays error icon when error is present', () => {
    useStore.setState({
      connectionStatus: 'disconnected',
      error: 'Connection failed',
    });

    render(<WebSocketIndicator />);

    const errorIcon = screen.getByTitle('Connection failed');
    expect(errorIcon).toBeInTheDocument();
  });

  it('shows pulsing animation for connecting status', () => {
    useStore.setState({ connectionStatus: 'connecting' });

    const { container } = render(<WebSocketIndicator />);

    const pulsingElement = container.querySelector('.animate-pulse');
    expect(pulsingElement).toBeInTheDocument();
  });

  it('shows pulsing animation for reconnecting status', () => {
    useStore.setState({ connectionStatus: 'reconnecting' });

    const { container } = render(<WebSocketIndicator />);

    const pulsingElement = container.querySelector('.animate-pulse');
    expect(pulsingElement).toBeInTheDocument();
  });

  it('does not show pulsing animation for connected status', () => {
    useStore.setState({ connectionStatus: 'connected' });

    const { container } = render(<WebSocketIndicator />);

    // Should have bg-green-100 but not animate-pulse
    const statusDot = container.querySelector('.bg-green-100');
    expect(statusDot).toBeInTheDocument();
    expect(statusDot).not.toHaveClass('animate-pulse');
  });
});

describe('WebSocketBadge', () => {
  it('renders green badge when connected', () => {
    useStore.setState({ connectionStatus: 'connected' });

    const { container } = render(<WebSocketBadge />);

    const badge = container.querySelector('.bg-green-500');
    expect(badge).toBeInTheDocument();
  });

  it('renders yellow pulsing badge when connecting', () => {
    useStore.setState({ connectionStatus: 'connecting' });

    const { container } = render(<WebSocketBadge />);

    const badge = container.querySelector('.bg-yellow-500.animate-pulse');
    expect(badge).toBeInTheDocument();
  });

  it('renders orange pulsing badge when reconnecting', () => {
    useStore.setState({ connectionStatus: 'reconnecting' });

    const { container } = render(<WebSocketBadge />);

    const badge = container.querySelector('.bg-orange-500.animate-pulse');
    expect(badge).toBeInTheDocument();
  });

  it('renders red badge when disconnected', () => {
    useStore.setState({ connectionStatus: 'disconnected' });

    const { container } = render(<WebSocketBadge />);

    const badge = container.querySelector('.bg-red-500');
    expect(badge).toBeInTheDocument();
  });

  it('has title attribute with connection status', () => {
    useStore.setState({ connectionStatus: 'connected' });

    const { container } = render(<WebSocketBadge />);

    const badge = container.querySelector('[title="connected"]');
    expect(badge).toBeInTheDocument();
  });
});
