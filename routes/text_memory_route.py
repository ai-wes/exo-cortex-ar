from fastapi import Body, HTTPException
import random
from utils.vectorstore import upsert_text_memory
from typing import List
from datetime import datetime

def dummy_embedding(text: str, length=8):
    return [random.random() for _ in range(length)]

def create_text_memory(payload: dict = Body(...)):
    """
    Expects JSON: {
        "title": str,
        "content": str,
        "tags": List[str],
        "timestamp": str
    }
    """
    content = payload.get("content", "")
    if not content:
        raise HTTPException(status_code=400, detail="No text content provided")

    # Optional fields with defaults
    title = payload.get("title", "Text Memory")
    tags = payload.get("tags", ["text"])
    timestamp = payload.get("timestamp", datetime.now().isoformat())

    # Generate text embedding
    embedding = dummy_embedding(content, length=8)

    # Upsert into VectorStore with all metadata
    upsert_text_memory(
        content=content,
        embedding=embedding,
        metadata={
            "title": title,
            "tags": tags,
            "timestamp": timestamp
        }
    )
    
    return {
        "message": "Text memory saved successfully",
        "data": {
            "title": title,
            "content": content,
            "tags": tags,
            "timestamp": timestamp
        }
    }
