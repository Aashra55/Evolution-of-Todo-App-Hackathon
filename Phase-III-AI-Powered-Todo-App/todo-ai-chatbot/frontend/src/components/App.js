// frontend/src/components/App.js
import React, { useState, useEffect } from 'react';
import ChatInput from './ChatInput';
import ChatDisplay from './ChatDisplay';
import TaskListPanel from './TaskListPanel';
import Notifications from './Notifications'; // Import Notifications component
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { FaRobot } from 'react-icons/fa'; // Import robot icon

// Get or create USER_ID from localStorage to persist across reloads
const getOrCreateUserId = () => {
  if (typeof window !== 'undefined') {
    let userId = localStorage.getItem('todo_user_id');
    if (!userId) {
      userId = uuidv4();
      localStorage.setItem('todo_user_id', userId);
    }
    return userId;
  }
  return uuidv4();
};

const USER_ID = getOrCreateUserId();
const CONVERSATION_ID = uuidv4(); // Generate a unique conversation ID for this session

function App() {
  const [messages, setMessages] = useState([]);
  const [tasks, setTasks] = useState([]); // State to hold tasks
  const [notifications, setNotifications] = useState([]); // State to hold notifications
  const [showChatModal, setShowChatModal] = useState(false); // State to control chat modal visibility
  // showTaskPanel state and toggleTaskPanel function removed as task panel is always visible on mobile

  const toggleChatModal = () => {
    setShowChatModal(!showChatModal);
  };

  // Helper function to add a notification
  const addNotification = (message, type = 'info') => {
    const id = uuidv4();
    setNotifications((prev) => [...prev, { id, message, type }]);
  };

  // Helper function to remove a notification
  const removeNotification = (id) => {
    setNotifications((prev) => prev.filter((note) => note.id !== id));
  };

  // Function to fetch tasks directly from the backend API (without sending chat message)
  const fetchTasks = async (silent = false) => {
    try {
      // Use direct tasks endpoint instead of chat endpoint
      const response = await axios.get(`http://localhost:8000/api/${USER_ID}/tasks`);
      const data = response.data;
      if (data.status === 'success' && Array.isArray(data.tasks)) {
        setTasks(data.tasks);
        if (!silent && data.message) {
          // Only show notification if not silent mode
          console.log('Tasks fetched:', data.message);
        }
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
      // Silently fail on initial load or if backend is not ready
      if (!silent && error.code !== 'ERR_NETWORK' && !error.message.includes('Network Error')) {
        const errorMessage = error.response?.data?.detail || error.message || 'Error fetching tasks from backend.';
        addNotification(`Error: ${errorMessage}`, 'error');
      }
    }
  };

  // Initial fetch of tasks when component mounts (silent mode - no notifications)
  useEffect(() => {
    fetchTasks(true); // Silent fetch on mount
  }, []);

  // Function to handle task checkbox toggle
  const handleTaskToggle = async (taskId) => {
    try {
      const response = await axios.patch(`http://localhost:8000/api/${USER_ID}/tasks/${taskId}/toggle`);
      if (response.data.status === 'success') {
        // Refresh tasks after toggle
        await fetchTasks(true); // Silent fetch
        addNotification(response.data.message || 'Task status updated', 'success');
      }
    } catch (error) {
      console.error('Error toggling task:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to update task status';
      addNotification(`Error: ${errorMessage}`, 'error');
    }
  };

  const handleSendMessage = async (text) => {
    const newUserMessage = { sender: 'user', text: text };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);

    try {
      const response = await axios.post(`http://localhost:8000/api/${USER_ID}/chat`, {
        message: text,
        conversation_id: CONVERSATION_ID
      });
      const agentResponseRaw = response.data.response;
      setMessages((prevMessages) => [...prevMessages, { sender: 'ai', text: agentResponseRaw }]);
      
      // Attempt to parse agent's raw response to check for status/message for notification
      try {
        const agentResponseParsed = JSON.parse(agentResponseRaw);
        if (agentResponseParsed.message) {
          addNotification(agentResponseParsed.message, agentResponseParsed.status || 'info');
        }
      } catch (e) {
        // Not a JSON response (could be plain text AI response or error message)
        // Only show notification if it's an error message
        if (agentResponseRaw.toLowerCase().includes('error') || agentResponseRaw.toLowerCase().includes('trouble')) {
          // It's likely an error message, don't show generic "Agent responded" notification
        } else {
          // It's a regular AI text response, no need for notification
        }
      }

      // After sending a message, re-fetch tasks to update the panel (silent mode)
      // This ensures task panel updates after add/complete/delete operations
      setTimeout(() => {
        fetchTasks(true); // Silent fetch to update task panel
      }, 500); // Small delay to ensure backend has processed the request

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Could not connect to the chatbot.';
      addNotification(`Error: ${errorMessage}`, 'error');
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'ai', text: `Error: ${errorMessage}` },
      ]);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="flex items-center justify-center py-6 px-6 shadow-sm bg-white border-b border-gray-200">
        <h1 className="text-3xl font-bold tracking-tight header-title">AI-Powered Todo Chatbot</h1>
        {/* Mobile Menu Button for Task Panel removed as task panel is always visible */}
      </header>
      <div className="flex flex-1 flex-col md:flex-row main-content">
        {/* Chat Section - Takes 2/3 width on desktop (left side), hidden on mobile main layout */}
        <div className="flex-col flex-grow hidden md:flex md:w-2/3 chat-section">
          <ChatDisplay messages={messages} />
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
        
        {/* Task Panel - Always visible below header on mobile, takes 1/3 width on desktop (right side) */}
        <aside className="w-full md:w-1/3 p-4 bg-white task-panel-section">
          <TaskListPanel tasks={tasks} onTaskToggle={handleTaskToggle} userId={USER_ID} />
        </aside>
      </div>
      <Notifications notifications={notifications} removeNotification={removeNotification} />

      {/* Floating Chat Button for Mobile - always visible */}
      <button
        onClick={toggleChatModal}
        className="fixed bottom-4 right-4 z-50 p-3 rounded-full shadow-lg transition-colors duration-300 md:hidden chat-bubble" // Visible on mobile, hidden on desktop
        aria-label="Open Chat"
      >
        <FaRobot size={28} className="text-white" />
      </button>

      {/* Chat Modal for Mobile */}
      {showChatModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 md:hidden"> {/* Only on mobile */}
          <div className="bg-white w-full h-full flex flex-col p-4 rounded-lg shadow-xl relative">
            <button onClick={toggleChatModal} className="absolute top-4 right-4 text-gray-600 hover:text-gray-800 focus:outline-none text-2xl font-bold">
              &times; 
            </button>
            <ChatDisplay messages={messages} />
            <ChatInput onSendMessage={handleSendMessage} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
