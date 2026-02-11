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
    <div className={`p-3 rounded-lg shadow-md flex justify-between items-center transition-opacity duration-300 ${type === 'success' ? 'bg-green-100 border-green-400 text-green-700' : type === 'error' ? 'bg-red-100 border-red-400 text-red-700' : 'bg-blue-100 border-blue-400 text-blue-700'}`}>
      <span className="text-sm font-medium">{message}</span>
      <button onClick={onClose} className="ml-4 text-lg font-bold text-gray-500 hover:text-gray-700 focus:outline-none">&times;</button>
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
