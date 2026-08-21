from pathlib import Path
import sys

REQUIRED = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/foundation/FND-HC-001_Project_Foundation_v0.1.md"),
    Path("planning/ROADMAP-HC-001.md"),
    Path("governance/IA-HC-001_Initial_Implementation_Authority_v0.1.md"),
    Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md"),
    Path("planning/IMP-HC-001_Bench_MVP_Implementation_Plan_v0.1.md"),
    Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md"),
    Path("docs/prototype/HC-P3-001_Bench_Wiring_BOM.md"),
    Path("project_context/CURRENT_STATE.md"),
    Path("docs/traceability/HC-TRACE-001_Traceability.md"),
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
    "F90 / PHYSICAL PROTOTYPE — P4 SCREEN REALIZATION IN PROGRESS",
    "e26af73899a363543cf889a80a69f076cb370836",
    "HC-P1-001` through `HC-P3-001`: `MERGED / VERIFIED`",
    "HC-P4-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "IA-HC-002`: `ACTIVE`",
    "Paweł Humięcki the best zootechnik",
    "Physical/live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P3 Bench wiring BOM / isolated I/O profile",
    "e26af73899a363543cf889a80a69f076cb370836",
    "P4 Physical screen realization/widget mapping",
    "8c4ca015c2bdaf0983dbb3d9a388b2dd1f48b301",
    "2ef612affa98add3b48f9f43b3df0332916e7c17",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("active IA-HC-002, P3 merge and P4 physical screen realization checks passed")
