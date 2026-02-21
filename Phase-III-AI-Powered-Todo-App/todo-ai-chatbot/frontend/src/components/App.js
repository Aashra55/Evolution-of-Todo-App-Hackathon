// frontend/src/components/App.js
import React, { useState, useEffect } from 'react';
import ChatInput from './ChatInput';
import ChatDisplay from './ChatDisplay';
import TaskListPanel from './TaskListPanel';
import Notifications from './Notifications'; // Import Notifications component
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { FaRobot } from 'react-icons/fa'; // Import robot icon
import { useRouter } from 'next/router'; // Import useRouter
import authService from '../services/authService'; // Import authService

// Configure Axios to include the Authorization header
const axiosInstance = axios.create();

axiosInstance.interceptors.request.use(
  (config) => {
    const token = authService.getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add an interceptor for handling 401 Unauthorized responses
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // If 401, token might be expired or invalid. Log out and redirect.
      authService.logout();
      if (typeof window !== 'undefined') {
        window.location.href = '/login'; // Redirect to login page
      }
    }
    return Promise.reject(error);
  }
);

function App() {
  const [messages, setMessages] = useState([]);
  const [tasks, setTasks] = useState([]); // State to hold tasks
  const [notifications, setNotifications] = useState([]); // State to hold notifications
  const [showChatModal, setShowChatModal] = useState(false); // State to control chat modal visibility
  const [isReady, setIsReady] = useState(false); // New state to track hydration/auth check readiness
  const router = useRouter();

  // Effect to check authentication status
  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
    } else {
      setIsReady(true);
    }
  }, [router]);

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
      const response = await axiosInstance.get(`http://localhost:8000/api/tasks`);
      const data = response.data;
      if (data.status === 'success' && Array.isArray(data.tasks)) {
        setTasks(data.tasks);
        if (!silent && data.message) {
          console.log('Tasks fetched:', data.message);
        }
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
      if (!silent && error.code !== 'ERR_NETWORK' && !error.message.includes('Network Error')) {
        const errorMessage = error.response?.data?.detail || error.message || 'Error fetching tasks from backend.';
        addNotification(`Error: ${errorMessage}`, 'error');
      }
    }
  };

  // Initial fetch of tasks when component mounts (silent mode - no notifications)
  useEffect(() => {
    if (authService.isAuthenticated()) { // Only fetch if authenticated
      fetchTasks(true); // Silent fetch on mount
    }
  }, [router]);

  // Function to handle task checkbox toggle
  const handleTaskToggle = async (taskId) => {
    try {
      const response = await axiosInstance.patch(`http://localhost:8000/api/tasks/${taskId}/toggle`);
      if (response.data.status === 'success') {
        await fetchTasks(true); // Silent fetch
        addNotification(response.data.message || 'Task status updated', 'success');
      }
    } catch (error) {
      console.error('Error toggling task:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to update task status';
      addNotification(`Error: ${errorMessage}`, 'error');
    }
  };

  // Function to handle task deletion
  const handleTaskDelete = async (taskId) => {
    try {
      const response = await axiosInstance.delete(`http://localhost:8000/api/tasks/${taskId}`);
      if (response.data.status === 'success') {
        await fetchTasks(true); // Silent fetch
        addNotification(response.data.message || 'Task deleted successfully', 'success');
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to delete task';
      addNotification(`Error: ${errorMessage}`, 'error');
    }
  };

  const handleSendMessage = async (text) => {
    const newUserMessage = { sender: 'user', text: text };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);

    try {
      // Conversation ID will be handled by the backend
      const response = await axiosInstance.post(`http://localhost:8000/api/chat`, {
        message: text,
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
        if (agentResponseRaw.toLowerCase().includes('error') || agentResponseRaw.toLowerCase().includes('trouble')) {
        } else {
        }
      }

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

  const handleLogout = () => {
    authService.logout();
    router.push('/login');
  };

  if (!isReady) {
    return null; // Don't render until authentication status is confirmed on client side
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="flex items-center justify-between py-6 px-6 shadow-sm bg-white border-b border-gray-200">
        <h1 className="text-3xl font-bold tracking-tight header-title">AI-Powered Todo Chatbot</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded transition-colors duration-300"
        >
          Logout
        </button>
      </header>
      <div className="flex flex-1 flex-col md:flex-row main-content">
        <div className="flex-col flex-grow hidden md:flex md:w-2/3 chat-section">
          <ChatDisplay messages={messages} />
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
        
        <aside className="w-full md:w-1/3 p-4 bg-white task-panel-section">
          <TaskListPanel tasks={tasks} onTaskToggle={handleTaskToggle} onTaskDelete={handleTaskDelete} />
        </aside>
      </div>
      <Notifications notifications={notifications} removeNotification={removeNotification} />

      <button
        onClick={toggleChatModal}
        className="fixed bottom-4 right-4 z-50 p-3 rounded-full shadow-lg transition-colors duration-300 md:hidden chat-bubble"
        aria-label="Open Chat"
      >
        <FaRobot size={28} className="text-white" />
      </button>

      {showChatModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 md:hidden">
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
