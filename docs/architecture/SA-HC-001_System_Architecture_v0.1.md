# SA-HC-001 — System Architecture v0.1

## Status

`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## 1. Purpose

This document defines the first complete system architecture for the project currently identified by the internal engineering codenames `PawelHumieckiHMI` / `HoofCare`.

It implements the baselined Foundation, ARS, ARB and the proposed ADR set without activating runtime implementation authority.

## 2. Architectural drivers

The architecture SHALL preserve:

- original KVK 801-1 safety independence;
- observational/read-only first integration with KVK;
- human clinical authority;
- local-first operation;
- auditable treatment-session provenance;
- recoverable data persistence;
- explicit separation between operator UI, machine observation and durable data services.

## 3. Logical components

### SA-HC-C01 — Industrial HMI

Responsibilities:

- operator workflow;
- animal/session selection;
- limb/claw/zone navigation;
- lesion/treatment/material entry;
- status and diagnostics display;
- report preview and follow-up interaction.

The HMI SHALL NOT:

- own machine safety;
- issue KVK actuation commands under current architecture;
- be the sole permanent archive;
- make autonomous veterinary decisions.

### SA-HC-C02 — Edge / Application Controller

Responsibilities:

- canonical session lifecycle;
- local data services;
- validation and fail-closed association;
- media metadata management;
- report generation orchestration;
- local API for the HMI;
- audit trail;
- future read-only KVK observation adapter boundary.

### SA-HC-C03 — Durable Local Store

Responsibilities:

- animals;
- sessions;
- findings;
- treatment records;
- materials;
- follow-up state;
- audit records;
- media metadata;
- configuration/version metadata.

The store SHALL be recoverable independently of HMI replacement.

### SA-HC-C04 — Media Store

Responsibilities:

- immutable session-linked `BEFORE` and `AFTER` media objects;
- provenance metadata;
- checks or identifiers sufficient to prevent silent reassignment.

### SA-HC-C05 — Animal Identity Adapter

Responsibilities:

- accept animal identity from supported source;
- expose normalized identity candidates to the application;
- preserve source/provenance;
- fail closed on ambiguous automatic association.

RFID is the preferred future source but not yet a hardware baseline.

### SA-HC-C06 — KVK Observation Adapter

Responsibilities:

- future observation of approved KVK state signals only;
- normalize observed states for workflow assistance;
- expose health/quality metadata for each signal.

Invariants:

- no write path;
- no hydraulic command path;
- no PLC program mutation;
- no safety dependency;
- physical implementation blocked until on-site audit.

### SA-HC-C07 — Report Service

Responsibilities:

- generate reports from canonical durable records;
- support farmer, veterinary, zootechnical, nutritionist and technical-service views;
- distinguish example/reference images from animal-specific evidence;
- include provenance and disclaimer metadata as required.

## 4. Hardware topology — bench MVP

The current bench topology is conceptual:

```text
24 VDC PSU
   |
   +-- Industrial HMI 10-inch class
   |       |
   |       +------ Ethernet / local application link
   |
   +-- Edge/Application Controller
   |       |
   |       +-- Durable local storage
   |       +-- Media storage
   |       +-- USB/serial test adapters
   |
   +-- Test/simulated I/O only
```

`Kinco GL100E 10.1"` remains a candidate HMI and is not an architectural baseline.

## 5. Future KVK topology

Physical KVK integration is deliberately deferred.

The target principle is:

```text
Original KVK 801-1 controls/safety
            |
      observational boundary
            |
      electrical/logical isolation
            |
     KVK Observation Adapter
            |
      Edge Controller
            |
           HMI
```

The observational boundary SHALL NOT provide any route back into machine actuation.

## 6. Primary data flow

### Treatment session

