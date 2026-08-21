# HC-TRACE-001 — Traceability

## Status

`ACTIVE — F20 / ARB`

| ID | Source | Requirement / decision | Downstream artifact | Status |
|---|---|---|---|---|
| HC-FND-001 | Project Owner direction | Project starts as managed engineering program | FND-HC-001 | Baselined |
| HC-FND-002 | Project Owner direction | First target machine is KVK 801-1, generation circa 2013 | FND-HC-001, ROADMAP-HC-001, ARS-HC-001, ARB-HC-001 | Baselined |
| HC-FND-003 | Project Owner direction | Current project/repository names are internal codenames only; commercial/product name remains TBD | README, FND-HC-001, CURRENT_STATE, ARS-HC-001, ARB-HC-001 | Baselined |
| HC-SAF-001 | Foundation / governance | No implementation may bypass machine safety | AGENTS.md, FND-HC-001, IA-HC-001, ARS-HC-001, ARB-HC-001 | Baselined |
| HC-SAF-002 | Foundation architecture intent | First KVK integration is read-only | FND-HC-001, IA-HC-001, ARS-HC-001, ARB-HC-001 | Baselined |
| HC-ARS-OP-001 | ARS | Operator needs rapid structured treatment-session workflow | ARS-HC-001, ARB-HC-001 | Baselined |
| HC-ARS-FARM-001 | ARS | Farmer needs individual reports, herd overview and follow-up queue | ARS-HC-001 | Baselined |
| HC-ARS-VET-001 | ARS | Veterinary users need provenance, history, escalation support and human clinical authority | ARS-HC-001, ARB-HC-001 | Baselined |
| HC-ARS-ZOO-001 | ARS | Zootechnical users need recurrence and group-level context | ARS-HC-001 | Baselined |
| HC-ARS-NUT-001 | ARS | Nutritionist needs trend context without causal overclaim | ARS-HC-001, ARB-HC-001 | Baselined |
| HC-ARS-TECH-001 | ARS | Technical service needs machine-safety independence, diagnostics and recoverability | ARS-HC-001, ARB-HC-001 | Baselined |
| HC-ARS-DATA-001 | ARS | Data requires integrity, auditability and media/session linkage | ARS-HC-001, ARB-HC-001 | Baselined |
| HC-ARS-REP-001 | ARS | Reporting must support farmer, veterinary, zootechnical, nutritionist and technical audiences | ARS-HC-001 | Baselined |
| HC-ARB-KVK-001 | ARB | First live KVK interface is observational/read-only | ARB-HC-001 | Proposed |
| HC-ARB-SAF-001 | ARB | HoofCare cannot become a dependency of original KVK safety | ARB-HC-001 | Proposed |
| HC-ARB-CLIN-001 | ARB | Final clinical authority remains human | ARB-HC-001 | Proposed |
| HC-ARB-DATA-001 | ARB | Bench MVP is local-first and session identity/media provenance form one integrity boundary | ARB-HC-001 | Proposed |
| HC-ARB-HMI-001 | ARB | HMI owns interaction, not machine safety or sole permanent archive | ARB-HC-001 | Proposed |
| HC-ARB-NET-001 | ARB | Bench operation has no Internet dependency | ARB-HC-001 | Proposed |
| HC-HW-001 | Prototype concept | Kinco GL100E 10.1" is current bench MVP candidate, not final baseline | FND-HC-001, CURRENT_STATE, ARS-HC-001, ARB-HC-001 | Candidate |
| HC-PROC-001 | Governance | Branch → Draft PR → CI/review → exact-head approval → merge → post-merge verification | AGENTS.md | Established |

## Canonical checkpoints

- `HC-FOUNDATION-001`: approved PR head `dd71ddac5cfc655a55263e2e28346e43f4df5044`, merged as `de68522e4851f645d65dee7dda08ef8fed6af955`.
- `HC-ARS-001`: approved PR head `650f2957c5b57a070108beb710724c59d07db2ad`, merged as `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.

## Closure rule

No row may move to `Implemented`, `Verified` or `Closed` without a linked baselined requirement/decision and fresh verification evidence appropriate to its layer.
