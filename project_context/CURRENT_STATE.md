# HoofCare — CURRENT STATE

## Naming status

`PawelHumieckiHMI` and `HoofCare` are internal engineering codenames only. They are not an approved commercial/product name. Final product name: `TBD — PROJECT OWNER DECISION REQUIRED`.

## Status

`F80 / BENCH IMPLEMENTATION — S1 DOMAIN/SESSION CORE IN PROGRESS`

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

## Current branch

`implementation/hc-s1-session-core`

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

`HC-S1-001 — Domain/session core`

TDD lineage:
- RED head: `52b4fca3ca719b035d2cc7c5091447c607b6fd83` — `runtime-ci` failed because `hoofcare` implementation did not yet exist;
- GREEN implementation introduced after RED and is verified by runtime CI on the active PR branch.

## S1 invariants

- new sessions start in `IDENTITY_PENDING`;
- ambiguous identity remains fail-closed and cannot bind animal history;
- confirmed identity moves the session to `IN_PROGRESS`;
- duplicate event IDs are idempotent;
- completion requires confirmed identity;
- completed/unresolved/cancelled sessions are terminal.

## Explicit blockers

- Physical KVK integration remains blocked until the actual machine is inspected and photographed.
- Commercial/product naming remains undecided.
