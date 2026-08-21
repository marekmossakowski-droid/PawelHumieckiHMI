# REQ-HC-001 — Implementable Requirements v0.1

## Status

`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## 1. Purpose

This document translates the approved Foundation, ARS, ARB, ADR set, System Architecture and LEL into implementable, testable requirements for the bench MVP and subsequent field integration preparation.

Current engineering identifiers `PawelHumieckiHMI` / `HoofCare` remain codenames only.

## 2. Authority boundary

These requirements do not activate implementation authority by themselves.

`IA-HC-001` remains `PROPOSED / NOT ACTIVE` until explicitly approved by the Project Owner.

No requirement below authorizes live KVK writes, hydraulic actuation, PLC mutation, safety mutation, autonomous veterinary diagnosis, deployment or production release.

## 3. Session lifecycle

### REQ-HC-SES-001 — Unique session identity
Each treatment session SHALL have a unique immutable session identifier.

### REQ-HC-SES-002 — Explicit lifecycle state
Each session SHALL be in exactly one lifecycle state defined by LEL-HC-001.

### REQ-HC-SES-003 — Durable completion
A session SHALL NOT be considered completed until canonical data are durably committed by the edge/application layer.

### REQ-HC-SES-004 — HMI restart recovery
After HMI restart, an in-progress recoverable session SHALL be restorable from canonical edge state without relying on transient HMI memory.

### REQ-HC-SES-005 — Idempotent event application
Repeated delivery of the same logical event SHALL NOT create duplicate logical records when an event identifier or deterministic deduplication key exists.

## 4. Animal identity

### REQ-HC-ID-001 — Internal immutable animal identity
The core model SHALL use an internal immutable animal identifier independent of the external tag technology.

### REQ-HC-ID-002 — External identifiers
The system SHALL support one or more external identifiers associated with one animal record.

### REQ-HC-ID-003 — Fail-closed ambiguity
Missing, conflicting or duplicate animal identity SHALL block automatic commit to animal history and place the session into an unresolved/identity-pending state.

### REQ-HC-ID-004 — Bench simulation
Bench MVP SHALL support simulated animal identifiers without requiring a physical RFID reader.

## 5. HMI workflow

### REQ-HC-HMI-001 — Session dashboard
The HMI SHALL provide a dashboard showing at least current animal/session status, completed-animal count and consumed-dressing/material count for the active work period.

### REQ-HC-HMI-002 — Codename banner separation
Engineering codenames SHALL NOT be presented as an approved commercial product name.

### REQ-HC-HMI-003 — Limb selection
The HMI SHALL provide unambiguous selection of front-left, front-right, rear-left and rear-right limbs.

### REQ-HC-HMI-004 — Claw selection
The HMI SHALL provide structured selection of the affected claw without requiring free text.

### REQ-HC-HMI-005 — Anatomical zone map
The HMI SHALL provide selectable anatomical zones including toe, sole, white line, axial wall, abaxial wall, heel/bulb region, soft heel tissue and interdigital cleft/space.

### REQ-HC-HMI-006 — Glove-oriented primary controls
Primary workflow controls SHALL be sized and spaced for a 10-inch class industrial touchscreen used with work gloves.

### REQ-HC-HMI-007 — No machine-control affordance
The bench and first field HMI SHALL NOT expose any UI control that can actuate KVK gates, straps, winches, lifts, valves, hydraulics or safety functions.

## 6. Clinical recording

### REQ-HC-CLIN-001 — Human classification
Lesion classification SHALL be explicitly selected/confirmed by a human operator.

### REQ-HC-CLIN-002 — Controlled vocabulary
Clinical classification SHALL use a controlled, versioned lesion catalogue for analytics-capable records.

### REQ-HC-CLIN-003 — Free-text supplement
Free text MAY supplement structured clinical data but SHALL NOT replace controlled lesion classification where analytics depend on it.

### REQ-HC-CLIN-004 — Taxonomy provenance
Each structured lesion record SHALL store the taxonomy/catalogue version used at the time of recording.

### REQ-HC-CLIN-005 — No autonomous diagnosis
The system SHALL NOT label machine-generated inference as a veterinary diagnosis.

## 7. Treatment and materials

### REQ-HC-TX-001 — Treatment action recording
The operator SHALL be able to record one or more treatment actions for a session.

### REQ-HC-TX-002 — Material usage recording
The operator SHALL be able to record consumed materials, including dressings, in structured form.

### REQ-HC-TX-003 — Period counters
Dashboard counters SHALL derive from committed session/material records rather than transient button presses alone.

### REQ-HC-TX-004 — Correction audit
Corrections to completed treatment/material records SHALL be auditable and SHALL NOT silently replace historical values.

## 8. Media

### REQ-HC-MED-001 — Media identity
Each media object SHALL have a unique media identifier.

### REQ-HC-MED-002 — Session linkage
Each treatment media object SHALL be linked to the originating session.

### REQ-HC-MED-003 — Provenance category
Media SHALL identify whether it is `BEFORE`, `AFTER`, imported reference/example, or another explicitly defined category.

### REQ-HC-MED-004 — Reference-image separation
Reference/example images SHALL never be silently presented as actual evidence from the treated animal.

### REQ-HC-MED-005 — Bench test media
Bench MVP SHALL use synthetic/test media only.

## 9. KVK observation boundary

### REQ-HC-KVK-001 — Read-only adapter contract
Any future KVK adapter SHALL expose observation/state data only.

### REQ-HC-KVK-002 — No write route
The software architecture SHALL contain no KVK command, configuration-write or actuation route under the current authority.

### REQ-HC-KVK-003 — Unknown remains unknown
Missing, stale, ambiguous or unverified KVK observation SHALL be represented as unavailable/unknown and SHALL NOT be inferred as a machine state.

### REQ-HC-KVK-004 — Safety independence
Loss, crash, restart or disconnection of all project components SHALL NOT alter or disable original KVK safety behavior.

### REQ-HC-KVK-005 — Physical integration block
No live KVK connection SHALL be implemented until the actual circa-2013 KVK 801-1 has been inspected and a verified interface record exists.

## 10. Data persistence and audit

### REQ-HC-DATA-001 — Local-first operation
Core session workflow SHALL operate without Internet connectivity.

### REQ-HC-DATA-002 — HMI-independent durable store
Historical treatment records SHALL reside in a durable local store independent from the replaceable HMI.

### REQ-HC-DATA-003 — Audit trail
Material changes to completed records SHALL produce an auditable change record containing at least record identity, timestamp and change context.

### REQ-HC-DATA-004 — No silent media reassignment
Media SHALL NOT be silently reassigned between animal/session records.

### REQ-HC-DATA-005 — Bench synthetic data
Bench MVP SHALL use synthetic/test animal and farm data only.

## 11. Reporting

### REQ-HC-REP-001 — Canonical data source
Reports SHALL be generated from committed canonical records and linked media, not transient HMI state.

### REQ-HC-REP-002 — PDF output
Bench MVP SHALL support generation of a local PDF treatment report using synthetic/test data.

### REQ-HC-REP-003 — Audience sections
The report model SHALL support sections for farmer, veterinarian, zootechnician, nutritionist and technical service.

### REQ-HC-REP-004 — Document provenance
Generated reports SHALL include a document/report identifier, generation timestamp and source session identifier.

### REQ-HC-REP-005 — Clinical disclaimer
Where appropriate, report output SHALL make clear that the system supports documentation and does not replace veterinary examination/diagnosis.

## 12. Diagnostics and recovery

### REQ-HC-DIAG-001 — Component health
The system SHALL expose local health state for HMI communication, edge/application service, storage and configured test peripherals.

### REQ-HC-DIAG-002 — Degraded mode
Failure of an optional peripheral such as camera or simulated RFID SHALL be represented explicitly and SHALL NOT corrupt canonical session state.

### REQ-HC-DIAG-003 — Recoverable incomplete session
A crash/restart during an incomplete session SHALL preserve enough durable state to allow operator recovery or explicit cancellation where feasible.

### REQ-HC-DIAG-004 — No safety coupling
Diagnostics or recovery logic SHALL NOT modify KVK safety state.

## 13. Bench MVP acceptance requirements

### REQ-HC-MVP-001 — End-to-end synthetic workflow
The bench MVP SHALL demonstrate:

`animal identity → session → limb → claw → zone → lesion → treatment → material → media → completion → PDF report`.

### REQ-HC-MVP-002 — Identity negative test
The bench MVP SHALL demonstrate that ambiguous/conflicting identity cannot be committed to animal history.

### REQ-HC-MVP-003 — HMI restart test
The bench MVP SHALL demonstrate recovery of a persisted in-progress session after HMI/UI restart.

### REQ-HC-MVP-004 — Duplicate event test
The bench MVP SHALL demonstrate that repeated delivery of a duplicate event does not duplicate the corresponding logical record.

### REQ-HC-MVP-005 — Reference-image labeling test
The bench MVP SHALL demonstrate that reference/example media remain visibly distinguished from actual-session media.

### REQ-HC-MVP-006 — No KVK actuation surface
Automated verification SHALL demonstrate absence of a KVK write/command API in the bench MVP public interfaces.

## 14. Deferred requirements

The following remain downstream of site audit or later authority:

- physical RFID hardware and tag standard;
- exact camera hardware;
- exact KVK electrical/protocol interface;
- production enclosure/IP class;
- external herd-management integrations;
- production backup targets and retention;
- remote/cloud synchronization;
- public deployment and release;
- any machine actuation.

## 15. Exit criteria

`REQ-HC-001` may be baselined when:

- each requirement traces to an approved upstream artifact;
- requirements are testable or explicitly deferred;
- no requirement creates authority beyond approved boundaries;
- physical KVK integration remains blocked pending site audit;
- Project Owner approves the final diff and exact head.
