from fastapi import FastAPI, HTTPException, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from utils.vectorstore import vector_store

from routes.text_memory_route import create_text_memory
from routes.audio_memory_route import create_audio_memory
from routes.image_memory_route import create_image_memory
from routes.video_memory_route import create_video_memory
from routes.spatial_memory_route import create_spatial_memory
# main.py (or a separate file of your choice)

import os
import base64
from uuid import uuid4
from datetime import datetime
from typing import List

from fastapi import FastAPI, File, UploadFile, Body, HTTPException

# LangChain + Deep Lake
from langchain_community.vectorstores import DeepLake
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings

app = FastAPI(title="VectorStore Memory API")

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    # You can add pre-processing logic here
    print(f"Incoming request: {request.method} {request.url}")
    
    # Call the next middleware/route handler
    response = await call_next(request)
    
    # You can add post-processing logic here
    print(f"Outgoing response status code: {response.status_code}")
    
    return response

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ⚠️ Install requirements:
#    pip install --upgrade --quiet langchain-openai langchain-community 'deeplake[enterprise]' tiktoken

# Initialize embeddings & vector store
embedding_function = OpenAIEmbeddings()  
# Adjust dataset_path as desired (local, s3, or hub://...)
db = DeepLake(
    dataset_path="./memories_vectorstore",  
    embedding=embedding_function,
    overwrite=False,
)

# ──────────────────────────────────────────────────────────
# Text Memory
# ──────────────────────────────────────────────────────────
@app.post("/memories/text")
def create_text_memory(
    payload: dict = Body(...)
):
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

    title = payload.get("title", "Text Memory")
    tags = payload.get("tags", ["text"])
    timestamp = payload.get("timestamp", datetime.now().isoformat())

    # Create Document + store
    doc = Document(
        page_content=content,  # embed text directly
        metadata={
            "id": str(uuid4()),
            "type": "text",
            "title": title,
            "tags": tags,
            "timestamp": timestamp,
        }
    )
    db.add_documents([doc])

    return {
        "message": "Text memory saved successfully",
        "data": {
            "title": title,
            "content": content,
            "tags": tags,
            "timestamp": timestamp,
        }
    }

# ──────────────────────────────────────────────────────────
# Image Memory
# ──────────────────────────────────────────────────────────
@app.post("/memories/image")
def create_image_memory(file: UploadFile = File(...)):
    """
    Expects a file upload, e.g. from a multipart/form-data request.
    """
    try:
        # Read bytes + store base64 (in practice, you might store a link to S3)
        image_bytes = file.file.read()
        base64_img = base64.b64encode(image_bytes).decode("utf-8")

        # Document with minimal text but including metadata
        doc = Document(
            page_content="",  # no textual content for images
            metadata={
                "id": str(uuid4()),
                "type": "image",
                "filename": file.filename,
                "base64": base64_img,
            }
        )
        db.add_documents([doc])
        return {"message": "Image memory upserted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ──────────────────────────────────────────────────────────
# Audio Memory
# ──────────────────────────────────────────────────────────
@app.post("/memories/audio")
def create_audio_memory(payload: dict = Body(...)):
    """
    Expects JSON: { "transcription": "some text from STT" }
    """
    transcription = payload.get("transcription", "")
    if not transcription:
        raise HTTPException(status_code=400, detail="No transcription provided")

    doc = Document(
        page_content=transcription,  
        metadata={
            "id": str(uuid4()),
            "type": "audio",
            "transcription": transcription,
        }
    )
    db.add_documents([doc])
    return {"message": "Audio memory (STT) upserted"}

# ──────────────────────────────────────────────────────────
# Video Memory
# ──────────────────────────────────────────────────────────
@app.post("/memories/video")
def create_video_memory(payload: dict = Body(...)):
    """
    Expects JSON: { "videoData": "<base64 or some URL>" }
    For real usage, parse frames or run a summarizer -> embed the summary in page_content.
    """
    video_data = payload.get("videoData", "")
    if not video_data:
        raise HTTPException(status_code=400, detail="No video data provided")

    # We place minimal text for embedding; actual usage: run a video summarizer
    doc = Document(
        page_content="",  
        metadata={
            "id": str(uuid4()),
            "type": "video",
            "videoData": video_data,
        }
    )
    db.add_documents([doc])
    return {"message": "Video memory upserted"}

# ──────────────────────────────────────────────────────────
# Spatial Memory
# ──────────────────────────────────────────────────────────
@app.post("/memories/spatial")
def create_spatial_memory(payload: dict = Body(...)):
    """
    Expects JSON: { "spatialData": "some reference or base64 of .obj" }
    For 3D data, you can store reference or entire mesh inside metadata.
    """
    spatial_data = payload.get("spatialData", "")
    if not spatial_data:
        raise HTTPException(status_code=400, detail="No spatial data provided")

    doc = Document(
        page_content="",  
        metadata={
            "id": str(uuid4()),
            "type": "spatial",
            "spatialData": spatial_data
        }
    )
    db.add_documents([doc])
    return {"message": "Spatial memory upserted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)