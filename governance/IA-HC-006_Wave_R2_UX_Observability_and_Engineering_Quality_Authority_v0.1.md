# IA-HC-006 — Wave R2 UX, Observability and Engineering Quality Authority v0.1

## Status
`PROPOSED / NOT ACTIVE — PROJECT OWNER APPROVAL REQUIRED`

## Authorized scope if activated
Bounded local synthetic/test-only remediation of `AUD-HC-018` through `AUD-HC-025` according to `IMP-HC-005`.

Permitted changes if activated:
- HMI navigation semantics and synthetic 1024×600 geometry validation;
- typed simulated observation provenance and quality/staleness metadata;
- explicit allowlisted local HMI/application action surfaces and negative capability tests;
- GitHub Actions/runtime-ci/docs-ci quality improvements limited to repository tests/static checks/coverage/semantic documentation consistency;
- local reproducible Python package/runtime entrypoint, configuration schema and launch/recovery documentation for synthetic bench execution only;
- simulated RFID identity resolution from adapter observation payload with mismatch/conflict fail-closed behavior.

## Explicit exclusions
This authority does not authorize physical HW-A1/HW-A2/HW-A3 PASS, native Kinco DTools artifact generation/upload, selection or deployment of a physical edge host, real-farm data, live RFID hardware, real KVK I/O, machine CAN/RS485/Modbus/serial, commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, network/cloud exposure, external report delivery, deployment/provisioning, signing, release or public distribution.

## Fail-closed rule
Any work that would require a physical device, live bus, real farm identity/data, network service, machine effect, signing/release or an unselected edge host is outside this authority and must stop for separate Project Owner approval.

## Completion condition
May be marked fulfilled only after `AUD-HC-018`–`AUD-HC-025` are individually reconciled with automated evidence and both runtime-ci and docs-ci are green.
