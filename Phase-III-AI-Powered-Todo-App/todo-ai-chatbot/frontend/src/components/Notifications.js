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
    <div className={`p-3 rounded-lg flex justify-between items-center transition-opacity duration-300 ${type === 'success' ? 'neon-notification-success' : type === 'error' ? 'neon-notification-error' : 'neon-notification-info'}`}>
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
