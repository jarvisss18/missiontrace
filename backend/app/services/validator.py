from app.models.reasoning import MissionReasoningResult, UnknownClaim
from app.services.ledger import EvidenceLedger

class EvidenceValidator:
    def __init__(self, ledger: EvidenceLedger):
        self.ledger = ledger

    def validate(self, result: MissionReasoningResult) -> MissionReasoningResult:
        valid_findings = []
        valid_hypotheses = []
        unknowns = result.unknowns.copy()

        # Check Findings (OBSERVED claims)
        for finding in result.findings:
            valid_evidence = []
            for ev_id in finding.evidence_ids:
                if self.ledger.get_evidence(ev_id):
                    valid_evidence.append(ev_id)
            
            if valid_evidence:
                finding.evidence_ids = valid_evidence
                valid_findings.append(finding)
            else:
                # Intercept unsupported claim
                unknowns.append(
                    UnknownClaim(
                        reason=f"Validation Failed for claim: '{finding.claim}'",
                        gap="No valid evidence IDs supported this observed claim. Intercepted by Validator.",
                        suggested_step="Verify AI source or check for missing telemetry."
                    )
                )

        # Check Hypotheses (INFERRED claims)
        for hyp in result.hypotheses:
            valid_evidence = []
            for ev_id in hyp.evidence_ids:
                if self.ledger.get_evidence(ev_id):
                    valid_evidence.append(ev_id)
                    
            hyp.evidence_ids = valid_evidence
            # Hypotheses are speculative, but they still MUST base speculation on SOMETHING.
            if valid_evidence:
                valid_hypotheses.append(hyp)
            else:
                unknowns.append(
                    UnknownClaim(
                        reason=f"Validation Failed for hypothesis: '{hyp.hypothesis}'",
                        gap="Hypothesis completely ungrounded. No valid evidence IDs.",
                        suggested_step="Review AI reasoning layer."
                    )
                )

        # We keep recommendations as is assuming they stem from valid findings/hypotheses 
        # (Though we could validate procedure IDs here too)
        
        result.findings = valid_findings
        result.hypotheses = valid_hypotheses
        result.unknowns = unknowns
        
        return result
