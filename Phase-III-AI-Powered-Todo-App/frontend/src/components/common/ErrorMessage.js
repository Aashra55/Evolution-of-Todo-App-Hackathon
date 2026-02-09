import React from 'react';

const ErrorMessage = ({ message = "An unexpected error occurred.", children }) => {
  return (
    <div className="error-message">
      <p>Error: {message}</p>
      {children}
    </div>
  );
};

export default ErrorMessage;
