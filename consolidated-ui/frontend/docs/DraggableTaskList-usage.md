# DraggableTaskList Component - Usage Guide

## Overview
The `DraggableTaskList` component provides a fully accessible drag-and-drop interface for reordering tasks within a project. It implements WCAG 2.1 AA compliance with complete keyboard navigation and screen reader support.

## Features
✅ **Drag-and-drop** with mouse or touch
✅ **Keyboard navigation** (Space to grab, Arrow keys to move, Space to drop)
✅ **Screen reader support** with live announcements
✅ **Visual feedback** - drag handles, drop indicators, focus rings
✅ **Optimistic updates** with automatic rollback on error
✅ **Zustand integration** for state management
✅ **API persistence** ready (hook provided for backend calls)

---

## Installation

Dependencies are already installed in `package.json`:
```json
{
  "@dnd-kit/core": "^6.3.1",
  "@dnd-kit/sortable": "^10.0.0",
  "@dnd-kit/utilities": "^3.2.2"
}
```

---

## Basic Usage

```tsx
import { DraggableTaskList } from '../components/DraggableTaskList';
import { useProjectStore } from '../store/useProjectStore';

function ProjectDashboard() {
  const selectedProjectId = useProjectStore((state) => state.selectedProjectId);
  const getProjectTasks = useProjectStore((state) => state.getProjectTasks);
  const reorderTasks = useProjectStore((state) => state.reorderTasks);

  if (!selectedProjectId) return <div>Select a project</div>;

  const tasks = getProjectTasks(selectedProjectId);

  return (
    <DraggableTaskList
      projectId={selectedProjectId}
      tasks={tasks}
      onReorder={(reorderedTasks) => {
        // Optimistic update
        reorderTasks(selectedProjectId, reorderedTasks);
      }}
    />
  );
}
```

---

## Advanced Usage with API Persistence

```tsx
import { DraggableTaskList } from '../components/DraggableTaskList';
import { useProjectStore } from '../store/useProjectStore';
import { persistTaskOrder } from '../api/tasks'; // Your API module

function ProjectDashboard() {
  const selectedProjectId = useProjectStore((state) => state.selectedProjectId);
  const getProjectTasks = useProjectStore((state) => state.getProjectTasks);
  const reorderTasks = useProjectStore((state) => state.reorderTasks);

  if (!selectedProjectId) return <div>Select a project</div>;

  const tasks = getProjectTasks(selectedProjectId);

  const handleReorder = (reorderedTasks: Task[]) => {
    // Optimistic update
    reorderTasks(selectedProjectId, reorderedTasks);
  };

  const handleReorderComplete = async (reorderedTasks: Task[]) => {
    try {
      // Persist to backend API
      await persistTaskOrder(selectedProjectId, reorderedTasks.map(t => t.id));
      console.log('Task order persisted successfully');
    } catch (error) {
      console.error('Failed to persist task order:', error);
      // Zustand store will automatically rollback on error
      throw error; // Let useDragAndDrop hook handle rollback
    }
  };

  return (
    <DraggableTaskList
      projectId={selectedProjectId}
      tasks={tasks}
      onReorder={handleReorder}
      onReorderComplete={handleReorderComplete}
      className="max-w-4xl mx-auto"
    />
  );
}
```

---

## Props API

### DraggableTaskList

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `projectId` | `string` | ✅ | ID of the project containing these tasks |
| `tasks` | `Task[]` | ✅ | Array of tasks to display (will be sorted by `order` property) |
| `onReorder` | `(tasks: Task[]) => void` | ✅ | Callback fired immediately when tasks are reordered (optimistic update) |
| `onReorderComplete` | `(tasks: Task[]) => void` | ❌ | Optional callback fired after successful drop (for API persistence) |
| `className` | `string` | ❌ | Additional CSS classes for the task list container |

### Task Interface

```typescript
interface Task {
  id: string;
  projectId: string;
  title: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  skill_name: string;
  schedule?: string;
  next_run_at?: Date;
  last_run_at?: Date;
  assignee?: string;
  dueDate?: Date;
  order?: number; // REQUIRED for drag-and-drop ordering
  createdAt: Date;
  updatedAt: Date;
}
```

---

## Keyboard Navigation Reference

| Key | Action |
|-----|--------|
| **Tab** | Navigate to next drag handle |
| **Shift+Tab** | Navigate to previous drag handle |
| **Space** | Grab task (when focused on drag handle) |
| **Arrow Up** | Move grabbed task up (while dragging) |
| **Arrow Down** | Move grabbed task down (while dragging) |
| **Space** | Drop task at current position (while dragging) |
| **Escape** | Cancel drag and return task to original position |

---

## Screen Reader Announcements

The component announces the following events to screen readers:

1. **Grab**: "Picked up task: [Task Title]. Use arrow keys to move, Space to drop, Escape to cancel."
2. **Move**: "Moving [Task Title] over [Other Task Title]"
3. **Drop**: "Dropped [Task Title] at position 3 of 10"
4. **Cancel**: "Cancelled dragging [Task Title]. Returned to original position."
5. **Error**: "Failed to reorder task: [Task Title]. Changes reverted."

---

## Visual Feedback

