// frontend/tests/unit/test_frontend_components.js
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../../src/components/App';
import ChatInput from '../../src/components/ChatInput';
import ChatDisplay from '../../src/components/ChatDisplay';
import TaskListPanel from '../../src/components/TaskListPanel';
import Notifications from '../../src/components/Notifications';

// Mock uuid for consistent IDs in tests
jest.mock('uuid', () => ({
  v4: () => 'mock-uuid',
}));

describe('App Component', () => {
  test('renders AI-powered Todo Chatbot heading', () => {
    render(<App />);
    expect(screen.getByText(/AI-powered Todo Chatbot/i)).toBeInTheDocument();
  });

  // More integration tests would go here, simulating API calls
});

describe('ChatInput Component', () => {
  test('renders an input field and a send button', () => {
    render(<ChatInput onSendMessage={() => {}} />);
    expect(screen.getByPlaceholderText(/Type your message.../i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Send/i })).toBeInTheDocument();
  });
});

describe('ChatDisplay Component', () => {
  test('renders messages correctly', () => {
    const messages = [
      { sender: 'user', text: 'Hello AI' },
      { sender: 'ai', text: 'Hello User' },
    ];
    render(<ChatDisplay messages={messages} />);
    expect(screen.getByText(/Hello AI/i)).toBeInTheDocument();
    expect(screen.getByText(/Hello User/i)).toBeInTheDocument();
  });

  test('renders tasks from a JSON message', () => {
    const messages = [
      { sender: 'ai', text: JSON.stringify({ status: 'success', message: 'Here are tasks', tasks: [{ id: '1', title: 'Test Task', completed: false }] }) },
    ];
    render(<ChatDisplay messages={messages} />);
    expect(screen.getByText(/Here are tasks/i)).toBeInTheDocument();
    expect(screen.getByText(/Test Task/i)).toBeInTheDocument();
  });
});

describe('TaskListPanel Component', () => {
  test('renders pending and completed tasks', () => {
    const tasks = [
      { id: '1', title: 'Pending Task', completed: false },
      { id: '2', title: 'Completed Task', completed: true },
    ];
    render(<TaskListPanel tasks={tasks} />);
    expect(screen.getByText(/Pending Task/i)).toBeInTheDocument();
    expect(screen.getByText(/Completed Task/i)).toBeInTheDocument();
  });
});

describe('Notifications Component', () => {
  test('renders notifications', () => {
    const notifications = [
      { id: '1', message: 'Task added!', type: 'success' },
    ];
    render(<Notifications notifications={notifications} removeNotification={() => {}} />);
    expect(screen.getByText(/Task added!/i)).toBeInTheDocument();
  });
});
