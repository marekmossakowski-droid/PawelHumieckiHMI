# HoofCare — CURRENT STATE

## Naming status

`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. They are not an approved commercial/product name. Final product name: `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status

`F10 / ARS — IN PROGRESS`

## Canonical repository

`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical main checkpoint

- `HC-FOUNDATION-001`: merged via PR #1.
- approved PR head: `dd71ddac5cfc655a55263e2e28346e43f4df5044`.
- canonical merge SHA: `de68522e4851f645d65dee7dda08ef8fed6af955`.

## Current branch

`requirements/hc-ars-001`

## Product baseline

- Product identity: not commercially named; current identifiers are codenames only.
- First target machine: KVK 801-1, generation circa 2013, older green construction.
- Current hardware candidate for bench MVP: Kinco GL100E 10.1"; candidate only, not baseline.
- Physical machine audit: `BLOCKED_BY_SITE_ACCESS` until access to the actual chute is available.

## Governance state

- `AGENTS.md`: established.
- `FND-HC-001`: `BASELINED` by approved and merged `HC-FOUNDATION-001`.
- `ROADMAP-HC-001`: established by the same foundation change set.
- `HC-TRACE-001`: established; actively maintained.
- `IA-HC-001`: proposed; `NOT ACTIVE`.
- Runtime implementation authority: `NOT ESTABLISHED`.

## Safety state

- System SHALL NOT replace or bypass original KVK safety functions.
- Initial KVK integration is read-only.
- No live KVK control is authorized.
- No autonomous veterinary diagnosis is authorized.

## Current workstream

`HC-ARS-001`

Purpose: define application and stakeholder requirements before ARB, ADR, system architecture, LEL and implementable requirements.

## Current ARS coverage

- operator workflow;
- farmer/herd-owner reporting;
- veterinary requirements and human clinical authority;
- zootechnical requirements;
- nutritionist trend context;
- technical-service requirements;
- data/audit/reporting requirements;
- HMI/environmental constraints;
- explicit safety and non-goal boundaries.

## Next dependency-ordered steps

1. Complete ARS traceability and consistency review.
2. Publish `HC-ARS-001` through Draft PR and CI.
3. Final reconciliation and exact-head Project Owner approval for merge.
4. After ARS merge, begin `F20 / ARB` autonomously.
5. Continue ADR → System Architecture → LEL → Requirements without runtime implementation until authority is explicitly active.

## Explicit blockers

- Physical KVK-specific hardware integration remains blocked until the actual machine can be inspected and photographed.
- Bench software implementation remains blocked until `IA-HC-001` is explicitly approved and activated.
- Commercial/product naming remains undecided and must not be inferred from repository or engineering codenames.
