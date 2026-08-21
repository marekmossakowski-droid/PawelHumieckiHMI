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
    "F80 / BENCH IMPLEMENTATION — S1 DOMAIN/SESSION CORE IN PROGRESS",
    "0d58eb2921df298114c304295a061547598ae541",
    "IA-HC-001`: `ACTIVE`",
    "ESTABLISHED — BOUNDED BENCH ONLY",
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

imp_text = Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "APPROVED / BASELINED — PR #8",
    "S1 — Domain/session core",
    "S4 — HMI prototype workflow",
    "S6 — Simulated adapters",
    "TDD rule",
    "No live KVK connection",
]:
    if marker not in imp_text:
        errors.append(f"Implementation plan missing marker: {marker}")

trace_text = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "HC-IA-001",
    "HC-S1-RED-001",
    "HC-S1-CORE-001",
    "HC-S1-FAILCLOSED-001",
    "HC-S1-IDEMP-001",
    "HC-S1-TERM-001",
]:
    if marker not in trace_text:
        errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("governance, active bench authority and S1 traceability checks passed")
