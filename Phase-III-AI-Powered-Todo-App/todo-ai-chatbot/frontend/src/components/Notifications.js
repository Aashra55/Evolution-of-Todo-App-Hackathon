// frontend/src/components/Notifications.js
import React, { useState, useEffect } from 'react';
import './Notifications.css'; // Assume you'll create a CSS file for styling

const Notification = ({ message, type, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 3000); // Auto-close after 3 seconds
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`notification ${type}`}>
      <span>{message}</span>
      <button onClick={onClose}>&times;</button>
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
