# IA-HC-003 — Isolated Bench Hardware Assembly Authority v0.1

## Status
`PROPOSED / NOT ACTIVE — PROJECT OWNER APPROVAL REQUIRED`

## Purpose
Authorize only the isolated physical assembly and bench verification described by `IMP-HC-002`, using dedicated test equipment and synthetic/test data, with no electrical, logical or mechanical path to the real KVK 801-1.

## Authorized bounded scope if activated
- receive and inspect the selected Kinco GL100E HMI and Kinco KS123-14DR I/O module;
- use the Project Owner's existing 24 VDC supply for isolated bench work after polarity/voltage verification;
- power and configure GL100E on the bench;
- load the approved synthetic/test HMI project;
- connect GL100E to KS123-14DR over local RS485/Modbus RTU;
- attach only dedicated test buttons, test contacts, lamps or equivalent non-machine test loads;
- read DI and exercise relay DO only against those dedicated bench test loads;
- validate touch workflow, navigation, local persistence, restart and local PDF reporting;
- make minimal software/configuration corrections required solely for this exact bench hardware profile, test-first and fail-closed;
- create photos, wiring diagrams, configuration snapshots and verification records that contain no real-farm data.

## Hardware boundary
Allowed hardware set for this authority:
- `Kinco GL100E`;
- `Kinco KS123-14DR`;
- existing isolated 24 VDC bench source;
- passive wiring, terminals, fusing/protection and dedicated test buttons/lamps/test loads;
- local engineering computer required to configure the HMI or capture evidence.

RFID is explicitly deferred and not authorized under this authority.

## Explicitly not authorized
- any electrical or logical connection to the actual KVK 801-1;
- any connection to KVK PLC, safety relay, sensors, actuators, cabinet terminals or machine communication buses;
- CAN/RS485/Modbus/serial to the KVK machine;
- KVK commands, writes, configuration or actuation;
- hydraulics, valves, motors, gates, winches, lifting or restraint control;
- PLC/safety mutation, safety-chain bypass or dependency;
- live RFID or real animal/farm identity data;
- autonomous veterinary diagnosis or medication dosing;
- network/cloud service exposure;
- external report delivery;
- production deployment, signing, release or public distribution.

## Fail-closed rule
If any planned wire, protocol endpoint, test load, software action or physical setup could influence the real KVK machine or use real-farm operational data, the action is outside `IA-HC-003` and must stop before connection or execution.

## Completion condition
`IA-HC-003` is fulfilled only after `HW-A1` through `HW-A7` of `IMP-HC-002` are completed, evidence is reconciled, and the isolated bench hardware is verified with `kvk_connected = false` and `real_farm_data_used = false`.

## Activation rule
Publication or merge of this document does not activate the authority unless the Project Owner's exact-head approval explicitly states that `IA-HC-003` is activated after controlled merge and Repository Verification.
