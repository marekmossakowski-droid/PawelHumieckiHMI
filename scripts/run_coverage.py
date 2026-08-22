from __future__ import annotations

from pathlib import Path
import sys
import trace
import unittest


def main() -> int:
    suite = unittest.defaultTestLoader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=1)
    tracer = trace.Trace(count=True, trace=False, ignoredirs=[sys.prefix, sys.exec_prefix])
    result = tracer.runfunc(runner.run, suite)

    coverdir = Path(".coverage-trace")
    coverdir.mkdir(exist_ok=True)
    tracer.results().write_results(show_missing=True, summary=True, coverdir=str(coverdir))

    if not result.wasSuccessful():
        return 1
    print(f"coverage artifacts: {coverdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
