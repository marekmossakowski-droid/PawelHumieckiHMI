from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/foundation/FND-HC-001_Project_Foundation_v0.1.md"),
    Path("planning/ROADMAP-HC-001.md"),
    Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md"),
    Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md"),
    Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md"),
    Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md"),
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
    "F90 / PHYSICAL PROTOTYPE — P5 NAVIGATION/STATE BINDING IN PROGRESS",
    "53b0f718892eaba1e9478cce76c5369a1b173794",
    "HC-P1-001` through `HC-P4-001`: `MERGED / VERIFIED`",
    "HC-P5-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "IA-HC-002`: `ACTIVE`",
    "Physical/live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P4 Physical screen realization/widget mapping",
    "53b0f718892eaba1e9478cce76c5369a1b173794",
    "P5 Physical navigation/state binding",
    "5995068062bd21b15702f8bc5a192fb74ca3438b",
    "a00ca743a58ae15b1f95eded4cb94ca50a387c2f",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("active IA-HC-002, P4 merge and P5 navigation/state binding checks passed")
