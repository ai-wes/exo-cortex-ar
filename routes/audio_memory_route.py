from fastapi import Body, HTTPException
import random
from utils.vectorstore import upsert_audio_memory
def dummy_embedding(text: str, length=8):
    return [random.random() for _ in range(length)]

def create_audio_memory(payload: dict = Body(...)):
    """
    Expects JSON: { "transcription": "text from STT" }
    """
    transcription = payload.get("transcription", "")
    if not transcription:
        raise HTTPException(status_code=400, detail="No transcription")

    # Generate embedding from transcription
    embedding = dummy_embedding(transcription, length=8)
    upsert_audio_memory(transcription, embedding)
    return {"message": "Audio memory (STT) upserted"}
