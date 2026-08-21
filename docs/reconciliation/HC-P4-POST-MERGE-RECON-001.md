# HC-P4-POST-MERGE-RECON-001 — Post-merge reconciliation

Status: DOCUMENTATION-ONLY / MERGE APPROVAL REQUIRED

## Established facts
- `HC-P4-001` approved exact head: `5575eabe0543a72e046a4d8bb7425e2ca1f1587d`;
- controlled merge commit: `c5101eb15933bc76b76a86dd3e8ed4f78141875f`;
- `runtime-ci` and `docs-ci` were green on the approved final P4 head before merge;
- `IA-HC-002` remains `APPROVED / ACTIVE` only for isolated off-machine / non-actuating / synthetic-test physical-prototype work.

## Reconciled state after merge
- `HC-P4-001 = MERGED / VERIFIED`;
- physical screen realization remains synthetic/test-only and contains no machine-control surface;
- `HC-P5-001 — Physical navigation and state binding` becomes the next dependency-ordered implementation slice.

## Explicit exclusions
This reconciliation adds no runtime or hardware behavior and does not authorize any electrical/logical connection to the real KVK 801-1, live RFID or real-farm data, machine CAN/RS-485/Modbus/serial, KVK commands/writes/configuration/actuation, hydraulics, PLC/safety mutation, network/cloud exposure, deployment, signing, release or public distribution.
