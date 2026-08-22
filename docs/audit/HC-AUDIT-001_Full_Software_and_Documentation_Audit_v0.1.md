# HC-AUDIT-001 — Full Software and Documentation Audit v0.1

## Status
`AUDIT COMPLETE / FINDINGS OPEN — REMEDIATION REQUIRED`

## Audit checkpoint
Canonical audited `main`: `3cfb3d324e8542871caa1386157f0b22bc008943`.

The audit covers source code, tests, CI, architecture/governance, requirements, traceability and readiness for the currently selected isolated bench hardware path. It does not claim physical verification of Kinco GL100E or Kinco KS123-14DR and does not change any authority.

## Executive conclusion
The repository has a strong safety/governance skeleton and useful synthetic domain prototypes, but current closure language overstates deployable physical readiness. The codebase is not yet ready for the first real GL100E application test without remediation.

The largest gaps are:
- no actual Kinco DTools/GL100E project artifact exists in the repository;
- the approved hardware path has no designated edge/application runtime host although the baselined architecture requires HMI-independent canonical persistence/reporting;
- the current `PDF` output is a text payload with a PDF header, not a structurally valid PDF document;
- synthetic acceptance can report PASS without durable end-to-end completion and contains hard-coded PASS assertions;
- hardware source/tests still describe generic 8DI/8DO hardware, while the selected KS123-14DR profile is 8DI/6 relay DO;
- multiple upstream formal documents remain marked `PROPOSED` even though project state and traceability treat them as baselined;
- several implementable requirements remain unimplemented or only partially represented.

Recommended technical gate: do not advance beyond `HW-A1` into `HW-A2/HW-A3` until P0/P1 remediation is reconciled and approved. This recommendation does not revoke `IA-HC-003`; it prevents false-positive bench acceptance.

## Finding register

