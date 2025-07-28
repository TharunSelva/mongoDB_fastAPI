from pydantic import BaseModel
from typing import List, Dict, Any

class AggregateRequest(BaseModel):
    pipeline: List[Dict[str, Any]]