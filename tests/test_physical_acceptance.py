from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from hoofcare.physical.acceptance import PhysicalPrototypeAcceptance


class PhysicalPrototypeAcceptanceTests(unittest.TestCase):
    def test_physical_prototype_acceptance_passes_end_to_end(self) -> None:
        with TemporaryDirectory() as tmp:
            result = PhysicalPrototypeAcceptance.synthetic(Path(tmp)).run()

        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.checks["screen_layout"], "PASS")
        self.assertEqual(result.checks["navigation"], "PASS")
        self.assertEqual(result.checks["persistence_restart"], "PASS")
        self.assertEqual(result.checks["local_report"], "PASS")
        self.assertEqual(result.checks["synthetic_only"], "PASS")
        self.assertEqual(result.checks["no_kvk_connection"], "PASS")
        self.assertEqual(result.checks["no_machine_control_surface"], "PASS")
        self.assertTrue(result.report_pdf.startswith(b"%PDF-1.4"))

    def test_physical_prototype_acceptance_rejects_machine_control_action(self) -> None:
        with TemporaryDirectory() as tmp:
            acceptance = PhysicalPrototypeAcceptance.synthetic(Path(tmp))
            with self.assertRaisesRegex(ValueError, "machine-control"):
                acceptance.assert_action_allowed("plc_write")

    def test_physical_prototype_acceptance_is_not_field_acceptance(self) -> None:
        with TemporaryDirectory() as tmp:
            result = PhysicalPrototypeAcceptance.synthetic(Path(tmp)).run()

        self.assertFalse(result.field_kvk_verified)
        self.assertFalse(result.real_farm_data_used)
        self.assertFalse(result.deployment_ready)


if __name__ == "__main__":
    unittest.main()
