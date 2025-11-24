/**
 * Optimized Calendar Component with Performance Enhancements
 *
 * Optimizations Applied:
 * 1. React.memo for CalendarDay components (prevent unnecessary re-renders)
 * 2. useMemo for task filtering/sorting
 * 3. Virtualization for month grid (lazy loading)
 * 4. Code splitting for heavy components
 *
 * P4_T8: Frontend Optimization
 * Target: <500ms render time for 100 tasks in month view
 */

import React, { useMemo, useCallback } from 'react';
import { FixedSizeGrid as Grid } from 'react-window';

interface Task {
  id: number;
  name: string;
  date: Date;
  status: string;
  priority: string;
}

interface CalendarDayProps {
  date: Date;
  tasks: Task[];
  onTaskClick?: (task: Task) => void;
}

/**
 * Memoized CalendarDay component
 *
 * Only re-renders when date or tasks change
 * Prevents expensive re-renders during parent state updates
 */
export const CalendarDay = React.memo<CalendarDayProps>(
  ({ date, tasks, onTaskClick }) => {
    const dayNumber = date.getDate();
    const isToday = useMemo(() => {
      const today = new Date();
      return (
        date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear()
      );
    }, [date]);

    return (
      <div
        className={`calendar-day ${isToday ? 'today' : ''}`}
        data-date={date.toISOString()}
      >
        <div className="day-number">{dayNumber}</div>
        <div className="day-tasks">
          {tasks.slice(0, 3).map((task) => (
            <div
              key={task.id}
              className={`task task-${task.status}`}
              onClick={() => onTaskClick?.(task)}
            >
              {task.name}
            </div>
          ))}
          {tasks.length > 3 && (
            <div className="task-overflow">+{tasks.length - 3} more</div>
          )}
        </div>
      </div>
    );
  },
  // Custom comparison function for shallow prop equality
  (prevProps, nextProps) => {
    return (
      prevProps.date.getTime() === nextProps.date.getTime() &&
      prevProps.tasks.length === nextProps.tasks.length &&
      prevProps.tasks.every((task, i) => task.id === nextProps.tasks[i].id)
    );
  }
);

CalendarDay.displayName = 'CalendarDay';

interface CalendarMonthProps {
  year: number;
  month: number;
  tasks: Task[];
  filters?: {
    status?: string;
    priority?: string;
    search?: string;
  };
  onTaskClick?: (task: Task) => void;
}

/**
 * Optimized Calendar Month View
 *
 * Uses virtualization and memoization for 100+ tasks
 */
