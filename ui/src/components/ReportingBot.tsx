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
            sendWebSocketMessage(
                REPORTING_WS_URL,
                JSON.stringify([...messages, userMessage])
            );
        },
        [messages, setMessages, setIsWaitingBot]
    );

    useEffect(() => {
        connectWebSocket(REPORTING_WS_URL, (data) => {
            const parsed = JSON.parse(data); // Convert JSON string to object
            const botMessage = {
                role: "bot",
                content: parsed.message, // Now safe to access
            };
            if (parsed.incident_report) {
                (botMessage as Message).incident_report =
                    parsed.incident_report;
            }
            setIsWaitingBot(false);
            setMessages((prev) => [...prev, botMessage as Message]);
        });

        return () => {
            disconnectWebSocket(REPORTING_WS_URL);
        };
    }, []);

    return (
        <Container maxWidth="lg" sx={{ mt: 4 }}>
            <Box
                sx={{
                    p: 3,
                    height: "80vh",
                    border: "1px solid #93c5fd", // light blue border (similar to Tailwind's border-blue-300)
                    borderRadius: 5,
                    boxShadow: "0 0 10px 2px rgba(29, 78, 216, 0.6)",
                    backgroundColor: "white",
                }}
            >
                <Typography
                    variant="h5"
                    gutterBottom
                    sx={{
                        color: "#1D4ED8",
                        fontWeight: "bold",
                    }}
                >
                    Dr. Report
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
