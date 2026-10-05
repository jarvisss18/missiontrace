# MissionTrace — Final Antigravity Build Specification

## Evidence-Grounded Mission Operations Copilot

### TECHFEST 2026–27 — SPACE TECHNOLOGY HACKATHON
### Problem Statement: ST-10

---

# 0. IMPORTANT PROJECT RULE

You are the implementation agent working with the developer on the MissionTrace project.

Your job is to help the developer build, test, inspect, debug, document, and improve the application.

## ABSOLUTE GIT RULE

**ANTIGRAVITY MUST NEVER COMMIT OR PUSH.**

The developer/team member must perform all Git commits and pushes manually.

Antigravity may inspect Git state and show commands, but must never execute:

```bash
git commit
git push
git commit --amend
git rebase
git cherry-pick
git reset --hard
git merge
git init
```

Do not modify Git history.

Do not create fake commits.

Do not manipulate timestamps.

Do not manipulate authorship.

Do not use GitHub APIs to create commits.

Do not automatically push anything.

---

# 1. PRODUCT IDENTITY

## Repository

GitHub repository:

`https://github.com/jarvisss18/OrbitOps`

Repository name:

`OrbitOps`

**Do NOT rename the repository.**

---

## Product Name

`MissionTrace`

Product title:

`MissionTrace — Evidence-Grounded Mission Operations Copilot`

Primary tagline:

> Every claim cited. Every gap admitted. Every action human-approved.

Core principle:

> When MissionTrace is not sure, it does not guess.

---

# 2. PROBLEM STATEMENT

## ST-10 — Mission Operations Copilot with Evidence-Grounded Decisions

Develop an operator assistant that queries:

- mission logs
- telemetry summaries
- procedures
- incident history

to:

- explain anomalies
- identify supporting evidence
- propose diagnostic steps
- generate an auditable incident timeline
- clearly distinguish observed facts from recommendations

The system must prioritize evidence traceability and operator control.

---

# 3. PRIMARY OBJECTIVE

Build a working hackathon MVP that allows an operator to ask a mission-related question and receive an evidence-grounded response.

The system must:

1. Understand an operator query.
2. Retrieve relevant mission evidence.
3. Correlate telemetry, logs, procedures, and incidents.
4. Explain anomalies.
5. Separate facts from hypotheses.
6. Provide evidence IDs for claims.
7. Provide diagnostic recommendations.
8. Identify missing or conflicting evidence.
9. Abstain when evidence is insufficient.
10. Generate an auditable incident timeline.
11. Validate LLM-generated claims deterministically.
12. Preserve provenance.
13. Keep the operator in control.
14. Never issue spacecraft commands.

---

# 4. CORE DESIGN PHILOSOPHY

MissionTrace is not simply a chatbot.

The important innovation is **evidence-grounded reasoning with deterministic validation**.

The architecture must enforce:

```text
ASK
  ↓
RETRIEVE
  ↓
ANALYZE
  ↓
VALIDATE
  ↓
RECOMMEND
  ↓
HUMAN DECISION
  ↓
AUDIT / TIMELINE
```

The LLM is a reasoning component.

The LLM is NOT the source of truth.

The evidence layer is the source of truth.

---

# 5. FOUR STATEMENT TYPES

MissionTrace MUST distinguish four types of statements.

## 5.1 OBSERVED

Directly supported by mission evidence.

Example:

```text
OBSERVED

BATT_V_A crossed the 26.5 V low limit at 04:12:07Z.

Evidence:
EV-017
```

An observed statement must have supporting evidence.

---

## 5.2 INFERRED

A hypothesis derived from observed evidence.

Example:

```text
INFERRED

The battery voltage drop coincides with eclipse entry.

Confidence:
Medium

Evidence:
EV-017
EV-024

Alternative:
Array degradation cannot yet be ruled out.

Discriminating check:
Compare array current against orbit-phase prediction.
```

An inference must never be presented as a confirmed fact.

---

## 5.3 RECOMMENDED

A proposed diagnostic or operational step.

Example:

```text
RECOMMENDED

Compare array current with orbit-phase prediction.

Procedure:
EPS-DIAG-03

Section:
§4.2

Version:
v7
```

Recommendations are suggestions.

The operator remains responsible for deciding whether to execute them.

---

## 5.4 UNKNOWN

Used when evidence is:

