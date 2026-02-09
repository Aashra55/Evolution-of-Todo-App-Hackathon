// services/chat_api.js
// This service module handles communication with the backend Chat API.

// Base URL for the API (adjust if running on a different port or path)
// In a real app, this might come from environment variables.
const API_BASE_URL = '/api'; // Assuming API routes are prefixed with /api

// Mock functions for API calls - replace with actual fetch/axios calls
// These mocks simulate responses from the backend.

async function handleApiResponse(response) {
    if (!response.ok) {
        // Handle HTTP errors
        const errorData = await response.json().catch(() => ({ message: "Unknown error" }));
        throw new Error(`HTTP error ${response.status}: ${errorData.message || response.statusText}`);
    }
    return response.json();
}

export async function getTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);
        return await handleApiResponse(response);
    } catch (error) {
        console.error("API Error fetching tasks:", error);
        throw error;
    }
}

export async function createTask(taskData) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        });
        return await handleApiResponse(response);
    } catch (error) {
        console.error("API Error creating task:", error);
        throw error;
    }
}

export async function updateTask(taskId, taskData) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        });
        return await handleApiResponse(response);
    } catch (error) {
        console.error("API Error updating task:", error);
        throw error;
    }
}

export async function deleteTask(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ message: "Unknown error" }));
            throw new Error(`HTTP error ${response.status}: ${errorData.message || response.statusText}`);
        }
        // DELETE operations often return 204 No Content, so no JSON parsing needed
        return true; 
    } catch (error) {
        console.error("API Error deleting task:", error);
        throw error;
    }
}

export async function completeTask(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}), // Body might be empty for this endpoint
        });
        return await handleApiResponse(response);
    } catch (error) {
        console.error("API Error completing task:", error);
        throw error;
    }
}

// Placeholder for sending chat messages to AI
export async function sendChatMessage(message, sessionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message, sessionId }),
        });
        return await handleApiResponse(response);
    } catch (error) {
        console.error("API Error sending chat message:", error);
        throw error;
    }
}
