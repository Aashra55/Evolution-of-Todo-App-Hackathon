// frontend/src/components/TaskListPanel.js
import React from 'react';

function TaskListPanel({ tasks }) {
  const pendingTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="p-4 bg-gray-100 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4 text-indigo-700">Your Tasks</h2>
      
      <h3 className="text-lg font-medium mb-2 text-gray-700">Pending ({pendingTasks.length})</h3>
      {pendingTasks.length > 0 ? (
        <ul className="space-y-2 mb-4">
          {pendingTasks.map(task => (
            <li key={task.id} className="p-3 bg-white rounded-md shadow-sm border border-gray-200">
              <strong className="text-indigo-600">{task.title}</strong>
              {task.description && <p className="text-gray-600 text-sm mt-1">{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500 mb-4">No pending tasks.</p>
      )}

      <h3 className="text-lg font-medium mb-2 text-gray-700">Completed ({completedTasks.length})</h3>
      {completedTasks.length > 0 ? (
        <ul className="space-y-2">
          {completedTasks.map(task => (
            <li key={task.id} className="p-3 bg-white rounded-md shadow-sm border border-gray-200 line-through text-gray-500">
              <strong className="text-indigo-600">{task.title}</strong>
              {task.description && <p className="text-gray-600 text-sm mt-1">{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500">No completed tasks.</p>
      )}
    </div>
  );
}

export default TaskListPanel;
