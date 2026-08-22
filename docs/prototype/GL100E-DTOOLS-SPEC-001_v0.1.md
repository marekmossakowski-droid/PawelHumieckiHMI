# GL100E-DTOOLS-SPEC-001 — Kinco GL100E DTools Realization Specification v0.1

## Status
`SPECIFICATION READY / NATIVE DTOOLS ARTIFACT REQUIRED BEFORE HW-A3 PASS`

## Scope
This is the deterministic realization specification for the selected isolated bench HMI `Kinco GL100E`, 10.1 inch, 1024×600. It is not a native Kinco DTools project/export and SHALL NOT be represented as one.

## Safety / authority boundary
- synthetic/test data only;
- no KVK connection;
- no machine-control action;
- local bench RS485/Modbus RTU only between GL100E and KS123-14DR;
- edge/application durable owner remains separate and currently `EDGE_HOST_REQUIRED`;
- HW-A1/HW-A2/HW-A3 remain physical gates.

## Global screen geometry
Canvas: `1024×600`.
Reserved header: `x=0 y=0 w=1024 h=64`.
Reserved footer/navigation: `x=0 y=536 w=1024 h=64`.
Content region: `x=24 y=80 w=976 h=440`.
Primary touch target minimum: `64×64`.
Preferred spacing between primary targets: `>=16 px`.

## Screen map
| Screen | DTools screen ID | Purpose |
|---|---:|---|
| DASHBOARD | 10 | start session, counters, reports entry |
| ANIMAL_SESSION | 20 | animal identity confirmation/cancel |
| LIMB_CLAW | 30 | limb and claw selection |
| ZONE_LESION | 40 | anatomical zone and lesion selection |
| TREATMENT | 50 | treatment/material entry and completion |
| REPORT_SUMMARY | 60 | committed report summary/local PDF status |

## Deterministic widget geometry
### DASHBOARD / 10
- `start_session`: x=40 y=120 w=300 h=96
- `open_reports`: x=40 y=240 w=300 h=96
- `completed_animals`: x=560 y=120 w=360 h=80
- `consumed_dressings`: x=560 y=224 w=360 h=80

### ANIMAL_SESSION / 20
- `animal_id`: x=40 y=120 w=600 h=72
- `identity_status`: x=40 y=208 w=600 h=64
- `confirm_identity`: x=40 y=360 w=280 h=96
- `cancel_session`: x=344 y=360 w=280 h=96

### LIMB_CLAW / 30
- `select_limb`: x=40 y=120 w=440 h=160
- `select_claw`: x=520 y=120 w=440 h=160
- `back`: x=40 y=448 w=160 h=72

### ZONE_LESION / 40
- `select_zone`: x=40 y=112 w=440 h=280
- `select_lesion`: x=520 y=112 w=440 h=280
- `back`: x=40 y=448 w=160 h=72

### TREATMENT / 50
- `select_treatment`: x=40 y=112 w=440 h=160
- `add_dressing`: x=520 y=112 w=200 h=96
- `dressings`: x=744 y=112 w=216 h=96
- `complete_session`: x=520 y=328 w=440 h=112
- `back`: x=40 y=448 w=160 h=72

### REPORT_SUMMARY / 60
- `report_id`: x=40 y=112 w=920 h=64
- `source_session_id`: x=40 y=192 w=920 h=64
- `generate_local_pdf`: x=40 y=344 w=360 h=96
- `back_to_dashboard`: x=424 y=344 w=360 h=96

## Navigation table
- `start_session`: 10 → 20
- `confirm_identity`: 20 → 30 only when identity status is CONFIRMED
- `cancel_session`: 20 → 10 with explicit cancel state
- `select_limb`: remain 30 and bind limb
- `select_claw`: 30 → 40 only after limb selected
- `select_zone`: remain 40 and bind zone
- `select_lesion`: 40 → 50 only after zone selected
- `select_treatment`: remain 50 and bind treatment
- `add_dressing`: remain 50 and increment synthetic/test counter
- `complete_session`: 50 → 60 only after durable completion acknowledgement from application layer
- `generate_local_pdf`: remain 60; display generation result only
- `back_to_dashboard`: 60 → 10
- `back`: previous workflow screen; SHALL NOT bypass required state gates.

## Binding manifest
HMI variables are presentation/cache variables, not canonical storage:
`animal_id`, `identity_status`, `limb`, `claw`, `zone`, `lesion`, `treatment`, `dressings`, `report_id`, `source_session_id`, `completed_animals`, `consumed_dressings`.

## KS123-14DR bench Modbus manifest
Transport: local isolated `RS485 / Modbus RTU` between GL100E and KS123-14DR only.

Logical bench channels:
- DI1..DI8 → synthetic test switch states;
- DO1..DO6 → dedicated non-machine indicator/test loads only.

Exact register/coil addresses SHALL be copied from the verified KS123-14DR vendor configuration/manual during HW-A1/HW-A2. Unknown addresses fail closed; no guessed address may be treated as verified.

## DTools realization checklist
1. Create project for exact GL100E / 1024×600.
2. Create screens 10/20/30/40/50/60.
3. Reproduce widget IDs and geometry exactly.
4. Implement navigation table with state guards.
5. Configure only local bench Modbus device for KS123-14DR after address verification.
6. Do not configure any KVK device, network/cloud endpoint or machine bus.
7. Build/compile in DTools with zero errors.
8. Export/save native project artifact and record DTools version, project hash and timestamp.
9. Capture screenshots of all six screens.
10. Native artifact remains `NATIVE_DTOOLS_ARTIFACT_REQUIRED` until steps 1–9 are evidenced.

## HW-A3 acceptance criteria
HW-A3 SHALL NOT PASS until a real DTools-generated project/export exists, the exact GL100E is physically verified, compile/upload evidence exists, touch/navigation is exercised on the real panel, and the observed screen geometry matches this specification.
