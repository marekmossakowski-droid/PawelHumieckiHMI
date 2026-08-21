# ADR-HC-003 — Animal Identity Strategy v0.1

## Status
`APPROVED / BASELINED — PR #4`

Approved PR head: `26c66a0e2ada0348c7204516c02f4c8b0581f38f`  
Canonical merge SHA: `c2493ef39a1b45b934cd2dc001279db110a17fc0`

## Decision
Animal identity SHALL be represented by an internal immutable animal identifier plus one or more external identifiers. RFID is the preferred acquisition method for field operation, but the core model SHALL NOT depend on one RFID technology or vendor.

The system SHALL require explicit confidence in identity before committing a session to animal history. Missing, conflicting or duplicate identity SHALL fail closed into an unresolved-session state.

## MVP
Bench MVP SHALL use synthetic identifiers and simulated RFID input only.

## Deferred choices
Exact tag standard, reader, antenna placement and herd-system mapping remain downstream decisions and depend on the target farm.
