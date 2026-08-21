# HC-TRACE-001 — Traceability

## Status
`ACTIVE — BENCH MVP CLOSED / IA-HC-002 ACTIVE / P1-P3 MERGED / VERIFIED / P4 IMPLEMENTED / MERGE APPROVAL PENDING`

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
| S1 Domain/session core | `52b4fca3ca719b035d2cc7c5091447c607b6fd83` | PR #9 `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2` | MERGED / VERIFIED |
| S2 Persistence/recovery | `cbb35f593173aea2bb2fc1d77e1c6f267217eb01` | PR #10 `c5f60dbf11b04b680c6f51f2e610d33906b08637` | MERGED / VERIFIED |
| S3 HMI↔edge contract | `882afd05b9cbb94bc3265652becc245992998271` | PR #11 `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a` | MERGED / VERIFIED |
| S4 HMI workflow/dashboard | `36608bfcdf02ef4585ee177519d8966ca143dd4b` | PR #12 `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34` | MERGED / VERIFIED |
| S5 Local canonical PDF | `1581c6393319e6ab3905e3132f8ead55c6f4bfb9` | PR #13 `30acc2d9a0833844e7279c68d9884cf9dd124cea` | MERGED / VERIFIED |
| S6 Simulated adapters | `5e62980786207d6caad78dfb82f1921f11d1bfd5` | PR #14 `56da4eaf1316c930ca6095cd068e90bd66e2f624` | MERGED / VERIFIED |
| S7 Bench integration/acceptance | `5791b86e8bb469d0a4c090880adca2939665ff03` | PR #16 `0827d0d4b51a0a63c773a1f8ce178d7954dc25a5` | MERGED / VERIFIED |
| P1 Physical prototype hardware profile | `87a9f6329e1ade0b1add79b4469ebb1b14393b40` | GREEN `601ae9fa2fab0bd9a3f72481bbc9ef3f77e7f452`; final `39678f0ca691001d56e60a91bd30b8235ff3f30e`; PR #29 merge `ec2cea9b144256baca29cd1ea2f03bf0dfcf6def` | MERGED / VERIFIED |
| P2 HMI layout/touch mapping | `8e199b0f9ea398ab21d8ad6e6062bf7291ae6df2` | GREEN `d2fa2a91b957362b0367d9f0b30f267ddcd1b784`; final `5ea083ad0ac9ed0b2c965af167a6db821429c9fb`; PR #31 merge `047e5bba348eaea0b52103230ec589df6f857036` | MERGED / VERIFIED |
| P3 Bench wiring BOM / isolated I/O | `65e62602e75d6f76c3f93824048ee02baf0beac1` | GREEN `506cdb249836401786e4899308f0bc5749382700`; final `2de9b10aab518ac8e92cfbaf84dbc64c728d9300`; PR #33 merge `a48eb7a8b1de94758e6c74945f710ff5084a4b8f` | MERGED / VERIFIED |
| P4 Physical screen realization | `fc475d55cfcc457ef0e8f885d5484589f4b9e0b6` | GREEN `13e0ca8bba90f71287230a6234f5e00cfdc5c36e`; final head pending reconciliation CI | IMPLEMENTED / MERGE APPROVAL PENDING |

## P4 verified invariants
- isolated synthetic/test-only screen realization;
- maps dashboard, animal-session, limb/claw, zone/lesion, treatment and report-summary screens;
- preserves required banner and dashboard counters;
- primary button touch targets remain >=48×48 px;
- `kvk_connection_allowed = false` and `real_farm_data_allowed = false`;
- no machine bus, command, write, configuration or actuation surface.

## Canonical checkpoints
PR #27 `3eb278f7a480734045027393a53a76f6cdc03f03`; PR #28 `ce72bc01f6ccbe671a5293bde8c0f19ef3ac3ee8`; PR #29 `ec2cea9b144256baca29cd1ea2f03bf0dfcf6def`; PR #30 `4228a1f0346480221d0afb779907537a50c65e70`; PR #31 `047e5bba348eaea0b52103230ec589df6f857036`; PR #32 `6b05f283c8e9e280ca0c91e26947cac8b149d24b`; PR #33 `a48eb7a8b1de94758e6c74945f710ff5084a4b8f`; approved post-P3 reconciliation PR #39 `ae871dd8a06f1854482c94b1241253df98d2689c`; corrective PR #41 `16f26ae8909e0d40037e163c90ccabf154070599`; corrective PR #49 `b47916aa23bae79008554d616b64a7f81cbde821` restoring exact approved tree `d094c02377b14ea8489ecdca8465841c4ce7de3a`.

## Next slice
After controlled merge and Repository Verification of P4, reconcile P4 as `MERGED / VERIFIED` before opening any P5 implementation.

## Authority boundary
`IA-HC-002` is active only for its literal isolated off-machine / non-actuating / synthetic-test physical-prototype scope. Any live KVK connection, machine I/O/control path, real-farm data, network/cloud exposure or deployment remains separately blocked.
