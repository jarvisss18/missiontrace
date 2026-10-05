from pydantic import BaseModel
from typing import List, Optional

class Finding(BaseModel):
    type: str = "OBSERVED"
    claim: str
    evidence_ids: List[str]
    confidence: float

class Hypothesis(BaseModel):
    type: str = "INFERRED"
    hypothesis: str
    confidence: str
    evidence_ids: List[str]
    alternative_explanations: Optional[str]
    discriminating_check: Optional[str]

class Recommendation(BaseModel):
    type: str = "RECOMMENDED"
    action: str
    procedure_id: Optional[str]
    section: Optional[str]
    version: Optional[str]

class UnknownClaim(BaseModel):
    type: str = "UNKNOWN"
    reason: str
    gap: str
    suggested_step: str

class MissionReasoningResult(BaseModel):
    findings: List[Finding]
    hypotheses: List[Hypothesis]
    recommendations: List[Recommendation]
    unknowns: List[UnknownClaim]
