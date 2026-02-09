// frontend/src/services/realtime_sync.js
// This module handles WebSocket communication with the Real-time Sync Service.

const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8003/ws'; // Default WebSocket URL

let websocket = null;
let reconnectInterval = 1000; // Start with 1 second
const maxReconnectInterval = 30000; // Max 30 seconds

export const connectWebSocket = (onMessageCallback) => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        console.log("WebSocket is already connected.");
        return;
    }

    websocket = new WebSocket(WS_BASE_URL);

    websocket.onopen = () => {
        console.log('WebSocket connected.');
        reconnectInterval = 1000; // Reset reconnect interval on successful connection
    };

    websocket.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            if (onMessageCallback) {
                onMessageCallback(message);
            }
        } catch (error) {
            console.error("Error parsing WebSocket message:", error);
        }
    };

    websocket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.reason);
        websocket = null; // Clear the old WebSocket instance
        // Attempt to reconnect after a delay
        setTimeout(() => {
            console.log(`Attempting to reconnect in ${reconnectInterval / 1000} seconds...`);
            reconnectInterval = Math.min(reconnectInterval * 2, maxReconnectInterval);
            connectWebSocket(onMessageCallback);
        }, reconnectInterval);
    };

    websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        websocket.close(); // Close to trigger onclose and reconnection logic
    };
};

export const disconnectWebSocket = () => {
    if (websocket) {
        websocket.close();
        websocket = null;
        console.log('WebSocket manually disconnected.');
    }
};

export const sendWebSocketMessage = (message) => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify(message));
    } else {
        console.warn('WebSocket is not connected. Message not sent:', message);
    }
};

// Example: send a heartbeat message
export const sendHeartbeat = () => {
    sendWebSocketMessage({ type: 'HEARTBEAT', timestamp: new Date().toISOString() });
};
