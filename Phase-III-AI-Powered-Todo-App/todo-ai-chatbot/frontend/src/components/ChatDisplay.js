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
    <div className="flex-1 p-4 overflow-y-auto bg-gray-900 text-gray-200 rounded-lg shadow-inner shadow-fuchsia-500/30">
      {messages.map((msg, index) => (
        <div key={index} className={`mb-3 p-3 rounded-lg max-w-sm ${msg.sender === 'user' ? 'ml-auto bg-cyan-600 text-white shadow-md shadow-cyan-500/50' : 'mr-auto bg-gray-700 text-gray-200 shadow-md shadow-fuchsia-500/50'}`}>
          <div className="flex items-center mb-1 font-bold">
            {msg.sender === 'user' ? <FaUser className="mr-2 text-cyan-400" /> : <FaRobot className="mr-2 text-fuchsia-400" />}
            <span className={msg.sender === 'user' ? 'text-cyan-400' : 'text-fuchsia-400'}>{msg.sender === 'user' ? 'You' : 'AI'}:</span>
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