- missing
- stale
- conflicting
- insufficient
- unavailable
- invalid

Example:

```text
UNKNOWN

Telemetry is unavailable from 04:20Z to 04:24Z.

The available evidence is insufficient to determine
whether solar-array degradation occurred at 04:21Z.

Suggested resolution:
Check next-pass telemetry playback.
```

Never guess when evidence is unavailable.

---

# 6. ABSOLUTE ABSTENTION REQUIREMENT

MissionTrace must demonstrate safe abstention.

Example scenario:

Telemetry is missing:

```text
04:20Z — 04:24Z
```

Operator asks:

```text
Did the solar array degrade at 04:21Z?
```

The system must NOT answer:

```text
Yes.
```

It must NOT invent telemetry.

It must NOT infer certainty from unrelated evidence.

Correct behavior:

```text
UNKNOWN

No telemetry is available for 04:21Z.

The available evidence is insufficient to determine
whether solar-array degradation occurred.

Evidence gap:
04:20Z–04:24Z telemetry loss.

Suggested next step:
Check next-pass playback.
```

This behavior is mandatory.

---

# 7. EVIDENCE LEDGER

The Evidence Ledger is the central provenance system.

Every meaningful factual claim should point to an evidence record.

Example:

```text
EV-017
EV-018
EV-024
```

## Evidence Schema

Each evidence record should contain:

```text
evidence_id
source_type
source_id
timestamp
time_range
content
metadata
quality
retrieval_time
integrity_hash
```

Example:

```json
{
  "evidence_id": "EV-017",
  "source_type": "telemetry",
  "source_id": "TEL-BATT-2026-10-05",
  "timestamp": "2026-10-05T04:12:07Z",
  "content": "BATT_V_A = 26.1 V",
  "quality": "VALID",
  "integrity_hash": "..."
}
```

---

# 8. EVIDENCE QUALITY

Support the following quality states:

```text
VALID
MISSING
STALE
CONFLICTING
SUSPICIOUS
INVALID
```

The UI must make problematic evidence visible.

For example:

```text
CONFLICTING

Two telemetry records report different values
for the same timestamp.
```

Do not silently choose one.

---

# 9. EVIDENCE PROVENANCE

Every claim should be traceable:

```text
Claim
 ↓
Evidence ID
 ↓
Source
 ↓
Timestamp
 ↓
Original record
```

The UI should allow the operator to inspect the evidence behind a claim.

---

# 10. INTEGRITY

Use SHA-256 hashes where appropriate.

Example:

```text
source record
      ↓
SHA-256
      ↓
integrity_hash
```

The purpose is to strengthen provenance and demonstrate that the evidence record can be traced back to its original source representation.

---

# 11. DETERMINISTIC VALIDATOR

Do NOT rely exclusively on LLM prompting.

Implement a deterministic validation layer.

The validator must check:

- evidence IDs exist
- evidence IDs actually support claims
- numeric values match evidence
- timestamps are consistent
- statement type is valid
- OBSERVED statements have evidence
- INFERRED statements are not represented as facts
- RECOMMENDED statements have procedure references where applicable
- UNKNOWN statements explain the evidence gap
- evidence conflicts are surfaced
- malformed citations are rejected
- unsupported claims are rejected or converted to UNKNOWN

---

# 12. UNSUPPORTED CLAIM PROTECTION

If the LLM produces:

```text
The solar array degraded at 04:21Z.
```

but no evidence supports this claim, the validator must reject it.

Possible result:

```text
UNKNOWN

The claim could not be supported by the available evidence.
```

Never allow unsupported statements to appear as established facts.

---

# 13. HYPOTHESIS ENGINE

MissionTrace must support competing hypotheses.

Do not force a single root cause.

Each hypothesis should contain:

```text
hypothesis
confidence
supporting evidence
alternative explanations
discriminating check
```

Example:

```text
Hypothesis A
Battery transient
Confidence: Medium
Evidence: EV-017, EV-018
Check: Compare EPS event timing.

Hypothesis B
Solar-array degradation
Confidence: Low
Evidence: EV-024
Check: Compare array current with orbital prediction.

Hypothesis C
Sensor anomaly
Confidence: Low
Evidence: EV-030
Check: Compare redundant sensor channel.
```

---

# 14. AUDITABLE TIMELINE

MissionTrace must generate a chronological investigation timeline.

