# HC-TRACE-001 — Traceability

## Status
`ACTIVE — BENCH MVP CLOSED / PHYSICAL PROTOTYPE CLOSED / IA-HC-003 ACTIVE / IA-HC-006 ACTIVE / IA-HC-007 ACTIVE / R0 CLOSED / R1 CLOSED / R2 GOVERNANCE RECOVERY CLOSED / HW-A1 CURRENT`

Compatibility marker for canonical governance CI: `HW-A1 CURRENT`.
Canonical IA-HC-003 activation merge compatibility marker: `52d65b18f966f553501a7829855f23b7390762a6`.
Compatibility marker retained: `ACTIVE — BENCH MVP CLOSED / PHYSICAL PROTOTYPE CLOSED / IA-HC-003 ACTIVE / R0 CLOSURE READY / HW-A1 CURRENT`.
Compatibility marker retained: `ACTIVE — BENCH MVP CLOSED / PHYSICAL PROTOTYPE CLOSED / IA-HC-003 ACTIVE / R0 CLOSED / R1 CLOSURE READY / HW-A1 CURRENT`.

## Baselined upstream lineage
| ID | Decision / requirement | Downstream | Status |
|---|---|---|---|
| HC-FND-001 | Managed engineering program | Foundation → IMP | BASELINED |
| HC-FND-002 | First target is circa-2013 KVK 801-1 | Foundation → REQ → IMP | BASELINED |
| HC-FND-003 | Current names are engineering codenames only | README / CURRENT_STATE | BASELINED |
| HC-SAF-001 | HoofCare cannot bypass or become part of KVK safety | IA / ARB / SA / REQ / IMP | BASELINED |
| HC-SAF-002 | KVK integration boundary is observational/read-only | IA / ADR / SA / LEL / REQ / IMP | BASELINED |
| HC-IMP-001 | Bench MVP implementation | IMP-HC-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IA-001 | Synthetic/test-only bench implementation authority | IA-HC-001 | FULFILLED |
| HC-IA-002 | Physical prototype authority | IA-HC-002 | FULFILLED |
| HC-IMP-002 | Isolated bench hardware assembly plan | IMP-HC-002 | APPROVED / ACTIVE |
| HC-IA-003 | Isolated bench hardware assembly authority | IA-HC-003 | APPROVED / ACTIVE |
| HC-AUDIT-001 | Full software/documentation audit | 25 findings / R0-R2 | MERGED / R0 CLOSED / R1 CLOSED / R2-D/E REVERIFICATION REQUIRED |
| HC-IMP-003 | Wave R0 remediation plan | IMP-HC-003 | FULFILLED FOR AUTHORIZED R0 SCOPE |
| HC-IA-004 | Wave R0 remediation authority | IA-HC-004 | FULFILLED FOR AUTHORIZED R0 SCOPE |
| HC-IMP-004 | Wave R1 data integrity/provenance plan | IMP-HC-004 | FULFILLED FOR AUTHORIZED R1 SCOPE |
| HC-IA-005 | Wave R1 data integrity/provenance authority | IA-HC-005 | FULFILLED FOR AUTHORIZED R1 SCOPE |
| HC-IMP-005 | Wave R2 UX/observability/engineering quality plan | IMP-HC-005 | APPROVED / RECOVERY ACTIVE |
| HC-IA-006 | Wave R2 recovery authority | IA-HC-006 | APPROVED / ACTIVE |
| HC-UX-001 | Role menu and job settlement design | UX-HC-001 / ADR-HC-008 / REQ-HC-002 | APPROVED / BASELINED V0.1 SLICE |
| HC-ADR-009 | Client generations and adaptive presentation | ADR-HC-009 | APPROVED DESIGN CONTENT / NO IMPLEMENTATION AUTHORITY |
| HC-IMP-UX-001 | Role menu and job settlement implementation plan | IMP-UX-HC-001 | APPROVED / ACTIVE |
| HC-IA-007 | Job settlement authority | IA-HC-007 | APPROVED / ACTIVE |
| HC-REQ-002-A1 | Zootechnician pricing access and freeze | REQ-HC-002-A1 | APPROVED / BASELINED / MERGED |
| HC-IA-007-A1 | Zootechnician pricing authority amendment | IA-HC-007-A1 | APPROVED / ACTIVE |
| HC-CLOSE-002-A1 | Bounded pricing-access closure | HC-REQ-HC-002-A1-CLOSURE-001 | CLOSURE READY / OWNER MERGE REQUIRED |
| HC-PLAN-STAT-001 | Job statistics and final settlement plan | 2026-08-23-job-statistics-final-settlement | PROPOSED / NOT ACTIVE |
| HC-REQ-002-S1 | Job statistics and final settlement requirements | REQ-HC-002-S1 | APPROVED / BASELINED |
| HC-IA-007-S1 | Job statistics and final settlement authority | IA-HC-007-S1 | APPROVED / ACTIVE PROSPECTIVELY |
| HC-HW-A1 | Goods-in verification | IMP-HC-002 / HW-A1 | WAITING FOR PHYSICAL HARDWARE |

