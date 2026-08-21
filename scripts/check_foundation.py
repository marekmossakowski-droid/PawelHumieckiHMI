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
    "F80 / BENCH IMPLEMENTATION — S2 DURABLE LOCAL PERSISTENCE IN PROGRESS",
    "7467ec4e30b5ecd8831c094bd90ba7d1fe0ad7b2",
    "IA-HC-001`: `ACTIVE`",
    "ESTABLISHED — BOUNDED BENCH ONLY",
    "HC-S2-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "live KVK I/O of any kind",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

ia_text = Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "ACTIVE — APPROVED BY PROJECT OWNER / PR #8",
    "9c939abea6794e2b5a4815c826410eb0166ab535",
    "0d58eb2921df298114c304295a061547598ae541",
    "live KVK I/O of any kind",
    "automatic veterinary diagnosis",
]:
    if marker not in ia_text:
        errors.append(f"Implementation Authority missing marker: {marker}")

trace_text = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "HC-S1-CORE-001",
    "HC-S2-RED-001",
    "HC-S2-STORE-001",
    "HC-S2-RECOVERY-001",
    "HC-S2-ATOMIC-001",
    "HC-S2-AUDIT-001",
    "HC-S2-FAILCLOSED-001",
]:
    if marker not in trace_text:
        errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("governance, active bench authority, S1 checkpoint and S2 persistence traceability checks passed")
