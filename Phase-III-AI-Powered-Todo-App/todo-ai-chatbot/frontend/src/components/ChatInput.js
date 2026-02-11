// frontend/src/components/ChatInput.js
import React, { useState } from 'react';

function ChatInput({ onSendMessage }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center p-4 bg-gray-800 border-t border-cyan-500">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        className="flex-grow p-2 border border-cyan-500 bg-gray-900 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-fuchsia-500 shadow-md shadow-cyan-500/50 mr-2"
      />
      <button
        type="submit"
        className="px-4 py-2 bg-cyan-600 text-gray-900 rounded-lg hover:bg-cyan-500 focus:outline-none focus:ring-2 focus:ring-fuchsia-500 focus:ring-opacity-75 shadow-md shadow-cyan-500/50 transition duration-300 ease-in-out"
      >
        Send
      </button>
    </form>
  );
}

export default ChatInput;
