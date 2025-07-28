from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Dict, Any
from db import db
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Define Pydantic model for request body
class AggregateRequest(BaseModel):
    pipeline: List[Dict[str, Any]]

@app.post("/aggregate")
async def aggregate_query(
    payload: AggregateRequest,
    api_key: str = Depends(verify_api_key)
):
    pipeline = payload.pipeline
    
    if not isinstance(pipeline, list):
        raise HTTPException(status_code=400, detail="Pipeline must be a list")

    collection = db[COLLECTION_NAME]
    cursor = collection.aggregate(pipeline)
    results = await cursor.to_list(length=1000)  # You can limit length here
    return {"results": results}
