# HC-R0-D-DOC-RECON-001 — Documentation and Lifecycle Reconciliation

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Purpose
Reconcile the authoritative project state after HC-AUDIT-001 and R0-A/R0-B/R0-C without changing previously approved technical content.

## Baselined upstream status
The following documents are already Project Owner-approved and are canonically `BASELINED`, even where their original frozen body still contains a historical pre-approval banner:
- FND-HC-001;
- ARS-HC-001;
- ARB-HC-001;
- ADR-HC-001 through ADR-HC-007;
- SA-HC-001;
- LEL-HC-001;
- REQ-HC-001.

This reconciliation record is the canonical status override for those historical proposal banners. It does not reopen or alter their approved technical content.

## Canonical lifecycle vocabulary
LEL-HC-001 is canonical for runtime lifecycle semantics:
- `NEW` = conceptual creation intent before Session materialization;
- `IDENTITY_PENDING`;
- `IN_PROGRESS`;
- `FOLLOW_UP_REQUIRED`;
- `COMPLETED`;
- `UNRESOLVED`;
- `CANCELLED`.

Where SA-HC-001 uses older vocabulary, compatibility is interpreted as:
- SA `ACTIVE` → LEL `IN_PROGRESS`;
- SA `INCOMPLETE` → non-terminal `IDENTITY_PENDING` or `IN_PROGRESS` depending on identity/workflow evidence;
- SA `VOIDED_WITH_AUDIT` → LEL `CANCELLED` plus audit record;
- conceptual SA `NEW` → pre-materialization intent.

No runtime state transition is added by this reconciliation.

## Hardware truth
The selected isolated bench target is now exactly:
- Kinco GL100E, 10.1 inch, 1024×600;
- Kinco KS123-14DR, 8 DI + 6 relay DO;
- existing isolated 24 VDC source, subject to physical verification;
- local RS485/Modbus RTU only between GL100E and KS123-14DR;
- RFID deferred.

The concrete edge/application runtime host remains unresolved as `EDGE_HOST_REQUIRED`. Canonical persistence/reporting SHALL NOT be silently moved into the GL100E.

## DTools truth
`GL100E-DTOOLS-SPEC-001` is a deterministic realization specification only.
A native Kinco DTools project/export remains `NATIVE_DTOOLS_ARTIFACT_REQUIRED` until actually generated and evidenced with the Kinco toolchain.

## Audit disposition after this change set
- AUD-HC-001: specification gap addressed; native artifact still physically/toolchain blocked before HW-A3 PASS.
- AUD-HC-002: architecture truth reconciled; concrete edge host intentionally unresolved and fail-closed.
- AUD-HC-003: corrected by R0-B.
- AUD-HC-004 / 005: corrected by R0-C.
- AUD-HC-006: corrected by R0-A.
- AUD-HC-015: canonical baseline status reconciled by this record and CURRENT_STATE/README/TRACE surfaces.
- AUD-HC-016: canonical lifecycle mapping established here.
- AUD-HC-017: requirement-level matrix established by HC-REQ-TRACE-001.

## Physical gates unchanged
- HW-A1 remains `WAITING FOR PHYSICAL HARDWARE`.
- HW-A2 remains not executed.
- HW-A3 remains not executed.
- no native DTools artifact is claimed.
- no edge deployment readiness is claimed.

## Authority boundary
No real KVK I/O, machine bus, commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, live RFID/real-farm data, network/cloud, deployment, signing, release or public distribution is authorized by this reconciliation.
