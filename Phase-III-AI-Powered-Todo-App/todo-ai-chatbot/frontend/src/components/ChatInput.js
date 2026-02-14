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
    <form onSubmit={handleSubmit} className="flex items-center md:p-4 bg-white border-t border-gray-200 md:ml-4">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        className="flex-grow md:p-4 p-3 modern-input md:mr-2 mr-3"
      />
      <button
        type="submit"
        className="md:px-6 md:py-4 px-5 py-3 modern-button md:ml-4"
      >
        <FaPaperPlane className="text-lg md:text-xl" />
      </button>
    </form>
  );
}

export default ChatInput;
