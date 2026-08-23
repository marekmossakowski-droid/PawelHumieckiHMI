from __future__ import annotations

from pathlib import Path
import sys


def require(text: str, marker: str, surface: str, errors: list[str]) -> None:
    if marker not in text:
        errors.append(f"{surface} missing semantic marker: {marker}")


def status_line(text: str) -> str | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == "## Status":
            for candidate in lines[index + 1:]:
                value = candidate.strip()
                if value.startswith("`") and value.endswith("`"):
                    return value.strip("`")
                if value:
                    break
    return None


def main() -> int:
    errors: list[str] = []

    current = Path("project_context/CURRENT_STATE.md").read_text(encoding="utf-8")
    trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
    plan = Path("planning/IMP-HC-005_Wave_R2_UX_Observability_and_Engineering_Quality_v0.1.md").read_text(encoding="utf-8")
    authority = Path("governance/IA-HC-006_Wave_R2_UX_Observability_and_Engineering_Quality_Authority_v0.1.md").read_text(encoding="utf-8")
    recovery_path = Path("governance/HC-IA-HC-006-RECOVERY-ACTIVATION-001.md")
    recovery = recovery_path.read_text(encoding="utf-8") if recovery_path.is_file() else ""
    reconciliation_path = Path("docs/reconciliation/HC-R2-GOVERNANCE-POST-MERGE-RECON-001.md")
    reconciliation = reconciliation_path.read_text(encoding="utf-8") if reconciliation_path.is_file() else ""

    expected_plan_status = "APPROVED / RECOVERY ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-006-RECOVERY-ACTIVATION-001"
    expected_authority_status = "APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-006-RECOVERY-ACTIVATION-001"
    if status_line(plan) != expected_plan_status:
        errors.append(f"IMP-HC-005 status conflict: expected {expected_plan_status!r}, got {status_line(plan)!r}")
    if status_line(authority) != expected_authority_status:
        errors.append(
            f"IA-HC-006 status conflict: expected {expected_authority_status!r}, got {status_line(authority)!r}"
        )
    if not recovery_path.is_file():
        errors.append("IA-HC-006 recovery activation record missing")
    else:
        require(recovery, "nie nadaje authority retroaktywnie", "HC-IA-HC-006-RECOVERY-ACTIVATION-001", errors)
        require(recovery, "PR #77 pozostaje `OPEN / MERGE BLOCKED BY GOVERNANCE RECOVERY`", "HC-IA-HC-006-RECOVERY-ACTIVATION-001", errors)
        require(recovery, "MERGED / VERIFIED — IA-HC-006 PROSPECTIVELY ACTIVE", "HC-IA-HC-006-RECOVERY-ACTIVATION-001", errors)
    if not reconciliation_path.is_file():
        errors.append("IA-HC-006 post-merge reconciliation record missing")
    else:
        require(reconciliation, "f664b680a6507eac4a5ab10dcd2dc7bba4953eb3", "HC-R2-GOVERNANCE-POST-MERGE-RECON-001", errors)
        require(reconciliation, "REPOSITORY VERIFIED / IA-HC-006 PROSPECTIVELY ACTIVE", "HC-R2-GOVERNANCE-POST-MERGE-RECON-001", errors)

    require(current, "`IMP-HC-005`: `APPROVED / RECOVERY ACTIVE`", "CURRENT_STATE", errors)
    require(current, "`IA-HC-006`: `APPROVED / ACTIVE", "CURRENT_STATE", errors)
    require(trace, "| HC-IA-006 | Wave R2 recovery authority | IA-HC-006 | APPROVED / ACTIVE |", "HC-TRACE-001", errors)

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
        "real-farm data",
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
