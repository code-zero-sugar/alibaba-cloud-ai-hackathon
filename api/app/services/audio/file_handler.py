import uuid
import os
import subprocess
from fastapi import UploadFile

SAVE_DIR = "uploads/audio"
TEMP_DIR = "uploads/temp"


async def save_audio_file(file: UploadFile) -> str:
    os.makedirs(SAVE_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    temp_webm_filename = f"{uuid.uuid4()}.webm"
    temp_webm_path = os.path.join(TEMP_DIR, temp_webm_filename)

    # Save the uploaded .webm temporarily
    contents = await file.read()
    with open(temp_webm_path, "wb") as f:
        f.write(contents)

    # Create a final WAV filename
    final_filename = f"{uuid.uuid4()}.wav"
    final_path = os.path.join(SAVE_DIR, final_filename)

    # Use ffmpeg to convert
    try:
        final_filename = f"{uuid.uuid4()}.pcm"
        final_path = os.path.join(SAVE_DIR, final_filename)

        subprocess.run(
            [
                "ffmpeg",
                "-i",
                temp_webm_path,
                "-f",
                "s16le",  # raw PCM format
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",  # required by Alibaba API
                "-ac",
                "1",  # mono
                final_path,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise Exception("FFmpeg conversion failed") from e
    finally:
        # Clean up temp file
        os.remove(temp_webm_path)

    return final_path
