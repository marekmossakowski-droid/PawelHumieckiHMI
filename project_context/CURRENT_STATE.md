# HoofCare — CURRENT STATE

## Naming status

`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. They are not an approved commercial/product name. Final product name: `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status

`F70 / IMPLEMENTATION PLAN + AUTHORITY GATE — IN PROGRESS`

## Canonical repository

`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical main checkpoints

- `HC-FOUNDATION-001`: PR #1 approved head `dd71ddac5cfc655a55263e2e28346e43f4df5044`, merged as `de68522e4851f645d65dee7dda08ef8fed6af955`.
- `HC-ARS-001`: PR #2 approved head `650f2957c5b57a070108beb710724c59d07db2ad`, merged as `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- `HC-ARB-001`: PR #3 approved head `59bfe6c6eb643ac16b49c84b10b1e6ecd0f2a130`, merged as `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- `HC-ADR-SET-001`: PR #4 approved head `26c66a0e2ada0348c7204516c02f4c8b0581f38f`, merged as `c2493ef39a1b45b934cd2dc001279db110a17fc0`.
- `HC-SYSTEM-ARCH-001`: PR #5 approved head `147877cf370f348a04d0b5fd923a641efb5b72fe`, merged as `5a0761dec9dbbca538be787839d93017f5c501df`.
- `HC-LEL-001`: PR #6 approved head `25d66772cf7459e4f12a3cb806de9567ad46b567`, merged as `a7d031317cf25934218cd09a4916449f2bf5b634`.
- `HC-REQ-001`: PR #7 approved head `c8608b35aefc815a74a20f443de679ac0db40e13`, merged as `e34e2a2ae3f709d83c24d528f8930b1b72060961`.

## Current branch

`planning/hc-imp-001`

## Product baseline

- Product identity: not commercially named; current identifiers are codenames only.
- First target machine: KVK 801-1, generation circa 2013, older green construction.
- Current hardware candidate for bench MVP: Kinco GL100E 10.1"; candidate only, not baseline.
- Physical machine audit: `BLOCKED_BY_SITE_ACCESS` until access to the actual chute is available.

## Governance state

- `FND-HC-001`: `BASELINED`.
- `ARS-HC-001`: `BASELINED`.
- `ARB-HC-001`: `BASELINED`.
- `ADR-HC-001` through `ADR-HC-007`: `APPROVED / BASELINED`.
- `SA-HC-001`: `BASELINED`.
- `LEL-HC-001`: `BASELINED`.
- `REQ-HC-001`: `BASELINED` by approved and merged PR #7.
- `IMP-HC-001`: `PROPOSED — PROJECT OWNER APPROVAL REQUIRED`.
- `IA-HC-001`: proposed; `NOT ACTIVE`.
- Runtime implementation authority: `NOT ESTABLISHED`.

## Safety state

- original KVK safety remains independent;
- initial KVK integration is observational/read-only;
- no live KVK write/control path is authorized;
- no autonomous veterinary diagnosis is authorized;
- loss of HMI/edge services must not affect original KVK safety.

## Current workstream

`HC-IMP-001`

Purpose: establish the smallest test-first bench MVP implementation plan and present `IA-HC-001` for explicit Project Owner activation without expanding authority beyond synthetic/test-only local runtime work.

## Planned implementation sequence after authority activation

1. Domain/session core with failing tests first.
2. Durable local persistence and restart recovery.
3. Local bench API / HMI contract.
4. HMI prototype workflow and counters.
5. Local PDF reporting from canonical records.
6. Simulated RFID and KVK observation adapters only.
7. Bench verification against REQ-HC-001.

## Explicit blockers

- Runtime implementation remains blocked until `IA-HC-001` is explicitly approved and activated.
- Physical KVK-specific hardware integration remains blocked until the actual machine can be inspected and photographed.
- Commercial/product naming remains undecided.
