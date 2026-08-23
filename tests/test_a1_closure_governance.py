from pathlib import Path
import unittest


class A1ClosureGovernanceTests(unittest.TestCase):
    def test_a1_closure_record_captures_verified_merge(self):
        path = Path("docs/closure/HC-REQ-HC-002-A1-CLOSURE-001.md")
        self.assertTrue(path.is_file(), "REQ-HC-002-A1 closure record must exist")
        text = path.read_text(encoding="utf-8")
        self.assertIn("CLOSURE READY — PROJECT OWNER MERGE REQUIRED", text)
        self.assertIn("8e2b2ed97f73d4f0c7015b189f7f9889e39df3ab", text)
        self.assertIn("5cc3f0e8c8fc3ff0181258f2610b04b207784e87", text)


if __name__ == "__main__":
    unittest.main()
