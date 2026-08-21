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
    "F80 / BENCH MVP — CLOSED / IMPLEMENTED / VERIFIED / RECONCILED PENDING CLOSURE MERGE",
    "0827d0d4b51a0a63c773a1f8ce178d7954dc25a5",
    "HC-S1-001` through `HC-S7-001`: `MERGED / VERIFIED`",
    "IA-HC-002`: `PROPOSED / NOT ACTIVE`",
    "Physical/live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "S7 Bench integration/acceptance",
    "419e513c9fad7f90b52744f811707ca154568362",
    "0827d0d4b51a0a63c773a1f8ce178d7954dc25a5",
    "HC-CLOSURE-001",
    "HC-IA-002",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

closure = Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md").read_text(encoding="utf-8")
if "PROJECT OWNER APPROVAL REQUIRED" not in closure:
    errors.append("closure record must remain approval-gated")

ia2 = Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in ["PROPOSED — NOT ACTIVE", "any electrical connection to the real KVK 801-1", "Fail-closed rule"]:
    if marker not in ia2:
        errors.append(f"IA-HC-002 missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("bench MVP closure and IA-HC-002 proposal governance checks passed")
