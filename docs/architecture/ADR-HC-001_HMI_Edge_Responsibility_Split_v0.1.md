# ADR-HC-001 — HMI / Edge Responsibility Split v0.1

## Status
`APPROVED / BASELINED — PR #4`

Approved PR head: `26c66a0e2ada0348c7204516c02f4c8b0581f38f`  
Canonical merge SHA: `c2493ef39a1b45b934cd2dc001279db110a17fc0`

## Decision
HMI SHALL be the operator interaction surface, not the sole system-of-record. Persistent session data, media indexing, report generation, backup/recovery and future external integrations SHALL reside in a separate local edge/controller service or equivalent non-HMI persistence layer.

The HMI MAY cache current-session state, but loss/replacement of the HMI SHALL NOT cause permanent loss of historical treatment records in the target architecture.

## Rationale
- isolates UI replacement from historical data;
- supports richer reporting/media than an HMI-only architecture;
- preserves local-first operation;
- reduces coupling between industrial visualization and data services.

## Constraints
- no live KVK actuation is introduced;
- HMI failure must not affect original KVK safety;
- bench implementation remains blocked until authority is activated.

## Consequences
System Architecture must define a clear HMI↔edge contract, session recovery semantics and offline behavior.
