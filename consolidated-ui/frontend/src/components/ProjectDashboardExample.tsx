/**
 * Example integration of DraggableTaskList in a project dashboard
 * This demonstrates how to connect the component to Zustand and handle API persistence
 *
 * NOTE: This is an example/reference implementation. Integrate into your actual dashboard component.
 */

import { DraggableTaskList } from './DraggableTaskList';
import { useProjectStore } from '../store/useProjectStore';
import type { Task } from '../types';

// Example API module (replace with your actual API)
const api = {
  /**
   * Persist task order to backend
   * @param projectId - Project ID
   * @param taskIds - Array of task IDs in new order
   */
  async persistTaskOrder(projectId: string, taskIds: string[]): Promise<void> {
    const response = await fetch(`/api/projects/${projectId}/tasks/reorder`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskIds }),
    });

    if (!response.ok) {
      throw new Error(`Failed to persist task order: ${response.statusText}`);
    }
  },
};

/**
 * Project Dashboard with Draggable Task List
 */
export function ProjectDashboardExample() {
  // Get Zustand store selectors
  const selectedProjectId = useProjectStore((state) => state.selectedProjectId);
  const getProjectTasks = useProjectStore((state) => state.getProjectTasks);
  const reorderTasks = useProjectStore((state) => state.reorderTasks);
  const getSelectedProject = useProjectStore((state) => state.getSelectedProject);

  // Get current project and tasks
  const project = getSelectedProject();
  const tasks = selectedProjectId ? getProjectTasks(selectedProjectId) : [];

  /**
   * Handle task reorder with optimistic update
   */
  const handleReorder = (reorderedTasks: Task[]) => {
    if (!selectedProjectId) return;

    // Optimistic update - immediately update UI
    reorderTasks(selectedProjectId, reorderedTasks);
  };

  /**
   * Persist task order to backend after successful drop
   */
  const handleReorderComplete = async (reorderedTasks: Task[]) => {
    if (!selectedProjectId) return;

    try {
      // Extract task IDs in new order
      const taskIds = reorderedTasks.map((task) => task.id);

      // Persist to backend
      await api.persistTaskOrder(selectedProjectId, taskIds);

      console.log('✅ Task order persisted successfully');
    } catch (error) {
      console.error('❌ Failed to persist task order:', error);

      // Error thrown here will trigger automatic rollback in useDragAndDrop hook
      // The Zustand store will revert to previous task order
      throw error;
    }
  };

  // Show message if no project selected
  if (!selectedProjectId || !project) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <div className="text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No project selected</h3>
          <p className="mt-1 text-sm text-gray-500">
            Select a project from the sidebar to view and manage tasks.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Project Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{project.name}</h1>
        <p className="mt-2 text-gray-600">{project.description}</p>
        <div className="mt-2 flex items-center gap-3">
          <span
            className={`
              px-3 py-1 rounded-full text-sm font-medium
              ${
                project.status === 'completed'
                  ? 'bg-green-100 text-green-800'
                  : project.status === 'in_progress'
                    ? 'bg-blue-100 text-blue-800'
                    : project.status === 'on_hold'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-gray-100 text-gray-800'
              }
            `}
          >
            {project.status.replace('_', ' ').toUpperCase()}
          </span>
          <span className="text-sm text-gray-500">
            {tasks.length} task{tasks.length !== 1 ? 's' : ''}
          </span>
        </div>
      </div>

      {/* Task Statistics */}
      {tasks.length > 0 && (
        <div className="mb-6 grid grid-cols-4 gap-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">
              {tasks.filter((t) => t.status === 'pending').length}
            </div>
            <div className="text-sm text-gray-600">Pending</div>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-blue-900">
              {tasks.filter((t) => t.status === 'running').length}
            </div>
            <div className="text-sm text-blue-600">Running</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-green-900">
              {tasks.filter((t) => t.status === 'completed').length}
            </div>
            <div className="text-sm text-green-600">Completed</div>
          </div>
          <div className="bg-red-50 p-4 rounded-lg">
            <div className="text-2xl font-bold text-red-900">
              {tasks.filter((t) => t.status === 'failed').length}
            </div>
            <div className="text-sm text-red-600">Failed</div>
          </div>
        </div>
      )}

      {/* Draggable Task List */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Tasks</h2>
        <DraggableTaskList
          projectId={selectedProjectId}
          tasks={tasks}
          onReorder={handleReorder}
          onReorderComplete={handleReorderComplete}
        />
      </div>

      {/* Accessibility Information */}
      <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">
          ♿ Accessibility Features
        </h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>✅ Full keyboard navigation support</li>
          <li>✅ Screen reader announcements for all actions</li>
          <li>✅ WCAG 2.1 AA compliant</li>
          <li>✅ Visible focus indicators</li>
          <li>✅ Color contrast ratios meet standards</li>
        </ul>
      </div>
    </div>
  );
}

/**
 * Usage in App.tsx or main dashboard route:
 *
 * import { ProjectDashboardExample } from './components/ProjectDashboardExample';
 *
 * function App() {
 *   return (
 *     <div>
 *       <Sidebar />
 *       <main>
 *         <ProjectDashboardExample />
 *       </main>
 *     </div>
 *   );
 * }
 */
