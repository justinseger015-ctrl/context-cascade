import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CronBuilder } from '../CronBuilder';

describe('CronBuilder', () => {
  const mockOnChange = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders preset buttons', () => {
    render(<CronBuilder value="" onChange={mockOnChange} />);

    expect(screen.getByText('Every minute')).toBeInTheDocument();
    expect(screen.getByText('Every hour')).toBeInTheDocument();
    expect(screen.getByText('Daily at 9am')).toBeInTheDocument();
    expect(screen.getByText('Weekly (Monday 9am)')).toBeInTheDocument();
  });

  it('renders custom cron input', () => {
    render(<CronBuilder value="" onChange={mockOnChange} />);

    const input = screen.getByPlaceholderText(/minute hour day/i);
    expect(input).toBeInTheDocument();
  });

  it('calls onChange when preset is clicked', async () => {
    const user = userEvent.setup();
    render(<CronBuilder value="" onChange={mockOnChange} />);

    const presetButton = screen.getByText('Every hour');
    await user.click(presetButton);

    expect(mockOnChange).toHaveBeenCalledWith('0 * * * *');
  });

  it('calls onChange when custom input changes', async () => {
    const user = userEvent.setup();
    render(<CronBuilder value="" onChange={mockOnChange} />);

    const input = screen.getByPlaceholderText(/minute hour day/i);
    await user.type(input, '0 9 * * *');

    expect(mockOnChange).toHaveBeenCalledWith('0 9 * * *');
  });

  it('highlights selected preset', () => {
    render(<CronBuilder value="0 * * * *" onChange={mockOnChange} />);

    const selectedButton = screen.getByText('Every hour').closest('button');
    expect(selectedButton).toHaveClass('bg-blue-50');
  });

  it('displays error message when provided', () => {
    const errorMessage = 'Invalid cron expression';
    render(<CronBuilder value="" onChange={mockOnChange} error={errorMessage} />);

    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  it('shows next run times for valid cron expression', () => {
    render(<CronBuilder value="0 9 * * *" onChange={mockOnChange} />);

    expect(screen.getByText(/next 5 executions/i)).toBeInTheDocument();
  });

  it('does not show next run times for invalid cron expression', () => {
    render(<CronBuilder value="invalid" onChange={mockOnChange} />);

    expect(screen.queryByText(/next 5 executions/i)).not.toBeInTheDocument();
  });

  it('shows syntax help in details element', () => {
    render(<CronBuilder value="" onChange={mockOnChange} />);

    const summary = screen.getByText(/cron expression syntax help/i);
    expect(summary).toBeInTheDocument();

    // Click to expand
    fireEvent.click(summary);

    expect(screen.getByText(/special characters/i)).toBeInTheDocument();
    expect(screen.getByText(/examples/i)).toBeInTheDocument();
  });

  it('clears preset selection when custom input is modified', async () => {
    const user = userEvent.setup();
    render(<CronBuilder value="0 * * * *" onChange={mockOnChange} />);

    // Initially selected preset
    const presetButton = screen.getByText('Every hour').closest('button');
    expect(presetButton).toHaveClass('bg-blue-50');

    // Type in custom input
    const input = screen.getByPlaceholderText(/minute hour day/i);
    await user.clear(input);
    await user.type(input, '0 9 * * *');

    // Preset should be deselected
    expect(presetButton).not.toHaveClass('bg-blue-50');
  });

  it('formats next run times correctly', () => {
    render(<CronBuilder value="0 9 * * *" onChange={mockOnChange} />);

    // Should show formatted dates with day, month, time
    const runTimes = screen.getAllByText(/\w{3}, \w{3} \d{1,2}, \d{2}:\d{2}:\d{2}/);
    expect(runTimes.length).toBeGreaterThan(0);
  });
});
