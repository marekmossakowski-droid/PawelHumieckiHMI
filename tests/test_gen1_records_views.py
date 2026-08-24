from dataclasses import fields
from datetime import date, datetime, timezone
from decimal import Decimal
import importlib
import unittest

from hoofcare.application.job_statistics import (
    JobStatistics,
    MaterialQuantity,
    StatisticsFilter,
)
from hoofcare.domain.jobs import JobState, SettlementLine
from hoofcare.hmi.gen1.shell import OwnerGateState, unlock_owner_zone
from hoofcare.reporting.settlement import SettlementDocument

try:
    from tests.job_fixtures import closed_job_fixture, open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import closed_job_fixture, open_job_fixture


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
    def setUp(self):
        self.module = importlib.import_module("hoofcare.hmi.gen1.records_views")

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

    def test_work_projection_has_counts_and_materials_but_no_money_field(self):
        view = self.module.project_work_statistics(statistics_fixture())

        self.assertEqual((view.completed_cows, view.open_jobs, view.closed_jobs), (3, 1, 1))
        self.assertEqual(view.material_quantities[0].code, "BLOCK")
        self.assertFalse(any(field.name.endswith("_grosz") for field in fields(type(view))))

    def test_settlement_uses_stored_lines_and_existing_pdf_renderer(self):
        document = settlement_document_fixture()
        view = self.module.project_settlement(document)

        self.assertIs(view.lines, document.lines)
        self.assertTrue(view.prices_visible)
        self.assertEqual(view.disclaimer, "DOKUMENT ROZLICZENIOWY — NIE JEST FAKTURĄ")
        pdf = self.module.render_settlement_pdf(document)
        self.assertTrue(pdf.startswith(b"%PDF-"))
        self.assertIn(b"RAZEM NETTO: 122,00 zl", pdf)

    def test_inconsistent_settlement_fails_closed(self):
        document = settlement_document_fixture()
        inconsistent = SettlementDocument(
            document.settlement_id,
            document.job_id,
            document.farm_id,
            document.operator_id,
            document.generated_at_iso,
            document.lines,
            1,
        )

        with self.assertRaisesRegex(ValueError, "settlement total is inconsistent"):
            self.module.project_settlement(inconsistent)

    def test_history_filters_are_inclusive_and_local(self):
        opened = open_job_fixture()
        closed = closed_job_fixture()
        view = self.module.project_history(
            (opened, closed),
            StatisticsFilter(
                date(2026, 8, 23),
                date(2026, 8, 23),
                operator_id="operator-pawel",
                farm_id="TEST-FARM-1",
                state=JobState.CLOSED,
            ),
        )

        self.assertEqual(tuple(item.job_id for item in view.items), (closed.job_id,))
        self.assertTrue(view.local_only)
        self.assertEqual(view.primary_actions, ("open_settlement", "generate_pdf", "back"))

    def test_history_without_closed_items_does_not_offer_settlement_actions(self):
        opened = open_job_fixture()
        view = self.module.project_history(
            (opened,),
            StatisticsFilter(opened.opened_at.date(), opened.opened_at.date()),
        )

        self.assertEqual(tuple(item.job_id for item in view.items), (opened.job_id,))
        self.assertEqual(view.primary_actions, ("back",))

    def test_admin_view_exposes_only_explicit_allowlisted_capabilities(self):
        capabilities = (
            "farms.read",
            "history.read",
            "reports.generate",
            "device.control",
            "kvk.write",
            "unknown.capability",
        )
        view = self.module.project_admin_capabilities(capabilities)

        self.assertEqual(
            view.visible_actions,
            ("open_farms", "open_history", "generate_report"),
        )
        self.assertNotIn("device.control", view.capability_ids)
        self.assertFalse(any("kvk" in action.lower() for action in view.visible_actions))

    def test_owner_dashboard_requires_active_synthetic_owner_session(self):
        now = datetime(2026, 8, 24, 8, tzinfo=timezone.utc)
        active = unlock_owner_zone("123456", now, OwnerGateState("123456"))
        view = self.module.project_owner_dashboard(
            active,
            now,
            ("farms.read", "audit.read", "diagnostics.read"),
        )

        self.assertEqual(
            view.surfaces,
            ("open_farms", "open_audit", "open_diagnostics"),
        )
        self.assertEqual(view.primary_actions, ("back",))
        many_surfaces = self.module.project_owner_dashboard(
            active,
            now,
            (
                "farms.read",
                "materials.read",
                "operators.read",
                "history.read",
                "reports.generate",
                "audit.read",
                "diagnostics.read",
            ),
        )
        self.assertLessEqual(len(many_surfaces.primary_actions), 4)
        with self.assertRaisesRegex(ValueError, "active owner session is required"):
            self.module.project_owner_dashboard(
                active,
                active.expires_at,
                ("farms.read",),
            )

    def test_records_projections_reject_wrong_input_types(self):
        with self.assertRaisesRegex(ValueError, "statistics must be JobStatistics"):
            self.module.project_work_statistics(object())
        with self.assertRaisesRegex(ValueError, "document must be a SettlementDocument"):
            self.module.project_settlement(object())
        with self.assertRaisesRegex(ValueError, "jobs must be an immutable tuple"):
            self.module.project_history([], StatisticsFilter(date.today(), date.today()))


if __name__ == "__main__":
    unittest.main()
