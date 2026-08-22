# HC-HW-A1 — Goods-in Verification Checklist v0.1

## Status
`READY FOR EXECUTION — REQUIRES PHYSICAL HARDWARE`

## Scope
Checklist for receipt verification of the isolated bench hardware authorized by `IA-HC-003`. This checklist does not authorize any connection to the real KVK 801-1.

## Required items
1. Kinco `GL100E` HMI.
2. Kinco `KS123-14DR` I/O module.
3. Existing isolated 24 VDC bench source — power-up belongs to HW-A2, not HW-A1.
4. Passive wiring / terminals / protection / test loads as available.

RFID is deferred and not part of HW-A1.

## Evidence to capture before power-up
### GL100E
- front photo;
- rear photo;
- manufacturer label / exact model;
- serial number or other unit identifier if present;
- visible 24 VDC power terminals;
- visible COM/RS485 terminals or connector labels;
- Ethernet/USB interfaces;
- mounting clips/accessories received;
- visible damage check.

### KS123-14DR
- front photo;
- side/back photo where applicable;
- manufacturer label / exact model;
- serial/unit identifier if present;
- visible 24 VDC power terminals;
- visible RS485 terminals;
- DI terminal group;
- relay DO terminal group;
- terminal blocks/accessories received;
- visible damage check.

## Acceptance gates
All of the following must be true before HW-A1 may be marked `PASSED`:
- exact HMI model is `GL100E`;
- exact I/O model is `KS123-14DR`;
- no shipping damage that may make energization unsafe;
- power terminal identification is unambiguous;
- RS485 terminal identification is unambiguous or official documentation is available;
- no machine/KVK cable is attached;
- no real-farm data is present in captured evidence;
- hardware evidence is sufficient to prepare the HW-A2 wiring sheet.

## Fail-closed conditions
HW-A1 = `FAILED / HOLD` if:
- model differs from selected hardware profile;
- label or terminal identity is ambiguous;
- enclosure/connector/terminal damage is visible;
- supplied voltage requirements are unclear;
- a proposed cable could connect to the real KVK;
- evidence contains real animal/farm identity data.

No power shall be applied under HW-A1.

## Evidence naming
Suggested filenames:
- `HW-A1_GL100E_FRONT.jpg`
- `HW-A1_GL100E_REAR.jpg`
- `HW-A1_GL100E_LABEL.jpg`
- `HW-A1_KS12314DR_FRONT.jpg`
- `HW-A1_KS12314DR_LABEL.jpg`
- `HW-A1_KS12314DR_TERMINALS.jpg`
- `HW-A1_ACCESSORIES.jpg`

## Exit
Positive evidence review establishes:
`HW-A1 = PASSED / VERIFIED`

Only then may execution proceed to:
`HW-A2 — Isolated 24 VDC bench wiring`.
