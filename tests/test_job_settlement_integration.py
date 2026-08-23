from pathlib import Path
from tempfile import TemporaryDirectory
import importlib
import unittest


def require_symbol(case: unittest.TestCase, symbol: str):
    try:
        module = importlib.import_module("hoofcare.integration.job_settlement")
    except ModuleNotFoundError:
        case.fail("hoofcare.integration.job_settlement must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobSettlementIntegrationTests(unittest.TestCase):
    def test_restart_preserves_counts_materials_total_and_pdf(self):
        scenario = require_symbol(self, "SyntheticJobSettlementScenario")
        with TemporaryDirectory() as directory:
            result = scenario(Path(directory)).run()
        self.assertEqual(result.completed_cows, 2)
        self.assertEqual(result.block_quantity, "2")
        self.assertEqual(result.total_net_grosz, 12200)
        self.assertFalse(result.work_prices_visible)
        self.assertEqual(result.total_label, "RAZEM NETTO: 122,00 zł")
        self.assertTrue(result.restart_consistent)
        self.assertTrue(result.pdf_bytes.startswith(b"%PDF-1.4\n"))

    def test_s1_requirements_map_to_exact_evidence(self):
        matrix = Path(
            "docs/traceability/HC-REQ-TRACE-001_Requirement_Level_Matrix_v0.1.md"
        ).read_text(encoding="utf-8")
        for requirement in (
            "REQ-HC-JOB-STAT-S1-001",
            "REQ-HC-JOB-STAT-S1-002",
            "REQ-HC-JOB-STAT-S1-003",
            "REQ-HC-JOB-STAT-S1-004",
            "REQ-HC-JOB-CLOSE-S1-001",
            "REQ-HC-JOB-CLOSE-S1-002",
            "REQ-HC-JOB-CLOSE-S1-003",
            "REQ-HC-JOB-CLOSE-S1-004",
        ):
            self.assertIn(requirement, matrix)
        self.assertIn("test_restart_preserves_counts_materials_total_and_pdf", matrix)


if __name__ == "__main__":
    unittest.main()
