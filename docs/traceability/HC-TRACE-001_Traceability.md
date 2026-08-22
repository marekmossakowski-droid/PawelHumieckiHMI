# HC-TRACE-001 — Traceability

## Status
`ACTIVE — BENCH MVP CLOSED / PHYSICAL PROTOTYPE CLOSED / IA-HC-003 ACTIVE / R0 CLOSURE READY / HW-A1 CURRENT`

Compatibility marker for canonical governance CI: `HW-A1 CURRENT`.
Canonical IA-HC-003 activation merge compatibility marker: `52d65b18f966f553501a7829855f23b7390762a6`.

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
| HC-AUDIT-001 | Full software/documentation audit | 25 findings / R0-R2 | MERGED / R0 REMEDIATED / R1-R2 OPEN |
| HC-IMP-003 | Wave R0 remediation plan | IMP-HC-003 | FULFILLED FOR AUTHORIZED R0 SCOPE / CLOSURE PENDING |
| HC-IA-004 | Wave R0 remediation authority | IA-HC-004 | ACTIVE UNTIL R0 CLOSURE MERGE |
| HC-HW-A1 | Goods-in verification | IMP-HC-002 / HW-A1 | WAITING FOR PHYSICAL HARDWARE |

## Wave R0 lineage
| Slice | Audit findings | Evidence | Status |
|---|---|---|---|
| R0-A Exact hardware profile | AUD-HC-006 | RED `d054fd8cf722bde2b8f08e95dd05d83de35bbf93` → GREEN `d75313e42b5ebad8b2f4edfda2f106077bd85aad` → final `f44c9e1dc6891ce1d807a1a338fc54a4a4e07784`; PR #61 | MERGED / VERIFIED |
| R0-B Valid local PDF | AUD-HC-003 | RED `510250cd3c5a782653cdef7f22111822a89bdf01` → GREEN `e6a1c3e6ba4541bd5e4cbe52007d25fee8ae5ab8` → final `388fd4a2b0ae498276eabe39ce2c3f7d08b349d2`; PR #62 | MERGED / VERIFIED |
| R0-C Durable completion / evidence acceptance | AUD-HC-004/005 | RED `3855899b667d59b89ee9a7f916fba841877094b1` → GREEN `3dc7117ff3b75b30517cc6291f456fe82e2d3561` → final `7803d530d94ae8a5dd35bba075c151e0fde1c25f`; PR #63 | MERGED / VERIFIED |
| R0-D GL100E spec / docs / requirement trace | AUD-HC-001/002/015/016/017 | final `48226bcdcad20b33533ed8ab3ee2d9b031ccbd63`; PR #64 → merge `8bab4dfe0c4e685f8030419bf8cddada61e6e03f` | MERGED / VERIFIED |

## R0 closure truth
`HC-R0-CLOSURE-001` is the closure gate for the authorized software/documentation scope only.
After controlled merge + Repository Verification it may establish:
- `WAVE R0 SOFTWARE/DOCUMENTATION REMEDIATION = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`;
- `IMP-HC-003 = FULFILLED FOR AUTHORIZED R0 SCOPE`;
- `IA-HC-004 = FULFILLED FOR AUTHORIZED R0 SCOPE`.

## DTools / GL100E truth
`GL100E-DTOOLS-SPEC-001` defines the exact 1024×600 realization specification.
A native DTools project/export remains `NATIVE_DTOOLS_ARTIFACT_REQUIRED / NOT YET EVIDENCED` until generated with the real Kinco toolchain and evidenced before HW-A3 PASS.

## Edge/application host truth
Architecture still requires HMI-independent canonical persistence/reporting. Concrete physical edge/application host remains `EDGE_HOST_REQUIRED / NOT YET SELECTED`.

## Physical execution state
Selected hardware boundary:
- Kinco GL100E 10.1 inch / 1024×600;
- Kinco KS123-14DR / 8 DI + 6 relay DO;
- existing isolated 24 VDC subject to physical verification;
- local RS485/Modbus only GL100E↔KS123-14DR;
- RFID deferred.

`HW-A1 = WAITING FOR PHYSICAL HARDWARE`. No power-up, upload or real panel acceptance is claimed.

## Authority boundary
No authority exists for live KVK integration. No real KVK I/O, machine CAN/RS-485/Modbus/serial, commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, real-farm data, network/cloud exposure, external report delivery, deployment, signing, release or public distribution is authorized.
