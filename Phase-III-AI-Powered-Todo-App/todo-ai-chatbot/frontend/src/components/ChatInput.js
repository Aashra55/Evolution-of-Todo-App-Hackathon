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
    <form onSubmit={handleSubmit} className="flex items-center p-4 bg-gray-100 border-t border-gray-200">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        className="flex-grow p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mr-2"
      />
      <button
        type="submit"
        className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50"
      >
        Send
      </button>
    </form>
  );
}

export default ChatInput;