Timeline events should include:

```text
timestamp
statement_type
description
evidence_ids
source
```

Example:

```text
04:12:07Z
OBSERVED
Battery voltage crossed the low threshold.
EV-017

04:12:09Z
OBSERVED
EPS_UV_WARN event was raised.
EV-018

04:31:00Z
INFERRED
Voltage drop coincides with eclipse entry.
EV-017, EV-024

04:35:00Z
RECOMMENDED
Compare array current with orbit-phase prediction.
EPS-DIAG-03 §4.2 v7
```

The timeline must be generated from the evidence layer.

Do not fabricate timeline events.

---

# 15. DATA MODEL

## Telemetry

```text
timestamp
satellite_id
subsystem
parameter
value
unit
quality
```

## Mission Log

```text
timestamp
log_id
severity
subsystem
message
```

## Procedure

```text
procedure_id
title
section
version
step
description
```

## Incident

```text
incident_id
timestamp
subsystem
description
resolution
```

## Evidence

```text
evidence_id
source_type
source_id
timestamp
content
quality
hash
```

---

# 16. SYNTHETIC DATA

Create realistic synthetic mission data.

The data must include:

- normal telemetry
- anomalous telemetry
- threshold crossings
- mission warnings
- repeated events
- missing intervals
- conflicting evidence
- historical incidents
- procedures
- timestamps
- procedure references

Clearly label all data as:

```text
SYNTHETIC DEMO DATA
```

Do not imply that synthetic data is real spacecraft telemetry.

---

# 17. REQUIRED DEMO SCENARIOS

## Scenario A — Supported anomaly

Question:

```text
Why did BATT_V_A drop around 04:12Z?
```

Expected output:

```text
OBSERVED
Battery voltage crossed threshold.

INFERRED
Possible correlation with eclipse entry.

RECOMMENDED
Compare array current with orbit-phase prediction.

Evidence:
EV-017
EV-018
EV-024
```

## Scenario B — Missing evidence

Question:

```text
Did the solar array degrade at 04:21Z?
```

Expected:

```text
UNKNOWN
```

with an explanation of the telemetry gap.

## Scenario C — Competing hypotheses

Question:

```text
What could explain the battery voltage drop?
```

Expected:

Multiple hypotheses rather than one forced root cause.

## Scenario D — Unsupported claim

Input:

```text
Array degradation occurred at 04:21Z.
```

If evidence does not support it:

```text
VALIDATION FAILED
```

or:

```text
UNKNOWN
```

## Scenario E — Procedure lookup

Question:

```text
What should the operator check next?
```

Expected:

```text
RECOMMENDED

Procedure:
EPS-DIAG-03

Section:
§4.2

Version:
v7
```

---

# 18. SYSTEM ARCHITECTURE

```text
                    OPERATOR
                        │
                        ▼
                QUERY INTERFACE
                        │
                        ▼
                  QUERY PLANNER
                        │
                        ▼
              READ-ONLY RETRIEVAL
                 /      |       \
                /       |        \
               ▼        ▼         ▼
         TELEMETRY    LOGS    PROCEDURES
                \       |        /
                 \      |       /
                  ▼     ▼       ▼
                 INCIDENT HISTORY
                        │
                        ▼
                 EVIDENCE LEDGER
                        │
                        ▼
                  LLM REASONER
                        │
                        ▼
                STRUCTURED OUTPUT
                        │
                        ▼
             DETERMINISTIC VALIDATOR
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
          APPROVED    UNKNOWN   REJECTED
              │
              ▼
             UI
              │
              ▼
       AUDIT / TIMELINE
```

---

# 19. OPERATOR WORKFLOW

```text
ASK
 ↓
RETRIEVE
 ↓
CORRELATE
 ↓
EXPLAIN
 ↓
VALIDATE
 ↓
RECOMMEND
 ↓
HUMAN DECISION
 ↓
AUDIT
```

The application is read-only.

It must NEVER directly send spacecraft commands.

---

# 20. TECHNOLOGY STACK

## Frontend

```text
React
TypeScript
Vite
Tailwind CSS
Recharts
```

## Backend

```text
Python
FastAPI
Pydantic
```

## Storage

Start simple:

```text
JSON
CSV
SQLite
```

Only introduce PostgreSQL / pgvector if it provides clear value and time permits.

Do not overengineer the MVP.

