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
    <div className="flex-1 p-4 overflow-y-auto chat-display-wrapper max-h-[calc(100vh-200px)] rounded-lg mb-4 md:ml-4" style={{ maxHeight: 'calc(100vh - 200px)' }}>
      {messages.map((msg, index) => (
        <div key={index} className={`mb-4 p-4 max-w-sm ${msg.sender === 'user' ? 'ml-auto user-message' : 'mr-auto ai-message'}`}>
          <div className="flex items-center mb-2 font-semibold">
            {msg.sender === 'user' ? <FaUser className="mr-2 user-icon" /> : <FaRobot className="mr-2 ai-icon" />}
            <span className={msg.sender === 'user' ? 'text-white' : 'text-gray-700'}>{msg.sender === 'user' ? 'You' : 'AI'}:</span>
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
