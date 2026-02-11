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
    <form onSubmit={handleSubmit} className="flex items-center p-4 dark-surface border-t neon-border-primary">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        className="flex-grow p-2 neon-input mr-2"
      />
      <button
        type="submit"
        className="px-4 py-2 neon-button transition duration-300 ease-in-out"
      >
        Send
      </button>
    </form>
  );
}

export default ChatInput;
