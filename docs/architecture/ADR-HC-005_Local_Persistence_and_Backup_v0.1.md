# ADR-HC-005 — Local Persistence and Backup v0.1

## Status
`APPROVED / BASELINED — PR #4`

Approved PR head: `26c66a0e2ada0348c7204516c02f4c8b0581f38f`  
Canonical merge SHA: `c2493ef39a1b45b934cd2dc001279db110a17fc0`

## Decision
The target system SHALL be local-first and SHALL continue core treatment-session operation without Internet connectivity. Durable structured data SHALL be stored outside the HMI in a local persistence layer with explicit backup and recovery semantics.

Completed records SHALL be append/audit oriented: corrections are recorded as traceable changes rather than silent history replacement.

## MVP
Bench MVP may use a lightweight local database or file-backed test store, provided the public data model is not coupled to a specific vendor.

## Production requirement
Backup interval, retention, recovery point objective and removable/network backup target must be defined before production release.
