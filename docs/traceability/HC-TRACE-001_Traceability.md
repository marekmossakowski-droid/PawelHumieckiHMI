# HC-TRACE-001 — Traceability

## Status
`ACTIVE — BENCH MVP CLOSED / PHYSICAL PROTOTYPE CLOSED / IA-HC-002 FULFILLED / BENCH HARDWARE ASSEMBLY READINESS NEXT`

## Baselined upstream lineage

| ID | Decision / requirement | Downstream | Status |
|---|---|---|---|
| HC-FND-001 | Managed engineering program | Foundation → IMP | BASELINED |
| HC-FND-002 | First target is circa-2013 KVK 801-1 | Foundation → REQ → IMP | BASELINED |
| HC-FND-003 | Current names are engineering codenames only | README / CURRENT_STATE | BASELINED |
| HC-SAF-001 | HoofCare cannot bypass or become part of KVK safety | IA / ARB / SA / REQ / IMP | BASELINED |
| HC-SAF-002 | KVK integration boundary is observational/read-only | IA / ADR / SA / LEL / REQ / IMP | BASELINED |
| HC-REQ-MVP-001 | Bench MVP requires end-to-end acceptance and negative tests | REQ → IMP → S1-S7 | VERIFIED |
| HC-IMP-001 | Seven test-first bench slices; no live KVK integration | IMP-HC-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IA-001 | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | FULFILLED FOR AUTHORIZED BENCH SCOPE |
| HC-CLOSURE-001 | Bench MVP closure record | HC-BENCH-MVP-CLOSURE-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IA-002 | Physical prototype authority | IA-HC-002 | FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE |
| HC-CLOSURE-002 | Physical prototype closure record | HC-PHYSICAL-PROTOTYPE-CLOSURE-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IMP-002 | Isolated bench hardware assembly plan | IMP-HC-002 | PROPOSED / NOT ACTIVE |
| HC-IA-003 | Isolated bench hardware assembly authority | IA-HC-003 | PROPOSED / NOT ACTIVE |

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
| P4 Physical screen realization | `13bccf1dafe1d2ebccc509bd0ab4a4f96e4fc0d7` | GREEN/final `5575eabe0543a72e046a4d8bb7425e2ca1f1587d`; PR #35 | MERGED / VERIFIED |
| P5 Physical navigation/state binding | `3f4db8258a85b6e2cc6349a5bb03d982066db732` | GREEN `de8dec19bc820b90bfebe4df669eb661e0af2add`; final `c1d01f66c17be44c07cf3bf3c26e935fd6e368f1`; PR #52 | MERGED / VERIFIED |
| P6 Physical persistence/reporting validation | `d78cd81c7bd35e3b2fe632febca104f074214900` | GREEN `bc3f9301c9e4743b93ec1d3d25970ea8127ba617`; final `4ab76ad972ccef8c74dabb75c9368d4ae3adcaa9`; PR #53 | MERGED / VERIFIED |
| P7 Physical prototype acceptance / closure-readiness | `db7b91525cc59a38207db8b8eb40320355ab8c12` | corrected GREEN `17bb4d430fdc96fea7a108b1e5b3152cc5be117a`; final `c6083495296a59835a427f035a11ecd859f5be6f`; PR #54 | MERGED / VERIFIED |

## Canonical physical-prototype closure
- PR #54 approved head `c6083495296a59835a427f035a11ecd859f5be6f` → merge `7e3f4e573bead9664e39422a97ab6cc3ddbb2c41`.
- PR #55 approved head `f7faea3620560ac409e23c0399a7f7f1c26a17dc` → merge `ad8b164ce3517064a1de92c986b27a8bfd024b8b`.
- `PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-002 = FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE`.

## Next bounded workstream — proposed only
`IMP-HC-002` and `IA-HC-003` prepare isolated bench hardware assembly using the selected procurement target:
- HMI: Kinco GL100E, 10.1-inch, 1024×600, DC 10–28 V, RS232/RS485/RS422 and Ethernet;
- I/O: Kinco KS123-14DR, 24 VDC, 8 DI + 6 relay DO, usable as a Modbus slave station;
- existing 24 VDC source;
- RFID explicitly deferred;
- RS485/Modbus tests only between HMI and dedicated bench I/O/test equipment.

These documents do not activate hardware assembly authority by themselves.

## Authority boundary
No active authority exists for live KVK integration. No real KVK I/O, machine CAN/RS-485/Modbus/serial, commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, real-farm data, network/cloud exposure, external report delivery, deployment, signing, release or public distribution is authorized.
