# HC-TRACE-001 — Traceability

## Status
`ACTIVE — F90 / PHYSICAL PROTOTYPE`

## Baselined upstream lineage

| ID | Decision / requirement | Downstream | Status |
|---|---|---|---|
| HC-FND-001 | Managed engineering program | Foundation → IMP | Baselined |
| HC-FND-002 | First target is circa-2013 KVK 801-1 | Foundation → REQ → IMP | Baselined |
| HC-FND-003 | Current names are engineering codenames only | README / CURRENT_STATE | Baselined |
| HC-SAF-001 | HoofCare cannot bypass or become part of KVK safety | IA / ARB / SA / REQ / IMP | Baselined |
| HC-SAF-002 | KVK integration boundary is observational/read-only | IA / ADR / SA / LEL / REQ / IMP | Baselined |
| HC-REQ-MVP-001 | Bench MVP requires end-to-end acceptance and negative tests | REQ → IMP → S1-S7 | Verified |
| HC-IMP-001 | Seven test-first bench slices; no live KVK integration | IMP-HC-001 | CLOSED / VERIFIED |
| HC-IA-001 | Runtime authority limited to local synthetic/test-only bench implementation | IA-HC-001 | FULFILLED |
| HC-CLOSURE-001 | Bench MVP closure record | HC-BENCH-MVP-CLOSURE-001 | MERGED / VERIFIED PR #17 |
| HC-IA-002 | Physical prototype authority | IA-HC-002 | ACTIVE — PR #17 |

## Runtime / physical prototype lineage

| Slice | RED evidence | Green / merged evidence | Status |
|---|---|---|---|
| S1 Domain/session core | `52b4fca3ca719b035d2cc7c5091447c607b6fd83` | PR #9 `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2` | MERGED / VERIFIED |
| S2 Persistence/recovery | `cbb35f593173aea2bb2fc1d77e1c6f267217eb01` | PR #10 `c5f60dbf11b04b680c6f51f2e610d33906b08637` | MERGED / VERIFIED |
| S3 HMI↔edge contract | `882afd05b9cbb94bc3265652becc245992998271` | PR #11 `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a` | MERGED / VERIFIED |
| S4 HMI workflow/dashboard | `36608bfcdf02ef4585ee177519d8966ca143dd4b` | PR #12 `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34` | MERGED / VERIFIED |
| S5 Local canonical PDF | `1581c6393319e6ab3905e3132f8ead55c6f4bfb9` | PR #13 `30acc2d9a0833844e7279c68d9884cf9dd124cea` | MERGED / VERIFIED |
| S6 Simulated adapters | `5e62980786207d6caad78dfb82f1921f11d1bfd5` | PR #14 `56da4eaf1316c930ca6095cd068e90bd66e2f624` | MERGED / VERIFIED |
| S7 Bench integration/acceptance | corrected RED `5791b86e8bb469d0a4c090880adca2939665ff03` | PR #16 `0827d0d4b51a0a63c773a1f8ce178d7954dc25a5` | MERGED / VERIFIED |
| P1 Physical hardware profile | `c274137e90f0da24898a1863de86b8b4fa4002cd` | GREEN `05dbd79b25f23ed3b5e578700add6c9dcf139886`; PR #18 `3425b2be7e581fcb079c8b3688b48533b780a06b` | MERGED / VERIFIED |
| P2 HMI layout/touch mapping | `8c243af4b136ac7eb5abe30d4dd326f977302a92` | GREEN `153a449903ffbb1a66cb237a4454437362f6fe80`; PR #19 `0404c45bf7adbdc9e6063501ce5adb7651dd5019` | MERGED / VERIFIED |
| P3 Bench wiring BOM / isolated I/O profile | `a7f0e9168d6987b9ef0fa642a0d7ec27fddb8375` | GREEN `87e5d5e5da8f491d930375d7bbeed7966e157ddb`; PR #20 `e26af73899a363543cf889a80a69f076cb370836` | MERGED / VERIFIED |
| P4 Physical screen realization/widget mapping | `8c4ca015c2bdaf0983dbb3d9a388b2dd1f48b301` | GREEN `2ef612affa98add3b48f9f43b3df0332916e7c17` | IMPLEMENTED / GREEN |

## P4 verified invariants
- all approved P2 screens have realized widget sets;
- dashboard banner and counters remain present;
- interactive controls preserve minimum 48×48 px touch targets;
- ambiguous/conflicting/unknown identity disables identity confirmation fail-closed;
- physical screen realization is isolated synthetic/test-only;
- no KVK command/write/configuration/actuation or machine-control widget/API exists.

## Canonical checkpoints
PR #1 `de68522e4851f645d65dee7dda08ef8fed6af955`; PR #2 `b0286b73b90c95f05b1d99ef58ac9a9fae197880`; PR #3 `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`; PR #4 `c2493ef39a1b45b934cd2dc001279db110a17fc0`; PR #5 `5a0761dec9dbbca538be787839d93017f5c501df`; PR #6 `a7d031317cf25934218cd09a4916449f2bf5b634`; PR #7 `e34e2a2ae3f709d83c24d528f8930b1b72060961`; PR #8 `0d58eb2921df298114c304295a061547598ae541`; PR #9 `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2`; PR #10 `c5f60dbf11b04b680c6f51f2e610d33906b08637`; PR #11 `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a`; PR #12 `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34`; PR #13 `30acc2d9a0833844e7279c68d9884cf9dd124cea`; PR #14 `56da4eaf1316c930ca6095cd068e90bd66e2f624`; PR #16 `0827d0d4b51a0a63c773a1f8ce178d7954dc25a5`; PR #17 `36ffda3b2363597b8a8aae3746e9d555450c625c`; PR #18 `3425b2be7e581fcb079c8b3688b48533b780a06b`; PR #19 `0404c45bf7adbdc9e6063501ce5adb7651dd5019`; PR #20 `e26af73899a363543cf889a80a69f076cb370836`.

## Closure rule
No physical-prototype row becomes Closed without fresh verification evidence and controlled merge on the exact Project Owner-approved head. Live KVK integration remains outside `IA-HC-002`.
