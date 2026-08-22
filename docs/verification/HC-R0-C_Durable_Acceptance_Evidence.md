# HC-R0-C — Durable completion and evidence-derived acceptance

## Status
`IMPLEMENTED / VERIFIED — AWAITING PROJECT OWNER MERGE APPROVAL`

## Scope
Remediation of `AUD-HC-004` and `AUD-HC-005` under active `IA-HC-004`.

## TDD lineage
- RED: `3855899b667d59b89ee9a7f916fba841877094b1` — runtime-ci failed as expected because durable completion/evidence acceptance APIs did not exist.
- GREEN: `3dc7117ff3b75b30517cc6291f456fe82e2d3561` — runtime-ci and docs-ci passed.

## Verified behavior
- completion is returned only after local persistence succeeds;
- persistence failure propagates and the original in-memory session remains `IN_PROGRESS`;
- acceptance verifies recovery of the committed completed session;
- report acceptance requires valid PDF structure evidence and canonical source session linkage;
- acceptance status is calculated from concrete checks rather than a standalone hard-coded end-to-end PASS value;
- synthetic-only and no-KVK-connection invariants remain explicit.

## Boundary
This work does not establish field acceptance, real-farm-data authority, edge-host deployment readiness or any real KVK integration.
