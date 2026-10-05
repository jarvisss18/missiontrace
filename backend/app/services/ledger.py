import json
import hashlib
from typing import List, Dict, Optional
from pathlib import Path

from app.models.evidence import EvidenceRecord

class EvidenceLedger:
    def __init__(self, data_dir: str = "../data"):
        self.data_dir = Path(data_dir)
        self.evidence_store: Dict[str, EvidenceRecord] = {}
        self._counter = 1
        self._load_all_data()

    def _generate_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _create_evidence(self, source_type: str, item: dict) -> None:
        ev_id = f"EV-{self._counter:03d}"
        self._counter += 1

        # Determine timestamp and source_id based on source type
        timestamp = item.get("timestamp", "UNKNOWN")
        content = json.dumps(item, sort_keys=True)
        quality = item.get("quality", "VALID")
        
        source_id = "UNKNOWN"
        if source_type == "telemetry":
            source_id = f"TEL-{item.get('subsystem')}-{item.get('parameter')}"
        elif source_type == "log":
            source_id = item.get("log_id", "LOG-UNKNOWN")
        elif source_type == "procedure":
            source_id = item.get("procedure_id", "PROC-UNKNOWN")
            timestamp = "STATIC" # Procedures don't have temporal occurrence in the same way
        elif source_type == "incident":
            source_id = item.get("incident_id", "INC-UNKNOWN")

        integrity_hash = self._generate_hash(content)

        record = EvidenceRecord(
            evidence_id=ev_id,
            source_type=source_type,
            source_id=source_id,
            timestamp=timestamp,
            content=content,
            quality=quality,
            integrity_hash=integrity_hash
        )
        self.evidence_store[ev_id] = record

    def _load_json_file(self, filename: str, source_type: str):
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"Warning: Data file {filepath} not found.")
            return

        with open(filepath, "r") as f:
            data = json.load(f)
            for record in data.get("records", []):
                self._create_evidence(source_type, record)

    def _load_all_data(self):
        self._load_json_file("telemetry/telemetry.json", "telemetry")
        self._load_json_file("logs/logs.json", "log")
        self._load_json_file("procedures/procedures.json", "procedure")
        self._load_json_file("incidents/incidents.json", "incident")
        print(f"Loaded {len(self.evidence_store)} evidence records into ledger.")

    def get_all_evidence(self) -> List[EvidenceRecord]:
        return list(self.evidence_store.values())

    def get_evidence(self, evidence_id: str) -> Optional[EvidenceRecord]:
        return self.evidence_store.get(evidence_id)

ledger = EvidenceLedger()
