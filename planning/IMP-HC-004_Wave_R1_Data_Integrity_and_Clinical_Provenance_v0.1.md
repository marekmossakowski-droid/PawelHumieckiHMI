# IMP-HC-004 — Wave R1 Data Integrity and Clinical Provenance v0.1

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Purpose
Close audit findings `AUD-HC-007` through `AUD-HC-014` before any future consideration of real-farm-data authority.

## Scope
Wave R1 is local, synthetic/test-only remediation. It covers persistence security/durability/integrity, amendment/audit provenance, domain invariants, idempotency isolation, canonical clinical/treatment/material/media records and report generation exclusively from committed canonical data.

## R1-A — Persistence path safety
- validate/map session identifiers to safe local filenames;
- add path-traversal negative tests;
- preserve existing local-only storage boundary.

## R1-B — Persistence durability and integrity
- add schema/version metadata;
- define corruption/integrity checks;
- use an explicit durable flush strategy appropriate to the local bench filesystem;
- serialize amendment append and sequence allocation.

## R1-C — Canonical amendment/audit provenance
Every material amendment SHALL include record identity, timestamp, change context and operator/source provenance. Completed records SHALL not be silently overwritten.

## R1-D — Domain invariants
Add construction/deserialization invariants so impossible identity/session combinations fail closed, including corruption tests.

## R1-E — Idempotency isolation
Namespace request idempotency by operation and resource/session, or bind request IDs to a deterministic request fingerprint and reject mismatched reuse.

## R1-F — Canonical clinical event/data model
Introduce structured canonical records/events for lesion/taxonomy version, treatment actions and consumed materials sufficient to meet current REQ-HC requirements for synthetic bench scope.

## R1-G — Canonical report source
Reports SHALL derive clinical/treatment/material content only from committed canonical records. Transient caller summaries SHALL not establish canonical report truth.

## R1-H — Media provenance
Introduce explicit media metadata including immutable media ID, originating session, category (`BEFORE`, `AFTER`, `REFERENCE` or explicit equivalent), timestamp/source provenance and no-silent-reassignment controls.

## Execution method
Each runtime change follows TDD: RED → minimal GREEN → verification → reconciliation. No slice may claim completion without both runtime-ci and docs-ci green.

## Explicit exclusions
No real-farm data; no live RFID hardware; no network/cloud; no external report delivery; no real KVK connection; no CAN/RS485/Modbus/serial to KVK; no machine commands/writes/configuration/actuation; no hydraulics; no PLC/safety mutation; no deployment/signing/release/public distribution.

## Exit criteria
Wave R1 may close only when `AUD-HC-007` through `AUD-HC-014` are individually reconciled with automated evidence and documentation/traceability, while all existing KVK/safety/privacy boundaries remain unchanged.
