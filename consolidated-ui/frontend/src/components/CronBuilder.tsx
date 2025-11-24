import React, { useState, useEffect } from 'react';
import { CRON_PRESETS, getNextRunTimes } from '../validation/taskSchema';

interface CronBuilderProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
}

/**
 * CronBuilder - Visual cron schedule builder with presets and preview
 *
 * Features:
 * - Preset selection for common schedules
 * - Custom cron expression input
 * - Real-time validation
 * - Preview of next 5 execution times
 */
export const CronBuilder: React.FC<CronBuilderProps> = ({ value, onChange, error }) => {
  const [selectedPreset, setSelectedPreset] = useState<string>('');
  const [customValue, setCustomValue] = useState<string>(value);
  const [nextRuns, setNextRuns] = useState<Date[]>([]);

  // Update next run times when value changes
  useEffect(() => {
    if (value) {
      const times = getNextRunTimes(value, 5);
      setNextRuns(times);
    } else {
      setNextRuns([]);
    }
  }, [value]);

  // Handle preset selection
  const handlePresetChange = (presetValue: string) => {
    setSelectedPreset(presetValue);
    if (presetValue !== '') {
      onChange(presetValue);
      setCustomValue(presetValue);
    }
  };

  // Handle custom input
  const handleCustomChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setCustomValue(newValue);
    onChange(newValue);
    setSelectedPreset(''); // Clear preset when typing custom
  };

  // Check if current value matches a preset
  useEffect(() => {
    const matchingPreset = CRON_PRESETS.find(p => p.value === value);
    if (matchingPreset) {
      setSelectedPreset(matchingPreset.value);
    }
  }, [value]);

  const formatDate = (date: Date) => {
    return date.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    });
  };

  return (
    <div className="space-y-4">
      {/* Preset Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Quick Presets
        </label>
        <div className="grid grid-cols-2 gap-2">
          {CRON_PRESETS.map((preset) => (
            <button
              key={preset.label}
              type="button"
              onClick={() => handlePresetChange(preset.value)}
              className={`
                px-3 py-2 text-sm rounded-md border transition-colors text-left
                ${
                  selectedPreset === preset.value
                    ? 'bg-blue-50 border-blue-500 text-blue-700'
                    : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                }
              `}
            >
              <div className="font-medium">{preset.label}</div>
              <div className="text-xs text-gray-500">{preset.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Custom Cron Expression */}
      <div>
        <label htmlFor="cron-custom" className="block text-sm font-medium text-gray-700 mb-2">
          Cron Expression
        </label>
        <input
          id="cron-custom"
          type="text"
          value={customValue}
          onChange={handleCustomChange}
          placeholder="* * * * * (minute hour day month weekday)"
          className={`
            w-full px-3 py-2 border rounded-md font-mono text-sm
            ${error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-blue-500'}
            focus:outline-none focus:ring-2
          `}
        />
        {error && (
          <p className="mt-1 text-sm text-red-600">{error}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          Format: minute (0-59) hour (0-23) day (1-31) month (1-12) weekday (0-6, 0=Sunday)
        </p>
      </div>

      {/* Next Run Times Preview */}
      {nextRuns.length > 0 && !error && (
        <div className="bg-gray-50 rounded-md p-3 border border-gray-200">
          <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
            <svg className="w-4 h-4 mr-1.5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Next 5 Executions
          </h4>
          <ul className="space-y-1">
            {nextRuns.map((date, index) => (
              <li key={index} className="text-xs text-gray-600 font-mono flex items-center">
                <span className="text-gray-400 mr-2">{index + 1}.</span>
                {formatDate(date)}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Cron Syntax Help */}
      <details className="text-sm">
        <summary className="cursor-pointer text-blue-600 hover:text-blue-700 font-medium">
          Cron Expression Syntax Help
        </summary>
        <div className="mt-2 space-y-2 text-gray-600 bg-blue-50 p-3 rounded border border-blue-200">
          <p><strong>Special Characters:</strong></p>
          <ul className="list-disc list-inside space-y-1 ml-2">
            <li><code className="bg-white px-1 rounded">*</code> - any value</li>
            <li><code className="bg-white px-1 rounded">,</code> - value list separator (e.g., 1,3,5)</li>
            <li><code className="bg-white px-1 rounded">-</code> - range of values (e.g., 1-5)</li>
            <li><code className="bg-white px-1 rounded">/</code> - step values (e.g., */15 = every 15)</li>
          </ul>
          <p className="mt-2"><strong>Examples:</strong></p>
          <ul className="list-disc list-inside space-y-1 ml-2">
            <li><code className="bg-white px-1 rounded">0 */2 * * *</code> - Every 2 hours at minute 0</li>
            <li><code className="bg-white px-1 rounded">30 9 * * 1-5</code> - 9:30 AM on weekdays</li>
            <li><code className="bg-white px-1 rounded">0 0 1,15 * *</code> - 12 AM on 1st and 15th of month</li>
          </ul>
        </div>
      </details>
    </div>
  );
};
