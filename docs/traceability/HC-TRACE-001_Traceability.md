# HC-TRACE-001 — Traceability

## Status
`ACTIVE — BENCH MVP CLOSED / PHYSICAL PROTOTYPE CLOSED / IA-HC-003 ACTIVE / IA-HC-006 ACTIVE / R0 CLOSED / R1 CLOSED / R2-D/E REVERIFIED / R2 CLOSURE OPEN / HW-A1 CURRENT`

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
| HC-AUDIT-001 | Full software/documentation audit | 25 findings / R0-R2 | MERGED / R0 CLOSED / R1 CLOSED / R2-D/E REVERIFIED / R2 CLOSURE OPEN |
| HC-IMP-003 | Wave R0 remediation plan | IMP-HC-003 | FULFILLED FOR AUTHORIZED R0 SCOPE |
| HC-IA-004 | Wave R0 remediation authority | IA-HC-004 | FULFILLED FOR AUTHORIZED R0 SCOPE |
| HC-IMP-004 | Wave R1 data integrity/provenance plan | IMP-HC-004 | FULFILLED FOR AUTHORIZED R1 SCOPE |
| HC-IA-005 | Wave R1 data integrity/provenance authority | IA-HC-005 | FULFILLED FOR AUTHORIZED R1 SCOPE |
| HC-IMP-005 | Wave R2 UX/observability/engineering quality plan | IMP-HC-005 | APPROVED / RECOVERY ACTIVE |
| HC-IA-006 | Wave R2 recovery authority | IA-HC-006 | APPROVED / ACTIVE |
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
| R2-D/E | AUD-HC-024/025 | PR #77; corrected RED `277dcf1f4c289ad2917e5da9df109e61c4705642` → GREEN `d6c7c4a3ae62c876901f74faa52f0a40c08c4476` | RECONCILED / TDD REVERIFIED / OWNER MERGE APPROVAL REQUIRED |

Recovery record: `HC-IA-HC-006-RECOVERY-ACTIVATION-001`.
Nie ustanawia retroaktywnego authority. R2 closure pozostaje otwarte.
Post-merge reconciliation: `HC-R2-GOVERNANCE-POST-MERGE-RECON-001`.
R2-D/E revalidation record: `HC-R2-DE-TDD-REVERIFICATION-001`.

## DTools / GL100E truth
`GL100E-DTOOLS-SPEC-001` defines the exact 1024×600 realization specification.
A native DTools project/export remains `NATIVE_DTOOLS_ARTIFACT_REQUIRED / NOT YET EVIDENCED` until generated with the real Kinco toolchain and evidenced before HW-A3 PASS.

## Edge/application host truth
Architecture still requires HMI-independent canonical persistence/reporting. The R2 local synthetic runtime package establishes a reproducible software entrypoint only; concrete physical edge/application host remains `EDGE_HOST_REQUIRED / NOT YET SELECTED`.

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
