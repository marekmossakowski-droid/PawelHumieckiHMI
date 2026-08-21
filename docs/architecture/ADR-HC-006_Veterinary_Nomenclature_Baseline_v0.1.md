# ADR-HC-006 — Veterinary Nomenclature Baseline v0.1

## Status
`APPROVED / BASELINED — PR #4`

Approved PR head: `26c66a0e2ada0348c7204516c02f4c8b0581f38f`  
Canonical merge SHA: `c2493ef39a1b45b934cd2dc001279db110a17fc0`

## Decision
The product SHALL use a controlled, versioned veterinary nomenclature for anatomical zones and hoof lesions. Free text may supplement but SHALL NOT replace controlled classification for analytics.

The clinical taxonomy SHALL be versioned independently from UI labels so wording can evolve without corrupting historical records.

Human clinical authority remains mandatory: the taxonomy supports consistent recording and does not grant autonomous diagnostic authority to the system.

## Minimum anatomical baseline
Toe, sole, white line, axial wall, abaxial wall, heel/bulb region, soft heel tissue and interdigital cleft/space.

## Deferred decision
The exact external veterinary reference/standard and mapping identifiers SHALL be verified and approved before production clinical use.
