// frontend/src/config/logging.js

const configureLogging = () => {
  // Basic logger for client-side, can be extended with external logging services
  const logger = {
    info: (...args) => console.log('INFO:', ...args),
    warn: (...args) => console.warn('WARN:', ...args),
    error: (...args) => console.error('ERROR:', ...args),
    debug: (...args) => console.debug('DEBUG:', ...args),
  };

  // Attach to window for easy access in browser console
  if (typeof window !== 'undefined') {
    window.appLogger = logger;
  }

  return logger;
};

export const appLogger = configureLogging();
