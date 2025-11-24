import { taskFormSchema, getNextRunTimes, CRON_PRESETS } from '../taskSchema';

describe('taskFormSchema', () => {
  it('validates correct task data', () => {
    const validData = {
      skillName: 'code-review',
      cronSchedule: '0 9 * * *',
      parameters: '{"key": "value"}',
      projectId: 'project-1',
      description: 'Test task',
      enabled: true,
    };

    const result = taskFormSchema.safeParse(validData);
    expect(result.success).toBe(true);
  });

  it('rejects missing required fields', () => {
    const invalidData = {
      parameters: '{}',
    };

    const result = taskFormSchema.safeParse(invalidData);
    expect(result.success).toBe(false);
    if (!result.success) {
      expect(result.error.issues.some(i => i.path[0] === 'skillName')).toBe(true);
      expect(result.error.issues.some(i => i.path[0] === 'cronSchedule')).toBe(true);
    }
  });

  it('validates cron expression format', () => {
    const invalidCron = {
      skillName: 'test',
      cronSchedule: 'invalid cron',
      parameters: '{}',
    };

    const result = taskFormSchema.safeParse(invalidCron);
    expect(result.success).toBe(false);
    if (!result.success) {
      const cronError = result.error.issues.find(i => i.path[0] === 'cronSchedule');
      expect(cronError?.message).toContain('Invalid cron expression');
    }
  });

  it('validates JSON parameters', () => {
    const invalidJson = {
      skillName: 'test',
      cronSchedule: '0 9 * * *',
      parameters: '{invalid json}',
    };

    const result = taskFormSchema.safeParse(invalidJson);
    expect(result.success).toBe(false);
    if (!result.success) {
      const jsonError = result.error.issues.find(i => i.path[0] === 'parameters');
      expect(jsonError?.message).toContain('Invalid JSON');
    }
  });

  it('allows empty parameters', () => {
    const emptyParams = {
      skillName: 'test',
      cronSchedule: '0 9 * * *',
      parameters: '',
    };

    const result = taskFormSchema.safeParse(emptyParams);
    expect(result.success).toBe(true);
  });

  it('allows optional fields to be undefined', () => {
    const minimalData = {
      skillName: 'test',
      cronSchedule: '0 9 * * *',
      parameters: '{}',
    };

    const result = taskFormSchema.safeParse(minimalData);
    expect(result.success).toBe(true);
  });
});

describe('getNextRunTimes', () => {
  it('returns next 5 run times by default', () => {
    const times = getNextRunTimes('0 9 * * *');
    expect(times).toHaveLength(5);
  });

  it('returns specified number of run times', () => {
    const times = getNextRunTimes('0 9 * * *', 3);
    expect(times).toHaveLength(3);
  });

  it('returns dates in chronological order', () => {
    const times = getNextRunTimes('0 9 * * *', 5);

    for (let i = 1; i < times.length; i++) {
      expect(times[i]?.getTime()).toBeGreaterThan(times[i - 1].getTime());
    }
  });

  it('returns empty array for invalid cron expression', () => {
    const times = getNextRunTimes('invalid');
    expect(times).toHaveLength(0);
  });

  it('calculates correct times for hourly schedule', () => {
    const times = getNextRunTimes('0 * * * *', 2);
    const timeDiff = (times[1]?.getTime() ?? 0) - (times[0]?.getTime() ?? 0);
    expect(timeDiff).toBe(60 * 60 * 1000); // 1 hour in milliseconds
  });

  it('calculates correct times for daily schedule', () => {
    const times = getNextRunTimes('0 9 * * *', 2);

    // Both should be at 9:00 AM
    expect(times[0]?.getHours()).toBe(9);
    expect(times[1]?.getHours()).toBe(9);

    // Should be 24 hours apart
    const timeDiff = (times[1]?.getTime() ?? 0) - (times[0]?.getTime() ?? 0);
    expect(timeDiff).toBe(24 * 60 * 60 * 1000);
  });
});

describe('CRON_PRESETS', () => {
  it('contains all expected presets', () => {
    const presetLabels = CRON_PRESETS.map(p => p.label);

    expect(presetLabels).toContain('Every minute');
    expect(presetLabels).toContain('Every hour');
    expect(presetLabels).toContain('Daily at 9am');
    expect(presetLabels).toContain('Weekly (Monday 9am)');
    expect(presetLabels).toContain('Custom');
  });

  it('all presets have valid cron expressions', () => {
    const invalidPresets = CRON_PRESETS.filter(
      preset => preset.value !== '' && getNextRunTimes(preset.value, 1).length === 0
    );

    expect(invalidPresets).toHaveLength(0);
  });

  it('custom preset has empty value', () => {
    const customPreset = CRON_PRESETS.find(p => p.label === 'Custom');
    expect(customPreset?.value).toBe('');
  });
});
