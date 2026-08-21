# HC-TRACE-001 — Traceability

## Status

`PROPOSED — FOUNDATION INITIALIZATION`

| ID | Source | Requirement / decision | Downstream artifact | Status |
|---|---|---|---|---|
| HC-FND-001 | Project Owner direction | HoofCare project starts as managed engineering program | FND-HC-001 | Proposed |
| HC-FND-002 | Project Owner direction | First target machine is KVK 801-1, generation circa 2013 | FND-HC-001, ROADMAP-HC-001 | Proposed |
| HC-SAF-001 | VoltOps-derived governance | No implementation may bypass machine safety | AGENTS.md, FND-HC-001, IA-HC-001 | Proposed |
| HC-SAF-002 | Project architecture intent | First KVK integration is read-only | FND-HC-001, IA-HC-001 | Proposed |
| HC-UX-001 | Existing concept work | HMI workflow covers animal → limb → claw → zone → lesion → treatment → materials → media → report | FND-HC-001, ROADMAP-HC-001 | Proposed |
| HC-DATA-001 | Existing concept work | Session records require animal/operator/time provenance | FND-HC-001 | Proposed |
| HC-VET-001 | Veterinary boundary | System supports human classification and documentation; no autonomous clinical authority | FND-HC-001, IA-HC-001 | Proposed |
| HC-HW-001 | Prototype concept | Kinco GL100E 10.1" is current bench MVP candidate, not final baseline | FND-HC-001, CURRENT_STATE | Proposed |
| HC-PROC-001 | VoltOps-derived governance | Branch → Draft PR → CI/review → exact-head approval → merge → post-merge verification | AGENTS.md | Established by bootstrap |

## Closure rule

No row may move to `Implemented`, `Verified` or `Closed` without a linked baselined requirement/decision and fresh verification evidence appropriate to its layer.
