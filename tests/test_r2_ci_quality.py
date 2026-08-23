import shutil
import subprocess
import sys
import tempfile
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

    def test_semantic_governance_checker_rejects_conflicting_ia_hc_006_status(self):
        repository_root = Path.cwd()
        checker = repository_root / 'scripts/check_semantic_governance.py'
        copied_paths = (
            Path('project_context/CURRENT_STATE.md'),
            Path('docs/traceability/HC-TRACE-001_Traceability.md'),
            Path('planning/IMP-HC-005_Wave_R2_UX_Observability_and_Engineering_Quality_v0.1.md'),
            Path('governance/IA-HC-006_Wave_R2_UX_Observability_and_Engineering_Quality_Authority_v0.1.md'),
        )

        with tempfile.TemporaryDirectory() as tmp:
            fixture_root = Path(tmp)
            for relative_path in copied_paths:
                destination = fixture_root / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(repository_root / relative_path, destination)

            authority_path = fixture_root / copied_paths[3]
            authority = authority_path.read_text(encoding='utf-8')
            authority = authority.replace(
                'APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-006-RECOVERY-ACTIVATION-001',
                'PROPOSED / NOT ACTIVE — PROJECT OWNER APPROVAL REQUIRED',
            )
            authority_path.write_text(authority, encoding='utf-8')

            current_path = fixture_root / copied_paths[0]
            current_path.write_text(
                current_path.read_text(encoding='utf-8')
                + '\n- `IA-HC-006`: `APPROVED / ACTIVE`.\n',
                encoding='utf-8',
            )
            trace_path = fixture_root / copied_paths[1]
            trace_path.write_text(
                trace_path.read_text(encoding='utf-8')
                + '\n| HC-IA-006 | Recovery authority | IA-HC-006 | APPROVED / ACTIVE |\n',
                encoding='utf-8',
            )

            result = subprocess.run(
                [sys.executable, str(checker)],
                cwd=fixture_root,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn('IA-HC-006 status conflict', result.stderr)

    def test_semantic_governance_checker_rejects_pending_ia_hc_006_after_recovery_merge(self):
        repository_root = Path.cwd()
        checker = repository_root / 'scripts/check_semantic_governance.py'
        copied_paths = (
            Path('project_context/CURRENT_STATE.md'),
            Path('docs/traceability/HC-TRACE-001_Traceability.md'),
            Path('planning/IMP-HC-005_Wave_R2_UX_Observability_and_Engineering_Quality_v0.1.md'),
            Path('governance/IA-HC-006_Wave_R2_UX_Observability_and_Engineering_Quality_Authority_v0.1.md'),
            Path('governance/HC-IA-HC-006-RECOVERY-ACTIVATION-001.md'),
        )

        with tempfile.TemporaryDirectory() as tmp:
            fixture_root = Path(tmp)
            for relative_path in copied_paths:
                destination = fixture_root / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(repository_root / relative_path, destination)

            authority_path = fixture_root / copied_paths[3]
            authority = authority_path.read_text(encoding='utf-8')
            authority = authority.replace(
                'APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-006-RECOVERY-ACTIVATION-001',
                'APPROVED / ACTIVATION PENDING CONTROLLED MERGE OF HC-IA-HC-006-RECOVERY-ACTIVATION-001',
            )
            authority_path.write_text(authority, encoding='utf-8')

            result = subprocess.run(
                [sys.executable, str(checker)],
                cwd=fixture_root,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn('IA-HC-006 status conflict', result.stderr)

    def test_semantic_governance_checker_rejects_conflicting_ia_hc_007_status(self):
        repository_root = Path.cwd()
        checker = repository_root / 'scripts/check_semantic_governance.py'
        copied_paths = (
            Path('project_context/CURRENT_STATE.md'),
            Path('docs/traceability/HC-TRACE-001_Traceability.md'),
            Path('planning/IMP-HC-005_Wave_R2_UX_Observability_and_Engineering_Quality_v0.1.md'),
            Path('governance/IA-HC-006_Wave_R2_UX_Observability_and_Engineering_Quality_Authority_v0.1.md'),
            Path('governance/HC-IA-HC-006-RECOVERY-ACTIVATION-001.md'),
            Path('docs/reconciliation/HC-R2-GOVERNANCE-POST-MERGE-RECON-001.md'),
            Path('planning/IMP-UX-HC-001_Role_Based_Menu_Job_Settlement_and_Statistics_v0.1.md'),
            Path('governance/IA-HC-007_Role_Based_Jobs_Settlement_and_Statistics_Authority_v0.1.md'),
        )

        with tempfile.TemporaryDirectory() as tmp:
            fixture_root = Path(tmp)
            for relative_path in copied_paths:
                destination = fixture_root / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(repository_root / relative_path, destination)

            plan_path = fixture_root / copied_paths[6]
            plan_path.write_text(
                plan_path.read_text(encoding='utf-8').replace(
                    'PROPOSED — PROJECT OWNER APPROVAL REQUIRED / IMPLEMENTATION BLOCKED',
                    'APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-ACTIVATION-001',
                ),
                encoding='utf-8',
            )
            current_path = fixture_root / copied_paths[0]
            current_path.write_text(
                current_path.read_text(encoding='utf-8')
                + '\n- `IA-HC-007`: `APPROVED / ACTIVE — PROJECT OWNER APPROVED VIA HC-IA-HC-007-ACTIVATION-001`.\n',
                encoding='utf-8',
            )
            trace_path = fixture_root / copied_paths[1]
            trace_path.write_text(
                trace_path.read_text(encoding='utf-8')
                + '\n| HC-IA-007 | Job settlement authority | IA-HC-007 | APPROVED / ACTIVE |\n',
                encoding='utf-8',
            )
            activation_path = fixture_root / 'governance/HC-IA-HC-007-ACTIVATION-001.md'
            activation_path.parent.mkdir(parents=True, exist_ok=True)
            activation_path.write_text(
                '# HC-IA-HC-007-ACTIVATION-001\n\n'
                'MERGED / REPOSITORY VERIFIED — IA-HC-007 PROSPECTIVELY ACTIVE\n'
                '8901922380a3ec342747088e5acccdcd4ca5b44d\n'
                '3a32e3b5b7d1f5b2693836c044ef73caa63276d3\n',
                encoding='utf-8',
            )
            reconciliation_path = fixture_root / 'docs/reconciliation/HC-UX-HC-001-POST-MERGE-RECON-001.md'
            reconciliation_path.parent.mkdir(parents=True, exist_ok=True)
            reconciliation_path.write_text(
                '# HC-UX-HC-001-POST-MERGE-RECON-001\n\n'
                'REPOSITORY VERIFIED / IA-HC-007 PROSPECTIVELY ACTIVE\n'
                '3a32e3b5b7d1f5b2693836c044ef73caa63276d3\n',
                encoding='utf-8',
            )

            result = subprocess.run(
                [sys.executable, str(checker)],
                cwd=fixture_root,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn('IA-HC-007 status conflict', result.stderr)

    def test_coverage_runner_exists(self):
        self.assertTrue(Path('scripts/run_coverage.py').is_file())


if __name__ == '__main__':
    unittest.main()
