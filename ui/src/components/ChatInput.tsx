// ChatInput.jsx
import { useState } from "react";
import { Box, TextField, IconButton } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import AudioRecorder from "./AudioRecorder";

type ChatInputProps = {
    onSend: (message: string) => void;
    isWaitingBot: boolean;
};

const ChatInput = ({ onSend, isWaitingBot }: ChatInputProps) => {
    const [inputValue, setInputValue] = useState("");

    const handleSend = () => {
        if (inputValue.trim() !== "") {
            onSend(inputValue.trim());
            setInputValue("");
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            // Prevent form submission if wrapping in a form element.
            e.preventDefault();
            handleSend();
        }
    };

  return (
    <Box display="flex" alignItems="center" mt={2}>
      <AudioRecorder onTranscribedText={setInputValue} />
      <TextField
        variant="outlined"
        placeholder="Type your message..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isWaitingBot}
        fullWidth
      />
      <IconButton color="primary" onClick={handleSend}>
        <SendIcon />
      </IconButton>
    </Box>
  );
};

export default ChatInput;
