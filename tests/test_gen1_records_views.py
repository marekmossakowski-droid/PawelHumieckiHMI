from decimal import Decimal
import importlib
import unittest

from hoofcare.application.job_statistics import JobStatistics, MaterialQuantity
from hoofcare.domain.jobs import SettlementLine
from hoofcare.reporting.settlement import SettlementDocument


def statistics_fixture():
    return JobStatistics(
        completed_cows=3,
        additional_material_quantities=(
            MaterialQuantity("BLOCK", "szt.", 0, Decimal("2")),
        ),
        open_jobs=1,
        closed_jobs=1,
        total_net_grosz=12200,
    )


def settlement_document_fixture():
    return SettlementDocument(
        settlement_id="TEST-SETTLEMENT-1",
        job_id="TEST-JOB-1",
        farm_id="TEST-FARM-1",
        operator_id="operator-pawel",
        generated_at_iso="2026-08-24T08:00:00+00:00",
        lines=(
            SettlementLine(
                "COW",
                "Korekcja",
                Decimal("1"),
                "szt.",
                12200,
                12200,
            ),
        ),
        total_net_grosz=12200,
    )


class Gen1RecordsViewsTests(unittest.TestCase):
    def test_work_and_settlement_views_keep_money_at_the_correct_boundary(self):
        try:
            module = importlib.import_module("hoofcare.hmi.gen1.records_views")
        except ModuleNotFoundError:
            self.fail("hoofcare.hmi.gen1.records_views must exist")
        self.assertTrue(
            hasattr(module, "project_work_statistics"),
            "project_work_statistics must exist",
        )
        work = module.project_work_statistics(statistics_fixture())
        closed = module.project_settlement(settlement_document_fixture())
        self.assertFalse(work.prices_visible)
        self.assertEqual(work.money_bindings, ())
        self.assertEqual(closed.total_label, "RAZEM NETTO: 122,00 zł")


if __name__ == "__main__":
    unittest.main()
