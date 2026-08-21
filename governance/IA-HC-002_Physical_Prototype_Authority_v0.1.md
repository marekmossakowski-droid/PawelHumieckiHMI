# IA-HC-002 — Physical Prototype Authority v0.1

## Status
`PROPOSED — NOT ACTIVE — PROJECT OWNER APPROVAL REQUIRED`

## Purpose
Authorize the next bounded phase after bench MVP closure: physical HMI prototype work performed off-machine or on a non-actuating mock-up using synthetic/test data.

## Authorized only after explicit Project Owner approval
- procure and bench-power the selected 10-inch-class HMI and associated low-voltage bench accessories;
- implement and test the approved dashboard/workflow on physical HMI hardware or a directly attached local edge controller;
- use synthetic/test data and simulated RFID/KVK observation sources;
- validate touch targets, operator ergonomics, screen navigation, local persistence, local reporting and restart behavior;
- develop mounting/interface mock-ups based on measurements/photos of the actual KVK 801-1;
- perform low-voltage bench wiring that is electrically isolated from the KVK machine;
- test local serial/RS-485/Modbus only against dedicated simulators/test equipment, never the KVK machine;
- create verification records and BOM updates.

## Explicitly not authorized
- any electrical connection to the real KVK 801-1;
- live RFID hardware attached to real animal/farm identity data;
- live KVK I/O of any kind;
- CAN/RS-485/Modbus/serial connection to the KVK machine;
- machine commands, writes, configuration or actuation;
- hydraulics, valves, motors, gates, winches or other actuator control;
- PLC, safety relay, emergency-stop, guarding or safety-chain mutation;
- bypassing or depending on original KVK safety functions;
- real-farm operational data without separate authority;
- autonomous veterinary diagnosis or medication dosing;
- network/cloud service exposure;
- production deployment, signing, release or public distribution.

## Preconditions for later live KVK observation authority
A future live observation-only authority cannot be proposed as active until all of the following are available:
1. photographs of the actual circa-2013 KVK 801-1;
2. identification of electrical cabinet, controls, supply, sensors and interfaces;
3. wiring/schematic evidence where available;
4. verified physical/electrical isolation concept;
5. explicit source-of-truth signal inventory;
6. risk review confirming no effect on original machine safety;
7. a separately approved implementation plan and Project Owner authority.

## Fail-closed rule
If a prototype task could create an electrical, logical or mechanical path capable of influencing the real KVK machine, it is outside `IA-HC-002` and must not proceed without a new explicit authority decision.
