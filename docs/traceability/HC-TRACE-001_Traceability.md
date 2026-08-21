# HC-TRACE-001 — Traceability

## Status
`ACTIVE — BENCH MVP CLOSED / IA-HC-002 ACTIVE / P1-P5 MERGED / VERIFIED / P6 IMPLEMENTED / GREEN`

## Baselined upstream lineage

| ID | Decision / requirement | Downstream | Status |
|---|---|---|---|
| HC-FND-001 | Managed engineering program | Foundation → IMP | Baselined |
| HC-FND-002 | First target is circa-2013 KVK 801-1 | Foundation → REQ → IMP | Baselined |
| HC-SAF-001 | HoofCare cannot bypass or become part of KVK safety | IA / ARB / SA / REQ / IMP | Baselined |
| HC-SAF-002 | KVK integration boundary is observational/read-only | IA / ADR / SA / LEL / REQ / IMP | Baselined |
| HC-IMP-001 | Seven test-first bench slices; no live KVK integration | IMP-HC-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IA-001 | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | FULFILLED FOR AUTHORIZED BENCH SCOPE |
| HC-IA-002 | Physical prototype authority | IA-HC-002 | APPROVED / ACTIVE — PR #27 |

## Runtime / physical prototype lineage

| Slice | RED evidence | Verification | Status |
|---|---|---|---|
| S1-S7 Bench MVP | canonical S1-S7 TDD lineage | PR #9 through #16 | MERGED / VERIFIED |
| P1 Physical prototype hardware profile | `87a9f6329e1ade0b1add79b4469ebb1b14393b40` | PR #29 merge `ec2cea9b144256baca29cd1ea2f03bf0dfcf6def` | MERGED / VERIFIED |
| P2 HMI layout/touch mapping | `8e199b0f9ea398ab21d8ad6e6062bf7291ae6df2` | PR #31 merge `047e5bba348eaea0b52103230ec589df6f857036` | MERGED / VERIFIED |
| P3 Bench wiring BOM / isolated I/O | `65e62602e75d6f76c3f93824048ee02baf0beac1` | PR #33 merge `a48eb7a8b1de94758e6c74945f710ff5084a4b8f` | MERGED / VERIFIED |
| P4 Physical screen realization | `13bccf1dafe1d2ebccc509bd0ab4a4f96e4fc0d7` | approved PR #35, restored by approved PR #43 merge `e6b62b4ffaf73103d57af24b8b60b5886643bb1c` | MERGED / VERIFIED |
| P5 Physical navigation/state binding | `0d2d38dcff7c5492145e7d106ff0c18c139d2c23` | GREEN/final `20a2a7324e76a2feeedfe5a864320159f36b82d4`; PR #45 merge `0676c5dd2f68f0e7a9322b003b1fa2da861d506e` | MERGED / VERIFIED |
| P6 Physical persistence/reporting validation | `02e1468e6b3103f23fecabee7b25862647f0bd62` | GREEN `0e002a4f336f87a14cf377e56d390e2da57746fc` | IMPLEMENTED / GREEN — MERGE APPROVAL PENDING |

## P6 verified invariants
- local committed synthetic session survives reload/restart validation;
- local canonical report is generated only from a committed canonical session;
- missing session fails closed;
- report retains source-session provenance and synthetic-test-only marking;
- real KVK connection, real-farm data, cloud upload and actuation surfaces remain absent.

## Canonical checkpoints
PR #27 `3eb278f7a480734045027393a53a76f6cdc03f03`; PR #29 `ec2cea9b144256baca29cd1ea2f03bf0dfcf6def`; PR #31 `047e5bba348eaea0b52103230ec589df6f857036`; PR #33 `a48eb7a8b1de94758e6c74945f710ff5084a4b8f`; P4 restoration PR #43 `e6b62b4ffaf73103d57af24b8b60b5886643bb1c`; P5 PR #45 `0676c5dd2f68f0e7a9322b003b1fa2da861d506e`.

## Authority boundary
`IA-HC-002` remains active only for isolated off-machine / non-actuating / synthetic-test physical-prototype work. Any live KVK connection, machine I/O/control path, real-farm data, network/cloud exposure or deployment remains separately blocked.
