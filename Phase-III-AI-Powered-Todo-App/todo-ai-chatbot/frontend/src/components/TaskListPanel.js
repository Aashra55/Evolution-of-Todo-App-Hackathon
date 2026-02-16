// frontend/src/components/TaskListPanel.js
import React from 'react';
import axios from 'axios';

function TaskListPanel({ tasks, onTaskToggle, userId }) {
  const pendingTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="p-4 task-panel-wrapper rounded-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Your Tasks</h2>
      
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-3 text-blue-600 flex items-center">
          <span className="inline-block w-3 h-3 bg-blue-500 rounded-full mr-2"></span>
          Pending ({pendingTasks.length})
        </h3>
        {pendingTasks.length > 0 ? (
          <ul className="space-y-2">
            {pendingTasks.map(task => (
              <li key={task.id} className="p-4 task-item task-item-pending border-l-4 border-blue-500 bg-blue-50">
                <div className="flex items-start">
                  <button
                    onClick={() => onTaskToggle && onTaskToggle(task.id)}
                    className="inline-block w-5 h-5 border-2 border-blue-500 rounded mr-3 mt-0.5 flex-shrink-0 cursor-pointer hover:bg-blue-100 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
                    aria-label={`Mark "${task.title}" as completed`}
                    title="Click to mark as completed"
                  ></button>
                  <div className="flex-1">
                    <strong className="task-title block mb-1 text-gray-800 font-semibold">{task.title}</strong>
                    {task.description && <p className="text-sm text-gray-600 mt-1">{task.description}</p>}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500 text-sm pl-5">No pending tasks.</p>
        )}
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-3 text-green-600 flex items-center">
          <span className="inline-block w-3 h-3 bg-green-500 rounded-full mr-2"></span>
          Completed ({completedTasks.length})
        </h3>
        {completedTasks.length > 0 ? (
          <ul className="space-y-2">
            {completedTasks.map(task => (
              <li key={task.id} className="p-4 task-item task-item-completed border-l-4 border-green-500 bg-green-50 opacity-75">
                <div className="flex items-start">
                  <button
                    onClick={() => onTaskToggle && onTaskToggle(task.id)}
                    className="inline-block w-5 h-5 bg-green-500 rounded mr-3 mt-0.5 flex-shrink-0 flex items-center justify-center cursor-pointer hover:bg-green-600 transition-colors focus:outline-none focus:ring-2 focus:ring-green-500"
                    aria-label={`Mark "${task.title}" as pending`}
                    title="Click to mark as pending"
                  >
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </button>
                  <div className="flex-1">
                    <strong className="task-title task-title-completed block mb-1 text-gray-600 line-through">{task.title}</strong>
                    {task.description && <p className="text-sm text-gray-500 mt-1 line-through">{task.description}</p>}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500 text-sm pl-5">No completed tasks.</p>
        )}
      </div>
    </div>
  );
}

export default TaskListPanel;