1. Operator starts session.
2. Animal identity is entered or observed.
3. Application validates identity state.
4. Operator selects limb, claw and anatomical zone.
5. Operator records lesion/classification.
6. Operator records treatment and materials.
7. Media may be attached with provenance.
8. Session is explicitly completed or left incomplete/follow-up-required.
9. Canonical record is committed to durable store.
10. Report service renders derived reports from committed records.

## 7. State model

Minimum session states:

- `NEW`;
- `IDENTITY_PENDING`;
- `ACTIVE`;
- `INCOMPLETE`;
- `COMPLETED`;
- `FOLLOW_UP_REQUIRED`;
- `VOIDED_WITH_AUDIT`.

Automatic association SHALL NOT transition to a committed animal history state when identity/provenance is ambiguous.

## 8. Trust and authority boundaries

### Machine safety authority

Remains entirely outside the project system.

### Clinical authority

Remains with the human operator/veterinary professional.

### Data authority

Canonical treatment data is owned by the application data layer, not transient HMI screen state.

### Project/runtime authority

`IA-HC-001` remains `PROPOSED / NOT ACTIVE`; this architecture does not authorize implementation.

## 9. Failure modes

### HMI failure

Expected behavior:

- no impact on original KVK safety;
- durable records already committed remain recoverable;
- incomplete local interaction may require operator restart/reconciliation.

### Edge/application failure

Expected behavior:

- no impact on original KVK safety;
- no silent commit of partially validated sessions;
- restart SHALL support deterministic recovery or explicit abandonment with audit.

### Identity reader failure

Expected behavior:

- manual identity workflow remains possible if authorized by later requirements;
- automatic association is disabled.

### KVK observation loss

Expected behavior:

- workflow assistance degrades to manual selection;
- original KVK operation is unaffected;
- stale/unknown machine state SHALL NOT be presented as current.

### Storage failure

Expected behavior:

- session commit fails closed;
- operator receives explicit error;
- no false success indication.

### Media failure

Expected behavior:

- media failure does not silently replace or relink evidence;
- session may continue according to later requirements, but media state is explicit.

## 10. Recovery principles

- deterministic startup validation;
- durable session IDs;
- explicit incomplete-session handling;
- backup/restore procedure before production release;
- no recovery action may introduce a KVK write path;
- recovery SHALL preserve auditability of record changes.

## 11. Network model

Bench MVP SHALL have no Internet dependency.

Local networking may be used between HMI and edge controller. Any future cloud or remote-access capability requires separate architecture, data/privacy and authority decisions.

## 12. Security principles

- least privilege between components;
- no credentials or secrets in treatment audit logs;
- explicit versioning of data contracts/configuration;
- no machine-control capability hidden inside diagnostic or data interfaces;
- external integrations are disabled until separately authorized.

## 13. Deployment units

Conceptual units:

1. HMI application/project;
2. edge/application runtime;
3. local durable database;
4. media storage;
5. report templates/service;
6. test/simulation adapters;
7. future read-only KVK adapter.

Exact technologies remain downstream implementation decisions where not already fixed by approved ADRs.

## 14. Verification strategy

Architecture-level verification SHALL include:

- boundary tests proving no KVK write interface exists;
- fail-closed identity/session tests;
- HMI replacement/data recovery scenario;
- simulated KVK observation loss;
- media/session provenance tests;
- report generation from committed canonical records;
- restart/recovery tests for incomplete sessions.

## 15. Open items for LEL / Requirements

- exact HMI-to-edge application protocol;
- data entities and field-level contracts;
- session transition rules;
- error/status vocabulary;
- report data contract;
- test fixture identities and sample cases;
- concrete persistence technology;
- exact supported animal identity formats;
- physical KVK signal map after site audit.

## 16. Exit criteria

`SA-HC-001` may be baselined when:

- it is consistent with Foundation, ARS, ARB and approved ADRs;
- all critical safety/clinical/data boundaries remain explicit;
- failure and recovery behavior are defined at architecture level;
- traceability and docs-ci are updated;
- Project Owner approves final diff and exact head.
