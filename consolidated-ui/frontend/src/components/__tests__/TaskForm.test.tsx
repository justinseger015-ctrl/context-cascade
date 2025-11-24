import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskForm } from '../TaskForm';
import { TaskFormData } from '../../validation/taskSchema';

// Mock CodeMirror to avoid complex setup
jest.mock('@uiw/react-codemirror', () => ({
  __esModule: true,
  default: ({ value, onChange }: { value: string; onChange: (val: string) => void }) => (
    <textarea
      data-testid="code-mirror"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  ),
}));

// Mock useSkills hook
jest.mock('../../hooks/useSkills', () => ({
  useSkills: () => ({
    skills: [
      { name: 'code-review', path: 'code-review', category: 'Quality' },
      { name: 'testing', path: 'testing', category: 'Testing' },
    ],
    loading: false,
    error: null,
  }),
  groupSkillsByCategory: (skills: any[]) =>
    skills.reduce((acc, skill) => {
      const category = skill.category || 'Other';
      if (!acc[category]) acc[category] = [];
      acc[category].push(skill);
      return acc;
    }, {}),
}));

describe('TaskForm', () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders all form fields', () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/skill/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/schedule/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/parameters/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/project/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/enable task/i)).toBeInTheDocument();
  });

  it('displays validation errors for required fields', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const submitButton = screen.getByRole('button', { name: /create task/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/skill name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/invalid cron expression/i)).toBeInTheDocument();
    });
  });

  it('validates cron expression format', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const cronInput = screen.getByPlaceholderText(/minute hour day/i);
    await userEvent.type(cronInput, 'invalid cron');

    const submitButton = screen.getByRole('button', { name: /create task/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid cron expression/i)).toBeInTheDocument();
    });
  });

  it('validates JSON parameters format', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const jsonEditor = screen.getByTestId('code-mirror');
    await userEvent.clear(jsonEditor);
    await userEvent.type(jsonEditor, '{invalid json}');

    const submitButton = screen.getByRole('button', { name: /create task/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid json format/i)).toBeInTheDocument();
    });
  });

  it('submits valid form data', async () => {
    const user = userEvent.setup();
    mockOnSubmit.mockResolvedValueOnce(undefined);

    render(<TaskForm onSubmit={mockOnSubmit} />);

    // Fill in skill
    const skillSelect = screen.getByLabelText(/skill/i);
    await user.selectOptions(skillSelect, 'code-review');

    // Fill in cron schedule
    const cronInput = screen.getByPlaceholderText(/minute hour day/i);
    await user.clear(cronInput);
    await user.type(cronInput, '0 9 * * *');

    // Fill in valid JSON
    const jsonEditor = screen.getByTestId('code-mirror');
    await user.clear(jsonEditor);
    await user.type(jsonEditor, '{"key": "value"}');

    // Submit form
    const submitButton = screen.getByRole('button', { name: /create task/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          skillName: 'code-review',
          cronSchedule: '0 9 * * *',
          parameters: '{"key": "value"}',
        })
      );
    });
  });

  it('calls onCancel when cancel button is clicked', async () => {
    render(<TaskForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);

    const cancelButton = screen.getByRole('button', { name: /cancel/i });
    fireEvent.click(cancelButton);

    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('disables submit button while submitting', async () => {
    const user = userEvent.setup();
    mockOnSubmit.mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 1000))
    );

    render(<TaskForm onSubmit={mockOnSubmit} />);

    // Fill in minimum required fields
    const skillSelect = screen.getByLabelText(/skill/i);
    await user.selectOptions(skillSelect, 'code-review');

    const cronInput = screen.getByPlaceholderText(/minute hour day/i);
    await user.type(cronInput, '0 9 * * *');

    // Submit form
    const submitButton = screen.getByRole('button', { name: /create task/i });
    await user.click(submitButton);

    // Button should be disabled while submitting
    expect(submitButton).toBeDisabled();
    expect(screen.getByText(/creating/i)).toBeInTheDocument();
  });

  it('displays error message on submit failure', async () => {
    const user = userEvent.setup();
    const errorMessage = 'Failed to create task: Network error';
    mockOnSubmit.mockRejectedValueOnce(new Error(errorMessage));

    render(<TaskForm onSubmit={mockOnSubmit} />);

    // Fill in minimum required fields
    const skillSelect = screen.getByLabelText(/skill/i);
    await user.selectOptions(skillSelect, 'code-review');

    const cronInput = screen.getByPlaceholderText(/minute hour day/i);
    await user.type(cronInput, '0 9 * * *');

    // Submit form
    const submitButton = screen.getByRole('button', { name: /create task/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/failed to create task/i)).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  it('updates parameters example when skill changes', async () => {
    const user = userEvent.setup();
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const skillSelect = screen.getByLabelText(/skill/i);
    await user.selectOptions(skillSelect, 'code-review');

    const jsonEditor = screen.getByTestId('code-mirror');
    await waitFor(() => {
      expect(jsonEditor).toHaveValue(expect.stringContaining('files'));
    });
  });
});
