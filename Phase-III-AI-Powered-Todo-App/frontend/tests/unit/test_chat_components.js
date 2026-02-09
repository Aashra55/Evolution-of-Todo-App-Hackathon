import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatInput from '../../src/components/chat/ChatInput';
import ChatWindow from '../../src/components/chat/ChatWindow';

// Mocking the environment variable for chat_api.js if it were to be imported
// process.env.REACT_APP_API_BASE_URL = 'http://localhost:8000'; 

describe('ChatInput', () => {
  test('renders input field and send button', () => {
    render(<ChatInput onSendMessage={() => {}} />);
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument();
  });

  test('calls onSendMessage with input value when button is clicked', () => {
    const mockOnSendMessage = jest.fn();
    render(<ChatInput onSendMessage={mockOnSendMessage} />);
    const inputElement = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    fireEvent.change(inputElement, { target: { value: 'Hello bot' } });
    fireEvent.click(sendButton);

    expect(mockOnSendMessage).toHaveBeenCalledTimes(1);
    expect(mockOnSendMessage).toHaveBeenCalledWith('Hello bot');
    expect(inputElement).toHaveValue(''); // Input should be cleared
  });

  test('does not call onSendMessage with empty message', () => {
    const mockOnSendMessage = jest.fn();
    render(<ChatInput onSendMessage={mockOnSendMessage} />);
    const sendButton = screen.getByRole('button', { name: /send/i });

    fireEvent.click(sendButton); // Click without typing anything
    expect(mockOnSendMessage).not.toHaveBeenCalled();
  });
});

describe('ChatWindow', () => {
  test('renders messages correctly', () => {
    const messages = [
      { role: 'user', content: 'Hi there!' },
      { role: 'bot', content: 'Hello!' },
    ];
    render(<ChatWindow messages={messages} />);

    expect(screen.getByText(/hi there!/i)).toBeInTheDocument();
    expect(screen.getByText(/hello!/i)).toBeInTheDocument();
    expect(screen.getByText('user:', { exact: false })).toBeInTheDocument();
    expect(screen.getByText('bot:', { exact: false })).toBeInTheDocument();
  });

  test('renders empty message list', () => {
    render(<ChatWindow messages={[]} />);
    expect(screen.queryByText(/user:/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/bot:/i)).not.toBeInTheDocument();
  });
});
