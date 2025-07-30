from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from typing import List, Dict, Any, Union
from pydantic import BaseModel
from bson import ObjectId
import json
import os

from schemas import AggregateRequest
from db import db  # Your database client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set in .env")

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

def convert_objectids(obj):
    if isinstance(obj, list):
        return [convert_objectids(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_objectids(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

@app.post("/aggregate")
async def aggregate_query(
    payload: AggregateRequest,
    api_key: str = Depends(verify_api_key)
):
    raw_pipeline = payload.pipeline

    # If pipeline items are strings, parse each JSON string to dict
    if isinstance(raw_pipeline, list) and raw_pipeline and isinstance(raw_pipeline[0], str):
        try:
            pipeline = [json.loads(stage) for stage in raw_pipeline]
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid pipeline JSON strings")
    else:
        pipeline = raw_pipeline

    if not isinstance(pipeline, list):
        raise HTTPException(status_code=400, detail="Pipeline must be a list")

    try:
        collection = db[payload.collection]
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=1000)
        results = convert_objectids(results)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
