# IA-HC-004 — Wave R0 Remediation Authority v0.1

## Status
`PROPOSED / NOT ACTIVE — PROJECT OWNER APPROVAL REQUIRED`

## Purpose
Authorize only the bounded software/documentation remediation required to close the Wave R0 findings recorded by `HC-AUDIT-001` and planned by `IMP-HC-003`.

## Authorized scope after explicit activation
If activated by Project Owner approval of an exact PR head and controlled merge, IA-HC-004 permits:
- TDD changes to the local synthetic/test-only Python runtime and tests for AUD-HC-003 through AUD-HC-006;
- exact selected hardware profile/BOM representation for Kinco GL100E + Kinco KS123-14DR + existing isolated 24 VDC;
- implementation of a structurally valid local PDF renderer for synthetic/test data only;
- application-level durable-completion transaction semantics using only local test storage;
- removal of hard-coded acceptance PASS pathways and replacement with evidence-derived checks;
- deterministic GL100E application specification files, geometry, navigation manifest and KS123-14DR bench Modbus manifest, but not creation/claim of a native DTools artifact unless actually produced with DTools;
- documentation-only reconciliation for AUD-HC-015 through AUD-HC-017;
- an abstract `EDGE_HOST_REQUIRED` deployment contract while the concrete edge host remains unresolved;
- local tests and CI necessary to verify the above.

## Explicitly not authorized
IA-HC-004 does not authorize:
- choosing or purchasing an edge/application host on behalf of the Project Owner;
- claiming a native Kinco DTools project/export exists without tool-generated evidence;
- HW-A1 acceptance, HW-A2 power-up or HW-A3 physical upload by software evidence alone;
- live RFID or real farm/animal data;
- any electrical/logical connection to a real KVK 801-1;
- KVK CAN/RS485/Modbus/serial;
- KVK commands, writes, configuration or actuation;
- hydraulics, PLC or safety mutation;
- network/cloud exposure or external report delivery;
- deployment/provisioning to production, signing, release or public distribution.

## Safety invariants
- `kvk_connection_allowed = false` remains invariant for all R0 runtime paths.
- `real_farm_data_allowed = false` remains invariant.
- GL100E↔KS123-14DR Modbus definitions are test/bench-only and SHALL NOT be reusable as a machine bus route without later authority.
- Unknown or unresolved edge host state SHALL fail closed as `EDGE_HOST_REQUIRED / NOT DEPLOYMENT READY`.
- DTools native artifact state SHALL fail closed as `NATIVE_DTOOLS_ARTIFACT_REQUIRED` until real evidence exists.

## Authority termination
IA-HC-004 is fulfilled when Wave R0 is closed/reconciled or superseded by explicit Project Owner decision. It does not automatically activate any later field, real-data, deployment or KVK authority.
