# ROADMAP-HC-001 — HoofCare KVK Retrofit Roadmap

## Status
`BASELINED / ACTIVE`

## Roadmap

### F0 — Foundation / Governance
Status: `CLOSED / BASELINED`.

### F10 — ARS / problem and stakeholder requirements
Status: `CLOSED / BASELINED`.

### F20 — ARB / boundaries
Status: `CLOSED / BASELINED`.

### F30 — ADR set
Status: `CLOSED / BASELINED`.

### F40 — System Architecture
Status: `CLOSED / BASELINED`.

### F50 — LEL / logical and electrical layer
Status: `CLOSED / BASELINED`.

### F60 — Requirements
Status: `CLOSED / BASELINED`.

### F70 — Bench MVP implementation
Canonical vertical slice:
`animal → limb → claw → zone → lesion → treatment → material → media → close session → report`.

Status: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`.

### F75 — Isolated physical prototype / bench hardware
Software and physical-prototype definition P1–P7 are closed and verified. The next bounded subphase is actual isolated bench hardware assembly.

Selected procurement target:
- Kinco GL100E HMI 10.1-inch / 1024×600;
- Kinco KS123-14DR I/O, 8 DI + 6 relay DO;
- existing 24 VDC supply;
- RFID deferred to a later phase.

Planned isolated bench path:
`24 VDC → GL100E ↔ RS485/Modbus RTU ↔ KS123-14DR → test buttons / test lamps only`.

No electrical or logical connection to the real KVK 801-1 is allowed in this phase.

Status: `SOFTWARE/PROFILE CLOSED; HARDWARE ASSEMBLY READINESS = NEXT / AUTHORITY REQUIRED`.

Exit: `ISOLATED BENCH HARDWARE ASSEMBLED / VERIFIED`.

### F80 — Physical KVK 801-1 audit and read-only retrofit design
Blocked until access to the actual circa-2013 KVK 801-1 is available.

Required evidence:
- machine photographs;
- cabinet / controls / supply identification;
- PLC/HMI and I/O inventory where present;
- wiring/schematic evidence where available;
- mounting points and dimensions;
- source-of-truth signal inventory;
- galvanic/electrical isolation concept;
- risk review preserving original machine safety.

F80 audit itself does not authorize live machine connection. A separate observation-only implementation plan and Project Owner authority are required before any live KVK signal acquisition.

Status: `BLOCKED_BY_SITE_ACCESS / NOT ACTIVE`.

Exit: `KVK READ-ONLY INTERFACE DESIGN VERIFIED`.

### F90 — Field pilot
- 10 animals;
- 50 animals;
- full working shift;
- usability and error analysis;
- workflow reconciliation.

Status: `NOT ACTIVE`.

Exit: `FIELD PILOT PASSED`.

### F100 — Product hardening / v1.0
- enclosure/environmental hardening;
- recovery and backup;
- operator/service documentation;
- installation package;
- release evidence.

Status: `NOT ACTIVE`.

Exit: `HOOFCARE KVK RETROFIT v1.0`.

## Current roadmap position
`F75 — ISOLATED BENCH HARDWARE ASSEMBLY READINESS`

Completed:
- Bench MVP = CLOSED;
- P1–P7 = MERGED / VERIFIED;
- Physical Prototype = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED;
- IA-HC-002 = FULFILLED.

Next Project Owner gate:
- `IMP-HC-002 — Isolated Bench Hardware Assembly Plan`;
- `IA-HC-003 — Isolated Bench Hardware Assembly Authority`.

Physical KVK-dependent work remains `BLOCKED_BY_SITE_ACCESS` and outside current authority.
