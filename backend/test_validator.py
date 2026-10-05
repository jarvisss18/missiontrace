from app.models.reasoning import MissionReasoningResult, Finding, Hypothesis
from app.services.validator import EvidenceValidator
from app.services.ledger import EvidenceLedger

ledger = EvidenceLedger(data_dir="../data")
validator = EvidenceValidator(ledger)

result = MissionReasoningResult(
    findings=[
        Finding(
            type="OBSERVED",
            claim="Hallucinated claim with fake evidence.",
            evidence_ids=["EV-FAKE-999"],
            confidence=0.9
        ),
        Finding(
            type="OBSERVED",
            claim="Valid claim with real evidence.",
            evidence_ids=["EV-001"], # Matches telemetry
            confidence=1.0
        )
    ],
    hypotheses=[],
    recommendations=[],
    unknowns=[]
)

validated = validator.validate(result)

print("--- VALIDATED FINDINGS ---")
for f in validated.findings:
    print(f"- {f.claim}")

print("\n--- UNKNOWNS GENERATED ---")
for u in validated.unknowns:
    print(f"- {u.reason} | {u.gap}")
