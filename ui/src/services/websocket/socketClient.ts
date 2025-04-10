type MessageCallback = (data: string) => void;

interface WebSocketInstance {
    socket: WebSocket;
    onMessage: MessageCallback;
}

const webSocketPool: Map<string, WebSocketInstance> = new Map();

export const connectWebSocket = (
    url: string,
    onMessage: (data: string) => void
) => {
    if (webSocketPool.has(url)) {
        console.warn(`WebSocket for [${url}] already exists.`);
        return;
    }

    const socket = new WebSocket(url);

    socket.onopen = () => {
        webSocketPool.set(url, { socket, onMessage });
        console.log(`WebSocket connected to ${url}`);
    };

    socket.onmessage = (event) => {
        console.log(`WebSocket [${url}] received:`, event.data);
        onMessage(event.data);
    };

    socket.onclose = () => {
        console.log(`WebSocket [${url}] disconnected`);
        webSocketPool.delete(url);
    };

    socket.onerror = (error) => {
        console.error(`WebSocket [${url}] error:`, error);
    };
};

/**
 * Sends a message to the specified WebSocket.
 * @param url - The WebSocket URL used as key.
 * @param message - The message to send.
 */
export const sendWebSocketMessage = (url: string, message: string) => {
    console.log(webSocketPool);

    const wsInstance = webSocketPool.get(url);
    if (wsInstance) {
        wsInstance.socket.send(message);
        console.log(`Message sent to WebSocket [${url}]:`, message);
    } else {
        console.error(`WebSocket [${url}] is not open or doesn't exist.`);
    }
};

/**
 * Gracefully disconnects the WebSocket for the given URL.
 * @param url - The WebSocket URL used as key.
 */
export const disconnectWebSocket = (url: string) => {
    const wsInstance = webSocketPool.get(url);
    if (wsInstance) {
        const readyState = wsInstance.socket.readyState;
        if (
            readyState === WebSocket.OPEN ||
            readyState === WebSocket.CONNECTING
        ) {
            wsInstance.socket.close();
            console.log(`WebSocket [${url}] manually disconnected.`);
        } else {
            console.warn(
                `WebSocket [${url}] is not open or connecting (state: ${readyState}). Skipping close.`
            );
        }
        webSocketPool.delete(url);
    } else {
        console.warn(`WebSocket [${url}] not found.`);
    }
};
