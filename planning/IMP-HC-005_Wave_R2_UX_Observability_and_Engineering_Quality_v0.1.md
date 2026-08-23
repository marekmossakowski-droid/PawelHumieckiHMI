# IMP-HC-005 — Wave R2 UX, Observability and Engineering Quality v0.1

## Status
`APPROVED / RECOVERY ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-006-RECOVERY-ACTIVATION-001`

Plan jest wykonywany w trybie governance recovery. Prospektywne `IA-HC-006` zaczyna obowiązywać dopiero po kontrolowanym merge rekordu recovery i Repository Verification; nie autoryzuje retroaktywnie PR #74–#76.

## Goal
Close `AUD-HC-018` through `AUD-HC-025` using bounded local synthetic/test-only changes before claiming bench runtime maturity.

## Global constraints
- No real-farm data.
- No live RFID hardware.
- No real KVK I/O or machine CAN/RS485/Modbus/serial.
- No commands/writes/configuration/actuation, hydraulics or PLC/safety mutation.
- No network/cloud, external report delivery, deployment, signing, release or public distribution.
- TDD is mandatory for runtime changes: RED → minimal GREEN → full runtime-ci/docs-ci → reconciliation.

## R2-A — HMI navigation and geometry (`AUD-HC-018`, `AUD-HC-019`)
- implement intentional `back` and `open_reports` semantics or remove unsupported actions from the public layout;
- establish concrete 1024×600 widget coordinates;
- validate screen fit, minimum spacing, no overlap, visibility and touch-target geometry;
- keep GL100E physical verification separate from synthetic geometry PASS.

## R2-B — Observation provenance and allowlisted capabilities (`AUD-HC-020`, `AUD-HC-021`)
- define typed observation envelopes with timestamp, source identity, quality and staleness state;
- make HMI/application action surfaces explicit allowlists;
- fail closed on unknown/exported actions;
- verify absence of machine-control capabilities by enumerating exported surfaces, not by a finite denylist only.

## R2-C — CI and semantic documentation quality (`AUD-HC-022`, `AUD-HC-023`)
- run runtime regression on `main` as well as PRs;
- add bounded static quality checks appropriate to this Python repository;
- add coverage reporting without introducing false hardening claims;
- strengthen docs-ci with semantic checks for lifecycle status, authority state, selected hardware profile and traceability consistency.

## R2-D — Reproducible local runtime packaging and RFID identity truth (`AUD-HC-024`, `AUD-HC-025`)
- define a local executable/package entrypoint and configuration schema for the bench application host without choosing or deploying a physical edge host;
- define reproducible local launch/recovery procedure and package verification;
- make simulated RFID identity resolution use the observation payload as source of truth;
- fail closed on mismatch/conflict between requested identity and observed RFID identity.

## Exit criteria
Wave R2 may close only when `AUD-HC-018`–`AUD-HC-025` each have automated evidence, documentation reconciliation, runtime-ci and docs-ci green, while HW-A1/HW-A2/HW-A3 and native DTools/edge-host dependencies remain truthfully separate.
