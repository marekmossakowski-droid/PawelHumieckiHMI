# HoofCare — CURRENT STATE

## Naming status

`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. They are not an approved commercial/product name. Final product name: `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status

`F80 / BENCH IMPLEMENTATION — S2 DURABLE LOCAL PERSISTENCE IN PROGRESS`

## Canonical repository

`marekmossakowski-droid/PawelHumieckiHMI`

## Canonical main checkpoints

- `HC-FOUNDATION-001`: PR #1 merged as `de68522e4851f645d65dee7dda08ef8fed6af955`.
- `HC-ARS-001`: PR #2 merged as `b0286b73b90c95f05b1d99ef58ac9a9fae197880`.
- `HC-ARB-001`: PR #3 merged as `9144a6a003f58ea12c5a6c3d4ff26c26527d0292`.
- `HC-ADR-SET-001`: PR #4 merged as `c2493ef39a1b45b934cd2dc001279db110a17fc0`.
- `HC-SYSTEM-ARCH-001`: PR #5 merged as `5a0761dec9dbbca538be787839d93017f5c501df`.
- `HC-LEL-001`: PR #6 merged as `a7d031317cf25934218cd09a4916449f2bf5b634`.
- `HC-REQ-001`: PR #7 merged as `e34e2a2ae3f709d83c24d528f8930b1b72060961`.
- `HC-IMP-001` + `IA-HC-001` activation: PR #8 approved head `9c939abea6794e2b5a4815c826410eb0166ab535`, merged as `0d58eb2921df298114c304295a061547598ae541`.
- `HC-S1-001 — Domain/session core`: PR #9 approved head `5f6015bc2fd8e949851fac4e1e9d61184e8da4ff`, merged as `7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2`.

## Current branch

`implementation/hc-s2-persistence`

## Product baseline

- Product identity: not commercially named; current identifiers are codenames only.
- First target machine: KVK 801-1, generation circa 2013, older green construction.
- Current hardware candidate for bench MVP: Kinco GL100E 10.1"; candidate only, not baseline.
- Physical machine audit: `BLOCKED_BY_SITE_ACCESS` until access to the actual chute is available.

## Governance state

- Foundation through REQ-HC-001: `BASELINED`.
- `IMP-HC-001`: `APPROVED / BASELINED` by PR #8.
- `IA-HC-001`: `ACTIVE` for bounded local bench MVP only.
- Runtime implementation authority: `ESTABLISHED — BOUNDED BENCH ONLY`.
- `HC-S1-001`: `MERGED / VERIFIED`.
- `HC-S2-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`.

## Active authority boundaries

Authorized:
- synthetic/test data;
- domain/session core;
- local persistence and restart recovery;
- local HMI↔edge contract;
- HMI prototype workflow;
- local PDF reporting;
- simulated RFID;
- simulated KVK observation events;
- automated tests and verification.

Not authorized:
- live KVK I/O of any kind;
- KVK commands/writes/configuration;
- hydraulics or actuation;
- PLC or safety mutation;
- autonomous veterinary diagnosis;
- medication dosing;
- production deployment/signing/release/public distribution;
- real farm data without separate data/privacy authority.

## Current workstream

`HC-S2-001 — Durable local persistence and restart recovery`

TDD lineage:
- RED head: `cbb35f593173aea2bb2fc1d77e1c6f267217eb01` — persistence/recovery tests precede the store implementation and `runtime-ci` failed;
- GREEN head: `6a1a6c205ce486fcf397ce2c5a2c239873a3154b` — `runtime-ci` and `docs-ci` both succeeded.

## S2 invariants

- canonical session snapshots are stored outside HMI state;
- non-terminal sessions can be reconstructed after process restart;
- snapshot replacement is atomic within the local filesystem boundary;
- amendment records are append-only and ordered;
- corrupt snapshots fail closed rather than producing a partial session;
- missing sessions are explicit errors;
- persistence remains local and synthetic/test-only under current authority.

## Next dependency-ordered step

After controlled merge and repository verification of `HC-S2-001`, begin `S3 — local bench API / HMI contract` autonomously under active `IA-HC-001`.

## Explicit blockers

- Physical KVK integration remains blocked until the actual machine is inspected and photographed.
- Commercial/product naming remains undecided.
