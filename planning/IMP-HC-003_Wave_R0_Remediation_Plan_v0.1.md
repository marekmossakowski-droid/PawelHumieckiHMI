# IMP-HC-003 — Wave R0 Remediation Plan v0.1

## Status
`FULFILLED FOR AUTHORIZED R0 SCOPE — CLOSURE PENDING OWNER MERGE`

## Purpose
Close the audit Wave R0 findings from `HC-AUDIT-001` before the first truthful GL100E application test.

## Scope
This plan covers only AUD-HC-001 through AUD-HC-006 and AUD-HC-015 through AUD-HC-017. No real KVK integration is included.

## Completed remediation
- R0-A: truthful hardware profile for Kinco GL100E + KS123-14DR, existing isolated 24 VDC, RFID deferred.
- R0-B: structurally valid deterministic local PDF renderer.
- R0-C: durable completion transaction boundary and evidence-derived acceptance.
- R0-D: `GL100E-DTOOLS-SPEC-001`, `HC-REQ-TRACE-001`, lifecycle/documentation reconciliation.

## Explicit unresolved dependencies
- concrete edge/application host remains `EDGE_HOST_REQUIRED / NOT YET SELECTED`;
- native Kinco DTools project/export remains `NATIVE_DTOOLS_ARTIFACT_REQUIRED / NOT YET EVIDENCED`;
- HW-A1 remains `WAITING FOR PHYSICAL HARDWARE`;
- HW-A2/HW-A3 remain not started/not passed;
- requirement-level PARTIAL/DEFERRED/BLOCKED items remain open;
- R1/R2 findings remain outside this closure.

## Closure criteria
The technical/software/documentation scope authorized by `IA-HC-004` is satisfied. Final closure requires controlled merge of `HC-R0-CLOSURE-001` and Repository Verification.

## Authority boundary
No real KVK integration, machine bus, actuation, hydraulics, PLC/safety mutation, live RFID/real-farm data, network/cloud, deployment, signing, release or public distribution is authorized.
