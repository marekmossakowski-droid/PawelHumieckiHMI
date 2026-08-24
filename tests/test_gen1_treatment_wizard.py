import importlib
import unittest


class Gen1TreatmentWizardTests(unittest.TestCase):
    def test_pawel_can_complete_every_required_treatment_step_without_camera(self):
        module = importlib.import_module("hoofcare.hmi.workflow")
        self.assertTrue(
            hasattr(module, "complete_synthetic_wizard"),
            "complete_synthetic_wizard must exist",
        )
        steps = tuple(step.value for step in module.complete_synthetic_wizard())
        self.assertEqual(
            steps,
            (
                "IDENTITY",
                "LIMB_CLAW",
                "ZONE_LESION",
                "TREATMENT",
                "MATERIALS",
                "FOLLOW_UP",
                "SUMMARY",
            ),
        )


if __name__ == "__main__":
    unittest.main()
