# HC-REQ-TRACE-001 — Requirement-Level Traceability Matrix v0.1

## Status
`ACTIVE / R0 RECONCILIATION`

Legend: `IMPLEMENTED`, `PARTIAL`, `DEFERRED`, `BLOCKED`.

| Requirement | Status | Primary evidence / disposition |
|---|---|---|
| REQ-HC-SES-001 | IMPLEMENTED | `domain/session.py`; unique UUID session |
| REQ-HC-SES-002 | IMPLEMENTED | domain state enum; LEL mapping |
| REQ-HC-SES-003 | IMPLEMENTED | R0-C `complete_and_commit`; persistence-failure negative test |
| REQ-HC-SES-004 | PARTIAL | local recovery tests exist; physical edge host unresolved |
| REQ-HC-SES-005 | PARTIAL | event duplicate IDs implemented; service-level idempotency hardening remains R1 |
| REQ-HC-ID-001 | PARTIAL | immutable session animal_id exists; separate canonical animal entity remains R1 |
| REQ-HC-ID-002 | DEFERRED | external identifier entity not yet implemented |
| REQ-HC-ID-003 | IMPLEMENTED | ambiguity fail-closed domain/application tests |
| REQ-HC-ID-004 | IMPLEMENTED | simulated identity/RFID path |
| REQ-HC-HMI-001 | PARTIAL | dashboard model exists; native GL100E realization pending HW-A3 |
| REQ-HC-HMI-002 | IMPLEMENTED | codename separation in governance/README |
| REQ-HC-HMI-003 | PARTIAL | synthetic workflow + DTools spec; physical test pending |
| REQ-HC-HMI-004 | PARTIAL | synthetic workflow + DTools spec; physical test pending |
| REQ-HC-HMI-005 | PARTIAL | zone model exists; full physical map validation pending |
| REQ-HC-HMI-006 | PARTIAL | 64×64 minimum + GL100E geometry spec; physical glove test pending |
| REQ-HC-HMI-007 | IMPLEMENTED | no machine-control UI/API under current scope; negative checks |
| REQ-HC-CLIN-001 | PARTIAL | human selection modeled synthetically |
| REQ-HC-CLIN-002 | PARTIAL | lesion enum/catalogue concept; versioned catalogue remains R1 |
| REQ-HC-CLIN-003 | DEFERRED | supplemental free text not canonicalized |
| REQ-HC-CLIN-004 | DEFERRED | taxonomy provenance remains R1 |
| REQ-HC-CLIN-005 | IMPLEMENTED | no autonomous diagnostic surface; disclaimer |
| REQ-HC-TX-001 | PARTIAL | synthetic treatment selection; canonical structured events remain R1 |
| REQ-HC-TX-002 | PARTIAL | dressing/material refs exist; canonical structured material records remain R1 |
| REQ-HC-TX-003 | PARTIAL | dashboard binding exists; committed-record counter implementation incomplete |
| REQ-HC-TX-004 | PARTIAL | amendment concept exists; provenance hardening remains R1 |
| REQ-HC-MED-001 | PARTIAL | reference IDs exist; canonical media entity remains R1 |
| REQ-HC-MED-002 | PARTIAL | media refs session-linked synthetically |
| REQ-HC-MED-003 | DEFERRED | BEFORE/AFTER/reference typed metadata remains R1 |
| REQ-HC-MED-004 | PARTIAL | policy represented; typed provenance remains R1 |
| REQ-HC-MED-005 | IMPLEMENTED | synthetic/test-only media boundary |
| REQ-HC-KVK-001 | BLOCKED | no live adapter; site audit required |
| REQ-HC-KVK-002 | IMPLEMENTED | current software exposes no live KVK write route |
| REQ-HC-KVK-003 | BLOCKED | real observation semantics require site/interface evidence |
| REQ-HC-KVK-004 | IMPLEMENTED FOR CURRENT SCOPE | system has no safety dependency or machine connection |
| REQ-HC-KVK-005 | IMPLEMENTED AS GATE | live connection explicitly blocked pending site audit |
| REQ-HC-DATA-001 | IMPLEMENTED | local/offline runtime and tests |
| REQ-HC-DATA-002 | PARTIAL | HMI-independent architecture preserved; concrete edge host `EDGE_HOST_REQUIRED` |
| REQ-HC-DATA-003 | PARTIAL | append-only amendment concept; mandatory provenance hardening remains R1 |
| REQ-HC-DATA-004 | PARTIAL | no silent reassignment path identified; canonical media entity remains R1 |
| REQ-HC-DATA-005 | IMPLEMENTED | synthetic/test-only invariant |
| REQ-HC-REP-001 | PARTIAL | committed session required; full clinical content canonicalization remains R1 |
| REQ-HC-REP-002 | IMPLEMENTED | R0-B structurally valid deterministic local PDF |
| REQ-HC-REP-003 | IMPLEMENTED | five audience sections |
| REQ-HC-REP-004 | IMPLEMENTED | report ID, timestamp, source session |
| REQ-HC-REP-005 | IMPLEMENTED | clinical disclaimer |
| REQ-HC-DIAG-001 | DEFERRED | component health model remains R2 |
| REQ-HC-DIAG-002 | PARTIAL | synthetic adapter failure boundaries exist; health envelope remains R2 |
| REQ-HC-DIAG-003 | PARTIAL | restart recovery exists; full incomplete-session transaction recovery remains later hardening |
| REQ-HC-DIAG-004 | IMPLEMENTED | no KVK safety coupling |
| REQ-HC-MVP-001 | PARTIAL | synthetic end-to-end exists; canonical structured clinical/media events incomplete |
| REQ-HC-MVP-002 | IMPLEMENTED | ambiguity negative tests |
| REQ-HC-MVP-003 | IMPLEMENTED FOR SYNTHETIC SCOPE | persisted session recovery tests |
| REQ-HC-MVP-004 | IMPLEMENTED AT DOMAIN LEVEL | duplicate event ID behavior; service-level request collision remains R1 |
| REQ-HC-MVP-005 | PARTIAL | reference labeling policy exists; typed media provenance remains R1 |
| REQ-HC-MVP-006 | IMPLEMENTED FOR CURRENT PUBLIC SURFACE | no KVK actuation route; broader allowlist hardening remains R2 |
| REQ-HC-JOB-ROLE-A1-001 | PARTIAL | local synthetic open/correct/treat/close domain and application flow; final physical HMI realization remains pending |
| REQ-HC-JOB-ROLE-A1-002 | IMPLEMENTED FOR SYNTHETIC SCOPE | `test_pawel_sees_prices_without_owner_pin_at_open_and_correction` |
| REQ-HC-JOB-ROLE-A1-003 | IMPLEMENTED FOR SYNTHETIC SCOPE | `test_work_screen_hides_prices_and_first_cow_removes_edit_action` |
| REQ-HC-JOB-PRICE-A1-001 | IMPLEMENTED FOR SYNTHETIC SCOPE | `test_open_correct_restart_complete_freeze_and_close`; `test_service_persists_correction_before_returning_success` |
| REQ-HC-JOB-PRICE-A1-002 | IMPLEMENTED FOR SYNTHETIC SCOPE | `test_first_completed_cow_freezes_all_prices`; `test_open_correct_restart_complete_freeze_and_close` |
| REQ-HC-JOB-PRICE-A1-003 | IMPLEMENTED FOR SYNTHETIC SCOPE | domain retry/conflict tests plus schema-v2 audit round-trip and corruption tests |
| REQ-HC-JOB-PRICE-A1-004 | IMPLEMENTED FOR SYNTHETIC SCOPE | immutable versioned snapshot tests and `test_open_correct_restart_complete_freeze_and_close` |

## R0 closures represented by this matrix
- AUD-HC-003: corrected by R0-B valid PDF renderer.
- AUD-HC-004 / AUD-HC-005: corrected by R0-C durable/evidence-derived acceptance.
- AUD-HC-006: corrected by R0-A exact GL100E + KS123-14DR profile.
- AUD-HC-017: requirement-level mapping established here.

This matrix does not convert PARTIAL/DEFERRED/BLOCKED requirements to implemented and does not expand authority.

`REQ-HC-002-A1` evidence remains local and synthetic/test-only. The mapping does
not claim a finished GUI, physical GL100E acceptance, Generation 2, real data,
device access, deployment or closed-settlement correction.
