from pydantic import BaseModel
from typing import Optional

class EvidenceRecord(BaseModel):
    evidence_id: str
    source_type: str
    source_id: str
    timestamp: str
    content: str
    quality: str
    integrity_hash: str
    time_range: Optional[str] = None
