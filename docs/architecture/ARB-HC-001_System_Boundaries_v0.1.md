# ARB-HC-001 — System Boundaries v0.1

## Status

`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## 1. Purpose

This document defines architectural boundaries for the project currently using the engineering codenames `PawelHumieckiHMI` / `HoofCare`. These names are not approved commercial names.

## 2. System boundary

The system boundary includes:

- HMI/operator workflow;
- local application state and treatment-session lifecycle;
- local persistence for approved data classes;
- report generation;
- image/media attachment;
- animal identification adapters;
- test/simulated I/O;
- future read-only machine-observation adapters.

The system boundary excludes, unless separately authorized:

- KVK machine actuation;
- hydraulic valve control;
- gate, strap, winch or lift control;
- KVK PLC program mutation;
- E-STOP, safety relay, safety PLC or interlock modification;
- autonomous treatment execution;
- autonomous veterinary diagnosis;
- medication dosing;
- production cloud processing of real farm data.

## 3. KVK boundary

### ARB-HC-KVK-001 — Read-only first

The first physical interface to the KVK 801-1 SHALL be observational/read-only.

### ARB-HC-KVK-002 — No safety dependency

HoofCare SHALL NOT be required for the KVK to enter, maintain or recover a safe state.

### ARB-HC-KVK-003 — No hidden write path

A read-only adapter SHALL NOT expose any hidden or dormant command/write channel to the KVK.

### ARB-HC-KVK-004 — Physical audit gate

No live KVK connection may be baselined before inspection of the actual circa-2013 KVK 801-1, identification of controller/I/O hardware and a documented interface record.

## 4. Safety boundary

Original KVK safety circuits remain authoritative and independent.

HoofCare may display or log safety-related status only if that observation is proven not to weaken, bypass or alter the safety circuit.

Any future state-changing machine path requires a separate Project Owner decision, new/extended Implementation Authority, explicit hazard analysis and architecture review.

## 5. Clinical boundary

### ARB-HC-CLIN-001 — Human clinical authority

The system supports structured human-entered classification, documentation and escalation. It does not own final veterinary diagnosis.

### ARB-HC-CLIN-002 — Advisory outputs

Trend or nutrition context SHALL be labeled as support information and SHALL NOT claim causal diagnosis.

## 6. Data boundary

### ARB-HC-DATA-001 — Local-first

The bench MVP is local-first and uses synthetic/test data unless separate approval authorizes real data.

### ARB-HC-DATA-002 — Session integrity

Animal identity, treatment session, media and operator provenance form one consistency boundary. Ambiguity SHALL fail closed before record commitment.

### ARB-HC-DATA-003 — HMI not sole archive

The target architecture SHALL NOT make the replaceable HMI the sole permanent archive for treatment history.

### ARB-HC-DATA-004 — External transfer

External/cloud transfer of real farm, animal or personal data is outside current authority and requires a separate privacy/data decision.

## 7. HMI boundary

The HMI owns operator interaction and presentation. It SHALL NOT automatically inherit responsibility for long-term persistence, machine safety or clinical authority.

The exact HMI/edge-controller responsibility split is deferred to ADR/System Architecture.

`Kinco GL100E 10.1"` remains a prototype candidate only.

## 8. Peripheral boundary

RFID, cameras, remote I/O and other peripherals SHALL connect through explicit adapters/interfaces. Failure or absence of a peripheral SHALL be represented explicitly rather than silently substituted with guessed data.

## 9. Network boundary

Bench operation SHALL remain functional without Internet dependency. Any future remote access, synchronization or cloud service is a downstream architectural and authority decision.

## 10. Failure boundaries

The architecture SHALL distinguish at minimum:

- HMI failure;
- controller/application failure;
- storage failure;
- RFID/identity failure;
- camera/media failure;
- machine-observation link failure;
- network failure.

No failure in HoofCare SHALL compromise original KVK safety behavior.

## 11. Deferred decisions

ARB does not decide:

- final HMI model;
- exact edge-controller technology;
- database engine;
- RFID protocol/device;
- camera technology;
- KVK fieldbus/electrical observation method;
- report engine;
- enclosure/IP class;
- cloud architecture.

These belong to ADR/System Architecture after the relevant evidence is available.

## 12. ARB exit criteria

`ARB-HC-001` may be baselined when:

- all safety, clinical, data and KVK boundaries are explicit;
- no implementation choice is silently elevated to an architectural decision;
- traceability to Foundation and ARS is complete;
- `IA-HC-001` remains inactive unless separately approved;
- Project Owner approves the final diff and exact head.