| ID | Severity | Area | Finding | Required remediation |
|---|---|---|---|---|
| AUD-HC-001 | P0 | HMI deployability | Repository contains declarative Python screen models but no Kinco DTools project, export/build artifact or deterministic generator capable of loading the designed GUI to GL100E. | Establish the actual GL100E/DTools application artifact, version it or reproducibly generate it, and add verification evidence. |
| AUD-HC-002 | P0 | Architecture / hardware | `SA-HC-001` requires a separate edge/application controller and HMI-independent durable store/report service, while current IA-HC-003 bench hardware is GL100E + KS123-14DR + passive test hardware and no dedicated runtime host is baselined. | Decide and baseline the edge runtime host for bench use, or explicitly redesign architecture if responsibilities are intentionally moved. |
| AUD-HC-003 | P0 | Reporting | `ReportDocument.to_pdf_bytes()` produces plain UTF-8 text beginning `%PDF-1.4`, without PDF objects/xref/trailer. Tests verify only the magic prefix. | Implement a valid local PDF renderer and parse/validate the resulting PDF in automated tests. |
| AUD-HC-004 | P0 | Acceptance integrity | `BenchMvpScenario` does not durably complete/persist the canonical session before report generation; `committed=True` is supplied as a caller flag, and `end_to_end` / `no_kvk_actuation_surface` PASS values are hard-coded. | Replace synthetic assertions with evidence derived from the canonical committed session and explicit negative capability tests. |
| AUD-HC-005 | P1 | Durable completion | `PhysicalPrototypeAcceptance` applies `COMPLETE` before persistence, contrary to REQ-HC-SES-003 / LEL-HC-D02 durable-completion semantics. | Introduce an application transaction/commit boundary in which completion is acknowledged only after durable persistence succeeds. |
| AUD-HC-006 | P1 | Hardware profile | Source profile and BOM use generic `10-inch-class-prototype`, 8DI/8DO and a new DIN PSU, while selected bench hardware is Kinco GL100E + KS123-14DR (8DI/6 relay DO) + existing isolated 24 VDC. Existing tests enforce the stale profile. | Replace generic profile/BOM with exact selected hardware profile and update tests. |
| AUD-HC-007 | P1 | Persistence security | `LocalSessionStore` builds file paths directly from caller-provided `session_id`, allowing path traversal if untrusted identifiers reach load/amendment APIs. | Validate identifiers or map them to safe filenames; add traversal negative tests. |
| AUD-HC-008 | P1 | Persistence durability/integrity | Snapshot `os.replace()` provides atomic replacement but no fsync durability, schema/version metadata or integrity check. Amendment JSONL writes are unlocked and sequence generation is race-prone. | Add schema/versioning, durable flush strategy appropriate to target filesystem, corruption/integrity policy and serialized append semantics. |
| AUD-HC-009 | P1 | Audit trail | Amendment records contain only sequence/kind/payload; required timestamp, record identity and change context/operator provenance are missing. | Define canonical amendment/audit schema and enforce mandatory provenance fields. |
| AUD-HC-010 | P1 | Domain invariants | Direct dataclass construction/deserialization can produce inconsistent identity/session combinations because validation exists mainly in factory methods. | Add `__post_init__` invariants and corruption tests for impossible identity/session states. |
| AUD-HC-011 | P1 | Idempotency | `BenchApplicationService._request_results` is global by `request_id`, not scoped to operation/session. Reuse of one request ID on another operation can return an unrelated cached result. | Namespace idempotency keys by operation and resource/session or persist a request fingerprint and reject mismatched reuse. |
| AUD-HC-012 | P1 | Clinical model | LEL/REQ require structured treatment, material, media, taxonomy version and audit events; core SessionEventType implements only identity, complete/follow-up/cancel/unresolved. | Implement the missing canonical event/data model before claiming complete MVP conformance. |
| AUD-HC-013 | P1 | Report canonical source | `PhysicalPersistenceReportingValidator.build_local_report()` accepts lesion/treatment/material summaries from transient caller input instead of committed canonical records. | Persist structured findings/treatments/materials and derive reports exclusively from committed records. |
| AUD-HC-014 | P1 | Media provenance | Media is represented as string references only; BEFORE/AFTER/REFERENCE category, timestamp, source and immutable linkage are not modeled. | Introduce a media metadata entity with explicit provenance/category and no-silent-reassignment controls. |
| AUD-HC-015 | P1 | Documentation state | Foundation, ARS, ARB, SA, LEL and REQ retain `PROPOSED — PROJECT OWNER APPROVAL REQUIRED` banners although current state/traceability mark their lineage baselined. README still reports Foundation initialization. | Perform controlled post-baseline documentation reconciliation without changing approved technical content. |
| AUD-HC-016 | P1 | State-model consistency | SA state vocabulary differs from LEL; code follows most LEL states but omits `NEW`. | Select one canonical lifecycle vocabulary, record compatibility mapping if needed, and align SA, LEL, REQ and code. |
| AUD-HC-017 | P1 | Requirement traceability | HC-TRACE-001 is slice-level. Most individual `REQ-HC-*` requirements lack explicit implementation/test/result mappings. | Add requirement-level trace matrix with status: implemented / partial / deferred / blocked and concrete evidence. |
| AUD-HC-018 | P2 | HMI navigation | Layout exposes `open_reports` and `back` controls that `PhysicalNavigationController` does not implement, so those buttons fail closed instead of navigating. | Implement intentional navigation semantics or remove unsupported controls. |
| AUD-HC-019 | P2 | HMI ergonomics | Touch validation only proves 64×64 size. There are no x/y coordinates, non-overlap, spacing, visibility or screen-fit checks. | Create concrete 1024×600 coordinates and automated geometry/ergonomics validation, then verify on GL100E. |
| AUD-HC-020 | P2 | Observation provenance | Simulated observations lack timestamp, source identity, quality/staleness metadata required by architecture/LEL principles. | Define typed observation envelope with provenance and quality state. |
| AUD-HC-021 | P2 | Acceptance denylist | No-machine-control verification relies on a small finite list of forbidden action names, not an allowlisted capability model. | Make the public HMI/action contract explicitly allowlist-only and test complete exported surfaces. |
| AUD-HC-022 | P2 | CI | runtime-ci runs unit tests on PRs and implementation-branch pushes, but not on pushes to `main`; no lint, type check, coverage threshold, package/build verification or dependency/security checks exist. | Run runtime regression on `main`, add static quality gates and coverage/reporting appropriate to the repo. |
| AUD-HC-023 | P2 | docs-ci | Governance CI is marker/string based and can pass while formal documents contradict current state. | Add semantic cross-document checks for status, authority, lifecycle, hardware profile and traceability. |
| AUD-HC-024 | P2 | Packaging/runtime | Repository has no defined Python package/build/runtime entrypoint for a deployable edge service and no reproducible bench runtime bundle. | Define executable runtime/package, configuration schema and local launch/recovery procedure before physical acceptance. |
| AUD-HC-025 | P2 | RFID simulation | Bench scenario checks that an RFID observation exists but then resolves to the method argument `animal_id` instead of the adapter observation value. | Resolve identity from the observation payload and explicitly test mismatch/conflict behavior. |

