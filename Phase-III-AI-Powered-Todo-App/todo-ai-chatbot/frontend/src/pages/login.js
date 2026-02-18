// frontend/src/pages/login.js
import React, { useState } from 'react';
import { useRouter } from 'next/router';
import authService from '../services/authService';
import Notifications from '../components/Notifications'; // Import Notifications component
import { v4 as uuidv4 } from 'uuid'; // For notification IDs

const LoginPage = () => {
  const [username, setUsername] = useState('');
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

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await authService.login(username, password);
      addNotification('Login successful!', 'success');
      router.push('/'); // Redirect to home page on successful login
    } catch (error) {
      addNotification(`Login failed: ${error}`, 'error');
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="bg-gray-800 p-8 rounded-lg shadow-neon-blue w-full max-w-md">
        <h2 className="text-3xl font-bold text-center text-white mb-6">Login</h2>
        <form onSubmit={handleLogin}>
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
              Sign In
            </button>
            <a
              href="/register"
              className="inline-block align-baseline font-bold text-sm text-white hover:text-gray-300"
            >
              Don't have an account? Register
            </a>
          </div>
        </form>
      </div>
      <Notifications notifications={notifications} removeNotification={removeNotification} />
    </div>
  );
};

export default LoginPage;
