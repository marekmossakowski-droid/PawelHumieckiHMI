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
    "F90 / PHYSICAL PROTOTYPE — P6 PERSISTENCE/REPORTING VALIDATION IN PROGRESS",
    "ce452c747be020075c7d447d004948040675cd63",
    "HC-P1-001` through `HC-P5-001`: `MERGED / VERIFIED`",
    "HC-P6-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "IA-HC-002`: `ACTIVE`",
    "Physical/live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P5 Physical navigation/state binding",
    "ce452c747be020075c7d447d004948040675cd63",
    "P6 Physical persistence/reporting validation",
    "3c541bb308a4ff1ad68cec0198323fbc6ca2696a",
    "41dac94a62e0aecf946b60cd6bd1dfa39442c4ef",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("active IA-HC-002, P5 merge and P6 persistence/reporting validation checks passed")
