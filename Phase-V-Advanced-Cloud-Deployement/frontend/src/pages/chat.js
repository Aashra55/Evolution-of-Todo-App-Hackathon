// pages/chat.js
import { useState, useEffect, useCallback } from 'react';
import Head from 'next/head';
// Assume a hypothetical function to interact with the backend API
import { createTask, getTasks, updateTask, deleteTask, completeTask } from '../services/chat_api'; 
import { connectWebSocket, disconnectWebSocket } from '../services/realtime_sync';
import TaskList from '../components/task_list'; // Import the TaskList component

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTasks = useCallback(async () => {
    setIsLoading(true);
    try {
      const fetchedTasks = await getTasks(); // This would call the backend API
      setTasks(fetchedTasks);
    } catch (error) {
      console.error("Error fetching tasks:", error);
      setMessages(prev => [...prev, { type: 'error', text: 'Failed to load tasks.' }]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // WebSocket message handler
  const handleWebSocketMessage = useCallback((message) => {
    console.log("WebSocket message received:", message);
    setMessages(prev => [...prev, { type: 'system', text: `Real-time update: ${message.type}` }]);

    switch (message.type) {
      case 'TASK_CREATED':
        setTasks(prev => [...prev, message.payload.task]);
        break;
      case 'TASK_UPDATED':
        setTasks(prev => prev.map(task => 
          task.id === message.payload.taskId 
            ? { ...task, ...message.payload.changes, ...message.payload.fullTask } 
            : task
        ));
        break;
      case 'TASK_DELETED':
        setTasks(prev => prev.filter(task => task.id !== message.payload.taskId));
        break;
      case 'BATCH_UPDATE':
          // For batch updates, it's often simpler to refetch or process each sub-update
          // For now, let's just refetch all tasks to ensure consistency
          fetchTasks(); 
          break;
      default:
        console.warn('Unknown WebSocket message type:', message.type);
    }
  }, [fetchTasks]);

  useEffect(() => {
    fetchTasks();
    connectWebSocket(handleWebSocketMessage);

    return () => {
      disconnectWebSocket();
    };
  }, [fetchTasks, handleWebSocketMessage]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { type: 'user', text: input }]);
    setIsLoading(true);
    setInput('');

    try {
      let response;
      if (input.toLowerCase().startsWith('create task')) {
          const taskTitle = input.substring('create task'.length).trim();
          if (taskTitle) {
              response = await createTask({ title: taskTitle }); // Call backend API
              // No need to setTasks directly here, WebSocket will update it
              setMessages(prev => [...prev, { type: 'bot', text: `Task "${response.title}" requested.` }]);
          } else {
              response = { response: "Please provide a title for the task." };
          }
      } else if (input.toLowerCase().startsWith('complete task')) {
          const taskId = input.substring('complete task'.length).trim();
          if (taskId) {
              response = await completeTask(taskId); // Call backend API
              // No need to setTasks directly here, WebSocket will update it
              setMessages(prev => [...prev, { type: 'bot', text: `Task "${taskId}" completion requested.` }]);
          } else {
              response = { response: "Please specify the task ID to complete." };
          }
      } else if (input.toLowerCase().startsWith('delete task')) {
          const taskId = input.substring('delete task'.length).trim();
          if (taskId) {
              response = await deleteTask(taskId); // Call backend API
              // No need to setTasks directly here, WebSocket will update it
              setMessages(prev => [...prev, { type: 'bot', text: `Task "${taskId}" deletion requested.` }]);
          } else {
              response = { response: "Please specify the task ID to delete." };
          }
      }
       else {
           // Send generic chat message to backend AI
           response = await sendChatMessage(input);
      }
      
      setMessages(prev => [...prev, { type: 'bot', text: response.response }]);

    } catch (error) {
      console.error("Error sending message:", error);
      setMessages(prev => [...prev, { type: 'error', text: 'Failed to send message or process command.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Head>
        <title>Todo AI Chatbot</title>
        <meta name="description" content="Chat interface for managing your tasks" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>Todo AI Chatbot</h1>
        
        <div className="chat-window">
          {messages.map((msg, index) => (
            <p key={index} className={msg.type}>
              <strong>{msg.type === 'user' ? 'You' : msg.type === 'bot' ? 'Bot' : 'System'}:</strong> {msg.text}
            </p>
          ))}
          {isLoading && <p><em>Bot is typing...</em></p>}
        </div>

        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
            placeholder="Type your message or command..."
          />
          <button onClick={handleSendMessage} disabled={isLoading}>Send</button>
        </div>

        <h2>Your Tasks</h2>
        {isLoading ? (
          <p>Loading tasks...</p>
        ) : (
          <TaskList tasks={tasks} /> // Use the TaskList component
        )}
      </main>

      <style jsx>{`
        main {
          padding: 2rem;
        }
        .chat-window {
          border: 1px solid #ccc;
          height: 300px;
          overflow-y: scroll;
          margin-bottom: 1rem;
          padding: 0.5rem;
        }
        .input-area {
          display: flex;
        }
        input[type="text"] {
          flex-grow: 1;
          margin-right: 0.5rem;
          padding: 0.5rem;
        }
        button {
          padding: 0.5rem 1rem;
        }
        p { margin: 0.5rem 0; }
        .user { color: blue; }
        .bot { color: green; }
        .system { color: gray; font-style: italic; }
        .error { color: red; }
      `}</style>
    </div>
  );
}