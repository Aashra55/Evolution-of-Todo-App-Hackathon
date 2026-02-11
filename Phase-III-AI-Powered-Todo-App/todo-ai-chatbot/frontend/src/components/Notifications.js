// frontend/src/components/Notifications.js
import React, { useState, useEffect } from 'react';

const Notification = ({ message, type, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 3000); // Auto-close after 3 seconds
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`p-3 rounded-lg shadow-lg flex justify-between items-center transition-opacity duration-300 ${type === 'success' ? 'bg-gray-800 border-cyan-500 text-cyan-400 shadow-cyan-500/50' : type === 'error' ? 'bg-gray-800 border-fuchsia-500 text-fuchsia-400 shadow-fuchsia-500/50' : 'bg-gray-700 border-gray-400 text-gray-100 shadow-gray-500/50'}`}>
      <span className="text-sm font-medium">{message}</span>
      <button onClick={onClose} className="ml-4 text-lg font-bold text-gray-400 hover:text-gray-200 focus:outline-none">&times;</button>
    </div>
  );
};

function Notifications({ notifications, removeNotification }) {
  return (
    <div className="notifications-container">
      {notifications.map((note) => (
        <Notification
          key={note.id}
          message={note.message}
          type={note.type}
          onClose={() => removeNotification(note.id)}
        />
      ))}
    </div>
  );
}

export default Notifications;
