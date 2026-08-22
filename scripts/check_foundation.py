from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"), Path("README.md"),
    Path("docs/foundation/FND-HC-001_Project_Foundation_v0.1.md"),
    Path("planning/ROADMAP-HC-001.md"),
    Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md"),
    Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md"),
    Path("governance/HC-IA-HC-002-ACTIVATION-001.md"),
    Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md"),
    Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md"),
    Path("docs/closure/HC-PHYSICAL-PROTOTYPE-CLOSURE-001.md"),
    Path("docs/prototype/HC-P3-001_Bench_Wiring_BOM.md"),
    Path("docs/reconciliation/HC-P3-POST-MERGE-RECON-001.md"),
    Path("docs/reconciliation/HC-P4-POST-MERGE-RECON-001.md"),
    Path("project_context/CURRENT_STATE.md"),
    Path("docs/traceability/HC-TRACE-001_Traceability.md"),
]
errors: list[str] = []
for path in REQUIRED:
    if not path.is_file(): errors.append(f"missing required artifact: {path}")
for path in Path(".").rglob("*.md"):
    if "\\n" in path.read_text(encoding="utf-8"):
        errors.append(f"literal \\n sequence found in markdown: {path}")

current = Path("project_context/CURRENT_STATE.md").read_text(encoding="utf-8")
for marker in [
    "P1-P7 MERGED / VERIFIED / CLOSURE READY",
    "7e3f4e573bead9664e39422a97ab6cc3ddbb2c41",
    "HC-PHYSICAL-PROTOTYPE-CLOSURE-001",
    "IA-HC-002`: nadal `APPROVED / ACTIVE`",
    "field_kvk_verified = false",
    "deployment_ready = false",
]:
    if marker not in current: errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P1-P7 MERGED / VERIFIED / PHYSICAL PROTOTYPE CLOSURE READY",
    "c6083495296a59835a427f035a11ecd859f5be6f",
    "7e3f4e573bead9664e39422a97ab6cc3ddbb2c41",
    "HC-CLOSURE-002",
]:
    if marker not in trace: errors.append(f"traceability missing marker: {marker}")

physical_closure = Path("docs/closure/HC-PHYSICAL-PROTOTYPE-CLOSURE-001.md").read_text(encoding="utf-8")
for marker in [
    "PROPOSED — PROJECT OWNER APPROVAL REQUIRED",
    "P1–P7: `MERGED / VERIFIED`",
    "field_kvk_verified = false",
    "FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE",
]:
    if marker not in physical_closure: errors.append(f"physical closure missing marker: {marker}")

bench_closure = Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md").read_text(encoding="utf-8")
if "CLOSED / IMPLEMENTED / VERIFIED / RECONCILED" not in bench_closure:
    errors.append("bench closure record must remain reconciled closed")

ia2 = Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in ["APPROVED / ACTIVE", "Fail-closed rule"]:
    if marker not in ia2: errors.append(f"IA-HC-002 missing marker: {marker}")

if errors:
    for error in errors: print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)
print("physical prototype P1-P7 verified and closure-ready governance checks passed")
