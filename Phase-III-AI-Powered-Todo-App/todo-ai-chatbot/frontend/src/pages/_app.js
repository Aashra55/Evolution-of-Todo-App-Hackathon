// frontend/src/pages/_app.js
import Head from 'next/head'; // Import Head component
import '../components/Notifications.css'; // Global Notifications styles
import '../styles/responsive.css'; // Global responsive styles
import '../styles/custom-neon.css'; // Custom neon styles

function MyApp({ Component, pageProps }) {
  return (
    <>
      {/* Removed <Head> component with link tags as they are moved to _document.js */}
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
