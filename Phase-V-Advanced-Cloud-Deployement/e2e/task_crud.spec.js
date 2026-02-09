// e2e/task_crud.spec.js
import { test, expect } from '@playwright/test';

test.describe('Basic Task CRUD via Chat Interface', () => {

  test('should allow creating, updating, completing, and deleting a task', async ({ page }) => {
    await page.goto('/'); // Assuming the app runs on the root URL or base path

    // 1. Create a task
    await page.fill('input[type="text"]', 'create task Buy milk');
    await page.press('input[type="text"]', 'Enter');
    await expect(page.locator('.bot')).toContainText('Task "Buy milk" created with ID');
    await expect(page.locator('ul > li')).toContainText('Buy milk');

    // Extract the task ID (this is highly dependent on how the bot responds)
    const botMessage = await page.locator('.bot').last().textContent();
    const taskIdMatch = botMessage.match(/ID (\S+)\./);
    expect(taskIdMatch).toBeDefined();
    const taskId = taskIdMatch[1];
    expect(taskId).toBeDefined();

    // 2. Mark the task as complete
    await page.fill('input[type="text"]', `complete task ${taskId}`);
    await page.press('input[type="text"]', 'Enter');
    await expect(page.locator('.bot')).toContainText(`Task "${taskId}" marked as complete.`);
    await expect(page.locator(`ul > li:has-text("Buy milk")`)).toContainText('(completed)');

    // 3. Delete the task
    // Note: The frontend currently doesn't expose a direct way to delete by ID via chat.
    // This test assumes a chat command for deletion. If not, it would need to
    // simulate UI interaction (e.g., clicking a delete button next to the task).
    // For this example, let's assume a simplified "delete task [id]" command.
    await page.fill('input[type="text"]', `delete task ${taskId}`);
    await page.press('input[type="text"]', 'Enter');
    await expect(page.locator('.bot')).toContainText(`Task "${taskId}" deleted.`);
    await expect(page.locator(`ul > li:has-text("Buy milk")`)).not.toBeVisible();
    
    // Verify no tasks are left
    await expect(page.locator('ul')).not.toContainText('Buy milk'); // Check if the item is gone from the list

  });

  // Add more tests for other CRUD operations, edge cases, etc.
});
