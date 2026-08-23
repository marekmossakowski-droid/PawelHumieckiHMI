# IA-HC-007-S1 — Job Statistics and Final Settlement Authority v0.1

## Status

`PROPOSED / NOT ACTIVE — PROJECT OWNER APPROVAL REQUIRED`

## Prospective scope

If separately approved, merged and activated after Repository Verification,
this authority MAY permit only local synthetic/test-only implementation of
`REQ-HC-002-S1 v0.1`:

- durable completed-cow counts derived from committed session links;
- additional-material quantities derived from committed usage records;
- statistics filtered by operator, synthetic farm, date range and job state;
- closed-job net totals derived from immutable historical settlement snapshots;
- deterministic `RAZEM NETTO` summary in integer grosz PLN;
- deterministic local PDF explicitly marked as not an invoice;
- presentation-only Generation 1 HMI models for counters and final summary;
- tests, local fixtures, documentation and traceability for this slice.

## Mandatory constraints

- Every runtime increment follows clean assertion RED → remote RED checkpoint → minimal GREEN → full regression.
- Counts have one source of truth: unique durable `COMPLETED` session assignments.
- Statistics are derived read-only views; no second mutable counter store is permitted.
- Historical totals use stored job pricing and settlement snapshots, not the current catalogue.
- Monetary values are integer grosz; material arithmetic uses `Decimal`, never binary `float`.
- Standard materials included in the cow rate are never charged a second time.
- A persistence failure propagates fail-closed and leaves the previous durable snapshot valid.
- All data and demonstrations remain local synthetic/test-only.

## Explicit exclusions

This proposal does not authorize real data; Generation 2 clients; closed
settlement correction; invoicing, VAT, fiscal documents, accounting or
payments; network/cloud or synchronization; live RFID, camera, device access,
KVK or machine I/O; commands, actuation, hydraulics or PLC/safety mutation;
production authentication; deployment, provisioning, signing, release or
public distribution; or merge/default-branch mutation without separate
exact-head approval.

## Activation gate

Runtime remains forbidden until all of the following occur:

1. Project Owner approves `REQ-HC-002-S1` content and exact final package head;
2. controlled merge uses expected-head protection;
3. Repository Verification passes on the exact merge tree;
4. a separate canonical activation record establishes `IA-HC-007-S1 = APPROVED / ACTIVE` prospectively;
5. the first runtime increment starts with its own clean assertion RED.

## Current effect

None. This document is a proposal and grants no implementation authority.

