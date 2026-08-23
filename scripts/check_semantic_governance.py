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
    requirement_trace_path = Path("docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md")
    requirement_trace = requirement_trace_path.read_text(encoding="utf-8") if requirement_trace_path.is_file() else ""
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
    pricing_closure_path = Path("docs/closure/HC-REQ-HC-002-A1-CLOSURE-001.md")
    pricing_closure = pricing_closure_path.read_text(encoding="utf-8") if pricing_closure_path.is_file() else ""
    statistics_plan_path = Path("docs/superpowers/plans/2026-08-23-job-statistics-final-settlement.md")
    statistics_plan = statistics_plan_path.read_text(encoding="utf-8") if statistics_plan_path.is_file() else ""
    statistics_requirement_path = Path("docs/requirements/REQ-HC-002-S1_Job_Statistics_and_Final_Settlement_v0.1.md")
    statistics_authority_path = Path("governance/IA-HC-007-S1_Job_Statistics_and_Final_Settlement_Authority_v0.1.md")
    statistics_decision_path = Path("docs/decisions/HC-REQ-HC-002-S1-PREPARATION-DECISION-001.md")
    statistics_activation_path = Path("governance/HC-IA-HC-007-S1-ACTIVATION-001.md")
    statistics_closure_path = Path("docs/closure/HC-REQ-HC-002-S1-CLOSURE-001.md")
    statistics_closure = statistics_closure_path.read_text(encoding="utf-8") if statistics_closure_path.is_file() else ""
    gen1_decision_path = Path("docs/decisions/HC-REQ-HC-003-G1-PREPARATION-DECISION-001.md")
    gen1_requirement_path = Path("docs/requirements/REQ-HC-003_Generation_1_Complete_HMI_GUI_and_DTools_v0.1.md")
    gen1_design_path = Path("docs/design/UX-HC-002_Generation_1_Complete_HMI_GUI_and_DTools_v0.1.md")
    gen1_plan_path = Path("docs/superpowers/plans/2026-08-24-generation-1-hmi-gui-dtools.md")
    gen1_authority_path = Path("governance/IA-HC-008_Generation_1_HMI_GUI_and_DTools_Authority_v0.1.md")
    gen1_baseline_path = Path("docs/decisions/HC-REQ-HC-003-G1-BASELINE-DECISION-001.md")
    gen1_activation_path = Path("governance/HC-IA-HC-008-ACTIVATION-001.md")

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
    if not pricing_closure_path.is_file():
        errors.append("REQ-HC-002-A1 closure record missing")
    else:
        require(pricing_closure, "CLOSURE READY — PROJECT OWNER MERGE REQUIRED", "HC-REQ-HC-002-A1-CLOSURE-001", errors)
        require(pricing_closure, "8e2b2ed97f73d4f0c7015b189f7f9889e39df3ab", "HC-REQ-HC-002-A1-CLOSURE-001", errors)
        require(pricing_closure, "5cc3f0e8c8fc3ff0181258f2610b04b207784e87", "HC-REQ-HC-002-A1-CLOSURE-001", errors)
    if not statistics_plan_path.is_file():
        errors.append("job statistics and final settlement plan missing")
    else:
        require(statistics_plan, "FULFILLED FOR AUTHORIZED S1 SCOPE — CLOSURE READY / PROJECT OWNER MERGE REQUIRED", "job statistics plan", errors)
        require(statistics_plan, "RAZEM NETTO", "job statistics plan", errors)
        require(statistics_plan, "no VAT, accounting or payment", "job statistics plan", errors)
    require(current, "`REQ-HC-002-A1 closure`: `CLOSURE READY", "CURRENT_STATE", errors)
    require(current, "`Job statistics and final settlement plan`: `FULFILLED FOR AUTHORIZED S1 SCOPE`", "CURRENT_STATE", errors)
    for path, label in (
        (statistics_requirement_path, "REQ-HC-002-S1"),
        (statistics_authority_path, "IA-HC-007-S1"),
        (statistics_decision_path, "HC-REQ-HC-002-S1-PREPARATION-DECISION-001"),
    ):
        if not path.is_file():
            errors.append(f"{label} surface missing")
    if statistics_requirement_path.is_file():
        statistics_requirement = statistics_requirement_path.read_text(encoding="utf-8")
        require(statistics_requirement, "APPROVED / BASELINED", "REQ-HC-002-S1", errors)
        require(statistics_requirement, "RAZEM NETTO", "REQ-HC-002-S1", errors)
    if statistics_authority_path.is_file():
        statistics_authority = statistics_authority_path.read_text(encoding="utf-8")
        require(statistics_authority, "APPROVED / ACTIVE", "IA-HC-007-S1", errors)
        require(statistics_authority, "grants no implementation authority", "IA-HC-007-S1", errors)
    if statistics_decision_path.is_file():
        statistics_decision = statistics_decision_path.read_text(encoding="utf-8")
        require(statistics_decision, "RUNTIME NOT AUTHORIZED", "statistics preparation decision", errors)
        require(statistics_decision, "5a83b305ae35c4550909c5ac717a75d2fa71e3f1", "statistics preparation decision", errors)
    if not statistics_activation_path.is_file():
        errors.append("IA-HC-007-S1 activation record missing")
    else:
        statistics_activation = statistics_activation_path.read_text(encoding="utf-8")
        require(statistics_activation, "97e33d09128f13383e4a57fa2de0217bebef4b19", "IA-HC-007-S1 activation", errors)
        require(statistics_activation, "e51bee95058c6fc4d9766af1467ac31202efc584", "IA-HC-007-S1 activation", errors)
        require(statistics_activation, "RUNTIME NOT STARTED", "IA-HC-007-S1 activation", errors)
    require(current, "`IA-HC-007-S1`: `FULFILLED FOR AUTHORIZED S1 SCOPE`", "CURRENT_STATE", errors)
    if not statistics_closure_path.is_file():
        errors.append("REQ-HC-002-S1 closure record missing")
    else:
        require(statistics_closure, "CLOSURE READY — PROJECT OWNER MERGE REQUIRED", "HC-REQ-HC-002-S1-CLOSURE-001", errors)
        require(statistics_closure, "5c7ac7811fcb524191f226acecfc54f5bb921064", "HC-REQ-HC-002-S1-CLOSURE-001", errors)
        require(statistics_closure, "53c4dbefad383446d4f64fffa52817f690777ec4", "HC-REQ-HC-002-S1-CLOSURE-001", errors)
    require(current, "`REQ-HC-002-S1`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED FOR BOUNDED SYNTHETIC SCOPE`", "CURRENT_STATE", errors)
    require(current, "`IA-HC-007-S1 runtime`: `S1-1/S1-2/S1-3/S1-4 MERGED / REPOSITORY VERIFIED`", "CURRENT_STATE", errors)
    require(current, "`REQ-HC-002-S1 closure`: `MERGED / REPOSITORY VERIFIED VIA PR #100`", "CURRENT_STATE", errors)
    require(trace, "| HC-IA-007-S1 | Job statistics and final settlement authority | IA-HC-007-S1 | FULFILLED FOR AUTHORIZED S1 SCOPE |", "HC-TRACE-001", errors)
    require(trace, "| HC-CLOSE-002-S1 | Bounded statistics and settlement closure | HC-REQ-HC-002-S1-CLOSURE-001 | MERGED / REPOSITORY VERIFIED |", "HC-TRACE-001", errors)

    for path, label in (
        (gen1_decision_path, "HC-REQ-HC-003-G1-PREPARATION-DECISION-001"),
        (gen1_requirement_path, "REQ-HC-003-G1"),
        (gen1_design_path, "UX-HC-002"),
        (gen1_plan_path, "Generation 1 GUI/DTools plan"),
        (gen1_authority_path, "IA-HC-008"),
    ):
        if not path.is_file():
            errors.append(f"{label} surface missing")
    if gen1_decision_path.is_file():
        gen1_decision = gen1_decision_path.read_text(encoding="utf-8")
        require(gen1_decision, "RUNTIME NOT AUTHORIZED", "Generation 1 preparation decision", errors)
        require(gen1_decision, "d2af53d739403ff6f4199fabe43159cb3de10317", "Generation 1 preparation decision", errors)
    if gen1_requirement_path.is_file():
        gen1_requirement = gen1_requirement_path.read_text(encoding="utf-8")
        require(gen1_requirement, "APPROVED / BASELINED — EFFECTIVE AFTER MERGE", "REQ-HC-003-G1", errors)
        require(gen1_requirement, "REQ-HC-G1-DTOOLS-004", "REQ-HC-003-G1", errors)
        if not requirement_trace_path.is_file():
            errors.append("HC-REQ-TRACE-001 surface missing for REQ-HC-003-G1")
        else:
            require(requirement_trace, "| REQ-HC-G1-DTOOLS-004 | PROPOSED / NOT IMPLEMENTED |", "HC-REQ-TRACE-001", errors)
    if gen1_design_path.is_file():
        gen1_design = gen1_design_path.read_text(encoding="utf-8")
        require(gen1_design, "APPROVED / BASELINED — EFFECTIVE AFTER MERGE", "UX-HC-002", errors)
        require(gen1_design, "EDGE_HOST_REQUIRED / NOT YET SELECTED", "UX-HC-002", errors)
        require(gen1_design, "1024×600", "UX-HC-002", errors)
    if gen1_plan_path.is_file():
        gen1_plan = gen1_plan_path.read_text(encoding="utf-8")
        require(gen1_plan, "APPROVED / ACTIVE — EFFECTIVE AFTER MERGE", "Generation 1 GUI/DTools plan", errors)
        require(gen1_plan, "clean assertion RED", "Generation 1 GUI/DTools plan", errors)
        require(gen1_plan, "Task G1-6", "Generation 1 GUI/DTools plan", errors)
    if gen1_authority_path.is_file():
        gen1_authority = gen1_authority_path.read_text(encoding="utf-8")
        expected_gen1_status = "APPROVED / ACTIVE — PROSPECTIVELY AFTER MERGE AND REPOSITORY VERIFICATION OF HC-IA-HC-008-ACTIVATION-001"
        if status_line(gen1_authority) != expected_gen1_status:
            errors.append(f"IA-HC-008 status conflict: expected {expected_gen1_status!r}")
        require(gen1_authority, "Przed merge i Repository Verification", "IA-HC-008", errors)
        for forbidden_boundary in (
            "Generation 2",
            "real data",
            "network/cloud",
            "KVK I/O",
            "PLC/safety mutation",
            "invoicing",
            "public distribution",
        ):
            require(gen1_authority, forbidden_boundary, "IA-HC-008", errors)
    if not gen1_baseline_path.is_file():
        errors.append("REQ-HC-003-G1 baseline decision missing")
    else:
        gen1_baseline = gen1_baseline_path.read_text(encoding="utf-8")
        require(gen1_baseline, "eb41f067d2c0c2c4eeba98c9d8ab4cdae598c361", "REQ-HC-003-G1 baseline", errors)
        require(gen1_baseline, "b25b5ff8a12f2aca37d109a72beaded3130e20ba", "REQ-HC-003-G1 baseline", errors)
    if not gen1_activation_path.is_file():
        errors.append("IA-HC-008 activation record missing")
    else:
        gen1_activation = gen1_activation_path.read_text(encoding="utf-8")
        require(gen1_activation, "f18df0d37df6ff241696822758e14f795107eddd", "IA-HC-008 activation", errors)
        require(gen1_activation, "eb41f067d2c0c2c4eeba98c9d8ab4cdae598c361", "IA-HC-008 activation", errors)
        require(gen1_activation, "b25b5ff8a12f2aca37d109a72beaded3130e20ba", "IA-HC-008 activation", errors)
        require(gen1_activation, "RUNTIME NOT STARTED", "IA-HC-008 activation", errors)
    require(current, "`REQ-HC-003-G1`: `APPROVED / BASELINED PROSPECTIVELY", "CURRENT_STATE", errors)
    require(current, "`IA-HC-008`: `ACTIVATION READY", "CURRENT_STATE", errors)
    require(trace, "| HC-IA-008 | Generation 1 HMI GUI and DTools authority | IA-HC-008 | ACTIVATION READY / OWNER MERGE REQUIRED |", "HC-TRACE-001", errors)

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
