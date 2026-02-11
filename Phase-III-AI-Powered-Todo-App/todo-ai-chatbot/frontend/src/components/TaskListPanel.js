// frontend/src/components/TaskListPanel.js
import React from 'react';

function TaskListPanel({ tasks }) {
  const pendingTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="p-4 task-panel-wrapper rounded-lg">
      <h2 className="text-xl font-semibold mb-4 neon-text-glow-primary">Your Tasks</h2>
      
      <h3 className="text-lg font-medium mb-2 light-text">Pending ({pendingTasks.length})</h3>
      {pendingTasks.length > 0 ? (
        <ul className="space-y-2 mb-4">
          {pendingTasks.map(task => (
            <li key={task.id} className="p-3 dark-surface rounded-md neon-glow-primary light-text">
              <strong className="neon-text-glow-primary">{task.title}</strong>
              {task.description && <p className="gray-text text-sm mt-1">{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="gray-text mb-4">No pending tasks.</p>
      )}

      <h3 className="text-lg font-medium mb-2 light-text">Completed ({completedTasks.length})</h3>
      {completedTasks.length > 0 ? (
        <ul className="space-y-2">
          {completedTasks.map(task => (
            <li key={task.id} className="p-3 dark-surface rounded-md neon-glow-secondary line-through gray-text">
              <strong className="neon-text-glow-secondary">{task.title}</strong>
              {task.description && <p className="gray-text text-sm mt-1">{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="gray-text">No completed tasks.</p>
      )}
    </div>
  );
}

export default TaskListPanel;
