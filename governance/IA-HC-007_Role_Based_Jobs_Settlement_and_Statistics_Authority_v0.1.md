# IA-HC-007 — Role-Based Jobs, Settlement and Statistics Authority v0.1

## Status

`PROPOSED / NOT ACTIVE — PROJECT OWNER APPROVAL REQUIRED`

## Proposed authorized scope

Bounded local synthetic/test-only implementation of `UX-HC-001` and `REQ-HC-002` according to `ADR-HC-008` and `IMP-UX-HC-001`.

If separately approved and activated, permitted changes are limited to:

- local job/pricing/material/settlement domain models;
- integer-grosz PLN calculations and decimal quantities;
- job price snapshots and job-local additional materials;
- durable local synthetic job persistence and audit records;
- completed-cow/material counters derived from committed local records;
- role-aware synthetic menu/view models and 1024×600 geometry tests;
- navigation labels for future controls/clinical areas without implementing their runtime behavior;
- operator/owner statistics derived from local synthetic records;
- local synthetic settlement summary and PDF clearly marked as not an invoice;
- tests, CI checks, documentation and traceability required for this scope.

## Mandatory constraints

- TDD is required for every runtime increment: clean assertion RED → minimal GREEN → full regression.
- Prices are stored as integer grosze; monetary calculation cannot use binary `float`.
- Completed-cow counts derive only from unique durably committed completed sessions.
- Price/catalog changes cannot silently recalculate historical jobs.
- Closed settlements are immutable; corrections are outside this authority.
- Owner and operator surfaces remain explicitly separated.
- All fixtures and demonstrations remain synthetic/test-only.

## Explicit exclusions

This proposed authority does not authorize:

- real-farm, real-client, real-animal, real-operator or real-price data;
- live RFID or physical camera/device access;
- real KVK I/O or machine CAN/RS485/Modbus/serial;
- commands, writes, configuration, actuation, hydraulics or PLC/safety mutation;
- network/cloud, external report delivery or remote access;
- invoicing, VAT calculation, fiscal documents, accounting, payments or payment-provider integration;
- production authentication or credential deployment;
- settlement correction workflows and clinical/control analytics;
- physical edge-host selection/deployment;
- DTools upload, HW-A1/HW-A2/HW-A3 PASS;
- deployment, provisioning, signing, release or public distribution;
- merge or default-branch mutation without separate exact-head approval.

## Fail-closed rule

Any requirement for real identities/data, external connectivity, financial system integration, device access, machine effect or production credentials is outside this authority and must stop for a separate Project Owner decision.

## Proposed activation condition

`IA-HC-007` may become active only after:

1. Project Owner explicitly approves this exact authority content and its exact repository head;
2. the approved authority artifact is merged through expected-head protection;
3. Repository Verification confirms the exact merge on canonical `main`;
4. canonical traceability records `IA-HC-007 = APPROVED / ACTIVE` prospectively.

No chat instruction or generic autonomy statement alone activates this authority.

## Completion condition

Authority may be marked fulfilled only after all `REQ-HC-002` requirements have traceable automated evidence, all approved implementation PRs are merged and Repository Verification passes, while real-data, device, deployment and financial-system boundaries remain closed.
