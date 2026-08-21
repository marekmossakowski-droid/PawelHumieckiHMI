# HoofCare — CURRENT STATE

## Naming status
`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. Final commercial/product name remains `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status
`F90 / PHYSICAL PROTOTYPE — P3 MERGED / VERIFIED / P4 NEXT`

## Canonical repository
`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical main checkpoints
- Foundation PR #1 → `de68522e4851f645d65dee7dda08ef8fed6af955`.
- ARS PR #2 → `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- ARB PR #3 → `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- ADR PR #4 → `c2493ef39a1b45b934cd2dc001279db110a17fc0`.
- System Architecture PR #5 → `5a0761dec9dbbca538be787839d93017f5c501df`.
- LEL PR #6 → `a7d031317cf25934218cd09a4916449f2bf5b634`.
- Requirements PR #7 → `e34e2a2ae3f709d83c24d528f8930b1b72060961`.
- IMP + IA activation PR #8 → `0d58eb2921df298114c304295a061547598ae541`.
- S1 PR #9 → `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2`.
- S2 PR #10 → `c5f60dbf11b04b680c6f51f2e610d33906b08637`.
- S3 PR #11 → `003c8d5d0ab9e026a76e4a519e8b1c246458bc8a`.
- S4 PR #12 → `e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34`.
- S5 PR #13 → `30acc2d9a0833844e7279c68d9884cf9dd124cea`.
- S6 PR #14 → `56da4eaf1316c930ca6095cd068e90bd66e2f624`.
- S7 PR #16 → `0827d0d4b51a0a63c773a1f8ce178d7954dc25a5`.
- Bench MVP closure PR #17 → `36ffda3b2363597b8a8aae3746e9d555450c625c`.
- Corrective authority rollback PR #21 → `ce58dd3e5ab9346442456736b646eacbc4309a8a`.
- IA-HC-002 activation PR #27 → `3eb278f7a480734045027393a53a76f6cdc03f03`.
- IA-HC-002 post-activation reconciliation PR #28 → `ce72bc01f6ccbe671a5293bde8c0f19ef3ac3ee8`.
- HC-P1-001 PR #29 → `ec2cea9b144256baca29cd1ea2f03bf0dfcf6def`.
- HC-P1 post-merge reconciliation PR #30 → `4228a1f0346480221d0afb779907537a50c65e70`.
- HC-P2-001 PR #31 approved head `5ea083ad0ac9ed0b2c965af167a6db821429c9fb` → merge `047e5bba348eaea0b52103230ec589df6f857036`.
- HC-P2 post-merge reconciliation PR #32 → `6b05f283c8e9e280ca0c91e26947cac8b149d24b`.
- HC-P3-001 PR #33 approved head `2de9b10aab518ac8e92cfbaf84dbc64c728d9300` → merge `a48eb7a8b1de94758e6c74945f710ff5084a4b8f`.
- Approved post-P3 reconciliation PR #39 → `ae871dd8a06f1854482c94b1241253df98d2689c`.
- Corrective removal PR #41 approved head `d38f89ccd0ded0daa9fc0ee30d7d0dbcb919a014` → merge `16f26ae8909e0d40037e163c90ccabf154070599`.

## Governance state
- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-001`: `FULFILLED FOR AUTHORIZED BENCH SCOPE`.
- `HC-S1-001` through `HC-S7-001`: `MERGED / VERIFIED`.
- `HC-BENCH-MVP-CLOSURE-001`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.
- `IA-HC-002`: `APPROVED / ACTIVE` only for its literal isolated off-machine / non-actuating / synthetic-test physical-prototype scope.
- `HC-P1-001` through `HC-P3-001`: `MERGED / VERIFIED`.
- `HC-P4-001`: `NEXT / NOT YET IMPLEMENTED`.

## Active authority boundaries
Authorized: isolated physical HMI prototype work, low-voltage bench work, synthetic/test data, simulated RFID/KVK sources, local persistence/reporting/navigation, and serial/RS-485/Modbus only against dedicated simulators/test equipment.

Not authorized: any electrical or logical connection to real KVK 801-1; live RFID with real-farm data; live KVK I/O; CAN/RS-485/Modbus/serial to the machine; KVK commands/writes/configuration/actuation; hydraulics; PLC/safety mutation; autonomous veterinary diagnosis; real-farm data; network/cloud exposure; deployment/signing/release/public distribution.

## P3 verified invariants
- nominal bench supply is 24 VDC;
- BOM includes 10.1-inch HMI, 8DI/8DO simulator I/O, terminal blocks, fuse protection, test switches and lamps;
- USB/RS-485 is permitted only against dedicated simulator/test equipment;
- KVK connection is explicitly forbidden;
- real-farm data are explicitly forbidden;
- no live machine-bus or actuation surface exists.

## Current / next workstream
`HC-P4-001 — Physical screen realization`

P4 may realize the already-approved 10.1-inch/1024×600 screen model as isolated synthetic/test-only physical-prototype widgets and bindings. It must preserve >=48×48 px primary touch targets, fail-closed identity states and the existing dashboard/workflow semantics, and must not add any KVK control affordance or machine I/O surface.

## Explicit blockers
- Any live KVK integration remains blocked until the actual circa-2013 KVK 801-1 is inspected and photographed and a separate live observation authority is approved.
- Commercial/product naming remains undecided.
