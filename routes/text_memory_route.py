from fastapi import Body, HTTPException
import random

from dummy_embedding import dummy_embedding

def create_text_memory(payload: dict = Body(...)):
    """
    Expects JSON: { "content": "some text" }
    """
    text_content = payload.get("content", "")
    if not text_content:
        raise HTTPException(status_code=400, detail="No text content provided")

    # Generate text embedding:
    embedding = dummy_embedding(text_content, length=8)

    # Upsert into VectorStore
    upsert_text_memory(text_content, embedding)
    return {"message": "Text memory upserted into VectorStore"}
