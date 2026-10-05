from app.services.retrieval import EvidenceRetriever
from app.services.llm import MockLLMProvider
from app.models.reasoning import MissionReasoningResult

class QueryPlanner:
    def __init__(self, retriever: EvidenceRetriever):
        self.retriever = retriever
        self.llm = MockLLMProvider()

    def handle_query(self, query: str) -> MissionReasoningResult:
        # Step 1: Retrieve all context matching the keywords (in a real system we'd extract key entities first)
        # For our MVP, we pass the query mostly unchanged but maybe take the first word or important words
        # Here we just pass None for broad retrieval, or pass parts of it.
        # Actually, let's just do a naive pass: get all evidence 
        # (in production we'd do vector search here)
        context = self.retriever.search(q=None) 
        
        # Step 2: Pass context and query to Reasoning Layer
        result = self.llm.process(query, context)
        
        return result
