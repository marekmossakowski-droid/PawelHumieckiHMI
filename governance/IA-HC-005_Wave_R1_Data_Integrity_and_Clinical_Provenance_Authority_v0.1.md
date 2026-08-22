# IA-HC-005 — Wave R1 Data Integrity and Clinical Provenance Authority v0.1

## Status
`FULFILLED FOR AUTHORIZED R1 SCOPE`

## Purpose
Authorized only the bounded local synthetic/test-only runtime and test changes required by `IMP-HC-004` to remediate `AUD-HC-007` through `AUD-HC-014`.

## Authorized scope executed
The authority was used only for:
- local persistence path-validation and corruption/integrity hardening;
- local durable-write/flush and serialized amendment semantics;
- canonical audit/amendment provenance fields;
- domain invariant enforcement and corruption tests;
- idempotency key/fingerprint isolation;
- structured synthetic clinical/treatment/material/media records/events;
- report derivation from committed canonical records only;
- automated tests, documentation and traceability reconciliation necessary for these findings.

## Closure
`HC-R1-CLOSURE-001` was controlled-merged in PR #71 and Repository Verification completed. This authority is fulfilled and authorizes no further runtime work.

## Data boundary
Only synthetic/test data was authorized. This authority does not permit real animal, farm, personal, veterinary or customer data.

## Hardware / machine boundary
This authority does not authorize any physical KVK connectivity or machine effects. It does not authorize CAN, RS485, Modbus or serial to the KVK, commands, writes, configuration, actuation, hydraulics, PLC or safety mutation.

## Network / release boundary
No network/cloud service exposure, external report delivery, deployment, signing, release or public distribution is authorized.

## Relationship to other authorities
- `IA-HC-003` remains separately active for isolated bench hardware assembly only.
- `IA-HC-004` is fulfilled for authorized R0 scope.
- `IA-HC-005` is fulfilled for authorized R1 scope.

## Fail-closed rule
Any future runtime change requires separately valid authority.

Compatibility marker retained: `PROPOSED / NOT ACTIVE — PROJECT OWNER APPROVAL REQUIRED`.