## LLM

Use an isolated provider layer:

```text
Application
    ↓
LLM Provider Interface
    ↓
Provider Implementation
```

The application must not be tightly coupled to one LLM vendor.

---

# 21. DEMO MODE

The application must support deterministic local demo mode.

It should work without:

- internet
- LLM API key
- external mission systems

If the LLM provider is unavailable:

```text
AI MODE UNAVAILABLE
Switching to deterministic demo mode.
```

The core demo must continue working.

---

# 22. FRONTEND DESIGN

MissionTrace should look like a professional mission-control application.

Avoid:

- generic SaaS dashboards
- excessive gradients
- cartoon graphics
- unnecessary 3D elements
- excessive neon
- flashy animations

Preferred:

```text
Dark command-center UI
Subtle grid
High contrast
Technical typography
Restrained cyan/blue accents
Compact information density
Clear evidence states
```

---

# 23. DASHBOARD STRUCTURE

```text
┌───────────────────────────────────────────────┐
│ MissionTrace                 SYSTEM: READY   │
├───────────────────────────────────────────────┤
│                                               │
│ Query Mission                                │
│ [ Why did BATT_V_A drop around 04:12Z? ]    │
│                                               │
├──────────────────────┬────────────────────────┤
│ Findings             │ Evidence               │
│                      │                        │
│ OBSERVED             │ EV-017                 │
│ INFERRED             │ EV-018                 │
│ RECOMMENDED          │ EV-024                 │
│ UNKNOWN              │                        │
├──────────────────────┴────────────────────────┤
│ Hypotheses                                    │
├───────────────────────────────────────────────┤
│ Investigation Timeline                        │
└───────────────────────────────────────────────┘
```

---

# 24. COMPONENTS

Recommended:

```text
AppShell
Header
SystemStatus
QueryPanel
EvidencePanel
EvidenceCard
FindingPanel
ObservedCard
InferredCard
RecommendationCard
UnknownCard
HypothesisPanel
HypothesisCard
Timeline
TimelineEvent
ProcedureReference
ValidationBadge
AuditPanel
```

Adjust only when a better architecture is justified.

---

# 25. BACKEND API

Implement:

```http
GET /health
GET /api/evidence
GET /api/evidence/{id}
POST /api/query
GET /api/timeline/{incident_id}
GET /api/procedures/{id}
POST /api/validate
```

Only expose endpoints that are actually implemented.

Do not create fake APIs merely for documentation.

---

# 26. PROJECT STRUCTURE

```text
OrbitOps/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── core/
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── ...
│
├── data/
│   ├── telemetry/
│   ├── logs/
│   ├── procedures/
│   └── incidents/
│
├── docs/
│
├── .env.example
├── .gitignore
├── README.md
└── ...
```

---

# 27. PHASE 0 — FOUNDATION

## Goal

Create a clean working project foundation.

Implement:

- project structure
- frontend shell
- backend shell
- FastAPI application
- `/health`
- basic MissionTrace dashboard
- README
- `.gitignore`
- `.env.example`
- environment configuration
- basic startup instructions

Do NOT implement the LLM yet.

Do NOT implement advanced retrieval yet.

## Phase 0 validation

Backend:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Test:

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "ok"
}
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Verify MissionTrace opens successfully.

Suggested commit:

```text
chore: initialize MissionTrace project
```

---

# 28. PHASE 1 — SYNTHETIC MISSION DATA

Create:

- telemetry dataset
- mission logs
- procedures
- incident history

Include:

- normal records
- anomaly records
- missing telemetry
- conflicting records
- procedure references
- historical incident examples

Clearly label:

```text
SYNTHETIC DEMO DATA
```

Suggested commit:

```text
feat: add synthetic mission datasets
```

---

# 29. PHASE 2 — EVIDENCE LEDGER

Implement:

- evidence IDs
- source mapping
- timestamps
- time ranges
- provenance
- evidence quality
- evidence hashing
- evidence retrieval
- evidence inspection

Example:

```text
EV-001
EV-002
EV-003
...
```

Suggested commit:

```text
feat: implement evidence ledger
```

---

# 30. PHASE 3 — RETRIEVAL

Implement read-only retrieval.

Support:

- keyword search
- subsystem filtering
- timestamp filtering
- time-range filtering
- source-type filtering
- evidence ranking

Optional:

