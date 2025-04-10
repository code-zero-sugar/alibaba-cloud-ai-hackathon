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

const INVESTIGATION_URL =
    import.meta.env.VITE_WS_URL + "/ws/investigation" ||
    "ws://localhost:8000/ws/investigation";
const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000";
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const Investigator = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", content: "Hello! How can I help you today?" },
  ]);
  const [isWaitingBot, setIsWaitingBot] = useState(false);

  const handleSendMessage = useCallback(
    (content: string) => {
      const userMessage = { role: "user", content };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setIsWaitingBot(true);
      sendWebSocketMessage(INVESTIGATION_URL, userMessage.content);
    },
    [setMessages, setIsWaitingBot]
  );

  useEffect(() => {
    connectWebSocket(WS_URL + "/ws/investigation", (rawData) => {
      const data = JSON.parse(rawData);

      const botMessage = {
        role: "bot",
        content: data.response,
        incident_reports: data.reference_incident_reports,
      };
      console.log(botMessage.incident_reports);
      setIsWaitingBot(false);
      setMessages((prev) => [...prev, botMessage as Message]);
    });

    return () => {
      disconnectWebSocket(INVESTIGATION_URL);
    };
  }, []);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
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
            fontWeight: 'bold',
          }}
        >
          Investigator
        </Typography>
        <ChatMessages messages={messages} isWaitingBot={isWaitingBot} />
        <ChatInput onSend={handleSendMessage} isWaitingBot={isWaitingBot} />
      </Box>
    </Container>
  );
};