## Requirement conformance snapshot

| Requirement area | Audit result | Notes |
|---|---|---|
| Session identity / basic state | PARTIAL | UUID session and basic state machine exist. Durable completion semantics are not compliant. |
| Idempotency | PARTIAL / DEFECT | Event-level duplicate IDs work, service request cache can collide across operations. |
| Animal identity | PARTIAL | Ambiguity fails closed, but no internal animal entity ↔ external identifiers model exists. |
| HMI workflow | PARTIAL | Limb/claw/zone/lesion flow exists synthetically; actual DTools application is absent. |
| Clinical taxonomy | PARTIAL | Lesion enum exists; catalogue/version provenance does not. |
| Treatment/materials | PARTIAL | Transient strings/refs exist; canonical structured records/events are absent. |
| Media | PARTIAL | Reference strings exist; provenance/category entity is absent. |
| KVK safety/read-only boundary | PASS FOR CURRENT SOFTWARE SCOPE | No live KVK adapter or actuation route identified; current adapters are simulated. |
| Local persistence | PARTIAL | JSON snapshots and restart recovery work in tests, but durability/integrity/security requirements need strengthening. |
| Audit trail | PARTIAL | Append-only concept exists, mandatory provenance/timestamp/context is missing. |
| Reporting | FAIL FOR PDF CONFORMANCE | Multi-audience model exists, output is not a valid PDF and clinical content is not entirely canonical. |
| Diagnostics/degraded mode | NOT IMPLEMENTED | No real component health model for HMI/application/storage/test peripheral. |
| Physical GL100E readiness | NOT IMPLEMENTED | Hardware profile is conceptual; DTools artifact is absent. |
| Bench I/O readiness | PARTIAL / STALE | Isolation intent is correct; profile/BOM does not match selected KS123-14DR. |

## Positive findings
The audit confirms several strong properties worth preserving:
- safety boundary is consistently no-actuation/read-only-first across governance and architecture;
- current code does not expose a real KVK hardware adapter or machine actuation path;
- identity ambiguity is treated fail-closed in the domain/application prototype;
- session IDs are immutable UUID values in normal construction;
- restart recovery and corrupt-JSON failure paths are covered by tests;
- HMI navigation is order-constrained and primary touch targets have minimum dimensions;
- synthetic adapters and real-farm-data prohibition are explicit;
- current `CURRENT_STATE` and `HC-TRACE-001` correctly identify `HW-A1` as waiting for physical hardware;
- there were no open PRs at the audited checkpoint;
- TODO/FIXME/NotImplemented/pass placeholder search found no unresolved implementation placeholders.

## Remediation waves

### Wave R0 — truth and deployability gate
Close AUD-HC-001 through AUD-HC-006 and AUD-HC-015 through AUD-HC-017 before progressing to an actual GL100E application test. This wave establishes the exact hardware/software architecture, valid PDF, genuine canonical end-to-end acceptance, exact I/O profile and truthful documentation.

### Wave R1 — data integrity and clinical provenance
Close AUD-HC-007 through AUD-HC-014. This wave hardens persistence, idempotency, audit trail, canonical clinical records and media provenance before any real-farm-data authority could ever be considered.

### Wave R2 — UX, observability and engineering quality
Close AUD-HC-018 through AUD-HC-025. This wave creates concrete screen geometry, complete navigation, typed observations, allowlisted actions, stronger CI and reproducible runtime packaging.

## Authority impact
This audit does not activate, revoke or expand any authority. `IA-HC-003` remains the current bounded isolated-bench authority. No real KVK I/O, machine CAN/RS485/Modbus/serial, commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, live RFID/real-farm data, cloud/network service, external report delivery, deployment, signing, release or public distribution is authorized by this audit.

## Recommended next state
Keep `HW-A1 = WAITING FOR PHYSICAL HARDWARE`, but run software/documentation remediation Wave R0 in parallel. Transition to physical power-up may remain physically blocked by goods-in evidence; the first application test on GL100E should additionally require a verified DTools artifact and reconciled exact hardware profile.