```text
semantic/vector retrieval
```

Only implement vector search if it does not slow down the core MVP.

Suggested commit:

```text
feat: add hybrid evidence retrieval
```

---

# 31. PHASE 4 — STRUCTURED MISSION REASONING

Implement:

```text
Query
 ↓
Retriever
 ↓
Evidence
 ↓
LLM
 ↓
Structured JSON
```

Example:

```json
{
  "findings": [
    {
      "type": "OBSERVED",
      "claim": "Battery voltage dropped below threshold.",
      "evidence_ids": ["EV-017"],
      "confidence": 1.0
    }
  ],
  "hypotheses": [],
  "recommendations": [],
  "unknowns": []
}
```

The exact schema may be improved during implementation.

Suggested commit:

```text
feat: add structured mission reasoning
```

---

# 32. PHASE 5 — DETERMINISTIC VALIDATOR

Implement validation rules.

Check:

```text
Evidence IDs
Claims
Numbers
Timestamps
Statement types
Procedure references
Unsupported claims
Evidence conflicts
Malformed outputs
```

Pipeline:

```text
LLM
 ↓
Structured Output
 ↓
Validator
 ↓
Approved Output
 ↓
UI
```

Suggested commit:

```text
feat: add evidence validation
```

---

# 33. PHASE 6 — ABSTENTION

Implement:

```text
UNKNOWN
```

Test:

- missing telemetry
- conflicting evidence
- stale evidence
- no relevant evidence
- invalid evidence

The application must explicitly explain why it cannot answer.

Suggested commit:

```text
feat: add abstention handling
```

---

# 34. PHASE 7 — INVESTIGATION TIMELINE

Implement:

- chronological events
- evidence links
- statement types
- source references
- incident context

Timeline must be generated from evidence.

Suggested commit:

```text
feat: add investigation timeline
```

---

# 35. PHASE 8 — OPERATOR DASHBOARD

Implement:

- query interface
- findings
- evidence
- hypotheses
- recommendations
- UNKNOWN state
- validation state
- timeline
- procedure references
- system status
- error states

Suggested commit:

```text
feat: build operator dashboard
```

---

# 36. PHASE 9 — EVALUATION

Create test scenarios:

- supported anomaly
- missing evidence
- competing hypotheses
- unsupported claim
- procedure lookup
- conflicting evidence

Backend tests:

```text
/health
Evidence model
Retrieval
Validator
Abstention
Timeline
```

Frontend checks:

```text
Dashboard
Query
Evidence
Observed
Inferred
Recommended
Unknown
Hypotheses
Timeline
Errors
```

End-to-end:

```text
Query
 ↓
Retrieval
 ↓
Evidence
 ↓
Reasoning
 ↓
Validation
 ↓
UI
```

Suggested commit:

```text
test: add anomaly evaluation scenarios
```

---

# 37. PHASE 10 — BUG FIXING AND INTEGRATION

Fix:

- backend/frontend integration
- schema mismatches
- UI errors
- API errors
- validation failures
- loading states
- empty states
- error states

Do not add major new features unless necessary.

Suggested commit:

```text
fix: resolve integration issues
```

---

# 38. PHASE 11 — DOCUMENTATION

Update:

```text
README.md
docs/
```

README must include:

1. Product overview
2. ST-10 problem
3. Solution
4. Architecture
5. Evidence Ledger
6. Four statement types
7. Validator
8. Abstention
9. Timeline
10. Technology stack
11. Installation
12. Run instructions
13. Demo scenarios
14. Testing
15. Limitations
16. Future scope

Never claim features that are not implemented.

Suggested commit:

```text
docs: update project documentation
```

---

# 39. FINAL RELEASE PHASE

Before submission:

- run backend tests
- run frontend tests/build
- test all demo scenarios
- test deterministic demo mode
- test missing evidence
- test unsupported claim
- test evidence inspection
- test timeline
- check README
- remove secrets
- verify `.gitignore`
- verify `.env` is not tracked
- inspect Git status
- verify repository builds from a clean checkout

Suggested final commit:

```text
release: prepare hackathon submission
```

---

# 40. GIT WORKFLOW — CRITICAL

Antigravity must actively guide the developer through Git.

After every completed milestone, Antigravity must:

