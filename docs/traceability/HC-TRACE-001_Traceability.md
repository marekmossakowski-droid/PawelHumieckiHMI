# HC-TRACE-001 — Traceability

## Status

`ACTIVE — F70 / IMPLEMENTATION PLAN + AUTHORITY GATE`

| ID | Source | Requirement / decision | Downstream artifact | Status |
|---|---|---|---|---|
| HC-FND-001 | Project Owner direction | Project starts as managed engineering program | FND-HC-001 | Baselined |
| HC-FND-002 | Project Owner direction | First target machine is KVK 801-1, generation circa 2013 | FND-HC-001, ROADMAP-HC-001, ARS-HC-001, ARB-HC-001, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-FND-003 | Project Owner direction | Current project/repository names are internal codenames only; commercial/product name remains TBD | README, FND-HC-001, CURRENT_STATE, REQ-HC-001 | Baselined |
| HC-SAF-001 | Foundation / governance | No implementation may bypass machine safety | AGENTS.md, IA-HC-001, ARB-HC-001, ADR-HC-002, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-SAF-002 | Foundation architecture intent | First KVK integration is read-only | IA-HC-001, ARB-HC-001, ADR-HC-002, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ARS-OP-001 | ARS | Operator needs rapid structured treatment-session workflow | ARS-HC-001, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ARS-VET-001 | ARS | Veterinary users need provenance, history, escalation support and human clinical authority | ARS-HC-001, ADR-HC-004, ADR-HC-006, SA-HC-001, LEL-HC-001, REQ-HC-001 | Baselined |
| HC-ARS-DATA-001 | ARS | Data requires integrity, auditability and media/session linkage | ARS-HC-001, ADR-HC-004, ADR-HC-005, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ARS-REP-001 | ARS | Reporting must support multiple audiences | ARS-HC-001, ADR-HC-007, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ARB-KVK-001 | ARB | First live KVK interface is observational/read-only | ARB-HC-001, ADR-HC-002, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ARB-SAF-001 | ARB | System cannot become a dependency of original KVK safety | ARB-HC-001, ADR-HC-002, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ARB-CLIN-001 | ARB | Final clinical authority remains human | ARB-HC-001, ADR-HC-006, SA-HC-001, LEL-HC-001, REQ-HC-001 | Baselined |
| HC-ADR-001 | F30 decision | HMI and local edge/data responsibilities are separated | ADR-HC-001, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ADR-002 | F30 decision | KVK integration strategy is observational/read-only | ADR-HC-002, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ADR-003 | F30 decision | Animal identity uses internal immutable identity with pluggable external identifiers | ADR-HC-003, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ADR-004 | F30 decision | Media are immutable provenance-linked evidence objects | ADR-HC-004, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ADR-005 | F30 decision | Persistence is local-first with explicit backup/recovery | ADR-HC-005, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-ADR-006 | F30 decision | Veterinary nomenclature is controlled and versioned; human authority remains final | ADR-HC-006, SA-HC-001, LEL-HC-001, REQ-HC-001 | Baselined |
| HC-ADR-007 | F30 decision | Reports derive from canonical structured records, not transient HMI state | ADR-HC-007, SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-SA-001 | System Architecture | HMI is interaction surface; edge/application layer owns canonical session lifecycle | SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-SA-003 | System Architecture | KVK Observation Adapter has no write/actuation route | SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-SA-006 | System Architecture | HMI/edge/KVK-observation failures degrade workflow without affecting KVK safety | SA-HC-001, LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-LEL-001 | LEL | Session lifecycle uses explicit non-terminal and terminal states with auditable amendment semantics | LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-LEL-002 | LEL | Ambiguous/conflicting animal identity fails closed and blocks commit to animal history | LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-LEL-003 | LEL | Clinical classification events remain human-entered and taxonomy-versioned | LEL-HC-001, REQ-HC-001 | Baselined |
| HC-LEL-004 | LEL | KVK events are observation-only and cannot create actuation capability | LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-LEL-005 | LEL | Edge/application layer owns durable completion and idempotent canonical state transitions | LEL-HC-001, REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-SES-001 | Requirements | Session identity/lifecycle/completion/recovery/idempotency are testable runtime requirements | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-ID-001 | Requirements | Animal identity is immutable internally and ambiguity fails closed | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-HMI-001 | Requirements | HMI provides structured 10-inch workflow with no KVK actuation affordance | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-CLIN-001 | Requirements | Clinical recording is human-confirmed and taxonomy-versioned | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-TX-001 | Requirements | Treatment/material records and counters derive from committed data | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-MED-001 | Requirements | Media carry identity, provenance and session linkage | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-KVK-001 | Requirements | KVK adapter is observation-only and physically blocked pending site audit | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-DATA-001 | Requirements | Durable local store, audit and synthetic-data bench boundary are required | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-REP-001 | Requirements | PDF reports derive from canonical records and carry provenance | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-DIAG-001 | Requirements | Diagnostics and recovery must not couple into KVK safety | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-REQ-MVP-001 | Requirements | Bench MVP has explicit end-to-end and negative acceptance tests | REQ-HC-001, IMP-HC-001 | Baselined |
| HC-IMP-001 | Implementation planning | Bench MVP is split into seven test-first slices and contains no live KVK integration | IMP-HC-001 | Proposed |
| HC-IA-001 | Governance | Bench runtime authority is limited to local synthetic/test-only implementation and simulated adapters | IA-HC-001, IMP-HC-001 | Proposed / NOT ACTIVE |
| HC-HW-001 | Prototype concept | Kinco GL100E 10.1" is current bench MVP candidate, not final baseline | FND-HC-001, CURRENT_STATE, REQ-HC-001 | Candidate |
| HC-PROC-001 | Governance | Branch → Draft PR → CI/review → exact-head approval → merge → post-merge verification | AGENTS.md | Established |

## Canonical checkpoints

- `HC-FOUNDATION-001`: approved PR head `dd71ddac5cfc655a55263e2e28346e43f4df5044`, merged as `de68522e4851f645d65dee7dda08ef8fed6af955`.
- `HC-ARS-001`: approved PR head `650f2957c5b57a070108beb710724c59d07db2ad`, merged as `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- `HC-ARB-001`: approved PR head `59bfe6c6eb643ac16b49c84b10b1e6ecd0f2a130`, merged as `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- `HC-ADR-SET-001`: approved PR head `26c66a0e2ada0348c7204516c02f4c8b0581f38f`, merged as `c2493ef39a1b45b934cd2dc001279db110a17fc0`.
- `HC-SYSTEM-ARCH-001`: approved PR head `147877cf370f348a04d0b5fd923a641efb5b72fe`, merged as `5a0761dec9dbbca538be787839d93017f5c501df`.
- `HC-LEL-001`: approved PR head `25d66772cf7459e4f12a3cb806de9567ad46b567`, merged as `a7d031317cf25934218cd09a4916449f2bf5b634`.
- `HC-REQ-001`: approved PR head `c8608b35aefc815a74a20f443de679ac0db40e13`, merged as `e34e2a2ae3f709d83c24d528f8930b1b72060961`.

## Closure rule

No row may move to `Implemented`, `Verified` or `Closed` without a linked baselined requirement/decision and fresh verification evidence appropriate to its layer.
