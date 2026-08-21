from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/foundation/FND-HC-001_Project_Foundation_v0.1.md"),
    Path("planning/ROADMAP-HC-001.md"),
    Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md"),
    Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md"),
    Path("governance/HC-IA-HC-002-ACTIVATION-001.md"),
    Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md"),
    Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md"),
    Path("docs/prototype/HC-P3-001_Bench_Wiring_BOM.md"),
    Path("docs/reconciliation/HC-P3-POST-MERGE-RECON-001.md"),
    Path("docs/reconciliation/HC-P4-POST-MERGE-RECON-001.md"),
    Path("project_context/CURRENT_STATE.md"),
    Path("docs/traceability/HC-TRACE-001_Traceability.md"),
]

errors: list[str] = []
for path in REQUIRED:
    if not path.is_file():
        errors.append(f"missing required artifact: {path}")

for path in Path(".").rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if "\\n" in text:
        errors.append(f"literal \\n sequence found in markdown: {path}")

current = Path("project_context/CURRENT_STATE.md").read_text(encoding="utf-8")
for marker in [
    "F90 / PHYSICAL PROTOTYPE — P4 MERGED / VERIFIED / P5 NEXT",
    "c5101eb15933bc76b76a86dd3e8ed4f78141875f",
    "IA-HC-002`: `APPROVED / ACTIVE`",
    "HC-P1-001` through `HC-P4-001`: `MERGED / VERIFIED`",
    "HC-P5-001 — Physical navigation and state binding",
    "Any live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P1-P4 MERGED / VERIFIED / P5 NEXT",
    "13bccf1dafe1d2ebccc509bd0ab4a4f96e4fc0d7",
    "5575eabe0543a72e046a4d8bb7425e2ca1f1587d",
    "c5101eb15933bc76b76a86dd3e8ed4f78141875f",
    "HC-P5-001 — Physical navigation and state binding",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

recon = Path("docs/reconciliation/HC-P4-POST-MERGE-RECON-001.md").read_text(encoding="utf-8")
for marker in [
    "HC-P4-001 = MERGED / VERIFIED",
    "c5101eb15933bc76b76a86dd3e8ed4f78141875f",
    "HC-P5-001 — Physical navigation and state binding",
]:
    if marker not in recon:
        errors.append(f"P4 reconciliation missing marker: {marker}")

closure = Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md").read_text(encoding="utf-8")
if "CLOSED / IMPLEMENTED / VERIFIED / RECONCILED" not in closure:
    errors.append("closure record must be reconciled closed")

ia2 = Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "APPROVED / ACTIVE",
    "3eb278f7a480734045027393a53a76f6cdc03f03",
    "any electrical connection to the real KVK 801-1",
    "Fail-closed rule",
]:
    if marker not in ia2:
        errors.append(f"IA-HC-002 missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("bench MVP closure, active IA-HC-002 and merged HC-P4 governance checks passed")
