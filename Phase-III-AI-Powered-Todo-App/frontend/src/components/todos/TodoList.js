import React from 'react';
import TodoItem from './TodoItem';

const TodoList = ({ todos }) => {
  return (
    <div className="todo-list">
      <h2>Your Todos</h2>
      {todos.length === 0 ? (
        <p className="empty-state">No todos yet! Start by adding one in the chat.</p>
      ) : (
        todos.map(todo => (
          <TodoItem key={todo.id} todo={todo} />
        ))
      )}
    </div>
  );
};

export default TodoList;
