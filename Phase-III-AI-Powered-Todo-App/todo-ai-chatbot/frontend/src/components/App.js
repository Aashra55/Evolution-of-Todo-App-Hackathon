// frontend/src/components/App.js
import React, { useState, useEffect } from 'react';
import ChatInput from './ChatInput';
import ChatDisplay from './ChatDisplay';
import TaskListPanel from './TaskListPanel';
import Notifications from './Notifications'; // Import Notifications component
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import { MdChatBubbleOutline } from 'react-icons/md'; // Import chat bubble icon

const USER_ID = uuidv4(); // Generate a unique user ID for this session
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

  // Function to fetch tasks from the backend
  const fetchTasks = async () => {
    try {
      // Simulate a command to list tasks for the agent
      const response = await axios.post(`http://localhost:8000/api/${USER_ID}/chat`, {
        message: "list all my tasks", // This message should trigger the list_tasks tool
        conversation_id: CONVERSATION_ID
      });
      const data = response.data;
      if (data.response) {
        try {
          const agentResponse = JSON.parse(data.response);
          if (agentResponse.tasks && Array.isArray(agentResponse.tasks)) {
            setTasks(agentResponse.tasks);
            if (agentResponse.message) {
              addNotification(agentResponse.message, 'success');
            }
          } else if (agentResponse.message) {
             addNotification(agentResponse.message, agentResponse.status === 'success' ? 'success' : 'error');
          }
        } catch (e) {
          console.error("Could not parse agent's task response:", e);
          addNotification("Error parsing agent's task response.", 'error');
        }
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
      addNotification('Error fetching tasks from backend.', 'error');
    }
  };

  // Initial fetch of tasks when component mounts
  useEffect(() => {
    fetchTasks();
  }, []);

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
        // Not a JSON response, or parsing failed, just add a generic info notification
        addNotification("Agent responded.", 'info');
      }

      // After sending a message, re-fetch tasks to update the panel
      fetchTasks();

    } catch (error) {
      console.error('Error sending message:', error);
      addNotification('Error: Could not connect to the chatbot.', 'error');
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'ai', text: 'Error: Could not connect to the chatbot.' },
      ]);
    }
  };

  return (
    <div className="min-h-screen flex flex-col dark-background light-text">
      <header className="flex items-center justify-center py-4 px-6 shadow-lg">
        <h1 className="text-3xl font-extrabold tracking-wide neon-text-glow-primary">AI-powered Todo Chatbot</h1>
        {/* Mobile Menu Button for Task Panel removed as task panel is always visible */}
      </header>
      <div className="flex flex-1 flex-col md:flex-row main-content">
        {/* Chat Section - Takes 2/3 width on desktop (left side), hidden on mobile main layout */}
        <div className="flex flex-col flex-grow hidden md:flex md:w-2/3 chat-section">
          <ChatDisplay messages={messages} />
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
        
        {/* Task Panel - Always visible below header on mobile, takes 1/3 width on desktop (right side) */}
        <aside className="w-full md:w-1/3 p-4 dark-surface task-panel-section">
          <TaskListPanel tasks={tasks} />
        </aside>
      </div>
      <Notifications notifications={notifications} removeNotification={removeNotification} />

      {/* Floating Chat Button for Mobile - always visible */}
      <button
        onClick={toggleChatModal}
        className="fixed bottom-4 right-4 z-50 p-3 rounded-full bg-neon-secondary shadow-lg hover:bg-neon-secondary-light transition-colors duration-300 md:hidden" // Visible on mobile, hidden on desktop
        aria-label="Open Chat"
      >
        <MdChatBubbleOutline size={28} className="text-white" />
      </button>

      {/* Chat Modal for Mobile */}
      {showChatModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75 md:hidden"> {/* Only on mobile */}
          <div className="bg-dark-background w-full h-full flex flex-col p-4 rounded-lg shadow-lg relative">
            <button onClick={toggleChatModal} className="absolute top-4 right-4 text-white focus:outline-none">
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
