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
ARB = Path("docs/architecture/ARB-HC-001_System_Boundaries_v0.1.md")
SA = Path("docs/architecture/SA-HC-001_System_Architecture_v0.1.md")
LEL = Path("docs/architecture/LEL-HC-001_Logical_Event_Lifecycle_v0.1.md")
REQ = Path("docs/requirements/REQ-HC-001_Implementable_Requirements_v0.1.md")
ADR_FILES = [Path(f"docs/architecture/ADR-HC-00{i}_{name}_v0.1.md") for i, name in [
    (1, "HMI_Edge_Responsibility_Split"),
    (2, "KVK_Read_Only_Integration"),
    (3, "Animal_Identity_Strategy"),
    (4, "Media_Acquisition_and_Storage"),
    (5, "Local_Persistence_and_Backup"),
    (6, "Veterinary_Nomenclature_Baseline"),
    (7, "Report_Generation_Architecture"),
]]

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
        errors.append("CURRENT_STATE must keep IA-HC-001 proposed and NOT ACTIVE")
    if "Runtime implementation authority: `NOT ESTABLISHED`" not in text and "Runtime implementation authority: NOT ESTABLISHED" not in text:
        errors.append("CURRENT_STATE must state runtime implementation authority is not established")
    if "HC-LEL-001" not in text or "a7d031317cf25934218cd09a4916449f2bf5b634" not in text:
        errors.append("CURRENT_STATE must record canonical LEL merge checkpoint")

if ARS.is_file():
    ars_text = ARS.read_text(encoding="utf-8")
    for marker in ["ARS-HC-OP-002", "ARS-HC-VET-002", "ARS-HC-SAF-001"]:
        if marker not in ars_text:
            errors.append(f"ARS missing marker: {marker}")

if ARB.is_file():
    arb_text = ARB.read_text(encoding="utf-8")
    for marker in ["ARB-HC-KVK-001", "ARB-HC-KVK-003", "ARB-HC-CLIN-001"]:
        if marker not in arb_text:
            errors.append(f"ARB missing marker: {marker}")

for path in ADR_FILES:
    if not path.is_file():
        errors.append(f"missing ADR: {path}")
    else:
        text = path.read_text(encoding="utf-8")
        if "APPROVED / BASELINED — PR #4" not in text:
            errors.append(f"ADR must record approved/baselined status: {path}")
        if "c2493ef39a1b45b934cd2dc001279db110a17fc0" not in text:
            errors.append(f"ADR must record canonical PR #4 merge SHA: {path}")

if SA.is_file():
    sa_text = SA.read_text(encoding="utf-8")
    for marker in ["SA-HC-C01", "SA-HC-C02", "SA-HC-C06", "no write path", "IDENTITY_PENDING"]:
        if marker not in sa_text:
            errors.append(f"System Architecture missing marker: {marker}")

if LEL.is_file():
    lel_text = LEL.read_text(encoding="utf-8")
    for marker in ["LEL-HC-I01", "LEL-HC-C01", "LEL-HC-T02", "LEL-HC-KVK-001", "LEL-HC-D02", "LEL-HC-D03", "IDENTITY_PENDING", "SESSION_COMPLETED"]:
        if marker not in lel_text:
            errors.append(f"LEL missing marker: {marker}")

if REQ.is_file():
    req_text = REQ.read_text(encoding="utf-8")
    for marker in [
        "REQ-HC-SES-003",
        "REQ-HC-ID-003",
        "REQ-HC-HMI-007",
        "REQ-HC-CLIN-005",
        "REQ-HC-KVK-002",
        "REQ-HC-KVK-005",
        "REQ-HC-REP-002",
        "REQ-HC-MVP-006",
        "PROJECT OWNER APPROVAL REQUIRED",
    ]:
        if marker not in req_text:
            errors.append(f"Requirements missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md")
if trace.is_file():
    trace_text = trace.read_text(encoding="utf-8")
    for marker in ["HC-LEL-001", "HC-LEL-006", "HC-REQ-SES-001", "HC-REQ-KVK-001", "HC-REQ-MVP-001"]:
        if marker not in trace_text:
            errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("governance through implementable requirements documentation checks passed")
