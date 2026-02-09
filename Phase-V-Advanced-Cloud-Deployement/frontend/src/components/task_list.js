// components/task_list.js
import React from 'react';

const TaskList = ({ tasks }) => {
  return (
    <ul>
      {tasks.length === 0 ? (
        <li>No tasks yet.</li>
      ) : (
        tasks.map((task) => (
          <li key={task.id}>
            <strong>{task.title}</strong> ({task.status}) - {task.description || 'No description'}
            {/* Display other attributes like priority, dueDate, tags as needed */}
          </li>
        ))
      )}
    </ul>
  );
};

export default TaskList;