import { test, expect } from '@playwright/test';

test.describe('Todo AI Chatbot E2E Tests', () => {
  test('should allow user to login and send a chat message', async ({ page }) => {
    // Navigate to the app (assuming it's running locally)
    await page.goto('http://localhost:3000'); // Assuming React app runs on port 3000

    // Wait for login simulation to complete (e.g., "Logging in..." message to disappear)
    await expect(page.getByText('Welcome to Todo AI Chatbot!')).toBeVisible();

    // Type a message into the chat input
    await page.getByPlaceholder('Type your message...').fill('Hello bot');
    await page.getByRole('button', { name: 'Send' }).click();

    // Expect user message to appear
    await expect(page.getByText('user: Hello bot')).toBeVisible();

    // Expect bot response to appear (might need to wait for network request)
    await expect(page.getByText('bot: Hello there! How can I help you with your todos today?')).toBeVisible();
  });

  test('should allow user to create a todo via chat', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.getByText('Welcome to Todo AI Chatbot!')).toBeVisible();

    const todoDescription = 'Buy groceries';
    await page.getByPlaceholder('Type your message...').fill(`create todo ${todoDescription}`);
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.getByText(`bot: Todo '${todoDescription}' created`)).toBeVisible();
    // Further assertions would be needed to verify the todo appears in the sidebar etc.
  });

  // Additional tests for listing, updating, deleting todos via chat would go here
});