## Wave R0 lineage
| Slice | Audit findings | Evidence | Status |
|---|---|---|---|
| R0-A | AUD-HC-006 | PR #61 | MERGED / VERIFIED |
| R0-B | AUD-HC-003 | PR #62 | MERGED / VERIFIED |
| R0-C | AUD-HC-004/005 | PR #63 | MERGED / VERIFIED |
| R0-D | AUD-HC-001/002/015/016/017 | PR #64 | MERGED / VERIFIED |

`WAVE R0 SOFTWARE/DOCUMENTATION REMEDIATION = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.

## Wave R1 lineage
| Slice | Audit findings | Evidence | Status |
|---|---|---|---|
| R1-A Persistence path safety | AUD-HC-007 | RED `08cf19d0aa1b5cedcc5bf6d52717116fc64c3df2` → GREEN/final `a594a32f30b3efb6506ce9a5b2d56aff9beac702`; PR #67 | MERGED / VERIFIED |
| R1-B/C Durability, integrity, audit provenance | AUD-HC-008/009 | RED `8a50d078a220a43f12fcc21939c9f3608594d0c3` → corrected GREEN/final `7fbe305b41445a8fbb594f1f08c684e4f1ec8f80`; PR #68 | MERGED / VERIFIED |
| R1-D/E Domain invariants + idempotency | AUD-HC-010/011 | RED `291c07c3d73a70f8ab88b606e65f8bd7a66bb7db` → GREEN/final `49abed2aa178131571739cb2039e1c0cced9a084`; PR #69 | MERGED / VERIFIED |
| R1-F/G/H Canonical clinical/media/report model | AUD-HC-012/013/014 | RED `aa32ab881cc01fba4cd9a081e3f5de2ca9199b7a` → GREEN/final `75222c31053f12ee81265beaf2376632a393f4ee`; PR #70 | MERGED / VERIFIED |

`WAVE R1 DATA INTEGRITY AND CLINICAL PROVENANCE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
`AUD-HC-007`–`AUD-HC-014 = CLOSED / VERIFIED`.
R1 closure gate: PR #71 merge `cbacafb9b09fa4530649d27b1b376659217939bb`.

## Wave R2 governance recovery lineage
| Slice | Audit findings | Evidence | Recovery status |
|---|---|---|---|
| R2-A | AUD-HC-018/019 | PR #74 / merge `9330a129ec37ac3f9d09b03e424981b9f2089075` | CONTENT REVERIFIED / GOVERNANCE GAP RECORDED |
| R2-B | AUD-HC-020/021 | PR #75 / merge `0a7795c41ac2b2416906869180289cdab2f53464` | CONTENT REVERIFIED / GOVERNANCE GAP RECORDED |
| R2-C | AUD-HC-022/023 | PR #76 / merge `61de55a84319a2ba29a21dda5387a603381873f8` | CONTENT REVERIFIED / SEMANTIC-GATE REPAIR IN RECOVERY |
| R2-D/E | AUD-HC-024/025 | PR #77 | OPEN / REBASE AND TDD REVERIFICATION REQUIRED |

Recovery record: `HC-IA-HC-006-RECOVERY-ACTIVATION-001`.
Nie ustanawia retroaktywnego authority. R2 closure pozostaje otwarte.
Post-merge reconciliation: `HC-R2-GOVERNANCE-POST-MERGE-RECON-001`.

## UX-HC-001 authority activation

