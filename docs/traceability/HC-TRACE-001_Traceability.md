# HC-TRACE-001 — Traceability

## Status
`ACTIVE — BENCH MVP CLOSED / IA-HC-002 ACTIVE / P1-P6 MERGED / VERIFIED / P7 IMPLEMENTED / GREEN`

## Baselined upstream lineage

| ID | Decision / requirement | Downstream | Status |
|---|---|---|---|
| HC-FND-001 | Managed engineering program | Foundation → IMP | Baselined |
| HC-FND-002 | First target is circa-2013 KVK 801-1 | Foundation → REQ → IMP | Baselined |
| HC-FND-003 | Current names are engineering codenames only | README / CURRENT_STATE | Baselined |
| HC-SAF-001 | HoofCare cannot bypass or become part of KVK safety | IA / ARB / SA / REQ / IMP | Baselined |
| HC-SAF-002 | KVK integration boundary is observational/read-only | IA / ADR / SA / LEL / REQ / IMP | Baselined |
| HC-REQ-MVP-001 | Bench MVP requires end-to-end acceptance and negative tests | REQ → IMP → S1-S7 | Verified |
| HC-IMP-001 | Seven test-first bench slices; no live KVK integration | IMP-HC-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IA-001 | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | FULFILLED FOR AUTHORIZED BENCH SCOPE |
| HC-CLOSURE-001 | Bench MVP closure record | HC-BENCH-MVP-CLOSURE-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IA-002 | Physical prototype authority | IA-HC-002 | APPROVED / ACTIVE — PR #27 |

## Runtime / physical prototype lineage

| Slice | RED evidence | Verification | Status |
|---|---|---|---|
| S1 Domain/session core | `52b4fca3ca719b035d2cc7c5091447c607b6fd83` | PR #9 | MERGED / VERIFIED |
| S2 Persistence/recovery | `cbb35f593173aea2bb2fc1d77e1c6f267217eb01` | PR #10 | MERGED / VERIFIED |
| S3 HMI↔edge contract | `882afd05b9cbb94bc3265652becc245992998271` | PR #11 | MERGED / VERIFIED |
| S4 HMI workflow/dashboard | `36608bfcdf02ef4585ee177519d8966ca143dd4b` | PR #12 | MERGED / VERIFIED |
| S5 Local canonical PDF | `1581c6393319e6ab3905e3132f8ead55c6f4bfb9` | PR #13 | MERGED / VERIFIED |
| S6 Simulated adapters | `5e62980786207d6caad78dfb82f1921f11d1bfd5` | PR #14 | MERGED / VERIFIED |
| S7 Bench integration/acceptance | `5791b86e8bb469d0a4c090880adca2939665ff03` | PR #16 | MERGED / VERIFIED |
| P1 Physical prototype hardware profile | `87a9f6329e1ade0b1add79b4469ebb1b14393b40` | PR #29 | MERGED / VERIFIED |
| P2 HMI layout/touch mapping | `8e199b0f9ea398ab21d8ad6e6062bf7291ae6df2` | PR #31 | MERGED / VERIFIED |
| P3 Bench wiring BOM / isolated I/O | `65e62602e75d6f76c3f93824048ee02baf0beac1` | PR #33 | MERGED / VERIFIED |
| P4 Physical screen realization | `13bccf1dafe1d2ebccc509bd0ab4a4f96e4fc0d7` | GREEN/final `5575eabe0543a72e046a4d8bb7425e2ca1f1587d`; PR #35 merge `c5101eb15933bc76b76a86dd3e8ed4f78141875f` | MERGED / VERIFIED |
| P5 Physical navigation/state binding | `3f4db8258a85b6e2cc6349a5bb03d982066db732` | GREEN `de8dec19bc820b90bfebe4df669eb661e0af2add`; final `c1d01f66c17be44c07cf3bf3c26e935fd6e368f1`; PR #52 merge `4484ed4a00c7a756e0663c3cb03c329a6d7dd2c5` | MERGED / VERIFIED |
| P6 Physical persistence/reporting validation | `d78cd81c7bd35e3b2fe632febca104f074214900` | GREEN `bc3f9301c9e4743b93ec1d3d25970ea8127ba617`; final `4ab76ad972ccef8c74dabb75c9368d4ae3adcaa9`; PR #53 merge `b4a4417c6d719d8f9db0a14db48871f863cb4440` | MERGED / VERIFIED |
| P7 Physical prototype acceptance / closure-readiness | `db7b91525cc59a38207db8b8eb40320355ab8c12` | implementation attempt `28a97276bf3eb43c977711b7670e6600db87f4fb`; corrected GREEN `17bb4d430fdc96fea7a108b1e5b3152cc5be117a` | IMPLEMENTED / GREEN / NOT YET MERGED |

## P7 verified invariants
- acceptance reuses the existing P2-P6 physical-prototype surfaces rather than adding a parallel runtime path;
- 10.1-inch / 1024×600 screen and minimum touch-target invariants are checked;
- nominal local navigation reaches report summary through fail-closed state binding;
- local durable session round-trip/restart and canonical local PDF provenance are checked;
- synthetic/test-only remains true and real-farm data remains false;
- KVK connection remains false;
- machine-control-like actions remain rejected and no machine-control control IDs are present;
- field KVK verification and deployment readiness remain explicitly false.

## Canonical P6 checkpoint
PR #53 approved head `4ab76ad972ccef8c74dabb75c9368d4ae3adcaa9` → merge `b4a4417c6d719d8f9db0a14db48871f863cb4440`.

## Next state
After Project Owner-approved P7 merge and Repository Verification, the isolated physical prototype may move to `CLOSURE READY`. A separate closure record is still required; field/KVK integration remains blocked.

## Authority boundary
`IA-HC-002` is active only for its literal isolated off-machine / non-actuating / synthetic-test physical-prototype scope. Any live KVK connection, machine I/O/control path, real-farm data, network/cloud exposure or deployment remains separately blocked.
