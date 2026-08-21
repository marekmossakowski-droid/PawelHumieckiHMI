# HC-TRACE-001 — Traceability

## Status

`ACTIVE — F80 / BENCH IMPLEMENTATION`

| ID | Source | Requirement / decision | Downstream artifact | Status |
|---|---|---|---|---|
| HC-FND-001 | Project Owner direction | Project starts as managed engineering program | FND-HC-001 | Baselined |
| HC-FND-002 | Project Owner direction | First target machine is KVK 801-1, generation circa 2013 | Foundation → REQ-HC-001 → IMP-HC-001 | Baselined |
| HC-FND-003 | Project Owner direction | Project/repository names are internal codenames only | README, FND-HC-001, CURRENT_STATE | Baselined |
| HC-SAF-001 | Governance | No implementation may bypass machine safety | AGENTS.md, IA-HC-001, architecture, requirements | Baselined |
| HC-SAF-002 | Architecture | First KVK integration is observational/read-only | IA-HC-001, ARB, ADR, SA, LEL, REQ, IMP | Baselined |
| HC-ARS-OP-001 | ARS | Operator needs rapid structured treatment-session workflow | ARS → SA → LEL → REQ → IMP | Baselined |
| HC-ARS-VET-001 | ARS | Human clinical authority and provenance are required | ARS → ADR → SA → LEL → REQ | Baselined |
| HC-ARS-DATA-001 | ARS | Data requires integrity, auditability and media/session linkage | ARS → SA → LEL → REQ → IMP | Baselined |
| HC-ARS-REP-001 | ARS | Reporting must support multiple audiences | ARS → ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ARB-KVK-001 | ARB | First live KVK interface is observational/read-only | ARB → ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ARB-SAF-001 | ARB | System cannot become a dependency of original KVK safety | ARB → SA → LEL → REQ → IMP | Baselined |
| HC-ARB-CLIN-001 | ARB | Final clinical authority remains human | ARB → ADR → SA → LEL → REQ | Baselined |
| HC-ADR-001 | ADR | HMI and local edge/data responsibilities are separated | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-002 | ADR | KVK integration strategy is observational/read-only | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-003 | ADR | Animal identity uses internal immutable identity with pluggable external identifiers | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-004 | ADR | Media are immutable provenance-linked evidence objects | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-005 | ADR | Persistence is local-first with explicit backup/recovery | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-ADR-006 | ADR | Veterinary nomenclature is controlled/versioned; human authority remains final | ADR → SA → LEL → REQ | Baselined |
| HC-ADR-007 | ADR | Reports derive from canonical structured records | ADR → SA → LEL → REQ → IMP | Baselined |
| HC-SA-001 | System Architecture | Edge/application layer owns canonical session lifecycle | SA → LEL → REQ → IMP → HC-S1-001 | Baselined |
| HC-SA-003 | System Architecture | KVK Observation Adapter has no write/actuation route | SA → LEL → REQ → IMP | Baselined |
| HC-SA-006 | System Architecture | Failures degrade workflow without affecting KVK safety | SA → LEL → REQ → IMP | Baselined |
| HC-LEL-001 | LEL | Session lifecycle has explicit non-terminal and terminal states | LEL → REQ → IMP → HC-S1-001 | Baselined |
| HC-LEL-002 | LEL | Ambiguous identity fails closed | LEL → REQ → IMP → HC-S1-001 | Baselined |
| HC-LEL-003 | LEL | Clinical classification remains human-entered and taxonomy-versioned | LEL → REQ | Baselined |
| HC-LEL-004 | LEL | KVK events are observation-only | LEL → REQ → IMP | Baselined |
| HC-LEL-005 | LEL | Edge owns durable/idempotent canonical transitions | LEL → REQ → IMP → HC-S1-001 | Baselined |
| HC-REQ-SES-001 | Requirements | Session lifecycle/completion/recovery/idempotency are testable runtime requirements | REQ → IMP → HC-S1-001 | Baselined |
| HC-REQ-ID-001 | Requirements | Animal identity is immutable internally and ambiguity fails closed | REQ → IMP → HC-S1-001 | Baselined |
| HC-REQ-HMI-001 | Requirements | Structured 10-inch HMI workflow has no KVK actuation affordance | REQ → IMP | Baselined |
| HC-REQ-CLIN-001 | Requirements | Clinical recording is human-confirmed and taxonomy-versioned | REQ → IMP | Baselined |
| HC-REQ-TX-001 | Requirements | Treatment/material counters derive from committed data | REQ → IMP | Baselined |
| HC-REQ-MED-001 | Requirements | Media carry identity, provenance and session linkage | REQ → IMP | Baselined |
| HC-REQ-KVK-001 | Requirements | KVK adapter is observation-only and blocked pending site audit | REQ → IMP | Baselined |
| HC-REQ-DATA-001 | Requirements | Durable local store/audit/synthetic bench boundary required | REQ → IMP | Baselined |
| HC-REQ-REP-001 | Requirements | PDF reports derive from canonical records | REQ → IMP | Baselined |
| HC-REQ-DIAG-001 | Requirements | Diagnostics/recovery cannot couple into KVK safety | REQ → IMP | Baselined |
| HC-REQ-MVP-001 | Requirements | Bench MVP has explicit acceptance/negative tests | REQ → IMP | Baselined |
| HC-IMP-001 | Implementation plan | Bench MVP split into seven test-first slices, no live KVK integration | IMP-HC-001 | Approved / Baselined PR #8 |
| HC-IA-001 | Governance | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | ACTIVE — PR #8 |
| HC-S1-RED-001 | TDD | Domain/session tests fail before implementation exists | tests/test_session_core.py, runtime-ci | Verified RED @ `52b4fca3ca719b035d2cc7c5091447c607b6fd83` |
| HC-S1-CORE-001 | S1 | New session begins IDENTITY_PENDING; confirmed identity enters IN_PROGRESS | src/hoofcare/domain/session.py | Implemented / GREEN |
| HC-S1-FAILCLOSED-001 | S1 | Ambiguous identity cannot bind animal_id or advance workflow | src/hoofcare/domain/session.py, tests | Implemented / GREEN |
| HC-S1-IDEMP-001 | S1 | Duplicate event IDs are idempotent | src/hoofcare/domain/session.py, tests | Implemented / GREEN |
| HC-S1-TERM-001 | S1 | Completion requires confirmed identity and terminal sessions reject new events | src/hoofcare/domain/session.py, tests | Implemented / GREEN |
| HC-HW-001 | Prototype concept | Kinco GL100E 10.1" remains bench MVP candidate, not baseline | CURRENT_STATE | Candidate |
| HC-PROC-001 | Governance | Draft PR → CI/review → exact-head approval → merge → verification | AGENTS.md | Established |

## Canonical checkpoints

- PR #1 Foundation → `de68522e4851f645d65dee7dda08ef8fed6af955`.
- PR #2 ARS → `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- PR #3 ARB → `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- PR #4 ADR set → `c2493ef39a1b45b934cd2dc001279db110a17fc0`.
- PR #5 System Architecture → `5a0761dec9dbbca538be787839d93017f5c501df`.
- PR #6 LEL → `a7d031317cf25934218cd09a4916449f2bf5b634`.
- PR #7 Requirements → `e34e2a2ae3f709d83c24d528f8930b1b72060961`.
- PR #8 IMP + IA activation: approved head `9c939abea6794e2b5a4815c826410eb0166ab535`, merged `0d58eb2921df298114c304295a061547598ae541`.

## Closure rule

No runtime row becomes Closed without fresh verification evidence and controlled merge on the exact approved head.
