# HC-P3-001 — Bench Wiring BOM

Status: IMPLEMENTED / GREEN — MERGE APPROVAL PENDING

Scope: isolated synthetic/test-only physical prototype bench under active `IA-HC-002`.

## Bench profile
- nominal supply: 24 VDC;
- 10.1-inch HMI;
- 8DI/8DO simulator I/O;
- DIN rail terminals and bench fuse protection;
- USB/RS-485 adapter permitted only for simulator/test-equipment use;
- momentary switches and indicator lamps for synthetic I/O stimulation.

## Isolation invariants
- no electrical or logical connection to the real KVK 801-1;
- no real-farm identity or animal data;
- no machine CAN/RS-485/Modbus/serial connection;
- no KVK commands, writes, configuration or actuation;
- no hydraulics, PLC or safety-chain integration.

This artifact is a prototype BOM/profile, not a procurement baseline and not a production wiring design.
