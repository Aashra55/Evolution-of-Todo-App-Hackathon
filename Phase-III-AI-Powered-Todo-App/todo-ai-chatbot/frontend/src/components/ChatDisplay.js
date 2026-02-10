// frontend/src/components/ChatDisplay.js
import React from 'react';

function ChatDisplay({ messages }) {
  const renderMessageContent = (msg) => {
    try {
      const parsedContent = JSON.parse(msg.text);
      if (parsedContent.tasks && Array.isArray(parsedContent.tasks)) {
        return (
          <>
            <p>{parsedContent.message || "Here are your tasks:"}</p>
            <ul>
              {parsedContent.tasks.map(task => (
                <li key={task.id} style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
                  <strong>{task.title}</strong>: {task.description || "No description"} ({task.completed ? "Completed" : "Pending"})
                </li>
              ))}
            </ul>
          </>
        );
      }
      return <p>{msg.text}</p>;
    } catch (e) {
      return <p>{msg.text}</p>;
    }
  };

  return (
    <div className="chat-display-area">
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.sender}`}>
          <strong>{msg.sender}:</strong> {renderMessageContent(msg)}
        </div>
      ))}
    </div>
  );
}

export default ChatDisplay;
