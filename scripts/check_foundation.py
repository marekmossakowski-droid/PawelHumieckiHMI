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
]

ARS = Path("docs/requirements/ARS-HC-001_Application_and_Stakeholder_Requirements_v0.1.md")

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
    if "IA-HC-001`: proposed; `NOT ACTIVE`" not in text and "IA-HC-001`: proposed; NOT ACTIVE" not in text:
        errors.append("CURRENT_STATE must keep IA-HC-001 proposed and NOT ACTIVE before Project Owner approval")
    if "Runtime implementation authority: `NOT ESTABLISHED`" not in text and "Runtime implementation authority: NOT ESTABLISHED" not in text:
        errors.append("CURRENT_STATE must state that runtime implementation authority is not established")

if ARS.is_file():
    ars_text = ARS.read_text(encoding="utf-8")
    required_ars_markers = [
        "ARS-HC-OP-002",
        "ARS-HC-VET-002",
        "ARS-HC-NUT-002",
        "ARS-HC-TECH-001",
        "ARS-HC-SAF-001",
        "ARS-HC-SAF-002",
        "PROJECT OWNER APPROVAL REQUIRED",
    ]
    for marker in required_ars_markers:
        if marker not in ars_text:
            errors.append(f"ARS missing required marker: {marker}")

    trace = Path("docs/traceability/HC-TRACE-001_Traceability.md")
    if trace.is_file():
        trace_text = trace.read_text(encoding="utf-8")
        for marker in ["HC-ARS-OP-001", "HC-ARS-VET-001", "HC-ARS-TECH-001"]:
            if marker not in trace_text:
                errors.append(f"traceability missing ARS marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("governance and requirements documentation checks passed")
