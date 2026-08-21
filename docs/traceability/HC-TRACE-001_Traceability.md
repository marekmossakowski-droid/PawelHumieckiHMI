# HC-TRACE-001 — Traceability

## Status

`ACTIVE — F40 / SYSTEM ARCHITECTURE`

| ID | Source | Requirement / decision | Downstream artifact | Status |
|---|---|---|---|---|
| HC-FND-001 | Project Owner direction | Project starts as managed engineering program | FND-HC-001 | Baselined |
| HC-FND-002 | Project Owner direction | First target machine is KVK 801-1, generation circa 2013 | FND-HC-001, ROADMAP-HC-001, ARS-HC-001, ARB-HC-001, SA-HC-001 | Baselined |
| HC-FND-003 | Project Owner direction | Current project/repository names are internal codenames only; commercial/product name remains TBD | README, FND-HC-001, CURRENT_STATE | Baselined |
| HC-SAF-001 | Foundation / governance | No implementation may bypass machine safety | AGENTS.md, FND-HC-001, IA-HC-001, ARS-HC-001, ARB-HC-001, ADR-HC-002, SA-HC-001 | Baselined |
| HC-SAF-002 | Foundation architecture intent | First KVK integration is read-only | FND-HC-001, IA-HC-001, ARS-HC-001, ARB-HC-001, ADR-HC-002, SA-HC-001 | Baselined |
| HC-ARS-OP-001 | ARS | Operator needs rapid structured treatment-session workflow | ARS-HC-001, ADR-HC-001, SA-HC-001 | Baselined |
| HC-ARS-FARM-001 | ARS | Farmer needs individual reports, herd overview and follow-up queue | ARS-HC-001, ADR-HC-007, SA-HC-001 | Baselined |
| HC-ARS-VET-001 | ARS | Veterinary users need provenance, history, escalation support and human clinical authority | ARS-HC-001, ADR-HC-004, ADR-HC-006, SA-HC-001 | Baselined |
| HC-ARS-NUT-001 | ARS | Nutritionist needs trend context without causal overclaim | ARS-HC-001, ADR-HC-006, ADR-HC-007, SA-HC-001 | Baselined |
| HC-ARS-TECH-001 | ARS | Technical service needs machine-safety independence, diagnostics and recoverability | ARS-HC-001, ADR-HC-001, ADR-HC-002, ADR-HC-005, SA-HC-001 | Baselined |
| HC-ARS-DATA-001 | ARS | Data requires integrity, auditability and media/session linkage | ARS-HC-001, ADR-HC-004, ADR-HC-005, SA-HC-001 | Baselined |
| HC-ARS-REP-001 | ARS | Reporting must support multiple audiences | ARS-HC-001, ADR-HC-007, SA-HC-001 | Baselined |
| HC-ARB-KVK-001 | ARB | First live KVK interface is observational/read-only | ARB-HC-001, ADR-HC-002, SA-HC-001 | Baselined |
| HC-ARB-SAF-001 | ARB | System cannot become a dependency of original KVK safety | ARB-HC-001, ADR-HC-002, SA-HC-001 | Baselined |
| HC-ARB-CLIN-001 | ARB | Final clinical authority remains human | ARB-HC-001, ADR-HC-006, SA-HC-001 | Baselined |
| HC-ARB-DATA-001 | ARB | Bench MVP is local-first and session identity/media provenance form one integrity boundary | ARB-HC-001, ADR-HC-003, ADR-HC-004, ADR-HC-005, SA-HC-001 | Baselined |
| HC-ARB-HMI-001 | ARB | HMI owns interaction, not machine safety or sole permanent archive | ARB-HC-001, ADR-HC-001, SA-HC-001 | Baselined |
| HC-ARB-NET-001 | ARB | Bench operation has no Internet dependency | ARB-HC-001, ADR-HC-005, SA-HC-001 | Baselined |
| HC-ADR-001 | F30 decision | HMI and local edge/data responsibilities are separated | ADR-HC-001, SA-HC-001 | Baselined |
| HC-ADR-002 | F30 decision | KVK integration strategy is observational/read-only | ADR-HC-002, SA-HC-001 | Baselined |
| HC-ADR-003 | F30 decision | Animal identity uses internal immutable identity with pluggable external identifiers | ADR-HC-003, SA-HC-001 | Baselined |
| HC-ADR-004 | F30 decision | Media are immutable provenance-linked evidence objects | ADR-HC-004, SA-HC-001 | Baselined |
| HC-ADR-005 | F30 decision | Persistence is local-first with explicit backup/recovery | ADR-HC-005, SA-HC-001 | Baselined |
| HC-ADR-006 | F30 decision | Veterinary nomenclature is controlled and versioned; human authority remains final | ADR-HC-006, SA-HC-001 | Baselined |
| HC-ADR-007 | F30 decision | Reports derive from canonical structured records, not transient HMI state | ADR-HC-007, SA-HC-001 | Baselined |
| HC-SA-001 | System Architecture | HMI is interaction surface; edge/application layer owns canonical session lifecycle | SA-HC-001 | Proposed |
| HC-SA-002 | System Architecture | Durable local store and media store are independent of HMI replacement | SA-HC-001 | Proposed |
| HC-SA-003 | System Architecture | KVK Observation Adapter has no write/actuation route | SA-HC-001 | Proposed |
| HC-SA-004 | System Architecture | Identity ambiguity blocks automatic commit to animal history | SA-HC-001 | Proposed |
| HC-SA-005 | System Architecture | Reports are generated from committed canonical records | SA-HC-001 | Proposed |
| HC-SA-006 | System Architecture | HMI/edge/KVK-observation failures degrade workflow without affecting KVK safety | SA-HC-001 | Proposed |
| HC-HW-001 | Prototype concept | Kinco GL100E 10.1" is current bench MVP candidate, not final baseline | FND-HC-001, CURRENT_STATE, ARS-HC-001, ARB-HC-001, SA-HC-001 | Candidate |
| HC-PROC-001 | Governance | Branch → Draft PR → CI/review → exact-head approval → merge → post-merge verification | AGENTS.md | Established |

## Canonical checkpoints

- `HC-FOUNDATION-001`: approved PR head `dd71ddac5cfc655a55263e2e28346e43f4df5044`, merged as `de68522e4851f645d65dee7dda08ef8fed6af955`.
- `HC-ARS-001`: approved PR head `650f2957c5b57a070108beb710724c59d07db2ad`, merged as `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- `HC-ARB-001`: approved PR head `59bfe6c6eb643ac16b49c84b10b1e6ecd0f2a130`, merged as `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- `HC-ADR-SET-001`: approved PR head `26c66a0e2ada0348c7204516c02f4c8b0581f38f`, merged as `c2493ef39a1b45b934cd2dc001279db110a17fc0`.

## Closure rule

No row may move to `Implemented`, `Verified` or `Closed` without a linked baselined requirement/decision and fresh verification evidence appropriate to its layer.
