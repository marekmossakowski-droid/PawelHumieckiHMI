# HoofCare — CURRENT STATE

## Naming status

`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. They are not an approved commercial/product name. Final product name: `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status

`F20 / ARB — IN PROGRESS`

## Canonical repository

`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical main checkpoints

- `HC-FOUNDATION-001`: PR #1 approved head `dd71ddac5cfc655a55263e2e28346e43f4df5044`, merged as `de68522e4851f645d65dee7dda08ef8fed6af955`.
- `HC-ARS-001`: PR #2 approved head `650f2957c5b57a070108beb710724c59d07db2ad`, merged as `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.

## Current branch

`architecture/hc-arb-001`

## Product baseline

- Product identity: not commercially named; current identifiers are codenames only.
- First target machine: KVK 801-1, generation circa 2013, older green construction.
- Current hardware candidate for bench MVP: Kinco GL100E 10.1"; candidate only, not baseline.
- Physical machine audit: `BLOCKED_BY_SITE_ACCESS` until access to the actual chute is available.

## Governance state

- `AGENTS.md`: established.
- `FND-HC-001`: `BASELINED`.
- `ARS-HC-001`: `BASELINED` by approved and merged `HC-ARS-001`.
- `ROADMAP-HC-001`: established.
- `HC-TRACE-001`: active.
- `IA-HC-001`: proposed; `NOT ACTIVE`.
- Runtime implementation authority: `NOT ESTABLISHED`.

## Safety state

- System SHALL NOT replace or bypass original KVK safety functions.
- Initial KVK integration is read-only.
- No live KVK control is authorized.
- No autonomous veterinary diagnosis is authorized.

## Current workstream

`HC-ARB-001`

Purpose: establish explicit system, KVK, safety, clinical, data, HMI, peripheral, network and failure boundaries before ADR and System Architecture.

## Next dependency-ordered steps

1. Complete ARB traceability and CI checks.
2. Publish and reconcile `HC-ARB-001` through Draft PR.
3. Final exact-head Project Owner approval for merge.
4. After merge, begin F30 / ADR set autonomously.
5. Continue System Architecture → LEL → Requirements without runtime implementation until authority is explicitly active.

## Explicit blockers

- Physical KVK-specific hardware integration remains blocked until the actual machine can be inspected and photographed.
- Bench software implementation remains blocked until `IA-HC-001` is explicitly approved and activated.
- Commercial/product naming remains undecided and must not be inferred from repository or engineering codenames.
