# HC-TRACE-001 — Traceability

## Status
`ACTIVE — BENCH MVP CLOSED / IA-HC-002 ACTIVE / P1 MERGED / VERIFIED / P2 NEXT`

## Baselined upstream lineage

| ID | Decision / requirement | Downstream | Status |
|---|---|---|---|
| HC-FND-001 | Managed engineering program | Foundation → IMP | Baselined |
| HC-FND-002 | First target is circa-2013 KVK 801-1 | Foundation → REQ → IMP | Baselined |
| HC-FND-003 | Current names are engineering codenames only | README / CURRENT_STATE | Baselined |
| HC-SAF-001 | HoofCare cannot bypass or become part of KVK safety | IA / ARB / SA / REQ / IMP | Baselined |
| HC-SAF-002 | KVK integration boundary is observational/read-only | IA / ADR / SA / LEL / REQ / IMP | Baselined |
| HC-REQ-MVP-001 | Bench MVP requires end-to-end acceptance and negative tests | REQ → IMP → S1-S7 | Verified |
| HC-REQ-MVP-002 | Ambiguous/conflicting identity cannot commit to animal history | REQ → S1/S3/S7 | Verified |
| HC-REQ-MVP-003 | Persisted in-progress session recovery is required | REQ → S2 | Verified |
| HC-REQ-MVP-004 | Duplicate events must not duplicate logical records | REQ → S1/S3 | Verified |
| HC-REQ-MVP-005 | Reference/example media must remain visibly distinguished | REQ → S5/S7 | Verified |
| HC-REQ-MVP-006 | Bench public interfaces expose no KVK write/command API | REQ → S3/S4/S6/S7 | Verified |
| HC-IMP-001 | Seven test-first bench slices; no live KVK integration | IMP-HC-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IA-001 | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | FULFILLED FOR AUTHORIZED BENCH SCOPE |
| HC-CLOSURE-001 | Bench MVP closure record | HC-BENCH-MVP-CLOSURE-001 | CLOSED / IMPLEMENTED / VERIFIED / RECONCILED |
| HC-IA-002 | Physical prototype authority | IA-HC-002 | APPROVED / ACTIVE — PR #27 |
| HC-IA-002-ACT-001 | Explicit Project Owner activation gate | HC-IA-HC-002-ACTIVATION-001 | APPROVED / MERGED / REPOSITORY VERIFIED |

## Runtime slice lineage

| Slice | RED evidence | Verification | Status |
|---|---|---|---|
| S1 Domain/session core | `52b4fca3ca719b035d2cc7c5091447c607b6fd83` | PR #9 `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2` | MERGED / VERIFIED |
| S2 Persistence/recovery | `cbb35f593173aea2bb2fc1d77e1c6f267217eb01` | PR #10 `c5f60dbf11b04b680c6f51f2e610d33906b08637` | MERGED / VERIFIED |
| S3 HMI↔edge contract | `882afd05b9cbb94bc3265652becc245992998271` | PR #11 `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a` | MERGED / VERIFIED |
| S4 HMI workflow/dashboard | `36608bfcdf02ef4585ee177519d8966ca143dd4b` | PR #12 `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34` | MERGED / VERIFIED |
| S5 Local canonical PDF | `1581c6393319e6ab3905e3132f8ead55c6f4bfb9` | PR #13 `30acc2d9a0833844e7279c68d9884cf9dd124cea` | MERGED / VERIFIED |
| S6 Simulated adapters | `5e62980786207d6caad78dfb82f1921f11d1bfd5` | PR #14 `56da4eaf1316c930ca6095cd068e90bd66e2f624` | MERGED / VERIFIED |
| S7 Bench integration/acceptance | `5791b86e8bb469d0a4c090880adca2939665ff03` | PR #16 `0827d0d4b51a0a63c773a1f8ce178d7954dc25a5` | MERGED / VERIFIED |
| P1 Physical prototype hardware profile | `87a9f6329e1ade0b1add79b4469ebb1b14393b40` | GREEN `601ae9fa2fab0bd9a3f72481bbc9ef3f77e7f452`; final `39678f0ca691001d56e60a91bd30b8235ff3f30e`; PR #29 merge `ec2cea9b144256baca29cd1ea2f03bf0dfcf6def` | MERGED / VERIFIED |

## Bench MVP verified invariants
- synthetic/test-only local execution;
- fail-closed identity ambiguity;
- durable local persistence and restart recovery;
- ordered operator HMI workflow and approved dashboard banner;
- canonical local reporting with provenance and explicit reference-media labeling;
- deterministic simulated RFID/KVK observations;
- end-to-end acceptance and negative verification;
- no KVK command/write/configuration/actuation surface;
- no live KVK, RFID, CAN, RS-485, Modbus, serial, hydraulics, PLC or safety integration.

## P1 verified invariants
- physical prototype mode remains `ISOLATED_SYNTHETIC`;
- 10.1-inch-class profile with nominal 24 VDC bench supply;
- DI/DO counts are descriptive only;
- KVK connection and real-farm data are explicitly denied;
- no live machine-bus or actuation enable surface is exposed.

## Canonical checkpoints
PR #1 `de68522e4851f645d65dee7dda08ef8fed6af955`; PR #2 `b0286b73b90c95f05b1d99ef58ac9a9fae197880`; PR #3 `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`; PR #4 `c2493ef39a1b45b934cd2dc001279db110a17fc0`; PR #5 `5a0761dec9dbbca538be787839d93017f5c501df`; PR #6 `a7d031317cf25934218cd09a4916449f2bf5b634`; PR #7 `e34e2a2ae3f709d83c24d528f8930b1b72060961`; PR #8 `0d58eb2921df298114c304295a061547598ae541`; PR #9 `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2`; PR #10 `c5f60dbf11b04b680c6f51f2e610d33906b08637`; PR #11 `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a`; PR #12 `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34`; PR #13 `30acc2d9a0833844e7279c68d9884cf9dd124cea`; PR #14 `56da4eaf1316c930ca6095cd068e90bd66e2f624`; PR #16 `0827d0d4b51a0a63c773a1f8ce178d7954dc25a5`; PR #17 `36ffda3b2363597b8a8aae3746e9d555450c625c`; PR #21 `ce58dd3e5ab9346442456736b646eacbc4309a8a`; PR #27 `3eb278f7a480734045027393a53a76f6cdc03f03`; PR #28 `ce72bc01f6ccbe671a5293bde8c0f19ef3ac3ee8`; PR #29 `ec2cea9b144256baca29cd1ea2f03bf0dfcf6def`.

## Next slice
`HC-P2-001 — Physical HMI layout and touch mapping` under the existing isolated synthetic/test-only `IA-HC-002` boundary.

## Authority boundary
`IA-HC-002` is active only for its literal isolated off-machine / non-actuating / synthetic-test physical-prototype scope. Any live KVK connection, machine I/O/control path, real-farm data, network/cloud exposure or deployment remains separately blocked.
