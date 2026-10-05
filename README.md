# MissionTrace

Evidence-Grounded Mission Operations Copilot

Every claim cited. Every gap admitted. Every action human-approved.

## ST-10 Problem Statement
MissionTrace is built for the TECHFEST 2026–27 Space Technology Hackathon (ST-10). It provides an evidence-based reasoning assistant that helps spacecraft operators analyze anomalies and telemetry gaps without hallucinating facts.

## Solution Architecture
1. **Evidence Ledger**: All telemetry, logs, and procedures are indexed and verifiable with SHA-256 hashes.
2. **Deterministic Validator**: AI assertions are strictly checked against available evidence.
3. **Four Statement Types**: OBSERVED, INFERRED, RECOMMENDED, and UNKNOWN.
4. **Investigation Timeline**: An auditable trace of claims and their evidence.

## Setup
Backend: Python + FastAPI
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Frontend: React + Vite + Tailwind CSS
```bash
cd frontend
npm install
npm run dev
```
