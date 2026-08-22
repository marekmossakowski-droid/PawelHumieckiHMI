# IMP-HC-003 — Wave R0 Remediation Plan v0.1

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Purpose
Close the audit Wave R0 findings from `HC-AUDIT-001` before the first truthful GL100E application test.

## Scope
This plan covers only AUD-HC-001 through AUD-HC-006 and AUD-HC-015 through AUD-HC-017. No real KVK integration is included.

## R0-A — Truthful hardware profile
Replace generic 10-inch / 8DI-8DO assumptions with the selected isolated bench target: Kinco GL100E 10.1 inch / 1024x600 / nominal 24 VDC, Kinco KS123-14DR 8 DI + 6 relay DO, existing isolated 24 VDC source subject to physical verification, RFID deferred, and local RS485/Modbus RTU only between GL100E and KS123-14DR.

## R0-B — Edge/application runtime host decision
Canonical persistence/reporting remains outside the replaceable HMI. Until a dedicated bench edge host is separately selected and approved, implementation may define an `EDGE_HOST_REQUIRED` runtime/deployment contract but SHALL NOT claim physical edge deployment readiness or move canonical durable ownership into the GL100E.

## R0-C — Valid PDF renderer
Replace the PDF-like text output with a deterministic structurally valid local PDF containing header, indirect objects, page tree, content stream, xref, trailer, startxref and EOF, with provenance, synthetic-test-only marker and clinical disclaimer. Tests SHALL verify structure beyond the magic prefix.

## R0-D — Durable completion transaction boundary
A session completion acknowledgement SHALL only be returned after canonical persistence succeeds. Persistence failure SHALL fail closed and SHALL NOT present completion as durable.

## R0-E — Truthful end-to-end acceptance
Remove hard-coded PASS values. Acceptance SHALL derive PASS from identity evidence, workflow state, durable completion, canonical recovery, committed-source report generation, explicit negative capability checks and synthetic-only invariants.

## R0-F — GL100E/DTools deployability package
Create a deterministic in-repo GL100E application specification package containing exact 1024x600 screens, widget IDs, labels, bindings, actions, x/y/width/height, navigation table, KS123-14DR Modbus manifest, DTools realization checklist and artifact acceptance criteria.

A native DTools project/export SHALL remain `REQUIRED BEFORE HW-A3 PASS`; the repository SHALL NOT claim that native artifact exists until it is actually created/exported with the Kinco toolchain.

## R0-G — Documentation and lifecycle reconciliation
Reconcile FND/ARS/ARB/SA/LEL/REQ/README status banners to actual approved/baselined state without changing approved technical content. LEL vocabulary is canonical: NEW (conceptual creation intent), IDENTITY_PENDING, IN_PROGRESS, FOLLOW_UP_REQUIRED, COMPLETED, UNRESOLVED, CANCELLED. The code may materialize a new Session directly as IDENTITY_PENDING; documentation shall map conceptual NEW to pre-materialization creation intent.

## R0-H — Requirement-level traceability
Create a matrix for each `REQ-HC-*` requirement with implementation evidence, automated test evidence, status IMPLEMENTED/PARTIAL/DEFERRED/BLOCKED and authority/workstream.

## Execution sequence
1. R0 governance/authority activation.
2. RED tests.
3. GREEN runtime changes.
4. GL100E specification package.
5. documentation/lifecycle reconciliation.
6. requirement-level trace matrix.
7. full runtime-ci/docs-ci.
8. R0 closure-readiness.

## Exit criteria
Wave R0 closes only when technical P0/P1 fixes are verified, documentation is truthful, the GL100E specification package exists, native DTools and edge-host physical deployment remain explicitly blocked unless separately evidenced/approved, and no KVK/safety/real-data boundary is expanded.
