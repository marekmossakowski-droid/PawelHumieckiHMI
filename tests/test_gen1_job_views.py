from dataclasses import fields
from datetime import date
from decimal import Decimal
import importlib
import unittest

from hoofcare.application.job_statistics import StatisticsFilter, derive_job_statistics
from hoofcare.domain.jobs import Job, JobPricingSnapshot, MaterialRate

try:
    from tests.job_fixtures import completed_session, open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import completed_session, open_job_fixture


def require_symbol(case: unittest.TestCase, symbol: str):
    try:
        module = importlib.import_module("hoofcare.hmi.gen1.job_views")
    except ModuleNotFoundError:
        case.fail("hoofcare.hmi.gen1.job_views must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


def active_job_fixture(*, material_quantity: Decimal = Decimal("2")):
    job = open_job_fixture()
    for index in range(1, 3):
        job = job.record_completed_session(
            completed_session(f"TEST-COW-{index}", f"TEST-SESSION-{index}"),
            f"TEST-COMPLETION-{index}",
        )
    return job.record_material(
        "TEST-MATERIAL-1",
        "TEST-SESSION-1",
        "BLOCK",
        material_quantity,
    )


def statistics_for(job):
    return derive_job_statistics(
        (job,),
        StatisticsFilter(date(2026, 8, 23), date(2026, 8, 23)),
    )


class Gen1JobViewsTests(unittest.TestCase):
    def setUp(self):
        self.JobOpeningView = require_symbol(self, "JobOpeningView")
        self.ActiveJobView = require_symbol(self, "ActiveJobView")
        self.project_job_opening = require_symbol(self, "project_job_opening")
        self.project_active_job = require_symbol(self, "project_active_job")

    def test_job_opening_exposes_stored_snapshot_and_operator_actions(self):
        job = open_job_fixture()

        view = self.project_job_opening(job)

        self.assertIs(view.pricing, job.pricing)
        self.assertEqual(view.pricing_version, 1)
        self.assertEqual(
            (view.job_id, view.farm_id, view.operator_id, view.planned_cows),
            ("TEST-JOB-1", "TEST-FARM-1", "operator-pawel", 40),
        )
        self.assertTrue(view.prices_visible)
        self.assertTrue(view.price_edit_allowed)
        self.assertEqual(view.actions, ("set_prices", "open_job"))
        self.assertNotIn("unlock_owner", view.actions)

    def test_first_completed_cow_removes_set_prices_from_opening_projection(self):
        job = open_job_fixture().record_completed_session(
            completed_session("TEST-COW-1", "TEST-SESSION-1"),
            "TEST-COMPLETION-1",
        )

        view = self.project_job_opening(job)

        self.assertFalse(view.price_edit_allowed)
        self.assertNotIn("set_prices", view.actions)

    def test_active_job_hides_prices_but_shows_counts_and_materials(self):
        job = active_job_fixture()

        view = self.project_active_job(job=job, statistics=statistics_for(job))

        self.assertEqual(
            (view.job_id, view.farm_id, view.completed_cows, view.planned_cows),
            ("TEST-JOB-1", "TEST-FARM-1", 2, 40),
        )
        self.assertEqual(view.unfinished_sessions, 0)
        self.assertEqual(view.material_quantities[0].code, "BLOCK")
        self.assertEqual(view.material_quantities[0].quantity, Decimal("2"))
        self.assertFalse(view.prices_visible)
        self.assertEqual(
            view.primary_actions,
            ("new_cow", "resume_cow", "materials", "more"),
        )
        self.assertFalse(
            any(field.name.endswith("_grosz") for field in fields(self.ActiveJobView))
        )

    def test_active_projection_rejects_statistics_from_a_different_job_set(self):
        job = active_job_fixture()
        unrelated_statistics = statistics_for(
            active_job_fixture(material_quantity=Decimal("1"))
        )

        with self.assertRaisesRegex(ValueError, "statistics do not match job"):
            self.project_active_job(job, unrelated_statistics)

    def test_active_projection_rejects_matching_quantity_with_wrong_material_metadata(self):
        job = active_job_fixture()
        unrelated_job = Job.open(
            "UNRELATED-JOB",
            "UNRELATED-FARM",
            "other-operator",
            job.opened_at,
            JobPricingSnapshot(
                9999,
                (MaterialRate("BLOCK", "Inny materiał", "kg", 1, 0),),
            ),
            999,
        )
        for index in range(1, 3):
            unrelated_job = unrelated_job.record_completed_session(
                completed_session(
                    f"UNRELATED-COW-{index}",
                    f"UNRELATED-SESSION-{index}",
                ),
                f"UNRELATED-COMPLETION-{index}",
            )
        unrelated_job = unrelated_job.record_material(
            "UNRELATED-MATERIAL",
            "UNRELATED-SESSION-1",
            "BLOCK",
            Decimal("2"),
        )

        with self.assertRaisesRegex(ValueError, "statistics do not match job"):
            self.project_active_job(job, statistics_for(unrelated_job))

    def test_projections_reject_wrong_input_types(self):
        job = open_job_fixture()
        statistics = statistics_for(job)

        with self.assertRaisesRegex(ValueError, "job must be a Job"):
            self.project_job_opening(object())
        with self.assertRaisesRegex(ValueError, "statistics must be JobStatistics"):
            self.project_active_job(job, object())
        with self.assertRaisesRegex(ValueError, "job must be a Job"):
            self.project_active_job(object(), statistics)


if __name__ == "__main__":
    unittest.main()
