import { useCallback, useEffect, useState } from "react";
import { Container, Box, Typography } from "@mui/material";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";
import { Message } from "./models";
import {
    connectWebSocket,
    disconnectWebSocket,
    sendWebSocketMessage,
} from "../services/websocket/socketClient";

const REPORTING_WS_URL =
    import.meta.env.VITE_WS_URL + "/ws/reporting" ||
    "ws://localhost:8000/ws/reporting";

export const ReportingBot = () => {
    const [messages, setMessages] = useState<Message[]>([
        { role: "bot", content: "Hi, What do you want to report?" },
    ]);
    const [isWaitingBot, setIsWaitingBot] = useState(false);

    const handleSendMessage = useCallback(
        (content: string) => {
            const userMessage = { role: "user", content };
            setMessages((prevMessages) => [...prevMessages, userMessage]);
            setIsWaitingBot(true);
            sendWebSocketMessage(REPORTING_WS_URL, userMessage.content);
        },
        [setMessages, setIsWaitingBot]
    );

    useEffect(() => {
        connectWebSocket(REPORTING_WS_URL, (data) => {
            const botMessage = {
                role: "bot",
                content: data,
            };
            setIsWaitingBot(false);
            setMessages((prev) => [...prev, botMessage as Message]);
        });

        return () => {
            disconnectWebSocket(REPORTING_WS_URL);
        };
    }, []);

    return (
        <Container maxWidth="sm">
            <Box
                sx={{
                    marginTop: 4,
                    padding: 3,
                    border: "1px solid #ddd",
                    borderRadius: 2,
                    boxShadow: 3,
                    backgroundColor: "white",
                }}
            >
                <Typography variant="h5" gutterBottom>
                    Reporting Bot
                </Typography>
                <ChatMessages messages={messages} isWaitingBot={isWaitingBot} />
                <ChatInput
                    onSend={handleSendMessage}
                    isWaitingBot={isWaitingBot}
                />
            </Box>
        </Container>
    );
};
