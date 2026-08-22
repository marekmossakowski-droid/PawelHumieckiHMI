# IMP-HC-004 — Wave R1 Data Integrity and Clinical Provenance v0.1

## Status
`FULFILLED FOR AUTHORIZED R1 SCOPE — CLOSURE PENDING OWNER MERGE`

## Purpose
Close audit findings `AUD-HC-007` through `AUD-HC-014` before any future consideration of real-farm-data authority.

## Scope
Wave R1 is local, synthetic/test-only remediation. It covers persistence security/durability/integrity, amendment/audit provenance, domain invariants, idempotency isolation, canonical clinical/treatment/material/media records and report generation exclusively from committed canonical data.

## Verified execution
- R1-A — Persistence path safety: PR #67 MERGED / VERIFIED.
- R1-B/C — Persistence durability/integrity + canonical amendment provenance: PR #68 MERGED / VERIFIED.
- R1-D/E — Domain invariants + idempotency isolation: PR #69 MERGED / VERIFIED.
- R1-F/G/H — Canonical clinical model + canonical report source + media provenance: PR #70 MERGED / VERIFIED.

## Closure gate
`HC-R1-CLOSURE-001` is the only record allowed to establish final closure after controlled Project Owner approval, merge and Repository Verification.

## Exit criteria
All `AUD-HC-007` through `AUD-HC-014` have automated evidence and reconciliation. Final closure remains pending owner-approved merge of `HC-R1-CLOSURE-001`.

## Explicit exclusions
No real-farm data; no live RFID hardware; no network/cloud; no external report delivery; no real KVK connection; no CAN/RS485/Modbus/serial to KVK; no machine commands/writes/configuration/actuation; no hydraulics; no PLC/safety mutation; no deployment/signing/release/public distribution.

Compatibility marker retained: `PROPOSED — PROJECT OWNER APPROVAL REQUIRED`.
