// frontend/src/pages/register.js
import React, { useState } from 'react';
import dynamic from 'next/dynamic'; // Import dynamic
import { useRouter } from 'next/router';
import authService from '../services/authService';
import { v4 as uuidv4 } from 'uuid'; // For notification IDs

// Dynamically import Notifications with SSR disabled
const Notifications = dynamic(() => import('../components/Notifications'), { ssr: false });


const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [notifications, setNotifications] = useState([]);
  const router = useRouter();

  // Helper function to add a notification
  const addNotification = (message, type = 'info') => {
    const id = uuidv4();
    setNotifications((prev) => [...prev, { id, message, type }]);
  };

  // Helper function to remove a notification
  const removeNotification = (id) => {
    setNotifications((prev) => prev.filter((note) => note.id !== id));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await authService.register(username, password, email); // Pass email here
      addNotification('Registration successful! Please log in.', 'success');
      router.push('/login'); // Redirect to login page after successful registration
    } catch (error) {
      addNotification(`Registration failed: ${error}`, 'error');
      console.error('Registration failed:', error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-neon-blue w-full max-w-md">
        <h2 className="text-3xl font-bold text-center text-white mb-6">Register</h2>
        <form onSubmit={handleRegister}>
          <div className="mb-4">
            <label className="block text-white text-sm font-bold mb-2" htmlFor="username">
              Username
            </label>
            <input
              type="text"
              id="username"
              className="shadow-inner appearance-none border border-gray-700 rounded w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-neon-blue bg-gray-700"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="mb-4"> {/* Email field */}
            <label className="block text-white text-sm font-bold mb-2" htmlFor="email">
              Email
            </label>
            <input
              type="email"
              id="email"
              className="shadow-inner appearance-none border border-gray-700 rounded w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-neon-blue bg-gray-700"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-white text-sm font-bold mb-2" htmlFor="password">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="shadow-inner appearance-none border border-gray-700 rounded w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-neon-blue bg-gray-700"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="flex items-center justify-between">
            <button
              type="submit"
              className="bg-neon-blue hover:bg-neon-blue-dark text-white font-bold py-3 px-6 rounded focus:outline-none focus:shadow-outline transition-all duration-300 transform hover:scale-105"
            >
              Register
            </button>
            <a
              href="/login"
              className="inline-block align-baseline font-bold text-sm text-white hover:text-gray-300"
            >
              Already have an account? Login
            </a>
          </div>
        </form>
      </div>
      {notifications.length > 0 && <Notifications notifications={notifications} removeNotification={removeNotification} />}
    </div>
  );
};

export default RegisterPage;
