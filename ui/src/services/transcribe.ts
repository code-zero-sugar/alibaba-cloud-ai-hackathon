const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const uploadAudio = async (audioBlob: Blob) => {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.webm");

    const response = await fetch(`${API_URL}/upload-audio`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Upload failed");
    }

    return response.json();
};
