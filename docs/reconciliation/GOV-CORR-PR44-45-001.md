# GOV-CORR-PR44-45-001 — Restore last Project Owner-approved checkpoint

Status: DOCUMENTATION-ONLY / MERGE APPROVAL REQUIRED

## Established fact
The last Project Owner-approved repository checkpoint is PR #43 merge `e6b62b4ffaf73103d57af24b8b60b5886643bb1c`, whose tree is `c3bb64e394df8bb287fef5108dffa9210d8d4cb6`.

PR #44 and PR #45 were merged without a new Project Owner exact-head approval in the active conversation lineage. Their resulting lifecycle/runtime changes are therefore not accepted as authority lineage.

## Correction
This branch restores exactly the tree of the last approved checkpoint after PR #43. It introduces no new runtime or hardware behavior and does not authorize P5 or P6.

## Explicit exclusions
No real KVK I/O, live RFID or real-farm data, machine CAN/RS-485/Modbus/serial, KVK commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, network/cloud exposure, deployment, signing, release or public distribution.
