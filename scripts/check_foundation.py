from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/foundation/FND-HC-001_Project_Foundation_v0.1.md"),
    Path("planning/ROADMAP-HC-001.md"),
    Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md"),
    Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md"),
    Path("governance/HC-IA-HC-002-ACTIVATION-001.md"),
    Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md"),
    Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md"),
    Path("project_context/CURRENT_STATE.md"),
    Path("docs/traceability/HC-TRACE-001_Traceability.md"),
    Path("src/hoofcare/physical/prototype_validation.py"),
    Path("tests/test_physical_persistence_reporting_validation.py"),
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
    "P5 MERGED / VERIFIED / P6 IMPLEMENTED / GREEN",
    "0676c5dd2f68f0e7a9322b003b1fa2da861d506e",
    "02e1468e6b3103f23fecabee7b25862647f0bd62",
    "0e002a4f336f87a14cf377e56d390e2da57746fc",
    "IA-HC-002`: `APPROVED / ACTIVE`",
    "Any live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P1-P5 MERGED / VERIFIED / P6 IMPLEMENTED / GREEN",
    "0d2d38dcff7c5492145e7d106ff0c18c139d2c23",
    "20a2a7324e76a2feeedfe5a864320159f36b82d4",
    "02e1468e6b3103f23fecabee7b25862647f0bd62",
    "0e002a4f336f87a14cf377e56d390e2da57746fc",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

closure = Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md").read_text(encoding="utf-8")
if "CLOSED / IMPLEMENTED / VERIFIED / RECONCILED" not in closure:
    errors.append("closure record must be reconciled closed")

ia2 = Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in ["APPROVED / ACTIVE", "3eb278f7a480734045027393a53a76f6cdc03f03", "any electrical connection to the real KVK 801-1", "Fail-closed rule"]:
    if marker not in ia2:
        errors.append(f"IA-HC-002 missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("bench MVP closure, active IA-HC-002, merged P5 and green P6 checks passed")
