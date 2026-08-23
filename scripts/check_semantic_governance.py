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
    job_plan = Path("planning/IMP-UX-HC-001_Role_Based_Menu_Job_Settlement_and_Statistics_v0.1.md").read_text(encoding="utf-8")
    job_authority = Path("governance/IA-HC-007_Role_Based_Jobs_Settlement_and_Statistics_Authority_v0.1.md").read_text(encoding="utf-8")
    job_activation_path = Path("governance/HC-IA-HC-007-ACTIVATION-001.md")
    job_activation = job_activation_path.read_text(encoding="utf-8") if job_activation_path.is_file() else ""
    job_reconciliation_path = Path("docs/reconciliation/HC-UX-HC-001-POST-MERGE-RECON-001.md")
    job_reconciliation = job_reconciliation_path.read_text(encoding="utf-8") if job_reconciliation_path.is_file() else ""
    pricing_authority = Path("governance/IA-HC-007-A1_Zootechnician_Pricing_Access_Amendment_v0.1.md").read_text(encoding="utf-8")
    pricing_activation_path = Path("governance/HC-IA-HC-007-A1-ACTIVATION-001.md")
    pricing_activation = pricing_activation_path.read_text(encoding="utf-8") if pricing_activation_path.is_file() else ""

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

    expected_job_plan_status = "APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-ACTIVATION-001"
    expected_job_authority_status = "APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-ACTIVATION-001"
    if status_line(job_plan) != expected_job_plan_status:
        errors.append(
            f"IMP-UX-HC-001 status conflict: expected {expected_job_plan_status!r}, got {status_line(job_plan)!r}"
        )
    if status_line(job_authority) != expected_job_authority_status:
        errors.append(
            f"IA-HC-007 status conflict: expected {expected_job_authority_status!r}, got {status_line(job_authority)!r}"
        )
    if not job_activation_path.is_file():
        errors.append("IA-HC-007 activation record missing")
    else:
        require(job_activation, "MERGED / REPOSITORY VERIFIED — IA-HC-007 PROSPECTIVELY ACTIVE", "HC-IA-HC-007-ACTIVATION-001", errors)
        require(job_activation, "8901922380a3ec342747088e5acccdcd4ca5b44d", "HC-IA-HC-007-ACTIVATION-001", errors)
        require(job_activation, "3a32e3b5b7d1f5b2693836c044ef73caa63276d3", "HC-IA-HC-007-ACTIVATION-001", errors)
    if not job_reconciliation_path.is_file():
        errors.append("IA-HC-007 post-merge reconciliation record missing")
    else:
        require(job_reconciliation, "REPOSITORY VERIFIED / IA-HC-007 PROSPECTIVELY ACTIVE", "HC-UX-HC-001-POST-MERGE-RECON-001", errors)
        require(job_reconciliation, "3a32e3b5b7d1f5b2693836c044ef73caa63276d3", "HC-UX-HC-001-POST-MERGE-RECON-001", errors)

    require(current, "`IMP-UX-HC-001`: `APPROVED / ACTIVE`", "CURRENT_STATE", errors)
    require(current, "`IA-HC-007`: `APPROVED / ACTIVE", "CURRENT_STATE", errors)
    require(trace, "| HC-IA-007 | Job settlement authority | IA-HC-007 | APPROVED / ACTIVE |", "HC-TRACE-001", errors)
    require(job_authority, "REQ-HC-002", "IA-HC-007", errors)
    for forbidden_boundary in (
        "real-farm",
        "live RFID",
        "real KVK I/O",
        "PLC/safety mutation",
        "network/cloud",
        "invoicing",
        "public distribution",
    ):
        require(job_authority, forbidden_boundary, "IA-HC-007", errors)

    expected_pricing_authority_status = (
        "APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-A1-ACTIVATION-001"
    )
    if status_line(pricing_authority) != expected_pricing_authority_status:
        errors.append(
            "IA-HC-007-A1 status conflict: expected "
            f"{expected_pricing_authority_status!r}, got {status_line(pricing_authority)!r}"
        )
    if not pricing_activation_path.is_file():
        errors.append("IA-HC-007-A1 activation record missing")
    else:
        require(
            pricing_activation,
            "MERGED / REPOSITORY VERIFIED — IA-HC-007-A1 PROSPECTIVELY ACTIVE",
            "HC-IA-HC-007-A1-ACTIVATION-001",
            errors,
        )
        require(pricing_activation, "fe5bc6f2c405415aa85251399334d5b335bddf0b", "HC-IA-HC-007-A1-ACTIVATION-001", errors)
        require(pricing_activation, "5cde8249336e45db373fbcb165369f7f18af31c5", "HC-IA-HC-007-A1-ACTIVATION-001", errors)
        require(pricing_activation, "1c6a2756ebb4f9c04b4ca4928b3671ea339f6b80", "HC-IA-HC-007-A1-ACTIVATION-001", errors)
        require(pricing_activation, "RUNTIME NOT STARTED", "HC-IA-HC-007-A1-ACTIVATION-001", errors)
    require(current, "`IA-HC-007-A1`: `APPROVED / ACTIVE", "CURRENT_STATE", errors)
    require(trace, "| HC-IA-007-A1 | Zootechnician pricing authority amendment | IA-HC-007-A1 | APPROVED / ACTIVE |", "HC-TRACE-001", errors)

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
