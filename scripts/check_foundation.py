from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md"),
    Path("docs/prototype/HC-P3-001_Bench_Wiring_BOM.md"),
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
    "F90 / PHYSICAL PROTOTYPE — P7 ACCEPTANCE / CLOSURE READINESS IN PROGRESS",
    "38122539e9b81f93025b0d88592244152988a676",
    "HC-P1-001` through `HC-P6-001`: `MERGED / VERIFIED`",
    "HC-P7-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "IA-HC-002`: `ACTIVE`",
    "PHYSICAL PROTOTYPE = CLOSURE READY",
    "Physical/live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P6 Physical persistence/reporting validation",
    "38122539e9b81f93025b0d88592244152988a676",
    "P7 Physical prototype acceptance / closure readiness",
    "74ad0ed8833eb686085c21d1470756eb922487a6",
    "dc54408931605e5bfac95ebeb056b669d0f50563",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("active IA-HC-002, P6 merge and P7 physical prototype acceptance checks passed")

# P7 final reconciliation checkpoint.
