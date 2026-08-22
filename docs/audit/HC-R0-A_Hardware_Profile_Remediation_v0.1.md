# HC-R0-A — Hardware Profile Remediation v0.1

## Status
`CLOSURE READY — PROJECT OWNER MERGE APPROVAL REQUIRED`

## Audit finding
Addresses `AUD-HC-006` under active `IA-HC-004` and `IMP-HC-003`.

## TDD lineage
- RED final test head: `d054fd8cf722bde2b8f08e95dd05d83de35bbf93` — runtime-ci expected failure.
- GREEN implementation head: `d75313e42b5ebad8b2f4edfda2f106077bd85aad` — runtime-ci PASS / docs-ci PASS.

## Canonical selected bench profile
- HMI: `Kinco GL100E`;
- display: 10.1 inch class;
- nominal supply: 24 VDC;
- I/O: `Kinco KS123-14DR`;
- digital inputs: 8;
- digital outputs: 6 relay outputs;
- supply source: existing isolated 24 VDC, subject to physical HW-A1/HW-A2 verification;
- bench communications: `RS485 / Modbus RTU`;
- communications scope: `GL100E_TO_KS123_14DR_ONLY`;
- real KVK connectivity: forbidden;
- real farm data: forbidden.

## Truthfulness boundary
This remediation aligns source code, tests and BOM with the selected bench hardware. It does not claim physical receipt, power-up, wiring verification, native Kinco DTools artifact, edge-host deployment or any KVK connection.

## Result
`AUD-HC-006 = REMEDIATED / VERIFIED IN SOFTWARE — PENDING CONTROLLED MERGE`.
