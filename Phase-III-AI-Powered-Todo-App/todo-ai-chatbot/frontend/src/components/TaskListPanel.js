// frontend/src/components/TaskListPanel.js
import React from 'react';

function TaskListPanel({ tasks }) {
  const pendingTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="p-4 bg-gray-900 rounded-lg shadow-lg border border-fuchsia-500 shadow-fuchsia-500/50">
      <h2 className="text-xl font-semibold mb-4 text-cyan-400 drop-shadow-md">Your Tasks</h2>
      
      <h3 className="text-lg font-medium mb-2 text-gray-200">Pending ({pendingTasks.length})</h3>
      {pendingTasks.length > 0 ? (
        <ul className="space-y-2 mb-4">
          {pendingTasks.map(task => (
            <li key={task.id} className="p-3 bg-gray-800 rounded-md shadow-md border border-cyan-500 shadow-cyan-500/30 text-gray-100">
              <strong className="text-cyan-300">{task.title}</strong>
              {task.description && <p className="text-gray-300 text-sm mt-1">{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-400 mb-4">No pending tasks.</p>
      )}

      <h3 className="text-lg font-medium mb-2 text-gray-200">Completed ({completedTasks.length})</h3>
      {completedTasks.length > 0 ? (
        <ul className="space-y-2">
          {completedTasks.map(task => (
            <li key={task.id} className="p-3 bg-gray-800 rounded-md shadow-md border border-fuchsia-500 shadow-fuchsia-500/30 line-through text-gray-400">
              <strong className="text-fuchsia-300">{task.title}</strong>
              {task.description && <p className="text-gray-400 text-sm mt-1">{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-400">No completed tasks.</p>
      )}
    </div>
  );
}

export default TaskListPanel;
