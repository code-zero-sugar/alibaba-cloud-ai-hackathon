from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.audio.file_handler import save_audio_file
from app.services.audio.transcribe_service import process

router = APIRouter()


@router.post("/upload-audio")
async def upload_audio(audio: UploadFile = File(...)):
    try:
        filepath = await save_audio_file(audio)
        result = process(filepath)  # Call the transcription process
        return {"message": "Upload successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
