import React from "react";
import IconButton from "@mui/material/IconButton";
import MicIcon from "@mui/icons-material/Mic";
import StopIcon from "@mui/icons-material/Stop";
import CircularProgress from "@mui/material/CircularProgress";
import { useVoiceInput } from "../hooks/useVoiceInput";

interface Props {
    onTranscribedText: (text: string) => void;
}

const AudioRecorder: React.FC<Props> = ({ onTranscribedText }) => {
    const {
        isRecording,
        isLoading,
        transcript,
        toggleRecording,
        reset,
        error,
    } = useVoiceInput();

    // Handle result when ready
    React.useEffect(() => {
        if (transcript) {
            onTranscribedText(transcript);
            reset(); // optional: clear state after use
        }
    }, [onTranscribedText, reset, transcript]);

    const renderIcon = () => {
        if (isLoading) return <CircularProgress size={24} />;
        if (isRecording) return <StopIcon />;
        return <MicIcon />;
    };

    return (
        <div className="flex items-center gap-2">
            <IconButton onClick={toggleRecording} color="primary">
                {renderIcon()}
            </IconButton>
            {error && <span className="text-red-500">{error}</span>}
        </div>
    );
};

export default AudioRecorder;
