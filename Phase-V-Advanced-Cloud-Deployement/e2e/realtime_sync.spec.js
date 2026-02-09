// e2e/realtime_sync.spec.js
import { test, expect } from '@playwright/test';

test.describe('Real-time Synchronization across multiple clients', () => {

  test('should reflect task creation in real-time on another client', async ({ browser }) => {
    // Open two browser contexts to simulate two clients
    const client1 = await browser.newPage();
    const client2 = await browser.newPage();

    await client1.goto('/'); // Assuming the app runs on the root URL
    await client2.goto('/');

    // Client 1 creates a task
    await client1.fill('input[type="text"]', 'create task Real-time Sync Test Task');
    await client1.press('input[type="text"]', 'Enter');
    await expect(client1.locator('.bot')).toContainText('Task "Real-time Sync Test Task" requested.');

    // Wait for client 2 to receive the update via WebSocket
    await client2.waitForFunction(() => document.body.textContent.includes('Real-time Sync Test Task'));

    // Verify client 2's task list shows the new task
    await expect(client2.locator('ul > li')).toContainText('Real-time Sync Test Task');
    await expect(client2.locator('.system')).toContainText('Real-time update: TASK_CREATED');

    // Extract task ID from client 1's bot message
    const botMessage1 = await client1.locator('.bot').last().textContent();
    const taskIdMatch1 = botMessage1.match(/Task "Real-time Sync Test Task" created with ID (\S+)\./);
    const taskId = taskIdMatch1 ? taskIdMatch1[1] : null;

    if (taskId) {
        // Client 2 marks the task as complete
        await client2.fill('input[type="text"]', `complete task ${taskId}`);
        await client2.press('input[type="text"]', 'Enter');
        await expect(client2.locator('.bot')).toContainText(`Task "${taskId}" completion requested.`);

        // Wait for client 1 to receive the update
        await client1.waitForFunction(id => document.body.textContent.includes(`Task "${id}" marked as complete.`), taskId);
        
        // Verify client 1's task list reflects the status change
        await expect(client1.locator(`ul > li:has-text("Real-time Sync Test Task")`)).toContainText('(completed)');
        await expect(client1.locator('.system')).toContainText('Real-time update: TASK_UPDATED');

        // Client 1 deletes the task
        await client1.fill('input[type="text"]', `delete task ${taskId}`);
        await client1.press('input[type="text"]', 'Enter');
        await expect(client1.locator('.bot')).toContainText(`Task "${taskId}" deletion requested.`);

        // Wait for client 2 to receive the update
        await client2.waitForFunction(id => !document.body.textContent.includes(`Task "${id}"`), taskId);

        // Verify client 2's task list no longer shows the task
        await expect(client2.locator('ul > li')).not.toContainText('Real-time Sync Test Task');
        await expect(client2.locator('.system')).toContainText('Real-time update: TASK_DELETED');
    } else {
        test.fail('Could not extract Task ID from bot message on Client 1.');
    }

    await client1.close();
    await client2.close();
  });
});
