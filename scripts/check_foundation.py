from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/foundation/FND-HC-001_Project_Foundation_v0.1.md"),
    Path("planning/ROADMAP-HC-001.md"),
    Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md"),
    Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md"),
    Path("project_context/CURRENT_STATE.md"),
    Path("docs/traceability/HC-TRACE-001_Traceability.md"),
    Path("docs/requirements/REQ-HC-001_Implementable_Requirements_v0.1.md"),
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
    "F80 / BENCH IMPLEMENTATION — S5 LOCAL CANONICAL PDF REPORTING IN PROGRESS",
    "e4d7d3b21e8baa17c239c6008fdac17a7cbe2e34",
    "IA-HC-001`: `ACTIVE`",
    "HC-S5-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "network/cloud delivery",
    "live KVK I/O of any kind",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace_text = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "HC-S4-DASH-001",
    "HC-S5-RED-001",
    "HC-S5-CANON-001",
    "HC-S5-PROV-001",
    "HC-S5-AUDIENCE-001",
    "HC-S5-DISCLAIMER-001",
    "HC-S5-LOCALPDF-001",
]:
    if marker not in trace_text:
        errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("governance, S4 checkpoint and S5 local reporting traceability checks passed")
