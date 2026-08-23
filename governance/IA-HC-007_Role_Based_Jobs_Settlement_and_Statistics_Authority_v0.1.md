# IA-HC-007 — Role-Based Jobs, Settlement and Statistics Authority v0.1

## Status

`APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-ACTIVATION-001`

## Authorized scope

Bounded local synthetic/test-only implementation of `UX-HC-001` and `REQ-HC-002` according to `ADR-HC-008` and `IMP-UX-HC-001`.

Permitted changes are limited to:

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

This authority does not authorize:

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

## Activation evidence

Project Owner zatwierdził exact head PR #80 `8901922380a3ec342747088e5acccdcd4ca5b44d` oraz prospektywną aktywację po Repository Verification. Kontrolowany merge utworzył `3a32e3b5b7d1f5b2693836c044ef73caa63276d3`; canonical `main`, rodzice, tree `fa8d5e3bdf1d71087b12472d8a649f6685ac6632` i pełne kontrole zostały zweryfikowane. Szczegóły utrwala `HC-IA-HC-007-ACTIVATION-001` i post-merge reconciliation.

## Completion condition

Authority may be marked fulfilled only after all `REQ-HC-002` requirements have traceable automated evidence, all approved implementation PRs are merged and Repository Verification passes, while real-data, device, deployment and financial-system boundaries remain closed.
