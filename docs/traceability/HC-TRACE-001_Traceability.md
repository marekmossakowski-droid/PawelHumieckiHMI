# HC-TRACE-001 — Traceability

## Status

`ACTIVE — F10 / ARS`

| ID | Source | Requirement / decision | Downstream artifact | Status |
|---|---|---|---|---|
| HC-FND-001 | Project Owner direction | Project starts as managed engineering program | FND-HC-001 | Baselined |
| HC-FND-002 | Project Owner direction | First target machine is KVK 801-1, generation circa 2013 | FND-HC-001, ROADMAP-HC-001, ARS-HC-001 | Baselined |
| HC-FND-003 | Project Owner direction | Current project/repository names are internal codenames only; commercial/product name remains TBD | README, FND-HC-001, CURRENT_STATE, ARS-HC-001 | Baselined |
| HC-SAF-001 | Foundation / VoltOps-derived governance | No implementation may bypass machine safety | AGENTS.md, FND-HC-001, IA-HC-001, ARS-HC-001 | Baselined |
| HC-SAF-002 | Foundation architecture intent | First KVK integration is read-only | FND-HC-001, IA-HC-001, ARS-HC-001 | Baselined |
| HC-UX-001 | Existing concept work | HMI workflow covers animal → limb → claw → zone → lesion → treatment → materials → media → report | FND-HC-001, ROADMAP-HC-001, ARS-HC-001 | ARS proposed |
| HC-DATA-001 | Foundation | Session records require animal/operator/time provenance | FND-HC-001, ARS-HC-001 | ARS proposed |
| HC-VET-001 | Foundation veterinary boundary | System supports human classification and documentation; no autonomous clinical authority | FND-HC-001, IA-HC-001, ARS-HC-001 | ARS proposed |
| HC-HW-001 | Prototype concept | Kinco GL100E 10.1" is current bench MVP candidate, not final baseline | FND-HC-001, CURRENT_STATE, ARS-HC-001 | Candidate |
| HC-PROC-001 | Governance | Branch → Draft PR → CI/review → exact-head approval → merge → post-merge verification | AGENTS.md | Established |
| HC-ARS-OP-001 | Stakeholder analysis | Operator needs rapid structured treatment-session workflow | ARS-HC-001 | Proposed |
| HC-ARS-FARM-001 | Stakeholder analysis | Farmer needs individual reports, herd overview and follow-up queue | ARS-HC-001 | Proposed |
| HC-ARS-VET-001 | Stakeholder analysis | Veterinary users need provenance, history, escalation support and human clinical authority | ARS-HC-001 | Proposed |
| HC-ARS-ZOO-001 | Stakeholder analysis | Zootechnical users need recurrence and group-level context | ARS-HC-001 | Proposed |
| HC-ARS-NUT-001 | Stakeholder analysis | Nutritionist needs trend context without causal overclaim | ARS-HC-001 | Proposed |
| HC-ARS-TECH-001 | Stakeholder analysis | Technical service needs machine-safety independence, diagnostics and recoverability | ARS-HC-001 | Proposed |
| HC-ARS-DATA-001 | Stakeholder analysis | Data requires integrity, auditability and media/session linkage | ARS-HC-001 | Proposed |
| HC-ARS-REP-001 | Stakeholder analysis | Reporting must support farmer, veterinary, zootechnical, nutritionist and technical audiences | ARS-HC-001 | Proposed |

## Canonical checkpoint

`HC-FOUNDATION-001` was approved on PR head `dd71ddac5cfc655a55263e2e28346e43f4df5044` and merged to `main` as `de68522e4851f645d65dee7dda08ef8fed6af955`.

## Closure rule

No row may move to `Implemented`, `Verified` or `Closed` without a linked baselined requirement/decision and fresh verification evidence appropriate to its layer.
