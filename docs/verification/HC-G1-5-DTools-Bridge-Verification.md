# HC-G1-5 Kinco DTools Bridge — verification record

Date: 2026-08-24

Scope: synthetic/test-only `HoofCare_GL100E_G1` under IA-HC-008

Platforms of this record: Linux development environment and approved Windows 11
read-only trial against Kinco DTools V4.5.

## Implemented boundary

- local MCP v2 `stdio` transport only;
- exact project name, selected executable path and executable SHA-256;
- installed v0.1.10 launcher is forced into `--read-only` mode and exposes only
  `dtools_status`, `dtools_inspect` and `dtools_capture`;
- the non-read-only catalog remains outside this approved trial and is not
  exposed by the installed launcher;
- permanent denial for download, upload, transfer, PLC, KVK, device, Ethernet, USB and COM targets;
- one action followed by literal postcondition verification;
- append-only redacted JSONL audit and DTools-window evidence;
- no global emergency hotkey registration in the read-only launcher because no
  state-changing tool is exposed;
- per-user installation under `%LOCALAPPDATA%\HoofCare\DToolsBridge`.

## Local evidence

| Check | Result |
|---|---|
| Focused policy/session/audit/controller/MCP tests | PASS |
| Clean tracked suite | PASS — 239 tests, 5 Windows-only skipped |
| MCP SDK used for local contract verification | `mcp==2.0.0` |
| Python | `3.12` local; package target `3.13` |
| Windows emulator integration | PASS — completed by the Windows build script |
| Windows v0.1.10 build and per-user install | PASS — `BUILD_OK`, `INSTALL_OK` |
| Windows MCP startup | PASS — local STDIO server connected in Codex |
| Real DTools read-only capture | PASS — `main_editor`, mechanism `WIN32` |
| Evidence archive SHA-256 | `d4e7d5639a4e37a5249c36d29419e2612b954b5ec79bae3af15c05558ebacb06` |
| Approved source head | `e30362d7cf206bf02e28601635b47c4a1b27bc87` |

## Windows read-only trial evidence

Project Owner decision: `PASS`, approved on 2026-08-24 for the exact source head
above, without any extension to save, PLC, KVK or device access.

Evidence archive supplied by the Project Owner:

- file: `HoofCare_DTools_Evidence_v0110.zip`;
- SHA-256: `d4e7d5639a4e37a5249c36d29419e2612b954b5ec79bae3af15c05558ebacb06`;
- session: `48e2f76438df49b58211e6dfed157832`;
- operation: `1`, tool `capture`, decision `ALLOW`, result `OK`;
- exact project: `HoofCare_GL100E_G1`;
- observed precondition and postcondition: `main_editor`;
- captured DTools window: `1920x1009`, RGB PNG;
- before/after SHA-256:
  `b9b53ec6cd382330680e1fe4771ea775f9409d25b3e79702630b36417b0fe444`;
- before and after are byte-identical, as expected for a read-only capture;
- visual inspection confirms the Kinco DTools main editor and the synthetic
  `HoofCare_GL100E_G1` project tree;
- audit contains no save, transfer, PLC, KVK or device operation.

## Mandatory scope statements

`REAL_DTOOLS_PROBE=PASS_READ_ONLY`

`PROJECT_SAVE=NOT_AUTHORIZED`

`DEVICE_ACCESS=NONE`

`PLC_ACCESS=NONE`

`KVK_ACCESS=NONE`

The production `load_g1_00_bitmap` step remains `PROFILE_STEP_UNVERIFIED` and
fail-closed until a read-only inspection of the real DTools UI establishes the
exact semantic control path. The emulator path is test-only.