export const CalendarMonth: React.FC<CalendarMonthProps> = ({
  year,
  month,
  tasks,
  filters,
  onTaskClick,
}) => {
  // Memoized: Filter and sort tasks
  // Only re-computes when tasks or filters change
  const filteredTasks = useMemo(() => {
    let filtered = tasks;

    if (filters?.status) {
      filtered = filtered.filter((task) => task.status === filters.status);
    }

    if (filters?.priority) {
      filtered = filtered.filter((task) => task.priority === filters.priority);
    }

    if (filters?.search) {
      const searchLower = filters.search.toLowerCase();
      filtered = filtered.filter((task) =>
        task.name.toLowerCase().includes(searchLower)
      );
    }

    // Sort by date, then priority
    return filtered.sort((a, b) => {
      const dateCompare = a.date.getTime() - b.date.getTime();
      if (dateCompare !== 0) return dateCompare;

      const priorityOrder = { high: 0, medium: 1, low: 2 };
      return (
        priorityOrder[a.priority as keyof typeof priorityOrder] -
        priorityOrder[b.priority as keyof typeof priorityOrder]
      );
    });
  }, [tasks, filters]);

  // Memoized: Group tasks by date
  const tasksByDate = useMemo(() => {
    const grouped = new Map<string, Task[]>();

    filteredTasks.forEach((task) => {
      const dateKey = task.date.toISOString().split('T')[0];
      if (!grouped.has(dateKey)) {
        grouped.set(dateKey, []);
      }
      grouped.get(dateKey)!.push(task);
    });

    return grouped;
  }, [filteredTasks]);

  // Memoized: Generate calendar days
  const calendarDays = useMemo(() => {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - startDate.getDay()); // Start from Sunday

    const days: Date[] = [];
    const currentDate = new Date(startDate);

    // Generate 6 weeks (42 days) for consistent grid
    for (let i = 0; i < 42; i++) {
      days.push(new Date(currentDate));
      currentDate.setDate(currentDate.getDate() + 1);
    }

    return days;
  }, [year, month]);

  // Memoized: Cell renderer for virtualized grid
  const Cell = useCallback(
    ({ columnIndex, rowIndex, style }: any) => {
      const dayIndex = rowIndex * 7 + columnIndex;
      const date = calendarDays[dayIndex];

      if (!date) {
        return <div style={style} />;
      }

      const dateKey = date.toISOString().split('T')[0];
      const dayTasks = tasksByDate.get(dateKey) || [];

      return (
        <div style={style}>
          <CalendarDay date={date} tasks={dayTasks} onTaskClick={onTaskClick} />
        </div>
      );
    },
    [calendarDays, tasksByDate, onTaskClick]
  );

  return (
    <div className="calendar-month">
      <div className="calendar-header">
        <div className="weekday">Sun</div>
        <div className="weekday">Mon</div>
        <div className="weekday">Tue</div>
        <div className="weekday">Wed</div>
        <div className="weekday">Thu</div>
        <div className="weekday">Fri</div>
        <div className="weekday">Sat</div>
      </div>

      {/* Virtualized grid for performance */}
      <Grid
        columnCount={7}
        columnWidth={140}
        height={600}
        rowCount={6}
        rowHeight={100}
        width={980}
      >
        {Cell}
      </Grid>

      {/* Task count summary */}
      <div className="calendar-footer">
        <span>
          Showing {filteredTasks.length} of {tasks.length} tasks
        </span>
      </div>
    </div>
  );
};

/**
 * Performance Monitoring HOC
 *
 * Tracks render times for performance analysis
 */
export function withPerformanceTracking<P extends object>(
  Component: React.ComponentType<P>,
  componentName: string
): React.FC<P> {
  return (props: P) => {
    const onRenderCallback = useCallback(
      (
        id: string,
        phase: 'mount' | 'update',
        actualDuration: number,
        baseDuration: number,
        startTime: number,
        commitTime: number
      ) => {
        if (process.env.NODE_ENV === 'development') {
          console.log(`[Performance] ${componentName} ${phase}:`, {
            actualDuration: `${actualDuration.toFixed(2)}ms`,
            baseDuration: `${baseDuration.toFixed(2)}ms`,
          });

          // Log slow renders (>100ms)
          if (actualDuration > 100) {
            console.warn(`[Performance] Slow render detected in ${componentName}`);
          }
        }
      },
      [componentName]
    );

    return (
      <React.Profiler id={componentName} onRender={onRenderCallback}>
        <Component {...props} />
      </React.Profiler>
    );
  };
}

// Usage with performance tracking:
export const CalendarMonthTracked = withPerformanceTracking(
  CalendarMonth,
  'CalendarMonth'
);

/**
 * Lazy loaded heavy components
 *
 * Code splitting for components not needed on initial render
 */
export const CalendarSettings = React.lazy(
  () => import('./CalendarSettings')
);

export const TaskDetailsModal = React.lazy(
  () => import('./TaskDetailsModal')
);

/**
 * Example usage:
 *
 * import { CalendarMonthTracked, TaskDetailsModal } from './CalendarOptimized';
 * import { Suspense } from 'react';
 *
 * function App() {
 *   const [tasks, setTasks] = useState<Task[]>([...]);
 *   const [filters, setFilters] = useState({});
 *
 *   return (
 *     <>
 *       <CalendarMonthTracked
 *         year={2025}
 *         month={0}
 *         tasks={tasks}
 *         filters={filters}
 *         onTaskClick={(task) => console.log(task)}
 *       />
 *
 *       <Suspense fallback={<div>Loading...</div>}>
 *         <TaskDetailsModal taskId={selectedTaskId} />
 *       </Suspense>
 *     </>
 *   );
 * }
 */
