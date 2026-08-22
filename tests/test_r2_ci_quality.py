import unittest
from pathlib import Path


class R2CIQualityTests(unittest.TestCase):
    def test_runtime_ci_runs_on_main_and_has_static_and_coverage_checks(self):
        workflow = Path('.github/workflows/runtime-ci.yml').read_text(encoding='utf-8')
        self.assertIn('- main', workflow)
        self.assertIn('python -m compileall -q src tests scripts', workflow)
        self.assertIn('python scripts/run_coverage.py', workflow)

    def test_docs_ci_runs_semantic_governance_checker(self):
        workflow = Path('.github/workflows/docs-ci.yml').read_text(encoding='utf-8')
        self.assertIn('python scripts/check_semantic_governance.py', workflow)

    def test_semantic_governance_checker_exists(self):
        self.assertTrue(Path('scripts/check_semantic_governance.py').is_file())

    def test_coverage_runner_exists(self):
        self.assertTrue(Path('scripts/run_coverage.py').is_file())


if __name__ == '__main__':
    unittest.main()
