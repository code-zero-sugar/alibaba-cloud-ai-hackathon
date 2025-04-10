import { useState, useRef, useEffect } from "react";
import { uploadAudio } from "../services/transcribe"; // your transcription backend call

type VoiceInputStatus = "idle" | "recording" | "transcribing" | "done";

export const useVoiceInput = () => {
    const [status, setStatus] = useState<VoiceInputStatus>("idle");
    const [transcript, setTranscript] = useState<string | null>(null);
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
    const [error, setError] = useState<string | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const audioChunksRef = useRef<Blob[]>([]);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
        });
        mediaRecorderRef.current = new MediaRecorder(stream);
        audioChunksRef.current = [];

        mediaRecorderRef.current.ondataavailable = (e) => {
            audioChunksRef.current.push(e.data);
        };

        mediaRecorderRef.current.onstop = () => {
            const blob = new Blob(audioChunksRef.current, {
                type: "audio/webm",
            });
            setAudioBlob(blob);
            setStatus("transcribing");
        };

        mediaRecorderRef.current.start();
        setStatus("recording");
        setTranscript(null);
        setError(null);
    };

    const stopRecording = () => {
        mediaRecorderRef.current?.stop();
    };

    const toggleRecording = () => {
        if (status === "recording") {
            stopRecording();
        } else {
            startRecording();
        }
    };

    const reset = () => {
        setStatus("idle");
        setTranscript(null);
        setAudioBlob(null);
        setError(null);
    };

    // Auto-transcribe when blob is ready
    useEffect(() => {
        const runTranscription = async () => {
            if (status === "transcribing" && audioBlob) {
                try {
                    const result = await uploadAudio(audioBlob);
                    setTranscript(result?.result || "");
                    setStatus("done");
                } catch (err) {
                    setError((err as Error).message);
                    setStatus("idle");
                }
            }
        };
        runTranscription();
    }, [status, audioBlob]);

    return {
        status,
        isRecording: status === "recording",
        isLoading: status === "transcribing",
        transcript,
        audioBlob,
        error,
        toggleRecording,
        reset,
    };
};
