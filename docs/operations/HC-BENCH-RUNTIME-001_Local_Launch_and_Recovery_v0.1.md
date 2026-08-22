# HC-BENCH-RUNTIME-001 — Local Launch and Recovery v0.1

## Status
`IMPLEMENTED FOR SYNTHETIC/TEST-ONLY BENCH SCOPE`

## Purpose
Defines the reproducible local launch/restart procedure for the HoofCare synthetic bench runtime. This is not a physical edge-host deployment record and does not authorize live KVK or RFID hardware.

## Package / entrypoint
- package metadata: `pyproject.toml`;
- console entrypoint: `hoofcare-bench = hoofcare.runtime.__main__:main`;
- module entrypoint equivalent: `python -m hoofcare.runtime <bench-runtime.json>`.

## Canonical configuration
Schema: `config/bench-runtime.schema.json`.
Example: `config/bench-runtime.example.json`.

Required fail-closed values:
- `mode = SYNTHETIC_TEST_ONLY`;
- `network_enabled = false`;
- `kvk_connected = false`.

Any attempt to enable network or KVK connectivity is rejected before runtime readiness is returned.

## Local launch
From an environment where the repository package is installed or `src` is on the Python path:

`hoofcare-bench config/bench-runtime.example.json`

The launcher creates only the configured local data/report directories and returns a JSON status object. It exposes no network listener and no KVK connection path.

## Restart / recovery
Re-run the same entrypoint with the same canonical configuration. Directory creation is idempotent; existing local data/report directories are reused rather than replaced. Existing persistence recovery semantics remain owned by the local store and are not expanded by this runtime launcher.

## Verification boundary
This procedure closes only the software/package portion of `AUD-HC-024`. It does not establish a physical edge host, HW-A1/HW-A2/HW-A3 PASS, native Kinco DTools artifact, deployment readiness, or production operations.

## Safety boundary
No real-farm data; no live RFID hardware; no real KVK I/O; no machine CAN/RS485/Modbus/serial; no commands/writes/configuration/actuation; no hydraulics; no PLC/safety mutation; no network/cloud; no external report delivery; no deployment/provisioning/signing/release/public distribution.
