// frontend/src/components/TaskListPanel.js
import React from 'react';

function TaskListPanel({ tasks }) {
  const pendingTasks = tasks.filter(task => !task.completed);
  const completedTasks = tasks.filter(task => task.completed);

  return (
    <div className="task-list-panel">
      <h2>Your Tasks</h2>
      
      <h3>Pending ({pendingTasks.length})</h3>
      {pendingTasks.length > 0 ? (
        <ul>
          {pendingTasks.map(task => (
            <li key={task.id}>
              <strong>{task.title}</strong>
              {task.description && <p>{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p>No pending tasks.</p>
      )}

      <h3>Completed ({completedTasks.length})</h3>
      {completedTasks.length > 0 ? (
        <ul>
          {completedTasks.map(task => (
            <li key={task.id} style={{ textDecoration: 'line-through' }}>
              <strong>{task.title}</strong>
              {task.description && <p>{task.description}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p>No completed tasks.</p>
      )}
    </div>
  );
}

export default TaskListPanel;
