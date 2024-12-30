from fastapi import FastAPI, HTTPException
import uvicorn
from utils.vectorstore import vector_store

from routes.text_memory_route import create_text_memory
from routes.audio_memory_route import create_audio_memory
from routes.image_memory_route import create_image_memory
from routes.video_memory_route import create_video_memory
from routes.spatial_memory_route import create_spatial_memory

app = FastAPI(title="VectorStore Memory API")

@app.post("/memories/text")
async def create_text_memory_handler(payload: dict):
    return await create_text_memory(payload)

@app.post("/memories/audio")
async def create_audio_memory_handler(payload: dict):
    return await create_audio_memory(payload)

@app.post("/memories/image")
async def create_image_memory_handler(file):
    return await create_image_memory(file)

@app.post("/memories/video")
async def create_video_memory_handler(payload: dict):
    return await create_video_memory(payload)

@app.post("/memories/spatial")
async def create_spatial_memory_handler(payload: dict):
    return await create_spatial_memory(payload)

@app.get("/search")
def search_memories(q: str, memory_type: str = None):
    """
    Example vector search in the VectorStore with optional memory type filtering.
    
    Args:
        q: Search query string
        memory_type: Optional filter for memory type ('text', 'audio', 'image', 'video', 'spatial')
    """
    from utils.vectorstore import dummy_embedding
    
    # Generate embedding from query
    emb = dummy_embedding(q)
    
    # Define valid memory types
    valid_types = {'text', 'audio', 'image', 'video', 'spatial'}
    
    # Validate memory_type if provided
    if memory_type and memory_type.lower() not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid memory_type. Must be one of: {', '.join(valid_types)}"
        )
    
    # Query the vector store with type filtering if specified
    if memory_type:
        results = vector_store.query(
            emb,
            k=5,
            filter={'type': memory_type.lower()}
        )
    else:
        results = vector_store.query(emb, k=5)
    
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)