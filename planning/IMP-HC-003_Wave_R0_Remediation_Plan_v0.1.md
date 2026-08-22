# IMP-HC-003 — Wave R0 Remediation Plan v0.1

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Purpose
Close the audit Wave R0 findings from `HC-AUDIT-001` before the first truthful GL100E application test.

## Scope
This plan covers only:
- AUD-HC-001 — GL100E/DTools deployability artifact;
- AUD-HC-002 — bench edge/application runtime host decision and boundary;
- AUD-HC-003 — structurally valid local PDF generation;
- AUD-HC-004 — truthful canonical end-to-end acceptance;
- AUD-HC-005 — durable completion semantics;
- AUD-HC-006 — exact GL100E + KS123-14DR hardware profile/BOM;
- AUD-HC-015 — documentation status reconciliation;
- AUD-HC-016 — lifecycle vocabulary reconciliation;
- AUD-HC-017 — requirement-level traceability.

No real KVK integration is included.

## R0-A — Truthful hardware profile
Replace generic 10-inch / 8DI-8DO assumptions with the selected isolated bench target:
- HMI: Kinco GL100E, 10.1 inch, 1024x600, nominal 24 VDC bench supply;
- I/O: Kinco KS123-14DR, 8 DI, 6 relay DO;
- supply: existing isolated 24 VDC source, subject to HW-A1/HW-A2 physical verification;
- RFID: deferred;
- RS485/Modbus RTU: local bench link only between GL100E and KS123-14DR.

TDD: RED exact-profile tests → GREEN source/BOM → reconciliation.

## R0-B — Edge/application runtime host decision
The baselined architecture requires canonical persistence/reporting outside the replaceable HMI. R0 therefore SHALL NOT falsely move durable canonical ownership into the GL100E.

Before runtime deployment, a dedicated bench edge host must be selected and baselined. Until that decision is approved, implementation may define an abstract `EDGE_HOST_REQUIRED` deployment profile and reproducible runtime contract, but SHALL NOT claim physical edge deployment readiness.

Owner decision candidates remain downstream and are not selected by this plan. Examples may include a small Linux SBC/IPC or an existing isolated development computer used only as bench edge host.

## R0-C — Valid PDF renderer
Replace PDF-like text output with a deterministic, structurally valid local PDF byte stream containing:
- PDF header;
- indirect objects;
- page tree;
- content stream;
- xref table;
- trailer/startxref/EOF;
- report provenance text;
- synthetic-test-only marker and clinical disclaimer.

Tests SHALL validate structure beyond the magic prefix and reject the former pseudo-PDF representation.

## R0-D — Durable completion transaction boundary
Introduce an application-level durable completion operation. A session completion acknowledgement SHALL be returned only after canonical persistence succeeds. Persistence failure SHALL keep completion unacknowledged/fail closed.

The physical acceptance harness SHALL use this boundary rather than applying `COMPLETE` first and persisting later.

## R0-E — Truthful end-to-end acceptance
Acceptance SHALL derive PASS from evidence. Remove hard-coded `end_to_end=PASS` and `no_kvk_actuation_surface=PASS` pathways.

Required evidence:
- identity resolved from adapter evidence;
- workflow selections recorded;
- session durably completed through the transaction boundary;
- canonical session recovered from store;
- report generated from the committed session;
- explicit exported-surface negative test proving no KVK actuation API;
- synthetic-only and no-real-farm-data invariants.

## R0-F — GL100E/DTools deployability package
Because a native DTools binary project cannot be honestly fabricated without the DTools toolchain and physical/tool verification, R0 SHALL create a deterministic `GL100E application specification package` in-repo containing:
- exact 1024x600 screen list;
- widget IDs, labels, bindings, actions, x/y/width/height;
- navigation table;
- Modbus tag/address manifest for KS123-14DR bench I/O;
- DTools realization checklist and artifact acceptance criteria;
- version/provenance metadata.

The native DTools project/export itself remains `REQUIRED BEFORE HW-A3 PASS` and must be imported/exported with the actual Kinco toolchain. The repository SHALL NOT claim a native DTools artifact exists until evidence is available.

## R0-G — Documentation and lifecycle reconciliation
Reconcile FND/ARS/ARB/SA/LEL/REQ/README status banners to their actual approved/baselined state without changing approved technical content.

Select the LEL lifecycle vocabulary as canonical for current implementation:
`NEW` (creation intent / pre-materialization concept), `IDENTITY_PENDING`, `IN_PROGRESS`, `FOLLOW_UP_REQUIRED`, `COMPLETED`, `UNRESOLVED`, `CANCELLED`.

Code may continue to materialize a new Session directly as `IDENTITY_PENDING`; documentation SHALL explicitly map conceptual `NEW` to session creation before the first durable/materialized state.

## R0-H — Requirement-level traceability
Create a matrix mapping each `REQ-HC-*` requirement to:
- implementation evidence;
- automated test evidence;
- status: IMPLEMENTED / PARTIAL / DEFERRED / BLOCKED;
- authority/workstream.

No requirement may be upgraded to IMPLEMENTED solely because a slice-level PR exists.

## Execution sequence
1. R0 governance/authority activation.
2. RED tests for exact hardware profile, PDF structure, durable completion and acceptance integrity.
3. GREEN runtime changes.
4. GL100E application specification package.
5. documentation/lifecycle reconciliation.
6. requirement-level trace matrix.
7. full runtime-ci/docs-ci.
8. final R0 closure-readiness PR.

## Exit criteria
Wave R0 can close only when:
- AUD-HC-003/004/005/006 are technically fixed and tested;
- AUD-HC-015/016/017 are reconciled;
- a truthful GL100E application specification exists;
- native DTools artifact remains explicitly blocked until created with DTools;
- edge host remains explicitly unresolved unless separately approved;
- no false claim of HW-A1/HW-A2/HW-A3 completion is made;
- all current KVK/safety/real-data exclusions remain intact.
