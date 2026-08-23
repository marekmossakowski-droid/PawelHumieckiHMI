import importlib
import unittest

try:
    from tests.job_fixtures import completed_session, open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import completed_session, open_job_fixture


def require_module(case: unittest.TestCase, module_name: str):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        case.fail(f"{module_name} must exist")


class JobMenuTests(unittest.TestCase):
    def setUp(self):
        module = require_module(self, "hoofcare.hmi.job_menu")
        self.JobScreenStage = getattr(module, "JobScreenStage")
        self.job_menu_view = getattr(module, "job_menu_view")

    def test_pawel_sees_prices_without_owner_pin_at_open_and_correction(self):
        job = open_job_fixture()

        opened = self.job_menu_view(job, self.JobScreenStage.OPEN)
        correction = self.job_menu_view(
            job,
            self.JobScreenStage.PRICE_CORRECTION,
        )

        self.assertTrue(opened.prices_visible)
        self.assertTrue(correction.prices_visible)
        self.assertTrue(correction.price_edit_allowed)
        self.assertNotIn("unlock_owner", correction.actions)

    def test_work_screen_hides_prices_and_first_cow_removes_edit_action(self):
        job = open_job_fixture()
        treatment = self.job_menu_view(job, self.JobScreenStage.TREATMENT)
        frozen = job.record_completed_session(
            completed_session("TEST-COW-1", "TEST-SESSION-1"),
            "TEST-COMPLETE-1",
        )
        summary = self.job_menu_view(frozen, self.JobScreenStage.SUMMARY)

        self.assertFalse(treatment.prices_visible)
        self.assertFalse(summary.price_edit_allowed)
        self.assertNotIn("correct_price", summary.actions)


class Gl100eJobLayoutTests(unittest.TestCase):
    def test_profile_keeps_touch_targets_at_least_64_pixels(self):
        module = require_module(self, "hoofcare.physical.job_layout")
        layout = getattr(module, "Gl100eJobLayout").default()

        self.assertEqual((layout.width_px, layout.height_px), (1024, 600))
        self.assertTrue(layout.touch_targets)
        self.assertTrue(
            all(
                target.width >= 64 and target.height >= 64
                for target in layout.touch_targets
            )
        )


if __name__ == "__main__":
    unittest.main()
