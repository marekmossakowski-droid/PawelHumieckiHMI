import importlib
import unittest


class Generation1CompleteWorkflowIntegrationTests(unittest.TestCase):
    def test_complete_generation_1_workflow_survives_restart(self):
        try:
            module = importlib.import_module("hoofcare.hmi.gen1.integration")
        except ModuleNotFoundError:
            module = None

        self.assertIsNotNone(
            module,
            "hoofcare.hmi.gen1.integration with run_complete_gen1_synthetic_scenario must exist",
        )
        self.assertTrue(
            hasattr(module, "run_complete_gen1_synthetic_scenario"),
            "run_complete_gen1_synthetic_scenario must exist",
        )

        result = module.run_complete_gen1_synthetic_scenario()
        self.assertEqual(result.completed_cows, 2)
        self.assertEqual(result.total_label, "RAZEM NETTO: 122,00 zł")
        self.assertTrue(result.prices_hidden_during_treatment)
        self.assertTrue(result.owner_zone_expired_after_idle)
        self.assertEqual(result.dtools_manifest_status, "VALIDATED_OFFLINE")


if __name__ == "__main__":
    unittest.main()
