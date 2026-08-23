from pathlib import Path
import unittest


class StatisticsAuthorityActivationTests(unittest.TestCase):
    def test_activation_record_binds_verified_pr94_evidence(self):
        path = Path("governance/HC-IA-HC-007-S1-ACTIVATION-001.md")
        self.assertTrue(path.is_file(), "IA-HC-007-S1 activation record must exist")
        text = path.read_text(encoding="utf-8")
        self.assertIn("97e33d09128f13383e4a57fa2de0217bebef4b19", text)
        self.assertIn("e51bee95058c6fc4d9766af1467ac31202efc584", text)
        self.assertIn("RUNTIME NOT STARTED", text)


if __name__ == "__main__":
    unittest.main()
