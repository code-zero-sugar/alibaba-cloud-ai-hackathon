// ChatMessage.jsx
import { Paper, Typography, Box, Avatar, Chip, Button } from "@mui/material";
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

    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

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

    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async () => {
        if (!message.incident_report) return;

        try {
            setIsSubmitting(true);

            const reportToSubmit = [
                {
                    ...message.incident_report,
                    reported_by: null,
                },
            ];

            const response = await fetch(`${API_URL}/incident_report`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(reportToSubmit),
            });

            if (!response.ok) throw new Error("Failed to submit report");

            alert("Report submitted successfully!");
        } catch (err) {
            console.error(err);
            alert("Failed to submit report.");
        } finally {
            setIsSubmitting(false);
        }
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

                {/* Inline Incident Report */}
                {message.incident_report && (
                    <Box
                        mt={2}
                        p={2}
                        bgcolor="#fff"
                        borderRadius={2}
                        border="1px solid #cbd5e1"
                    >
                        <Typography
                            variant="subtitle1"
                            fontWeight="bold"
                            gutterBottom
                        >
                            Incident Report
                        </Typography>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                            <strong>Description:</strong>{" "}
                            {message.incident_report.desc}
                        </Typography>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                            <strong>Explanation:</strong>{" "}
                            {message.incident_report.explanation}
                        </Typography>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                            <strong>Action Taken:</strong>{" "}
                            {message.incident_report.action}
                        </Typography>
                        {message.incident_report.reported_by && (
                            <Typography variant="body2" sx={{ mb: 2 }}>
                                <strong>Reported By:</strong>{" "}
                                {message.incident_report.reported_by}
                            </Typography>
                        )}
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleSubmit}
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? "Submitting..." : "Submit Report"}
                        </Button>
                    </Box>
                )}

                {/* Render clickable badges if any reports are provided */}
                {message.incident_reports &&
                    message.incident_reports.length > 0 && (
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
            <ReportDialog
                open={open}
                handleClose={handleClose}
                selectedReport={selectedReport}
            />
        </Box>
    );
};

export default ChatMessage;
