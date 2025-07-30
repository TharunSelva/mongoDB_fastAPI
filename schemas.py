from pydantic import BaseModel
from typing import List, Dict, Any

class AggregateRequest(BaseModel):
    # added this to specify that any collection can be used (previously only the "comments" collection):
    collection: str
    pipeline: List[Dict[str, Any]]
