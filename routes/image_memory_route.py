from fastapi import File, UploadFile, HTTPException
import random
import base64
from utils.vectorstore import upsert_image_memory
def dummy_embedding(text: str, length=8):
    return [random.random() for _ in range(length)]
def create_image_memory(file: UploadFile = File(...)):
    """
    Expects a file upload, e.g. from a multipart/form-data request:
      formData.append("file", { uri, type, name })
    """
    try:
        image_bytes = file.file.read()
        base64_img = base64.b64encode(image_bytes).decode("utf-8")
        # In real usage, call a vision model for the embedding
        embedding = dummy_embedding("image:" + file.filename, length=8)
        upsert_image_memory({"filename": file.filename, "base64": base64_img}, embedding)
        return {"message": "Image memory upserted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
