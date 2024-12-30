from fastapi import Body, HTTPException
import random
from utils.vectorstore import upsert_video_memory

from dummy_embedding import dummy_embedding

def create_video_memory(payload: dict = Body(...)):
    """
    Expects JSON, e.g.: { "videoData": "<base64 or URL>" }
    We'll do a dummy embedding. In real usage, parse frames or run a summarizer -> embed the summary.
    """
    video_data = payload.get("videoData", "")
    if not video_data:
        raise HTTPException(status_code=400, detail="No video data")

    # Example embedding from a summary or screenshot
    embedding = dummy_embedding("video:" + video_data, length=8)
    upsert_video_memory({"base64_or_url": video_data}, embedding)
    return {"message": "Video memory upserted"}
