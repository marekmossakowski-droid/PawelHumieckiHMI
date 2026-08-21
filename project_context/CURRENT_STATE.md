# HoofCare — CURRENT STATE

## Naming status

`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. They are not an approved commercial/product name. Final product name: `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status

`F30 / ADR — IN PROGRESS`

## Canonical repository

`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical main checkpoints

- `HC-FOUNDATION-001`: PR #1 approved head `dd71ddac5cfc655a55263e2e28346e43f4df5044`, merged as `de68522e4851f645d65dee7dda08ef8fed6af955`.
- `HC-ARS-001`: PR #2 approved head `650f2957c5b57a070108beb710724c59d07db2ad`, merged as `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- `HC-ARB-001`: PR #3 approved head `59bfe6c6eb643ac16b49c84b10b1e6ecd0f2a130`, merged as `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.

## Current branch

`architecture/hc-adr-set-001`

## Product baseline

- Product identity: not commercially named; current identifiers are codenames only.
- First target machine: KVK 801-1, generation circa 2013, older green construction.
- Current hardware candidate for bench MVP: Kinco GL100E 10.1"; candidate only, not baseline.
- Physical machine audit: `BLOCKED_BY_SITE_ACCESS` until access to the actual chute is available.

## Governance state

- `FND-HC-001`: `BASELINED`.
- `ARS-HC-001`: `BASELINED`.
- `ARB-HC-001`: `BASELINED` by approved and merged `HC-ARB-001`.
- `HC-TRACE-001`: active.
- `IA-HC-001`: proposed; `NOT ACTIVE`.
- Runtime implementation authority: `NOT ESTABLISHED`.

## Safety state

- original KVK safety remains independent;
- initial KVK integration is observational/read-only;
- no live KVK write/control path is authorized;
- no autonomous veterinary diagnosis is authorized.

## Current workstream

`HC-ADR-SET-001`

Purpose: establish the material architecture decisions required before System Architecture.

## Proposed ADR set

1. `ADR-HC-001` — HMI / edge responsibility split.
2. `ADR-HC-002` — KVK read-only integration strategy.
3. `ADR-HC-003` — animal identity strategy.
4. `ADR-HC-004` — media acquisition and storage.
5. `ADR-HC-005` — local persistence and backup.
6. `ADR-HC-006` — veterinary nomenclature baseline.
7. `ADR-HC-007` — report generation architecture.

All seven remain `PROPOSED — PROJECT OWNER APPROVAL REQUIRED` until exact-head approval and merge.

## Next dependency-ordered steps

1. Complete ADR traceability and docs-ci checks.
2. Publish `HC-ADR-SET-001` through Draft PR.
3. Final reconciliation and exact-head Project Owner approval for merge.
4. After merge, begin F40 / System Architecture autonomously.
5. No runtime implementation until implementation authority is explicitly activated.

## Explicit blockers

- Physical KVK-specific hardware integration remains blocked until the actual machine can be inspected and photographed.
- Bench software implementation remains blocked until `IA-HC-001` is explicitly approved and activated.
- Commercial/product naming remains undecided.
