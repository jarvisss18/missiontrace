from app.services.planner import QueryPlanner
from app.services.retrieval import EvidenceRetriever
from app.services.validator import EvidenceValidator
from app.services.ledger import EvidenceLedger

ledger = EvidenceLedger(data_dir="../data")
retriever = EvidenceRetriever(ledger)
validator = EvidenceValidator(ledger)
planner = QueryPlanner(retriever, validator)

print("--- TEST 1: EMPTY CONTEXT (OBSCURE QUERY) ---")
res1 = planner.handle_query("some obscure query")
for u in res1.unknowns:
    print(f"- {u.reason} | {u.gap}")

print("\n--- TEST 2: CONFLICTING CONTEXT (THERMAL QUERY) ---")
res2 = planner.handle_query("why did thermal fail?")
for u in res2.unknowns:
    print(f"- {u.reason} | {u.gap}")
