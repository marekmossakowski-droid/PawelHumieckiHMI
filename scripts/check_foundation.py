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
    "F90 / PHYSICAL PROTOTYPE — P1 HARDWARE PROFILE IN PROGRESS",
    "36ffda3b2363597b8a8aae3746e9d555450c625c",
    "BENCH MVP`: `CLOSED / IMPLEMENTED / VERIFIED / RECONCILED`",
    "IA-HC-002`: `ACTIVE`",
    "HC-P1-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "Physical/live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

ia2 = Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "ACTIVE — PROJECT OWNER APPROVED VIA PR #17",
    "36ffda3b2363597b8a8aae3746e9d555450c625c",
    "any electrical connection to the real KVK 801-1",
    "Fail-closed rule",
]:
    if marker not in ia2:
        errors.append(f"IA-HC-002 missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("bench MVP closure, active IA-HC-002 and P1 physical prototype checks passed")
