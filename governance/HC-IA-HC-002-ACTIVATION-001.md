# HC-IA-HC-002-ACTIVATION-001 — Physical Prototype Authority Activation Decision

## Status
`PROPOSED — PROJECT OWNER EXACT-HEAD APPROVAL REQUIRED`

## Purpose
Materialize the explicit Project Owner decision required to activate `IA-HC-002 — Physical Prototype Authority v0.1` after verified Bench MVP closure.

## Effect upon controlled merge of the exact Project Owner-approved head
- `HC-BENCH-MVP-CLOSURE-001 = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`;
- `IMP-HC-001 = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`;
- `IA-HC-001 = FULFILLED FOR AUTHORIZED BENCH SCOPE`;
- `IA-HC-002 = APPROVED / ACTIVE` only for the literal bounded physical-prototype scope defined in `governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md`.

## Authorized bounded physical-prototype scope after activation
- off-machine or non-actuating mock-up work only;
- selected 10-inch-class HMI and associated low-voltage bench accessories;
- synthetic/test data and simulated RFID/KVK observation sources;
- physical HMI dashboard/workflow, touch-target, navigation, local persistence, local reporting and restart validation;
- mounting/interface mock-ups based on measurements/photos;
- low-voltage bench wiring electrically isolated from the KVK machine;
- serial/RS-485/Modbus testing only against dedicated simulators/test equipment;
- verification records and BOM updates.

## Explicit exclusions remain closed
Activation does not authorize:
- any electrical or logical connection to the real KVK 801-1;
- live RFID with real animal/farm identity data;
- live KVK I/O;
- CAN/RS-485/Modbus/serial connection to the KVK machine;
- machine commands, writes, configuration or actuation;
- hydraulics, valves, motors, gates, winches or other actuator control;
- PLC, safety relay, E-STOP, guarding or safety-chain mutation;
- real-farm operational data;
- autonomous veterinary diagnosis or medication dosing;
- network/cloud service exposure;
- deployment, signing, release or public distribution.

## Fail-closed rule
If any task could create an electrical, logical or mechanical path capable of influencing the real KVK machine, or would use real-farm data, it remains outside `IA-HC-002` and must not proceed without a new explicit authority decision.

## Activation rule
This document does not activate `IA-HC-002` merely by existing on a branch or in an open PR. Activation occurs only after explicit Project Owner approval of the final exact head and controlled merge of that exact approved head to `main`, followed by Repository Verification.
