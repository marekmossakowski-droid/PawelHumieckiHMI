# HC-REQ-HC-003-G1-CLOSURE-001 — Generation 1 bounded closure evidence

## Status

`PROPOSED / BOUNDED RUNTIME-GUI CLOSURE READY / NATIVE DTOOLS EVIDENCE BLOCKED / PROJECT OWNER MERGE REQUIRED`

## Scope

This record reconciles Task `G1-6 — Restart integration, requirement traceability and bounded closure` under active `IA-HC-008`.

It does not claim physical GL100E acceptance, upload, deployment, real data, device access, live RFID/camera, KVK I/O, machine control or completion of the native DTools artifact requirement.

## Fresh G1-6 TDD lineage

- RED head: `acd924888953427f66309e8847e0fed550b64456` — test-only checkpoint; production surface absent.
- GREEN head: `784fe3635077e45c5fc0a30dd72eb7a049676b64` — complete synthetic restart orchestration through existing public seams.
- GREEN verification: `runtime-ci #508 = SUCCESS`, `docs-ci #397 = SUCCESS`.

The scenario exercises:
- durable local job/session stores with restart;
- exactly two uniquely completed synthetic cows;
- idempotent retry without counter inflation;
- canonical settlement projection `RAZEM NETTO: 122,00 zł`;
- routine work with prices hidden;
- deterministic owner-zone inactivity expiry;
- repository GL100E manifest validation in offline synthetic/no-device scope.

## Requirement-level bounded evidence

| Requirement | Bounded G1 disposition | Primary evidence |
|---|---|---|
| REQ-HC-G1-NAV-001 | IMPLEMENTED | G1-1 route graph + G1 manifest route coverage |
| REQ-HC-G1-NAV-002 | IMPLEMENTED | G1-1 deterministic allow/deny/recovery guards |
| REQ-HC-G1-NAV-003 | IMPLEMENTED FOR REPOSITORY DEVICE PROFILE | G1-5 GL100E 1024×600 geometry, >=64×64 targets; physical glove acceptance remains outside this closure |
| REQ-HC-G1-JOB-001 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-2 opening/pricing projections and canonical Job model |
| REQ-HC-G1-JOB-002 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-2 pricing boundary; G1-6 verifies routine work prices hidden |
| REQ-HC-G1-JOB-003 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-2 active-job projection |
| REQ-HC-G1-TREAT-001 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-3 complete treatment wizard projections |
| REQ-HC-G1-TREAT-002 | IMPLEMENTED FOR SYNTHETIC SCOPE | canonical durable completion; G1-6 restart/idempotency evidence |
| REQ-HC-G1-TREAT-003 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-3 material projections without routine prices |
| REQ-HC-G1-TREAT-004 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-1/G1-3 fail-closed recovery and completion guards |
| REQ-HC-G1-STAT-001 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-4 work statistics projection |
| REQ-HC-G1-STAT-002 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-4 stored settlement projection; G1-6 `RAZEM NETTO: 122,00 zł` |
| REQ-HC-G1-STAT-003 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-4 local history/report surfaces and deterministic PDF reuse |
| REQ-HC-G1-ADMIN-001 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-1 six-digit gate, lockout and ten-minute expiry; G1-6 expiry evidence |
| REQ-HC-G1-ADMIN-002 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-4 explicit capability allowlist |
| REQ-HC-G1-ADMIN-003 | IMPLEMENTED FOR SYNTHETIC SCOPE | G1-1/G1-2 operator paths independent of owner unlock |
| REQ-HC-G1-ADAPT-001 | IMPLEMENTED | semantic G1 view models separated from physical profile |
| REQ-HC-G1-ADAPT-002 | IMPLEMENTED FOR REPOSITORY DEVICE PROFILE | G1-5 `Gl100eProfile` and validated manifest |
| REQ-HC-G1-ADAPT-003 | IMPLEMENTED AS EXCLUSION | no Generation 2/network/synchronization implementation in G1 scope |
| REQ-HC-G1-DTOOLS-001 | BLOCKED | canonical `dtools/gl100e/README.md` truthfully states `NATIVE_DTOOLS_ARTIFACT_REQUIRED` |
| REQ-HC-G1-DTOOLS-002 | IMPLEMENTED | fail-closed typed binding manifest and validator |
| REQ-HC-G1-DTOOLS-003 | BLOCKED | offline native DTools compile with zero-error log/hash is not yet evidenced |
| REQ-HC-G1-DTOOLS-004 | IMPLEMENTED AS SAFETY BOUNDARY | upload/physical acceptance remain separately blocked; HW-A1/HW-A2/HW-A3 are not claimed PASS |

Summary: `21/23` G1 requirements have bounded repository/synthetic evidence; `2/23` remain explicitly blocked by missing native DTools project/compile evidence.

## Closure decision if this exact PR head is approved and merged

The merge MAY establish only:

`G1-1..G1-6 RUNTIME/GUI = IMPLEMENTED / VERIFIED / RECONCILED FOR BOUNDED SYNTHETIC SCOPE`

and:

`REQ-HC-003-G1 = PARTIALLY FULFILLED / NATIVE DTOOLS ARTIFACT AND OFFLINE COMPILE EVIDENCE REMAIN BLOCKED`.

It MUST NOT establish full REQ-HC-003-G1 closure while `REQ-HC-G1-DTOOLS-001` or `REQ-HC-G1-DTOOLS-003` remains blocked.

## Explicit blockers

- `native_dtools_artifact = REQUIRED / NOT YET EVIDENCED`;
- `edge_host = EDGE_HOST_REQUIRED / NOT YET SELECTED`;
- physical GL100E receipt/inspection and hardware gates remain separate;
- no physical upload or panel acceptance is authorized by this record.

## Safety boundary

No Generation 2, real-farm data, network/cloud synchronization, live RFID, camera, device/KVK I/O, machine bus, commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, production authentication, invoicing/VAT/accounting/payments, deployment, signing, release or public distribution is authorized.
