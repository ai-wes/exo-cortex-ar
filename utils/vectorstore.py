import os
import random
from uuid import uuid4

# If you're using the Deep Lake VectorStore:
# pip install deeplake
# from deeplake.core.vectorstore import VectorStore

# If you want to keep everything local/naive (no real DB),
# you can store them in a global list. For demonstration,
# let's assume you DO want the real VectorStore approach:

try:
    from deeplake.core.vectorstore import VectorStore

    DATASET_PATH = "./memories_vectorstore"  # local or s3://, etc.
    vector_store = VectorStore(path=DATASET_PATH)
except ImportError:
    # If Deep Lake isn't installed, fallback to an in-memory list
    print("Deep Lake not installed; using an in-memory store for demonstration.")
    vector_store = []
    class InMemoryVectorStore:
        def upsert(self, docs):
            vector_store.extend(docs)

    vector_store = InMemoryVectorStore()

def upsert_text_memory(content: str, embedding: list[float], metadata: dict = None):
    """
    Upsert text memory into the vector store.
    
    Args:
        content: The text content to store
        embedding: Vector embedding of the content
        metadata: Additional metadata like title, tags, timestamp
    """
    doc_id = str(uuid4())
    
    # Combine base metadata with additional metadata
    base_metadata = {
        "type": "text",
        "content": content
    }
    if metadata:
        base_metadata.update(metadata)
    
    doc = {
        "id": doc_id,
        "embedding": embedding,
        "metadata": base_metadata
    }
    vector_store.upsert([doc])
    return doc_id

def upsert_video_memory(video_info: dict, embedding: list[float]):
    """Upsert video memory (base64/URL) + embedding."""
    doc_id = str(uuid4())
    doc = {
        "id": doc_id,
        "embedding": embedding,
        "metadata": {
            "type": "video",
            "info": video_info
        }
    }
    vector_store.upsert([doc])

def upsert_image_memory(image_info: dict, embedding: list[float]):
    """Upsert image memory (base64, filename) + embedding."""
    doc_id = str(uuid4())
    doc = {
        "id": doc_id,
        "embedding": embedding,
        "metadata": {
            "type": "image",
            "info": image_info
        }
    }
    vector_store.upsert([doc])

def upsert_audio_memory(transcription: str, embedding: list[float]):
    """Upsert audio memory (text transcription) + embedding."""
    doc_id = str(uuid4())
    doc = {
        "id": doc_id,
        "embedding": embedding,
        "metadata": {
            "type": "audio",
            "transcription": transcription
        }
    }
    vector_store.upsert([doc])