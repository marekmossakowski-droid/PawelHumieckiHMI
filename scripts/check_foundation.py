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
    "F80 / BENCH IMPLEMENTATION — S3 LOCAL HMI-EDGE CONTRACT IN PROGRESS",
    "c5f60dbf11b04b680c6f51f2e610d33906b08637",
    "IA-HC-001`: `ACTIVE`",
    "ESTABLISHED — BOUNDED BENCH ONLY",
    "HC-S3-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "live KVK I/O of any kind",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

ia_text = Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "ACTIVE — APPROVED BY PROJECT OWNER / PR #8",
    "0d58eb2921df298114c304295a061547598ae541",
    "live KVK I/O of any kind",
    "automatic veterinary diagnosis",
]:
    if marker not in ia_text:
        errors.append(f"Implementation Authority missing marker: {marker}")

trace_text = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "HC-S2-STORE-001",
    "HC-S3-RED-001",
    "HC-S3-CONTRACT-001",
    "HC-S3-IDEMP-001",
    "HC-S3-FAILCLOSED-001",
    "HC-S3-NOACT-001",
]:
    if marker not in trace_text:
        errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("governance, active bench authority, S2 checkpoint and S3 contract traceability checks passed")
