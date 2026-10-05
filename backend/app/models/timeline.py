from pydantic import BaseModel
from typing import List

class TimelineEvent(BaseModel):
    timestamp: str
    statement_type: str
    description: str
    evidence_ids: List[str]
    source: str