1. Stop implementation.
2. Run/check the project.
3. Show files changed.
4. Show tests/checks.
5. Show `git status`.
6. Show `git diff --stat`.
7. Tell the developer whether the milestone is ready for manual commit.
8. Provide the exact commit command.
9. Provide the exact push command.
10. Wait for the developer to manually commit and push.
11. Never execute the commit/push itself.

---

# 41. BEFORE STARTING A MILESTONE

Developer manually runs:

```bash
git status
```

If the repository is clean, start the milestone.

If there are uncommitted changes:

```text
Do not blindly overwrite them.
Inspect first.
```

---

# 42. AFTER ANTIGRAVITY COMPLETES A MILESTONE

Antigravity should inspect:

```bash
git status
git diff
git diff --stat
```

Then report:

```text
MILESTONE COMPLETE

Implemented:
- ...

Files changed:
- ...

Dependencies added:
- ...

Tests/checks:
- ...

Known limitations:
- ...

Git status:
...

Diff summary:
...

READY FOR MANUAL COMMIT:
Yes / No

Suggested commit:
git add .
git commit -m "<message>"

Suggested push:
git push origin main

IMPORTANT:
No Git commit or push was performed.
Manual team-member review is required.
```

---

# 43. MANUAL COMMIT PROCEDURE

Developer manually reviews the changes.

```bash
git status
git diff
git diff --stat
```

If correct:

```bash
git add .
git status
git commit -m "<milestone commit message>"
```

---

# 44. MANUAL PUSH PROCEDURE

After successful commit:

```bash
git push origin main
git status
```

Expected:

```text
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

# 45. EXACT COMMIT COMMANDS BY PHASE

## Phase 0

```bash
git add .
git commit -m "chore: initialize MissionTrace project"
git push origin main
```

## Phase 1

```bash
git add .
git commit -m "feat: add synthetic mission datasets"
git push origin main
```

## Phase 2

```bash
git add .
git commit -m "feat: implement evidence ledger"
git push origin main
```

## Phase 3

```bash
git add .
git commit -m "feat: add hybrid evidence retrieval"
git push origin main
```

## Phase 4

```bash
git add .
git commit -m "feat: add structured mission reasoning"
git push origin main
```

## Phase 5

```bash
git add .
git commit -m "feat: add evidence validation"
git push origin main
```

## Phase 6

```bash
git add .
git commit -m "feat: add abstention handling"
git push origin main
```

## Phase 7

```bash
git add .
git commit -m "feat: add investigation timeline"
git push origin main
```

## Phase 8

```bash
git add .
git commit -m "feat: build operator dashboard"
git push origin main
```

## Phase 9

```bash
git add .
git commit -m "test: add anomaly evaluation scenarios"
git push origin main
```

## Phase 10

```bash
git add .
git commit -m "fix: resolve integration issues"
git push origin main
```

## Phase 11

```bash
git add .
git commit -m "docs: update project documentation"
git push origin main
```

## Final release

```bash
git add .
git commit -m "release: prepare hackathon submission"
git push origin main
```

**Important:** These commands are provided for the developer to run manually. Antigravity must not execute the commit or push commands.

---

# 46. WHEN TO COMMIT

Do NOT commit every tiny change.

Commit when:

```text
Meaningful milestone
        ↓
Implementation complete
        ↓
Tests/checks pass
        ↓
Developer reviews diff
        ↓
Manual commit
        ↓
Manual push
```

A reasonable target is approximately one meaningful commit every 30–90 minutes during active development, but functionality matters more than commit count.

Do NOT create artificial commits.

---

# 47. WHEN TO PUSH

Push after a successful manual commit when:

- milestone is stable
- developer reviewed the diff
- tests/checks pass
- commit represents a coherent unit of work

Recommended:

```bash
git status
git diff
git add .
git status
git commit -m "..."
git push origin main
git status
```

---

# 48. WHEN NOT TO COMMIT

Do NOT commit when:

- tests are failing
- application is broken
- secrets are present
- `.env` is tracked
- generated caches are included
- dependencies are accidentally committed
- change is incomplete
- milestone is experimental
- developer has not reviewed the diff

---

# 49. FILES THAT MUST NOT BE COMMITTED

Never commit:

```text
.env
API keys
passwords
tokens
private keys
credentials
node_modules/
Python virtual environments
large generated caches
temporary files
local secrets
```

---

# 50. ANTIGRAVITY MILESTONE STOP RULE

After each milestone, Antigravity MUST STOP.

Do not automatically proceed to the next phase.

Use:

```text
MILESTONE COMPLETE

