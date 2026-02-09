import React from 'react';

const EmptyState = ({ message = "No items to display.", children }) => {
  return (
    <div className="empty-state">
      <p>{message}</p>
      {children}
    </div>
  );
};

export default EmptyState;
