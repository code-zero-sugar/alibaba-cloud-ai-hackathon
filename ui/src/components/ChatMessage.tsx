// ChatMessage.jsx
import {
  Paper,
  Typography,
  Box,
  Avatar,
  Chip
} from "@mui/material";
import { Message } from "./models";
import ReactMarkdown from "react-markdown";
import { useState } from "react";
import ReportDialog from "./ReportDialog";

export type IncidentReportDto = {
  id: number;
  desc: string;
  explanation: string;
  action: string;
  reported_by?: string | null;
  created_at: string;
  updated_at: string;
};

type ChatMessageProps = {
  message: Message;
};

const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === "user";

  const userAvatar = "/avatar/nurse.png"; // Replace with your user avatar image URL
  const botAvatar = "/avatar/robot.png"; // Replace with your bot avatar image URL

  // State for modal dialog
  const [open, setOpen] = useState(false);
  const [selectedReport, setSelectedReport] =
    useState<IncidentReportDto | null>(null);

  const handleClickOpen = (report: IncidentReportDto) => {
    setSelectedReport(report);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedReport(null);
  };

  return (
    <Box
      display="flex"
      alignItems="flex-start"
      justifyContent={isUser ? "flex-end" : "flex-start"}
      mb={2}
    >
      {/* Avatar for bot messages on the left */}
      {!isUser && (
        <Avatar alt="Bot" src={botAvatar} sx={{ marginRight: 1 }}>
          B
        </Avatar>
      )}

      <Paper
        elevation={3}
        sx={{
          p: 1.5,
          backgroundColor: isUser ? "#dbeafe" : "#bfdbfe", // User: blue-100; Bot: blue-200
          maxWidth: "70%",
          borderRadius: 2,
        }}
      >
        <Typography variant="body1">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </Typography>

        {/* Render clickable badges if any reports are provided */}
        {message.incident_reports && message.incident_reports.length > 0 && (
          <Box mt={2}>
            {message.incident_reports.map((report) => (
              <Chip
                key={report.id}
                label={`R - ${report.id}`}
                clickable
                color="primary"
                onClick={() => handleClickOpen(report)}
                sx={{ marginRight: 1, marginBottom: 1 }}
              />
            ))}
          </Box>
        )}
      </Paper>

      {/* Avatar for user messages on the right */}
      {isUser && (
        <Avatar alt="User" src={userAvatar} sx={{ marginLeft: 1 }}>
          U
        </Avatar>
      )}

      {/* Modal for displaying report details */}
      <ReportDialog open={open} handleClose={handleClose} selectedReport={selectedReport}/>
    </Box>
  );
};

export default ChatMessage;
