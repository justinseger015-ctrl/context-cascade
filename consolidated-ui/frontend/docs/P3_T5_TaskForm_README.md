# P3_T5 - Task Creation Form with Validation

## Overview

Comprehensive task creation form for scheduling automated skill execution with full validation, visual cron builder, and JSON parameter editor.

## Features Implemented

### ✅ Core Features

1. **Skill Selection Dropdown**
   - Categorized dropdown populated from `.claude/skills` directory
   - Mock implementation with 11+ skills across 6 categories
   - Ready for backend API integration (`GET /api/v1/skills`)

2. **Visual Cron Builder**
   - 12 preset schedules (Every minute, Every hour, Daily at 9am, etc.)
   - Custom cron expression input with live validation
   - Real-time preview of next 5 execution times
   - Inline syntax help with examples
   - Auto-formatted date display

3. **JSON Parameter Editor**
   - CodeMirror integration with JSON syntax highlighting
   - Real-time JSON validation
   - Auto-population of skill-specific examples
   - Line numbers, bracket matching, auto-completion
   - 200px height with scrollable overflow

4. **Project Assignment**
   - Dropdown for project selection (placeholder for P3_T1 Zustand integration)
   - Currently populated with mock projects
   - Optional field

5. **Form Validation**
   - React Hook Form + Zod schema validation
   - Client-side validation for:
     - Required fields (skill name, cron schedule)
     - Cron expression format (validated with `cron-parser`)
     - JSON syntax (validated with `JSON.parse`)
   - Inline error messages with red borders
   - Validation triggers on submit and field blur

6. **Optimistic UI Updates**
   - Placeholder implementation ready for Zustand integration (P3_T1)
   - TODO comments marking integration points
   - Error rollback mechanism prepared

## File Structure

```
frontend/src/
├── components/
│   ├── TaskForm.tsx              # Main task creation form
│   ├── CronBuilder.tsx           # Visual cron schedule builder
│   ├── TaskFormDemo.tsx          # Demo page for testing
│   ├── index.ts                  # Component exports
│   └── __tests__/
│       ├── TaskForm.test.tsx     # TaskForm component tests
│       └── CronBuilder.test.tsx  # CronBuilder component tests
├── validation/
│   ├── taskSchema.ts             # Zod validation schema
│   └── __tests__/
│       └── taskSchema.test.ts    # Schema validation tests
├── hooks/
│   └── useSkills.ts              # Hook to fetch available skills
└── types/
    ├── task.types.ts             # Task-related TypeScript types
    └── index.ts                  # Centralized type exports
```

## Components

### TaskForm

**Props:**
```typescript
interface TaskFormProps {
  onSubmit: (data: TaskFormData) => Promise<void>;
  onCancel?: () => void;
}
```

**Usage:**
```tsx
import { TaskForm } from './components/TaskForm';

function App() {
  const handleSubmit = async (data: TaskFormData) => {
    // POST /api/v1/tasks
    await fetch('/api/v1/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  return <TaskForm onSubmit={handleSubmit} />;
}
```

### CronBuilder

**Props:**
```typescript
interface CronBuilderProps {
  value: string;
  onChange: (value: string) => void;
  error?: string;
}
```

**Usage:**
```tsx
import { CronBuilder } from './components/CronBuilder';

function MyForm() {
  const [cron, setCron] = useState('0 9 * * *');
  const [error, setError] = useState<string>();

  return (
    <CronBuilder
      value={cron}
      onChange={setCron}
      error={error}
    />
  );
}
```

## Validation Schema

```typescript
export const taskFormSchema = z.object({
  skillName: z.string().min(1, 'Skill name is required'),
  cronSchedule: cronValidator, // Custom cron expression validator
  parameters: jsonValidator,   // Custom JSON validator
  projectId: z.string().optional(),
  description: z.string().optional(),
  enabled: z.boolean().default(true),
});

export type TaskFormData = z.infer<typeof taskFormSchema>;
```

## Cron Presets

| Label | Expression | Description |
|-------|-----------|-------------|
| Every minute | `* * * * *` | Runs every minute |
| Every 5 minutes | `*/5 * * * *` | Runs every 5 minutes |
| Every hour | `0 * * * *` | Runs at minute 0 of every hour |
| Daily at 9am | `0 9 * * *` | Runs at 09:00 every day |
| Weekly (Monday 9am) | `0 9 * * 1` | Runs at 09:00 every Monday |
| Monthly (1st at 9am) | `0 9 1 * *` | Runs at 09:00 on day 1 of month |
| Weekdays at 9am | `0 9 * * 1-5` | Runs at 09:00 Monday-Friday |

## API Integration Points

### Skills Endpoint (TODO)

**Backend needs to implement:**
```typescript
GET /api/v1/skills

Response:
{
  skills: [
    {
      name: "code-review-assistant",
      path: "code-review-assistant",
      category: "Quality"
    }
  ]
}
```

**Current implementation:**
- `useSkills` hook in `src/hooks/useSkills.ts`
- Currently returns mock data
- Replace mock with actual API call when backend ready

### Task Creation Endpoint

