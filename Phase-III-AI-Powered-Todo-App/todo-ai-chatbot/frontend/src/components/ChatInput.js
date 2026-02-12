// frontend/src/components/ChatInput.js
import React, { useState } from 'react';
import { FaUser, FaRobot, FaPaperPlane } from 'react-icons/fa'; // Import FaPaperPlane

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
        className="flex-grow p-4 neon-input mr-2"
      />
      <button
        type="submit"
        className="px-8 py-4 neon-button transition duration-300 ease-in-out ml-4"
      >
        <FaPaperPlane className="text-lg md:text-xl" />
      </button>
    </form>
  );
}

export default ChatInput;
