import React from 'react';
import type { TaskStatus, TaskFilters as TaskFiltersType } from '../types';

interface TaskFiltersProps {
  filters: TaskFiltersType;
  onFilterChange: (filters: TaskFiltersType) => void;
  availableSkills: string[];
}

const statusOptions: TaskStatus[] = ['pending', 'running', 'completed', 'failed'];

const statusColors: Record<TaskStatus, string> = {
  pending: 'bg-gray-200 text-gray-800',
  running: 'bg-blue-200 text-blue-800',
  completed: 'bg-green-200 text-green-800',
  failed: 'bg-red-200 text-red-800',
};

export const TaskFilters: React.FC<TaskFiltersProps> = ({
  filters,
  onFilterChange,
  availableSkills,
}) => {
  const toggleStatus = (status: TaskStatus) => {
    const currentStatuses = filters.status || [];
    const newStatuses = currentStatuses.includes(status)
      ? currentStatuses.filter((s) => s !== status)
      : [...currentStatuses, status];

    onFilterChange({
      ...filters,
      status: newStatuses.length > 0 ? newStatuses : undefined,
    });
  };

  const toggleSkill = (skill: string) => {
    const currentSkills = filters.skill_name || [];
    const newSkills = currentSkills.includes(skill)
      ? currentSkills.filter((s) => s !== skill)
      : [...currentSkills, skill];

    onFilterChange({
      ...filters,
      skill_name: newSkills.length > 0 ? newSkills : undefined,
    });
  };

  const clearFilters = () => {
    onFilterChange({});
  };

  const hasActiveFilters = (filters.status?.length || 0) > 0 || (filters.skill_name?.length || 0) > 0;

  return (
    <div className="bg-white rounded-lg shadow p-4 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="text-sm text-blue-600 hover:text-blue-800 transition-colors"
          >
            Clear all
          </button>
        )}
      </div>

      {/* Status Filters */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
        <div className="flex flex-wrap gap-2">
          {statusOptions.map((status) => {
            const isActive = filters.status?.includes(status);
            return (
              <button
                key={status}
                onClick={() => toggleStatus(status)}
                className={`px-3 py-1.5 rounded-full text-sm font-medium transition-all ${
                  isActive
                    ? statusColors[status]
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            );
          })}
        </div>
      </div>

      {/* Skill Filters */}
      {availableSkills.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Skills</label>
          <div className="flex flex-wrap gap-2">
            {availableSkills.map((skill) => {
              const isActive = filters.skill_name?.includes(skill);
              return (
                <button
                  key={skill}
                  onClick={() => toggleSkill(skill)}
                  className={`px-3 py-1.5 rounded-full text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-purple-200 text-purple-800'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {skill}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
