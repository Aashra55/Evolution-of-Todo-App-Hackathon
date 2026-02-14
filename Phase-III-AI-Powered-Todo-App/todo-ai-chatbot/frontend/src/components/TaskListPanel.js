// frontend/src/components/TaskListPanel.js
import React from 'react';

function TaskListPanel({ tasks }) {
  const pendingTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="p-4 task-panel-wrapper rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Your Tasks</h2>
      
      <h3 className="text-lg font-semibold mb-3 text-gray-700">Pending ({pendingTasks.length})</h3>
      {pendingTasks.length > 0 ? (
        <ul className="space-y-2 mb-6">
          {pendingTasks.map(task => (
            <li key={task.id} className="p-4 task-item task-item-pending">
              <strong className="task-title block mb-1">{task.title}</strong>
              {task.description && <p className="text-sm text-gray-600 mt-1">{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500 mb-6 text-sm">No pending tasks.</p>
      )}

      <h3 className="text-lg font-semibold mb-3 text-gray-700">Completed ({completedTasks.length})</h3>
      {completedTasks.length > 0 ? (
        <ul className="space-y-2">
          {completedTasks.map(task => (
            <li key={task.id} className="p-4 task-item task-item-completed">
              <strong className="task-title task-title-completed block mb-1">{task.title}</strong>
              {task.description && <p className="text-sm text-gray-500 mt-1">{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500 text-sm">No completed tasks.</p>
      )}
    </div>
  );
}

export default TaskListPanel;
