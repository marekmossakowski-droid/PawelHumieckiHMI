# LEL-HC-001 — Logical Event Lifecycle v0.1

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## 1. Purpose
LEL-HC-001 defines the logical event and state model for the treatment-session workflow. It does not authorize runtime implementation, live KVK connectivity or machine actuation.

## 2. Session lifecycle
A treatment session SHALL use the following externally visible states:

1. `NEW`
2. `IDENTITY_PENDING`
3. `IN_PROGRESS`
4. `FOLLOW_UP_REQUIRED`
5. `COMPLETED`
6. `UNRESOLVED`
7. `CANCELLED`

`COMPLETED` is terminal for the original record. Later corrections SHALL create auditable amendment events rather than silent replacement.

## 3. Core events
The canonical event vocabulary SHALL include at least:

- `SESSION_STARTED`
- `IDENTITY_OBSERVED`
- `IDENTITY_RESOLVED`
- `IDENTITY_CONFLICTED`
- `LIMB_SELECTED`
- `CLAW_SELECTED`
- `ZONE_SELECTED`
- `LESION_RECORDED`
- `TREATMENT_RECORDED`
- `MATERIAL_CONSUMED`
- `MEDIA_ATTACHED`
- `FOLLOW_UP_REQUESTED`
- `SESSION_COMPLETED`
- `SESSION_CANCELLED`
- `SESSION_AMENDED`
- `KVK_STATE_OBSERVED`
- `KVK_STATE_UNAVAILABLE`
- `REPORT_REQUESTED`
- `REPORT_GENERATED`
- `REPORT_FAILED`

## 4. Identity rules
### LEL-HC-I01 — Fail-closed association
A session SHALL NOT transition to committed animal history while animal identity is missing, ambiguous, duplicated or conflicting.

### LEL-HC-I02 — Conflict handling
`IDENTITY_CONFLICTED` SHALL transition the session to `UNRESOLVED` or keep it in a non-committable identity-resolution state until a human resolves the conflict.

### LEL-HC-I03 — External identifiers
RFID or other external identifiers SHALL be observations used to resolve an internal immutable animal identity; they are not themselves the canonical database primary key.

## 5. Clinical workflow rules
### LEL-HC-C01 — Human clinical authority
`LESION_RECORDED` represents a human-entered classification. The event SHALL NOT represent autonomous diagnosis by the system.

### LEL-HC-C02 — Structured location
A lesion record SHALL reference limb, claw and anatomical zone from controlled identifiers where applicable.

### LEL-HC-C03 — Controlled taxonomy version
A lesion record SHALL retain the nomenclature/taxonomy version used at recording time.

## 6. Material and treatment rules
### LEL-HC-T01 — Treatment is explicit
Treatment and consumed material events SHALL be explicit user actions or deterministic consequences of explicit user-confirmed workflow actions.

### LEL-HC-T02 — No machine actuation semantics
No event defined by this LEL SHALL map to KVK hydraulic, valve, gate, strap, winch, lift, PLC configuration or safety actuation.

## 7. Media lifecycle
### LEL-HC-M01 — Provenance
`MEDIA_ATTACHED` SHALL include a media identifier, session identifier, category, timestamp and provenance/source metadata.

### LEL-HC-M02 — Evidence categories
Actual treatment media categories such as `BEFORE` and `AFTER` SHALL remain distinguishable from `REFERENCE` or `EXAMPLE` media.

### LEL-HC-M03 — No silent reassignment
Media SHALL NOT be silently reassigned between sessions or animals.

## 8. KVK observation lifecycle
### LEL-HC-KVK-001 — Observation only
`KVK_STATE_OBSERVED` is informational context only. It SHALL NOT create or imply an actuation capability.

### LEL-HC-KVK-002 — Unverified state
Missing, stale, contradictory or unverified KVK state SHALL be represented as unavailable/unknown rather than inferred.

### LEL-HC-KVK-003 — Safety independence
Loss of KVK observation data, HMI, edge controller or network SHALL have no effect on original KVK safety behavior.

## 9. Commit semantics
### LEL-HC-D01 — Canonical owner
The edge/application layer SHALL own canonical session state transitions and durable commit semantics. HMI display state is not canonical by itself.

### LEL-HC-D02 — Atomic completion intent
A `SESSION_COMPLETED` request SHALL either produce one durably committed completed session or fail without falsely presenting completion as durable.

### LEL-HC-D03 — Idempotency
Repeated delivery of the same logical command/event SHALL NOT create duplicate treatment sessions, duplicate material consumption records or duplicate media linkage when an idempotency key/event identity is available.

## 10. Report lifecycle
### LEL-HC-R01 — Canonical source
`REPORT_GENERATED` SHALL derive from committed canonical records and linked media, not transient HMI screen state.

### LEL-HC-R02 — Report failure
`REPORT_FAILED` SHALL NOT mutate or roll back the already committed treatment record.

## 11. Failure and recovery semantics
- HMI restart: active non-terminal session may be reloaded from canonical edge state.
- Edge restart: durable sessions SHALL be recovered from the local store; transient requests SHALL not be assumed successful without durable evidence.
- Media-store unavailable: core clinical record may continue if policy permits, but media status SHALL remain explicit and no missing media SHALL be fabricated.
- Identity adapter unavailable: manual/synthetic identity handling may be used only where allowed; ambiguous identity remains fail-closed.
- Report service unavailable: treatment record remains valid; reporting enters retryable/failed state.
- KVK observation unavailable: workflow may degrade to manual limb selection/context; no KVK state is inferred.

## 12. HMI command boundary
The HMI MAY request logical actions such as selecting a limb, recording a lesion or completing a session. The HMI SHALL NOT be authoritative for persistence success until the edge/application layer acknowledges durable state.

## 13. Audit rules
The system SHALL retain enough audit information to reconstruct:
- session creation and completion;
- animal identity resolution changes;
- clinical classification changes;
- material consumption changes;
- media attachment/removal/amendment;
- follow-up state changes;
- amendments to completed records.

## 14. Explicit exclusions
This LEL does not define or authorize:
- KVK control commands;
- safety logic;
- PLC writes;
- hydraulic actuation;
- autonomous veterinary diagnosis;
- medication dosing;
- cloud deployment;
- production release.

## 15. Exit criteria
LEL-HC-001 may be baselined when:
- lifecycle states and event semantics are consistent with SA-HC-001;
- no hidden KVK write path exists;
- fail-closed identity and durable completion semantics are explicit;
- clinical human authority is preserved;
- traceability is updated;
- docs-ci passes;
- Project Owner approves the final exact head.
