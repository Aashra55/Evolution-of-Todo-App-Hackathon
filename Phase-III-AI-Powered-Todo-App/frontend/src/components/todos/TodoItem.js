import React from 'react';

const TodoItem = ({ todo }) => {
  return (
    <div className={`todo-item ${todo.status}`}>
      <span className="todo-description">{todo.description}</span>
      <span className="todo-status">({todo.status})</span>
      {todo.due_date && <span className="todo-due-date">Due: {new Date(todo.due_date).toLocaleDateString()}</span>}
    </div>
  );
};

export default TodoItem;
