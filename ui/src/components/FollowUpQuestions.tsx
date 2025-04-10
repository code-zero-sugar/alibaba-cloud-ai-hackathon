import React from "react";
import {
    Box,
    Typography,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
} from "@mui/material";
import ArrowRightIcon from "@mui/icons-material/ArrowRight";

const FollowUpQuestions = ({ questions }: { questions: string[] }) => {
    if (!questions || questions.length === 0) return null;

    return (
        <Box mt={2}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                Follow-up Questions:
            </Typography>
            <List dense>
                {questions.map((question, index) => (
                    <ListItem key={index}>
                        <ListItemIcon>
                            <ArrowRightIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={question} />
                    </ListItem>
                ))}
            </List>
        </Box>
    );
};

export default FollowUpQuestions;
