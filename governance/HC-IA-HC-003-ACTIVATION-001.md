# HC-IA-HC-003-ACTIVATION-001 — Activation record

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Purpose
Aktywacja `IA-HC-003 — Isolated Bench Hardware Assembly Authority v0.1` wyłącznie dla izolowanego bench hardware opisanego przez `IMP-HC-002`.

## Preconditions verified before owner gate
- `PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`;
- `IA-HC-002 = FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE`;
- `IMP-HC-002 = PROPOSED / NOT ACTIVE`;
- `IA-HC-003 = PROPOSED / NOT ACTIVE`;
- selected hardware target: `Kinco GL100E + Kinco KS123-14DR`;
- existing isolated 24 VDC source is available;
- RFID remains deferred;
- `field_kvk_verified = false`, `real_farm_data_used = false`, `deployment_ready = false`.

## Activation effect if approved
After Project Owner exact-head approval, controlled merge and Repository Verification:
- `IMP-HC-002 = APPROVED / ACTIVE`;
- `IA-HC-003 = APPROVED / ACTIVE`;
- authorized execution may begin only at `HW-A1 — Goods-in verification` and proceed through `HW-A7 — Bench acceptance` in order;
- all work remains isolated, synthetic/test-only and off-machine.

## Authorized hardware boundary
- `Kinco GL100E`;
- `Kinco KS123-14DR`;
- existing isolated 24 VDC bench source;
- passive wiring, terminals, protection, dedicated test buttons/contacts/lamps/test loads;
- local engineering computer for configuration/evidence.

## Explicit exclusions
No real KVK I/O; no connection to KVK PLC, safety relay, sensors, actuators, cabinet terminals or machine buses; no CAN/RS485/Modbus/serial to KVK; no KVK commands/writes/configuration/actuation; no hydraulics; no PLC/safety mutation; no live RFID/real-farm data; no network/cloud; no external report delivery; no deployment/signing/release/public distribution.

## Fail-closed rule
Any planned connection or action capable of influencing the real KVK machine, using real-farm operational data, or leaving the isolated bench boundary is outside `IA-HC-003` and must stop before connection or execution.

## Owner gate
This record does not activate anything by publication alone. Activation requires explicit Project Owner approval of the exact PR head that contains this record.
