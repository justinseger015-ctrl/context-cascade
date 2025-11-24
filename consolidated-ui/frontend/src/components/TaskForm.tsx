import React, { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import CodeMirror from '@uiw/react-codemirror';
import { json } from '@codemirror/lang-json';
import { taskFormSchema, TaskFormData, DEFAULT_PARAMETERS, PARAMETER_EXAMPLES } from '../validation/taskSchema';
import { CronBuilder } from './CronBuilder';
import { useSkills, groupSkillsByCategory } from '../hooks/useSkills';

interface TaskFormProps {
  onSubmit: (data: TaskFormData) => Promise<void>;
  onCancel?: () => void;
}

/**
 * TaskForm - Comprehensive task creation form with validation
 *
 * Features:
 * - Skill selection from .claude/skills directory
 * - Visual cron builder with presets
 * - CodeMirror JSON editor for parameters
 * - Project assignment
 * - React Hook Form + Zod validation
 * - Optimistic UI updates (placeholder for Zustand integration)
 * - Inline error messages
 */
export const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, onCancel }) => {
  const { skills, loading: skillsLoading } = useSkills();
  const groupedSkills = groupSkillsByCategory(skills);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    control,
    watch,
    setValue,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(taskFormSchema),
    defaultValues: {
      skillName: '',
      cronSchedule: '',
      parameters: DEFAULT_PARAMETERS,
      projectId: '',
      description: '',
      enabled: true,
    } as TaskFormData,
  });

  const selectedSkill = watch('skillName');
  const parametersValue = watch('parameters');

  // Update parameters example when skill changes
  React.useEffect(() => {
    if (selectedSkill && parametersValue === DEFAULT_PARAMETERS) {
      const exampleKey = selectedSkill.toLowerCase();
      const example = PARAMETER_EXAMPLES[exampleKey as keyof typeof PARAMETER_EXAMPLES] || PARAMETER_EXAMPLES.default;
      setValue('parameters', example);
    }
  }, [selectedSkill, parametersValue, setValue]);

  const handleFormSubmit = async (data: TaskFormData) => {
    try {
      setSubmitting(true);
      setSubmitError(null);

      // TODO: Optimistic UI update with Zustand (P3_T1 integration)
      // const tempTask = {
      //   id: `temp-${Date.now()}`,
      //   ...data,
      //   status: 'pending',
      //   createdAt: new Date().toISOString(),
      // };
      // useTaskStore.getState().addTask(tempTask);

      await onSubmit(data);

      // Success - form will be closed by parent
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Failed to create task');

      // TODO: Rollback optimistic update
      // useTaskStore.getState().removeTask(tempTask.id);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      {/* Skill Selection */}
      <div>
        <label htmlFor="skillName" className="block text-sm font-medium text-gray-700 mb-2">
          Skill <span className="text-red-500">*</span>
        </label>
        {skillsLoading ? (
          <div className="flex items-center space-x-2 text-gray-500">
            <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <span className="text-sm">Loading skills...</span>
          </div>
        ) : (
          <select
            id="skillName"
            {...register('skillName')}
            className={`
              w-full px-3 py-2 border rounded-md
              ${errors.skillName ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}
              focus:outline-none focus:ring-2
            `}
          >
            <option value="">Select a skill...</option>
            {Object.entries(groupedSkills).map(([category, categorySkills]) => (
              <optgroup key={category} label={category}>
                {categorySkills.map((skill) => (
                  <option key={skill.path} value={skill.name}>
                    {skill.name}
                  </option>
                ))}
              </optgroup>
            ))}
          </select>
        )}
        {errors.skillName && (
          <p className="mt-1 text-sm text-red-600">{errors.skillName.message}</p>
        )}
      </div>

      {/* Cron Schedule Builder */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Schedule <span className="text-red-500">*</span>
        </label>
        <Controller
          name="cronSchedule"
          control={control}
          render={({ field }) => (
            <CronBuilder
              value={field.value}
              onChange={field.onChange}
              error={errors.cronSchedule?.message}
            />
          )}
        />
      </div>

      {/* Parameters JSON Editor */}
      <div>
        <label htmlFor="parameters" className="block text-sm font-medium text-gray-700 mb-2">
          Parameters (JSON)
        </label>
        <Controller
          name="parameters"
          control={control}
          render={({ field }) => (
            <div className="border rounded-md overflow-hidden">
              <CodeMirror
                value={field.value}
                height="200px"
                extensions={[json()]}
                onChange={field.onChange}
                className={errors.parameters ? 'border-2 border-red-500' : ''}
                theme="light"
                basicSetup={{
                  lineNumbers: true,
                  highlightActiveLineGutter: true,
                  highlightSpecialChars: true,
                  foldGutter: true,
                  bracketMatching: true,
                  closeBrackets: true,
                  autocompletion: true,
                }}
              />
            </div>
          )}
        />
        {errors.parameters && (
          <p className="mt-1 text-sm text-red-600">{errors.parameters.message}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          Enter task-specific parameters as JSON. Leave empty {'{}}'} if no parameters needed.
        </p>
      </div>

      {/* Project Assignment */}
      <div>
        <label htmlFor="projectId" className="block text-sm font-medium text-gray-700 mb-2">
          Project (Optional)
        </label>
        <select
          id="projectId"
          {...register('projectId')}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">No project assignment</option>
          {/* TODO: Populate from Zustand projects store (P3_T1) */}
          <option value="project-1">Project Alpha</option>
          <option value="project-2">Project Beta</option>
          <option value="project-3">Project Gamma</option>
        </select>
      </div>

      {/* Description */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
          Description (Optional)
        </label>
        <textarea
          id="description"
          {...register('description')}
          rows={3}
          placeholder="Brief description of what this task does..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Enabled Toggle */}
      <div className="flex items-center">
        <input
          id="enabled"
          type="checkbox"
          {...register('enabled')}
          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
        />
        <label htmlFor="enabled" className="ml-2 block text-sm text-gray-700">
          Enable task immediately
        </label>
      </div>

      {/* Submit Error */}
      {submitError && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3 flex items-start">
          <svg className="w-5 h-5 text-red-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h4 className="text-sm font-medium text-red-800">Failed to create task</h4>
            <p className="text-sm text-red-700 mt-1">{submitError}</p>
          </div>
        </div>
      )}

      {/* Form Actions */}
      <div className="flex items-center justify-end space-x-3 pt-4 border-t border-gray-200">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={submitting}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          disabled={submitting || skillsLoading}
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
        >
          {submitting ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Creating...
            </>
          ) : (
            'Create Task'
          )}
        </button>
      </div>
    </form>
  );
};
