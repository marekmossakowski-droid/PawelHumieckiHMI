from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"), Path("README.md"),
    Path("docs/foundation/FND-HC-001_Project_Foundation_v0.1.md"),
    Path("planning/ROADMAP-HC-001.md"),
    Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md"),
    Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md"),
    Path("governance/HC-IA-HC-002-ACTIVATION-001.md"),
    Path("governance/IA-HC-003_Isolated_Bench_Hardware_Assembly_Authority_v0.1.md"),
    Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md"),
    Path("planning/IMP-HC-002_Isolated_Bench_Hardware_Assembly_Plan_v0.1.md"),
    Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md"),
    Path("docs/closure/HC-PHYSICAL-PROTOTYPE-CLOSURE-001.md"),
    Path("docs/prototype/HC-P3-001_Bench_Wiring_BOM.md"),
    Path("docs/reconciliation/HC-P3-POST-MERGE-RECON-001.md"),
    Path("docs/reconciliation/HC-P4-POST-MERGE-RECON-001.md"),
    Path("project_context/CURRENT_STATE.md"),
    Path("docs/traceability/HC-TRACE-001_Traceability.md"),
]
errors: list[str] = []
for path in REQUIRED:
    if not path.is_file():
        errors.append(f"missing required artifact: {path}")
for path in Path(".").rglob("*.md"):
    if "\\n" in path.read_text(encoding="utf-8"):
        errors.append(f"literal \\n sequence found in markdown: {path}")

current = Path("project_context/CURRENT_STATE.md").read_text(encoding="utf-8")
for marker in [
    "PHYSICAL PROTOTYPE = CLOSED / IMPLEMENTED / VERIFIED / RECONCILED",
    "IA-HC-002`: `FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE`",
    "IA-HC-003 — Isolated Bench Hardware Assembly Authority`: `PROPOSED / NOT ACTIVE`",
    "Kinco GL100E",
    "Kinco KS123-14DR",
    "field_kvk_verified = false",
    "deployment_ready = false",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "PHYSICAL PROTOTYPE CLOSED / IA-HC-002 FULFILLED",
    "ad8b164ce3517064a1de92c986b27a8bfd024b8b",
    "HC-IMP-002",
    "HC-IA-003",
    "PROPOSED / NOT ACTIVE",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

physical_closure = Path("docs/closure/HC-PHYSICAL-PROTOTYPE-CLOSURE-001.md").read_text(encoding="utf-8")
for marker in [
    "CLOSED / IMPLEMENTED / VERIFIED / RECONCILED",
    "ad8b164ce3517064a1de92c986b27a8bfd024b8b",
    "field_kvk_verified = false",
    "FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE",
]:
    if marker not in physical_closure:
        errors.append(f"physical closure missing marker: {marker}")

bench_closure = Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md").read_text(encoding="utf-8")
if "CLOSED / IMPLEMENTED / VERIFIED / RECONCILED" not in bench_closure:
    errors.append("bench closure record must remain reconciled closed")

ia2 = Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in ["FULFILLED FOR AUTHORIZED PHYSICAL-PROTOTYPE SCOPE", "Fail-closed rule"]:
    if marker not in ia2:
        errors.append(f"IA-HC-002 missing marker: {marker}")

ia3 = Path("governance/IA-HC-003_Isolated_Bench_Hardware_Assembly_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "PROPOSED / NOT ACTIVE",
    "Kinco GL100E",
    "Kinco KS123-14DR",
    "RFID is explicitly deferred",
    "Fail-closed rule",
]:
    if marker not in ia3:
        errors.append(f"IA-HC-003 missing marker: {marker}")

imp2 = Path("planning/IMP-HC-002_Isolated_Bench_Hardware_Assembly_Plan_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "PROPOSED / NOT ACTIVE",
    "HW-A1",
    "HW-A7",
    "GL100E ↔ RS485 / Modbus RTU ↔ KS123-14DR",
    "kvk_connected = false",
]:
    if marker not in imp2:
        errors.append(f"IMP-HC-002 missing marker: {marker}")

roadmap = Path("planning/ROADMAP-HC-001.md").read_text(encoding="utf-8")
for marker in [
    "F75 — Isolated physical prototype / bench hardware",
    "ISOLATED BENCH HARDWARE ASSEMBLY READINESS",
    "BLOCKED_BY_SITE_ACCESS",
]:
    if marker not in roadmap:
        errors.append(f"roadmap missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)
print("physical prototype closure reconciled; bench hardware assembly readiness proposed; governance checks passed")
