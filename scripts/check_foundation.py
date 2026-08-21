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
    "F90 / PHYSICAL PROTOTYPE — P2 HMI LAYOUT IMPLEMENTED / MERGE APPROVAL PENDING",
    "4228a1f0346480221d0afb779907537a50c65e70",
    "IA-HC-002`: `APPROVED / ACTIVE`",
    "HC-P1-001`: `MERGED / VERIFIED`",
    "HC-P2-001`: `IMPLEMENTED / GREEN — MERGE APPROVAL PENDING`",
    "8e199b0f9ea398ab21d8ad6e6062bf7291ae6df2",
    "d2fa2a91b957362b0367d9f0b30f267ddcd1b784",
    "Any live KVK integration remains blocked",
]:
    if marker not in current:
        errors.append(f"CURRENT_STATE missing marker: {marker}")

trace = Path("docs/traceability/HC-TRACE-001_Traceability.md").read_text(encoding="utf-8")
for marker in [
    "P2 IMPLEMENTED / MERGE APPROVAL PENDING",
    "8e199b0f9ea398ab21d8ad6e6062bf7291ae6df2",
    "d2fa2a91b957362b0367d9f0b30f267ddcd1b784",
    "10.1-inch, 1024×600 target layout",
]:
    if marker not in trace:
        errors.append(f"traceability missing marker: {marker}")

closure = Path("docs/closure/HC-BENCH-MVP-CLOSURE-001.md").read_text(encoding="utf-8")
if "CLOSED / IMPLEMENTED / VERIFIED / RECONCILED" not in closure:
    errors.append("closure record must be reconciled closed")

ia2 = Path("governance/IA-HC-002_Physical_Prototype_Authority_v0.1.md").read_text(encoding="utf-8")
for marker in [
    "APPROVED / ACTIVE",
    "3eb278f7a480734045027393a53a76f6cdc03f03",
    "any electrical connection to the real KVK 801-1",
    "Fail-closed rule",
]:
    if marker not in ia2:
        errors.append(f"IA-HC-002 missing marker: {marker}")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("bench MVP closure, active IA-HC-002 and HC-P2 governance checks passed")
