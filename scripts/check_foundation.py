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
    if "IA-HC-001`: proposed; NOT ACTIVE" not in text:
        errors.append("CURRENT_STATE must keep IA-HC-001 proposed and NOT ACTIVE before Project Owner approval")
    if "Runtime implementation authority: NOT ESTABLISHED" not in text:
        errors.append("CURRENT_STATE must state that runtime implementation authority is not established")

if errors:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)

print("foundation governance checks passed")