- approved exact head PR #80: `8901922380a3ec342747088e5acccdcd4ca5b44d`;
- controlled merge: `3a32e3b5b7d1f5b2693836c044ef73caa63276d3`;
- verified tree: `fa8d5e3bdf1d71087b12472d8a649f6685ac6632`;
- activation record: `HC-IA-HC-007-ACTIVATION-001`;
- post-merge reconciliation: `HC-UX-HC-001-POST-MERGE-RECON-001`;
- `IA-HC-007 = APPROVED / ACTIVE` prospectively for local synthetic/test-only `REQ-HC-002` v0.1 implementation.

No runtime implementation is claimed by the activation package. PR #77 and R2 closure remain separate.

## ADR-HC-009 reconciliation proposal

- ADR-HC-009 publication merge: `0e13e1d762a332b126358cd2f490d68793249755`;
- canonical ADR blob: `fe02c1d75f58d1e48ddb2b83e321e1e1f93b3c41`;
- `REQ-HC-002-A1` defines the proposed pre-first-completed-cow correction window;
- `IA-HC-007-A1` was `PROPOSED / NOT ACTIVE` until exact-head approval,
  controlled merge, Repository Verification and the canonical activation record;
  those gates are now satisfied.

The approved authority does not claim completed runtime implementation and does
not authorize Generation 2, closed-settlement corrections, real data, device
access or deployment.

Content decision: Project Owner approved `REQ-HC-002-A1` and the written
design on PR #86 exact head `c651534ca6fafd037d4887b2b8face2aea158753` and
authorized preparation of the TDD plan only. Merge and `IA-HC-007-A1`
activation were subsequently completed by controlled merge and Repository
Verification recorded in `HC-IA-HC-007-A1-ACTIVATION-001`. Runtime is now
implemented for the bounded local synthetic/test-only A1 slice, with final
integration evidence pending controlled merge and Repository Verification.

## REQ-HC-002-A1 implementation evidence

- A1-1: immutable versioned pricing snapshot, audit, retry conflict and freeze;
- A1-2: local schema-v2 atomic persistence and fail-closed audit validation;
- A1-3: durable application correction use case;
- A1-4: semantic price visibility/editability and separate GL100E profile;
- A1-5: `test_open_correct_restart_complete_freeze_and_close` plus requirement-level mapping.

This evidence does not claim a finished GUI/DTools project, physical acceptance,
Generation 2, real data, device access, deployment or closed-settlement correction.

PR #92 was controlled-merged as `8e2b2ed97f73d4f0c7015b189f7f9889e39df3ab`;
Repository Verification confirmed exact tree
`5cc3f0e8c8fc3ff0181258f2610b04b207784e87` and 139/139 tests. The bounded
A1 workstream is closure-ready, not yet canonically closed. Statistics and final
settlement planning is documented separately as `PROPOSED / NOT ACTIVE`.

Preparation decision `HC-REQ-HC-002-S1-PREPARATION-DECISION-001` permitted only
the Draft authority package. Project Owner approval and verified PR #94 merge
are bound by `HC-IA-HC-007-S1-ACTIVATION-001`; runtime remains not started.

## DTools / GL100E truth
`GL100E-DTOOLS-SPEC-001` defines the exact 1024×600 realization specification.
A native DTools project/export remains `NATIVE_DTOOLS_ARTIFACT_REQUIRED / NOT YET EVIDENCED` until generated with the real Kinco toolchain and evidenced before HW-A3 PASS.

## Edge/application host truth
Architecture still requires HMI-independent canonical persistence/reporting. Concrete physical edge/application host remains `EDGE_HOST_REQUIRED / NOT YET SELECTED`.

## Physical execution state
Selected/order-confirmed hardware boundary:
- Kinco GL100E 10.1 inch / 1024×600;
- Kinco KS123-14DR / 8 DI + 6 relay DO;
- existing isolated 24 VDC subject to physical verification;
- local RS485/Modbus only GL100E↔KS123-14DR;
- RFID deferred.

`HW-A1 = WAITING FOR PHYSICAL HARDWARE`. Purchase confirmation does not equal goods-in verification. No power-up, upload or real panel acceptance is claimed.

## Authority boundary
No authority exists for live KVK integration. No real KVK I/O, machine CAN/RS-485/Modbus/serial, commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, real-farm data, network/cloud exposure, external report delivery, deployment, signing, release or public distribution is authorized.
