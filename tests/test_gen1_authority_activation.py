from pathlib import Path
import unittest


class Generation1AuthorityActivationTests(unittest.TestCase):
    def test_activation_record_binds_verified_pr101_evidence(self):
        path = Path("governance/HC-IA-HC-008-ACTIVATION-001.md")
        self.assertTrue(path.is_file(), "IA-HC-008 activation record must exist")
        text = path.read_text(encoding="utf-8")
        self.assertIn("f18df0d37df6ff241696822758e14f795107eddd", text)
        self.assertIn("eb41f067d2c0c2c4eeba98c9d8ab4cdae598c361", text)
        self.assertIn("b25b5ff8a12f2aca37d109a72beaded3130e20ba", text)
        self.assertIn("RUNTIME NOT STARTED", text)


if __name__ == "__main__":
    unittest.main()
