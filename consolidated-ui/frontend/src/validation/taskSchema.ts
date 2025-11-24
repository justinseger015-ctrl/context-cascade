import { z } from 'zod';
import cronParser from 'cron-parser';

/**
 * Validates cron expression format and parseability
 */
const cronValidator = z.string().refine(
  (value) => {
    try {
      cronParser.parseExpression(value);
      return true;
    } catch (error) {
      return false;
    }
  },
  {
    message: 'Invalid cron expression. Use format: "* * * * *" (minute hour day month weekday)',
  }
);

/**
 * Validates JSON string format
 */
const jsonValidator = z.string().refine(
  (value) => {
    if (!value.trim()) return true; // Empty is valid (optional parameters)
    try {
      JSON.parse(value);
      return true;
    } catch (error) {
      return false;
    }
  },
  {
    message: 'Invalid JSON format',
  }
);

/**
 * Task creation form schema with comprehensive validation
 */
export const taskFormSchema = z.object({
  skillName: z.string().min(1, 'Skill name is required'),
  cronSchedule: cronValidator,
  parameters: jsonValidator,
  projectId: z.string().optional(),
  description: z.string().optional(),
  enabled: z.boolean().default(true),
});

export type TaskFormData = z.infer<typeof taskFormSchema>;

/**
 * Generates next N execution times for a cron expression
 */
export function getNextRunTimes(cronExpression: string, count: number = 5): Date[] {
  try {
    const interval = cronParser.parseExpression(cronExpression);
    const times: Date[] = [];

    for (let i = 0; i < count; i++) {
      times.push(interval.next().toDate());
    }

    return times;
  } catch (error) {
    return [];
  }
}

/**
 * Common cron presets for quick selection
 */
export const CRON_PRESETS = [
  { label: 'Every minute', value: '* * * * *', description: 'Runs every minute' },
  { label: 'Every 5 minutes', value: '*/5 * * * *', description: 'Runs every 5 minutes' },
  { label: 'Every 15 minutes', value: '*/15 * * * *', description: 'Runs every 15 minutes' },
  { label: 'Every 30 minutes', value: '*/30 * * * *', description: 'Runs every 30 minutes' },
  { label: 'Every hour', value: '0 * * * *', description: 'Runs at minute 0 of every hour' },
  { label: 'Every 6 hours', value: '0 */6 * * *', description: 'Runs at minute 0 every 6 hours' },
  { label: 'Daily at 9am', value: '0 9 * * *', description: 'Runs at 09:00 every day' },
  { label: 'Daily at midnight', value: '0 0 * * *', description: 'Runs at 00:00 every day' },
  { label: 'Weekly (Monday 9am)', value: '0 9 * * 1', description: 'Runs at 09:00 every Monday' },
  { label: 'Monthly (1st at 9am)', value: '0 9 1 * *', description: 'Runs at 09:00 on day 1 of every month' },
  { label: 'Weekdays at 9am', value: '0 9 * * 1-5', description: 'Runs at 09:00 Monday through Friday' },
  { label: 'Custom', value: '', description: 'Enter your own cron expression' },
] as const;

/**
 * Default empty parameters object
 */
export const DEFAULT_PARAMETERS = '{}';

/**
 * Example parameters for common skill types
 */
export const PARAMETER_EXAMPLES = {
  'code-review': '{\n  "files": ["src/**/*.ts"],\n  "severity": "high"\n}',
  'testing': '{\n  "coverage": 80,\n  "timeout": 30000\n}',
  'deployment': '{\n  "environment": "staging",\n  "branch": "main"\n}',
  default: '{}',
};
