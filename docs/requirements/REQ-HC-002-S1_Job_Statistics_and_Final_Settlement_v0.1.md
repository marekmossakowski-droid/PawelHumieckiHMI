# REQ-HC-002-S1 — Job Statistics and Final Settlement v0.1

## Status

`APPROVED / BASELINED — PROJECT OWNER APPROVED VIA PR #94; ACTIVATION RECORDED BY HC-IA-HC-007-S1-ACTIVATION-001`

## Purpose

This bounded slice refines `REQ-HC-002` for local synthetic/test-only job
statistics and the final net settlement summary. It adds no accounting,
invoicing, payment or remote-client behavior.

## Requirements

### REQ-HC-JOB-STAT-S1-001 — Durable cow count

Daily and job cow counts SHALL derive only from unique, durably assigned
`COMPLETED` sessions. Drafts, cancellations, failed persistence, retries and
duplicate events SHALL NOT increment a count.

### REQ-HC-JOB-STAT-S1-002 — Additional-material totals

Material statistics SHALL derive from durable job usage records and SHALL
preserve each material code, unit and declared decimal precision. Standard
materials included in the cow rate SHALL NOT create separate charge lines.

### REQ-HC-JOB-STAT-S1-003 — Filters

Statistics SHALL support inclusive date range, operator, synthetic farm and
job-state filters. An operator view SHALL NOT expose another operator's jobs;
the owner aggregate remains a separate presentation surface.

### REQ-HC-JOB-STAT-S1-004 — Historical provenance

Counts, material quantities and monetary totals SHALL derive from durable job
records and stored settlement snapshots, never the current catalogue or
transient presentation state.

### REQ-HC-JOB-CLOSE-S1-001 — Closing gate

A job SHALL NOT close while a session is active or unresolved, a durable write
is unconfirmed, required pricing/unit data is absent, or the total is not
deterministic.

### REQ-HC-JOB-CLOSE-S1-002 — Net summary

The closed summary SHALL show cow quantity and rate, every separately charged
additional material, quantities, unit net prices, line net values and a
dominant `RAZEM NETTO: X XXX,XX zł`.

### REQ-HC-JOB-CLOSE-S1-003 — Stored settlement

Closure SHALL persist an immutable settlement identifier, timezone-aware
timestamp, operator, line snapshot and integer-grosz total before reporting
success. Restart SHALL reproduce the same result without recalculation.

### REQ-HC-JOB-CLOSE-S1-004 — Local document

The system MAY generate a deterministic local PDF summary clearly marked
`DOKUMENT ROZLICZENIOWY — NIE JEST FAKTURĄ`. It SHALL contain no VAT, payment,
fiscal or accounting semantics.

## Verification gates

Each runtime increment requires clean assertion RED, remote test-only
checkpoint, minimal GREEN, targeted tests, full regression, Draft PR and
separate exact-head owner approval before merge.

## Explicit exclusions

No real farm/client/operator/animal/price/material data; no Generation 2
clients; no correction of a closed settlement; no network/cloud,
synchronization, device/camera/RFID/KVK/machine I/O, control, hydraulics or
PLC/safety mutation; no invoicing, VAT, accounting, payments, production
authentication, deployment, signing, release or public distribution.
