import json
from typing import List, Optional
from app.models.timeline import TimelineEvent
from app.services.ledger import EvidenceLedger

class TimelineService:
    def __init__(self, ledger: EvidenceLedger):
        self.ledger = ledger

    def generate_timeline(self, incident_id: Optional[str] = None) -> List[TimelineEvent]:
        all_evidence = self.ledger.get_all_evidence()
        events = []

        # If incident_id is passed, we could filter contextually around its timestamp
        # For MVP, we will render all chronological evidence as the timeline

        for record in all_evidence:
            # Skip records without a temporal timestamp (like static procedures)
            if record.timestamp in ["STATIC", "UNKNOWN"]:
                continue

            # Parse content to formulate a human-readable description
            try:
                content_dict = json.loads(record.content)
            except:
                content_dict = {}

            statement_type = "OBSERVED"
            desc = ""

            if record.source_type == "telemetry":
                desc = f"{content_dict.get('parameter', 'Telemetry')} value: {content_dict.get('value')} {content_dict.get('unit', '')}"
            elif record.source_type == "log":
                statement_type = content_dict.get("severity", "LOG")
                desc = content_dict.get("message", "Log recorded.")
            elif record.source_type == "incident":
                statement_type = "INCIDENT"
                desc = content_dict.get("description", "Incident recorded.")

            # Create event
            event = TimelineEvent(
                timestamp=record.timestamp,
                statement_type=statement_type,
                description=desc,
                evidence_ids=[record.evidence_id],
                source=record.source_type.upper()
            )
            events.append(event)

        # Sort chronologically
        events.sort(key=lambda x: x.timestamp)
        return events