### Priority Colors
- **Low**: Gray background (`bg-gray-100 border-gray-300`)
- **Medium**: Blue background (`bg-blue-50 border-blue-300`)
- **High**: Yellow background (`bg-yellow-50 border-yellow-400`)
- **Critical**: Red background (`bg-red-50 border-red-400`)

### Status Badges
- **Pending**: Gray badge (`bg-gray-500`)
- **Running**: Blue badge (`bg-blue-500`)
- **Completed**: Green badge (`bg-green-500`)
- **Failed**: Red badge (`bg-red-500`)

### Drag Indicators
- **Dragging**: Semi-transparent (opacity 0.5) with blue ring
- **Drop Target**: Blue dashed border overlay
- **Focus**: Blue ring (`ring-2 ring-blue-500`)

---

## Zustand Store Integration

### Adding Tasks
```typescript
const addTask = useProjectStore((state) => state.addTask);

// New tasks automatically get order assigned
addTask('project-123', {
  title: 'New Task',
  description: 'Task description',
  status: 'pending',
  priority: 'medium',
  skill_name: 'development',
});
```

### Updating Tasks
```typescript
const updateTask = useProjectStore((state) => state.updateTask);

updateTask('project-123', 'task-456', {
  status: 'completed',
  priority: 'high',
});
```

### Deleting Tasks
```typescript
const deleteTask = useProjectStore((state) => state.deleteTask);

deleteTask('project-123', 'task-456');
```

### Getting Tasks
```typescript
const getProjectTasks = useProjectStore((state) => state.getProjectTasks);

const tasks = getProjectTasks('project-123');
// Returns tasks sorted by order property
```

---

## Error Handling

### Automatic Rollback
If `onReorderComplete` throws an error, the component automatically:
1. Reverts tasks to previous order in Zustand store
2. Announces error to screen reader
3. Logs error to console

```typescript
const handleReorderComplete = async (reorderedTasks: Task[]) => {
  try {
    await api.persistTaskOrder(projectId, reorderedTasks);
  } catch (error) {
    // Automatic rollback triggered
    // Screen reader announces: "Failed to reorder task: [Task Title]. Changes reverted."
    throw error; // Required for rollback to work
  }
};
```

---

## Performance Considerations

### Large Lists
For lists with 50+ tasks, consider:
1. **Virtualization**: Use `react-window` or `react-virtuoso`
2. **Pagination**: Split tasks across multiple pages
3. **Lazy Loading**: Load tasks on scroll

### Debouncing API Calls
```typescript
import { debounce } from 'lodash';

const debouncedPersist = debounce(async (tasks: Task[]) => {
  await api.persistTaskOrder(projectId, tasks);
}, 1000);

const handleReorderComplete = (tasks: Task[]) => {
  debouncedPersist(tasks);
};
```

---

## Accessibility Testing

### Automated Tests
```bash
# Run component tests
npm test -- DraggableTaskList.test.tsx

# Run Lighthouse audit
npm run build
lighthouse http://localhost:3000/projects --view
```

### Manual Testing Checklist
- [ ] Tab to all drag handles
- [ ] Grab task with Space key
- [ ] Move task with Arrow keys
- [ ] Drop task with Space key
- [ ] Cancel with Escape key
- [ ] Test with NVDA screen reader
- [ ] Verify focus indicator visible
- [ ] Check color contrast (4.5:1 minimum)

See `docs/keyboard-navigation-tests.md` for comprehensive test cases.

---

## Troubleshooting

### Tasks Not Reordering
**Issue**: Drag-and-drop not working
**Solutions**:
1. Verify tasks have `order` property
2. Check `onReorder` callback is updating Zustand store
3. Ensure tasks are sorted by `order` before passing to component

### Keyboard Navigation Not Working
**Issue**: Space key not grabbing task
**Solutions**:
1. Ensure drag handle has `tabindex="0"`
2. Check focus is on drag handle (blue ring visible)
3. Verify `useDragAndDrop` hook sensors configured correctly

### Screen Reader Not Announcing
**Issue**: NVDA not reading announcements
**Solutions**:
1. Check `role="status"` element exists
2. Verify `aria-live="assertive"` attribute
3. Use NVDA speech viewer to debug
4. Ensure announcement state is updating

### API Persistence Failing
**Issue**: Changes not saving to backend
**Solutions**:
1. Check `onReorderComplete` callback is provided
2. Verify API endpoint is correct
3. Check network tab for failed requests
4. Ensure error is thrown to trigger rollback

---

## Example API Module

```typescript
// src/api/tasks.ts
export async function persistTaskOrder(
  projectId: string,
  taskIds: string[]
): Promise<void> {
  const response = await fetch(`/api/projects/${projectId}/tasks/reorder`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ taskIds }),
  });

  if (!response.ok) {
    throw new Error(`Failed to persist task order: ${response.statusText}`);
  }
}
```

---

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 90+ | ✅ Full |
| IE 11 | - | ❌ Not supported |

---

## Related Documentation

- [dnd-kit Documentation](https://docs.dndkit.com/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Zustand Documentation](https://zustand.docs.pmnd.rs/)
- [Keyboard Navigation Tests](./keyboard-navigation-tests.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-08 | Initial implementation with WCAG 2.1 AA support |

---

## License

MIT License - See project root for details
