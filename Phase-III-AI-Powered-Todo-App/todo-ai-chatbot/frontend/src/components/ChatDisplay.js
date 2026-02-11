// frontend/src/components/ChatDisplay.js
import React from 'react';
import { FaUser, FaRobot } from 'react-icons/fa'; // Import icons

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
    <div className="flex-1 p-4 overflow-y-auto dark-surface text-light-text rounded-lg neon-glow-secondary">
      {messages.map((msg, index) => (
        <div key={index} className={`mb-3 p-3 rounded-lg max-w-sm ${msg.sender === 'user' ? 'ml-auto neon-user-message' : 'mr-auto neon-ai-message'}`}>
          <div className="flex items-center mb-1 font-bold">
            {msg.sender === 'user' ? <FaUser className="mr-2 neon-dark-text" /> : <FaRobot className="mr-2 neon-light-text" />}
            <span className={msg.sender === 'user' ? 'neon-dark-text' : 'neon-light-text'}>{msg.sender === 'user' ? 'You' : 'AI'}:</span>
          </div>
          <div className="text-sm">
            {renderMessageContent(msg)}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ChatDisplay;
