// frontend/src/pages/_app.js
import Head from 'next/head'; // Import Head component
import '../components/Notifications.css'; // Global Notifications styles
import '../styles/responsive.css'; // Global responsive styles

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
