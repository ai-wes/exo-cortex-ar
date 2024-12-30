from fastapi import Body, HTTPException
import random
#from utils.vectorstore import upsert_spatial_memory
def dummy_embedding(text: str, length=8):
    return [random.random() for _ in range(length)]


def create_spatial_memory(payload: dict = Body(...)):
    """
    Expects { "spatialData": "some reference or base64 of .obj" }
    We'll do a dummy embedding from the text. 
    """
    spatial_data = payload.get("spatialData", "")
    if not spatial_data:
        raise HTTPException(status_code=400, detail="No spatial data provided")

    embedding = dummy_embedding(spatial_data, length=8)
    #upsert_spatial_memory({"reference": spatial_data}, embedding)
    return {"message": "Spatial memory upserted"}
