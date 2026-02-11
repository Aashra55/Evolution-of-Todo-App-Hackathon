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
    <div className="flex-1 p-4 overflow-y-auto bg-white rounded-lg shadow-inner">
      {messages.map((msg, index) => (
        <div key={index} className={`mb-2 p-3 rounded-lg max-w-xs ${msg.sender === 'user' ? 'ml-auto bg-indigo-500 text-white' : 'mr-auto bg-gray-200 text-gray-800'}`}>
          <div className="flex items-center mb-1">
            {msg.sender === 'user' ? <FaUser className="mr-2" /> : <FaRobot className="mr-2" />}
            <strong>{msg.sender === 'user' ? 'You' : 'AI'}:</strong>
          </div>
          {renderMessageContent(msg)}
        </div>
      ))}
    </div>
  );
}

export default ChatDisplay;
