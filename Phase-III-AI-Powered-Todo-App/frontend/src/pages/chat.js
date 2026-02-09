import React, { useState, useEffect } from 'react';
import ChatWindow from '../components/chat/ChatWindow';
import ChatInput from '../components/chat/ChatInput';
import { sendMessage, loginUser } from '../services/chat_api';

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [authToken, setAuthToken] = useState(null);
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Simulate a login process to get an auth token
    const performLogin = async () => {
      try {
        // Use a default user for basic implementation
        const token = await loginUser("testuser", "testpassword"); 
        setAuthToken(token);
        setMessages([{ role: 'system', content: 'Welcome to Todo AI Chatbot! How can I help you today?' }]);
      } catch (err) {
        setError("Failed to login: " + err.message);
      }
    };
    performLogin();
  }, []);

  const handleSendMessage = async (text) => {
    if (!authToken) {
      setError("Please log in to send messages.");
      return;
    }

    const userMessage = { role: 'user', content: text };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setLoading(true);
    setError(null);

    try {
      const response = await sendMessage(text, conversationId, authToken);
      if (response && response.reply) {
        const botMessage = { role: 'bot', content: response.reply };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        setConversationId(response.conversation_id); // Update conversation ID
      } else {
        setError("Received an empty or invalid response from the bot.");
      }
    } catch (err) {
      setError("Error sending message: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  if (!authToken) {
    return <div className="loading-message">Logging in...</div>;
  }

  return (
    <div className="chat-page">
      <h1>Todo AI Chatbot</h1>
      <ChatWindow messages={messages} />
      {loading && <div className="loading-indicator">Typing...</div>}
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatPage;
