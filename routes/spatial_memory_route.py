from fastapi import Body, HTTPException
import random
from utils.vectorstore import upsert_spatial_memory
from dummy_embedding import dummy_embedding


def create_spatial_memory(payload: dict = Body(...)):
    """
    Expects { "spatialData": "some reference or base64 of .obj" }
    We'll do a dummy embedding from the text. 
    """
    spatial_data = payload.get("spatialData", "")
    if not spatial_data:
        raise HTTPException(status_code=400, detail="No spatial data provided")

    embedding = dummy_embedding(spatial_data, length=8)
    upsert_spatial_memory({"reference": spatial_data}, embedding)
    return {"message": "Spatial memory upserted"}
