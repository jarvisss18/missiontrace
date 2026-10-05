import json
from typing import List, Optional
from datetime import datetime

from app.models.evidence import EvidenceRecord
from app.services.ledger import EvidenceLedger

class EvidenceRetriever:
    def __init__(self, ledger: EvidenceLedger):
        self.ledger = ledger

    def search(
        self,
        q: Optional[str] = None,
        source_type: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[EvidenceRecord]:
        
        all_evidence = self.ledger.get_all_evidence()
        results = []
        
        # Keyword casing for simple match
        q_lower = q.lower() if q else None

        for record in all_evidence:
            # Source Type Filter
            if source_type and record.source_type != source_type:
                continue
                
            # Time Range Filtering (Simple string comparison works for ISO8601 timestamps)
            # Procedures might have "STATIC" timestamps, usually we skip time filters for them
            if record.timestamp != "UNKNOWN" and record.timestamp != "STATIC":
                if start_time and record.timestamp < start_time:
                    continue
                if end_time and record.timestamp > end_time:
                    continue

            # Keyword Keyword Filter (checks inside the raw content dump)
            if q_lower:
                if q_lower not in record.content.lower():
                    continue
                    
            results.append(record)

        # Basic Ranking: chronological by timestamp if available
        # Those with STATIC/UNKNOWN will fall to the end
        results.sort(key=lambda x: x.timestamp)
        return results
