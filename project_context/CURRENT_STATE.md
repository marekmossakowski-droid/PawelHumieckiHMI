# HoofCare — CURRENT STATE

## Naming status

`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. They are not an approved commercial/product name. Final product name: `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status

`F40 / SYSTEM ARCHITECTURE — IN PROGRESS`

## Canonical repository

`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical main checkpoints

- `HC-FOUNDATION-001`: PR #1 approved head `dd71ddac5cfc655a55263e2e28346e43f4df5044`, merged as `de68522e4851f645d65dee7dda08ef8fed6af955`.
- `HC-ARS-001`: PR #2 approved head `650f2957c5b57a070108beb710724c59d07db2ad`, merged as `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- `HC-ARB-001`: PR #3 approved head `59bfe6c6eb643ac16b49c84b10b1e6ecd0f2a130`, merged as `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- `HC-ADR-SET-001`: PR #4 approved head `26c66a0e2ada0348c7204516c02f4c8b0581f38f`, merged as `c2493ef39a1b45b934cd2dc001279db110a17fc0`.

## Current branch

`architecture/hc-system-architecture-001`

## Product baseline

- Product identity: not commercially named; current identifiers are codenames only.
- First target machine: KVK 801-1, generation circa 2013, older green construction.
- Current hardware candidate for bench MVP: Kinco GL100E 10.1"; candidate only, not baseline.
- Physical machine audit: `BLOCKED_BY_SITE_ACCESS` until access to the actual chute is available.

## Governance state

- `FND-HC-001`: `BASELINED`.
- `ARS-HC-001`: `BASELINED`.
- `ARB-HC-001`: `BASELINED`.
- `ADR-HC-001` through `ADR-HC-007`: `APPROVED / BASELINED` by approved and merged PR #4.
- `HC-TRACE-001`: active.
- `IA-HC-001`: proposed; `NOT ACTIVE`.
- Runtime implementation authority: `NOT ESTABLISHED`.

## Safety state

- original KVK safety remains independent;
- initial KVK integration is observational/read-only;
- no live KVK write/control path is authorized;
- no autonomous veterinary diagnosis is authorized;
- loss of HMI/edge services must not affect original KVK safety.

## Current workstream

`HC-SYSTEM-ARCH-001`

Purpose: establish component responsibilities, data flows, hardware topology, trust boundaries, failure modes, recovery principles and deployment units before LEL and implementable requirements.

## System Architecture component set

1. Industrial HMI.
2. Edge/Application Controller.
3. Durable Local Store.
4. Media Store.
5. Animal Identity Adapter.
6. Future KVK Observation Adapter — read-only only.
7. Report Service.

## Current architectural invariants

- HMI is not the sole system-of-record.
- canonical records live in the local data/application layer.
- KVK integration has no write route.
- ambiguous animal identity fails closed.
- clinical authority remains human.
- bench MVP has no Internet dependency.
- report generation derives from committed canonical records.

## Next dependency-ordered steps

1. Complete System Architecture traceability and docs-ci checks.
2. Publish `HC-SYSTEM-ARCH-001` through Draft PR.
3. Final reconciliation and exact-head Project Owner approval for merge.
4. After merge, begin F50 / LEL autonomously.
5. Continue Requirements planning without runtime implementation until `IA-HC-001` is explicitly activated.

## Explicit blockers

- Physical KVK-specific hardware integration remains blocked until the actual machine can be inspected and photographed.
- Bench software implementation remains blocked until `IA-HC-001` is explicitly approved and activated.
- Commercial/product naming remains undecided.