Implemented:
...

Files changed:
...

Tests/checks:
...

Known limitations:
...

Suggested manual commit:
...

Suggested manual push:
...

No Git commit or push was performed.

Please review the changes manually.

When ready, manually run the provided Git commands and then instruct me to continue to the next phase.
```

This is mandatory.

---

# 51. ANTIGRAVITY OPERATING RULES

For every implementation request:

1. Inspect existing code first.
2. Understand the current architecture.
3. Do not unnecessarily rewrite working code.
4. Implement only the requested milestone.
5. Keep modules maintainable.
6. Avoid unnecessary dependencies.
7. Test immediately.
8. Do not fabricate functionality.
9. Do not fabricate test results.
10. Do not fabricate evidence.
11. Do not fabricate telemetry.
12. Do not fabricate API responses.
13. Do not silently hide errors.
14. Do not silently resolve conflicting evidence.
15. Do not guess when evidence is missing.
16. Never commit.
17. Never push.
18. Stop after each milestone.

---

# 52. ERROR HANDLING

## No LLM API key

Use:

```text
Deterministic Demo Mode
```

Show status clearly.

## Missing evidence

Return:

```text
UNKNOWN
```

## Conflicting evidence

Show:

```text
CONFLICTING EVIDENCE
```

and explain the conflict.

## Invalid LLM output

Reject the output.

Do not display malformed claims as facts.

## Unsupported claim

Reject or convert to:

```text
UNKNOWN
```

## Backend unavailable

Display a clear error.

Do not silently fabricate backend responses.

---

# 53. SECURITY

Never commit:

```text
API keys
passwords
tokens
private credentials
.env
```

Use:

```text
.env.example
```

Never put secrets in frontend source code.

---

# 54. TESTING REQUIREMENTS

## Backend

Test:

```text
Health endpoint
Evidence creation
Evidence retrieval
Evidence quality
Retrieval
Validator
Unsupported claims
Abstention
Timeline
Procedure lookup
```

## Frontend

Test:

```text
Dashboard
Query input
Loading state
Error state
Evidence cards
Observed card
Inferred card
Recommendation card
Unknown card
Hypothesis panel
Timeline
Procedure reference
Validation state
```

## End-to-end

```text
Operator query
      ↓
Query planner
      ↓
Retrieval
      ↓
Evidence ledger
      ↓
Reasoning
      ↓
Validator
      ↓
Approved result
      ↓
Operator UI
      ↓
