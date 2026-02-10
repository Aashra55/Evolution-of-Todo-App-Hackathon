// frontend/src/components/App.js
import React, { useState, useEffect } from 'react';
import ChatInput from './ChatInput';
import ChatDisplay from './ChatDisplay';
import TaskListPanel from './TaskListPanel';
import Notifications from './Notifications'; // Import Notifications component
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import '../styles/responsive.css'; // Import responsive styles

const USER_ID = uuid4(); // Generate a unique user ID for this session
const CONVERSATION_ID = uuid4(); // Generate a unique conversation ID for this session

function App() {
  const [messages, setMessages] = useState([]);
  const [tasks, setTasks] = useState([]); // State to hold tasks
  const [notifications, setNotifications] = useState([]); // State to hold notifications

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
      console.error("Error fetching tasks:", error);
      addNotification("Error fetching tasks from backend.", 'error');
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
    <div className="App">
      <header className="app-header">
        <h1>AI-powered Todo Chatbot</h1>
      </header>
      <div className="main-content">
        <div className="chat-section">
          <ChatDisplay messages={messages} />
          <ChatInput onSendMessage={handleSendMessage} />
        </div>
        <aside className="task-panel-section">
          <TaskListPanel tasks={tasks} />
        </aside>
      </div>
      <Notifications notifications={notifications} removeNotification={removeNotification} />
    </div>
  );
}

export default App;