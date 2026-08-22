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
    Path("docs/bench/HC-HW-A1_Goods_In_Verification_Checklist_v0.1.md"),
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
    "IA-HC-003 — Isolated Bench Hardware Assembly Authority`: `APPROVED / ACTIVE`",
    "CURRENT STEP = HW-A1 — GOODS-IN VERIFICATION / WAITING FOR PHYSICAL HARDWARE",
    "Kinco GL100E",
    "Kinco KS123-14DR",
    "field_kvk_verified = false",
    "deployment_ready = false",
    "kvk_connected = false",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "PHYSICAL PROTOTYPE CLOSED",
    "IA-HC-003 ACTIVE",
    "HW-A1 CURRENT",
    "52d65b18f966f553501a7829855f23b7390762a6",
    "HC-IMP-002",
    "HC-IA-003",
    "APPROVED / ACTIVE",
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
    "APPROVED / ACTIVE",
    "52d65b18f966f553501a7829855f23b7390762a6",
    "Kinco GL100E",
    "Kinco KS123-14DR",
    "RFID is explicitly deferred",
    "Fail-closed rule",
]:
    if marker not in ia3:
        errors.append(f"IA-HC-003 missing marker: {marker}")

imp2 = Path("planning/IMP-HC-002_Isolated_Bench_Hardware_Assembly_Plan_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "APPROVED / ACTIVE",
    "HW-A1",
    "HW-A7",
    "GL100E ↔ RS485 / Modbus RTU ↔ KS123-14DR",
    "kvk_connected = false",
]:
    if marker not in imp2:
        errors.append(f"IMP-HC-002 missing marker: {marker}")

hw_a1 = Path("docs/bench/HC-HW-A1_Goods_In_Verification_Checklist_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "READY FOR EXECUTION — REQUIRES PHYSICAL HARDWARE",
    "No power shall be applied under HW-A1",
    "GL100E",
    "KS123-14DR",
    "HW-A2 — Isolated 24 VDC bench wiring",
]:
    if marker not in hw_a1:
        errors.append(f"HW-A1 checklist missing marker: {marker}")

roadmap = Path("planning/ROADMAP-HC-001.md").read_text(encoding="utf-8")
for marker in [
    "F75 — Isolated physical prototype / bench hardware",
    "BLOCKED_BY_SITE_ACCESS",
]:
    if marker not in roadmap:
        errors.append(f"roadmap missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)
print("IA-HC-003 active; HW-A1 goods-in verification waiting for physical hardware; governance checks passed")
