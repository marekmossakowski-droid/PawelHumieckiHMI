# HC-IA-HC-002-ACTIVATION-001 — Physical Prototype Authority Activation Decision

## Status
`APPROVED / MERGED / REPOSITORY VERIFIED`

Project Owner approved exact head `3a3623d82a879c2b1b4ac3ce70f3d687b8e13710`; controlled merge completed as `3eb278f7a480734045027393a53a76f6cdc03f03`.

## Effect
- `HC-BENCH-MVP-CLOSURE-001 = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`;
- `IMP-HC-001 = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`;
- `IA-HC-001 = FULFILLED FOR AUTHORIZED BENCH SCOPE`;
- `IA-HC-002 = APPROVED / ACTIVE` only for the literal bounded physical-prototype scope defined in `governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md`.

## Authorized bounded physical-prototype scope
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
