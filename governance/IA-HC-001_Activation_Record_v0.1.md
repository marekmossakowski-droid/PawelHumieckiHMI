# IA-HC-001 — Activation Record v0.1

## Status
`PENDING PROJECT OWNER APPROVAL`

## Activation condition
`IA-HC-001 — Initial Implementation Authority v0.1` becomes `ACTIVE` only when the Project Owner explicitly approves the exact final head of the pull request containing this activation record and authorizes controlled merge to `main`.

## Activated scope
Activation permits only the bounded bench-MVP scope already defined in `IA-HC-001` and `IMP-HC-001`:
- local synthetic/test-only runtime implementation;
- domain/session core;
- local persistence and restart recovery;
- local HMI/edge contract;
- HMI prototype workflow;
- local PDF reporting;
- simulated RFID input;
- simulated KVK observation events;
- automated tests and verification evidence.

## Exclusions remain absolute
Activation does NOT authorize:
- live KVK I/O of any kind;
- KVK commands, writes or configuration changes;
- hydraulic, gate, strap, winch or lift control;
- PLC or safety mutation;
- autonomous veterinary diagnosis;
- medication dosing or automatic treatment execution;
- production deployment, signing, release or public distribution;
- real-farm data processing beyond a separately approved data/privacy boundary.

## Effect of approved merge
After the activation condition is satisfied and the exact approved PR is merged, `IA-HC-001` is considered `ACTIVE` for the bounded bench-MVP scope without further approval. Post-merge reconciliation shall record the approved head and merge SHA before or together with the first runtime implementation slice.
