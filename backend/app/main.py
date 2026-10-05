from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from app.services.ledger import ledger
from app.services.retrieval import EvidenceRetriever
from app.models.evidence import EvidenceRecord

retriever = EvidenceRetriever(ledger)

app = FastAPI(title="MissionTrace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/evidence", response_model=List[EvidenceRecord])
def get_all_evidence(
    q: Optional[str] = None,
    source_type: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
):
    return retriever.search(q=q, source_type=source_type, start_time=start_time, end_time=end_time)

@app.get("/api/evidence/{evidence_id}", response_model=EvidenceRecord)
def get_evidence_by_id(evidence_id: str):
    record = ledger.get_evidence(evidence_id)
    if not record:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return record

