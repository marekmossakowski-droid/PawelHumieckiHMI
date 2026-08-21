# IMP-HC-001 — Bench MVP Implementation Plan v0.1

## Status
`APPROVED / BASELINED — PR #8`

Approved exact head: `9c939abea6794e2b5a4815c826410eb0166ab535`  
Canonical merge SHA: `0d58eb2921df298114c304295a061547598ae541`

## Purpose
Define the smallest authorized implementation sequence for a bench-only HoofCare MVP derived from the baselined Foundation, ARS, ARB, ADR set, System Architecture, LEL and REQ-HC-001.

## Scope
Bench-only runtime implementation using synthetic/test data. No live KVK connection, no machine actuation, no hydraulic or PLC writes, no safety mutation, no production deployment.

## Implementation slices

### S1 — Domain/session core
- explicit session state machine matching LEL-HC-001;
- animal identity resolution states including fail-closed ambiguity;
- treatment, material and media references;
- idempotent event application;
- unit tests first.

### S2 — Durable local persistence
- local structured store outside HMI;
- append/audit-oriented amendments;
- restart recovery of non-terminal sessions;
- synthetic data only.

### S3 — Bench API / HMI contract
- local-only contract between HMI presentation and edge/application layer;
- no command surface for KVK actuation;
- explicit error and degraded states.

### S4 — HMI prototype workflow
- dashboard counters;
- animal/session screen;
- limb/claw/zone selection;
- lesion classification entry;
- treatment/material entry;
- media placeholders and BEFORE/AFTER semantics;
- completion/follow-up flow.

### S5 — Reporting
- local PDF generation from committed canonical records;
- audience-oriented sections;
- synthetic/test media only.

### S6 — Simulated adapters
- simulated RFID input;
- simulated KVK observation events only;
- no live hardware I/O.

### S7 — Bench verification
- acceptance tests mapped to REQ-HC-001;
- restart/recovery tests;
- idempotency tests;
- ambiguous identity fail-closed tests;
- report provenance tests;
- verification evidence committed before closure.

## Explicitly out of scope
- live KVK I/O of any kind;
- writes/commands/configuration toward KVK;
- hydraulic control;
- PLC mutation;
- safety functions or safety dependency;
- autonomous veterinary diagnosis;
- production RFID/camera selection;
- production backup/retention policy;
- deployment, signing, release or public distribution.

## TDD rule
Each runtime slice SHALL begin with failing tests derived from REQ-HC-001 and LEL-HC-001, then minimal implementation, then refactor with regression coverage.

## Merge discipline
Every implementation slice SHALL use branch → Draft PR → CI/review → final exact-head Project Owner approval → controlled merge → post-merge verification.

## Entry gate
Satisfied by Project Owner approval and controlled merge of PR #8. `IA-HC-001` is active only within the bounded bench scope defined in that authority.
