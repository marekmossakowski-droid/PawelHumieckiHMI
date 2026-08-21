from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/foundation/FND-HC-001_Project_Foundation_v0.1.md"),
    Path("planning/ROADMAP-HC-001.md"),
    Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md"),
    Path("project_context/CURRENT_STATE.md"),
    Path("docs/traceability/HC-TRACE-001_Traceability.md"),
    Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md"),
]
REQ = Path("docs/requirements/REQ-HC-001_Implementable_Requirements_v0.1.md")
IMP = Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md")
IA = Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md")

errors: list[str] = []
for path in REQUIRED:
    if not path.is_file():
        errors.append(f"missing required artifact: {path}")

for path in Path(".").rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if "\\n" in text:
        errors.append(f"literal \\n sequence found in markdown: {path}")

current = Path("project_context/CURRENT_STATE.md")
if current.is_file():
    text = current.read_text(encoding="utf-8")
    for marker in [
        "F70 / IMPLEMENTATION PLAN + AUTHORITY GATE — IN PROGRESS",
        "HC-REQ-001",
        "e34e2a2ae3f709d83c24d528f8930b1b72060961",
        "IA-HC-001`: proposed; `NOT ACTIVE`",
        "Runtime implementation authority: `NOT ESTABLISHED`",
    ]:
        if marker not in text:
            errors.append(f"CURRENT_STATE missing marker: {marker}")

if REQ.is_file():
    req_text = REQ.read_text(encoding="utf-8")
    for marker in ["REQ-HC-SES-003", "REQ-HC-ID-003", "REQ-HC-HMI-007", "REQ-HC-KVK-002", "REQ-HC-MVP-006"]:
        if marker not in req_text:
            errors.append(f"Requirements missing marker: {marker}")

if IMP.is_file():
    imp_text = IMP.read_text(encoding="utf-8")
    for marker in [
        "S1 — Domain/session core",
        "S4 — HMI prototype workflow",
        "S6 — Simulated adapters",
        "TDD rule",
        "No live KVK connection",
        "IA-HC-001",
        "PROPOSED — PROJECT OWNER APPROVAL REQUIRED",
    ]:
        if marker not in imp_text:
            errors.append(f"Implementation plan missing marker: {marker}")

if IA.is_file():
    ia_text = IA.read_text(encoding="utf-8")
    for marker in [
        "PROPOSED — PROJECT OWNER APPROVAL REQUIRED",
        "simulated KVK state inputs",
        "live write access to any KVK controller",
        "automatic veterinary diagnosis",
        "becomes `ACTIVE` only after explicit Project Owner approval",
    ]:
        if marker not in ia_text:
            errors.append(f"Implementation Authority missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md")
if trace.is_file():
    trace_text = trace.read_text(encoding="utf-8")
    for marker in ["HC-REQ-SES-001", "HC-REQ-KVK-001", "HC-IMP-001", "HC-IA-001"]:
        if marker not in trace_text:
            errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("governance through implementation planning documentation checks passed")