**Expected API:**
```typescript
POST /api/v1/tasks

Request:
{
  skillName: string;
  cronSchedule: string;
  parameters: string; // JSON string
  projectId?: string;
  description?: string;
  enabled: boolean;
}

Response:
{
  task: {
    id: string;
    ...requestFields,
    status: 'pending' | 'running' | 'completed' | 'failed',
    createdAt: string;
    updatedAt: string;
    nextRun: string;
  }
}
```

## Zustand Integration (P3_T1 Dependency)

**TODO comments mark integration points:**

```typescript
// TaskForm.tsx line 96-102
// TODO: Optimistic UI update with Zustand (P3_T1 integration)
// const tempTask = {
//   id: `temp-${Date.now()}`,
//   ...data,
//   status: 'pending',
//   createdAt: new Date().toISOString(),
// };
// useTaskStore.getState().addTask(tempTask);
```

**Expected Zustand store:**
```typescript
interface TaskStore {
  tasks: ScheduledTask[];
  addTask: (task: ScheduledTask) => void;
  removeTask: (id: string) => void;
  updateTask: (id: string, updates: Partial<ScheduledTask>) => void;
}
```

## Testing

### Run Tests

```bash
npm test -- --testPathPatterns="TaskForm|CronBuilder|taskSchema"
```

### Test Coverage

- **TaskForm.test.tsx**: 10 test cases
  - Form rendering
  - Validation errors
  - Cron validation
  - JSON validation
  - Form submission
  - Cancel handling
  - Submit button states
  - Error display

- **CronBuilder.test.tsx**: 11 test cases
  - Preset buttons
  - Custom input
  - onChange callbacks
  - Preset selection
  - Error messages
  - Next run times preview
  - Syntax help

- **taskSchema.test.ts**: 15 test cases
  - Schema validation
  - Cron expression validation
  - JSON validation
  - Optional fields
  - Next run times calculation
  - Preset validation

## Development Demo

**Run demo page:**

```tsx
// In App.tsx or separate route
import { TaskFormDemo } from './components/TaskFormDemo';

function App() {
  return <TaskFormDemo />;
}
```

**Demo features:**
- Complete form with all validation
- Success state with submitted data preview
- Error state simulation
- Feature documentation panel

## Dependencies

**New packages installed:**

```json
{
  "react-hook-form": "^7.x",
  "zod": "^3.x",
  "@hookform/resolvers": "^3.x",
  "cron-parser": "^4.x",
  "@uiw/react-codemirror": "^4.x",
  "@codemirror/lang-json": "^6.x"
}
```

## TypeScript Types

**Exported types:**

```typescript
// Component types
export type { TaskFormData } from '../validation/taskSchema';
export type { Skill } from '../hooks/useSkills';

// API types
export type {
  ScheduledTask,
  TaskExecution,
  CreateTaskPayload,
  UpdateTaskPayload,
  TaskListResponse,
  TaskResponse,
  TaskApiError,
} from './task.types';
```

## Accessibility

- ✅ Semantic HTML (`<label>`, `<select>`, `<textarea>`, `<button>`)
- ✅ ARIA labels where needed
- ✅ Keyboard navigation support
- ✅ Focus management
- ✅ Error announcements
- ✅ Color contrast (WCAG AA compliant)

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ React 18+
- ✅ TypeScript 5.6+

## Future Enhancements

1. **Backend Integration**
   - Replace mock skills with API call
   - Implement actual task creation endpoint
   - Add loading states for API calls

2. **Zustand Store Integration (P3_T1)**
   - Connect to tasksSlice
   - Implement optimistic updates
   - Add rollback on error

3. **Additional Features**
   - Task templates
   - Bulk task creation
   - Schedule conflict detection
   - Task history/logs
   - Advanced cron builder (visual time picker)

## Deliverables Checklist

- [x] TaskForm.tsx component with React Hook Form + Zod
- [x] CronBuilder.tsx with presets and validation
- [x] taskSchema.ts with Zod validation
- [x] Skill name dropdown (mock data ready for API)
- [x] CodeMirror JSON editor with syntax highlighting
- [x] Project dropdown (placeholder for Zustand)
- [x] Cron expression validation with next 5 run times preview
- [x] JSON syntax validation with error messages
- [x] Optimistic UI update preparation (TODO comments)
- [x] Inline error messages throughout form
- [x] Component tests (TaskForm, CronBuilder, taskSchema)
- [x] TypeScript types (task.types.ts)
- [x] Demo page (TaskFormDemo.tsx)
- [x] Component exports (index.ts)
- [x] Comprehensive documentation (this README)

## Notes

- All components follow React best practices (hooks, memoization)
- Form state managed by React Hook Form for performance
- Validation happens on submit and blur
- Next run times calculated in real-time using `cron-parser`
- CodeMirror provides professional JSON editing experience
- Ready for P3_T1 Zustand integration (marked with TODO comments)
- Tests cover happy path and error scenarios
- TypeScript strict mode compliance

## Support

For issues or questions:
- Check component tests for usage examples
- Review TaskFormDemo for complete implementation
- See inline TODO comments for integration points
