# ARS-HC-001 — Application and Stakeholder Requirements v0.1

## Status

`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## 1. Purpose

This document defines stakeholder and application-level requirements for the project currently identified by the engineering codenames `PawelHumieckiHMI` / `HoofCare`. These codenames are not an approved product or commercial name.

## 2. Stakeholders

Primary stakeholders:

- hoof-trimming operator / zootechnician;
- farmer / herd owner;
- veterinarian;
- nutritionist;
- farm technical/maintenance service;
- Project Owner / product owner.

Secondary stakeholders:

- installation/integration technician;
- future support/service personnel;
- future external herd-management system integrators.

## 3. Operational context

The first target environment is a retrofit around a `KVK 801-1`, generation circa 2013, older green construction. Physical integration details remain unverified until the actual machine is inspected.

The application SHALL support work in an agricultural environment with dirt, moisture, gloves, time pressure and repeated animal-processing cycles.

## 4. Operator requirements

### ARS-HC-OP-001 — Fast session start

The operator SHALL be able to start or resume an animal treatment session with minimal interaction.

### ARS-HC-OP-002 — Animal identity

The system SHALL associate a treatment session with an explicit animal identity before committing the record to animal history.

If identity is missing, ambiguous or conflicting, the system SHALL fail closed and prevent automatic assignment to an animal record.

### ARS-HC-OP-003 — Limb selection

The operator SHALL be able to select one of four limbs using an unambiguous visual control.

### ARS-HC-OP-004 — Claw selection

For the selected limb, the operator SHALL be able to identify the affected claw without relying on free-text description.

### ARS-HC-OP-005 — Anatomical zone selection

The system SHALL provide a veterinary-consistent hoof map including at least:

- toe;
- sole;
- white line;
- axial wall;
- abaxial wall;
- heel/bulb region;
- soft heel tissue;
- interdigital cleft/space.

### ARS-HC-OP-006 — Lesion recording

The operator SHALL be able to record a lesion from a controlled catalogue and optionally add notes.

The UI SHALL NOT present automated classification as a veterinary diagnosis.

### ARS-HC-OP-007 — Treatment recording

The operator SHALL be able to record performed treatment actions and consumed materials.

### ARS-HC-OP-008 — Before/after evidence

The system SHOULD support attaching `BEFORE` and `AFTER` images to a treatment session with provenance metadata.

### ARS-HC-OP-009 — Session closure

The system SHALL provide an explicit session-completion action and SHALL distinguish incomplete, completed and follow-up-required states.

### ARS-HC-OP-010 — Glove usability

Primary workflow controls SHALL be sized and spaced for practical use on a 10-inch class industrial touchscreen while wearing work gloves.

## 5. Farmer / herd owner requirements

### ARS-HC-FARM-001 — Individual animal report

The system SHALL generate an understandable post-treatment report for the animal.

### ARS-HC-FARM-002 — Herd overview

The system SHALL provide aggregate counts and trends for hoof lesions, treatments, follow-ups and material usage.

### ARS-HC-FARM-003 — Follow-up visibility

Animals requiring reassessment SHALL be visible as a distinct follow-up queue.

## 6. Veterinary requirements

### ARS-HC-VET-001 — Clinical provenance

Each clinical record SHALL identify, where available:

- animal;
- operator;
- timestamp;
- limb;
- claw;
- anatomical zone;
- selected lesion;
- treatment;
- media provenance.

### ARS-HC-VET-002 — Human clinical authority

The system SHALL keep final clinical classification and veterinary decisions under human authority.

### ARS-HC-VET-003 — Escalation support

The system SHOULD allow the operator to flag a case for veterinary review and record the reason for escalation.

### ARS-HC-VET-004 — History

The system SHALL preserve a chronological history of hoof-related records per animal.

## 7. Zootechnical requirements

### ARS-HC-ZOO-001 — Locomotion / recurrence context

The system SHOULD support recording locomotion score or equivalent observational context and identifying recurring hoof problems.

### ARS-HC-ZOO-002 — Group analysis

The system SHOULD support future analysis by herd group, lactation/stage or other husbandry grouping without requiring redesign of the core session model.

## 8. Nutritionist requirements

### ARS-HC-NUT-001 — Trend information

The system SHALL make lesion trends available in a form that can support nutritional investigation at herd/group level.

### ARS-HC-NUT-002 — No causal overclaim

The system SHALL NOT infer that a hoof lesion proves a nutritional cause. Nutrition-related outputs SHALL be advisory context only.

## 9. Technical-service requirements

### ARS-HC-TECH-001 — Machine independence

Failure of the project system SHALL NOT disable or degrade the original safety function of the KVK chute.

### ARS-HC-TECH-002 — Read-only first integration

The first physical integration with the KVK SHALL be observational/read-only.

### ARS-HC-TECH-003 — Service diagnostics

The system SHOULD expose diagnostics for its own power, communications, storage and connected peripheral status.

### ARS-HC-TECH-004 — Replaceable HMI

Loss or replacement of the HMI SHALL NOT be the sole point of permanent loss for historical treatment data in the target architecture.

### ARS-HC-TECH-005 — Recoverability

The system SHALL define backup and recovery behavior before production release.

## 10. Data and audit requirements

### ARS-HC-DATA-001 — Session integrity

A committed treatment session SHALL have a unique identifier and consistent lifecycle state.

### ARS-HC-DATA-002 — Auditability

Material changes to completed treatment records SHALL be auditable.

### ARS-HC-DATA-003 — Media linkage

Attached media SHALL be linked to the specific session and shall not be silently reassigned to another animal.

### ARS-HC-DATA-004 — Local-first bench MVP

The bench MVP SHALL use synthetic/test data only unless a separate privacy/data decision authorizes real farm or animal data.

## 11. Reporting requirements

### ARS-HC-REP-001 — Multi-audience report

The report model SHALL support views useful to:

- farmer;
- veterinarian;
- zootechnician;
- nutritionist;
- technical service.

### ARS-HC-REP-002 — Image labeling

Reference/example images SHALL be clearly distinguished from images captured from the actual treated animal.

### ARS-HC-REP-003 — Non-diagnostic disclaimer

Where required, generated reports SHALL state that the system supports documentation and does not replace veterinary examination or diagnosis.

## 12. Hardware / environmental requirements

### ARS-HC-HW-001 — HMI class

The first bench prototype SHOULD target a 10-inch class industrial HMI. `Kinco GL100E 10.1"` remains a candidate only and is not yet an architectural baseline.

