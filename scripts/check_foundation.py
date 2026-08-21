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
    "F90 / PHYSICAL PROTOTYPE — P3 BENCH WIRING/BOM IN PROGRESS",
    "0404c45bf7adbdc9e6063501ce5adb7651dd5019",
    "HC-P2-001`: `MERGED / VERIFIED`",
    "HC-P3-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "IA-HC-002`: `ACTIVE`",
    "Physical/live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P2 HMI layout/touch mapping",
    "0404c45bf7adbdc9e6063501ce5adb7651dd5019",
    "P3 Bench wiring BOM / isolated I/O profile",
    "a7f0e9168d6987b9ef0fa642a0d7ec27fddb8375",
    "87e5d5e5da8f491d930375d7bbeed7966e157ddb",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

p3 = Path("docs/prototype/HC-P3-001_Bench_Wiring_BOM.md").read_text(encoding="utf-8")
for marker in ["24 VDC", "8DI/8DO", "no electrical or logical connection to the real KVK 801-1"]:
    if marker not in p3:
        errors.append(f"P3 BOM missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("active IA-HC-002, P2 merge and P3 isolated bench wiring/BOM checks passed")
