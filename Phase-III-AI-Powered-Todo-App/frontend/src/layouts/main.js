import React from 'react';
import ChatPage from '../pages/chat'; // Assuming ChatPage is the main chat interface
// import TodoDashboard from '../pages/todo_dashboard'; // Placeholder for future todo display

const MainLayout = () => {
  return (
    <div className="main-layout">
      <header className="app-header">
        <h1>Todo AI Chatbot</h1>
      </header>
      <div className="content-area">
        <aside className="todo-sidebar">
          {/* <TodoDashboard /> */}
          <p>Todo items will be displayed here.</p>
        </aside>
        <main className="chat-main">
          <ChatPage />
        </main>
      </div>
      <footer className="app-footer">
        <p>© 2026 Todo AI Chatbot</p>
      </footer>
    </div>
  );
};

export default MainLayout;
