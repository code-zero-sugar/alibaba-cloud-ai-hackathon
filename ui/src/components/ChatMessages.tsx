// ChatMessages.jsx
import { useEffect, useRef } from "react";
import { Box } from "@mui/material";
import ChatMessage from "./ChatMessage";
import { Message } from "./models";

type ChatMessagesProps = {
  messages: Message[];
  isWaitingBot: boolean;
};

const ChatMessages = ({ messages, isWaitingBot }: ChatMessagesProps) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <Box
      sx={{
        height: "80%",
        overflowY: "auto",
        p: 5,
        mt: 2,
        backgroundColor: "#ebf8ff", // light blue background (similar to Tailwind's bg-blue-50)
        border: "1px solid #bfdbfe", // light blue border (similar to Tailwind's border-blue-200)
        borderRadius: 4,
      }}
    >
      {messages.map((message, index) => (
        <ChatMessage key={index} message={message} />
      ))}
      {isWaitingBot && (
        <ChatMessage
          message={{
            role: "bot",
            content: "Thinking...",
          }}
        />
      )}
      {/* Empty div to scroll to the bottom */}
      <div ref={messagesEndRef} />
    </Box>
  );
};

export default ChatMessages;