### ARS-HC-HW-002 — 24 VDC ecosystem

The prototype architecture SHOULD prefer industrial 24 VDC components where practical.

### ARS-HC-HW-003 — Farm environment

Production hardware SHALL be selected for the expected agricultural environment, including dust, moisture and cleaning exposure. Exact IP rating and mounting requirements remain an architectural decision.

## 13. Safety and authority requirements

### ARS-HC-SAF-001 — No safety bypass

The system SHALL NOT bypass, replace or weaken original KVK safety circuits, E-STOP, safety relays, interlocks or safety PLC functions.

### ARS-HC-SAF-002 — No machine actuation under current authority

No live hydraulic, valve, gate, strap, winch or lift command path is authorized under the current project authority state.

### ARS-HC-SAF-003 — Fail-closed association

Ambiguous identity, session corruption or conflicting provenance SHALL block automatic record association.

## 14. Explicit non-goals for current phase

The current phase does not establish requirements for:

- autonomous veterinary diagnosis;
- medication dosing;
- live KVK actuation;
- replacement of KVK PLC/safety controls;
- remote unattended machine operation;
- public cloud handling of real farm data;
- commercial branding;
- production release.

## 15. Open dependencies

The following require later ARB/ADR/Architecture decisions:

1. exact KVK 801-1 interface after physical audit;
2. animal identification technology and protocol;
3. image acquisition architecture;
4. local persistence/database technology;
5. HMI versus edge-controller responsibility split;
6. veterinary nomenclature baseline;
7. backup and recovery design;
8. production enclosure/IP/environmental class;
9. report-generation technology.

## 16. ARS exit criteria

`ARS-HC-001` may be baselined when:

- stakeholder set and needs are accepted;
- safety and clinical boundaries are preserved;
- requirements are traceable to Foundation;
- unresolved architecture choices remain explicitly downstream rather than being silently decided in ARS;
- Project Owner approves the final diff and exact head.
