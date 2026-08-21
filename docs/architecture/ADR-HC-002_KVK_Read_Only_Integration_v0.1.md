# ADR-HC-002 — KVK Read-Only Integration Strategy v0.1

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Decision
The first physical integration with the KVK 801-1 SHALL be observational/read-only. HoofCare SHALL consume only machine state needed to support workflow context and diagnostics. No output, command, configuration write, safety dependency or control path to the KVK is permitted under this decision.

The actual electrical/protocol interface remains TBD until physical audit of the user's circa-2013 green KVK 801-1.

## Required properties
- no hidden write path;
- electrical/logical isolation appropriate to the discovered interface;
- loss of HoofCare communication has no effect on KVK safety or operation;
- ambiguous or unverified machine-state data is treated as unavailable, not inferred.

## Deferred choices
PLC vendor, protocol, signal list, isolation hardware and wiring method are downstream of the site audit.
