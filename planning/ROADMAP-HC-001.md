# ROADMAP-HC-001 — HoofCare KVK Retrofit Roadmap

## Status

`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Roadmap

### F0 — Foundation / Governance

- Foundation.
- AGENTS.md.
- Current State.
- Traceability.
- Initial Implementation Authority.

Exit: `FOUNDATION BASELINED`.

### F10 — ARS / problem and stakeholder requirements

- operator workflow;
- farmer reporting;
- veterinary reporting;
- zootechnical reporting;
- nutritionist reporting;
- technical-service requirements;
- environmental and usability constraints.

Exit: `ARS BASELINED`.

### F20 — ARB / boundaries

- KVK boundary;
- safety boundary;
- clinical decision boundary;
- local data boundary;
- external integration boundary.

Exit: `ARB BASELINED`.

### F30 — ADR set

Required material decisions include at least:

- HMI/edge architecture;
- KVK read-only integration strategy;
- animal identification strategy;
- image acquisition and storage;
- local persistence and backup;
- veterinary nomenclature source;
- report generation architecture.

Exit: required ADRs `APPROVED`.

### F40 — System Architecture

- component model;
- data flows;
- hardware topology;
- trust boundaries;
- failure modes;
- recovery;
- deployment model.

Exit: `SYSTEM ARCHITECTURE BASELINED`.

### F50 — LEL / logical and electrical layer

- HMI;
- 24 VDC supply;
- remote I/O;
- galvanic isolation;
- Ethernet/RS485;
- RFID;
- cameras;
- KVK signal observation;
- enclosure and mounting assumptions.

Exit: `LEL BASELINED`.

### F60 — Requirements

- functional requirements;
- safety requirements;
- data requirements;
- UI requirements;
- reporting requirements;
- audit requirements;
- performance and recovery requirements.

Exit: `REQUIREMENTS BASELINED`.

### F70 — Bench MVP implementation

First vertical slice:

`animal → limb → claw → zone → lesion → treatment → material → before/after media → close session → report`

KVK integration remains simulated/read-only.

Exit: `BENCH MVP IMPLEMENTED`.

### F80 — Physical KVK 801-1 audit and retrofit integration

Blocked until access to the physical 2013-generation KVK 801-1 is available.

- machine photos;
- PLC/HMI identification;
- cabinet and I/O inventory;
- safe signal interface;
- mounting point;
- electrical verification.

Exit: `KVK INTERFACE VERIFIED`.

### F90 — Field pilot

- 10 animals;
- 50 animals;
- full working shift;
- usability and error analysis;
- workflow reconciliation.

Exit: `FIELD PILOT PASSED`.

### F100 — Product hardening / v1.0

- enclosure/environmental hardening;
- recovery and backup;
- operator/service documentation;
- installation package;
- release evidence.

Exit: `HOOFCARE KVK RETROFIT v1.0`.

## Current roadmap position

`F0 — FOUNDATION / GOVERNANCE`

Physical KVK-dependent work is explicitly `BLOCKED_BY_SITE_ACCESS`, not a blocker for Foundation, ARS, ARB, ADR preparation or bench-prototype design.