Timeline
```

---

# 55. EVALUATION TARGETS

These are targets and MUST NOT be claimed as achieved until actually tested.

Target:

```text
≥95% of claims have valid evidence IDs
```

Target:

```text
100% of displayed numerical values match evidence
```

Target:

```text
Supported cause appears in top 3 hypotheses
```

Target:

```text
0 spacecraft commands issued
```

Distinguish:

```text
TARGET
```

from:

```text
MEASURED RESULT
```

---

# 56. 24-HOUR HACKATHON EXECUTION PLAN

## First 12 hours — Online

### H0–H1

Foundation:

- repo
- frontend
- backend
- `/health`
- basic UI

### H1–H3

Synthetic data:

- telemetry
- logs
- procedures
- incidents

### H3–H5

Evidence Ledger:

- evidence IDs
- provenance
- timestamps
- quality
- hashes

### H5–H7

Retrieval:

- search
- filters
- time windows
- source types

### H7–H9

Reasoning:

- structured output
- OBSERVED
- INFERRED
- RECOMMENDED
- UNKNOWN
- hypotheses

### H9–H11

Validator:

- citations
- numeric consistency
- unsupported claims
- conflicts

### H11–H12

Backend integration.

---

# 57. SECOND 12 HOURS — OFFLINE

### H12–H14

Frontend dashboard.

### H14–H16

Evidence and hypothesis UI.

### H16–H17

Timeline.

### H17–H18

Abstention.

### H18–H19

Conflict handling.

### H19–H20

Evaluation.

### H20–H21

Bug fixing.

### H21–H22

UI polish.

### H22–H23

README and demo preparation.

### H23–H24

Final testing.

---

# 58. PRIORITY IF TIME RUNS OUT

Implement in this order:

```text
1. Evidence Ledger
2. Retrieval
3. Deterministic Validator
4. Abstention
5. Supported anomaly scenario
6. Operator UI
7. Timeline
8. Hypotheses
9. Live LLM
10. Advanced infrastructure
```

A reliable small MVP is better than a complex unfinished system.

---

# 59. DEFINITION OF DONE

MissionTrace is MVP-complete when an operator can:

- open MissionTrace
- ask an anomaly question
- retrieve evidence
- see evidence IDs
- inspect evidence provenance
- see OBSERVED findings
- see INFERRED hypotheses separately
- receive RECOMMENDED diagnostic steps
- receive UNKNOWN when evidence is insufficient
- see competing hypotheses
- view an investigation timeline
- inspect procedure references
- demonstrate unsupported-claim rejection
- demonstrate missing-evidence abstention
- run deterministic demo mode
- operate without sending spacecraft commands

---

# 60. README REQUIREMENTS

README should include:

```text
MissionTrace
ST-10 Problem Statement
Why the Problem Matters
Solution
Core Principles
Architecture
Evidence Ledger
Four Statement Types
Validator
Abstention
Hypothesis Engine
Auditable Timeline
Technology Stack
Project Structure
Setup
Running Backend
Running Frontend
Demo Scenarios
Testing
Evaluation
Limitations
Future Scope
```

Never document functionality that does not actually exist.

---

# 61. FUTURE SCOPE

Future features may include:

- predictive anomaly detection
- knowledge graphs
- multi-mission correlation
- real telemetry connectors
- XTCE integration
- advanced provenance
- voice interface
- multilingual support
- forecasting
- ground-system integration
- secure on-premise LLM
- digital twin integration
- cross-spacecraft analysis

Do NOT implement these unless the core MVP is stable.

---

# 62. FINAL DEMO NARRATIVE

MissionTrace does not merely answer mission questions.

It retrieves the evidence.

It shows what was observed.

It separates what is inferred.

It recommends what the operator can check.

It explicitly identifies what is unknown.

And it records the evidence chain in an auditable timeline.

The strongest demonstration is:

```text
SUPPORTED ANSWER
        ↓
EVIDENCE
        ↓
INFERENCE
        ↓
RECOMMENDATION
        ↓
AUDIT TRAIL
```

followed by:

```text
MISSING EVIDENCE
        ↓
UNKNOWN
        ↓
NO GUESSING
```

---

# 63. FINAL ANTIGRAVITY INSTRUCTION

**START WITH PHASE 0 ONLY.**

Do not implement all phases at once.

First:

1. Inspect the existing OrbitOps repository.
2. Confirm the current Git state.
3. Create the MissionTrace foundation.
4. Create frontend shell.
5. Create backend shell.
6. Implement FastAPI `/health`.
7. Create initial MissionTrace dashboard.
8. Create README.
9. Create `.gitignore`.
10. Create `.env.example`.
11. Verify frontend.
12. Verify backend.
13. Run basic checks.
14. Inspect Git diff.
15. Report all changes.
16. Tell the developer exactly when the milestone is ready for manual commit.
17. Provide the exact manual commit command.
18. Provide the exact manual push command.
19. DO NOT execute `git commit`.
20. DO NOT execute `git push`.
21. STOP and wait for the developer.

---

# 64. FINAL MILESTONE REPORT FORMAT

After every phase, use:

```text
MILESTONE COMPLETE
===================

Phase:
<phase name>

Implemented:
- ...
- ...
- ...

Files changed:
- ...
- ...
- ...

Dependencies added:
- ...
- ...

Tests/checks:
- ...
- ...

Known limitations:
- ...
- ...

Git status:
<output>

Diff summary:
<summary>

READY FOR MANUAL COMMIT:
Yes / No

Suggested commit:
git add .
git commit -m "<message>"

Suggested push:
git push origin main

IMPORTANT:
No Git commit was performed.
No Git push was performed.

The developer must review the changes manually,
run the Git commands manually, and then instruct
Antigravity to continue to the next milestone.
```

---

# 65. GOLDEN RULE

## MissionTrace must never pretend to know what the evidence does not support.

> Every claim cited. Every gap admitted. Every action human-approved.

## Development rule:

> Every milestone tested. Every diff reviewed. Every commit manual. Every push manual.

# END OF BUILD SPECIFICATION
