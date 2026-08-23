from datetime import datetime, timezone
import importlib
import unittest

try:
    from tests.job_fixtures import closed_job_fixture, open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import closed_job_fixture, open_job_fixture


def require_symbol(case: unittest.TestCase, symbol: str):
    try:
        module = importlib.import_module("hoofcare.reporting.settlement")
    except ModuleNotFoundError:
        case.fail("hoofcare.reporting.settlement must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobSettlementReportTests(unittest.TestCase):
    def setUp(self):
        self.SettlementDocument = require_symbol(self, "SettlementDocument")
        self.format_pln = require_symbol(self, "format_pln")

    def test_closed_job_uses_stored_settlement_lines_and_total(self):
        job = closed_job_fixture()
        document = self.SettlementDocument.from_closed_job(
            job, datetime(2026, 8, 23, 19, tzinfo=timezone.utc)
        )
        self.assertEqual(document.settlement_id, "TEST-JOB-1-SETTLEMENT-1")
        self.assertEqual(document.total_net_grosz, 155600)
        self.assertEqual(tuple(line.code for line in document.lines), ("COW", "BLOCK"))
        self.assertEqual(document.disclaimer, "DOKUMENT ROZLICZENIOWY — NIE JEST FAKTURĄ")

    def test_pdf_is_deterministic_local_summary_not_invoice(self):
        document = self.SettlementDocument.from_closed_job(
            closed_job_fixture(), datetime(2026, 8, 23, 19, tzinfo=timezone.utc)
        )
        first = document.render_pdf()
        second = document.render_pdf()
        self.assertEqual(first, second)
        self.assertTrue(first.startswith(b"%PDF-1.4\n"))
        self.assertIn(b"RAZEM NETTO: 1 556,00 zl", first)
        self.assertIn(b"NIE JEST FAKTURA", first)
        self.assertNotIn(b"VAT", first)

    def test_open_job_and_naive_generation_time_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "closed job"):
            self.SettlementDocument.from_closed_job(
                open_job_fixture(), datetime(2026, 8, 23, 19, tzinfo=timezone.utc)
            )
        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            self.SettlementDocument.from_closed_job(
                closed_job_fixture(), datetime(2026, 8, 23, 19)
            )

    def test_pln_format_uses_integer_grosz(self):
        self.assertEqual(self.format_pln(155600), "1 556,00 zł")
        with self.assertRaisesRegex(ValueError, "integer grosz"):
            self.format_pln(12.5)


if __name__ == "__main__":
    unittest.main()
