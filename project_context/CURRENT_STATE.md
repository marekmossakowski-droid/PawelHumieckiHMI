# HoofCare — CURRENT STATE

## Naming status

`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. They are not an approved commercial/product name. Final product name: `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status

`FOUNDATION / GOVERNANCE INITIALIZATION`

## Canonical repository

`marekmossakowski-droid/PawelHumieckiHMI`

## Current branch

`foundation/hc-foundation-001`

## Product baseline

- Product identity: not commercially named; current identifiers are codenames only.
- First target machine: KVK 801-1, generation circa 2013, older green construction.
- Current hardware candidate for bench MVP: Kinco GL100E 10.1".
- Physical machine audit: `BLOCKED_BY_SITE_ACCESS` until access to the actual chute is available.

## Governance state

- `AGENTS.md`: bootstrap established on main.
- `FND-HC-001`: proposed.
- `ROADMAP-HC-001`: proposed.
- `IA-HC-001`: proposed; NOT ACTIVE.
- Runtime implementation authority: NOT ESTABLISHED.

## Safety state

- System SHALL NOT replace or bypass original KVK safety functions.
- Initial KVK integration is read-only.
- No live KVK control is authorized.
- No autonomous veterinary diagnosis is authorized.

## Current workstream

`HC-FOUNDATION-001`

Purpose: establish project SSOT, governance, roadmap, initial authority boundary and traceability before any runtime implementation.

## Next dependency-ordered steps

1. Complete traceability for Foundation.
2. Keep PR #1 as Draft until final reconciliation.
3. Verify final diff/head after codename clarification.
4. Request Project Owner approval for the new exact head.
5. After merge, begin ARS workstream.

## Explicit blockers

- Physical KVK-specific hardware integration remains blocked until the actual machine can be inspected and photographed.
- Bench software implementation remains blocked until `IA-HC-001` is explicitly approved and activated.
- Commercial/product naming remains undecided and must not be inferred from repository or engineering codenames.
