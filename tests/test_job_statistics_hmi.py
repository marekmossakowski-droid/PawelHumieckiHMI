from datetime import date, datetime, timezone
import importlib
import unittest

from hoofcare.application.job_statistics import StatisticsFilter, derive_job_statistics
from hoofcare.reporting.settlement import SettlementDocument

try:
    from tests.job_fixtures import closed_job_fixture, open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import closed_job_fixture, open_job_fixture


def require_symbol(case: unittest.TestCase, symbol: str):
    module = importlib.import_module("hoofcare.hmi.job_menu")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobStatisticsHmiTests(unittest.TestCase):
    def setUp(self):
        self.daily_work_view = require_symbol(self, "daily_work_view")
        self.closed_job_summary_view = require_symbol(self, "closed_job_summary_view")

    def test_daily_work_view_shows_counts_and_materials_without_prices(self):
        stats = derive_job_statistics(
            (open_job_fixture(), closed_job_fixture()),
            StatisticsFilter(date(2026, 8, 23), date(2026, 8, 23)),
        )
        view = self.daily_work_view(stats)
        self.assertEqual((view.completed_cows, view.open_jobs, view.closed_jobs), (40, 1, 1))
        self.assertEqual(view.material_quantities[0].code, "BLOCK")
        self.assertFalse(view.prices_visible)
        self.assertNotIn("total_net_grosz", view.data_bindings)

    def test_closed_summary_exposes_stored_lines_and_dominant_total(self):
        document = SettlementDocument.from_closed_job(
            closed_job_fixture(), datetime(2026, 8, 23, 19, tzinfo=timezone.utc)
        )
        view = self.closed_job_summary_view(document)
        self.assertTrue(view.prices_visible)
        self.assertEqual(view.lines, document.lines)
        self.assertEqual(view.total_net_grosz, 155600)
        self.assertEqual(view.total_label, "RAZEM NETTO: 1 556,00 zł")
        self.assertEqual(view.actions, ("generate_settlement_pdf", "back_to_dashboard"))


if __name__ == "__main__":
    unittest.main()
