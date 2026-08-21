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
    "P5 IMPLEMENTED / GREEN / AWAITING PROJECT OWNER APPROVAL",
    "3f4db8258a85b6e2cc6349a5bb03d982066db732",
    "de8dec19bc820b90bfebe4df669eb661e0af2add",
    "IA-HC-002`: `APPROVED / ACTIVE`",
    "Any live KVK integration remains blocked",
]:
    if marker not in current: errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P5 IMPLEMENTED / GREEN",
    "3f4db8258a85b6e2cc6349a5bb03d982066db732",
    "de8dec19bc820b90bfebe4df669eb661e0af2add",
    "HC-P6-001 — Physical persistence and reporting validation",
]:
    if marker not in trace: errors.append(f"traceability missing marker: {marker}")

closure = Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md").read_text(encoding="utf-8")
if "CLOSED / IMPLEMENTED / VERIFIED / RECONCILED" not in closure:
    errors.append("closure record must be reconciled closed")
ia2 = Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in ["APPROVED / ACTIVE", "Fail-closed rule"]:
    if marker not in ia2: errors.append(f"IA-HC-002 missing marker: {marker}")
if errors:
    for error in errors: print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)
print("bench MVP closure, active IA-HC-002 and HC-P5 GREEN governance checks passed")
