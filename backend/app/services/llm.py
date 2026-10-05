import json
from typing import List
from app.models.evidence import EvidenceRecord
from app.models.reasoning import (
    MissionReasoningResult,
    Finding,
    Hypothesis,
    Recommendation,
    UnknownClaim
)

class MockLLMProvider:
    def process(self, query: str, context: List[EvidenceRecord]) -> MissionReasoningResult:
        query_lower = query.lower()
        
        # Scenario B (Missing evidence / Abstention)
        if "04:21z" in query_lower and "array degrade" in query_lower:
            return MissionReasoningResult(
                findings=[],
                hypotheses=[],
                recommendations=[],
                unknowns=[
                    UnknownClaim(
                        reason="No telemetry is available for 04:21Z.",
                        gap="04:20Z - 04:24Z telemetry loss.",
                        suggested_step="Check next-pass playback."
                    )
                ]
            )

        # Scenario A & C (Anomalous battery drop)
        if "batt" in query_lower and "drop" in query_lower:
            # We assume these EV IDs align structurally with our Phase 1 dataset
            return MissionReasoningResult(
                findings=[
                    Finding(
                        type="OBSERVED",
                        claim="Battery voltage crossed the low threshold (26.5V).",
                        evidence_ids=["EV-003", "EV-005"], # Adjust manually to match real ledger
                        confidence=1.0
                    )
                ],
                hypotheses=[
                    Hypothesis(
                        type="INFERRED",
                        hypothesis="Possible correlation with eclipse entry.",
                        confidence="Medium",
                        evidence_ids=["EV-005"], 
                        alternative_explanations="Array degradation cannot yet be ruled out.",
                        discriminating_check="Compare array current against orbit-phase prediction."
                    )
                ],
                recommendations=[
                    Recommendation(
                        type="RECOMMENDED",
                        action="Compare array current with orbit-phase prediction.",
                        procedure_id="EPS-DIAG-03",
                        section="§4.2",
                        version="v7"
                    )
                ],
                unknowns=[]
            )

        # Default fallback
        return MissionReasoningResult(
            findings=[],
            hypotheses=[],
            recommendations=[],
            unknowns=[
                UnknownClaim(
                    reason="The query was not fully understood by the demo mock provider.",
                    gap="Demo fallback state active.",
                    suggested_step="Try one of the provided demo scenarios."
                )
            ]
        )
