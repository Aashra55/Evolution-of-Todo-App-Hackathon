import React from 'react';

const LoadingIndicator = ({ message = "Loading...", children }) => {
  return (
    <div className="loading-indicator">
      <p>{message}</p>
      {children}
    </div>
  );
};

export default LoadingIndicator;
