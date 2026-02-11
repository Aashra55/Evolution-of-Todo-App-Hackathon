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
    <form onSubmit={handleSubmit} className="flex items-center p-4 dark-surface ml-4">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        className="flex-grow p-3 neon-input mr-6"
      />
      <button type="submit" className="px-8 py-3 neon-button transition duration-300 ease-in-out ml-4">
        Send
      </button>
    </form>
  );
}

export default ChatInput;
