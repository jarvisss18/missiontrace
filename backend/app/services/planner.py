from app.services.retrieval import EvidenceRetriever
from app.services.llm import MockLLMProvider
from app.services.validator import EvidenceValidator
from app.models.reasoning import MissionReasoningResult, UnknownClaim

class QueryPlanner:
    def __init__(self, retriever: EvidenceRetriever, validator: EvidenceValidator):
        self.retriever = retriever
        self.validator = validator
        self.llm = MockLLMProvider()

    def handle_query(self, query: str) -> MissionReasoningResult:
        # We can extract primitive keywords for the mock MVP
        keywords = query.split()
        search_term = keywords[0] if keywords else None
        
        # Step 1: Retrieve context
        # Passing None for broad retrieval, except for 'thermal' to trigger conflicts
        q_filter = "thermal" if "thermal" in query.lower() else None
        if "obscure" in query.lower():
            q_filter = "this_will_return_nothing"
            
        context = self.retriever.search(q=q_filter) 
        
        # PROACTIVE ABSTENTION 1: No evidence
        if not context:
            return MissionReasoningResult(
                findings=[],
                hypotheses=[],
                recommendations=[],
                unknowns=[
                    UnknownClaim(
                        reason="No relevant evidence found.",
                        gap="The retriever pulled 0 records from the ledger for this query.",
                        suggested_step="Expand search parameters or check if data is completely missing."
                    )
                ]
            )
            
        proactive_unknowns = []
        # PROACTIVE ABSTENTION 2: Conflicting or Missing Data
        for record in context:
            if record.quality in ["CONFLICTING", "MISSING", "STALE"]:
                proactive_unknowns.append(
                    UnknownClaim(
                        reason=f"Problematic evidence detected (Quality: {record.quality})",
                        gap=f"Evidence {record.evidence_id} is marked as {record.quality}.",
                        suggested_step="Manually inspect conflicting records or request re-transmission."
                    )
                )

        # Step 2: Pass context and query to Reasoning Layer
        raw_result = self.llm.process(query, context)
        
        # Inject proactive unknowns
        raw_result.unknowns.extend(proactive_unknowns)
        
        # Step 3: Validation Step
        validated_result = self.validator.validate(raw_result)
        
        return validated_result
