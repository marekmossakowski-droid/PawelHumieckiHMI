from __future__ import annotations

from pathlib import Path
import sys


def require(text: str, marker: str, surface: str, errors: list[str]) -> None:
    if marker not in text:
        errors.append(f"{surface} missing semantic marker: {marker}")


def main() -> int:
    errors: list[str] = []

    current = Path("project_context/CURRENT_STATE.md").read_text(encoding="utf-8")
    trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
    plan = Path("planning/IMP-HC-005_Wave_R2_UX_Observability_and_Engineering_Quality_v0.1.md").read_text(encoding="utf-8")
    authority = Path("governance/IA-HC-006_Wave_R2_UX_Observability_and_Engineering_Quality_Authority_v0.1.md").read_text(encoding="utf-8")

    for marker in (
        "Kinco GL100E",
        "Kinco KS123-14DR",
        "HW-A1",
        "WAITING FOR PHYSICAL HARDWARE",
        "field_kvk_verified = false",
        "deployment_ready = false",
        "kvk_connected = false",
    ):
        require(current, marker, "CURRENT_STATE", errors)

    for marker in ("Kinco GL100E", "Kinco KS123-14DR", "HW-A1"):
        require(trace, marker, "HC-TRACE-001", errors)

    for finding in range(18, 26):
        require(plan, f"AUD-HC-{finding:03d}", "IMP-HC-005", errors)
    for slice_name in ("R2-A", "R2-B", "R2-C", "R2-D"):
        require(plan, slice_name, "IMP-HC-005", errors)

    require(authority, "AUD-HC-018", "IA-HC-006", errors)
    require(authority, "AUD-HC-025", "IA-HC-006", errors)
    for forbidden_boundary in (
        "No real-farm data",
        "real KVK I/O",
        "PLC/safety mutation",
        "network/cloud",
        "signing",
        "public distribution",
    ):
        require(authority, forbidden_boundary, "IA-HC-006", errors)

    forbidden_claims = (
        "HW-A1 = PASS",
        "HW-A2 = PASS",
        "HW-A3 = PASS",
        "deployment_ready = true",
        "kvk_connected = true",
        "field_kvk_verified = true",
    )
    for claim in forbidden_claims:
        if claim in current:
            errors.append(f"CURRENT_STATE contains unauthorized/unevidenced claim: {claim}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("semantic governance consistency checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
