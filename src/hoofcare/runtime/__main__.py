from __future__ import annotations

import json
import sys
from pathlib import Path

from hoofcare.runtime.bench import BenchRuntimeConfig, launch_bench_runtime


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("ERROR: usage: python -m hoofcare.runtime <bench-runtime.json>", file=sys.stderr)
        return 2
    try:
        config = BenchRuntimeConfig.from_json_file(Path(args[0]))
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: bench runtime configuration invalid: {exc}", file=sys.stderr)
        return 2
    try:
        status = launch_bench_runtime(config)
    except OSError as exc:
        print(f"ERROR: bench runtime launch failed: {exc}", file=sys.stderr)
        return 3
    print(json.dumps(status, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
