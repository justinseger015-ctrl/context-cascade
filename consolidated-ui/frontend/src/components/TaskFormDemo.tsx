import React, { useState } from 'react';
import { TaskForm } from './TaskForm';
import { TaskFormData } from '../validation/taskSchema';

/**
 * TaskFormDemo - Demo page showcasing the TaskForm component
 *
 * This is a temporary demo component for development and testing.
 * In production, TaskForm will be integrated into the main dashboard.
 */
export const TaskFormDemo: React.FC = () => {
  const [showForm, setShowForm] = useState(true);
  const [lastSubmission, setLastSubmission] = useState<TaskFormData | null>(null);

  const handleSubmit = async (data: TaskFormData) => {
    console.log('Task submitted:', data);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    setLastSubmission(data);
    setShowForm(false);

    // In production, this would:
    // 1. Call POST /api/v1/tasks
    // 2. Update Zustand store optimistically
    // 3. Handle success/error states
  };

  const handleCancel = () => {
    setShowForm(false);
  };

  const handleReset = () => {
    setLastSubmission(null);
    setShowForm(true);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Task Creation Form</h1>
          <p className="mt-2 text-gray-600">
            Create scheduled tasks for automated skill execution
          </p>
        </div>

        {/* Form Container */}
        {showForm ? (
          <div className="bg-white rounded-lg shadow-md p-6">
            <TaskForm onSubmit={handleSubmit} onCancel={handleCancel} />
          </div>
        ) : (
          <div className="space-y-6">
            {/* Success Message */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <div className="flex items-start">
                <svg className="w-6 h-6 text-green-600 mt-0.5 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <h3 className="text-lg font-medium text-green-900">Task Created Successfully!</h3>
                  <p className="mt-1 text-sm text-green-700">
                    Your scheduled task has been created and will run according to the specified schedule.
                  </p>
                </div>
              </div>
            </div>

            {/* Submitted Data Preview */}
            {lastSubmission && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Submitted Data</h3>
                <div className="space-y-3">
                  <div>
                    <span className="text-sm font-medium text-gray-500">Skill:</span>
                    <p className="text-gray-900">{lastSubmission.skillName}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">Schedule:</span>
                    <p className="text-gray-900 font-mono text-sm">{lastSubmission.cronSchedule}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">Parameters:</span>
                    <pre className="mt-1 bg-gray-50 p-3 rounded border border-gray-200 text-sm overflow-x-auto">
                      {JSON.stringify(JSON.parse(lastSubmission.parameters), null, 2)}
                    </pre>
                  </div>
                  {lastSubmission.projectId && (
                    <div>
                      <span className="text-sm font-medium text-gray-500">Project:</span>
                      <p className="text-gray-900">{lastSubmission.projectId}</p>
                    </div>
                  )}
                  {lastSubmission.description && (
                    <div>
                      <span className="text-sm font-medium text-gray-500">Description:</span>
                      <p className="text-gray-900">{lastSubmission.description}</p>
                    </div>
                  )}
                  <div>
                    <span className="text-sm font-medium text-gray-500">Status:</span>
                    <p className="text-gray-900">
                      {lastSubmission.enabled ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          Enabled
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          Disabled
                        </span>
                      )}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center space-x-3">
              <button
                onClick={handleReset}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Create Another Task
              </button>
              <a
                href="/"
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Back to Dashboard
              </a>
            </div>
          </div>
        )}

        {/* Feature Documentation */}
        <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">✨ Features Implemented</h3>
          <ul className="space-y-2 text-sm text-blue-800">
            <li className="flex items-start">
              <svg className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>Skill Dropdown:</strong> Categorized selection from .claude/skills directory</span>
            </li>
            <li className="flex items-start">
              <svg className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>Visual Cron Builder:</strong> 12 presets + custom input with validation</span>
            </li>
            <li className="flex items-start">
              <svg className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>Next Run Preview:</strong> Shows next 5 execution times in real-time</span>
            </li>
            <li className="flex items-start">
              <svg className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>CodeMirror Editor:</strong> Syntax highlighting for JSON parameters</span>
            </li>
            <li className="flex items-start">
              <svg className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>React Hook Form + Zod:</strong> Type-safe validation with inline errors</span>
            </li>
            <li className="flex items-start">
              <svg className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>Optimistic UI:</strong> Ready for Zustand integration (P3_T1)</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
