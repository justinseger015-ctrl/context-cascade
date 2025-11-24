import { render, screen, fireEvent } from '@testing-library/react';
import { TaskFilters } from './TaskFilters';
import type { TaskFilters as TaskFiltersType } from '../types';

describe('TaskFilters', () => {
  const mockOnFilterChange = jest.fn();
  const defaultProps = {
    filters: {} as TaskFiltersType,
    onFilterChange: mockOnFilterChange,
    availableSkills: ['react-developer', 'api-designer', 'tester'],
  };

  beforeEach(() => {
    mockOnFilterChange.mockClear();
  });

  it('renders status filters', () => {
    render(<TaskFilters {...defaultProps} />);

    expect(screen.getByText('Pending')).toBeInTheDocument();
    expect(screen.getByText('Running')).toBeInTheDocument();
    expect(screen.getByText('Completed')).toBeInTheDocument();
    expect(screen.getByText('Failed')).toBeInTheDocument();
  });

  it('renders skill filters when available', () => {
    render(<TaskFilters {...defaultProps} />);

    expect(screen.getByText('react-developer')).toBeInTheDocument();
    expect(screen.getByText('api-designer')).toBeInTheDocument();
    expect(screen.getByText('tester')).toBeInTheDocument();
  });

  it('toggles status filter on click', () => {
    render(<TaskFilters {...defaultProps} />);

    fireEvent.click(screen.getByText('Pending'));

    expect(mockOnFilterChange).toHaveBeenCalledWith({
      status: ['pending'],
    });
  });

  it('toggles multiple status filters', () => {
    const filters: TaskFiltersType = { status: ['pending'] };
    render(<TaskFilters {...defaultProps} filters={filters} />);

    fireEvent.click(screen.getByText('Running'));

    expect(mockOnFilterChange).toHaveBeenCalledWith({
      status: ['pending', 'running'],
    });
  });

  it('removes status filter when clicked again', () => {
    const filters: TaskFiltersType = { status: ['pending', 'running'] };
    render(<TaskFilters {...defaultProps} filters={filters} />);

    fireEvent.click(screen.getByText('Pending'));

    expect(mockOnFilterChange).toHaveBeenCalledWith({
      status: ['running'],
    });
  });

  it('toggles skill filter', () => {
    render(<TaskFilters {...defaultProps} />);

    fireEvent.click(screen.getByText('react-developer'));

    expect(mockOnFilterChange).toHaveBeenCalledWith({
      skill_name: ['react-developer'],
    });
  });

  it('clears all filters', () => {
    const filters: TaskFiltersType = {
      status: ['pending', 'running'],
      skill_name: ['react-developer'],
    };
    render(<TaskFilters {...defaultProps} filters={filters} />);

    fireEvent.click(screen.getByText('Clear all'));

    expect(mockOnFilterChange).toHaveBeenCalledWith({});
  });

  it('does not show clear button when no filters active', () => {
    render(<TaskFilters {...defaultProps} />);

    expect(screen.queryByText('Clear all')).not.toBeInTheDocument();
  });

  it('applies correct styling to active filters', () => {
    const filters: TaskFiltersType = { status: ['pending'] };
    render(<TaskFilters {...defaultProps} filters={filters} />);

    const pendingButton = screen.getByText('Pending');
    expect(pendingButton).toHaveClass('bg-gray-200', 'text-gray-800');
  });
});
